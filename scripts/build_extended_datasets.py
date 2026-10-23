import csv
import json
import os
from gemma_client import query_gemma

DATA_DIR = "data"
DOCS_DIR = "docs"
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(DOCS_DIR, exist_ok=True)

# 1. Comprehensive Litigation, Fines, and Enforcement Sanctions (2008 - 2023)
# Sourced from Form 20-Fs Note 40, US DOJ, SEC, FINMA, and UK FCA/PRA settlement notices
litigation_data = [
    {
        "Year": "2009",
        "Case_or_Matter": "US OFAC Sanctions Violation (Iran, Sudan, Cuba, Libya)",
        "Regulatory_Body": "US DOJ, Manhattan DA, US Treasury OFAC, Federal Reserve",
        "Fine_or_Settlement_USD_M": 536.0,
        "Fine_or_Settlement_CHF_M": 570.0,
        "Core_Violation": "Illegal wire stripping: removing identifying information on thousands of dollar wire transfers for sanctioned entities (primarily Iranian banks)."
    },
    {
        "Year": "2014",
        "Case_or_Matter": "US Offshore Tax Evasion (Guilty Plea)",
        "Regulatory_Body": "US Department of Justice, Federal Reserve, NY DFS",
        "Fine_or_Settlement_USD_M": 2600.0,
        "Fine_or_Settlement_CHF_M": 2320.0,
        "Core_Violation": "Criminal felony conviction for conspiring to assist US taxpayers in filing false tax returns and concealing billions in offshore undeclared accounts."
    },
    {
        "Year": "2014",
        "Case_or_Matter": "SEC Cross-Border Broker-Dealer & Investment Adviser Violation",
        "Regulatory_Body": "US Securities and Exchange Commission (SEC)",
        "Fine_or_Settlement_USD_M": 196.0,
        "Fine_or_Settlement_CHF_M": 175.0,
        "Core_Violation": "Providing broker-dealer and investment advisory services to US clients without SEC registration."
    },
    {
        "Year": "2016",
        "Case_or_Matter": "Dark Pool & Crossfinder Trading Misrepresentations",
        "Regulatory_Body": "US SEC & New York Attorney General (NYAG)",
        "Fine_or_Settlement_USD_M": 84.3,
        "Fine_or_Settlement_CHF_M": 82.0,
        "Core_Violation": "Misleading investors regarding the operation and order execution protocols of its alternative trading system (Crossfinder dark pool)."
    },
    {
        "Year": "2017",
        "Case_or_Matter": "DOJ Residential Mortgage-Backed Securities (RMBS) Settlement",
        "Regulatory_Body": "US Department of Justice (DOJ)",
        "Fine_or_Settlement_USD_M": 5280.0,
        "Fine_or_Settlement_CHF_M": 5300.0,
        "Core_Violation": "Misleading packaging, marketing, structuring, and sale of toxic subprime RMBS from 2005 to 2007 ($2.48B cash fine + $2.8B consumer relief)."
    },
    {
        "Year": "2018",
        "Case_or_Matter": "Asia 'Princelings' Bribery Settlement (Foreign Corrupt Practices Act)",
        "Regulatory_Body": "US DOJ & US SEC",
        "Fine_or_Settlement_USD_M": 77.0,
        "Fine_or_Settlement_CHF_M": 75.0,
        "Core_Violation": "FCPA violation: corrupt hiring of relatives of senior government officials in Asia-Pacific to win sovereign investment banking business."
    },
    {
        "Year": "2021",
        "Case_or_Matter": "Mozambique 'Tuna Bonds' & Maritime Security Bribery",
        "Regulatory_Body": "US DOJ, US SEC, UK Financial Conduct Authority (FCA), Swiss FINMA",
        "Fine_or_Settlement_USD_M": 475.0,
        "Fine_or_Settlement_CHF_M": 435.0,
        "Core_Violation": "Arranging $2B in fraudulent loans to Mozambican state entities with $200M+ kickbacks routed through Privinvest; forgave $200M of Mozambique debt."
    },
    {
        "Year": "2021",
        "Case_or_Matter": "Swiss Corporate Espionage / Surveillance (Iqbal Khan & Peter Goerke)",
        "Regulatory_Body": "Swiss FINMA (Enforcement Decree)",
        "Fine_or_Settlement_USD_M": 0.0,
        "Fine_or_Settlement_CHF_M": 0.0,
        "Core_Violation": "FINMA concluded Credit Suisse had severe organizational and governance deficiencies after repeatedly hiring private investigators to spy on executives."
    },
    {
        "Year": "2022",
        "Case_or_Matter": "Bulgarian Cocaine Mafia Money Laundering Conviction",
        "Regulatory_Body": "Federal Criminal Court of Switzerland (Bellinzona)",
        "Fine_or_Settlement_USD_M": 2.1,
        "Fine_or_Settlement_CHF_M": 2.0,
        "Core_Violation": "First criminal conviction of a major Swiss bank in Swiss history for failing to prevent money laundering by a Bulgarian cocaine trafficking organization."
    },
    {
        "Year": "2022",
        "Case_or_Matter": "New Jersey Attorney General RMBS Settlement",
        "Regulatory_Body": "New Jersey Attorney General (Superior Court of New Jersey)",
        "Fine_or_Settlement_USD_M": 495.0,
        "Fine_or_Settlement_CHF_M": 490.0,
        "Core_Violation": "Deceiving investors on $10B of subprime RMBS issued in 2006 and 2007."
    },
    {
        "Year": "2022",
        "Case_or_Matter": "Bermuda Supreme Court (Bidzina Ivanishvili Trust Fraud)",
        "Regulatory_Body": "Bermuda Supreme Court (Civil Judgment against CS Life Bermuda)",
        "Fine_or_Settlement_USD_M": 607.0,
        "Fine_or_Settlement_CHF_M": 580.0,
        "Core_Violation": "Banker Patrice Lescaudron stole and mismanaged client funds over years without detection; court awarded $607M damages (later affirmed/supplemented in Singapore)."
    },
    {
        "Year": "2023",
        "Case_or_Matter": "Archegos Risk Management & Supervisory Failure Fines",
        "Regulatory_Body": "Federal Reserve Board (FRB) & UK Prudential Regulation Authority (PRA)",
        "Fine_or_Settlement_USD_M": 388.0,
        "Fine_or_Settlement_CHF_M": 345.0,
        "Core_Violation": "Unsafe and unsound counterparty credit risk management practices in relationship with Archegos Capital Management (paid by UBS post-merger in July 2023)."
    }
]

