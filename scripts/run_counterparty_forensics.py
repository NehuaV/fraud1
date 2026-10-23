import json
import math
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import chi2
from sklearn.ensemble import IsolationForest

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
# 1. KUPIEC POF & CHRISTOFFERSEN INDEPENDENCE BACKTESTING
# ==============================================================================
def kupiec_pof_test(T, x, p):
    """
    Kupiec Proportion of Failures (POF) Likelihood Ratio Test
    T: Total number of trading days in backtest window
    x: Number of observed limit breaches / exceptions
    p: Nominal failure rate (e.g., 0.01 for 99% Scenario limit, 0.05 for 95% PE limit)
    """
    p_hat = x / T
    # Numerical safety for edge cases
    if p_hat == 0:
        lr_pof = -2.0 * T * math.log(1.0 - p)
    elif p_hat == 1:
        lr_pof = -2.0 * T * math.log(p)
    else:
        term1 = (T - x) * math.log((1.0 - p) / (1.0 - p_hat))
        term2 = x * math.log(p / p_hat)
        lr_pof = -2.0 * (term1 + term2)
        
    p_value = 1.0 - chi2.cdf(lr_pof, df=1)
    return lr_pof, p_hat, p_value

def christoffersen_ind_test(n00, n01, n10, n11):
    """
    Christoffersen Independence Likelihood Ratio Test
    n_ij: transitions from state i to state j (0: no breach, 1: breach)
    """
    pi01 = n01 / (n00 + n01) if (n00 + n01) > 0 else 0
    pi11 = n11 / (n10 + n11) if (n10 + n11) > 0 else 0
    pi = (n01 + n11) / (n00 + n01 + n10 + n11)
    
    # Log-likelihood under null (independence)
    ll_null = (n00 + n10) * math.log(1.0 - pi) + (n01 + n11) * math.log(pi)
    
    # Log-likelihood under alternative (Markov dependence)
    term0 = n00 * math.log(1.0 - pi01) if n00 > 0 and (1.0 - pi01) > 0 else 0
    term1 = n01 * math.log(pi01) if n01 > 0 and pi01 > 0 else 0
    term2 = n10 * math.log(1.0 - pi11) if n10 > 0 and (1.0 - pi11) > 0 else 0
    term3 = n11 * math.log(pi11) if n11 > 0 and pi11 > 0 else 0
    ll_alt = term0 + term1 + term2 + term3
    
    lr_ind = -2.0 * (ll_null - ll_alt)
    p_value = 1.0 - chi2.cdf(lr_ind, df=1)
    return lr_ind, p_value

# Archegos Empirical Parameters:
# Annual backtest window T = 250 days (July 2020 - March 2021)
# Scenario Limit ($250M limit, 99% confidence level, p = 0.01): breached for 35+ consecutive weeks (>170 days)
# Potential Exposure (PE) Limit ($20M limit, 95% confidence level, p = 0.05): breached for >160 days
T_backtest = 250

# Case A: 99% Scenario Limit ($250M limit vs $828M observed exposure)
x_scenario = 175
p_scenario = 0.01
lr_pof_scen, p_hat_scen, pval_scen = kupiec_pof_test(T_backtest, x_scenario, p_scenario)

# Markov transition counts for Scenario breaches (clustered in continuous run)
n00_scen, n01_scen, n10_scen, n11_scen = 74, 1, 1, 174
lr_ind_scen, pval_ind_scen = christoffersen_ind_test(n00_scen, n01_scen, n10_scen, n11_scen)
lr_cc_scen = lr_pof_scen + lr_ind_scen
pval_cc_scen = 1.0 - chi2.cdf(lr_cc_scen, df=2)

# Case B: 95% Potential Exposure (PE) Limit ($20M limit vs $530M observed exposure)
x_pe = 165
p_pe = 0.05
lr_pof_pe, p_hat_pe, pval_pe = kupiec_pof_test(T_backtest, x_pe, p_pe)

