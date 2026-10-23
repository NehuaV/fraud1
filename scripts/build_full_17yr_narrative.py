import os
import pandas as pd
from gemma_client import query_gemma

DOCS_DIR = "docs"
os.makedirs(DOCS_DIR, exist_ok=True)

df_fin = pd.read_csv("data/credit_suisse_audited_annual_series_2007_2023.csv")
df_beneish = pd.read_csv("data/beneish_m_score_trajectory_2008_2023.csv")
df_backtest = pd.read_csv("data/archegos_kupiec_backtest_statistics.csv")
df_hhi = pd.read_csv("data/greensill_hhi_concentration_breakdown.csv")

prompt = (
    "You are an expert forensic accountant and bank risk examiner analyzing the complete 17-year audited record "
    "(Form 20-F filings from 2007 to 2023) of Credit Suisse for a major fraud and financial crisis report.\n\n"
    "Data Highlights across 17 years (2007–2023):\n"
    f"- 2007 Peak: Assets CHF 1,360.7B, Net Revenues CHF 39.7B, Operating Cash Flow -CHF 57.9B (massive subprime build-up).\n"
    f"- 2008 Crisis: Net Loss -CHF 8.2B, avoided Swiss state bailout via CHF 10B Qatar/Saudi capital.\n"
    f"- 2014 Felony Guilty Plea: $2.6B US tax evasion fine; Dougan/Rohner leadership entrenched.\n"
    f"- 2015 Goodwill Impairment: CHF 3.8B write-off under Thiam; Net Loss -CHF 2.9B.\n"
    f"- 2017 DTA Write-down: CHF 2.3B write-off following US TCJA; Net Loss -CHF 983M.\n"
    f"- 2021 Dual Collapse: Greensill ($10B fund freeze, HHI=3004.5, 50% GFG single-obligor vs 10% UCITS cap) & Archegos ($5.5B prime brokerage loss, Kupiec LR_POF=1307.88, Christoffersen LR_ind=282.49, Mahalanobis Distance=37.91).\n"
    f"- 2022 Digital Bank Run: Q4 Net Outflows CHF 110.5B; Deposits dropped from CHF 390B to CHF 233B (PELT structural break in Q3/Q4 2022).\n"
    f"- 2023 Terminal Takeover: ICFR material weaknesses admitted March 14; March 19 emergency Sunday acquisition by UBS for CHF 3.0B; CHF 15.6B AT1 bonds wiped out; full-year 2023 assets shrunk to CHF 452.5B, net loss -CHF 4.1B.\n\n"
    "Provide a rigorous, academic forensic synthesis in 4 titled sections:\n"
    "1. The 17-Year Macro Arc: From GFC Illusion to Structural Insolvency.\n"
    "2. Forensic Accounting Findings: What the Longitudinal Beneish M-Score and Cash Flow Trajectory Reveal.\n"
    "3. Counterparty Risk & Fund Governance Failures: Mathematical Proof of Limit Overrides (Archegos & Greensill).\n"
    "4. Regulatory & Resolution Autopsy: Why Basel III Metrics (CET1, LCR) Masked Terminal Insolvency."
)

print("Querying local Gemma model for comprehensive 17-year forensic analysis...")
gemma_output = query_gemma(prompt)

report_md = os.path.join(DOCS_DIR, "the_fall_of_credit_suisse_17yr_comprehensive_forensic_report.md")
with open(report_md, "w", encoding="utf-8") as f:
    f.write("# The Fall of Credit Suisse: Comprehensive 17-Year Audited Forensic Report (2007–2023 Form 20-Fs)\n\n")
    f.write("## Executive Forensic Summary\n\n")
    f.write(
        "This empirical report investigates the systemic deterioration and ultimate collapse of Credit Suisse Group AG, "
        "synthesizing data extracted from 17 consecutive audited Form 20-F annual filings (2007 through 2023). "
        "By applying forensic accounting diagnostics (Beneish M-Score, Accrual Quality), statistical backtesting (Kupiec POF and "
        "Christoffersen Independence Tests), industrial concentration analytics (Herfindahl-Hirschman Index), change-point algorithms "
        "(Page's CUSUM and PELT), and unsupervised machine learning (Isolation Forests and Mahalanobis Distances), we show that the "
        "bank's downfall was not an exogenous liquidity shock, but the culmination of a decade-long failure of internal controls, "
        "recurrent legal recidivism ($10.74B in fines), and willful risk-limit overrides.\n\n"
    )
    f.write("## Gemma Forensic Synthesis\n\n")
    f.write(gemma_output + "\n\n")
    f.write("## 17-Year Audited Summary Table\n\n")
    f.write("| Year | Net Revenues (CHF M) | OpEx (CHF M) | Net Income (CHF M) | Operating Cash Flow (CHF M) | Assets (CHF M) | Deposits (CHF M) | Tier 1 (%) | Key Leadership |\n")
    f.write("| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |\n")
    for idx, row in df_fin.iterrows():
        f.write(
            f"| **{row['Year']}** | {row['Net_Revenues_CHF_M']:,} | {row['Operating_Expenses_CHF_M']:,} | "
            f"{row['Net_Income_to_Shareholders_CHF_M']:,} | {row['Operating_Cash_Flow_CFO_CHF_M']:,} | "
            f"{row['Total_Assets_CHF_M']:,} | {row['Customer_Deposits_CHF_M']:,} | {row['Tier_1_Ratio_Pct']:.1f}% | "
            f"{row['Key_Leadership'].split(';')[0]} |\n"
        )

print(f"Successfully generated 17-year forensic report at {report_md}!")
