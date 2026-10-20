# Anvest — Subscription Model, Unit Economics & Billing Design

**Date:** 2026-08-31 · **Status:** investigation complete, engineering plan not yet started
**Companion docs:** `GTM_PLAN.md` (§4 Phase-2 pricing — this doc supersedes its pricing numbers and keeps its phasing), `FUNDING_PLAN.md` (§7.2 use of funds — team costs taken from there), `docs/ai-enrichment-cost-architecture-2026-08.md`, `docs/copilot_eval_2026-07-29.md`
**FX used throughout:** **₹95.69/USD** (30 Aug 2026). `FUNDING_PLAN.md` uses ₹96.57 from 26 Jul — re-check before quoting either.

---

## 0. The three findings that should change the plan

Read these first; everything else is supporting work.

1. **Price is not the margin lever. The free tier's AI allowance is.** At 3% free→paid conversion there are 32 free users per paying user. Giving each of them 10 copilot questions a month drops blended gross margin to **38.6%** at 2,500 subscribers. Giving them 3 puts it at **70.0%**. Same prices, same infrastructure, same product. (§5.4)

2. **Production is running on models that retire in ~6 weeks.** `ops/local-hosting/local-backend.env` pins `gemini-2.5-flash` / `gemini-2.5-flash-lite`. Google's Vertex retirement date for the 2.5 family is **16 October 2026** (release notes say 16th, lifecycle page says 20th — Google's own docs disagree, and Google says the date is not final until Gemini 3 is GA, with 6 months' notice from lock-in). Every unit-cost number in this document is therefore a *migration* number, not a current-state number. The cheapest successor, `gemini-3.1-flash-lite`, is **2.5× the input price and 3.75× the output price** of what we run today. (§3.2)

3. **Screener.in has already shipped metered AI over filings, and priced it.** ₹100/M input, ₹800/M output, **"around ₹10–30 per answer," up to ₹100** for document-heavy queries, with ₹500 of credits bundled into its ₹4,999/yr Premium. This is simultaneously our strongest competitive weapon (we can include what they meter) and proof that the incumbent is now in our category. It also means the "conversational AI over an Indian filings corpus" gap named in `GTM_PLAN.md` §3 is **no longer unoccupied**. (§4.2)

---

## 1. What is actually built, measured today

Not projections — these were read off the running system on 2026-08-31.

| Thing | Measured value | How |
|---|---|---|
| Registered users | **60** | `SELECT count(*) FROM users` |
| Anonymous visitors tracked | 37 | `anonymous_usage` |
| Authenticated usage rows | 4 | `authenticated_usage` |
| Warehouse size | **198 GB** | `pg_database_size('anvest')` |
| — of which `feature_store_daily` | **180 GB** (91%) | `pg_total_relation_size` |
| Active symbols | **5,964** | `symbols WHERE is_active` |
| Corporate announcements | **2,888,644** | row count |
| New announcements/month (steady state) | ~16–17K (Jun 15,718 · Jul 17,300) | `created_at` histogram |
| Qdrant index on disk | **28 GB** | `du -sh /qdrant/storage` |
| Frontend pages | 66 route files | `find market-ui/app -name page.tsx` |
| Backend routes | 12 query-api + 18 broker-portfolio modules | directory listing |
| Copilot services | 43 service modules | directory listing |
| **Billing code** | **none — zero matches for razorpay/stripe/cashfree/payu/paytm** | grep across all repos |
| **`users` table plan/tier column** | **none** | `data-platform/app/models/user.py` |

**Live container footprints** (`docker stats`): broker-portfolio 366 MB (1.5 GB limit) · query-api 247 MB (768 MB limit) · Qdrant 2.39 GB (6.35 GB limit) · cloudflared 36 MB. Embedding sidecar holds 450–900 MB per `WORKLOAD_PRIORITY.md`. **Nothing in the serving path is memory-hungry except Postgres and Qdrant.** That matters for VM sizing (§3.1).

### 1.1 The metering layer already exists

`data-platform/app/services/usage_limits.py` is a working PLG meter, and it is the natural insertion point for tiers — not a greenfield build:

```python
ANONYMOUS_USAGE_LIMITS   = {"stock_views": 3, "screener_runs": 3, "strategy_runs": 3}
AUTHENTICATED_USAGE_LIMITS = {"strategy_runs": 5}   # per day, resets on last_reset_at < CURRENT_DATE
```

Two counter tables (`anonymous_usage` keyed by `X-Visitor-Id`, `authenticated_usage` keyed by user, with daily reset), atomic conditional-UPDATE increments, a documented refusal to do runtime DDL, and a typed 403 payload (`LIMIT_EXCEEDED` / `DAILY_LIMIT_EXCEEDED`) the frontend already handles. Anonymous enforcement is currently **off** behind `ANVEST_ENFORCE_ANONYMOUS_RESEARCH_LIMITS`.

What it does *not* have: a plan concept, a per-plan limit table, copilot-question metering (only stock views / screener / strategy runs), monthly periods (only lifetime-anonymous and daily-authenticated), or any notion of an entitlement that survives a failed payment.

### 1.2 Rate-limit lanes are already tiered by identity

`broker-portfolio/app_factory.py` selects: authenticated+trusted (8/s, burst 80) → trusted-but-anonymous (5/s, burst 40) → global (2/s, burst 20), plus dedicated lanes for auth endpoints, screen-coverage preflight, and strategy runs. A paid tier maps cleanly onto a fourth lane. No new architecture needed.

---

## 2. What "50% profit margin" has to mean

This is the one place where a sloppy definition would make the whole document worthless, so it is settled up front.

- **Gross margin** = (net revenue − COGS) / net revenue, where COGS = LLM inference + serving infrastructure + payment fees + OCR. This is the number a SaaS business is judged on and the number we can control at launch.
- **Operating margin** = gross margin − salaries − compliance − growth spend. Including a founder salary and three hires, this is dominated by headcount at any subscriber count below ~10,000.

**Both are computed below.** The honest summary: **≥50% gross margin is reachable at ~700 subscribers and is essentially a design choice.** ≥50% *operating* margin with a 4-person team needs **~13,900 subscribers** and is a scale question, not a pricing question. Anyone who tells you a pre-PMF product can hit 50% net margin while paying three engineers is describing a much later company.

