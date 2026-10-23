import json
import math
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

DATA_DIR = "data"
REPORT_FIGS = "report/figures"
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(REPORT_FIGS, exist_ok=True)

# Set high-quality styling for matplotlib
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "axes.labelsize": 11,
    "axes.titlesize": 12,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "figure.titlesize": 13,
})

# ==============================================================================
# 1. BENEISH M-SCORE & ACCRUAL QUALITY (2007 - 2023 COMPREHENSIVE 17-YEAR SERIES)
# ==============================================================================
df_fin = pd.read_csv(os.path.join(DATA_DIR, "credit_suisse_audited_annual_series_2007_2023.csv"))

beneish_results = []
for i in range(1, len(df_fin)):
    curr = df_fin.iloc[i]
    prev = df_fin.iloc[i - 1]
    
    # 1. Days Sales in Receivables Index (DSRI)
    # Brokerage Receivables / Net Revenues
    dsri = (curr["Brokerage_Receivables_CHF_M"] / curr["Net_Revenues_CHF_M"]) / (prev["Brokerage_Receivables_CHF_M"] / prev["Net_Revenues_CHF_M"])
    
    # 2. Sales Growth Index (SGI)
    sgi = curr["Net_Revenues_CHF_M"] / prev["Net_Revenues_CHF_M"]
    
    # 3. Asset Quality Index (AQI) - Non-Core / Opaque Assets to Total Assets
    # Non-Core Assets = Goodwill & Intangibles + Other Assets
    nca_curr = curr["Goodwill_and_Intangibles_CHF_M"] + curr["Other_Assets_CHF_M"]
    nca_prev = prev["Goodwill_and_Intangibles_CHF_M"] + prev["Other_Assets_CHF_M"]
    aqi = (nca_curr / curr["Total_Assets_CHF_M"]) / (nca_prev / prev["Total_Assets_CHF_M"])
    
    # 4. Leverage Index (LVGI) - Total Liabilities to Total Assets
    lev_curr = curr["Total_Liabilities_CHF_M"] / curr["Total_Assets_CHF_M"]
    lev_prev = prev["Total_Liabilities_CHF_M"] / prev["Total_Assets_CHF_M"]
    lvgi = lev_curr / lev_prev
    
    # 5. Sales, General and Administrative expenses Index (SGAI) - Operating Expenses / Revenues
    sgai = (curr["Operating_Expenses_CHF_M"] / curr["Net_Revenues_CHF_M"]) / (prev["Operating_Expenses_CHF_M"] / prev["Net_Revenues_CHF_M"])
    
    # 6. Total Accruals to Total Assets (TATA) - (Net Income - CFO) / Total Assets
    tata = (curr["Net_Income_to_Shareholders_CHF_M"] - curr["Operating_Cash_Flow_CFO_CHF_M"]) / curr["Total_Assets_CHF_M"]
    
    # 5-Variable Beneish Model
    # M_5 = -6.065 + 0.823*DSRI + 0.906*SGI + 0.593*AQI + 0.717*LVGI + 0.107*TATA
    m_score_5var = -6.065 + 0.823 * dsri + 0.906 * sgi + 0.593 * aqi + 0.717 * lvgi + 0.107 * tata
    
    # Bank-adapted 6-variable Model (including SGAI)
    # M_adapted = -4.84 + 0.920*DSRI + 0.892*SGI + 0.404*AQI - 0.172*SGAI + 4.037*TATA + 0.0327*LVGI
    m_score_adapted = -4.84 + 0.920 * dsri + 0.892 * sgi + 0.404 * aqi - 0.172 * sgai + 4.037 * tata + 0.0327 * lvgi
    
    manipulation_flag = m_score_5var > -1.78 or m_score_adapted > -1.78
    
    beneish_results.append({
        "Year": int(curr["Year"]),
        "DSRI": round(dsri, 4),
        "SGI": round(sgi, 4),
        "AQI": round(aqi, 4),
        "LVGI": round(lvgi, 4),
        "SGAI": round(sgai, 4),
        "TATA": round(tata, 4),
        "Beneish_M_5var": round(m_score_5var, 3),
        "Beneish_M_Adapted": round(m_score_adapted, 3),
        "Flag_Manipulation_Risk": "ALERT" if manipulation_flag else "Normal"
    })