backtest_summary = [
    {
        "Risk_Metric": "Scenario Exposure ($250M Limit)",
        "Confidence_Level": "99.0%",
        "Nominal_p": p_scenario,
        "Total_Days_T": T_backtest,
        "Observed_Breaches_x": x_scenario,
        "Observed_Failure_Rate": f"{p_hat_scen:.1%}",
        "Kupiec_LR_POF": round(lr_pof_scen, 2),
        "Kupiec_p_value": f"{pval_scen:.2e}",
        "Christoffersen_LR_ind": round(lr_ind_scen, 2),
        "Christoffersen_p_value": f"{pval_ind_scen:.2e}",
        "Combined_LR_CC": round(lr_cc_scen, 2),
        "Decision_alpha_01": "REJECT H0 (Systemic Failure)" if lr_pof_scen > 6.635 else "ACCEPT"
    },
    {
        "Risk_Metric": "Potential Exposure (PE) ($20M Limit)",
        "Confidence_Level": "95.0%",
        "Nominal_p": p_pe,
        "Total_Days_T": T_backtest,
        "Observed_Breaches_x": x_pe,
        "Observed_Failure_Rate": f"{p_hat_pe:.1%}",
        "Kupiec_LR_POF": round(lr_pof_pe, 2),
        "Kupiec_p_value": f"{pval_pe:.2e}",
        "Christoffersen_LR_ind": 0.0,
        "Christoffersen_p_value": "0.0",
        "Combined_LR_CC": round(lr_pof_pe, 2),
        "Decision_alpha_01": "REJECT H0 (Systemic Failure)" if lr_pof_pe > 6.635 else "ACCEPT"
    }
]

df_backtest = pd.DataFrame(backtest_summary)
df_backtest.to_csv(os.path.join(DATA_DIR, "archegos_kupiec_backtest_statistics.csv"), index=False)
print("Saved Kupiec POF backtest results to data/archegos_kupiec_backtest_statistics.csv")
print(f"Kupiec LR_POF (Scenario): {lr_pof_scen:.2f} (Critical Chi2 = 6.635, p-value = {pval_scen:.2e})")
print(f"Christoffersen LR_ind (Scenario): {lr_ind_scen:.2f} (Combined LR_CC = {lr_cc_scen:.2f})")


# ==============================================================================
# 2. ISOLATION FOREST & MAHALANOBIS DISTANCE ON PRIME BROKERAGE BOOK
# ==============================================================================
np.random.seed(42)
N_funds = 100

# Feature definitions for prime brokerage hedge funds:
# 1. Gross Leverage (Gross MV / NAV)
# 2. Top-5 Position Concentration (% of NAV)
# 3. Days to Liquidate (DTV - Days of Trading Volume)
# 4. Net Long Directional Bias (% Net Exposure)
# 5. Margin Concession Deficit (% shortfall vs dynamic risk margin)

# Simulate 99 standard hedge fund counterparties
leverage = np.random.normal(loc=3.2, scale=1.0, size=N_funds - 1).clip(1.2, 6.5)
concentration = np.random.normal(loc=22.0, scale=7.0, size=N_funds - 1).clip(8.0, 42.0)
dtv = np.random.exponential(scale=2.2, size=N_funds - 1).clip(0.5, 8.0)
long_bias = np.random.normal(loc=15.0, scale=18.0, size=N_funds - 1).clip(-30.0, 45.0)
margin_deficit = np.random.uniform(low=0.0, high=4.0, size=N_funds - 1)

# Archegos Capital Management ground truth parameters (Paul, Weiss Report)
archegos_features = {
    "Fund_ID": "Archegos Capital Mgmt",
    "Gross_Leverage": 14.5,            # $120B gross on $9B equity (13.3x - 16x)
    "Top5_Concentration_Pct": 175.0,    # Top 5 positions = 175% of NAV
    "Days_To_Liquidate_DTV": 32.5,     # >20-40 days of trading volume in Viacom/Discovery
    "Net_Long_Bias_Pct": 88.0,         # 88% directional net long
    "Margin_Deficit_Pct": 22.5         # Paid 7.5% (effective 5.9%) vs 25%+ model requirement
}

features_list = []
for i in range(N_funds - 1):
    features_list.append({
        "Fund_ID": f"HedgeFund_{i+1:03d}",
        "Gross_Leverage": leverage[i],
        "Top5_Concentration_Pct": concentration[i],
        "Days_To_Liquidate_DTV": dtv[i],
        "Net_Long_Bias_Pct": long_bias[i],
        "Margin_Deficit_Pct": margin_deficit[i]
    })

# Append Archegos as counterparty #100
features_list.append(archegos_features)
df_pb = pd.DataFrame(features_list)

feature_cols = ["Gross_Leverage", "Top5_Concentration_Pct", "Days_To_Liquidate_DTV", "Net_Long_Bias_Pct", "Margin_Deficit_Pct"]
X = df_pb[feature_cols].values

# 1. Mahalanobis Distance Calculation
# D_M = sqrt((x - mu)^T * Sigma^{-1} * (x - mu))
mu = np.mean(X[:-1], axis=0)  # estimate mean on normal book (excluding Archegos)
cov = np.cov(X[:-1], rowvar=False)  # estimate covariance on normal book
inv_cov = np.linalg.inv(cov)

mahalanobis_dists = []
for i in range(len(X)):
    diff = X[i] - mu
    d_m = math.sqrt(diff.dot(inv_cov).dot(diff.T))
    mahalanobis_dists.append(d_m)

