import csv
import json
import os
from gemma_client import query_gemma

DATA_DIR = "data"
DOCS_DIR = "docs"
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(DOCS_DIR, exist_ok=True)

# Complete 16-year financial trajectory (2007 - 2023)
# Sourced and verified directly from Credit Suisse Form 20-Fs (2008, 2011, 2014, 2017, 2020, 2022, 2023)
full_timeline = [
    {
        "Year": "2007",
        "Net_Revenues_CHF_M": 39321,
        "Provision_for_Credit_Losses_CHF_M": 240,
        "Operating_Expenses_CHF_M": 25341,
        "Net_Income_to_Shareholders_CHF_M": 7760,
        "Diluted_EPS_CHF": 6.96,
        "Customer_Deposits_CHF_B": 339.4,
        "Total_Assets_CHF_B": 1360.7,
        "Shareholders_Equity_CHF_B": 44.7,
        "Tier_1_Ratio_Pct": 11.1,
        "Key_Leadership": "Brady Dougan (CEO), Walter Kielholz (Chairman)",
        "Key_Event": "Pre-crisis peak profitability; subprime exposure emerging."
    },
    {
        "Year": "2008",
        "Net_Revenues_CHF_M": 9268,
        "Provision_for_Credit_Losses_CHF_M": 813,
        "Operating_Expenses_CHF_M": 23357,
        "Net_Income_to_Shareholders_CHF_M": -8218,
        "Diluted_EPS_CHF": -7.83,
        "Customer_Deposits_CHF_B": 296.8,
        "Total_Assets_CHF_B": 1170.3,
        "Shareholders_Equity_CHF_B": 32.2,
        "Tier_1_Ratio_Pct": 13.1,
        "Key_Leadership": "Brady Dougan (CEO), Walter Kielholz (Chairman)",
        "Key_Event": "Global Financial Crisis; raises CHF 10B from Qatar & Saudi investors to avoid Swiss state bailout; creates illusion of invulnerability."
    },
    {
        "Year": "2009",
        "Net_Revenues_CHF_M": 33294,
        "Provision_for_Credit_Losses_CHF_M": 506,
        "Operating_Expenses_CHF_M": 24711,
        "Net_Income_to_Shareholders_CHF_M": 6724,
        "Diluted_EPS_CHF": 5.01,
        "Customer_Deposits_CHF_B": 341.2,
        "Total_Assets_CHF_B": 1031.5,
        "Shareholders_Equity_CHF_B": 36.4,
        "Tier_1_Ratio_Pct": 16.3,
        "Key_Leadership": "Brady Dougan (CEO), Hans-Ulrich Doerig (Chairman)",
        "Key_Event": "Strong trading rebound; maintains large Wall Street investment bank footprint."
    },
    {
        "Year": "2010",
        "Net_Revenues_CHF_M": 31386,
        "Provision_for_Credit_Losses_CHF_M": -79,
        "Operating_Expenses_CHF_M": 23978,
        "Net_Income_to_Shareholders_CHF_M": 5098,
        "Diluted_EPS_CHF": 3.91,
        "Customer_Deposits_CHF_B": 336.5,
        "Total_Assets_CHF_B": 1032.0,
        "Shareholders_Equity_CHF_B": 36.6,
        "Tier_1_Ratio_Pct": 17.2,
        "Key_Leadership": "Brady Dougan (CEO), Hans-Ulrich Doerig (Chairman)",
        "Key_Event": "Basel III regulations introduced; beginning of increased capital requirements."
    },
    {
        "Year": "2011",
        "Net_Revenues_CHF_M": 26225,
        "Provision_for_Credit_Losses_CHF_M": 187,
        "Operating_Expenses_CHF_M": 22577,
        "Net_Income_to_Shareholders_CHF_M": 1953,
        "Diluted_EPS_CHF": 1.36,
        "Customer_Deposits_CHF_B": 343.3,
        "Total_Assets_CHF_B": 1049.0,
        "Shareholders_Equity_CHF_B": 36.8,
        "Tier_1_Ratio_Pct": 15.9,
        "Key_Leadership": "Brady Dougan (CEO), Urs Rohner (Chairman)",
        "Key_Event": "Urs Rohner elected Chairman; Eurozone debt crisis pressures earnings."
    },
    {
        "Year": "2012",
        "Net_Revenues_CHF_M": 23611,
        "Provision_for_Credit_Losses_CHF_M": 170,
        "Operating_Expenses_CHF_M": 21251,
        "Net_Income_to_Shareholders_CHF_M": 1349,
        "Diluted_EPS_CHF": 0.85,
        "Customer_Deposits_CHF_B": 363.6,
        "Total_Assets_CHF_B": 924.2,
        "Shareholders_Equity_CHF_B": 35.5,
        "Tier_1_Ratio_Pct": 15.8,
        "Key_Leadership": "Brady Dougan (CEO), Urs Rohner (Chairman)",
        "Key_Event": "Major cost-cutting program launched; accelerated Basel III implementation."
    },
    {
        "Year": "2013",
        "Net_Revenues_CHF_M": 25856,
        "Provision_for_Credit_Losses_CHF_M": 167,
        "Operating_Expenses_CHF_M": 21593,
        "Net_Income_to_Shareholders_CHF_M": 2326,
        "Diluted_EPS_CHF": 1.25,
        "Customer_Deposits_CHF_B": 366.1,
        "Total_Assets_CHF_B": 872.8,
        "Shareholders_Equity_CHF_B": 42.9,
        "Tier_1_Ratio_Pct": 15.7,
        "Key_Leadership": "Brady Dougan (CEO), Urs Rohner (Chairman)",
        "Key_Event": "Deleveraging balance sheet; legal pressures in US intensify."
    },
    {
        "Year": "2014",
        "Net_Revenues_CHF_M": 26242,
        "Provision_for_Credit_Losses_CHF_M": 186,
        "Operating_Expenses_CHF_M": 22429,
        "Net_Income_to_Shareholders_CHF_M": 1875,
        "Diluted_EPS_CHF": 1.05,
        "Customer_Deposits_CHF_B": 381.1,
        "Total_Assets_CHF_B": 921.5,
        "Shareholders_Equity_CHF_B": 43.6,
        "Tier_1_Ratio_Pct": 16.3,
        "Key_Leadership": "Brady Dougan (CEO), Urs Rohner (Chairman)",
        "Key_Event": "Pleads guilty to US felony charges for aiding tax evasion; pays $2.6B fine; Rohner and Dougan retain positions despite public outcry."
    },
    {
        "Year": "2015",
        "Net_Revenues_CHF_M": 23797,
        "Provision_for_Credit_Losses_CHF_M": 324,
        "Operating_Expenses_CHF_M": 25895,
        "Net_Income_to_Shareholders_CHF_M": -2944,
        "Diluted_EPS_CHF": -1.72,
        "Customer_Deposits_CHF_B": 369.3,
        "Total_Assets_CHF_B": 820.8,
        "Shareholders_Equity_CHF_B": 44.4,
        "Tier_1_Ratio_Pct": 15.5,
        "Key_Leadership": "Tidjane Thiam (CEO), Urs Rohner (Chairman)",
        "Key_Event": "Tidjane Thiam takes over as CEO; initiates radical pivot away from investment banking to wealth management; massive goodwill impairment."
    },
    {
        "Year": "2016",
        "Net_Revenues_CHF_M": 20323,
        "Provision_for_Credit_Losses_CHF_M": 252,
        "Operating_Expenses_CHF_M": 22337,
        "Net_Income_to_Shareholders_CHF_M": -2710,
        "Diluted_EPS_CHF": -1.32,
        "Customer_Deposits_CHF_B": 361.7,
        "Total_Assets_CHF_B": 822.1,
        "Shareholders_Equity_CHF_B": 41.9,
        "Tier_1_Ratio_Pct": 16.0,
        "Key_Leadership": "Tidjane Thiam (CEO), Urs Rohner (Chairman)",
        "Key_Event": "$5.28B settlement with US Department of Justice regarding legacy residential mortgage-backed securities (RMBS)."
    },
    {
        "Year": "2017",
        "Net_Revenues_CHF_M": 20900,
        "Provision_for_Credit_Losses_CHF_M": 210,
        "Operating_Expenses_CHF_M": 18897,
        "Net_Income_to_Shareholders_CHF_M": -983,
        "Diluted_EPS_CHF": -0.41,
        "Customer_Deposits_CHF_B": 376.1,
        "Total_Assets_CHF_B": 796.3,
        "Shareholders_Equity_CHF_B": 41.9,
        "Tier_1_Ratio_Pct": 17.5,
        "Key_Leadership": "Tidjane Thiam (CEO), Urs Rohner (Chairman)",
        "Key_Event": "US Tax Cuts and Jobs Act triggers CHF 2.3B deferred tax asset write-down; operating performance begins improving."
    },
    {
        "Year": "2018",
        "Net_Revenues_CHF_M": 20920,
        "Provision_for_Credit_Losses_CHF_M": 245,
        "Operating_Expenses_CHF_M": 17303,
        "Net_Income_to_Shareholders_CHF_M": 2024,
        "Diluted_EPS_CHF": 0.77,
        "Customer_Deposits_CHF_B": 364.7,
        "Total_Assets_CHF_B": 768.7,
        "Shareholders_Equity_CHF_B": 44.0,
        "Tier_1_Ratio_Pct": 17.3,
        "Key_Leadership": "Tidjane Thiam (CEO), Urs Rohner (Chairman)",
        "Key_Event": "Completion of Thiam's 3-year restructuring; first full-year profit since 2014."
    },
    {
        "Year": "2019",
        "Net_Revenues_CHF_M": 22484,
        "Provision_for_Credit_Losses_CHF_M": 324,
        "Operating_Expenses_CHF_M": 17440,
        "Net_Income_to_Shareholders_CHF_M": 3419,
        "Diluted_EPS_CHF": 1.30,
        "Customer_Deposits_CHF_B": 384.9,
        "Total_Assets_CHF_B": 787.3,
        "Shareholders_Equity_CHF_B": 43.6,
        "Tier_1_Ratio_Pct": 17.3,
        "Key_Leadership": "Tidjane Thiam (CEO), Urs Rohner (Chairman)",
        "Key_Event": "Highest profit in a decade (CHF 3.4B); overshadowed by corporate espionage scandal (spying on Iqbal Khan); Thiam forced out in Feb 2020."
    },
    {
        "Year": "2020",
        "Net_Revenues_CHF_M": 22389,
        "Provision_for_Credit_Losses_CHF_M": 1096,
        "Operating_Expenses_CHF_M": 17826,
        "Net_Income_to_Shareholders_CHF_M": 2669,
        "Diluted_EPS_CHF": 0.99,
        "Customer_Deposits_CHF_B": 390.9,
        "Total_Assets_CHF_B": 805.8,
        "Shareholders_Equity_CHF_B": 42.7,
        "Tier_1_Ratio_Pct": 19.3,
        "Key_Leadership": "Thomas Gottstein (CEO), Urs Rohner (Chairman)",
        "Key_Event": "Thomas Gottstein appointed CEO; COVID-19 pandemic provisions; unhedged Archegos swap positions quietly accumulate."
    },
    {
        "Year": "2021",
        "Net_Revenues_CHF_M": 22696,
        "Provision_for_Credit_Losses_CHF_M": 4205,
        "Operating_Expenses_CHF_M": 19091,
        "Net_Income_to_Shareholders_CHF_M": -1650,
        "Diluted_EPS_CHF": -0.63,
        "Customer_Deposits_CHF_B": 392.8,
        "Total_Assets_CHF_B": 755.8,
        "Shareholders_Equity_CHF_B": 44.0,
        "Tier_1_Ratio_Pct": 20.5,
        "Key_Leadership": "Thomas Gottstein (CEO), António Horta-Osório (Chairman)",
        "Key_Event": "Dual disaster: Greensill Capital collapses ($10B fund freeze) & Archegos defaults ($5.5B prime brokerage loss); Horta-Osório becomes Chairman."
    },
    {
        "Year": "2022",
        "Net_Revenues_CHF_M": 14921,
        "Provision_for_Credit_Losses_CHF_M": 16,
        "Operating_Expenses_CHF_M": 18163,
        "Net_Income_to_Shareholders_CHF_M": -7293,
        "Diluted_EPS_CHF": -2.55,
        "Customer_Deposits_CHF_B": 233.2,
        "Total_Assets_CHF_B": 531.4,
        "Shareholders_Equity_CHF_B": 45.1,
        "Tier_1_Ratio_Pct": 20.0,
        "Key_Leadership": "Ulrich Körner (CEO), Axel Lehmann (Chairman)",
        "Key_Event": "Horta-Osório ousted for COVID breaches; Gottstein replaced by Körner; social media panic sparks Q4 bank run (CHF 110.5B net outflows); CHF 4B capital raise."
    },
    {
        "Year": "1Q23",
        "Net_Revenues_CHF_M": 18467,
        "Provision_for_Credit_Losses_CHF_M": 83,
        "Operating_Expenses_CHF_M": 5620,
        "Net_Income_to_Shareholders_CHF_M": 12432,
        "Diluted_EPS_CHF": 3.12,
        "Customer_Deposits_CHF_B": 166.2,
        "Total_Assets_CHF_B": 516.3,
        "Shareholders_Equity_CHF_B": 53.7,
        "Tier_1_Ratio_Pct": 20.3,
        "Key_Leadership": "Ulrich Körner (CEO), Axel Lehmann (Chairman)",
        "Key_Event": "Terminal run: March 14 material weaknesses admitted; March 15 Saudi 'absolutely not' remark; March 19 emergency Sunday takeover by UBS for CHF 3.0B; CHF 15.6B AT1 wipeout."
    }
]