Two further deductions that are easy to forget and are applied everywhere below:

- **GST 18%.** SaaS is taxable at 18% with no concession by subscription value or customer type. Indian B2C convention is to display prices GST-inclusive, so a ₹199 sticker yields **₹168.64** of net revenue. That is a 15.3% haircut before any cost.
- **Payment fee.** Razorpay's published domestic rate is 2%, plus 18% GST *on the fee* → **2.36% effective** of the gross collected.

---

## 3. Cost model

### 3.1 Infrastructure — moving off the Mac to GCP asia-south1 (Mumbai)

`GTM_PLAN.md` §5 estimates public beta at "$150–250/mo" on a single e2-standard-4. **That figure does not survive contact with the measured system.** An e2-standard-4 is 4 vCPU / 16 GB; the warehouse is 198 GB and the vector index is 28 GB. Real prices (asia-south1, 1-year committed-use discount where noted):

| Resource | On-demand/mo | 1-yr CUD/mo |
|---|---|---|
| e2-standard-4 (4 vCPU / 16 GB) | $117.51 | $74.03 |
| e2-standard-8 (8 vCPU / 32 GB) | $235.01 | $148.06 |
| n2-standard-8 (8 vCPU / 32 GB) | $272.55 | $214.55 |
| pd-balanced | \$0.12/GB-month | — |
| pd-ssd | \$0.204/GB-month | — |

**Three configurations, costed:**

| | Config A — Minimum viable | Config B — Production split | Config C — Full cloud |
|---|---|---|---|
| App + Redis + sidecar | *(shared)* | e2-standard-4 CUD $74.03 | same as B |
| Postgres | e2-standard-8 CUD $148.06 (shared with app) | n2-standard-8 CUD $214.55 | same as B |
| Postgres disk | 400 GB pd-balanced $48 | 300 GB pd-balanced $36 | same as B |
| Qdrant | e2-standard-2 CUD $37.02 | e2-standard-4 CUD $74.03 | same as B |
| Qdrant disk | 100 GB $12 | 100 GB $12 | same as B |
| Batch/ingestion | **Mac (₹0)** | **Mac (₹0)** | e2-standard-8 spot $70 + L4 bursts ~$30 |
| Egress | $12 | $24 | $24 |
| Snapshots/backup | $15 | $25 | $25 |
| Vercel Pro | $20 | $20 | $20 |
| **Total** | **$292/mo ≈ ₹27,900** | **$480/mo ≈ ₹45,900** | **$580/mo ≈ ₹55,500** |

**Recommendation: launch on Config A, move to B when paid subscribers pass ~1,000.** Config A works because the 180 GB `feature_store_daily` table is only read by backtests, not by the serving path — page loads hit `ohlcv_daily`, `financials_*`, `stock_profiles`, all of which fit comfortably in 32 GB of page cache. The risk it carries is exactly the one `WORKLOAD_PRIORITY.md` documents: concurrent heavy analytics on `feature_store_daily` drove 7k–31k swapouts/s and timed out both the embedding and Qdrant probes. On a shared VM that becomes a user-visible outage, which is why B separates them.

**A free 47% storage cut is available now.** Sampling `feature_store_daily` shows four formula versions still resident: v3 26% · v2 26% · v1 26% · part2b 21%. Only v2/v3 are live (`anvest-v3-cutover-readiness`). Pruning v1 + part2b removes roughly **85 GB** — worth ~$10/mo on pd-balanced but far more on Cloud SQL SSD, and it shrinks every backup, restore drill and migration window. Do this *before* the migration, not after; you pay to move bytes you are going to delete.

**Variation — managed Postgres.** Cloud SQL charges ~$0.0413/vCPU-hr and ~$0.0070/GB-RAM-hr in us-central1, with SSD storage at **$0.222/GB-month**, and Asia regions run 20–40% above that. At 200 GB that is ~$44–62/month for storage alone, before compute, versus $24 self-managed on pd-balanced. Cloud SQL buys automated backups, PITR and failover. **Recommendation: self-managed on a VM at launch** — `ops/backup/` already has verified backup, verification and restore-drill scripts, so the main thing Cloud SQL sells has already been built. Revisit when there is someone other than the founder on call.

**Variation — Hetzner.** ~€40–80/month for equivalent hardware, as `GTM_PLAN.md` notes. Genuinely cheaper. Costs: ~150 ms extra RTT to Indian users on every uncached API call (the stock page fans out to ~12 panel endpoints on first paint), and a data-residency conversation with any B2B customer that has a compliance function. **Not recommended for serving; reasonable for batch.**

### 3.2 LLM inference — the number that decides everything

**Measured baseline:** `docs/copilot_eval_2026-07-29.md` records **$0.0030 per question** across a 30-question golden set on `gemini-2.5-flash`, with a 10% fast-path rate (137 ms, no model call).

Treat that number with the same suspicion the eval doc treats its own: it is 30 questions, run cold on a box concurrently running the reparser, and the harness's Precision/Recall measure entity resolution rather than retrieval. It is the best number we have and it is not a good one. **First engineering task in §8 is to re-measure it properly.**

Back-solving the prompt shape from that cost at 2.5-flash's $0.30/$2.50 per million, with output capped at 700 tokens (`ANVEST_AI_MAX_OUTPUT_TOKENS=700`), gives roughly **4,167 input + 700 output tokens per question**. Applying that same shape to every model we could migrate to:

| Model | $/M in | $/M out | Cost/question | ₹/question |
|---|---|---|---|---|
| gemini-2.5-flash — **in production, retires ~16 Oct 2026** | 0.30 | 2.50 | $0.00300 | **₹0.287** |
| gemini-2.5-flash-lite — **in production (router), same retirement** | 0.10 | 0.40 | $0.00070 | ₹0.067 |
| gemini-3.1-flash-lite | 0.25 | 1.50 | $0.00209 | **₹0.200** |
| gemini-3-flash | 0.50 | 3.00 | $0.00418 | **₹0.400** |
| gemini-3-flash, 70% context-cache hit ($0.05/M cached) | — | — | $0.00287 | ₹0.275 |
| gemini-3.5-flash | 1.50 | 9.00 | $0.01255 | ₹1.201 |

