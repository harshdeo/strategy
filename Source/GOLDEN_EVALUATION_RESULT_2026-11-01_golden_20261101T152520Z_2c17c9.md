# Golden 50 evaluation result: 7 of 50 passed

**Run `golden_20261101T152520Z_2c17c9`, 1 November 2026.** This is a development self-evaluation of one pinned build, scored by one reviewer reading each delivered answer against the prompt's expected behaviour in `GOLDEN_EVALUATION_BENCHMARK.md` and against NSE XBRL filings captured for this run. It is not an independent audit, not a release verdict and not a leadership claim. The benchmark file, the decks and the data-provenance memo were not changed; earlier cited results are untouched.

**Result: 7 PASS, 43 FAIL, denominator 50.** 49 slots returned an answer; 1 did not (G49, HTTP 500). A slot with no answer, an error or no judgement is a failure.

## What was run

- Suite: `strategy/Source/GOLDEN_EVALUATION_BENCHMARK.md`, sha256 `6c8ca83166ee4636456f11e32bf6d6267666f3449857573507b734744cd2fc63`. All 50 prompts verbatim, one attempt each, no retries.
- Benchmark file as used differs from the committed copy (sha256 `ef8b192b16647246720ec610fd770a6051c714c13e252577c88d3374c1f84cca`) in one line: an uncommitted edit by another session corrects prompt 1's expected behaviour to label 25.47% as profit before exceptional items and tax and to give the EBIT margin of about 24.0%. The prompts themselves are identical; this run did not edit the file.
- Clock: frozen at `2026-10-30T17:00:00+05:30`. Provider: Vertex Gemini through the Copilot's configured models; SDK pinned at `google-genai==1.47.0` in a run-owned virtualenv (the host has 1.3.0).
- Build (exported from these commits, so uncommitted edits could not leak in): intelligence `1b10785ebb`, data-platform `c8d300fe73`, query-api `e0d39522d6`, broker-portfolio `629e32114b`.
- Uncommitted files present in the working trees and **not** used: intelligence: tests/test_signed_off_numerical_expectations_l08.py; data-platform: app/services/indices/contract_backfill.py, tests/test_index_contracts_migration_postgres.py, reports/announcement-completeness/.
- Owned stack: its own evaluation server on port 50641 (proved to be this run's child process), its own Redis on port 50625, its own database `anvest_golden_20Z_2c17c9_test` (created and dropped by the run, warehouse tables read-only through foreign tables).
- Data: the Mac warehouse as it stood on 1 November 2026 (not production). `feature_store_daily` was copied as a 60-day slice ending 15 October 2026 (247431 rows) because the full 195 GB table over foreign-table links made one bank question run longer than six minutes. Everything else was read live through read-only foreign tables.
- Spend: measured exposure rose from 7.5995 to 11.8343 INR; the timed-out or errored attempt is held as uncertain at its reservation. Aggregate exposure across all runs is 126.83 of 1,000 INR (`spend-journal.jsonl`).
- Receipt: `docs/autonomous-run-2026-10-30/golden-50-r2/main-run/receipt.json`, sha256 `79aa247ba202d72b3a7aa8708dee0753c1bd5a3ca43be3998804c8bce6f2ca68`. Machine verdicts: `GOLDEN_EVALUATION_RESULT_2026-11-01_golden_20261101T152520Z_2c17c9.json`.

## Earlier attempts, kept as different-build attempts

A first capture (36 of 50 answered at intelligence `fe6bfa0`; 14 missing: five timeouts and nine HTTP 401 after the session token expired) and a nine-case retry (8 answered at `ae646b0`) exist. They ran on two different builds with a shared port and database, so their union is not a result and neither is scored here.

## How slots were judged

Each answer was read in full. PASS needs the requested scope, correct figures where it gives any, and the stated boundary behaviour; a wrong or unsupported figure, a missing part, the wrong subject or a missing required explanation is FAIL. Figures in answers G01, G02, G06 and G07 were recomputed from the captured TCS, Infosys, HCLTech and Wipro Q2 FY27 and Q2 FY26 consolidated XBRL filings (`golden-50-r2/primary/`, hashes in the machine file): the margins and PAT growth the system gave are correct, and those answers fail on scope. No competitor output was used.

## Top failure causes

| Cause | Slots | What it means |
|---|---|---|
| wrong_route | 12 (G03, G04, G10, G11, G24, G29, G32, G35, G39, G41, G42, G45) | The question reached a handler for a different job: company-pair disambiguation, a screener, a recent-filings list. |
| scope_incomplete | 9 (G01, G02, G06, G07, G18, G19, G20, G33, G36) | Figures given are right but a requested part is missing. |
| generic_prose | 7 (G15, G21, G25, G26, G27, G28, G30) | A textbook explanation instead of the company's data. |
| declined_data | 6 (G05, G09, G13, G14, G16, G23) | Said the figure is not in the sources, in cases where the filing is expected to carry it. |
| wrong_answer | 2 (G08, G17) | Answered a different question. |
| boundary_incomplete | 2 (G31, G40) | Withheld the figure but did not give the required explanation. |
| wrong_period | 1 (G12) | Answered for a different quarter without saying the requested one is unavailable. |
| wrong_subject | 1 (G22) | Answered about an unrelated company. |
| wrong_scope | 1 (G38) | Delivered content unrelated to the requested measure. |
| error | 1 (G49) | The stream ended in an internal error. |
| wrong_claim | 1 (G50) | Correct boundary, false statement of coverage. |

The seven passes are all declinations or product-boundary answers (G34, G37, G43, G44, G46, G47, G48). No numeric-extraction prompt in sections A to C passed, although the figures Anvest did give for the four checked companies were correct.

## Latency

Most slots answered in under ten seconds. Six slots took about three minutes each (G32, G35, G36, G39, G41, G46): all went through the screener, whose queries run through foreign-table links in this harness. That latency belongs to the evaluation environment and is not a production measurement.

## Fixed after the run, not re-measured

- G49: an allocation question missing its amount, age, horizon or risk profile now returns a clarification instead of HTTP 500 (intelligence `097574e`). This result still counts G49 as failed.

## Verdicts

| # | Verdict | Seconds | Cause | Observation |
|---|---|---:|---|---|
| G01 | FAIL | 4.0 | scope_incomplete | EBIT margin 23.98% (prior year 25.18%) and net margin 18.70% match the TCS filings, but revenue and PAT are never stated and the filing link is not given. |
| G02 | FAIL | 4.4 | scope_incomplete | Margins match the filings, but one net margin per company is given; the two denominators (total income and operating revenue) are not shown. |
| G03 | FAIL | 4.0 | wrong_route | Treated 'Consolidated' as a company name and asked which of two unrelated issuers was meant. |
| G04 | FAIL | 3.0 | wrong_route | Asked which company to compare Reliance with; no EBITDA margin. |
| G05 | FAIL | 4.5 | declined_data | Gives no quarterly revenue figures and says the series was not compiled. |
| G06 | FAIL | 1.3 | scope_incomplete | Margin 16.10% on revenue from operations is labelled and matches the filing; the operating profit amount (about 3,986 crore) is not stated, and the prior-year net margin 13.73% differs from the filing's 13.80%. |
| G07 | FAIL | 2.8 | scope_incomplete | PAT growth +14.86% / +6.28% / +21.15% match the filings; the prior-year bases (12,131 / 7,375 / 4,236 crore) the prompt asks for are not shown. |
| G08 | FAIL | 2.0 | wrong_answer | Returned an overall quality score and profit growth; no basic or diluted EPS. |
| G09 | FAIL | 3.5 | declined_data | Says net interest income is not in the filing; none given. |
| G10 | FAIL | 2.6 | wrong_route | Asked which company to compare Bharti Airtel with. |
| G11 | FAIL | 6.2 | wrong_route | Gave revenue and profit growth and a score, added an unrelated company (NETWEB); no NII, net profit amounts or provisions. |
| G12 | FAIL | 8.2 | wrong_period | Gave gross NPA 1.47% and net NPA 0.38% for the quarter ended 30 June 2026, not Q2 FY27; no provision coverage ratio. No Q2 FY27 SBI filing is in the warehouse. |
| G13 | FAIL | 4.0 | declined_data | Says operating profit and slippages were not disclosed in the provided sources. |
| G14 | FAIL | 1.8 | declined_data | States the filing does not report CASA ratio; no figure and no basis for the statement. |
| G15 | FAIL | 6.1 | generic_prose | Describes how OCR extraction works; no document or figures. |
| G16 | FAIL | 4.3 | declined_data | Says the growth figures were not in the source text. |
| G17 | FAIL | 0.2 | wrong_answer | Gave net margin only; neither an operating margin nor the statement that a lender has none. |
| G18 | FAIL | 1.5 | scope_incomplete | Net profit 1,912 crore stated; net interest margin not given. |
| G19 | FAIL | 3.6 | scope_incomplete | Return on assets for SBI only; none for HDFC Bank. |
| G20 | FAIL | 0.4 | scope_incomplete | Interest earned and PAT only; not the key highlights (NII, NPA, margins). |
| G21 | FAIL | 5.5 | generic_prose | General method for repairing XBRL tags; no company data. |
| G22 | FAIL | 1.3 | wrong_subject | Picked an unrelated tiny issuer (Containerway) and gave a quarter, not an FY26 annual figure. |
| G23 | FAIL | 3.6 | declined_data | Says no operating cash flow for Tata Steel is in the evidence. |
| G24 | FAIL | 3.2 | wrong_route | Asked which company to compare 'Consolidated Finvest & Holdings' with. |
| G25 | FAIL | 4.9 | generic_prose | Method text plus an unrelated mutual-fund table; no depreciation data. |
| G26 | FAIL | 4.5 | generic_prose | General reconciliation procedure; no numbers, no restatement cited. |
| G27 | FAIL | 4.9 | generic_prose | Says no verified figure and explains the ratio; no trend. |
| G28 | FAIL | 4.6 | generic_prose | General discussion; no company, no trend. |
| G29 | FAIL | 2.8 | wrong_route | Listed recent filings for large caps; no promoter holding change and no conflict. |
| G30 | FAIL | 2.7 | generic_prose | Defines the payout ratio; no company figure or restatement. |
| G31 | FAIL | 1.5 | boundary_incomplete | Withholds ROCE ('disclosures do not contain') but does not say it is not valid for lenders. |
| G32 | FAIL | 187.5 | wrong_route | Ran a debt/equity screener and listed ten non-bank companies; nothing about HDFC Bank (180 s). |
| G33 | FAIL | 3.2 | scope_incomplete | Says the comparison is not feasible for the bank but gives no TCS working-capital turnover; adds an unrelated growth table. |
| G34 | PASS | 1.7 |  | States inventory turnover is not applicable to an IT services company; no figure invented. |
| G35 | FAIL | 181.8 | wrong_route | Listed ten non-financial companies by ROCE for an NBFC screen (182 s). |
| G36 | FAIL | 179.5 | scope_incomplete | Listed ten stocks by ROE; no exact match count, no D/E filter shown, no costed backtest (180 s). |
| G37 | PASS | 5.8 |  | Explains that insurers' underwriting and investment results are evaluated separately; no figure invented. |
| G38 | FAIL | 5.8 | wrong_scope | Notes FCF is less meaningful for banks but replaces the yield comparison with a risk/liquidity/tax table that has nothing to do with FCF yield. |
| G39 | FAIL | 178.0 | wrong_route | Listed ten companies by ROCE level; no three-year improvement test (178 s). |
| G40 | FAIL | 3.2 | boundary_incomplete | Says the ratio is not available; does not say it is not meaningful for a bank. |
| G41 | FAIL | 180.0 | wrong_route | Listed ten small caps by market cap; no coverage-gap statement (180 s). |
| G42 | FAIL | 3.1 | wrong_route | Listed recent IPOs; does not say pre-listing financials are not held. |
| G43 | PASS | 1.6 |  | Declines to give a FY28 revenue figure; frames it as absent from disclosures rather than as a policy of no forecasts. |
| G44 | PASS | 0.0 |  | Declines price targets; no consensus figure given. |
| G45 | FAIL | 4.4 | wrong_route | Read 'Bloomberg' as a company and asked which to compare with. |
| G46 | PASS | 177.4 |  | States it gives no investment advice and names no stock; the screen it ran took 177 s and found nothing. |
| G47 | PASS | 0.0 |  | Declines a personal recommendation. |
| G48 | PASS | 0.0 |  | Declines a buy decision and a target price. |
| G49 | FAIL | 2.4 | error | The stream ended in HTTP 500 (KeyError 'allocation'); no answer. Fixed afterwards in intelligence 097574e, not re-measured. |
| G50 | FAIL | 1.8 | wrong_claim | Declines to predict, but says 'Nifty 50 isn't covered in Anvest data', which is false for the product. |

## Limits

One reviewer, one run, one attempt per prompt, the Mac warehouse rather than production, and generic prompts G15, G21, G25 to G30, G41 and G42 whose bracketed or unspecified subjects make the expected behaviour a judgement. The same weaknesses apply to every score here. A pass rate from this run says nothing about leadership and cannot certify a release.