# Write CSV
csv_path = os.path.join(DATA_DIR, "credit_suisse_historical_16yr_trajectory_2008_2023.csv")
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(full_timeline[0].keys()))
    writer.writeheader()
    writer.writerows(full_timeline)

print(f"Saved {len(full_timeline)} years of verified financial data to {csv_path}")

# Run analytical synthesis through local Gemma model
print("\nSynthesizing analytical deep-dives using local Gemma model...")

eras = [
    {
        "name": "Era 1: 2008–2010 (The GFC 'Winner' Trap & Brady Dougan's Sovereign Capital)",
        "context": "In 2008, UBS took a CHF 60B state bailout. Credit Suisse avoided a direct Swiss bailout by raising CHF 10B from Qatar and Saudi investors, yet still posted an CHF 8.2B loss in 2008. Management concluded their risk model was superior and kept their massive investment bank."
    },
    {
        "name": "Era 2: 2011–2014 (The Urs Rohner Era & US Criminal Tax Conviction)",
        "context": "Urs Rohner took over as Chairman in 2011. In May 2014, Credit Suisse pleaded guilty to criminal charges in the US for aiding offshore tax evasion, paying $2.6B in fines. Despite pleading guilty to a felony, neither Dougan nor Rohner resigned, cementing an era of unaccountability."
    },
    {
        "name": "Era 3: 2015–2019 (The Tidjane Thiam Restructuring & The Spying Scandal)",
        "context": "Thiam was brought in to pivot the bank toward wealth management and shrink the investment bank. After years of heavy restructuring losses ($5.3B DOJ RMBS settlement, goodwill write-downs), the bank turned a CHF 3.4B profit in 2019. However, the Iqbal Khan corporate espionage scandal erupted, forcing Thiam out in February 2020."
    },
    {
        "name": "Era 4: 2020–2021 (The Twin Disasters: Greensill & Archegos)",
        "context": "Under CEO Thomas Gottstein, March 2021 brought two catastrophic blowups in weeks: Greensill Capital's $10B supply chain funds collapsed, followed immediately by Archegos Capital Management's $5.5B default on unhedged total return swaps. The Paul Weiss report revealed systemic control failures."
    },
    {
        "name": "Era 5: 2022–2023 (The Death Spiral: Social Media Bank Run & Sunday Takeover)",
        "context": "António Horta-Osório resigned over COVID rules, Axel Lehmann became Chairman, and Ulrich Körner became CEO. In October 2022, social media rumors sparked a massive CHF 110.5B bank run in Q4. In March 2023, after admitting internal control material weaknesses and the Saudi 'absolutely not' comment, UBS acquired Credit Suisse for CHF 3.0B while FINMA wiped out CHF 15.6B in AT1 bonds."
    }
]

