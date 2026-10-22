import csv
import json
import os

DATA_DIR = "data"
DOCS_DIR = "docs"
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(DOCS_DIR, exist_ok=True)

# 1. Annual Financial Trajectory (2019 - 2023)
# Sourced from 2020 Form 20-F, 2022 Form 20-F, 2023 Form 20-F, and Q1 2023 Form 6-K
annual_financials = [
    {
        "Year": "2019",
        "Net_Revenues_CHF_M": 22484,
        "Provision_for_Credit_Losses_CHF_M": 324,
        "Total_Operating_Expenses_CHF_M": 17440,
        "Pre_Tax_Income_CHF_M": 4720,
        "Net_Income_to_Shareholders_CHF_M": 3419,
        "Diluted_EPS_CHF": 1.30,
        "Customer_Deposits_CHF_B": 384.9,
        "Cash_and_Due_from_Banks_CHF_B": 105.8,
        "Total_Assets_CHF_B": 787.3,
        "Shareholders_Equity_CHF_B": 43.6,
        "CET1_Ratio_Pct": 12.7,
        "Tier_1_Leverage_Ratio_Pct": 5.5,
    },
    {
        "Year": "2020",
        "Net_Revenues_CHF_M": 22389,
        "Provision_for_Credit_Losses_CHF_M": 1096,
        "Total_Operating_Expenses_CHF_M": 17826,
        "Pre_Tax_Income_CHF_M": 3467,
        "Net_Income_to_Shareholders_CHF_M": 2669,
        "Diluted_EPS_CHF": 0.99,
        "Customer_Deposits_CHF_B": 390.9,
        "Cash_and_Due_from_Banks_CHF_B": 159.4,
        "Total_Assets_CHF_B": 805.8,
        "Shareholders_Equity_CHF_B": 42.7,
        "CET1_Ratio_Pct": 12.9,
        "Tier_1_Leverage_Ratio_Pct": 6.4,
    },
    {
        "Year": "2021",
        "Net_Revenues_CHF_M": 22696,
        "Provision_for_Credit_Losses_CHF_M": 4205,
        "Total_Operating_Expenses_CHF_M": 19091,
        "Pre_Tax_Income_CHF_M": -600,
        "Net_Income_to_Shareholders_CHF_M": -1650,
        "Diluted_EPS_CHF": -0.63,
        "Customer_Deposits_CHF_B": 392.8,
        "Cash_and_Due_from_Banks_CHF_B": 164.8,
        "Total_Assets_CHF_B": 755.8,
        "Shareholders_Equity_CHF_B": 44.0,
        "CET1_Ratio_Pct": 14.4,
        "Tier_1_Leverage_Ratio_Pct": 6.1,
    },
    {
        "Year": "2022",
        "Net_Revenues_CHF_M": 14921,
        "Provision_for_Credit_Losses_CHF_M": 16,
        "Total_Operating_Expenses_CHF_M": 18163,
        "Pre_Tax_Income_CHF_M": -3258,
        "Net_Income_to_Shareholders_CHF_M": -7293,
        "Diluted_EPS_CHF": -2.55,
        "Customer_Deposits_CHF_B": 233.2,
        "Cash_and_Due_from_Banks_CHF_B": 68.5,
        "Total_Assets_CHF_B": 531.4,
        "Shareholders_Equity_CHF_B": 45.1,
        "CET1_Ratio_Pct": 14.1,
        "Tier_1_Leverage_Ratio_Pct": 7.7,
    },
    {
        "Year": "1Q23 (Annualized/Actual)",
        "Net_Revenues_CHF_M": 18467,  # Includes CHF 15,007M AT1 wipeout gain
        "Provision_for_Credit_Losses_CHF_M": 83,
        "Total_Operating_Expenses_CHF_M": 5620,
        "Pre_Tax_Income_CHF_M": 12764,
        "Net_Income_to_Shareholders_CHF_M": 12432,
        "Diluted_EPS_CHF": 3.12,
        "Customer_Deposits_CHF_B": 166.2,
        "Cash_and_Due_from_Banks_CHF_B": 139.7,  # Boosted by CHF 108B SNB liquidity borrowing
        "Total_Assets_CHF_B": 516.3,
        "Shareholders_Equity_CHF_B": 53.7,
        "CET1_Ratio_Pct": 20.3,
        "Tier_1_Leverage_Ratio_Pct": 8.0,
    },
]

