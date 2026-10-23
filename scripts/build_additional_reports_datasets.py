import csv
import json
import os
import shutil
from gemma_client import query_gemma

DATA_DIR = "data"
DOCS_DIR = "docs"
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(DOCS_DIR, exist_ok=True)

# 1. Copy curated datasets from additional_reports/analysis/data/ into data/
src_archegos = "additional_reports/analysis/data/archegos_indicators.csv"
dst_archegos = os.path.join(DATA_DIR, "archegos_early_warning_indicators.csv")
if os.path.exists(src_archegos):
    shutil.copy(src_archegos, dst_archegos)

src_lcr = "additional_reports/analysis/data/deposit_outflow_lcr.csv"
dst_lcr = os.path.join(DATA_DIR, "snb_lcr_stress_gap_test.csv")
if os.path.exists(src_lcr):
    shutil.copy(src_lcr, dst_lcr)

src_imf = "additional_reports/analysis/data/imf_basel_core_principles.csv"
dst_imf = os.path.join(DATA_DIR, "imf_basel_core_principles_scorecard.csv")
if os.path.exists(src_imf):
    shutil.copy(src_imf, dst_imf)

# 2. Extract Greensill Multi-Obligor Programs & Overdue Future Receivables Notes
# Sourced from additional_reports/greensill/20211007-scff-portfolio-details.pdf (Page 5)
greensill_programs = [
    {
        "Program_Name": "Fairymead MOP",
        "Provides_For_Future_Receivables": "Yes",
        "Underlying_Obligors_Count": 33,
        "Total_Amount_Outstanding_USD_B": 0.44,
        "Notes_Due_Payment_Outstanding_Pct": 100.0,
        "Associated_Group": "GFG Alliance / Liberty Steel related SPV"
    },
    {
        "Program_Name": "Rasmussen MOP",
        "Provides_For_Future_Receivables": "Yes",
        "Underlying_Obligors_Count": 15,
        "Total_Amount_Outstanding_USD_B": 0.29,
        "Notes_Due_Payment_Outstanding_Pct": 100.0,
        "Associated_Group": "GFG Alliance / Liberty Steel related SPV"
    },
    {
        "Program_Name": "Liberty Commodities MOP 2018",
        "Provides_For_Future_Receivables": "No",
        "Underlying_Obligors_Count": 31,
        "Total_Amount_Outstanding_USD_B": 0.27,
        "Notes_Due_Payment_Outstanding_Pct": 100.0,
        "Associated_Group": "GFG Alliance (Sanjeev Gupta direct operating entity)"
    },
    {
        "Program_Name": "Currajong MOP",
        "Provides_For_Future_Receivables": "Yes",
        "Underlying_Obligors_Count": 17,
        "Total_Amount_Outstanding_USD_B": 0.27,
        "Notes_Due_Payment_Outstanding_Pct": 100.0,
        "Associated_Group": "Greensill Capital / GFG captive financing vehicle"
    },
    {
        "Program_Name": "Onesteel TCUK MOP 2018",
        "Provides_For_Future_Receivables": "Yes",
        "Underlying_Obligors_Count": 53,
        "Total_Amount_Outstanding_USD_B": 0.18,
        "Notes_Due_Payment_Outstanding_Pct": 100.0,
        "Associated_Group": "GFG Alliance (Whyalla / Liberty Steel Australia)"
    },
    {
        "Program_Name": "Seaview MOP",
        "Provides_For_Future_Receivables": "Yes",
        "Underlying_Obligors_Count": 11,
        "Total_Amount_Outstanding_USD_B": 0.12,
        "Notes_Due_Payment_Outstanding_Pct": 92.0,
        "Associated_Group": "Greensill Capital SPV"
    },
    {
        "Program_Name": "Rehbein MOP",
        "Provides_For_Future_Receivables": "Yes",
        "Underlying_Obligors_Count": 19,
        "Total_Amount_Outstanding_USD_B": 0.05,
        "Notes_Due_Payment_Outstanding_Pct": 92.0,
        "Associated_Group": "Greensill Capital SPV"
    }
]