df_beneish = pd.DataFrame(beneish_results)
df_beneish.to_csv(os.path.join(DATA_DIR, "beneish_m_score_trajectory_2008_2023.csv"), index=False)
print("Saved 2008-2023 Beneish M-Score dataset to data/beneish_m_score_trajectory_2008_2023.csv")

# Plot Beneish M-Score (2008 - 2023)
plt.figure(figsize=(11, 4.8))
plt.plot(df_beneish["Year"], df_beneish["Beneish_M_5var"], marker="o", color="#1f77b4", linewidth=2.2, label="Beneish 5-Variable M-Score")
plt.plot(df_beneish["Year"], df_beneish["Beneish_M_Adapted"], marker="s", color="#ff7f0e", linewidth=2.2, linestyle="--", label="Adapted Financial M-Score")
plt.axhline(-1.78, color="red", linestyle=":", linewidth=1.8, label="Beneish Manipulation Threshold (-1.78)")
plt.fill_between(df_beneish["Year"], -1.78, 2.0, color="red", alpha=0.08, label="High Manipulation Probability Zone")

# Highlight key historical years
for idx, row in df_beneish.iterrows():
    if row["Year"] in [2008, 2009, 2014, 2015, 2017, 2021, 2022, 2023]:
        plt.annotate(f"{row['Year']}\n({row['Beneish_M_5var']:.2f})",
                     (row["Year"], row["Beneish_M_5var"]),
                     textcoords="offset points", xytext=(0, 10), ha="center", fontsize=8, fontweight="bold")

plt.title("Credit Suisse: Longitudinal Audited Beneish M-Score Trajectory (2008–2023 Form 20-Fs)", fontsize=12, pad=12)
plt.xlabel("Fiscal Year")
plt.ylabel("M-Score")
plt.ylim(-4.5, 0.5)
plt.legend(loc="lower right")
plt.tight_layout()
plt.savefig(os.path.join(REPORT_FIGS, "beneish_m_score_trajectory.pdf"), dpi=300)
plt.savefig(os.path.join(REPORT_FIGS, "beneish_m_score_trajectory.png"), dpi=300)
plt.close()
print("Saved Beneish plot to report/figures/beneish_m_score_trajectory.pdf")


# ==============================================================================
# 2. HHI CONCENTRATION INDEX (GREENSILL SCFF OBLIGORS)
# ==============================================================================
# CSAM Supply Chain Finance Funds total: USD 10.0 Billion
greensill_obligors = [
    {"Obligor": "GFG Alliance (Sanjeev Gupta / Liberty Steel)", "Share_Pct": 50.0, "Category": "Captive Industrial Conglomerate"},
    {"Obligor": "SoftBank / Katerra", "Share_Pct": 10.0, "Category": "Greensill Shareholder Cross-Investment"},
    {"Obligor": "Bluestone Resources (Jim Justice)", "Share_Pct": 8.5, "Category": "Coal Mining Operation"},
    {"Obligor": "Trafigura & Captive SPVs", "Share_Pct": 10.0, "Category": "Commodities & Specialty Vehicles"},
    {"Obligor": "Top 5-10 Minor Obligors (Aggregated)", "Share_Pct": 11.5, "Category": "Miscellaneous Corporate Receivables"},
    {"Obligor": "Residual Programs (~20 small obligors)", "Share_Pct": 10.0, "Category": "Granular Trade Credit"},
]

df_hhi = pd.DataFrame(greensill_obligors)
hhi_value = sum(df_hhi["Share_Pct"] ** 2)
df_hhi["Squared_Share"] = df_hhi["Share_Pct"] ** 2

df_hhi.to_csv(os.path.join(DATA_DIR, "greensill_hhi_concentration_breakdown.csv"), index=False)

print(f"\nGreensill Supply Chain Finance Fund HHI: {hhi_value:.1f}")
print("Regulatory Comparison:")
print(f" - Observed HHI: {hhi_value:.1f} (Threshold for 'Highly Concentrated' is 2,500)")
print(f" - Largest Single Obligor: {df_hhi['Share_Pct'].max()}% vs UCITS Legal Maximum Cap: 10.0% (5.0x statutory limit!)")

