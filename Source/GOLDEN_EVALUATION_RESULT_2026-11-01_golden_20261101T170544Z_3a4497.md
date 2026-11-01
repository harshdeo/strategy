# Golden 50 evaluation result 2: 24 of 50 passed

**Run `golden_20261101T170544Z_3a4497`, 1 November 2026, on the repaired build.** A development self-evaluation by one reviewer, scored like the first result ([GOLDEN_EVALUATION_RESULT_2026-11-01_golden_20261101T152520Z_2c17c9.md](GOLDEN_EVALUATION_RESULT_2026-11-01_golden_20261101T152520Z_2c17c9.md): 7 of 50): every delivered answer read in full against the prompt's expected behaviour in `GOLDEN_EVALUATION_BENCHMARK.md` and against NSE XBRL filings captured for the runs. **Read this number with one caution: the repairs were written after reading the first run's failures on these same 50 prompts, so this is a development measure of those repairs and not a held-out test. It cannot certify a release or a leadership claim.** The benchmark file, the decks, the memo and the first result are unchanged.

**Result: 24 PASS, 26 FAIL, denominator 50.** All 50 slots returned an answer; no slot errored or was skipped. A slot with no answer, an error or no judgement is a failure.

## What was run

- Suite: `strategy/Source/GOLDEN_EVALUATION_BENCHMARK.md`, sha256 `6c8ca83166ee4636456f11e32bf6d6267666f3449857573507b734744cd2fc63`; 50 prompts verbatim, one attempt each, no retries. The file differs from the committed copy in prompt 1's expected-behaviour text only (an uncommitted edit by another session, present before both runs).
- Clock `2026-10-30T17:00:00+05:30`. Vertex Gemini through the Copilot's configured models; SDK `google-genai==1.47.0` in a run-owned virtualenv.
- Build exported from commits: intelligence `91b8edbaf8`, data-platform `c8d300fe73`, query-api `e0d39522d6`, broker-portfolio `629e32114b`. Uncommitted files present and **not** used: intelligence: tests/test_signed_off_numerical_expectations_l08.py; data-platform: app/services/indices/contract_backfill.py, tests/test_index_contracts_migration_postgres.py, reports/announcement-completeness/.
- Owned stack: its own server on port 57092 (proved to be this run's child), Redis on port 57078, database `anvest_golden_44Z_3a4497_test` created and dropped by the run; warehouse tables read through read-only foreign tables.
- Data: the Mac warehouse of 1 November 2026, not production; `feature_store_daily` as a 60-day slice (247431 rows).
- Every answer carries the canonical identity hash recorded at capture (`answer_identity.verify_receipt`: no problems); adapter run `eval_owned_a6d151731f`.
- Spend: measured exposure 19.7785 to 22.0304 INR; aggregate exposure across all runs 137.03 of 1,000 INR.
- Receipt `docs/autonomous-run-2026-10-30/golden-50-r3/result-run/receipt.json`, sha256 `f6a3a0ef33ca0444ebdc469330bfb3d6588ebb8e04a934ac6e7d278cab47fed5`; machine verdicts `GOLDEN_EVALUATION_RESULT_2026-11-01_golden_20261101T170544Z_3a4497.json`. Intermediate runs on earlier commits of the repair are kept in `golden-50-r3/` and are not scored.

## Change since the first result (7 of 50)

Gained (17): G01, G02, G03, G04, G07, G08, G09, G11, G31, G32, G35, G38, G40, G41, G42, G45, G50. Lost (0): none.

What was repaired (intelligence `3a762bf`..`91b8edb`, query-api `e0d3952`, market-ui `7c6b271`):

- Routing: "compare to Q1", "standalone vs consolidated", "reported and adjusted" and metric lists ("NII, net profit") no longer read as company comparisons; metric names such as debt-to-equity are not screens; basis words and data vendors are not company names.
- Scope of what was asked: revenue and PAT with margins, operating profit amount, both net-margin denominators, the prior-year base, standalone and consolidated side by side, EPS, EBITDA margin (operating EBITDA, never the EBIT margin), bank net interest income, provisions and pre-provision profit from the filing's own tags.
- Boundaries: ratios that do not exist for lenders are explained; IT services carry no inventory; insurers have no operating margin; free cash flow across a bank is flagged; questions about an unnamed company ask for one; pre-listing financials and licensed terminals are stated plainly; forecast questions always carry the decline; an index with no row has no verified close rather than being "not covered"; a quarter not on record is said before the quarter that is.
- Harness: allocation questions missing inputs ask for them (no longer HTTP 500); the screener-time cost of this harness is unchanged.

## Remaining failure causes

| Cause | Slots | Meaning |
|---|---|---|
| scope_incomplete | 8 (G13, G17, G18, G19, G20, G33, G36, G39) | Figures given are right but a requested part is missing. |
| needs_company | 8 (G21, G24, G25, G26, G27, G28, G29, G30) | Asked which company: the prompt names none, and the expected data is not served. |
| declined_data | 5 (G05, G10, G14, G16, G23) | Said the figure is not in the sources where the filings are expected to carry it. |
| wrong_figure | 1 (G06) | A figure in the answer differs from the filing. |
| unconfirmed_absence | 1 (G12) | Said a filing is not on record; absence could not be confirmed. |
| generic_prose | 1 (G15) | Method text or an unrelated table instead of the data. |
| wrong_subject | 1 (G22) | Answered about an unrelated company. |
| boundary_policy | 1 (G49) | Needs a product-policy decision, not a code fix. |

Data the answers need and the warehouse does not hold: bank KPI facts (CASA, NIM, advances and deposit growth, slippages, provision coverage) are not in the filings' result tags and `business_kpi_facts` is empty on this warehouse (I0601); Airtel's adjusted EBITDA is in the company release, not the XBRL; Tata Steel and HDFC Bank cash-flow and long revenue histories are not served; the screener does not run costed backtests or three-year improvement tests (G36, G39). Wipro's stored prior-year PAT is on a different basis from the current one (G06, I0607).

## Latency

Most slots answered in under ten seconds. G36, G39 and G46 took about three minutes each: all three go through the screener, whose queries run through foreign-table links in this harness; that is not a production measurement.

## Verdicts

| # | Verdict | First result | Seconds | Cause | Observation |
|---|---|---|---:|---|---|
| G01 | PASS | FAIL | 4.1 |  | Revenue 73,188 cr and PAT 13,934 cr, EBIT margin 23.98% labelled as EBIT / revenue from operations, down 120 bps YoY from 25.18%, with the 8 Oct 2026 NSE filing cited. All match the filing. |
| G02 | PASS | FAIL | 2.1 |  | Net margin on total income (15.65% / 14.31%) and on revenue from operations (15.92% / 14.41%) for each company, denominators labelled; all match the filings. |
| G03 | PASS | FAIL | 2.2 |  | Consolidated (73,188 / 13,934 cr) and standalone (60,441 / 14,104 cr) side by side, each labelled; both match the filings. |
| G04 | PASS | FAIL | 0.2 |  | EBITDA margin 17.01% (operating EBITDA over revenue from operations, other income excluded), previous quarter 15.24%, +177 bps; both recomputed from the Reliance filings. |
| G05 | FAIL | FAIL | 9.6 | declined_data | Says a trend is available for FY27 and gives no quarterly figures. |
| G06 | FAIL | FAIL | 1.2 | wrong_figure | Operating profit 3,986 cr, EBIT margin and denominators are right, but the prior-year net margin is 13.73% against 13.80% in the filing: the stored prior-year PAT is profit attributable to owners while the current one is total profit (S4-PAT-BASIS). |
| G07 | PASS | FAIL | 2.7 |  | PAT growth +14.86% / +6.28% / +21.15% with the prior-year bases 12,131 / 7,375 / 4,236 cr shown; all match the filings. |
| G08 | PASS | FAIL | 0.4 |  | Basic 10.07 and diluted 10.05, prior year 7.85 and 7.83, as filed (Bajaj Finance consolidated tags). |
| G09 | PASS | FAIL | 2.2 |  | Net interest income 30,336 cr as interest earned less interest expended, with operating profit before provisions 24,010, provisions 895 and PAT 17,312 cr, in the bank layout; all match the filing. |
| G10 | FAIL | FAIL | 1.7 | declined_data | Says Q2 FY27 data is not in the filings; gives no reported-to-adjusted bridge. |
| G11 | PASS | FAIL | 1.2 |  | Net interest income, operating profit before provisions, provisions and PAT for both banks (44,464 / 32,872 / 4,209 / 20,700 and 30,336 / 24,010 / 895 / 17,312 cr); all match the filings. |
| G12 | FAIL | FAIL | 7.8 | unconfirmed_absence | Says no Q2 FY27 figure is on record and gives the 30 June quarter (gross NPA 1.47%, net 0.38%, which match that filing); no provision coverage ratio. Whether SBI had filed Q2 by the clock could not be confirmed here, so the slot is unjudged and fails. |
| G13 | FAIL | FAIL | 2.2 | scope_incomplete | Operating profit before provisions 7,564 cr matches the filing; slippage data is not given (stated). |
| G14 | FAIL | FAIL | 0.3 | declined_data | Gives interest earned and PAT; no CASA ratio. |
| G15 | FAIL | FAIL | 5.6 | generic_prose | Method sentence followed by an unrelated mutual-fund table. |
| G16 | FAIL | FAIL | 4.3 | declined_data | Gives no advances or deposit growth. |
| G17 | FAIL | FAIL | 0.2 | scope_incomplete | Explains that a lender has no operating margin, which is defensible, but gives none of the bank-format operating profit the prompt points to. |
| G18 | FAIL | FAIL | 1.6 | scope_incomplete | Net profit 1,912 cr; no net interest margin. |
| G19 | FAIL | FAIL | 3.9 | scope_incomplete | States SBI return on assets 1.09% (the June filing carries 1.11%) and none for HDFC Bank. |
| G20 | FAIL | FAIL | 0.3 | scope_incomplete | Interest earned and PAT only; not the key highlights. |
| G21 | FAIL | FAIL | 3.6 | needs_company | Asks which company; the prompt names none, but the repaired data is not served. |
| G22 | FAIL | FAIL | 1.3 | wrong_subject | Answers about an unrelated tiny issuer and gives a quarter, not an FY26 annual figure. |
| G23 | FAIL | FAIL | 4.2 | declined_data | Says no operating cash flow for Tata Steel is in the evidence. |
| G24 | FAIL | FAIL | 2.2 | needs_company | Asks which company; no discrepancy flagged. |
| G25 | FAIL | FAIL | 3.1 | needs_company | Asks which company; no depreciation data. |
| G26 | FAIL | FAIL | 2.5 | needs_company | Asks which company; no reconciliation. |
| G27 | FAIL | FAIL | 3.0 | needs_company | Asks which company; no trend. |
| G28 | FAIL | FAIL | 2.6 | needs_company | Asks which company; no trend. |
| G29 | FAIL | FAIL | 2.2 | needs_company | Asks which company; no conflict flagged. |
| G30 | FAIL | FAIL | 0.0 | needs_company | Asks which company; no payout ratio. |
| G31 | PASS | FAIL | 0.4 |  | Withholds ROCE for both lenders and explains that capital employed is not defined for them. |
| G32 | PASS | FAIL | 2.1 |  | States debt-to-equity is not meaningful for HDFC Bank because a lender's borrowings fund its loan book. |
| G33 | FAIL | FAIL | 3.7 | scope_incomplete | Says the comparison is not meaningful for the bank but gives no TCS working-capital turnover. |
| G34 | PASS | PASS | 0.4 |  | States inventory turnover does not apply to an IT services company, which carries no meaningful inventory. |
| G35 | PASS | FAIL | 0.0 |  | Declines to screen NBFCs on ROCE and says why, with the measures to use instead. |
| G36 | FAIL | FAIL | 178.6 | scope_incomplete | Lists ten stocks by ROE; no exact match count, no debt-to-equity filter shown and no costed backtest (179 s). |
| G37 | PASS | PASS | 2.2 |  | Explains that insurers' underwriting and investing results are judged separately and names the measures used. |
| G38 | PASS | FAIL | 3.6 |  | Flags that free cash flow is not defined the same way for a bank and asks for the FMCG and IT companies. |
| G39 | FAIL | FAIL | 178.9 | scope_incomplete | Lists ten companies by ROCE level; no three-year improvement test (179 s). |
| G40 | PASS | FAIL | 1.4 |  | States asset turnover is not meaningful for a lender and why. |
| G41 | PASS | FAIL | 2.5 |  | Names the placeholder as no company and says the line is only there when the company discloses it. |
| G42 | PASS | FAIL | 2.1 |  | States pre-listing financials are not in the exchange warehouse. |
| G43 | PASS | PASS | 1.8 |  | Declines a FY28 revenue figure; frames it as absent from disclosures rather than as a no-forecast policy. |
| G44 | PASS | PASS | 0.0 |  | Declines price targets; no consensus figure given. |
| G45 | PASS | FAIL | 3.1 |  | States what Anvest's data comes from and that a licensed terminal cannot be compared with. |
| G46 | PASS | PASS | 191.8 |  | States it gives no investment advice and names no stock; the screen it ran took 192 s. |
| G47 | PASS | PASS | 0.0 |  | Declines a personal recommendation. |
| G48 | PASS | PASS | 0.0 |  | Declines a buy decision and a target price. |
| G49 | FAIL | FAIL | 2.4 | boundary_policy | No longer an error: it asks for age, horizon and risk profile, which leads to an allocation rather than the refusal the benchmark expects. Whether Anvest should refuse or compute is a product-policy decision. |
| G50 | PASS | FAIL | 1.8 |  | Says Anvest does not forecast index moves and that Nifty 50 has no verified close at this date. |

## Limits

One reviewer, one run, one attempt per prompt, the Mac warehouse rather than production, and generic prompts G15, G21 to G30, G41 and G42 whose unnamed subjects make the expected behaviour a judgement (asking for the company was scored as a failure where the benchmark expects the data, and a pass where it expects a boundary statement). The repairs were fitted to these prompts. Independent grading on a sealed set is a separate process that has not happened.