**Planning assumption used in every margin calculation below: `gemini-3-flash` at ₹0.400/question, times 0.9 for the measured 10% fast-path rate = ₹0.360 per copilot question.** That is the conservative-but-not-paranoid choice: 3.1-flash-lite for the router and simple lookups, 3-flash for synthesis. It is 39% more expensive than today's stack and we should plan for it.

**Context caching is the cheapest available optimisation and is not currently used.** Cached input is $0.05/M on 3-flash — a 10× discount. The evidence builder already has a Redis evidence cache and a question-aware cache; the same evidence blocks that get reused across turns in a thread are exactly what Vertex context caching bills at 1/10th. A 70% cache-hit rate takes ₹0.400 → ₹0.275, a 31% cut on the single largest variable cost.

**Platform-fixed AI cost (does not scale with users):**

| Line | Monthly | Basis |
|---|---|---|
| Weekly announcement enrichment | **$0.04** | measured ₹0.0053/call × 150 calls/run cap (`ai-enrichment-cost-architecture-2026-08.md`) |
| Daily AI profile refresh (delta-only, 25 symbols/day) | **$1.76** | ~1.7k tokens/symbol, one call, priced at 3-flash |
| Cloud Vision OCR | **~$35** | $1.50/1,000 pages; ~17K announcements/mo, ~30% scanned, ~3 pages each |
| **Total** | **~$37/mo ≈ ₹3,500** | |

This is the payoff from the cost architecture work in August: enrichment costs **four cents a month**. The 6,257-calls-per-3-days gate that preceded it would have been a genuine COGS line. Note one deferred item: a full `stock_profiles` regeneration is ~9,177 calls ≈ **$22 one-off** — cheap, and worth doing before launch since 5 of 8 profile sections are NULL on existing rows.

### 3.3 Payment processing

| | Razorpay | Cashfree | PayU |
|---|---|---|---|
| Domestic rate (published) | 2% (cards, UPI, netbanking, wallets) | 1.90% base; promo 1.6% for new merchants signed 18 Sep 2025 – 31 Jul 2026, 12 months, needs UPI ≥40% of volume, reverts to 1.95% above ₹1 cr/month | ~2% |
| GST on fee | 18% → **2.36% effective** | 18% → **2.24% effective** | 18% |
| Setup / AMC | **₹0 / ₹0** | ₹0 setup / **₹4,999/yr AMC** | varies |
| Subscriptions add-on | +0.9% **on cards**; UPI Autopay and eNACH at platform rate | folded into plan | — |
| Pricing transparency | fully published | quote-based | partial |
| International cards | up to 3% + GST | — | — |

**Effective cost on a ₹199 monthly charge:** Razorpay UPI Autopay ₹4.70 · Razorpay card subscription (2.9% + GST = 3.42%) ₹6.81 · Cashfree ₹4.46 (before amortising the ₹4,999 AMC, which is ₹417/month — i.e. Cashfree is only cheaper above roughly **₹174,000/month** of processed volume, ≈ 1,050 Plus subscribers).

**Recommendation: Razorpay.** Not because it is cheapest — it is not — but because (a) the published, no-AMC pricing is the right shape below ~1,000 subscribers, (b) UPI Autopay, eNACH and card mandates are all first-party rather than bolted on, and (c) `GTM_PLAN.md` week 10 already assumes it, so this is confirmation rather than a new decision. **Revisit at ~₹2L/month of processed volume**, where Cashfree's lower rate starts beating its AMC and where Razorpay's rack 2% becomes negotiable (2% is a rack rate; volume discounts exist and nobody at scale pays it).

**Do not use Stripe or a merchant-of-record (Paddle, Lemon Squeezy, Dodo) for the Indian business.** MoRs charge 5–8% and their value is handling foreign sales-tax registration — which is irrelevant when 100% of revenue is domestic and we are GST-registered anyway. They become interesting only if the H2 global expansion in `FUNDING_PLAN.md` §6.2 happens, and that is explicitly gated behind India PMF.

### 3.4 Team cost

From `FUNDING_PLAN.md` §7.2, converted at ₹95.69:

| Role | Plan figure | ₹/month |
|---|---|---|
| Founder salary | $45K / 18 mo | ~₹2.39L |
| Hire #1 — growth/content | $67K / 18 mo | ~₹3.56L |
| Hire #2 — data/backend eng | $52K / 15 mo | ~₹3.32L |
| Hire #3 — full-stack (from month 6) | $36K / 12 mo | ~₹2.87L |

These are consistent with the market: Indian software engineer averages ₹9–12 LPA in 2026, with product-company mid-levels averaging ~₹35L and Bangalore carrying a 15–20% premium. Hire #2 at ~₹40 LPA is a competitive senior offer; Hire #3 at ~₹34 LPA is mid-level. Three scenarios are modelled in §5.3: solo (₹2.0L/mo), founder + 2 engineers (₹6.5L/mo), founder + 3 hires (₹9.5L/mo).

---

## 4. Competitive analysis

### 4.1 The Indian retail research market, priced

All prices verified 2026-08-31 from vendor pages where available.

| Product | Monthly | Annual | Effective ₹/mo | What you get | AI over filings? |
|---|---|---|---|---|---|
| **Screener.in** Premium | — | **₹4,999** (incl. GST) | ₹417 | Unlimited follows, 800 stock alerts, 75 screen alerts, unlimited key insights & concall notes, segment results, CSV export, **₹500 AI credits** | **Yes — metered** |
| **Trendlyne** GuruQ | ₹310 | ₹2,190 | ₹183 | DVM scores, 1,758 screener params, 30 watchlists, 150 target alerts, 75 screener alerts, 200 backtests/yr | No |
| **Trendlyne** StratQ | — | ₹4,950–5,900 | ₹412–492 | 3,512 params, 15-min technicals, 200 watchlists, 300 alerts, 1,200 backtests/yr, SmartOptions | No |
| **Tickertape** Pro | — | **₹2,399** | ₹200 | Screener, MMI, portfolio analytics | No |
| **Tijori Finance** | ₹330 | **₹3,500** | ₹292 | 6,000+ metrics, historic data, reverse DCF, in-depth comparisons; free Mint Premium | No |
| **StockEdge** Premium | ₹399 | **₹1,649** | ₹137 | 500+ scans, 2 custom scans, 20 combination scans, fundamental/momentum scores | No |
| **StockEdge** Pro | ₹1,499 | ₹6,594 | ₹550 | 50 custom scans, chart patterns, industry sector rotation | No |
| **StockEdge** Club | ₹2,499 | ₹13,194 | ₹1,100 | + Stock AI, trade ideas, live query resolution, daily reports | Partial ("Stock AI") |
| **Finology ONE** (Ticker + Quest) | ₹299 | ~₹3,588 | ₹299 | Bundled research + education | No |
| **AlphaSense** (global B2B analogue) | — | **$15,000–20,000/seat** | ~₹1.2–1.6L/mo | Enterprise filings/transcript search + AI | Yes |

