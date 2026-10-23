# Credit Suisse project: source and analytical-data review

## Bottom line

The source pack supports a strong technical-analysis section, but not a conventional supervised fraud-detection model. There is no transaction-level dataset, labelled fraud outcome, full email corpus, or daily deposit series. The defensible analytical framing is therefore:

> **Could a transparent early-warning system have detected the accumulation and non-remediation of risk before the Archegos loss and the 2023 liquidity crisis?**

The analysis can combine three layers:

1. **Counterparty early-warning analysis (Archegos):** compare exposures, margins, concentrations and revenues with limits, historical levels and peer values.
2. **Liquidity stress-gap analysis (Credit Suisse):** compare observed deposit outflows with Liquidity Coverage Ratio (LCR) assumptions.
3. **Control and supervision gap analysis:** code the IMF Basel Core Principle grades and compare them with FINMA, parliamentary and FSB findings.

This is relevant to fraud analytics because it tests the detection and escalation of red flags, control overrides, anomalous counterparty behaviour, whistleblower information and governance failures. It should not claim that the entire fall of Credit Suisse was itself a fraud. The Archegos report explicitly distinguishes control and management failures from fraudulent or illegal conduct by Credit Suisse personnel.

## 1. Requirements from the handout

The common report must be at least three double-column pages, excluding the bibliography, and follow the supplied LaTeX template. The required sections are:

1. Executive summary.
2. Research objectives and data collection.
3. Methodological approach.
4. Validation and quality control.
5. Challenges, timeline and communication of results.

The presentation is 25 minutes plus 10 minutes of questions, and each of the three team members must present at least eight minutes. For the Credit Suisse group, the report is due **2 November 2026** and the presentation is on **5 November 2026**.

The handout offers a grade bonus for a technical analysis using real-world or realistic data. It requires the data, methods, parameters and evaluation metrics to be stated, with properly labelled and discussed tables and figures.

## 2. Source audit

| Source | What it contributes | Analytical value | Main caution |
|---|---|---:|---|
| Credit Suisse Special Committee report on Archegos (2021) | Detailed chronology, exposures, limits, margins, concentrations, risk discussions and loss | Very high | Internal retrospective report; values are selected rather than a complete raw dataset |
| SNB Financial Stability Report 2024 | Deposit-outflow rates by category and episode, LCR assumptions, capital and liquidity lessons | Very high | Aggregated bank data; only two crisis episodes in Table 4 |
| Federal Council report on banking stability (2024) | Official chronology, CHF 138bn Q4 2022 deposit withdrawal, liquidity facilities and policy measures | High | Policy report, not a raw dataset |
| IMF Switzerland Basel Core Principles assessment (2025) | Grades for all 29 principles and detailed supervisory findings | High | Post-crisis national framework assessment; not proof of causation in the Credit Suisse failure |
| FSB public-sector backstop peer review (2026) | Cross-country framework and Switzerland's current assessment | High | Assessment reflects law in force as of August 2026; proposed PLB legislation is excluded |
| FSB 2023 bank-failures report | Resolution preparedness, alternatives and lessons from Credit Suisse | Medium-high | Resolution focus rather than misconduct detection |
| FINMA lessons-learned press release (2023) | Enforcement and supervisory activity counts, risk-culture findings | Medium | Summary page; use the full FINMA report if it becomes available |
| Parliamentary Investigation Committee press release (2024) | Official conclusions on management responsibility, regulatory filter and authority coordination | Medium | Press-release summary, not the full parliamentary report |
| Grünewald academic article (2025) | Legal assessment of the rescue merger against FSB Key Attributes | Medium | Secondary interpretation; useful for discussion rather than primary fact finding |
| Guardian Greensill article (2025) | Evidence that anonymous warnings existed from 2018 and 2019; USD 10bn fund scale | Medium-low | Journalistic secondary source; trace claims to the underlying FINMA Greensill report where possible |

## 3. Quantitative analysis

### 3.1 Archegos: simple controls would have produced repeated high-severity alerts

The Special Committee report contains enough values to reconstruct a small early-warning dataset.

| Indicator | Observed | Benchmark | Derived result |
|---|---:|---:|---:|
| Potential exposure, August 2020 | Just under USD 530m | USD 20m limit | **26.5x the limit** |
| Scenario exposure, 22 July 2020 | USD 828m | USD 250m limit | **3.31x the limit** |
| Gross market value, 8 March 2021 | USD 20bn | Next-largest client: USD 5bn | **4.0x the peer** |
| Net-long bias, 8 March 2021 | More than USD 7bn | Next-largest long-biased client: USD 1.5bn | **about 4.67x the peer** |
| Swap margin | 20% historical average | 7.5% from May 2019 | **62.5% reduction** |
| Effective swap margin, September 2020 | 5.9% | 20% historical average | **70.5% below the earlier average** |
| Realised loss | About USD 5.5bn | USD 17.4m 2020 revenue in CPOC materials | **about 316 years of 2020 revenue** |