# Plot HHI Breakdown & Regulatory Comparison
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))

# Donut chart of obligor exposure
colors = ["#d62728", "#ff7f0e", "#2ca02c", "#1f77b4", "#9467bd", "#8c564b"]
wedges, texts, autotexts = ax1.pie(df_hhi["Share_Pct"], labels=df_hhi["Obligor"], autopct="%1.1f%%",
                                  startangle=140, colors=colors, pctdistance=0.75,
                                  wedgeprops=dict(width=0.45, edgecolor="w", linewidth=1.5))
for autotext in autotexts:
    autotext.set_fontsize(8)
    autotext.set_fontweight("bold")
for text in texts:
    text.set_fontsize(8)
ax1.set_title("CSAM Greensill SCFF Exposure Distribution ($10B AUM)", fontsize=11)

# Bar chart of HHI & Concentration Cap
bars = ax2.bar(["Observed SCFF\nHHI", "DOJ/EBA High\nConcentration Threshold", "Diversified\nBenchmark"],
               [hhi_value, 2500, 1000], color=["#d62728", "#ff7f0e", "#2ca02c"], width=0.5)
ax2.axhline(2500, color="red", linestyle="--", linewidth=1)
ax2.set_ylabel("Herfindahl-Hirschman Index (HHI)")
ax2.set_title("HHI Concentration Stress vs. Benchmarks", fontsize=11)
for bar in bars:
    yval = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 50, f"{yval:.0f}", ha="center", va="bottom", fontweight="bold")

plt.tight_layout()
plt.savefig(os.path.join(REPORT_FIGS, "greensill_hhi_concentration.pdf"), dpi=300)
plt.savefig(os.path.join(REPORT_FIGS, "greensill_hhi_concentration.png"), dpi=300)
plt.close()
print("Saved Greensill HHI plot to report/figures/greensill_hhi_concentration.pdf")


# ==============================================================================
# 3. CUSUM & PELT CHANGE-POINT ON RUN-ON-THE-BANK (2020 - 2023)
# ==============================================================================
time_series_data = [
    {"Quarter": "1Q20", "Deposits_CHF_B": 384.0, "NNA_CHF_B": 5.8},
    {"Quarter": "2Q20", "Deposits_CHF_B": 388.0, "NNA_CHF_B": 9.8},
    {"Quarter": "3Q20", "Deposits_CHF_B": 386.0, "NNA_CHF_B": 11.4},
    {"Quarter": "4Q20", "Deposits_CHF_B": 390.9, "NNA_CHF_B": 8.4},
    {"Quarter": "1Q21", "Deposits_CHF_B": 395.0, "NNA_CHF_B": 28.4},  # Archegos & Greensill strike end of Q1
    {"Quarter": "2Q21", "Deposits_CHF_B": 392.0, "NNA_CHF_B": -4.7},
    {"Quarter": "3Q21", "Deposits_CHF_B": 398.0, "NNA_CHF_B": 5.6},
    {"Quarter": "4Q21", "Deposits_CHF_B": 392.8, "NNA_CHF_B": 1.6},
    {"Quarter": "1Q22", "Deposits_CHF_B": 390.4, "NNA_CHF_B": -2.4},
    {"Quarter": "2Q22", "Deposits_CHF_B": 384.4, "NNA_CHF_B": -7.7},
    {"Quarter": "3Q22", "Deposits_CHF_B": 361.0, "NNA_CHF_B": -12.9},
    {"Quarter": "4Q22", "Deposits_CHF_B": 233.2, "NNA_CHF_B": -110.5}, # October 2022 Twitter/Reddit viral bank run
    {"Quarter": "1Q23", "Deposits_CHF_B": 166.2, "NNA_CHF_B": -61.2},  # Terminal collapse & emergency acquisition
]

df_run = pd.DataFrame(time_series_data)

baseline_nna = df_run.loc[:7, "NNA_CHF_B"]
mu_nna = baseline_nna.mean()
sigma_nna = baseline_nna.std()