**The retail band is ₹137–550/month effective, and it is crowded.** Six credible products sit inside it. There is no room to be "the cheap one" — StockEdge Premium at ₹137/mo effective already owns that slot, and Trendlyne GuruQ at ₹183 offers 1,758 screener parameters for it.

**The gap is not price. It is the ₹550–1,100/month band, where StockEdge Pro and Club sit almost alone**, and where the only AI offering ("Stock AI", bundled into a ₹13,194/yr plan) is undifferentiated.

### 4.2 Screener AI changes the competitive picture

`GTM_PLAN.md` §3 claimed the "conversational AI over a filings corpus" cell was empty for every Indian competitor. **That is no longer true.** Screener AI is live, reads annual reports and earnings calls directly, and is explicitly positioned against exactly the substitute we positioned against: *"unlike ChatGPT, Perplexity, or Gemini, Screener AI has direct access to the official filings."*

Two consequences, one bad and one very good.

**Bad:** the incumbent with the largest DIY-investor audience in India has entered our category, and our comparison slide needs rewriting.

**Good — and it is worth more than the bad:** **they metered it, and we can include it.** Screener charges ₹100/M input and ₹800/M output, **₹10–30 per answer, up to ₹100** for document-heavy queries. Our modelled cost is **₹0.36/question**. Even granting that their answers may read more documents per query, the ₹500 of credits bundled with a ₹4,999 Premium buys roughly **17–50 answers per year**.

That is a straight, verifiable, published-price comparison:

> Screener Premium: ₹4,999/yr, ~17–50 AI answers included, then ₹10–30 each.
> Anvest Pro: ₹4,999/yr, **1,500 answers included** — which would cost **₹15,000–45,000** at Screener's own published rates.

Our own included-answer cost at 1,500/yr is **₹540**, against ₹4,236 of net-of-GST revenue. We can afford this comfortably; they apparently cannot, or have chosen not to. **This should be the single headline of the pricing page.**

The reason we can and they can't is architectural, and it is the thing to say when asked: their cost per answer scales with how many documents the model reads, because the model does the reading. Ours does not, because the retrieval layer (bge-m3 over a pre-chunked corpus) does the reading and the model receives a bounded ~4K-token evidence pack. Metered pricing is what you build when you cannot bound your own input.

### 4.3 Where Anvest genuinely differentiates

Standing on the measured system, not the roadmap:

- **Grounded-or-silent with rendered citations**, plus a generate→verify→self-repair loop across five copilots (`copilot_verification.generate_verified`). Nobody in the retail band ships numerical post-validation.
- **2.89M corporate announcements**, OCR'd and vectorised. Screener AI reads annual reports and concalls; the announcement stream — where the actual surprises live — is ours.
- **ITR module.** No research competitor has it. Counter-seasonal acquisition (Jun–Sep) with a portfolio-data payload.
- **NL→DSL screener with self-correction**, versus formula syntax everywhere else.
- **Strategy/backtest lab** — StockEdge and Trendlyne sell backtest *counts* (200/yr on GuruQ, 1,200/yr on StratQ), which tells us it is a scarce, chargeable unit in this market. Our backtester runs 4.2–4.4s on a quiet machine.

And the honest counter-column: **end-of-day prices, not live**; the 30-question eval suite cannot yet prove retrieval quality; `B8` consolidated-financials gaps remain for ~4,517 symbol-FY periods; and there are 60 registered users.

### 4.4 Are businesses a viable customer? Yes — and probably first

`FUNDING_PLAN.md` §4.4 already makes this argument and the cost model confirms it decisively: **40 B2B seats at ₹2,999/mo = ₹1.2L MRR, versus 100 retail Pro subs at ₹417/mo = ₹42K MRR.** One needs ~150 conversations; the other needs thousands of free users, months of SEO, and a payments funnel.

The margin math is even more lopsided than the revenue math (§5.2): a Desk seat carries **90.8% contribution margin at typical usage and 65.1% even at a 2,000-question monthly cap**, because B2B price is 15× retail while B2B usage is only ~5× retail.

Three distinct business segments, in order of how quickly they can be sold:

1. **SEBI-registered RAs, boutique PMS and small AMC analysts** — the beachhead. They read filings manually every day, they already buy research tools, and per `FUNDING_PLAN.md` §8 they double as the best angel and diligence pool. AlphaSense is the functional comparable at ₹12–16 **lakh** per seat per year; ₹36K/seat/yr is 2–3% of that.
2. **Wealth-management and distributor networks** (RIAs, MFDs with HNI books) — need client-ready, cited output. Sold per seat with white-label report export.
3. **API / data licensing** — brokers, fintechs, and content businesses wanting the announcements corpus or the scoring endpoints. Highest revenue per unit of engineering, and it is how a broker integration (`FUNDING_PLAN.md` §7.4, Narrative B / Rainmatter) would actually start commercially. **Gate this behind legal review** — the data-provenance memo and ₹50–75K counsel opinion in `FUNDING_PLAN.md` §3.4 are prerequisites to *redistribution*, which is a different licence question from serving our own users.

**The regulatory constraint on B2B is real and shapes the product, not just the copy.** Until corporate RA registration (~₹5.5L + GST, plus the RAASB lien-marked deposit and revised NISM-XV), Anvest must stay strictly informational: no buy/sell/hold, no target prices, the Anvest Score framed as a data summary. SEBI has held that "educational" disclaimers do not exempt actionable signals. **This is a feature for B2B**: an RA does not want our recommendation — they want our evidence, with the citation, so they can put their own name on the call. Sell the seat as *research productivity*, never as *research opinion*. The Dec-2024 RA amendments' AI-disclosure duty is then something we help them discharge, since every answer already carries its sources.

