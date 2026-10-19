# Investor materials: evidence and review record

**Internal. Updated 20 October 2026.** Current decks contain 16 main slides plus 5 appendix slides for seed investors and 10 slides for the Zerodha partner proposal. Public materials carry the date only. Prior materials remain in `../Archive/`; they are historical and must not be sent.

## Positioning and founder decisions

Anvest is India's AI research co-pilot for SEBI-registered professionals and serious investors. Cited filing answers connect to editable screens, costed backtests, paper practice and portfolio planning. Desk and partner API/MCP licences are the commercial priorities. Retail is self-serve upside. Live strategies require approvals and partner contracts.

The founder goes full-time at round close. The adviser bench is being built; no adviser or design partner is named. No pilot outreach or paying-customer traction is claimed. The ask leads with $500K, first close $400K and room to $700K, at a $3.5M post-money cap, with the instrument subject to counsel.

## Current production evidence

Read-only production extracts and source checks live in `../Source/evidence_snapshot.json`, `filing_selection.json` and `filing_check.json`. Scripts alongside them reproduce the queries and checks. The extract ran just after midnight IST on 20 October.

| Metric | Result | Scope and limitation |
|---|---:|---|
| Announcement-date records, Jul / Aug / Sep 2026 | 45,997 / 61,875 / 38,558 | IST month boundaries; Q2 FY27 average 48,810/month, shown as ~49K. Records in the warehouse, not a count of unique PDFs. |
| Corporate-announcement rows | 2,937,136 | Rounded to 2.94M in current materials |
| Current dashboard symbols | 6,086 | Separate scope from all active symbols and historical profiles |
| Non-empty AI profiles, distinct symbols | 6,119 | Warehouse scope, including symbols outside the current dashboard |
| Registered accounts | 31 | Includes founder and test accounts; replaces unsupported ~100 claim |
| Logged research queries / accounts | 418 / 16 | Includes founder/testing; not a count of satisfied external customers |
| Saved backtest records | 238 | Not a completed-run counter or retained-user measure |
| Saved screens | 2 | Not all screen executions |

The old ~17K/month number counted ingestion dates in June–July. August's ingestion count includes a large backfill; ingestion dates cannot establish monthly filing supply. Current materials use announcement dates instead. All page counts are rounded to 6K+ to avoid conflating the dashboard, symbols table and profile universe. The preserved flow screenshot is a dated historical demonstration and still shows its original count.

The 1.35M indexed passages and approximately 584K parsed filings remain explicitly dated 19 October snapshots, not independently recounted by this pass. The data-quality moat metrics retain their original audit scope: 15,899 recovered cash-flow rows, 3,608 conflicting source figures across 1,022 companies, and 10 scanned bank filings in the Q1 FY27 sample. They are not a general accuracy rate.

## Fifty-filing source audit

The frozen selection is the latest 50 distinct consolidated Q2 FY27 companies in production with a September-quarter revenue line, PAT and an NSE XBRL link, ordered by filing date descending, then symbol. It is a deterministic convenience sample, not a random holdout.

All **50 of 50** matched revenue and PAT to downloaded NSE XBRL facts. The checker independently checks the original document's consolidated basis, July–September duration, context, currency unit and exact values, and stores a SHA-256 for each source. Missing sources and ambiguous facts fail. No model or serving API was called. This is an extraction audit, not a fifty-answer AI benchmark. The main traction slide and one-pager say so.

The earlier live spot-check involved TCS, HCL Technologies and Wipro answers, plus an Infosys decline. Keep that four-question observation separate. It does not establish general accuracy. A release-quality independent answer benchmark and a head-to-head competitor comparison remain outstanding.

## TCS margin clarification and code

For Q2 FY27 consolidated TCS, revenue from operations is ₹73,188 Cr, total income ₹74,525 Cr and PAT ₹13,934 Cr. PAT / total income is 18.70%; PAT / revenue from operations is 19.04%. These are different definitions, not inconsistent PAT figures. Operating margin was 25.47% versus 26.14% a year earlier, down 67 bps using the displayed two-decimal margins.

The preserved cover screenshot is the real 19 October production answer. No screenshot text or pixels were fabricated. Its caption supplies the denominator and YoY change. The partner deck's editable text uses the clarified answer. The broker response code now names the actual net-margin denominator, computes the YoY basis-point change and shares one company/period header when both results and margins are requested. Three new regression tests and the existing intelligence tests passed: 60 tests in an isolated database. The source fix is committed locally as broker `18b988d`, not deployed.

## Model and market reconciliation

`../Financial_Models/operating_model.py` remains the source of planning figures. All figures are assumptions, not signed revenue or a forecast. ₹95/$ is a fixed planning rate from the 16 October reference, not a claim about today's FX.