The revenue comparison is a scale comparison, not an expected-loss estimate. The report also gives an approximately USD 16m revenue figure elsewhere, so the exact ratio depends on which rounded revenue value is used. The conclusion is unchanged: the downside was orders of magnitude larger than the annual revenue.

Other warning signals strengthen the result:

- Archegos's portfolio was between 63% and 95% net long almost every week until default.
- Its top five positions reached 175% of NAV by December 2020.
- Credit Suisse paid Archegos USD 2.4bn of excess variation margin between 11 and 19 March 2021 while the dynamic-margin proposal was being ignored.
- On 12 March, Credit Suisse renewed USD 13bn of net-long positions, mostly at the existing 7.5% margin.
- On 25 March, margin calls totalled more than USD 2.8bn; Archegos could not pay.
- At the final prime-broker call, Archegos reported USD 120bn gross exposure and only USD 9-10bn equity, implying gross leverage of about **12-13x**.

**Interpretation:** the failure was not a lack of observable signals. It was a failure to connect signals, enforce limits, update margin, assign ownership and escalate decisions. A rule-based alert using only breach ratios and margin deterioration would have triggered months before the default.

### 3.2 Liquidity: observed deposit runs exceeded regulatory assumptions

SNB Table 4 permits a direct back-test of LCR run-off assumptions.

| Episode and category | LCR assumption | Observed 30-day outflow | Observed / assumed |
|---|---:|---:|---:|
| October 2022 - retail | 12% | 24% | **2.00x** |
| October 2022 - high-value retail | 20% | 44% | **2.20x** |
| October 2022 - total deposits | 28% | 31% | **1.11x** |
| March 2023 - retail | 12% | 24% | **2.00x** |
| March 2023 - high-value retail | 20% | 41% | **2.05x** |
| March 2023 - total deposits | 25% | 32% | **1.28x** |

In March 2023, high-value retail deposits fell 33% in one week, already **1.65x** the 20% run-off assumed for a full 30 days. The SNB states that roughly CHF 200bn left Credit Suisse between October 2022 and March 2023 - more than half of customer deposits and roughly 30% of the September 2022 balance sheet. About CHF 90bn left in October 2022 alone.

The Federal Council separately reports CHF 138bn of client-deposit withdrawals between October and year-end 2022. The figures measure different scopes and periods and should not be treated as contradictory.

**Interpretation:** regulatory compliance was not equivalent to resilience. A monitoring system should combine LCR with deposit concentration, digital-withdrawal speed, social-media signals and forward-looking scenario tests.

### 3.3 IMF scorecard: supervisory weaknesses remained broad after the crisis

The 2025 IMF assessment grades all 29 Basel Core Principles:

- **11 compliant (37.9%)**
- **10 largely compliant (34.5%)**
- **8 materially non-compliant (27.6%)**
- **0 non-compliant**

Therefore, **18 of 29 principles (62.1%) were not fully compliant**. The materially non-compliant principles were:

- responsibilities, objectives and powers;
- independence, accountability, resourcing and legal protection;
- supervisory techniques and tools;
- corrective and sanctioning powers;
- risk-management process;
- capital adequacy;
- related-party transactions; and
- country and transfer risks.

This supports a report argument about structural weaknesses in powers, resourcing, intervention and risk oversight. It does **not** establish that any single grade caused Credit Suisse to fail; the assessment was conducted after the event and applies to Switzerland's framework as a whole.

### 3.4 Resolution funding: high operational readiness but low legal funding flexibility

The FSB's October 2026 peer review rates Switzerland as:

- funding flexibility: **Low**;
- operational readiness: **High**;
- overall credibility: **Materially non-compliant**;
- loss recovery: **Largely compliant**;
- moral hazard: **Largely compliant**; and
- overall assessment: **Materially non-compliant**.

The apparent tension is informative. Swiss authorities demonstrated same-day operational capability in March 2023, but the permanent legal framework assessed in 2026 still lacked a sufficiently scalable public backstop because the proposed PLB was not yet established in dedicated legislation as of the review's August 2026 cutoff.

## 4. Recommended methodology for the report

### A. Counterparty early-warning score