---

## 5. Proposed tiers and the margin proof

### 5.1 The tiers

| | **Free** | **Anvest Plus** | **Anvest Pro** | **Anvest Desk** (B2B) |
|---|---|---|---|---|
| **Price (GST-incl.)** | ₹0 | **₹199/mo · ₹1,799/yr** | **₹599/mo · ₹4,999/yr** | **₹2,999/seat/mo · ₹29,990/seat/yr** |
| Effective ₹/mo | — | ₹150 annual | ₹417 annual | ₹2,499 annual |
| **Positioned against** | — | Tickertape ₹200, Tijori ₹292, Trendlyne GuruQ ₹183 | Screener ₹417, StratQ ₹412–492, StockEdge Pro ₹550 | AlphaSense ₹1.2–1.6L/mo |
| **Copilot questions** | **3/month** (+3 lifetime anonymous) | **150/month** | **600/month** | **2,000/seat/month** |
| Stock pages | unlimited, delayed | unlimited | unlimited | unlimited |
| Screener runs | 5/day | unlimited | unlimited | unlimited |
| NL→DSL screener | 3/month | unlimited | unlimited | unlimited |
| Watchlists | 2 | 10 | unlimited | unlimited |
| Alerts | 5 | 50 | 500 | 2,000 |
| **Proactive "since you last viewed" digest** | — | weekly | **daily** | daily + team feed |
| Portfolio X-ray | — | basic | full + attribution | multi-portfolio |
| Backtests | — | **20/month** | **300/month** | 1,000/month |
| Paper trading | — | 1 workspace | unlimited | unlimited |
| Data export (CSV) | — | ✅ | ✅ | ✅ + bulk |
| ITR module | ✅ free | ✅ | ✅ | — |
| Report export (PDF, cited) | — | — | ✅ | ✅ white-label |
| API access | — | — | — | ✅ metered |
| Seats | 1 | 1 | 1 | 5+ |
| Support | community | email | priority email | named contact + SLA |

**Why these numbers:**

- **Plus at ₹1,799/yr undercuts every annual plan in the band except StockEdge Premium (₹1,649)** while including something none of them have. The monthly at ₹199 is deliberately unattractive relative to annual (₹1,799 = 9 months) to drive the annual mix that §5.5 shows is worth more than the price difference.
- **Pro at ₹4,999/yr matches Screener exactly.** Deliberate: it makes the comparison a single-variable one, and the single variable is 1,500 included AI answers versus ~17–50. Do not undercut here — undercutting invites a price comparison; matching forces a value comparison we win.
- **The 150 / 600 / 2,000 question caps are the margin.** They are set at roughly 7× typical modelled usage so that essentially no honest user meets them, while a scripted abuser is bounded at a known cost. §5.4 shows what happens without them.
- **Backtest counts follow the market's convention** (Trendlyne sells 200/yr on GuruQ, 1,200/yr on StratQ). Ours are per *month*, which reads as far more generous and costs us CPU rather than tokens.

`GTM_PLAN.md` proposed a single Pro at ₹249/mo — that was one tier, priced below the entire competitive band, and it left the ₹550–1,100 gap (§4.1) unoccupied. This structure supersedes it.

### 5.2 Per-subscriber unit economics

Assumptions: prices GST-inclusive → net = price/1.18 · payment fee 2.36% of gross · 70% annual / 30% monthly mix · LLM at ₹0.360/question · typical usage Plus 20 q/mo, Pro 80 q/mo, Desk 400 q/mo.

| Tier | Blended gross ₹/mo | Net revenue ₹ | Payment fee ₹ | LLM ₹ (typical) | LLM ₹ (at cap) | **CM% typical** | **CM% at cap** |
|---|---|---|---|---|---|---|---|
| Plus | 165 | 140 | 3.9 | 7.2 | 54 | **92.1%** | **58.5%** |
| Pro | 471 | 399 | 11.1 | 28.8 | 216 | **90.0%** | **43.1%** |
| Desk (per seat) | 2,649 | 2,245 | 62.5 | 144.0 | 720 | **90.8%** | **65.1%** |

**Every tier clears 50% contribution margin even if the subscriber consumes their entire monthly allowance — except Pro at 43.1%.** That is acceptable (a Pro user consuming 600 questions every month is a rounding error, and they are the ones writing the reviews), but it is the number to watch. If Pro cap-hitters exceed ~15% of the Pro base, either lower the cap to 400 or move Pro synthesis to 3.1-flash-lite for non-thread queries.

### 5.3 Blended P&L at scale

Mix assumption: 75% Plus / 22% Pro / 3% Desk seats. Infra Config B ($480/mo) + fixed AI/OCR ($37/mo). Free-tier drag at 3% conversion, 3 free questions/month.

| Subscribers | Net MRR ₹ | COGS ₹ | *of which free-tier LLM* | Gross margin ₹ | **GM%** |
|---|---|---|---|---|---|
| 100 | 25,987 | 55,237 | 3,492 | −29,250 | −112.6% |
| 250 | 64,967 | 63,968 | 8,730 | 998 | 1.5% |
| 500 | 129,933 | 78,522 | 17,460 | 51,412 | 39.6% |
| **~700** | — | — | — | — | **50%** ← threshold |
| 1,000 | 259,867 | 107,628 | 34,920 | 152,239 | 58.6% |
| 2,500 | 649,666 | 194,947 | 87,300 | 454,719 | **70.0%** |
| 5,000 | 1,299,333 | 340,479 | 174,600 | 958,854 | 73.8% |
| 10,000 | 2,598,666 | 631,543 | 349,200 | 1,967,123 | 75.7% |

**≥50% gross margin at ~689 subscribers. ≥70% at ~2,503.** On Config A infra rather than B, the 50% threshold falls to roughly 500.

Including team cost:

| Team | Cash break-even | **≥50% operating margin** |
|---|---|---|
| Solo founder (₹2.0L/mo) | **1,238 subs** | **3,478 subs** |
| Founder + 2 engineers (₹6.5L/mo) | **3,469 subs** | **9,752 subs** |
| Founder + 3 hires (₹9.5L/mo) | **4,957 subs** | **13,935 subs** |