| Month 15 | $400K first close | $500K target | $700K maximum |
|---|---:|---:|---:|
| ARR run-rate | ₹68 L | ₹87 L | ₹1.06 Cr |
| Desk teams / seats | 55 / ~173 | 77 / ~243 | 88 / ~276 |
| Paying partner target | 2 | 2 | 3 |
| Net burn / month | ₹13.9 L | ₹15.4 L | ₹15.6 L |
| Cash path without new funding | Cash to M31; top-up needed | M42 break-even | M40 break-even |

The deck distinguishes two paths: the $500K default-alive case reaches M42 break-even under its assumptions, while a separate Series A scenario scales to about ₹23.1 Cr Year-5 ARR. Its rounded components are ₹13.4 Cr Desk/retail plus ₹9.7 Cr partners/strategies. The scenario now includes salaries for all additional sellers and marketing of ₹6 L/month from M19 and ₹10 L/month from M37; the earlier code added sales capacity without its salary expense. The scale scenario also now preserves the target case exactly through M18 before partner growth changes from 6% to 5%; correcting the earlier inconsistent start changes Year-5 ARR from ₹22.99 Cr to ₹23.11 Cr, still about ₹23 Cr. Scenario cash excludes an unspecified Series A amount and must be read as the unfunded cash balance.

Year-5 Desk seats (4,132) equal 19% of the initial 21,750-seat professional SAM. Years 3–5 therefore expand to broader distributors, family offices and CA/wealth practices. This is now beside the appendix assumptions and reflected in all funding/GTM documents. ARN and EUIN counts describe distribution professionals/registrations, not that many unique firms. Professional and retail opportunities can overlap; the market estimate is a gross list-price opportunity, not a deduplicated customer census.

## Product and mobile demo status

The QR decodes to the real public screener with `profit_margin > 0 AND roe > 15 AND debt_to_equity < 1`. A clean, signed-out iPhone 13 browser replay on 20 October returned HTTP 200, 533 matches, no page errors and no horizontal document overflow. ITC showed 22.41%. The historical 19 October flow screenshot shows 516 matches; live counts change. It remains unchanged by founder instruction. This was a browser mobile emulation check, not a physical phone scan.

The 19 October canonical VM runbook records that the inline screener connectivity and memory settings shipped while holding broker image `dac19f8`; frontend `cc42014` shipped the references fix. The first-run backtest, paper-return denominator and broker step-up changes remain held behind the separate broker release decision. A reviewed hotfix branch based on `dac19f8` exists. The analyst rebuild must not ship incidentally: its sealed independent release holdout and release decision are absent. This pass did not push, deploy, lift the gate or alter production state.

Before a live backtest demo, pre-run the same date window to warm the existing 24-hour cache. Avoid adding virtual cash after opening paper positions until the broker fix ships. These are temporary presenter precautions, not fixes or release evidence.

## Other corrections

- Removed public draft labels and internal build terminology. Speaker notes retain investor talking points and source context.
- Removed the unsupported “Only Anvest” statement and zero-CAC assertions. Organic distribution still carries content and operating costs.
- Marked team workspaces as planned instead of presenting every commercial capability as live.
- Repaired invalid negative chart-axis ids and dangling partner-deck content-type entries while preserving native tables/charts and all screenshot bytes.
- Recovered one-pager/memo templates from temporary files into `../Source/` and added reproducible edit, export and audit scripts.
- Added Strategy to the workspace snapshot mapping so materials and code have local Git recovery. No GitHub publication is implied.

## Sources and remaining diligence

The deck's existing competitor matrix remains a dated 19 October public-page comparison, not a hands-on benchmark. Sources: [Trendlyne](https://trendlyne.com/features/matrix/), [Screener Premium](https://www.screener.in/premium/), [Tijori](https://www.tijorifinance.com/), [Tickertape](https://www.tickertape.in/premium), [StockGro](https://www.stockgro.club/faq/), [Streak](https://streak.tech/). A dash means not found on those pages, not proven unavailable. Jio's screenshot remains real; the price band and dates also appear in [Reliance's exchange announcement](https://links.sgx.com/FileOpen/RIL_SE_14102026_.ashx?App=Announcement&FileID=907073). The ₹30,213 Cr maximum is 27 crore shares at ₹1,119. These are IPO terms, not an Anvest projection.

Before sending: obtain counsel's review of investment terms, IP/employer clauses, licensing and registration posture; confirm founder/adviser status and any new pilot claims; fill email and partner placeholders; run `../check_materials.py`. Payment checkout and the complete sitemap remain first-90-days deliverables. Measure external activation/retention before describing registered accounts or internal tests as customer traction.
