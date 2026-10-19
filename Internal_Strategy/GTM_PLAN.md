# Anvest — Current Go-to-Market Plan

**INTERNAL — not for sharing. Updated 14 October 2026; synced with the materials on 20 October 2026.**

## Product and customer entry point

Anvest offers one AI experience across investing tasks. Users ask in plain English and receive explanations with links into relevant workflows. Live tools include cited filing research, AI screening, portfolio X-ray, historical backtesting, paper trading, wealth planning, calculators and educational guides.

The first paid customer test is a professional team reviewing disclosures across a coverage list. Sell that recurring job first. Retail workflows test the longer-term platform opportunity without assuming that every module retains users or earns revenue.

## First 90 days from 14 October

| Period | Work | Evidence |
|---|---|---|
| Days 1–7 | Verify registration counts, instrument activation and repeat use, check the demo flow, review serving and broker/data dependencies | Dated metrics and a reliable demonstration |
| Days 8–30 | Interview professional prospects, demonstrate their actual workflow and offer paid pilots | Paid pilots, task frequency, time saved and recorded objections |
| Days 31–60 | Improve the workflow customers repeat, answer quality and reliability | Weekly use, renewals or repeat invoices, support burden and fully loaded cost |
| Days 61–90 | Expand sales and distribution where retained paid use supports it | Measured prospect-to-paid funnel and credible customer economics |

**After the round closes, the first 90 days target:** a short list of 200 RA, IA and PMS firms, 40 live demos and 10 paid Desk pilots, with live checkout, the full sitemap submitted and a first broker MCP pilot. Seats are paid from month 3 in the operating model. No pilot outreach has started yet (19 Oct 2026).

These are work periods, not a forecast of traction. The proposed outreach count and conversion rates remain hypotheses until measured. Track contact and follow-up status in `../Outreach/Anvest_Investor_Tracker.xlsx`, using the current targeting plan for priorities rather than older workbook rankings.

## Professional sales

1. Choose a narrow group of analysts, boutique PMS or advisory desks with a repeated filing-review task.
2. Demonstrate that task using a coverage list they recognise and disclose missing or stale data.
3. Agree pilot scope, price, duration and success criteria.
4. Measure repeated use, accepted answers, time saved and renewal. An unpaid expression of interest is not revenue.

Desk is ₹2,999 per seat per month at launch pricing, sold in 1–5+ seat plans so solo RAs and IAs can start small; the model assumes three seats per team on average. Billing goes live in the first 90 days after close; until then the materials call it launch pricing. Test seat count and team minimums through actual buying behaviour. See `../Financial_Models/PRICING_AND_UNIT_ECONOMICS.md` for the dated baseline model.

## Retail learning and conversion

Measure whether AI-led transitions help users complete tasks:

- Research question to a useful answer or prepared screen.
- Screen to a historical backtest.
- Backtest to paper practice and journal review.
- Wealth or calculator question to an understood scenario and later revisit.
- Guide or explanation to successful use of a tool.

Record activation, repeat use, paid conversion and task cost by workflow and cohort. Cross-tool clicks alone are not value or retention. Keep simulated performance distinct from realised investment outcomes.

## Acquisition channels

Four channels, in this order: (1) founder-led sales to the 3,900 SEBI-registered firms, starting with 1–5 seat boutiques, then distribution professionals; (2) search built from source data — 6K+ stock, 991 fund, IPO and bond pages answering long-tail filing queries, once the full sitemap ships; (3) broker and wealth-app integrations through the API and MCP; (4) shareable cited answers, screens and backtests, with education creators on referral terms reviewed by counsel within SEBI's finfluencer rules. Increase acquisition spending only after identifying a retained, affordable customer workflow.

## Broker partners

Use the strategic integration deck for an 8–12 week scoped read-only research pilot with an opted-in cohort and agreed metrics. Keep its commercial discussion separate from fundraising. The retained deck contains Zerodha/Kite-specific content; adapt it before pitching another broker.

## Demo observation

On 19 October the signed-in journey passed end to end: "Find profitable companies with high ROE and low debt" produced a 516-stock screen (profit margin > 0, ROE > 15%, D/E < 1), a one-year costed backtest and a 10-stock paper basket (pitch review §5). Earlier, on 14 October, a home-screen question requesting profitable companies with ROCE above 20% and debt-to-equity below 0.5 produced a prepared screener link. Opening it loaded the formula and a results table. The chat initially reported a stock-loading fallback. Recheck that full path before an investor demonstration. This observation does not certify the warehouse's numerical accuracy.

## Scope and expansion

Improve reliability and test paid research use during this round. Deepen existing AI learning, strategy and planning workflows where customer evidence supports them.

**This round's operating plan** (`../Financial_Models/operating_model.py`) counts Desk seats, retail subscriptions and paid partner integrations only: ₹87 L ARR run-rate at month 15 on the $500K plan, ₹68 L at the $400K first close and ₹1.06 Cr at $700K. **The long-term scenario** adds strategy subscriptions, from month 22 at the earliest, and more partner contracts. Both are conditional on a Series A, SEBI RA registration, exchange empanelment, a partner broker and signed partner agreements, and they do not change this round's budget. Advisory services, brokerage, international markets and HFT keep their separate gates in `INVESTOR_TARGETING_PLAN.md`.

## Market expansion and funding paths (20 October 2026)

The $500K target case reaches month-42 break-even without new funding under the model assumptions. The separate Series A scenario scales to approximately ₹23.1 Cr Year-5 ARR: ₹13.4 Cr from Desk and retail plus ₹9.7 Cr from conditional partner and strategy revenue, rounded. Years 3–5 expand Desk into broader distribution professionals, family offices and CA/wealth practices. The 4,132 Year-5 seats would equal 19% of the initial 21,750-seat professional SAM, so the initial segment alone is not the growth plan. The broader ₹1,284 Cr professional TAM is a list-price opportunity, not a count of signed customers or unique firms: ARN and EUIN holders are people/registrations.

Scenario expenses now include every added seller's salary and higher marketing from months 19 and 37. Scenario cash excludes an unspecified Series A amount and is an unfunded balance, not a funded runway promise. Revenue remains a planning scenario. No later approvals or contracts are presumed complete.

Production snapshot, 20 October 2026: 31 registered accounts; 418 logged research queries across 16 accounts; 238 saved backtest records; 2 saved screens. These include founder and testing activity. They are not paid-customer, retention, completed-run or external-user metrics. Source audit: revenue and PAT matched 50 of 50 recent consolidated Q2 FY27 NSE XBRL filings; this measures line-item extraction, not full AI answer accuracy.