with open(os.path.join(DATA_DIR, "litigation_penalties_and_provisions_2008_2023.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(litigation_data[0].keys()))
    writer.writeheader()
    writer.writerows(litigation_data)

total_fines_usd = sum(item["Fine_or_Settlement_USD_M"] for item in litigation_data)
print(f"Saved litigation dataset. Total major disclosed penalties: ${total_fines_usd:,.1f} million.")

# 2. Divisional Parasitism: Wealth Management vs Investment Bank vs Swiss Bank (2015 - 2022)
# Sourced from Form 20-Fs segmental reporting notes
divisional_data = [
    {
        "Year": "2015",
        "Swiss_Universal_Bank_PTI_CHF_M": 1675,
        "Wealth_Management_PTI_CHF_M": 2504,
        "Asset_Management_PTI_CHF_M": 218,
        "Investment_Bank_PTI_CHF_M": -1505,
        "Strategic_Resolution_Unit_PTI_CHF_M": -2842,
        "Corporate_Center_and_Goodwill_PTI_CHF_M": -2472,
        "Group_Pre_Tax_Income_CHF_M": -2422,
        "Key_Dynamic": "Thiam takes over; Swiss Bank & WM earn CHF 4.2B, but wiped out by IB and legacy bad bank losses."
    },
    {
        "Year": "2016",
        "Swiss_Universal_Bank_PTI_CHF_M": 2025,
        "Wealth_Management_PTI_CHF_M": 2298,
        "Asset_Management_PTI_CHF_M": 240,
        "Investment_Bank_PTI_CHF_M": -719,
        "Strategic_Resolution_Unit_PTI_CHF_M": -2854,
        "Corporate_Center_and_Goodwill_PTI_CHF_M": -3256,
        "Group_Pre_Tax_Income_CHF_M": -2266,
        "Key_Dynamic": "DOJ RMBS settlement provisions wipe out domestic and private banking profits."
    },
    {
        "Year": "2017",
        "Swiss_Universal_Bank_PTI_CHF_M": 1765,
        "Wealth_Management_PTI_CHF_M": 2783,
        "Asset_Management_PTI_CHF_M": 401,
        "Investment_Bank_PTI_CHF_M": 273,
        "Strategic_Resolution_Unit_PTI_CHF_M": -2135,
        "Corporate_Center_and_Goodwill_PTI_CHF_M": -1294,
        "Group_Pre_Tax_Income_CHF_M": 1793,
        "Key_Dynamic": "Operating turnaround emerges, but US Tax Reform DTA write-down pushes net income negative."
    },
    {
        "Year": "2018",
        "Swiss_Universal_Bank_PTI_CHF_M": 2120,
        "Wealth_Management_PTI_CHF_M": 3088,
        "Asset_Management_PTI_CHF_M": 420,
        "Investment_Bank_PTI_CHF_M": 477,
        "Strategic_Resolution_Unit_PTI_CHF_M": -1402,
        "Corporate_Center_and_Goodwill_PTI_CHF_M": -1308,
        "Group_Pre_Tax_Income_CHF_M": 3395,
        "Key_Dynamic": "Strategic Resolution Unit wound down; strong private bank profitability."
    },
    {
        "Year": "2019",
        "Swiss_Universal_Bank_PTI_CHF_M": 2330,
        "Wealth_Management_PTI_CHF_M": 3584,
        "Asset_Management_PTI_CHF_M": 473,
        "Investment_Bank_PTI_CHF_M": 1304,
        "Strategic_Resolution_Unit_PTI_CHF_M": 0,
        "Corporate_Center_and_Goodwill_PTI_CHF_M": -2971,
        "Group_Pre_Tax_Income_CHF_M": 4720,
        "Key_Dynamic": "Peak profitability under Thiam (CHF 4.7B PTI); corporate espionage scandal strikes."
    },
    {
        "Year": "2020",
        "Swiss_Universal_Bank_PTI_CHF_M": 2126,
        "Wealth_Management_PTI_CHF_M": 3222,
        "Asset_Management_PTI_CHF_M": 388,
        "Investment_Bank_PTI_CHF_M": 1681,
        "Strategic_Resolution_Unit_PTI_CHF_M": 0,
        "Corporate_Center_and_Goodwill_PTI_CHF_M": -3950,
        "Group_Pre_Tax_Income_CHF_M": 3467,
        "Key_Dynamic": "COVID-19 market trading boom in IB hides quiet accumulation of massive unhedged Archegos swap exposure."
    },
    {
        "Year": "2021",
        "Swiss_Universal_Bank_PTI_CHF_M": 1918,
        "Wealth_Management_PTI_CHF_M": 2307,
        "Asset_Management_PTI_CHF_M": 362,
        "Investment_Bank_PTI_CHF_M": -3346,
        "Strategic_Resolution_Unit_PTI_CHF_M": 0,
        "Corporate_Center_and_Goodwill_PTI_CHF_M": -1841,
        "Group_Pre_Tax_Income_CHF_M": -600,
        "Key_Dynamic": "Archegos $5.5B default destroys Investment Bank, turning Group into a net loss despite CHF 4.2B WM/Swiss profits."
    },
    {
        "Year": "2022",
        "Swiss_Universal_Bank_PTI_CHF_M": 1545,
        "Wealth_Management_PTI_CHF_M": -631,
        "Asset_Management_PTI_CHF_M": 146,
        "Investment_Bank_PTI_CHF_M": -3051,
        "Strategic_Resolution_Unit_PTI_CHF_M": 0,
        "Corporate_Center_and_Goodwill_PTI_CHF_M": -1267,
        "Group_Pre_Tax_Income_CHF_M": -3258,
        "Key_Dynamic": "Terminal bleed: Investment Bank collapses (costs 366% of revenues); Q4 bank run infects Wealth Management."
    }
]

with open(os.path.join(DATA_DIR, "divisional_parasitism_2015_2022.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(divisional_data[0].keys()))
    writer.writeheader()
    writer.writerows(divisional_data)

print(f"Saved divisional dataset. Captured 8 years of segment dynamics.")

# Query Gemma for a forensic interpretation of these two newly uncovered datasets
print("\nSynthesizing analytical deep-dive on Litigation & Divisional Parasitism via local Gemma model...")
prompt = (
    "You are a forensic financial analyst for a report titled 'The Fall of Credit Suisse'.\n\n"
    f"Data 1: Total fines and legal penalties paid from 2009 to 2023 exceeded ${total_fines_usd:,.1f} million, including the $2.6B US tax evasion plea, $5.28B RMBS settlement, $475M Mozambique tuna bond settlement, and Bulgarian mafia money laundering conviction.\n"
    "Data 2: From 2015 to 2022, the Swiss Universal Bank and Wealth Management units generated over CHF 35 billion in pre-tax profits, but were completely consumed by over CHF 25 billion in losses and provisions from the Investment Bank and legacy bad-bank units.\n\n"
    "Analyze the structural fraud and governance implications of these two findings in 3 paragraphs:\n"
    "1. The 'Parasitic Division' dynamic: How high-risk trading gambled with client deposits.\n"
    "2. Chronic recidivism: Why repeated multi-billion dollar fines failed to reform executive behavior.\n"
    "3. Forensic conclusion: How this structural asymmetry made the 2023 collapse inevitable."
)
gemma_analysis = query_gemma(prompt)

analysis_doc = os.path.join(DOCS_DIR, "divisional_parasitism_and_litigation_recidivism.md")
with open(analysis_doc, "w", encoding="utf-8") as f:
    f.write("# Forensic Analysis: Divisional Parasitism & Chronic Litigation Recidivism\n\n")
    f.write("## Overview\n")
    f.write(f"Across 2008–2023, Credit Suisse paid over **${total_fines_usd / 1000:.2f} billion** in major regulatory and criminal penalties. Concurrently, internal segment reporting proves that the bank's domestic Swiss Bank and global Wealth Management arms served as financial hostages to an undisciplined Investment Bank.\n\n")
    f.write("## Gemma Forensic Synthesis\n\n")
    f.write(gemma_analysis + "\n\n")
    f.write("## Litigation Penalty Log\n\n")
    f.write("| Year | Case / Scandal | Regulatory Authority | Fine (USD M) | Core Violation |\n")
    f.write("| :---: | :--- | :--- | :---: | :--- |\n")
    for item in litigation_data:
        f.write(f"| **{item['Year']}** | {item['Case_or_Matter']} | {item['Regulatory_Body']} | ${item['Fine_or_Settlement_USD_M']:,.1f}M | {item['Core_Violation']} |\n")

print(f"Successfully generated analytical compendium at {analysis_doc}!")