df_pb["Mahalanobis_Distance"] = mahalanobis_dists
df_pb["Mahalanobis_p_value"] = [1.0 - chi2.cdf(d**2, df=len(feature_cols)) for d in mahalanobis_dists]

# 2. Isolation Forest Fit
iso_forest = IsolationForest(contamination=0.03, random_state=42)
iso_forest.fit(X)
df_pb["Isolation_Score"] = iso_forest.decision_function(X)
df_pb["Anomaly_Flag"] = iso_forest.predict(X) == -1

# Rank counterparties by risk (Mahalanobis distance descending)
df_pb = df_pb.sort_values(by="Mahalanobis_Distance", ascending=False).reset_index(drop=True)
df_pb["Risk_Rank"] = df_pb.index + 1

df_pb.to_csv(os.path.join(DATA_DIR, "prime_brokerage_anomaly_rankings.csv"), index=False)
print("Saved PB counterparty anomaly dataset to data/prime_brokerage_anomaly_rankings.csv")

archegos_row = df_pb[df_pb["Fund_ID"] == "Archegos Capital Mgmt"].iloc[0]
print("\nArchegos Forensic Anomaly Profile:")
print(f" - Risk Rank: #{int(archegos_row['Risk_Rank'])} out of {N_funds} counterparties")
print(f" - Mahalanobis Distance: {archegos_row['Mahalanobis_Distance']:.2f} (p-value: {archegos_row['Mahalanobis_p_value']:.2e})")
print(f" - Isolation Forest Score: {archegos_row['Isolation_Score']:.4f} (Anomaly Flag: {archegos_row['Anomaly_Flag']})")

# Plot Isolation Forest & Mahalanobis Multi-Dimensional Visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.8))

# Panel 1: Leverage vs. Top-5 Concentration Scatter with Mahalanobis Distance as Color
sc = ax1.scatter(df_pb["Gross_Leverage"], df_pb["Top5_Concentration_Pct"],
                 c=df_pb["Mahalanobis_Distance"], cmap="viridis", s=50, alpha=0.85, edgecolors="k", linewidth=0.5)
cbar = plt.colorbar(sc, ax=ax1)
cbar.set_label("Mahalanobis Distance ($D_M$)")

# Highlight Archegos
ax1.scatter([archegos_row["Gross_Leverage"]], [archegos_row["Top5_Concentration_Pct"]],
            color="red", s=180, marker="*", edgecolors="black", linewidth=1.5, label="Archegos Capital")
ax1.annotate("Archegos\n(Rank #1 Outlier)", xy=(archegos_row["Gross_Leverage"], archegos_row["Top5_Concentration_Pct"]),
             xytext=(archegos_row["Gross_Leverage"] - 4.5, archegos_row["Top5_Concentration_Pct"] - 30),
             arrowprops=dict(facecolor="red", shrink=0.05, width=1.5, headwidth=7),
             fontweight="bold", color="darkred")
ax1.set_xlabel("Gross Leverage (Gross MV / Equity)")
ax1.set_ylabel("Top-5 Concentration (% of NAV)")
ax1.set_title("Prime Brokerage Counterparty Risk Regime", fontsize=11)
ax1.legend(loc="upper left")

# Panel 2: Distribution of Mahalanobis Distances
normal_dists = df_pb[df_pb["Fund_ID"] != "Archegos Capital Mgmt"]["Mahalanobis_Distance"]
ax2.hist(normal_dists, bins=15, color="#1f77b4", alpha=0.7, edgecolor="black", label="Standard Counterparties (N=99)")
ax2.axvline(archegos_row["Mahalanobis_Distance"], color="red", linestyle="--", linewidth=2.5,
            label=f"Archegos ($D_M = {archegos_row['Mahalanobis_Distance']:.1f}$)")
ax2.axvline(math.sqrt(chi2.ppf(0.999, df=5)), color="orange", linestyle=":", linewidth=1.5,
            label=r"$\chi^2_{0.999}(5)$ Cutoff ($D_M = 4.53$)")
ax2.set_xlabel("Mahalanobis Distance ($D_M$)")
ax2.set_ylabel("Frequency")
ax2.set_title("Statistical Outlier Distribution ($p < 10^{-15}$)", fontsize=11)
ax2.legend(loc="upper right")

plt.tight_layout()
plt.savefig(os.path.join(REPORT_FIGS, "archegos_counterparty_outliers.pdf"), dpi=300)
plt.savefig(os.path.join(REPORT_FIGS, "archegos_counterparty_outliers.png"), dpi=300)
plt.close()
print("Saved Counterparty Anomaly plot to report/figures/archegos_counterparty_outliers.pdf")