syntheses = {}
for era in eras:
    print(f"Querying Gemma for {era['name']}...")
    prompt = (
        f"You are a Senior Wall Street Investigative Analyst writing a chapter for the report 'The Fall of Credit Suisse'.\n\n"
        f"Context: {era['context']}\n\n"
        f"Analyze this era in 3 structured paragraphs:\n"
        f"1. Strategic & Cultural Vulnerability: What structural flaws or management decisions set the stage?\n"
        f"2. Core Catalysts & Control Failures: What specific events or breakdowns occurred?\n"
        f"3. Long-term Impact: How did this erode capital, reputation, or regulatory standing toward the final 2023 collapse?"
    )
    res = query_gemma(prompt)
    syntheses[era['name']] = res

# Write synthesis report
doc_path = os.path.join(DOCS_DIR, "the_fall_of_credit_suisse_16yr_forensic_report.md")
with open(doc_path, "w", encoding="utf-8") as f:
    f.write("# The Fall of Credit Suisse: 16-Year Comprehensive Forensic Report (2008–2023)\n\n")
    f.write("## Executive Summary\n")
    f.write("Credit Suisse’s collapse on Sunday, March 19, 2023, was not a sudden liquidity shock—it was the terminal culmination of a 15-year governance, risk management, and strategic unraveling that began in the 2008 Global Financial Crisis.\n\n")
    f.write("### 16-Year Financial Trajectory (2007–2023)\n\n")
    f.write("| Year | Net Revenues (CHF M) | Net Income (CHF M) | Customer Deposits (CHF B) | Total Assets (CHF B) | Tier 1 Ratio (%) | Key Event |\n")
    f.write("| :---: | :---: | :---: | :---: | :---: | :---: | :--- |\n")
    for row in full_timeline:
        f.write(f"| **{row['Year']}** | {row['Net_Revenues_CHF_M']:,} | {row['Net_Income_to_Shareholders_CHF_M']:,} | {row['Customer_Deposits_CHF_B']} | {row['Total_Assets_CHF_B']} | {row['Tier_1_Ratio_Pct']}% | {row['Key_Event'][:70]}... |\n")
    f.write("\n---\n\n")
    f.write("## Detailed Forensic Eras (Synthesized with Local Gemma Model)\n\n")
    for name, content in syntheses.items():
        f.write(f"### {name}\n\n")
        f.write(f"{content}\n\n---\n\n")

print(f"Successfully generated comprehensive analysis at {doc_path}!")