with open(os.path.join(DATA_DIR, "financial_trajectory_2019_2023.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(annual_financials[0].keys()))
    writer.writeheader()
    writer.writerows(annual_financials)

# 2. Quarterly Run on the Bank & Outflows (1Q22 - 1Q23)
# Sourced from quarterly earnings presentations, Form 6-Ks, and Q1 2023 report
quarterly_run = [
    {
        "Quarter": "1Q22",
        "Group_NNA_CHF_B": -2.4,
        "Wealth_Mgmt_NNA_CHF_B": 4.8,
        "Swiss_Bank_NNA_CHF_B": 1.2,
        "Asset_Mgmt_NNA_CHF_B": -8.4,
        "Customer_Deposits_CHF_B": 384.6,
        "Total_AuM_CHF_B": 1555.0,
        "WM_AuM_CHF_B": 707.0,
        "Average_Daily_LCR_Pct": 178,
    },
    {
        "Quarter": "2Q22",
        "Group_NNA_CHF_B": -7.7,
        "Wealth_Mgmt_NNA_CHF_B": -1.4,
        "Swiss_Bank_NNA_CHF_B": -0.1,
        "Asset_Mgmt_NNA_CHF_B": -6.2,
        "Customer_Deposits_CHF_B": 371.8,
        "Total_AuM_CHF_B": 1454.0,
        "WM_AuM_CHF_B": 662.0,
        "Average_Daily_LCR_Pct": 191,
    },
    {
        "Quarter": "3Q22",
        "Group_NNA_CHF_B": -12.9,
        "Wealth_Mgmt_NNA_CHF_B": -6.4,
        "Swiss_Bank_NNA_CHF_B": -1.5,
        "Asset_Mgmt_NNA_CHF_B": -4.2,
        "Customer_Deposits_CHF_B": 361.0,
        "Total_AuM_CHF_B": 1401.0,
        "WM_AuM_CHF_B": 635.0,
        "Average_Daily_LCR_Pct": 192,
    },
    {
        "Quarter": "4Q22",
        "Group_NNA_CHF_B": -110.5,
        "Wealth_Mgmt_NNA_CHF_B": -92.7,
        "Swiss_Bank_NNA_CHF_B": -8.3,
        "Asset_Mgmt_NNA_CHF_B": -11.7,
        "Customer_Deposits_CHF_B": 233.2,
        "Total_AuM_CHF_B": 1294.0,
        "WM_AuM_CHF_B": 540.0,
        "Average_Daily_LCR_Pct": 144,
    },
    {
        "Quarter": "1Q23",
        "Group_NNA_CHF_B": -61.2,
        "Wealth_Mgmt_NNA_CHF_B": -47.1,
        "Swiss_Bank_NNA_CHF_B": -6.9,
        "Asset_Mgmt_NNA_CHF_B": -11.6,
        "Customer_Deposits_CHF_B": 166.2,
        "Total_AuM_CHF_B": 1253.0,
        "WM_AuM_CHF_B": 502.5,
        "Average_Daily_LCR_Pct": 178,  # Boosted artificially by SNB liquidity lines
    },
]

with open(os.path.join(DATA_DIR, "quarterly_run_on_the_bank_2022_2023.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(quarterly_run[0].keys()))
    writer.writeheader()
    writer.writerows(quarterly_run)

# 3. Archegos Forensic Metrics
archegos_metrics = {
    "Counterparty": "Archegos Capital Management (Sung Kook 'Bill' Hwang family office)",
    "Total_Loss_Sustained_USD": "5.5 billion (approx. CHF 4.8 billion)",
    "Default_Date": "March 25, 2021",
    "Peak_Gross_Notional_Exposure_USD": "Over 24 billion",
    "Trading_Mechanism": "Synthetic Total Return Swaps (TRS) & Contracts for Difference (CFD)",
    "Core_Concentrations": ["ViacomCBS", "Discovery", "Tencent Music", "Baidu", "GSX Techedu", "Vipshop"],
    "Paul_Weiss_Investigation": {
        "Report_Date": "July 29, 2021",
        "Pages": 181,
        "Lead_Investigators": "Brad S. Karp, Claudia Hammerman, Jessica S. Carey (Paul, Weiss)",
        "Interviews_Conducted": 80,
        "Documents_Reviewed": "Over 10 million",
        "Key_Failures_Identified": [
            "Incompetent margin management: Archegos was charged static 10% margin despite concentrated, volatile single-stock swap positions.",
            "Failure of dynamic margining: Dynamic margin framework was approved but repeatedly postponed for Archegos.",
            "Chronic limit breaches: Persistent potential exposure (PE) and scenario stress limit excesses over many months without business escalation.",
            "Siloed risk monitoring: Prime Services Risk (first line) and Credit Risk Management (second line) failed to communicate and challenge business heads.",
            "Culture of short-term revenue maximization: Prioritized prime brokerage fees over obvious tail-risk warnings.",
            "Executive accountability: Forced departure of Investment Bank CEO Brian Chin and Chief Risk Officer Lara Warner."
        ]
    }
}

with open(os.path.join(DATA_DIR, "archegos_metrics.json"), "w", encoding="utf-8") as f:
    json.dump(archegos_metrics, f, indent=2, ensure_ascii=False)

# 4. Takeover, Capital Destruction & AT1 Bail-in Terms
takeover_terms = {
    "Announcement_Date": "Sunday, March 19, 2023",
    "Effective_Merger_Date": "June 12, 2023",
    "Acquiring_Entity": "UBS Group AG",
    "Acquired_Entity": "Credit Suisse Group AG",
    "Legal_Mechanism": "Swiss Federal Council Emergency Ordinance (Articles 184 and 185 of Swiss Federal Constitution), suspending shareholder voting rights",
    "Exchange_Ratio": "1 UBS share for every 22.48 Credit Suisse shares",
    "Total_Purchase_Consideration_CHF": "3.0 billion (approx. USD 3.25 billion)",
    "Implied_Share_Price_at_Deal_CHF": 0.76,
    "Friday_Pre_Deal_Close_Price_CHF": 1.86,
    "Discount_to_Friday_Close_Pct": 59.1,
    "Peak_Share_Price_Feb_2021_CHF": 13.40,
    "Total_Market_Cap_Destruction_Pct": 94.3,
    "Saudi_National_Bank_SNB_Position": {
        "Capital_Injected_Nov_2022_CHF": "1.5 billion",
        "Stake_Percentage": "9.9%",
        "Purchase_Price_Per_Share_CHF": 3.82,
        "Implied_Value_at_Merger_CHF": "300 million",
        "Estimated_Capital_Loss_CHF": "1.2 billion (-80.1% loss in under 4 months)"
    },
    "AT1_Bail_In_Write_Down": {
        "Total_Nominal_Amount_Written_Down_CHF": "15.6 billion (approx. USD 17.0 billion)",
        "Accounting_Gain_Recognized_in_1Q23_CHF": "15.007 billion",
        "Ordering_Authority": "Swiss Financial Market Supervisory Authority (FINMA)",
        "Legal_Controversy": "Complete write-down of Tier 1 subordinated debt to zero while common equity holders received CHF 3B, upending standard creditor priority hierarchy (absolute priority rule) and sparking multi-billion dollar lawsuits in Swiss, US, and UK courts."
    },
    "Swiss_State_and_Central_Bank_Liquidity_Support": {
        "SNB_Emergency_Liquidity_Assistance_ELA_CHF": "50 billion",
        "SNB_ELA_Plus_Preferential_Bankruptcy_Status_CHF": "100 billion",
        "Public_Liquidity_Backstop_PLB_CHF": "100 billion",
        "Total_Potential_Central_Bank_Liquidity_CHF": "250 billion",
        "Actual_Peak_Drawn_Balance_as_of_March_31_2023_CHF": "108 billion",
        "Federal_Loss_Protection_Guarantee_for_UBS_CHF": "9 billion (for losses on non-core portfolio exceeding CHF 5 billion, later terminated voluntarily by UBS in August 2023)"
    }
}

with open(os.path.join(DATA_DIR, "takeover_and_at1_terms.json"), "w", encoding="utf-8") as f:
    json.dump(takeover_terms, f, indent=2, ensure_ascii=False)

print("Research datasets successfully created in /data:")
print(" - data/financial_trajectory_2019_2023.csv")
print(" - data/quarterly_run_on_the_bank_2022_2023.csv")
print(" - data/archegos_metrics.json")
print(" - data/takeover_and_at1_terms.json")