with open(os.path.join(DATA_DIR, "greensill_scff_overdue_programs.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(greensill_programs[0].keys()))
    writer.writeheader()
    writer.writerows(greensill_programs)

# 3. Mozambique Hidden Debt & Forensic Audit Breakdown
# Sourced from Kroll 2017 Audit, SEC Release No. 11001, and UK High Court [2024] EWHC 1957 (Comm)
mozambique_flows = [
    {
        "Component": "Total Syndicated Loans Arranged",
        "Amount_USD_M": 2007.0,
        "Key_Entities": "ProIndicus ($622M), EMATUM ($850M), MAM ($535M)",
        "Description": "Contracted sovereign-guaranteed debt arranged by Credit Suisse and VTB."
    },
    {
        "Component": "Contractor Over-Invoicing / Inflated Assets",
        "Amount_USD_M": 713.0,
        "Key_Entities": "Privinvest (Iskandar Safa)",
        "Description": "Kroll 2017 independent forensic audit identified $713M in equipment over-pricing across patrol boats and tuna vessels."
    },
    {
        "Component": "Unaccounted Loan Proceeds",
        "Amount_USD_M": 500.0,
        "Key_Entities": "Privinvest & Mozambican State Fronts",
        "Description": "Kroll audit found $500M in loan disbursements completely unaccounted for in equipment delivery."
    },
    {
        "Component": "Bank Fees and Commissions Pocketed",
        "Amount_USD_M": 200.0,
        "Key_Entities": "Credit Suisse & VTB Capital",
        "Description": "Upfront arranger fees deducted directly from loan proceeds before disbursement."
    },
    {
        "Component": "Bribes and Kickbacks Funneled",
        "Amount_USD_M": 200.0,
        "Key_Entities": "Pearse, Singh, Subeva (CS Bankers) & Manuel Chang (Finance Minister)",
        "Description": "DOJ indictment and SEC order established $200M+ paid by Privinvest to officials and bankers."
    },
    {
        "Component": "Global Regulatory & Legal Settlement",
        "Amount_USD_M": 475.0,
        "Key_Entities": "US DOJ, SEC, UK FCA, Swiss FINMA",
        "Description": "October 2021 settlement: $175M criminal fine, $100M SEC disgorgement, $200M debt forgiveness to Mozambique."
    }
]

with open(os.path.join(DATA_DIR, "mozambique_forensic_audit_breakdown.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(mozambique_flows[0].keys()))
    writer.writeheader()
    writer.writerows(mozambique_flows)

print("Successfully compiled extended datasets from additional_reports:")
print(" - data/archegos_early_warning_indicators.csv")
print(" - data/snb_lcr_stress_gap_test.csv")
print(" - data/imf_basel_core_principles_scorecard.csv")
print(" - data/greensill_scff_overdue_programs.csv")
print(" - data/mozambique_forensic_audit_breakdown.csv")

# 4. Synthesize analytical deep dive on LCR Stress Gap & Greensill Future Receivables using Gemma
prompt = (
    "You are a Senior Bank Stress Test and Fraud Analytics Expert writing for 'The Fall of Credit Suisse'.\n\n"
    "Data 1: Swiss National Bank (SNB) Table 4 reveals that in October 2022, high-value retail deposits fell by 44% in 30 days (2.20x the 20% regulatory LCR assumption), and in March 2023, high-value retail deposits fell by 33% in just one week (1.65x the entire 30-day LCR assumption).\n"
    "Data 2: Internal Credit Suisse Asset Management portfolio details from October 2021 reveal that across its Supply Chain Finance Funds, programs explicitly backed by 'future receivables' (Fairymead, Rasmussen, Currajong) were 100% overdue and defaulted.\n\n"
    "Analyze these two findings in 3 structured paragraphs:\n"
    "1. The Regulatory Mirage of the Liquidity Coverage Ratio (LCR): Why the Basel III LCR metric failed to predict a digital-era run.\n"
    "2. Fictitious Invoicing in Greensill: How packaging unaccrued 'future claims' violated core fund accounting.\n"
    "3. Forensic Synthesis: How supervisory failure (reflected in the IMF's 8 'Materially Non-Compliant' Basel Core Principle grades for Switzerland) allowed both breakdowns to compound into the 2023 collapse."
)

print("\nSynthesizing analytical deep-dive via local Gemma model...")
gemma_res = query_gemma(prompt)

report_out = os.path.join(DOCS_DIR, "snb_lcr_failure_and_greensill_forensics.md")
with open(report_out, "w", encoding="utf-8") as f:
    f.write("# Forensic Report: SNB LCR Stress-Gap Failure & Greensill Future Receivables\n\n")
    f.write("## Overview\n")
    f.write("This compendium examines evidence from the Swiss National Bank Financial Stability Report 2024, the internal CSAM October 2021 SCFF portfolio disclosures, and the IMF Basel Core Principles scorecard.\n\n")
    f.write("## Gemma Forensic Analysis\n\n")
    f.write(gemma_res + "\n\n")
    f.write("## SNB LCR Stress-Gap Evidence (Table 4)\n\n")
    f.write("| Episode and Category | LCR Assumption | Observed 30-day Outflow | Observed / Assumed Multiple |\n")
    f.write("| :--- | :---: | :---: | :---: |\n")
    f.write("| **October 2022 - High-value retail** | 20% | **44%** | **2.20x** |\n")
    f.write("| **October 2022 - Total deposits** | 28% | **31%** | **1.11x** |\n")
    f.write("| **March 2023 - High-value retail (1 week)** | 20% (30-day) | **33% (7 days)** | **1.65x in 1 week** |\n")
    f.write("| **March 2023 - High-value retail (30 days)** | 20% | **41%** | **2.05x** |\n")
    f.write("| **March 2023 - Total deposits** | 25% | **32%** | **1.28x** |\n\n")
    f.write("## Greensill SCFF Defaulted Future Receivables Programs\n\n")
    f.write("| Program Name | Future Receivables | Obligors (#) | Amount (USD B) | Overdue (%) | Associated Entity |\n")
    f.write("| :--- | :---: | :---: | :---: | :---: | :--- |\n")
    for p in greensill_programs:
        f.write(f"| **{p['Program_Name']}** | {p['Provides_For_Future_Receivables']} | {p['Underlying_Obligors_Count']} | ${p['Total_Amount_Outstanding_USD_B']}B | **{p['Notes_Due_Payment_Outstanding_Pct']}%** | {p['Associated_Group']} |\n")

print(f"Successfully generated analytical writeup at {report_out}!")
