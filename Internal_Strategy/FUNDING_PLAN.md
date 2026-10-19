# Anvest — Current Funding Plan

**INTERNAL — not for sharing. Updated 14 October 2026; positioning revised and the operating model added 19 October 2026 (materials dated 20 October 2026; see [PITCH_REVIEW_2026-10-19.md](PITCH_REVIEW_2026-10-19.md)).**

## Company and positioning

Anvest is India's AI research co-pilot: cited filing answers, costed backtests and portfolio impact, for SEBI-registered professionals and serious investors. One question flows into a cited answer, an AI-built screen, a cost-realistic backtest and paper trading. Stock, IPO, mutual fund, bond and wealth tools sit in the same workspace. The verified warehouse and dedicated engines supply evidence, calculations and simulations.

Two revenue engines carry this round: Desk seats for professionals (RAs, IAs, PMS desks and distributors, 1–5+ seats) and an Intelligence API/MCP licence for brokers, wealth apps and AI agents, priced per active user with volume tiers. Retail Plus/Pro subscriptions are self-serve upside from the free funnel. Research-backed, exchange-registered strategies through partner brokers follow SEBI RA registration and exchange empanelment, after the Series A.

## Current round

| Item | Working plan |
|---|---|
| Headline raise | $500,000 |
| First close | $400,000 |
| Room to | $700,000 |
| Post-money cap | $3.5 million, same stated cap across the round |
| Instrument | CCD/CCPS; exact structure to be confirmed with counsel |
| Runway | At $500K, revenue covers costs by about month 42 with cash never below about ₹51 L, without new funding. At $400K, cash lasts about 31 months. |
| Founder | Harsh Bhardwaj, full-time on Anvest from the close of this round; IP arrangements to be confirmed in diligence |

Lead with $500K. The first close at $400K needs an institutional lead plus angels, larger angel commitments, or a clearly defined smaller initial close. Four to six ₹10–25 lakh cheques alone cannot fill it. See [INVESTOR_TARGETING_PLAN.md](INVESTOR_TARGETING_PLAN.md) for sequencing and investor priorities. Historical cheque ranges and fund theses require verification before outreach.

## Use of funds

| Allocation | $400K | $500K | $700K | Purpose |
|---|---:|---:|---:|---|
| Team | $155K | $185K | $195K | Growth lead, data engineer, full-stack/quant engineer; a second seller from month 9 at $500K (month 6 at $700K) |
| Compliance and infrastructure | $60K | $65K | $65K | SEBI RA registration and counsel, exchange data licence, serving and inference |
| Growth and founder | $100K | $100K | $125K | Desk pilots, launch, CAC tests and founder salary |
| Reserve and runway | $85K | $150K | $315K | Cash held beyond the 18-month spend |
| Total | $400K | $500K | $700K | |

The budget funds the first revenue engines. Strategy revenue begins only after RA registration, exchange empanelment and a partner broker, and no brokerage or HFT business is funded by it.

## This round's operating plan, and the long-term scenario

All figures come from [operating_model.py](../Financial_Models/operating_model.py), a monthly model of users, conversion, churn, seller capacity, partner usage, pricing, salaries, serving, data, compliance and growth spend. It also writes [Anvest_Operating_Model.xlsx](../Financial_Models/Anvest_Operating_Model.xlsx) for the data room. Every input is a planning assumption, not measured conversion or contracted revenue.

| Month 15 | $400K first close | $500K target | $700K maximum |
|---|---:|---:|---:|
| Net MRR | ₹5.7 L | ₹7.3 L | ₹8.8 L |
| ARR run-rate | ₹68 L (~$72K) | ₹87 L (~$92K) | ₹1.06 Cr (~$112K) |
| Desk teams (seats) | 55 (~173) | 77 (~243) | 88 (~276) |
| Paying partner integrations | 2 | 2 | 3 |
| Retail subscribers | ~186 | ~186 | ~230 |
| Net burn per month | ₹13.9 L | ₹15.4 L | ₹15.6 L |
| Plan spend, months 1–18 | ₹3.0 Cr | ₹3.3 Cr | ₹3.7 Cr |
| Without new funding | cash to month 31 | break-even month 42 | break-even month 40 |

Key drivers: the founder sells one team a month from month 3; each seller adds four teams a month once ramped (half rate for the first two months); teams average three seats (1–5+ seat plans) at about ₹2,245 net per seat after GST and discounts, with 2% monthly churn. Partners go live at months 10 and 14 with 4,000 active users each, growing 6% a month, priced ₹15 → ₹10 → ₹6 per user by volume band.