Use a transparent score rather than machine learning because the available data are sparse and contain only one positive outcome.

For observation date \(t\), define:

\[
S_t = w_1 \log(1+PE_t/L_{PE})
    + w_2 \log(1+SE_t/L_{SE})
    + w_3(1-M_t/M_{hist})
    + w_4 C_t
    + w_5 G_t
\]

where:

- \(PE_t/L_{PE}\): potential exposure divided by its limit;
- \(SE_t/L_{SE}\): scenario exposure divided by its limit;
- \(M_t/M_{hist}\): effective margin relative to the historical margin;
- \(C_t\): concentration score (for example, top-five positions/NAV or position/float); and
- \(G_t\): governance score for unresolved breaches, cancelled meetings, missing deadlines or limit increases during a breach.

Start with equal weights and then run a sensitivity analysis with exposure indicators weighted twice as heavily. Cap extreme ratios before aggregation so one variable does not dominate.

Suggested alert rules:

- amber: any exposure above 1.0x limit;
- red: any exposure above 2.0x limit, margin below 10%, or a top position above 5% of float;
- critical: two red signals persist for more than one reporting cycle without a named owner and deadline.

### B. Liquidity assumption-gap test

For each deposit category \(c\) and episode \(e\), calculate:

\[
Gap_{c,e} = ObservedOutflow_{c,e} - LCRAssumption_{c,e}
\]

and

\[
Multiple_{c,e} = ObservedOutflow_{c,e}/LCRAssumption_{c,e}.
\]

Rank categories by both absolute percentage-point gap and the multiple. High-value retail is the most important category in both episodes.

### C. Qualitative control-failure coding

Code dated events into a small taxonomy:

1. warning received;
2. limit breached;
3. model or metric challenged;
4. exception granted or limit increased;
5. remediation proposed;
6. remediation delayed or cancelled;
7. issue escalated;
8. loss or liquidity event.

Then calculate warning-to-action lag, number of unresolved red flags and number of exceptions granted while a breach was active. This directly links fraud-analytics concepts (signals, alert triage, escalation and case management) to the case.

## 5. Validation and quality control

- **Source triangulation:** require an official or primary source for every quantitative claim. Use the Guardian and academic paper mainly for context and interpretation.
- **Recalculation:** retain the CSV files and formulas for all derived ratios.
- **Sensitivity:** test alternative score weights and alert thresholds; report whether the qualitative conclusion changes.
- **Temporal integrity:** use only information documented as available by each date when discussing whether an alert could have fired.
- **Avoid leakage:** do not use the eventual loss amount as an input to a pre-default alert score.
- **Missing-data treatment:** label approximate values, inequalities (for example, “more than USD 7bn”) and rounded values explicitly.
- **Robustness limit:** do not report precision, recall or AUC; one failure case cannot support those metrics.
- **External validity:** present Archegos as an illustrative case study, not proof that the proposed rules generalise to all banks or fraud types.

## 6. Report-ready thesis and section plan

### Thesis

Credit Suisse's collapse was not caused by an absence of data. Across counterparty risk, liquidity and supervision, material warning signals existed but were fragmented, discounted, overridden or acted on too slowly. A transparent early-warning and escalation system could have identified the accumulation of risk well before the terminal crisis, although the available public data are insufficient to estimate how much loss would have been prevented.

### Suggested allocation

- **Section 1 - Executive summary:** crisis as a cumulative control and confidence failure; headline analytical results.
- **Section 2 - Objectives and data:** define the early-warning question; distinguish public aggregate data from unavailable bank-level raw data.
- **Section 3 - Method:** early-warning score, LCR gap test and event coding.
- **Section 4 - Validation:** triangulation, sensitivity, temporal integrity and limitations.
- **Section 5 - Challenges/timeline/communication:** confidentiality, sparse labels, hindsight bias and client-facing dashboard or regulator memo.

## 7. Completed and next tasks

Completed:

- reviewed the handout and all ten PDFs in the reports folder;
- extracted three analysis-ready datasets;
- recalculated breach multiples, margin deterioration, LCR gaps and IMF grade distributions; and
- identified the strongest source for each claim.

Recommended next steps:

1. Insert the two main analyses (Archegos controls and LCR gap) into Sections 3-4.
2. Use the IMF and FSB scores as supporting evidence, not as the central empirical result.
3. Obtain the full FINMA Credit Suisse and Greensill reports if possible.
4. If a richer analysis is desired, add daily Credit Suisse share price, CDS and deposit-flow data, but keep that separate from the source-pack analysis.