For calibration: `FUNDING_PLAN.md` §7.3 targets 15,000 MAU and $21K (₹20L) MRR by month 15. **At 3% conversion, 15,000 MAU is only 450 subscribers** — below cash break-even. Hitting ₹20L MRR needs roughly **7,700 subscribers at this blended ARPU**, which at 3% conversion implies ~257,000 MAU, or a much higher conversion rate, or a much heavier B2B mix. **The B2B mix is the realistic answer**: 150 Desk seats alone is ₹3.4L MRR at 90.8% margin, and reaching it needs conversations rather than traffic. This is worth reconciling in the funding materials.

### 5.4 The finding that matters most: free-tier AI allowance

Blended gross margin at 2,500 subscribers, 3% conversion, varying only the free tier's monthly copilot allowance and the model:

| Free q/month | 3.1-flash-lite (₹0.20) | **3-flash (₹0.40)** | 3.5-flash (₹1.20) |
|---|---|---|---|
| 0 | 86.5% | **83.4%** | 71.1% |
| 1 | 82.0% | **79.0%** | 66.6% |
| **3** | 73.1% | **70.0%** | 57.6% |
| 5 | 64.1% | **61.0%** | 48.7% |
| 10 | 41.7% | **38.6%** | 26.3% |

At 3% conversion each paying subscriber carries 32.3 free users. Their questions are billed to us at the same rate as a Pro subscriber's. **Ten free questions a month costs more per paying subscriber than that subscriber's own usage, their payment fee and their share of infrastructure combined.**

Related sensitivity, same model, on usage and model choice together:

| Scenario | GM @ 2,500 | GM @ 10,000 | 50% GM reached at |
|---|---|---|---|
| 3.1-flash-lite, typical usage | 73.1% | 78.8% | 620 subs |
| **3-flash, typical (plan)** | **70.0%** | **75.7%** | **689 subs** |
| 3-flash, 2× usage | 63.8% | 69.5% | 888 subs |
| 3.5-flash, typical | 57.6% | 63.3% | 1,249 subs |
| **3.5-flash, 2× usage** | **39.1%** | **44.8%** | **never** |

**A migration to 3.5-flash combined with usage running 2× the model would put 50% gross margin permanently out of reach at any subscriber count.** This is the concrete reason the model-migration decision in §8 is a business decision, not an infrastructure chore.

**Therefore, three hard rules:**
1. **Free signed-in tier: 3 copilot questions/month.** Not per day. The existing anonymous 3-lifetime limit stays and gets switched on.
2. **Never route free-tier traffic to the expensive model.** Free and Plus answer on `gemini-3.1-flash-lite`; Pro and Desk get `gemini-3-flash`. This is a genuine product differentiator ("Pro uses our most capable model"), it is honest, and it is what makes the free tier survivable.
3. **The SEO strategy does not require free AI.** `GTM_PLAN.md` names programmatic SEO over 6,137 stock pages as the highest-ROI channel. Those pages are served from **pre-generated** `stock_profiles` and cached summaries — zero marginal LLM cost per visitor. Free-tier live copilot access is a *conversion* mechanism, not an acquisition one, and 3/month is enough to demonstrate the "aha."

### 5.5 Annual mix

| Annual share | Effective ₹/mo (Plus) | Net ₹ | Fee ₹ | CM ₹ | CM% |
|---|---|---|---|---|---|
| 0% | 199 | 169 | 4.70 | 157 | 92.9% |
| 50% | 174 | 148 | 4.12 | 137 | 92.3% |
| 70% | 165 | 140 | 3.89 | 128 | 92.1% |
| 90% | 155 | 131 | 3.65 | 120 | 91.7% |

Margin *percentage* barely moves — but that is not why annual matters. Annual gives **12 months of cash up front**, one payment-failure event instead of twelve, and it removes eleven monthly opportunities to churn. At a pre-PMF company with no CAC data, **cash-up-front and churn-suppression are worth more than the ~10% of revenue the discount costs.** Push annual hard.

---

## 6. Billing models and subscription UX

### 6.1 The regulatory frame (this shapes the UX more than any design choice)

- **RBI's e-mandate framework** requires a one-time Additional Factor Authentication to register a mandate; recurring debits up to **₹15,000** then run without OTP. Select categories (insurance, MF SIPs, credit card bills) go to ₹1,00,000 — we are not one of them, and do not need to be.
- **Every Anvest price is far below ₹15,000**, including the ₹29,990 annual Desk seat… which is *not*. **A ₹29,990 annual B2B charge cannot ride a frictionless e-mandate.** Bill Desk annually by invoice/NEFT or as a ₹2,999 monthly mandate; do not build an annual autopay flow for it and discover this in production.
- Users can pause or cancel mandates themselves at any time via AFA. Assume mandate cancellations will arrive out-of-band from our UI, and reconcile from webhooks rather than trusting our own database.
- **GST at 18% must be charged and remitted**, and registration is mandatory above ₹20L turnover. Display prices inclusive (Indian B2C convention), show the GST split on the invoice, issue a GST invoice per charge. For Desk customers the GST invoice with our GSTIN is not a nicety — it is how they claim input tax credit, and its absence will lose deals.

### 6.2 Billing model options

| Model | How it works | Fit for Anvest | Verdict |
|---|---|---|---|
| **A. Flat recurring (monthly + annual)** | Fixed price, fixed entitlements | Matches every competitor; simplest to explain; predictable revenue | **Ship this. Core of Plus, Pro, Desk.** |
| **B. Flat + hard cap** | A, with a monthly question ceiling that blocks at the limit | Bounds COGS exactly; the cap is invisible at 7× typical usage | **Ship this — it is what makes §5.2 true.** |
| **C. Metered / pay-as-you-go credits** | Buy ₹ of credits, spend per answer | This is Screener's model. Punishes exploration, makes users count tokens, caps our own upside | **Reject as the primary model.** Keep as a top-up (§6.3) |
| **D. Hybrid: flat + overage top-up** | B, plus optional ₹99 = 150 extra questions | Cap becomes an upsell rather than a wall; preserves the "included" headline | **Ship in phase 2**, after real usage data |
| **E. Usage-based B2B (API)** | Per-call / per-1,000-calls tiers | The right shape for the API segment; nothing else fits | **Ship for Desk API only** |
| **F. Seat-based B2B** | Per seat/month, 5-seat minimum | Standard for RA/PMS; matches AlphaSense's shape at 2–3% of price | **Ship for Desk** |
| **G. Freemium with time-limited trial** | 14-day full Pro, no card | Highest funnel conversion in Indian consumer SaaS; no mandate friction before value | **Ship. Recommended over card-required trial** |
| **H. Lifetime / one-time** | Single payment, perpetual access | Fatal with per-question COGS — unbounded liability against bounded revenue | **Reject outright** |
| **I. Broker/partner bundle** | Anvest bundled into a broker's plan, rev-share or per-MAU | The Narrative-B / Rainmatter path; highest-leverage distribution available | **Structure now, sell after PMF** |