Unit economics at $500K: gross margin about 46% at month 15, because fixed serving and data costs sit on a small base; about 83% at year-5 scale. Desk CAC is about ₹0.73 lakh per team, repaid by about 11 months of team revenue (about 23 months of team gross margin).

**Long-term scenario (conditional, not funded by this round).** Built on the $500K plan, it assumes a Series A near month 18 that funds sellers (15 including the founder by year 5) and marketing, eight more partner integrations from month 20 at 10,000 users each, and strategy subscriptions from month 22 once SEBI RA registration, exchange empanelment and a partner broker are in place. Exit ARR: ₹2.3 Cr in year 2, ₹6.5 Cr in year 3, ₹13.2 Cr in year 4 and ₹23.1 Cr (~$2.4M) in year 5. Desk and retail account for ₹13.4 Cr of year 5; partners and strategies add ₹9.7 Cr only if their gates clear.

The journey review figures (base ₹83 L ARR, 43 teams, a ₹29.9 Cr year 5) and every earlier case are superseded; the pitch review records why. The other month-15 milestones are SEBI RA registration and a published head-to-head benchmark.

After any change to the model or the materials, run `/opt/homebrew/bin/python3 ../check_materials.py`. [PRICING_AND_UNIT_ECONOMICS.md](../Financial_Models/PRICING_AND_UNIT_ECONOMICS.md) remains the dated reference for tier design and unit costs; re-measure cost per answer after the October model migration.

## Execution and evidence

Follow [GTM_PLAN.md](GTM_PLAN.md): sell one recurring professional job, improve reliability, measure retail workflows and expand the channels that show retained paid use. The first 90 days after close target 200 RA, IA and PMS firms, 40 live demos and 10 paid Desk pilots, plus live checkout, the full sitemap and a first broker MCP pilot. Selected investor conversations can proceed in parallel with the customer work. No Desk pilot outreach has started yet; do not describe pilots as underway.

The 20 October production extract records 31 registered accounts, 418 logged research queries across 16 accounts, 238 saved backtest records and 2 saved screens, including founder/testing. These replace the unsupported approximately 100 sign-up claim. Measure external activation, repeat use and paid pilots separately. Pre-revenue remains the documented status until actual receipts establish otherwise.

## Expansion

Deeper education and wealth-planning workflows follow customer evidence. Exchange-registered strategies through partner brokers are the main growth-stage opportunity: they build on the live backtesting and paper-trading stack and on the RA registration this round funds. Licensed wealth services, brokerage, other markets and advanced quant research need separate economics, operating readiness and approvals; the deck's appendix roadmap lists them as H3.

## Diligence and materials

The operational checklist and Q&A are in [INVESTOR_TARGETING_PLAN.md](INVESTOR_TARGETING_PLAN.md). The broker/data audit is [LIVE_DATA_AND_BROKER_STRATEGY.md](LIVE_DATA_AND_BROKER_STRATEGY.md), explicitly dated 9 October. Use [README.md](../README.md) to select shareable files; the tracker and planning documents stay internal.

## Market expansion and funding paths (20 October 2026)

The $500K target case reaches month-42 break-even without new funding under the model assumptions. The separate Series A scenario scales to approximately ₹23.1 Cr Year-5 ARR: ₹13.4 Cr from Desk and retail plus ₹9.7 Cr from conditional partner and strategy revenue, rounded. Years 3–5 expand Desk into broader distribution professionals, family offices and CA/wealth practices. The 4,132 Year-5 seats would equal 19% of the initial 21,750-seat professional SAM, so the initial segment alone is not the growth plan. The broader ₹1,284 Cr professional TAM is a list-price opportunity, not a count of signed customers or unique firms: ARN and EUIN holders are people/registrations.

Scenario expenses now include every added seller's salary and higher marketing from months 19 and 37. Scenario cash excludes an unspecified Series A amount and is an unfunded balance, not a funded runway promise. Revenue remains a planning scenario. No later approvals or contracts are presumed complete.

Production snapshot, 20 October 2026: 31 registered accounts; 418 logged research queries across 16 accounts; 238 saved backtest records; 2 saved screens. These include founder and testing activity. They are not paid-customer, retention, completed-run or external-user metrics. Source audit: revenue and PAT matched 50 of 50 recent consolidated Q2 FY27 NSE XBRL filings; this measures line-item extraction, not full AI answer accuracy.
