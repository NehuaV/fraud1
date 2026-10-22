# The Fall of Credit Suisse: Research Findings & Data Extraction Compendium

This document synthesizes primary financial data, forensic metrics, and regulatory findings extracted from Credit Suisse's historical archive (Forms 20-F, Form 6-K filings, and investor presentations) to support the report **"The Fall of Credit Suisse"**.

---

## 1. Quantitative Core Datasets

### A. Annual Financial Collapse (2019 – 2023)
*File reference:* [`data/financial_trajectory_2019_2023.csv`](file:///Users/dobri/git/homework/fraud1/data/financial_trajectory_2019_2023.csv)
*Sources:* 2020 Form 20-F, 2022 Form 20-F, and Q1 2023 Form 6-K.

| Metric | 2019 | 2020 | 2021 | 2022 | 1Q23 (Reported)* |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Net Revenues (CHF M)** | 22,484 | 22,389 | 22,696 | 14,921 | 18,467* |
| **Credit Loss Provisions (CHF M)** | 324 | 1,096 | 4,205 | 16 | 83 |
| **Operating Expenses (CHF M)** | 17,440 | 17,826 | 19,091 | 18,163 | 5,620 |
| **Pre-tax Income / (Loss) (CHF M)** | 4,720 | 3,467 | (600) | (3,258) | 12,764* |
| **Net Income to Shareholders (CHF M)** | 3,419 | 2,669 | (1,650) | **(7,293)** | 12,432* |
| **Customer Deposits (CHF B)** | 384.9 | 390.9 | 392.8 | **233.2** | **166.2** |
| **Cash & Due from Banks (CHF B)** | 105.8 | 159.4 | 164.8 | **68.5** | 139.7** |
| **Total Assets (CHF B)** | 787.3 | 805.8 | 755.8 | 531.4 | 516.3 |
| **Shareholders' Equity (CHF B)** | 43.6 | 42.7 | 44.0 | 45.1 | 53.7 |
| **CET1 Capital Ratio (%)** | 12.7% | 12.9% | 14.4% | 14.1% | 20.3%* |

*\*Note on 1Q23 accounting anomaly:* 1Q23 reported net income and revenue were artificially inflated by a **CHF 15,007 million gain** recognized from FINMA's ordered write-down of Additional Tier 1 (AT1) notes to zero. On an adjusted operating basis, the bank suffered an adjusted pre-tax loss of **CHF 1,316 million**.
*\*\*Note on 1Q23 Cash:* Cash reserves at March 31, 2023 were sustained only through **CHF 108 billion in net borrowings from the Swiss National Bank (SNB)**.

---

### B. The Anatomy of the Bank Run (Quarterly Outflows 2022 – 2023)
*File reference:* [`data/quarterly_run_on_the_bank_2022_2023.csv`](file:///Users/dobri/git/homework/fraud1/data/quarterly_run_on_the_bank_2022_2023.csv)
*Sources:* 4Q22 Investor Presentation and 1Q23 Financial Report.

| Period | Group Net New Assets (NNA) | Wealth Mgmt NNA | Swiss Bank NNA | Asset Mgmt NNA | Customer Deposits | Total AuM |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **1Q22** | -CHF 2.4B | +CHF 4.8B | +CHF 1.2B | -CHF 8.4B | CHF 384.6B | CHF 1,555.0B |
| **2Q22** | -CHF 7.7B | -CHF 1.4B | -CHF 0.1B | -CHF 6.2B | CHF 371.8B | CHF 1,454.0B |
| **3Q22** | -CHF 12.9B | -CHF 6.4B | -CHF 1.5B | -CHF 4.2B | CHF 361.0B | CHF 1,401.0B |
| **4Q22** | **-CHF 110.5B** | **-CHF 92.7B** | **-CHF 8.3B** | **-CHF 11.7B** | **CHF 233.2B** | CHF 1,294.0B |
| **1Q23** | **-CHF 61.2B** | **-CHF 47.1B** | **-CHF 6.9B** | **-CHF 11.6B** | **CHF 166.2B** | CHF 1,253.0B |
| **Total Outflows** | **-CHF 194.7B** | **-CHF 142.8B** | **-CHF 15.6B** | **-CHF 42.1B** | **-CHF 226.6B** | **-CHF 302.0B** |

#### Key Analytical Insights:
1. **The October 2022 Social Media Trigger:** In 4Q22, ~two-thirds of the total CHF 92.7B Wealth Management outflow occurred in the month of October alone, coinciding with viral Reddit/Twitter rumors questioning Credit Suisse's solvency.
2. **Deposit Run Composition:** 57% to 60% of Wealth Management and Swiss Bank net asset outflows in both 4Q22 and 1Q23 represented immediate liquid cash deposit withdrawals rather than reallocations of securities portfolios.
3. **The Terminal March 2023 Surge:** Between March 15 and March 19, 2023, deposit withdrawals accelerated to an estimated CHF 10B+ per day, making market opening on Monday, March 20, untenable without resolution.

---

## 2. Forensic Investigation & Case Studies

### A. The Archegos Capital Management Collapse
*File reference:* [`data/archegos_metrics.json`](file:///Users/dobri/git/homework/fraud1/data/archegos_metrics.json)  
*Primary Report:* [`credit_suisse_archive_downloads/20210729-6k-mr-archegosreport.pdf`](file:///Users/dobri/git/homework/fraud1/credit_suisse_archive_downloads/20210729-6k-mr-archegosreport.pdf) (181 pages by Paul, Weiss).

* **Direct Financial Loss:** **\$5.5 billion (approx. CHF 4.8 billion)**.
* **Mechanism:** Synthetic Total Return Swaps (TRS). Credit Suisse bought underlying equities (ViacomCBS, Discovery, Baidu, Tencent Music) as hedges while giving Archegos synthetic leveraged economic exposure.
* **Peak Gross Notional Exposure:** Over **\$24 billion**.
* **Underlying Control Failures:**
  1. *Static vs. Dynamic Margining:* Prime Services charged a flat, static margin of ~10% despite extreme portfolio concentration and market capitalization dominance. Dynamic margin rules were approved in 2019/2020 but never applied to Archegos to avoid losing client revenue.
  2. *Ignored Limit Breaches:* Archegos persistently exceeded internal Potential Exposure (PE) and Stress Scenario limits for months with zero escalation to executive committees.
  3. *Unhedged Liquidation Race:* When ViacomCBS issued a \$3B stock offering on March 22, 2021 and its stock tanked, rival prime brokers (Morgan Stanley, Goldman Sachs) rapidly liquidated Archegos collateral, leaving Credit Suisse holding massive illiquid blocks.

---

### B. The Saudi National Bank (SNB) Anchor & The "Absolutely Not" Moment
*File reference:* [`data/takeover_and_at1_terms.json`](file:///Users/dobri/git/homework/fraud1/data/takeover_and_at1_terms.json)

* **November 2022 Injection:** Saudi National Bank acquired a 9.9% stake for **CHF 1.5 billion** at **CHF 3.82 per share**.
* **March 15, 2023 Trigger:** SNB Chairman Ammar Al Khudairy, when asked in a Bloomberg TV interview whether SNB would provide further financial assistance if Credit Suisse faced another call for liquidity, replied:  
  > *"The answer is absolutely not, for many reasons outside the simplest reason, which is regulatory and statutory [reaching a 10% threshold creates complex regulatory obligations]."*
* **Immediate Market Reaction:** CS shares fell 31% in hours, reaching an intraday low of CHF 1.55. 1-year Senior Credit Default Swaps (CDS) spiked past 1,000 bps, signaling imminent default.
* **Outcome for SNB:** At the merger acquisition price of CHF 0.76/share, SNB's stake was valued at ~CHF 300 million, realizing a **loss of ~CHF 1.2 billion (-80.1%)** in under four months.

---

### C. The AT1 Instrument Expropriation (CHF 15.6B Wipeout)
*File reference:* [`data/takeover_and_at1_terms.json`](file:///Users/dobri/git/homework/fraud1/data/takeover_and_at1_terms.json)

* **Total Nominal Value Cancelled:** **CHF 15.6 billion (\$17 billion)**.
* **Ordering Body:** FINMA, executing the Swiss Federal Council's emergency decree of March 19, 2023.
* **The Legal Controversy:**
  * Under standard corporate insolvency principles (the *Absolute Priority Rule*), equity absorbs first losses before hybrid capital instruments.
  * In the merger, common equity shareholders received **CHF 3.0 billion** in UBS shares, while Additional Tier 1 bondholders were wiped out to **zero**.
  * Contractual trigger: Credit Suisse's AT1 prospectuses contained a unique Swiss statutory clause permitting full permanent write-down upon a "Viability Event" (*Verfallklausel*), specifically defined as the receipt of extraordinary government support.
  * Sparked dozens of investor lawsuits globally (e.g., Quinn Emanuel, Pallas Partners) challenging the constitutionality of the emergency decree.

---

## 3. Recommended Structure for the Report

1. **Chapter 1: The Hollowed Fortress (2019–2021)**
   * Historical prestige vs. structural unprofitability.
   * The culture of risk negligence: Greensill Capital (\$10B freeze) and Archegos (\$5.5B loss).
   * Key primary evidence: *Paul, Weiss Investigation Report (Excerpts from Section I & IV)*.

2. **Chapter 2: Governance Paralysis & Churn (2022)**
   * Executive instability: Horta-Osório resignation, Gottstein ouster, Körner appointment.
   * Disastrous financial performance: 2022 net loss of CHF 7.3B.
   * Key primary evidence: *2022 Form 20-F & Executive Board Appointment Filings*.

3. **Chapter 3: The Failed Renaissance & Social Media Run (Q3–Q4 2022)**
   * The October 27, 2022 strategy: CS First Boston carve-out, Apollo SPG deal, CHF 4B capital raise.
   * The first bank run: CHF 110.5B of net asset outflows in Q4 2022.
   * Key primary evidence: *4Q22 Investor Presentation Slides 11–19*.

4. **Chapter 4: The 10-Day Death Spiral (March 9–19, 2023)**
   * March 9: SEC late-night call halts the 2022 Annual Report.
   * March 14: Filing of Form 20-F admitting "material weaknesses" in internal financial controls.
   * March 15: SVB collapse contagion + SNB "absolutely not" statement.
   * March 16: SNB extends CHF 50B Emergency Liquidity Assistance.
   * Key primary evidence: *Form 6-Ks dated March 9, 14, 16, and 20, 2023*.

5. **Chapter 5: The Sunday Resolution & The Fallout (March 19, 2023 onward)**
   * The emergency shotgun wedding: UBS pays CHF 3B; Swiss state guarantees CHF 9B; SNB commits CHF 250B total liquidity.
   * The AT1 wipeout controversy: CHF 15.6B extinguished; accounting paradox of CHF 15B paper gain.
   * Final Q1 2023 bleeding: CHF 61.2B outflow post-mortem.
   * Key primary evidence: *Q1 2023 Form 6-K & Form 20-F 2023*.