**Recommended: B + F + G at launch; D and E in phase 2; I opportunistically.**

### 6.3 Subscription UX — the decisions that matter

1. **UPI Autopay first, cards second.** UPI is the default Indian payment rail, the mandate is set with a familiar app approval, and there is no card-expiry failure mode. It is also cheaper for us on subscriptions (Razorpay adds 0.9% on *card* subscriptions, not UPI Autopay). Order the checkout: **UPI Autopay → Cards → Netbanking/eNACH** (eNACH for Desk only — the setup takes days and is wrong for retail).
2. **Trial without a card.** 14 days of Pro, no payment instrument. Requiring a mandate up front is the largest single drop-off point in Indian consumer subscription funnels, and we have a much better conversion event available: the user's first grounded, cited answer about a stock they own.
3. **Show the meter, never surprise with it.** A persistent, quiet "127 of 150 questions this month" in the copilot header. At 80% show a soft nudge; at 100% show what upgrading buys — never a bare error. The existing `usage_limits` 403 payload (`error_code`, `action`, `limit`, `message`) already carries what the UI needs; it needs `remaining` and `resets_at` added.
4. **Grandfather aggressively and say so.** Early subscribers keep their price for life. It costs little at these volumes and it is the standard response to the "will you raise prices once I'm locked in" objection that any Screener user will have.
5. **Annual is the default selection**, with "₹1,799/yr — 9 months' price" as the framing rather than a percentage. Indian consumers respond to absolute-months framing.
6. **Dunning must be gentle and long.** A failed UPI mandate is usually a bank issue, not intent to churn. Retry on days 1, 3, 7; keep access live throughout; downgrade to Free on day 10 rather than locking the account. Never delete user data on downgrade — watchlists, alerts and portfolios all persist read-only, which makes win-back a one-click event.
7. **Self-serve cancel, no retention maze.** Regulatorily safer, and a cancellation flow that offers "pause for 3 months" instead of a phone call converts better anyway.
8. **Invoices with GSTIN, automatically emailed.** Non-negotiable for Desk; appreciated by retail users who expense it.
9. **Proration on upgrade, credit on downgrade.** Plus→Pro mid-cycle should be instant and prorated. Razorpay Subscriptions supports this; do not hand-roll it.
10. **One entitlement check, server-side, everywhere.** Never gate in the frontend. The `usage_limits` service is the single decision point and should stay that way — the same architectural discipline `app/services/ai_enrichment/policy.py` already applies to spend.

### 6.4 Failure modes to design against now

- **Webhook loss.** Razorpay webhooks are at-least-once and occasionally late. Entitlement must be derivable from a reconciliation poll against the subscriptions API, not solely from webhook arrival. Store the provider's subscription object, not just our interpretation of it.
- **Double-charging on retry.** Idempotency keys on every mutation.
- **Entitlement drift.** Nightly reconciliation job: for every active local subscription, confirm the provider agrees. Log divergences loudly. This is the billing analogue of the checkpoint-clobber and cache-corruption classes of bug this codebase has repeatedly found — two writers, no reconciliation.
- **The cap as a support burden.** Every 403 from `usage_limits` should be logged with user, action and plan, so "is the cap too low" is answerable from data in week two rather than argued from intuition.

---

## 7. Variations worth considering

Presented because the brief asked for implementation variations; each has a real trade-off rather than being a strictly worse option.

**Pricing structure**
- **V1 — Two tiers instead of three (drop Plus).** Free → Pro ₹4,999 only. Simpler, higher ARPU, but concedes the entire ₹137–300 band where six competitors live, and the volume goal in the brief argues against it.
- **V2 — Plus at ₹99/mo (₹999/yr).** Genuinely undercuts everyone. CM stays ~85% at typical usage. Real risk: it prices Anvest below StockEdge and signals "budget option" against a Screener-grade data claim. **Consider only as a launch-window promotion with a stated end date**, never as list price.
- **V3 — Usage-based Pro** (₹199 base + ₹1/question). Perfectly aligned COGS, and it is what Screener does. Rejected as primary (§6.2 C) but a defensible A/B if included-question economics turn out worse than modelled.
- **V4 — Annual-only, no monthly.** Screener and Tickertape both do this. Better cash and churn; loses the users who genuinely will not commit ₹1,799 to an unproven product. **Not recommended pre-PMF** — monthly is a cheap way to buy willingness-to-pay data.

**Infrastructure**
- **V5 — Stay on the Mac through beta.** Saves ₹28K/month. `GTM_PLAN.md` §7.5 already calls single-Mac production a launch risk, and Qdrant died under normal batch load on 2026-07-29. Below ~200 subscribers the cost saving is real; above that, one outage during a Reddit launch costs more than a year of the VM.
- **V6 — Hybrid: serving on GCP, batch on the Mac.** This is Configs A and B and the recommendation. Keeps ₹0 batch compute and the existing launchd supervision.
- **V7 — Cloud SQL instead of self-managed Postgres.** +$20–40/month for managed backups and failover. Buys sleep; the restore drills already exist.

**LLM**
- **V8 — Model tiering by plan** (free/Plus on 3.1-flash-lite, Pro/Desk on 3-flash). Recommended in §5.4. Turns a cost control into a feature.
- **V9 — Vertex context caching on the evidence pack.** ~31% cut on the dominant variable cost, no quality change. Should be done regardless of tier design.
- **V10 — Self-hosted open model on a spot L4 for batch.** `GTM_PLAN.md` §5 already proposes this for bulk extraction, and the L4 recipe is written (`anvest-gpu-embedding-vm-recipe`). Do not extend it to interactive traffic: an always-on GPU violates the standing rule and would dominate infra cost at these volumes.