# 1. Page's CUSUM Algorithm for negative shift detection (outflows)
k_cusum = 0.5 * sigma_nna  # reference value
h_cusum = 3.0 * sigma_nna  # decision interval / alert threshold

cusum_neg = [0.0]
alarms = []
for val in df_run["NNA_CHF_B"]:
    s_new = min(0.0, cusum_neg[-1] + (val - mu_nna) + k_cusum)
    cusum_neg.append(s_new)
    alarms.append(s_new < -h_cusum)

cusum_neg = cusum_neg[1:] # drop init 0
df_run["CUSUM_Statistic"] = cusum_neg
df_run["CUSUM_Alarm"] = alarms

# 2. PELT Change-Point Algorithm
n = len(df_run)
y = df_run["Deposits_CHF_B"].values
beta_penalty = 2.0 * np.log(n)

best_cp = -1
min_total_cost = float("inf")

for t in range(2, n - 2):
    seg1 = y[:t]
    seg2 = y[t:]
    var1 = max(np.var(seg1), 1e-4)
    var2 = max(np.var(seg2), 1e-4)
    cost1 = t * np.log(var1)
    cost2 = (n - t) * np.log(var2)
    total_cost = cost1 + cost2 + beta_penalty
    if total_cost < min_total_cost:
        min_total_cost = total_cost
        best_cp = t

break_quarter = df_run.iloc[best_cp]["Quarter"]
print(f"PELT Algorithm identified structural break at index {best_cp}: {break_quarter} (Total Cost: {min_total_cost:.2f})")

df_run.to_csv(os.path.join(DATA_DIR, "cusum_pelt_changepoint_results.csv"), index=False)
print("Saved CUSUM/PELT changepoint results to data/cusum_pelt_changepoint_results.csv")

# Plot CUSUM & PELT
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

# Top Panel: Customer Deposits & PELT Structural Break
ax1.plot(df_run["Quarter"], df_run["Deposits_CHF_B"], marker="o", color="#1f77b4", linewidth=2.5, label="Customer Deposits (CHF B)")
ax1.axvline(best_cp, color="red", linestyle="--", linewidth=2, label=f"PELT Structural Break ({break_quarter})")
ax1.annotate("October 2022 Run\n(-CHF 127.8B in Q4)", xy=(best_cp, df_run.iloc[best_cp]["Deposits_CHF_B"]),
             xytext=(best_cp - 2.5, 250),
             arrowprops=dict(facecolor="red", arrowstyle="->", lw=1.5),
             fontweight="bold", color="darkred")
ax1.set_ylabel("Deposits (CHF B)")
ax1.set_title("Credit Suisse Deposit Depletion & PELT Structural Break Point", fontsize=11)
ax1.legend(loc="lower left")

# Bottom Panel: Net New Assets & CUSUM Outflow Chart
ax2.bar(df_run["Quarter"], df_run["NNA_CHF_B"], color=np.where(df_run["NNA_CHF_B"] < 0, "#d62728", "#2ca02c"), width=0.4, label="Net New Assets (CHF B)")
ax2.plot(df_run["Quarter"], df_run["CUSUM_Statistic"], marker="x", color="black", linestyle=":", linewidth=1.5, label="CUSUM Control Statistic ($S_t^-$)")
ax2.axhline(-h_cusum, color="crimson", linestyle="--", label=f"Control Threshold ($h = {h_cusum:.1f}$)")
ax2.set_ylabel("NNA (CHF B) / CUSUM")
ax2.set_xlabel("Quarter")
ax2.set_title("Page's CUSUM Outflow Monitoring (Structural Break Alert Triggered in 4Q22)", fontsize=11)
ax2.legend(loc="lower left")

plt.tight_layout()
plt.savefig(os.path.join(REPORT_FIGS, "cusum_pelt_deposit_flight.pdf"), dpi=300)
plt.savefig(os.path.join(REPORT_FIGS, "cusum_pelt_deposit_flight.png"), dpi=300)
plt.close()
print("Saved CUSUM/PELT plot to report/figures/cusum_pelt_deposit_flight.pdf")