**B2B**
- **V11 — Desk as a 5-seat minimum team plan at ₹12,999/mo.** Higher deal size, fewer deals, better fit for a PMS.
- **V12 — Per-report pricing for RAs** (₹499 per cited, exportable company report). Zero commitment, matches how boutique RAs actually budget, and it is a very natural upsell into a seat.
- **V13 — White-label / API only**, no Anvest-branded seat. The broker-integration path; highest engineering cost, highest ceiling, needs the provenance legal opinion first.

---

## 8. What must happen before any of this is real

Ordered by dependency, not by size. **No pricing decision is final until items 1–3 return numbers.**

1. **Re-measure cost per question honestly.** The $0.0030 figure is 30 questions, cold, on a loaded box, on a model that retires in six weeks. Expand `golden_dataset.json` toward 150 questions (already an open task), instrument real token counts into `llm_token_telemetry` for interactive traffic — the table exists and has exactly one non-synthetic row — and re-run per candidate model. **Everything in §5 moves if this number moves.**
2. **Decide and execute the Gemini 2.5 → 3.x migration.** Retirement is ~16 Oct 2026. Benchmark 3.1-flash-lite and 3-flash on the golden set for quality and cost together. `test_no_legacy_gemini_models.py` CI-gates hardcoded ids and the working ids live only in `local-backend.env` — so this is a config-and-verify job, not a refactor, but it must be scheduled now.
3. **Turn on metering and watch it for four weeks before pricing.** Enable `ANVEST_ENFORCE_ANONYMOUS_RESEARCH_LIMITS`, add copilot-question metering to `usage_limits`, and log every 403. The 150/600/2,000 caps are 7× a *modelled* typical usage; they should be 7× a *measured* one.
4. **Unblock and budget Vertex billing.** Per `ai-enrichment-cost-architecture-2026-08.md`, `anvest-505415` is ACTIVE with `billingEnabled: false`, and ADC expiry has silently killed Vertex stages since 13 August (`anvest-adc-expiry-kills-all-vertex-stages`). A paid product cannot run on credentials that expire silently. Link the billing account, set the budget alert, and fix the ADC refresh.
5. **Prune `feature_store_daily` v1 + part2b** (~85 GB, 47%) before migrating anything to cloud storage.
6. **Serving migration to GCP Config A.** Hard gate before any public link is posted, per `GTM_PLAN.md` §7.5.
7. **Then** the billing engineering plan: plan/entitlement schema, Razorpay Subscriptions integration, webhook + reconciliation, pricing page, trial flow, upgrade/downgrade proration, GST invoicing, dunning.
8. **In parallel, and independent of all of the above: sell 5 Desk seats.** §4.4 and `FUNDING_PLAN.md` §4.4 both conclude B2B is faster, higher-ARPU and more fundable than retail. It needs ~150 conversations and no payments infrastructure at all — the first five can be invoiced manually. **Doing this before building the billing system tells us whether we are building the right one.**

---

## 9. Sources

**Competitor pricing** — [Screener Premium](https://www.screener.in/premium/) · [Screener AI](https://www.screener.in/ai/) · [Trendlyne plans](https://trendlyne.com/subscription/plans/) · [StockEdge pricing](https://stockedge.com/pricing) · [Tickertape Pro pricing](https://www.tickertape.in/blog/new-tickertape-pro-pricing/) · [Tijori review/pricing](https://www.findmymoat.com/tools/tijori-finance-ideas-dashboard) · [Finology subscribe](https://www.finology.in/subscribe) · [India screener guide 2026](https://www.winvesta.in/blog/investors/fundamental-analysis-tools-and-screeners-2026-guide) · [AlphaSense pricing](https://www.vendr.com/marketplace/alphasense)

**Cloud & model pricing** — [GCP asia-south1 rates](https://gcloud-compute.com/asia-south1.html) · [Cloud SQL pricing](https://cloud.google.com/sql/pricing) · [Gemini API pricing Aug 2026](https://benchlm.ai/google/api-pricing) · [Gemini pricing 2026 overview](https://www.cloudzero.com/blog/gemini-pricing/) · [Vertex AI deprecations](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/deprecations) · [Gemini 2.5 retirement discussion](https://discuss.ai.google.dev/t/gemini-2-5-flash-lite-retirement-date-different-for-gemini-api-vs-vertex-ai/177897) · [Cloud Vision OCR pricing](https://www.buildmvpfast.com/api-costs/ocr)

**Payments & tax** — [Razorpay pricing](https://razorpay.com/pricing/) · [Razorpay: cheapest gateway for recurring billing](https://razorpay.com/blog/cheapest-payment-gateway-for-recurring-billing-e-nach-upi-autopay-and-subscription/) · [Razorpay vs Cashfree (D2C Lab)](https://d2c-acquisitionlab.com/guides/razorpay-vs-cashfree-india) · [Cashfree subscriptions](https://www.cashfree.com/docs/payments/subscription/introduction) · [RBI e-mandate framework 2026](https://www.outlookbusiness.com/ampstories/news/rbi-e-mandate-framework-2026-new-rules-for-auto-pay-upi-cards-wallets) · [GST on SaaS in India](https://www.kanakkupillai.com/learn/gst-for-saas-companies-in-india/)

**Salary benchmarks** — [Software engineer salary India 2026](https://resources.instahyre.com/blog/software-engineer-salary-in-india/) · [Backend developer CTC 2026](https://resumevera.com/salary-guide/backend-developer)

**FX** — ₹95.69/USD, 30 Aug 2026 ([exchangerates.org.uk](https://www.exchangerates.org.uk/USD-INR-spot-exchange-rates-history-2026.html))

**Internal** — `ops/business/GTM_PLAN.md` · `ops/business/FUNDING_PLAN.md` · `docs/copilot_eval_2026-07-29.md` · `docs/ai-enrichment-cost-architecture-2026-08.md` · `ops/local-hosting/WORKLOAD_PRIORITY.md` · `data-platform/app/services/usage_limits.py` · `broker-portfolio/broker_portfolio/app_factory.py`

*Model workings, re-runnable: `ops/business/model.py` (LLM unit cost + infra configs), `ops/business/margin.py` (tiers, break-even, sensitivities).*
