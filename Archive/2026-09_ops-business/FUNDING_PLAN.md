# Anvest — Funding Plan

**Date:** 2026-07-26 · **Revised 2026-09-03** (post-YC decision — §8 and §9 rewritten, §7.1 repriced)
**Entity:** Anvest Fintech Private Limited · anvest.in
**Founder:** Harsh Bhardwaj (solo, hiring — plus a paid advisory bench, see §3.5)
**Companion docs:** `GTM_PLAN.md` (market + go-to-market), `SUBSCRIPTION_MODEL_2026-08-31.md` (pricing, unit economics, competitive re-read — **supersedes the pricing in this doc and in GTM_PLAN**), `plan.md` (engineering roadmap), `financial_parsing.md` (data-quality state of play).
**Target:** **YC Fall 2026 — rejected** (§9). The parallel campaign is now the only track. **Repriced: $3.5M post-money cap, $400K base / up to $700K (11.4–20% dilution)**, identical terms for every investor. The reasoning for the change, and what would earn the old $5.0M number back, is in §7.1. Ranked target list in §8. Rate: ₹95.69/USD (30 Aug 2026).

---

## 0. The One Thing To Understand Before Reading Further

**Your fundraising problem is not your materials. It is that you have zero users.**

Everything in this document is downstream of that single fact. A solo founder with a genuinely impressive, bootstrapped, technically deep platform and **no usage data** is, to a pre-seed investor in 2026, indistinguishable from a very talented person with a hobby. The median Indian seed ticket is holding at ~$1M and the market is described by every investor writing publicly this year as *more metric-driven and more conservative* than founders expect. You will be asked "how many people used this last week?" in the first five minutes of every meeting, and there is no clever answer.

The good news: this is the cheapest problem on your list to fix. You have a working product on a live domain. **200–500 real users and 20–40 paying professional seats is 6–8 weeks of work, not a funding round.** With that, the same deck that gets ignored today becomes a competitive pre-seed.

So this plan is sequenced deliberately:

| | Window | What you do |
|---|---|---|
| **Track A** | Tonight → tomorrow 8pm PT | YC Fall 2026 application. Free optionality, hard deadline, forces narrative clarity. Do it regardless of readiness. |
| **Track B** | Weeks 1–3 | Make the product safe to show a stranger. Fix the trust bugs, get off the Mac, badge the bad data, instrument everything. |
| **Track C** | Weeks 2–8 | **Manufacture traction.** ITR season (live now, ends Aug 31 for F&O filers) + B2B research seats + alpha cohort. This is the actual fundraise. |
| **Track D** | Weeks 6–14 | Investor process: warm intros, angels first, micro-VCs second, term sheet target end-October. |

Do not invert B/C and D. Pitching at zero traction burns the intro — investors remember a "no," and a second bite at the same fund in four months is much harder than a first bite in four months.

---

## 1. Nature of the Business (the matter-of-fact version)

Anvest is a **vertically integrated equity research platform for Indian retail investors**. Three layers, built bottom-up, all bootstrapped:

**Layer 1 — Data warehouse (the part that took a year and nobody sees).**
~6,137 active NSE/BSE symbols. XBRL-parsed annual + quarterly financials with consolidated/standalone handling and derived QoQ/YoY metrics. Shareholding patterns. 584K corporate announcements over 2 years. **Price data is end-of-day: the exchanges' own published bhavcopy files, ingested by a scheduled 7pm job.** Not a real-time feed — that arrives later, via broker websockets (§6). Plus a repair layer that has already fought and won non-trivial data wars — market-cap cache corruption that was wrong for ~78% of NSE equities, 15,899 recovered cash-flow rows, NSE's malformed FY23+ XBRL context dates, annual coverage mined out of Q4 filings because no separate annual XBRL exists.

**Layer 2 — Filings corpus (the moat).**
Announcement PDFs robust-parsed and OCR'd, chunked with bge-m3, 1.35M+ vectors in Qdrant, incremental daily parsing. This includes scanned SME filings that no competitor indexes because it requires an OCR queue and per-page spend nobody bothered with.

**Layer 3 — Grounded AI surfaces.**
A research copilot with a planner → provider → compression → synthesis pipeline, generate→verify→self-repair loops, Redis evidence caching and SSE streaming. NL→DSL screener that self-corrects. Portfolio X-ray, watchlist AI, sector-calibrated Anvest Score, 5,405 generated company profiles, global chat. One architectural invariant runs through all of it: **the LLM never does arithmetic, and if coverage is missing it says so rather than guessing.**

**Adjacent, and more strategically valuable than it looks — the ITR engine.**
A deterministic Python tax compiler for AY 2026-27: ingests ITD prefill JSON, AIS PDFs, Zerodha/Groww P&L exports and ELSS statements; runs FIFO lot reconstruction for capital gains; computes under both regimes; auto-selects ITR-1/2/3; emits schema-valid official ITD JSON with a 4-layer differential validation suite. Zero LLM calls in the calculation path.

**Production reality (state this plainly to investors, it reads as capital efficiency, not amateurism):** Vercel frontend, two FastAPI services + Qdrant + Redis in Docker behind a Cloudflare tunnel **on the founder's Mac**, Postgres native on the same host, nightly batch via launchd. Total infrastructure spend to date: ~$0 plus free GCP credits.

---

## 2. The USP

**One sentence:** *Anvest can answer "why did this company's margins fall last quarter?" for any of 6,137 Indian listed companies by quoting the actual filing it came from — because it is the only product that has parsed, OCR'd and vectorized two years of Indian announcement PDFs on top of a full-universe XBRL warehouse, in an architecture where the model is structurally forbidden from doing the arithmetic.*

**Why it is hard to copy — be specific, "we have better AI" is not an answer:**

1. **The corpus is a grind, not a prompt.** 584K announcements, robust parsing, an OCR queue for scanned SME filings, 1.35M chunks. Twelve-plus months of unglamorous data engineering with no demo value until the day it works.
2. **The repair layer is the actual IP.** Anyone can call an XBRL parser. Almost nobody has discovered that NSE's FY23+ filings carry malformed context dates, that annual consolidated data has to be mined out of Q4 filings, or that a naive parse produces PAT > revenue on RELIANCE FY22. Every one of those is a bug you only find by serving real queries and being embarrassed. That knowledge is not in a repo anyone can clone.
3. **Grounded-or-silent is an architecture, not a policy.** Coverage assessment gates, evidence-builder provenance, verify-and-repair loops. Retrofitting this into a chat wrapper is a rewrite.
4. **It compounds in the wrong direction for competitors.** Every filing parsed makes the next answer better and the eval set richer. A competitor starting today starts at zero corpus against your two years.

**What is *not* your moat, and do not claim it is:** the chat interface, the gradient design system, the prompt engineering, or "AI-first." All copyable in a sprint. Every minute of the pitch spent there is a minute an investor spends thinking about Perplexity.

---

## 3. Honest Drawbacks — The Diligence Kill-List

Ranked by probability of killing a round. Each has a fix, a cost, and a time. **Read this section as your pre-raise checklist, not as criticism.**

### 3.1 Zero users, zero revenue, zero telemetry — *fatal, fixable in 6 weeks*
No DAU/MAU, no retention curve, no willingness-to-pay evidence, no engagement telemetry on any AI surface. You cannot even answer "which of your eight AI surfaces do people actually use?" because you do not measure it (gap D2).
**Fix:** PostHog wired in week 1. Then Track C. **Cost:** ₹0. **Blocker for:** every conversation.

### 3.2 Known-wrong numbers served unbadged — *fatal to your specific pitch, fixable in days*
You are going to pitch "numerically trustworthy" while `query-api` silently substitutes standalone financials for consolidated across **4,517 symbol-FY periods** (B8), and ~**3,170 quarterly rows across 720 symbols** have `pat` disagreeing with `pbt − tax_expense` beyond plausible one-off explanations (B9). If a diligence process spot-checks BERGEPAINT — which you have already confirmed is implausible — the entire trust thesis inverts in one screenshot.
**Fix:** do not attempt the parser-level fix before pitching. **Badge it.** Render "standalone — consolidated not filed" where substitution happens; flag suspect rows and suppress them from AI answers and score inputs. A visible data-corrections changelog turns your worst liability into your most credible artifact — *"here is every number we got wrong and when we fixed it"* is a thing no competitor in this market will publish. **Cost:** ~1 week. **Blocker for:** any live demo.

### 3.3 Production runs on your laptop — *serious, fixable for ₹4–9K/month*
Postgres, Redis, Qdrant, both APIs, the tunnel and all enrichment on one 24GB Mac with documented OOM history, a Docker runtime that does not auto-start after reboot, and (until recently) a Redis container with no restart policy that was silently down for 7 hours. An investor who asks "what happens if your house loses power during market hours" gets an answer you do not want to give.
**Fix:** move serving to an e2-standard-4 (~$100/mo) or Hetzner (~€40/mo); Mac becomes the batch node. **Cost:** ~1 week + ₹4–9K/mo. **Blocker for:** any public launch, and for the "is this a company or a project" judgment.

### 3.4 Data provenance — *manageable, and better than it first looks; needs a written memo, not a panic*
Any fintech-literate investor's counsel will ask where your prices come from. Your actual position is materially cleaner than most people building in this space, and the memo practically writes itself:

- **You use the exchanges' published end-of-day bhavcopy, ingested nightly at 7pm.** Not a real-time feed, not a scraped live-quote endpoint. That distinction is the whole ballgame: the enforcement risk and licensing regime around exchange market data is overwhelmingly about *real-time* price, quote and depth redistribution. EOD settlement files the exchange itself publishes for public download are a different animal. **Say "end-of-day bhavcopy, refreshed at 7pm" in the first sentence** — it pre-empts the question you'd otherwise look evasive about.
- **Corporate filings and XBRL are statutory public disclosures.** This is the bulk of your moat, and it is your strongest ground — companies are legally *required* to publish this, precisely so it can be read.
- **Never describe anything as a "live feed" or "real-time" that isn't licensed.** Audit your own site copy and this deck for that word. Right now the product is EOD and should say so — an explicit "as of yesterday's close" label is a trust feature, not an apology.
- **The forward path is priced.** Real-time arrives via broker websockets for accounts users connect themselves (Kite Connect class, ~₹2K/mo — the user's own licensed entitlement, not your redistribution), or a licensed vendor feed (₹15–25K/yr/segment) once revenue justifies it. Same mechanism unlocks live portfolio tracking. It's in the use-of-funds.

**What still needs doing:** a one-page written memo documenting each source, its licence basis, and the forward path — plus a ₹50–75K counsel review before the first institutional meeting. NSE's data policy does govern redistribution and you want a lawyer's signature, not your own inference, on the conclusion. **Cost:** half a day of writing + the review. **Blocker for:** institutional diligence only — angels won't ask.

### 3.5 Solo founder — *real headwind, but a co-founder is the wrong fix. Buy the gap with advisor equity instead.*

**The numbers, plainly.** Solo founders launch ~35% of startups but close only ~15–17% of priced VC rounds; two-person teams take ~36%. The funding discount is roughly 2x and it is not imagined. Working the other way: solo-founded ventures are ~2.5x more likely to *survive*, largely by avoiding co-founder conflict — which is the most common way early startups die. YC's own published position is that solo founders are less likely to be funded. So: a genuine headwind, not a disqualification.

**Do not recruit a finance co-founder.** It is the one profile that helps least. You already know NSE's post-FY23 XBRL context dates are malformed, that annual consolidated has to be mined out of Q4 filings, that a naive parse puts RELIANCE FY22 PAT above revenue. You built a FIFO capital-gains engine and an ITR-3 compiler that validates against ITD schema. A CA, ex-banker or equity analyst duplicates your strongest axis and leaves the actual hole — **zero users** — exactly where it is. You would pay ~35% of the company for redundancy.

**The asymmetry that settles the timing.** A co-founder now costs 30–50% at zero valuation. The same person at month 9, with ₹1L MRR and a retention curve, costs 10–20% — or joins as employee #1 on 3% ESOP with a title. The search itself takes 3–9 months, during which the ITR window closes and the traction sprint stalls. And the option is one-directional: you can add a co-founder later; you cannot remove one. Unwinding partly-vested equity from someone who left is a diligence problem that outlives the person.

**Do this instead — the highest-leverage cap-table move available to you.** Recruit **2–3 SEBI-registered RAs or boutique PMS analysts as paid advisors** on FAST-style terms: 0.5–1% each, 2-year vest, 3-month cliff (the Founder Institute's FAST template, v3 as of June 2026, raised pre-seed standard grants to 0.50%). Roughly **2% of equity total** buys:

| What you get | Why it matters here |
|---|---|
| Regulatory credibility | Accelerates the RA registration path and gives the AI-disclosure obligations a named owner |
| The B2B channel | These are your first paying professional seats — advisor and customer are the same person |
| Domain validation investors can phone | Third-party confirmation your data is right, from people qualified to judge it |
| A team slide with real names | Answers "who else is around this?" without giving away a third of the company |

That is the same coverage a finance co-founder would give, at roughly 1/17th the equity cost.

**The one legitimate co-founder case, and it isn't finance.** You have budgeted ~₹43L/year for growth. A genuinely good Indian consumer-fintech growth lead costs ₹35–60L and will be weighing offers from funded companies. An equity-motivated partner beats a salaried employee on a 0-to-1 distribution problem. If you go this route the profile is: someone who has taken an Indian consumer fintech from 0 to 100K+ users, or a fundamentals-focused creator with an existing audience willing to come in as a partner. Never "finance experience" generically.

**Decision rule — commit to this now so you don't relitigate it monthly.** Stay solo through the pre-seed. **If by month 6 the growth hire has not pushed DAU/MAU past ~15%, that is your evidence you need an equity-motivated partner rather than an employee** — and by then you will be paying ~15%, not ~40%. Use YC Co-Founder Matching (free, no batch required) to keep a warm pipeline in the meantime.

**How to answer the objections in the room:**
- *"Bus factor."* → Documentation quality, `CLAUDE.md` and architecture docs, supervised launchd jobs, named contractors on standby. Your internal docs are unusually good; that is a genuine asset here.
- *"Who does distribution?"* → No rhetorical answer exists. Hire #1 is growth/content — name the profile with a start date, and show it's the largest line in the use of funds.
- *"Who owns compliance?"* → The RA advisory bench plus a fractional compliance consultant, budgeted.
- *"Why no co-founder?"* → Say the honest version: what got built alone in twelve months is the evidence, and you would rather add the right partner at month 9 than the available one at month 0.

**Do not** hide the solo status, and do not gesture at vague "advisors" — name them, with signed agreements. Investors discount ambiguity harder than a clearly-owned weakness.

### 3.6 Scope sprawl — *the most self-inflicted wound in your current materials*
`plan.md` runs research → live data → alpha lab → algo execution → **broker licence** → **HFT**. Internally that is a fine long-range thesis. In a pitch it is a liability. A ₹3–5Cr broker capital requirement and an NSE colocation rack read to an investor as *this founder does not know what to say no to* — which is precisely the trait pre-seed investors screen hardest for in solo founders.

**Cut Phases 5 and 6 out of the pitch entirely.** Not "later" — gone. Execution (Phase 4) survives only as one line on a vision slide. What you are raising for is a research product that becomes a daily habit and gets paid for. Depth beats breadth in a 12-minute meeting.

### 3.7 The Anvest Score is a regulatory liability as currently framed — *cheap to fix now, expensive later*
A proprietary score with pros/cons on a page a retail investor reads is functionally close to a recommendation, and SEBI has explicitly held that "educational" disclaimers do **not** exempt actionable signals. Corporate RA registration is ~₹5L in fees plus the RAASB lien-marked deposit, revised NISM-XV certification, and — under the Dec-2024 amendments — an affirmative obligation to disclose the extent of AI use and full accountability for AI output.
**Fix now (₹0):** hard product rules — no buy/sell/hold language, no target prices, score framed and labelled as a data summary, disclaimers on every AI surface, and a copy review before any public launch. **Fix later (₹5.5L + GST, budgeted in the raise):** register. Your "grounded or silent" invariant is, conveniently, already the compliance architecture the amendments contemplate — say that out loud; it turns a cost centre into a differentiator.

### 3.8 Willingness to pay is entirely unproven
Screener.in at ₹4,999/yr and Trendlyne at ₹2,190–5,900/yr prove the market exists. But Indian retail is genuinely price-sensitive and competitors run generous free tiers. Your ₹249/mo plan is a guess. **Test it in Track C with 20 real transactions before you put a revenue model in a deck.** One paying user is worth more than any pricing analysis.

### 3.9 Uncommitted work and stale tests
Entire modules untracked in git (broker-portfolio's `research_providers/`, telemetry, prompts), ~40 one-off scripts at workspace root, a local venv on Python 3.9 running code that needs 3.10+, three copilot tests asserting JSON against an SSE endpoint. Any technical diligence includes a repo walkthrough. **Cost:** 2 days (gaps C1–C3, C5).

### 3.10 Vertex quota ceiling
429s at ~2–6 concurrent requests. That is not a platform that survives a Product Hunt spike, and it is a trivially avoidable embarrassment. **File the quota raise this week** — it is free and takes days. Prove the vLLM-on-spot-L4 fallback during the backfill so you have a second answer.

---

## 4. Product-Market Fit: What Is Actually Missing

You have **product**. You do not have **fit**, and the gap is more specific than "no users."

### 4.1 The structural problem: research tools are ask-driven, and ask-driven products have terrible DAU/MAU

This is the crux of what you asked about retention. A user opens a research tool when they have already decided to research something — which for a typical retail investor is a handful of times a month. That ceiling is a property of the *interaction model*, not of your execution. You can build a perfect ask-driven product and still see DAU/MAU around 10%.

Every high-DAU/MAU finance product solves this the same way: **it has something to say before you ask.** Broker apps have your P&L. Groww has your portfolio moving. Anvest, today, waits to be asked.

**The single highest-leverage feature you have not built is the proactive digest.** *"Since you last viewed HDFC Bank: Q1 beat on margins, promoter holding unchanged, two analyst meets scheduled."* It reuses the evidence builder and cache you already have — it is days of work, not months — and it converts the product from a tool into a habit. It is already correctly identified in `plan.md` §3 1.2 and `GTM_PLAN.md` as the top retention build. **Ship it before the alpha cohort, not after.** DAU/MAU is the metric your raise will live or die on, and this is the mechanism.

Sequence the habit loop deliberately:

| Trigger | Mechanism | Cadence |
|---|---|---|
| Portfolio moved | Digest on holdings, grounded in filings | Daily, market days |
| Filing landed on a watched name | Push/email: what the filing actually said | Event-driven |
| Score or fundamental changed materially | Explained delta, with the source | Weekly |
| Tax event | ITR workspace nudge | Seasonal (Jun–Aug) |

### 4.2 The "aha" is unvalidated
Your hypothesis — first grounded answer with a citation on a stock the user owns — is a good one. It is still a hypothesis. Until you have watched ten strangers hit it or fail to, you are guessing. Five 15-minute calls with real users will teach you more than the next 5,000 lines of code.

### 4.3 Portfolio connection is the PMF unlock, not a feature
Almost everything that makes Anvest personal — digest, X-ray, tax, relevance ranking — needs to know what the user owns. Read-only broker OAuth (Kite first) has no execution-compliance burden and is the highest-value integration on your list. **Prioritise it above every remaining data-quality task except the trust badges.**

### 4.4 Retail may not be your first revenue — and this changes the whole raise
Consider seriously reordering your GTM. `GTM_PLAN.md` puts B2B research seats at Phase 3 (months 5–9). **Move it to now.** The arithmetic is stark:

- 100 retail Pro subs at ₹249/mo = **₹25K MRR**, requires thousands of free users, months of SEO, and a payments funnel.
- 40 professional seats (SEBI-registered RAs, boutique PMS analysts, research associates) at ₹3,000/mo = **₹1.2L MRR**, requires ~150 conversations.

The second is faster, higher-ARPU, needs no consumer scale, and — critically — is *far* more fundable. "₹1.2L MRR from 40 professional seats, 3,000 free retail users, growing 40% MoM" is a real pre-seed. RAs already pay for research productivity tools and feel the pain of reading filings manually every single day. They are also your best distribution: an RA who uses Anvest recommends it to clients.

B2C retail remains the long-term prize and the story. B2B is how you get funded to build it.

### 4.5 The ITR window is open right now and closes in five weeks
This is time-critical and easy to miss: **ITR-1/2 filers are due July 31, 2026 (five days). ITR-3/4 non-audit filers — which is every F&O trader — are due August 31, 2026** (a permanent change under the Finance Act 2026, not an extension).

Your ITR engine already handles ITR-3 with F&O business handoff, and F&O traders are exactly the segment SEBI's crackdown is pushing toward investing — your stated segment #2. You have a working compiler, a live domain, and a five-week window of the highest-intent, most-searched financial query in India.

**This is the cheapest user acquisition you will ever get, and it hands you portfolio data as a side effect.** Free ITR-3 compilation → import broker P&L → those holdings seed the research copilot and digest. Counter-seasonal, zero-CAC, and no competitor in research does it. If you do one growth thing in the next five weeks, do this.

Two hard caveats: (a) tax software errors are a legal and reputational hazard — ship it as "generates the official JSON for you to review and upload," never as "we file for you," with your 4-layer validation surfaced to the user; (b) it must not consume the whole quarter. Two weeks of polish and a landing page, then back to the core loop.

---

## 5. Market–Product Gaps: Where Anvest Fits

The market context is in `GTM_PLAN.md` §2–3 and holds up. The compressed funding version:

**The tailwind is regulatory, which makes it durable.** SEBI's own FY25 study: 91% of individual F&O traders lost money, ₹1.06 lakh crore in net losses, up 41% YoY. The top four brokers shed ~2M active investors in H1 2025 as margin rules and expiry limits bit. The regulator is actively herding retail from speculation toward research and investing. A trustworthy research product is not fighting the current.

**Every incumbent sits in exactly one of three camps, and none occupies the middle:**

| Camp | Who | What they can't do |
|---|---|---|
| Tables without conversation | Screener.in, Trendlyne, Tickertape, StockEdge | Assume you already know what ROCE means and what to ask. Serves the top ~5%. |
| Tips without transparency | Univest, MarketsMojo, advisory apps | Black-box "buy X target Y." Trust dies with the first bad call. Regulatorily heavy. |
| Conversation without a warehouse | Perplexity Finance, ChatGPT | Fluent and wrong. No point-in-time Indian XBRL, no OCR'd SME filings, no accountability. |

**The unoccupied position:** a grounded AI equity research analyst for Indian retail — conversational like Perplexity, numerically trustworthy like Screener, explainable unlike Univest.

**The scale of the gap:** ~210M demat accounts. Perhaps 5M use a Screener-class tool. The other ~205M get their research from WhatsApp forwards and YouTube. You are not fighting Screener for its 5M; you are building the product the other 205M can actually use — and the ladder from novice-explainer to expert-tables is the mechanism.

**The category is proven at the institutional tier, which is your valuation argument.** AlphaSense raised $350M in 2026 at a $7.5B valuation on $600M+ ARR, used by ~80% of top hedge funds. Rogo closed a $75M Series C in January 2026 at $750M post-money. Grounded AI research over financial documents is a demonstrated multi-billion-dollar category — it has simply never been built for Indian retail, where the addressable population is two orders of magnitude larger and nobody has done the data work.

**Positioning line for the deck:** *"AlphaSense for 200 million Indian retail investors."* One clause, instantly legible, and true.

---

## 6. Direction: What To Cut, What To Double Down On

The strategic pushback on your current roadmap:

**Cut from the story, defer in the build:**
- Broker licence (Phase 5) and HFT (Phase 6). ₹3–5Cr capital, 12–18 months, a different company. Gone from every investor conversation.
- Algo execution (Phase 4). One vision-slide line, no more.
- Alpha lab / DRL (Phase 3). Genuinely interesting, but pre-seed capital buys distribution and retention, not research theatre. Deep RL in a pre-seed deck actively hurts you — it signals a founder optimising for intellectual interest over users.
- Live real-time market data *as a paid feed*. You are EOD today — bhavcopy ingested at 7pm — and that is genuinely sufficient for a research use case; label it "as of yesterday's close" and move on. Live quotes and live portfolio tracking are a real near-term unlock, but the cheap path is broker websockets on accounts the user connects themselves, plus free delayed snapshots on the top ~500 symbols. Do not buy a feed licence pre-revenue.

**Double down on, in strict order:**
1. **Trust badges + citations rendered.** Your entire differentiation is provenance. Ship it, then say it everywhere.
2. **Proactive digest.** The DAU/MAU mechanism. Days of work. Highest leverage remaining build.
3. **Read-only broker OAuth.** Makes everything personal. Unlocks digest, X-ray, tax — and it is the same integration that later delivers live quotes and live portfolio tracking, so it is not a detour.
4. **B2B research seats.** Fastest path to defensible revenue and to a fundable metric.
5. **ITR-3 free tier — the next five weeks.** Zero-CAC acquisition with a portfolio-data payload.
6. **Programmatic SEO.** 6,137 pages with genuinely unique AI-generated content answering "is X a good stock" — a query Screener's bare tables structurally cannot answer. Highest-ROI organic channel and it compounds while you sleep. Needs ISR/SSG, structured data, sitemap.

**The 18-month direction in one line:** *become the default place an Indian retail investor goes to understand a company, monetize it as a subscription with a professional tier, and earn the right to execution later.* Not "become a broker."

### 6.1 Holding the bigger ambition without looking unfocused — the horizons frame

I earlier said to cut the broker and HFT phases entirely. That was right about *pitch time* and wrong as a blanket rule, so here is the sharper version. There is a professional way to hold a large ambition in a pre-seed room, and it is to put it on a timeline with capital gates attached:

| | Window | What | How it's funded |
|---|---|---|---|
| **H1** | now → 18 months | India research. The default surface. Subscription + professional seats. | **This round.** The only horizon you ask them to underwrite. |
| **H2** | 18 → 36 months | Execution layer (read-only broker link becomes order routing under the SEBI retail-algo framework) **+ the first international market.** | Seed / Series A, gated on H1 metrics. |
| **H3** | 36 months + | Alpha lab, backtesting, and ultimately the broker licence. | Separate, capital-intensive, explicitly not costed into this round. |

The distinction that matters: **H2's global expansion is the same business in a new geography — the standard market-expansion vector every VC wants to see. H3's broker licence is a different business** with different capital, licences and headcount. Naming H3 on one line signals you know the destination. Spending pitch time on it signals you cannot prioritise. One slide, one line each, then move on.

### 6.2 Global — after India PMF is proven, not before

**The thesis:** what took a year to build is not India-specific. The *architecture* — statutory-filing ingestion, OCR over scanned PDFs, chunking and embedding, coverage gating, grounded synthesis with verification — is market-agnostic. What is India-specific is a thin top layer: the XBRL dialect, the exchange's particular malformations, the local filing calendar and language. **Swapping that layer is months, not years.** The moat replicates; the work does not repeat.

**The qualifying test for a target market** — all four must hold:

1. Mandatory structured financial disclosure (so a warehouse is buildable at all)
2. A large, growing, underserved retail investor base
3. No incumbent that has already done the filings-corpus work
4. English or a language with strong model support for the parsing layer

**Where that points, in order:** Indonesia, Vietnam and the Philippines (large young retail bases, rapid demat growth, thin research tooling) · UAE and Saudi (high-value users, capital-markets buildout, English-friendly filings) · Brazil (scale, retail boom, but Portuguese-language parsing and a more crowded local field).

**Deliberately not first:** the US, UK and EU. Those markets have AlphaSense at $7.5B, Fiscal.ai, Koyfin and a dozen others. The gap Anvest exploits — *nobody bothered to build the data layer* — does not exist there. Developed markets are an H3-or-later consideration, and probably as a professional/B2B product rather than retail.

**The hard gate — write it down so you don't drift:** no second market until India shows **≥25% DAU/MAU, ≥₹15L MRR and a positive contribution margin per user.** A research product nobody has validated in one market is not a platform, it is a demo in two languages. India first is a discipline, not a ceiling — and saying so out loud is what makes the global slide credible rather than hand-wavy.

**Why it belongs in the pitch anyway:** it is the answer to "how big can this get?" India alone caps the story at a few hundred crore of ARR. The same pipeline across four emerging markets is the difference between a good outcome and a fund-returner — and that is the calculation your investor is actually running.

---

## 7. The Raise

### 7.0 "Is 14% for ₹3Cr too much to give away?" — and the answer to *most money, least dilution*

**Currency note:** this section is USD-first because YC is the current priority and prices in dollars. Rate used throughout: **₹96.57/USD (26 Jul 2026)** — check it before quoting anything, it has moved ~11% since the start of the year.

**Target: $500K (≈₹4.83Cr) at 7–12%.** That clears your ₹3Cr floor with room, and it is exactly the size of YC's standard deal — which is not a coincidence, and is the whole answer to your question.

#### The misconception worth naming first

Valuation is not set by the size of your ambition. It is set by evidence of progress against risk retired. "This is just step one, we'll be the all-in-one platform" is the single most common sentence in venture — investors have heard it thousands of times and it moves the cap by exactly zero. What moves it: users, revenue, growth rate, team pedigree, competitive urgency. **Asking for a higher cap because the roadmap is bigger is the fastest way to get passed on**, because it signals you don't understand how the instrument is priced.

So "most money for least dilution" is not a negotiating posture. It is a function of two things you can actually change: **which investor you're talking to, and how much risk you've already retired.**

#### The single best deal available to you is the one you're already applying for

| | Money in | Equity now | Effective post-money |
|---|---|---|---|
| **YC standard deal** | **$500K** | **7%** for the first $125K | ~$1.79M on the priced tranche; **$375K on an uncapped MFN** that prices at your *next* round |
| India pre-seed, no traction | $310K (₹3Cr) | 14.3% | ~$2.2M (₹21Cr) |
| India pre-seed, with traction | $400–500K | 10–12% | $4–5M |

Read the top row carefully. **YC gives you 60% more money for half the equity** — and the larger $375K tranche is uncapped, so it converts at whatever your next round prices at rather than locking in today's zero-traction valuation. If you are optimising for maximum capital at minimum dilution, YC's standard deal is not merely competitive, it is the best instrument on this page. It is also why the sequencing in §0 matters more than any term you'll negotiate: **YC acceptance is worth more than every negotiating lever combined**, and the second-best lever — traction — is the same thing that gets you accepted.

#### The three structures, in order of preference

| | Raise | Post-money cap | Dilution | Runway | When |
|---|---|---|---|---|---|
| **A. YC** ⭐ | **$500K** | 7% priced + MFN | **~7% now** | 18 mo, 3 hires | If accepted. Everything else becomes a top-up. |
| **B. Post-YC / with-traction round** | $400–500K | $4–5M | 10–12% | 18 mo, 3 hires | After YC acceptance, or after Track C. A YC badge or ₹1L MRR both support this cap. |
| C. India pre-seed, cold | $310–400K | $2.2–3M | 13–15% | 15–18 mo | Only if A and B both fail. This is the structure you were quoted, and its problem isn't the 14% — it's that it prices you at your weakest moment. |

**The honest constraint:** at zero traction and no YC badge, you don't get to pick between these — the market picks for you, and it picks C. There is no clever structure that yields $500K at 8% from a cold Indian angel who has just been told the product has no users. **Both levers that move you from C to B are things you do, not things you ask for.**

#### The four levers that genuinely reduce dilution, ranked

1. **Get into YC, or generate traction.** Same lever, different label. Worth 5–8 points.
2. **Revenue.** Every dollar of MRR is a dollar you don't raise. 40 professional seats at $35 = $1,400/month ≈ $17K/year of burn you never dilute for.
3. **Raise less now, more later at a higher price.** $100K taken now at a $2.3M cap costs 4.3%. The same $100K at a $9M seed costs 1.1% — one-quarter the dilution for identical capital.
4. **Uncapped or high-cap MFN notes** for part of the round. YC's $375K tranche is precisely this instrument; you can replicate the structure with angels.

#### The part to sit with

Your stated destination — research → algo → alpha → backtesting → **broker** — is capital-intensive by construction. SEBI stockbroker registration plus exchange membership realistically needs **₹3–5Cr (~$310–520K) of regulatory capital alone**, before opex, compliance headcount, OMS/RMS and deposits. You cannot reach that on $500K, or on $5M. Carta's 2026 data puts the median founding team at **~56% after seed, ~36% after Series A, ~23% after Series B** — and that is the *normal* path, not a cautionary tale. If you raise what H3 requires, you will hold something in the 15–25% range by the time you are a broker.

Two coherent strategies. Pick one deliberately rather than drift:

- **The venture path.** Dilution is the price of a capital-intensive destination. Optimise for company value, not ownership percentage. 20% of a $600M company beats 80% of a $12M one.
- **The Zerodha path.** They built India's largest broker with zero VC — by being profitable from brokerage revenue almost immediately. Your equivalent: monetise research hard and early, stay default-alive, fund each horizon from the last one's cash flow. Slower, may forfeit the timing window, demands revenue discipline from month one. But you keep the company.

**You don't have to choose today** — and YC's structure happens to keep both doors open, since $500K at 7% leaves you majority-owned with real runway. But do not raise venture money while privately planning to keep 80%. That mismatch surfaces later as a governance fight.

**The framing that should settle it:** dilution is only expensive if the capital doesn't buy more progress than it costs. $500K that takes you from 0 to 15,000 MAU and $21K MRR raises the company's value by far more than 7%. The question is never "how much am I giving up" — it is "does this money retire enough risk to be worth its price." Right now, for you, it clearly does.

### 7.1 Structure

> **Revised 2026-09-03.** YC rejected the Fall 2026 application. The two-track structure below collapses to one, and the cap comes down from $5.0M to **$3.5M**. The reasoning is at the end of this section under *"Why the cap moved"* — read that before quoting any number to anyone.

**The single track — the campaign every investor is offered.** Angels, micro-VCs, Rainmatter, Groww, any strategic: same instrument, same cap. **One fixed structure for everyone — see the rule below before anything else.**

#### The rule: same cap for every investor, always

Never offer different investors different valuations in the same round. In a market as small and networked as Indian fintech VC, investors compare notes — Rainmatter's team and a micro-VC partner have almost certainly been in a deal together before. A founder caught pricing the same round differently for different people doesn't get a second meeting with either. The narrative can — and should — differ by audience (§7.4). The price never does.

#### The mechanism for "maximum funding, minimum dilution": a fixed cap with room to upsize

The instinct to raise more by raising the cap is backwards — a higher cap with no evidence to support it gets a worse reception, not a better one (§7.0). The correct lever is the other direction: **hold the cap fixed, and let more capital in at that same price if there's demand.** Every additional dollar at a fixed cap costs the same dilution per dollar as the first one — it doesn't get more expensive as more investors want in, which is exactly what "maximum funding for minimum share" means in practice.

| | **Base round** | **Upsized (if demand supports it)** |
|---|---|---|
| **Post-money cap** | **$3.5M** (₹33.5Cr) — fixed, identical for every investor | Same $3.5M — does not move |
| **Amount raised** | $400K | up to **$700K** |
| **Dilution** | **11.4%** | up to **20%** |
| **Instrument** | CCD/CCPS for Indian angels and funds; post-money SAFE where an investor is set up for one — same cap expressed in the appropriate instrument for each jurisdiction | Same |
| **Runway** | 15–18 months, 2 hires + advisors (§7.2) | 18 months, 3 hires + the reserve line spent rather than held (§7.2) |

Both ends sit inside the benchmarked band — 11.4% is at the disciplined end of India pre-seed (10–15%), 20% is the top of the seed band and still below where a lead expects board rights or a priced round. **$3.5M is the number to defend, not $400K or $700K** — that's the one figure that must not move regardless of how the round fills.

**Where the upsize capacity is most likely to be used:** an institutional pre-seed lead (Eximius, a micro-VC, or a broker-affiliated strategic) wanting a larger allocation than a typical angel cheque. Reserve **$200–300K of headroom** explicitly for that rather than allocating the whole $400K to angels first and having nothing left when a fund wants a real position.

Everything below is modelled on the **$400K base case**; the use-of-funds table (§7.2, still written against $500K) needs the reserve/contractor line trimmed first — that line is designed to absorb exactly this.

| | |
|---|---|
| **Structure note** | Convertible/SAFE, not priced. At this stage a priced round means a valuation argument you cannot win, plus ₹3–5L in legal fees. It defers the fight to a seed where your metrics do the arguing. |
| **Advisor equity** | ~2% total across 2–3 RA/PMS advisors, FAST terms (0.5–1% each, 2-year vest, 3-month cliff). Non-cash — it does not consume the raise. Grant *before* the round closes so it sits below the cap, not above it. |

#### Why the cap moved from $5.0M to $3.5M

The $5.0M number rested on three legs. Two of them broke in August.

1. **The YC application, submitted and pending.** Gone — rejected (§9). A rejection is not a negative signal to investors (acceptance is ~1%, and nobody weighs a rejection), but it is no longer a *positive* one either. It cannot be cited, hinted at, or implied in any conversation.
2. **"Nobody else is doing conversational AI over an Indian filings corpus."** Gone — **Screener.in shipped exactly that, metered, and priced it publicly** (`SUBSCRIPTION_MODEL_2026-08-31.md` §4.2). The incumbent with the largest DIY-investor audience in India is now in the category. The moat argument survives and is arguably sharper (their cost scales per document read, ours doesn't — §7.4 and the pricing doc), but "empty category" is no longer available as a valuation argument.
3. **The depth of what was built solo.** Intact, and still the strongest thing on the table.

Against that, one leg got *better*: there are now **60 registered users** where there were zero. Small, but the difference between "pre-launch" and "launched with early users" is a real category change in how a pre-seed investor reads the company.

**The comparable that settles it, and the one an India fintech investor will know cold:** Trendlyne — a mature product with real users and revenue — has raised **$2.64M in total across five rounds**. Tickertape raised a **$5M seed** and was then acquired by Zerodha. This category, in India, has historically not been a big-cheque venture category. Walking into a fintech-literate fund with a $5.0M cap, 60 users and no revenue invites exactly the comparison you do not want.

$3.5M sits at the top of the Indian seed cluster (₹15–25Cr pre-money ≈ $1.6–2.6M) without crossing into the band that requires metrics to defend, and is *conservative* against micro-VC convention (sub-$40M funds lead $500–800K for 8–12%, which implies $4–10M post). Priced there, the round is an easy yes rather than a negotiation — and that is the actual mechanism for "most money, least dilution."

**The arithmetic that justifies taking the lower number.** 11.4% at a cap that clears beats 10% at a cap that doesn't. A round that sits open for six months at an undefendable price and then reprices costs more total dilution than one priced to close — plus six months of runway, and the reputational cost of a visible down-move in a market where investors talk to each other.

**What earns $5.0M back — and the trigger to reprice upward:** revenue. Not users, not another product surface. **The moment there are ~20 paying B2B seats (~₹60K MRR) or ₹1L MRR from any mix**, the conversation changes from "pre-revenue research app" to "early-revenue B2B data company," and $5.0M+ becomes defensible on the numbers instead of on the story. If that lands mid-round, do **not** reprice the investors already committed — honour the $3.5M for everyone in this round (the rule above), and take the higher number at the seed. `SUBSCRIPTION_MODEL_2026-08-31.md` §4.4 argues those seats are reachable from ~150 conversations, which is a faster path to a better valuation than any amount of pitching at the wrong price.

### 7.2 Use of funds

Modelled on **$500K over 18 months** (~$28K/month). Rupee figures at ₹96.57/USD.

| Line | Amount | Why |
|---|---|---|
| Hire #1 — growth / content (18 mo) | **$67K** | Answers the "who does distribution" objection. SEO + fintwit + creator partnerships. Non-negotiable for a solo founder. |
| Hire #2 — data / backend engineer (15 mo) | **$52K** | Closes B8/B9 properly, owns ingestion, removes the bus factor. |
| Hire #3 — full-stack, from month 6 (12 mo) | **$36K** | Ships the habit loop and the B2B surface. |
| Hire #4 / contractor pool (opportunistic) | **$45K** | Held in reserve. Deploy only if Track C proves a specific bottleneck — do not pre-commit. |
| Compliance + legal | **$25K** | SEBI RA registration (~₹5.5L + GST), RAASB lien-marked deposit, data-provenance counsel opinion, AI-disclosure copy review. |
| Infra, inference, data | **$45K** | Serving VM off the Mac, Vertex/inference, spot-GPU batch, Vercel Pro, broker API (unlocks live quotes + live portfolio tracking). |
| Growth experiments | **$60K** | Creator partnerships, ITR-season landing pages, the first real paid tests to establish a CAC number. |
| Founder salary (18 mo, modest) | **$45K** | Investors prefer a paid founder to a distracted one. |
| Buffer / contingency | **$125K** | 25%. Deliberately large, and say so: at YC terms it costs nothing extra, and it converts an 18-month plan into ~24 months if hiring slows. Runway is the only thing that reliably buys a better next round. |
| **Total** | **$500K** (≈₹4.83Cr) | |

**If the round comes in at $400K instead:** cut hire #4 ($45K) and half the buffer ($55K). Everything H1 requires still ships. Nothing above hire #3 is load-bearing.

### 7.3 What the round must produce (the seed story you are pre-selling)
By month 15: **15,000 MAU · DAU/MAU ≥ 25% · $21K MRR (₹18L) · 150+ professional seats · SEBI RA registered · Recall@5 ≥ 0.85 published · live quotes and live portfolio tracking shipped.** That is a **$9–14M seed raising $1.5–2M**. Say this in the pitch — investors buy the *next* round's story, not this one's.

### 7.4 One round, two narratives — never two prices

The document kit (`INVESTOR_DOCUMENT_KIT.md`) is built around a single discipline: **the deal terms in §7.1 are identical for every investor in Track 2. Only the story changes, and only along one axis — whether the investor has a distribution channel Anvest could plug into.**

**Narrative A — the platform story.** For generalist angels, micro-VCs, and any fund without a consumer or broker distribution asset (Titan, Sparrow, All In, Better, Gemba, the operator/RA angel tier). Anvest as a standalone destination: the AlphaSense-for-India research product, the horizons framework (H1 research → H2 execution + global → H3 full stack), the moat, the traction plan. This is the deck already built (`Anvest_PreSeed_Deck.pptx`).

**Narrative B — the integration story.** For investors who *are*, or are affiliated with, a brokerage: Rainmatter (Zerodha), and — with the caveat below — Groww. The pitch inverts: instead of "invest in us as a destination app that competes for the same user's attention as your own platform," it's **"invest in us as the AI research layer that makes your existing platform stickier, without you having to build it."** This directly resolves the Rainmatter/Tickertape conflict flagged in §8 — reframed as complementary rather than competitive — and turns Anvest's biggest current limitation (end-of-day data, no broker relationship) into the reason the strategic should want in: a broker partnership is what upgrades Anvest to live data, and Anvest is what gives the broker a grounded AI layer they don't have to build in-house. Grounded concretely in a real, current fact: Zerodha has already built **Kite MCP**, a Model Context Protocol endpoint that lets AI assistants connect to a user's live Zerodha account — Rainmatter's own team has signaled, through the product itself, that this is a thesis they're actively building toward. Anvest is exactly the kind of grounded, citation-first, verify-before-answering AI system that a broker would want sitting on top of that connection rather than a generic chatbot. This is the new deck (`Anvest_Strategic_Integration_Deck.pptx`).

**On Groww specifically — treat as narrative B in tone, but calibrate expectations.** Groww's own investment history (Digio, Nimbbl, CoinCRED, Cybrilla — five deals, all fintech infrastructure/plumbing, not consumer research apps) suggests they invest opportunistically in adjacent infrastructure rather than running an active fund the way Rainmatter does. Groww also already has its own in-app research and discovery surface, which makes them more directly a competitor than a natural integration partner. Approach as a strategic/corp-dev conversation rather than a standard VC pitch, keep expectations modest, and don't lead the outreach sequence with them — Rainmatter is the stronger, better-grounded version of this exact thesis.

**Dilution path at YC terms:** 93% after the $125K priced tranche → ~91% after ~2% advisors → ~82% after a 10% ESOP pool → **~66% after a 20% seed** (before the $375K MFN converts, which costs a further 2–4% at seed pricing). Healthy for a solo founder two rounds in. On Structure C the same chain lands nearer 60%.

---

## 8. Investor Targets, Ranked by Probability

> **Rewritten 2026-09-03**, post-YC-rejection. The previous version ranked by *fit*. This one ranks by **probability of a cheque within 90 days**, which is a different and more useful ordering when there is no accelerator badge coming and the runway is the founder's own salary. Fit still matters — it is the tiebreaker, not the sort key.

**The filter applied to every name below:** actively deploying into **India**, and either fintech-focused or with demonstrated fintech deal flow. Funds that invest globally but rarely in India, or in India but never in fintech, are not listed regardless of brand — they are a slower "no" dressed as a maybe.

### 8.0 The two facts that move every probability on this page

Before the list, the two variables that shift these odds more than any choice of investor:

1. **Full-time or not.** Every institutional investor below will ask, in the first meeting, whether the founder has left the job. A solo founder who is still employed is, to a pre-seed fund, an unfunded hypothesis — and several of these funds (100X.VC, Eximius, any accelerator) treat full-time commitment as a hard filter, not a preference. If the answer is "I leave when the round closes," say exactly that and name the date; if the answer is vaguer than that, the round is materially harder to close than anything below implies.
2. **First revenue.** ~20 B2B seats (~₹60K MRR) or ₹1L MRR from any mix moves this company out of "pre-revenue research app" and into a category where the numbers argue instead of the story (§7.1). `SUBSCRIPTION_MODEL_2026-08-31.md` §4.4 puts that at roughly 150 conversations. **That is fewer conversations than this investor list contains** — which is the single most important sentence in this section.

---

### Band 1 — Start here. Highest probability, fastest, and useful beyond the cheque.

**1. Category B angels — SEBI-registered RAs, boutique PMS founders, ex-brokerage product heads.** ₹10–25L each, 8–15 of them.
Highest-probability money available to this company, and the reason is structural: **they are also the customer**. An RA who buys a ₹2,999/month Desk seat has already diligenced the data by using it, and an angel cheque from someone who is already paying is a fundamentally easier conversation than one from someone evaluating a pitch. Capital, first revenue, product feedback, and regulatory cover arrive in the same relationship.
- *Why this is now first rather than third:* the B2B beachhead argument (`SUBSCRIPTION_MODEL_2026-08-31.md` §4.4 — 40 seats at ₹2,999 = ₹1.2L MRR vs 100 retail Pro at ₹417 = ₹42K MRR, at 90.8% contribution margin) means the sales pipeline and the angel pipeline are **the same list of people**. Working it produces revenue whether or not it produces a cheque, and revenue is what repairs the valuation (§7.1).
- *Path:* the SEBI RA public register; LinkedIn; fintwit. Lead with a seat, not a raise.

**2. Category C angels — fundamentals-focused finfluencers (50–300K subs).** ₹5–25L each, plus a revenue-share referral.
Capital and distribution in one line item; the highest-leverage cap-table entry available to a solo consumer-fintech founder. Approach with a working demo run **on their own portfolio**.
- *Regulatory care:* a creator promoting a research product touches SEBI advertising and advice rules. Get the copy reviewed. Avoid anyone who sells tips — their audience is the wrong audience and the association is a liability at RA registration.

**3. Eximius Ventures — the best institutional fit in the country for this specific company, right now.**
Pre-seed fund, Delhi NCR + Bengaluru, **thesis-driven with FinTech as a named vertical**, initial cheque **~$500K**, and explicitly invests at the *pre-product / early-traction* stage — which is precisely where 60 users and no revenue sits. **Fund II is a $30M vehicle targeting 25–30 companies**, i.e. fresh capital with a mandate to deploy. 34 investments to date, 4 in the trailing twelve months. Fintech portfolio includes Jar, Finarkein and Vegapay.
- *Why they rank above the generalist micro-VCs:* a fintech thesis means no time spent explaining what XBRL is, why SEBI RA registration matters, or why a filings corpus is hard. At pre-seed, the investor who already understands the domain is worth more than the one with the bigger brand.
- *Path:* direct via eximiusvc.com; portfolio-founder intro (Finarkein is the closest thematic neighbour).

---

### Band 2 — Institutional pre-seed. Real process, 4–10 weeks, any one can lead.

**4. Better Capital.** India's largest pre-seed fund by volume — 200+ companies, solo-GP model. Backs technical first-time founders, which is the profile here. Fast, decisive, low-ceremony.

**5. All In Capital · Gemba Capital · Whiteboard Capital · Inuka VC · Zeropearl · OTP Ventures · Sparrow Capital.** The matured India micro-VC tier — the category has grown from ~100 funds in 2022 to **200–250+ by 2026**, with average fund size now $25–30M. Convention: **sub-$40M funds lead $500–800K for 8–12%**; $40–100M funds lead $1–1.5M for 12–15%. Any one of them can take the whole $400K base at the $3.5M cap, and at that cap they are being offered a *better* price than their own convention implies.
- *Source of truth:* Blume's validated list of ~200 sub-$100M India funds (published April 2026) — every fund on it has been spoken to, co-invested with, or independently verified by Blume. Use it instead of a generic database.

**6. Titan Capital** (Kunal Bahl / Rohit Bansal). Sector-agnostic, pre-seed native, Fund III. Strong downstream signalling for the seed. Slower and more competitive than Band 1; worth the process for the signal alone.

**7. WaterBridge · India Quotient · Huddle.** Delhi/Bengaluru seed funds that write genuine first cheques and have fintech in the book. Second wave — approach after two or three Band 1/2 conversations have sharpened the pitch.

**8. AI-lane micro-VCs — Z21 Ventures, Neon Fund, Bold Capital, Grayscale.vc, FortyTwo VC, Sense AI.**
Worth more attention than the previous version of this list gave them, for one reason: **AI startups took $676M across 57 deals in H1 2026, up 317% YoY — the defining sector story of this funding cycle.** The grounded-retrieval-with-verification architecture is a genuine AI story, not a wrapper story, and these funds can evaluate that. Weaker on Indian retail-fintech nuance, so lead with the architecture (bounded evidence packs, verify-and-repair, published retrieval eval) rather than the market.

---

### Band 3 — Strategics. Different narrative (§7.4), same terms, slower clock.

**9. Rainmatter (Zerodha) — still the best thematic fit, but recalibrated downward on timing.**
₹1,500Cr+ across 160+ companies since 2016; no board seats, no operational interference; patient capital. **But the honest read of their current deployment:** the portfolio is now most concentrated in **climate tech (44 companies)**, then health and fitness (41), with fintech third at 37 — and the publicly visible 2026 investments (Lissun, Arboreal, Immuneel Therapeutics, VoltSeal, Farm Watt) are climate and health, not fintech. They have not left fintech — they participated in **Wint Wealth's $27M round** — but a first-cheque fintech bet is not where their marginal rupee is currently going.
- *What this changes:* Rainmatter stays on the list and keeps its own deck (`Anvest_Strategic_Integration_Deck.pptx`), but should **no longer be treated as the first stop**. Run it in parallel with Band 1, not ahead of it, and do not let the round's timing depend on it.
- *The conflict, unchanged:* Zerodha owns Tickertape. Raise it yourself in meeting one; the integration narrative (§7.4) is the answer.

**10. Nithin / Nikhil Kamath (personal angel route).** Coordinate as one effort with Rainmatter — never two uncoordinated threads. Nithin responds to substantive public technical writing; a published data-corrections changelog or a retrieval-eval writeup is a better approach vector than a cold pitch.

**11. Groww / Lalit Keshre — BD conversation, not a VC pitch.** Groww Ventures' disclosed history (Digio, Nimbbl, CoinCRED, Cybrilla) is opportunistic infrastructure investing, and Groww ships its own in-app research surface. Lead with partnership; hold the equity ask. Template C in `COLD_EMAILS.md`.

---

### Band 4 — Not now. Meet for free, explicitly "not raising."

Accel and Lightspeed remain the two most active India fintech investors by deal count. **Lightspeed led Centricity's $20M wealthtech seed**; **Bertelsmann India backed Univest**; **Vertex Ventures SEA & India led Wint Wealth's $27M** (with Eight Roads, 3one4, Arkam and Rainmatter participating); **TVS Capital led Neo Group's $53M** at a $1.1bn valuation. Also: Peak XV/Surge, Elevation, Z47, Prime Venture, Blume, Arkam, 3one4.

The market context that makes this a *later* list rather than a *no* list: Indian fintech raised **$2.2B+ across 100+ rounds in H1 2026 — the strongest half since H1 2023**, and wealthtech specifically rose **84% YoY in Q1 ($560.8M across 18 deals)**. The money is emphatically there. But average wealthtech deal value in that quarter was **$31.2M** — it is concentrated in companies with metrics. Meet these funds now, framed as *"not raising, would value your view in six months."* It costs nothing and starts the seed round warm.

### Explicitly not targets, and why

- **Fundamentum.** Appears at the top of Q1 2026 India-fintech *seed* league tables, which is misleading. Fundamentum invests at **Series B/C**, and Fund III writes initial cheques of roughly **₹100Cr (~$10.5M)**. Approaching them now wastes the introduction.
- **Antler India.** Day-zero residency and co-founder matching is most of the value proposition, and neither applies — there is a built product and no co-founder search. Takes a large equity chunk for the stage. Skip unless the round stalls completely.
- **Anyone requiring a co-founder as a precondition.** §3.5 settles this: the fix is the advisory bench, not a late co-founder hunt conducted under fundraising pressure.

### Accelerators — one is worth doing, on a dated deadline

| Programme | Terms | Deadline | Verdict |
|---|---|---|---|
| **YC Winter 2027** | $125K/7% + $375K uncapped MFN | **2 Nov 2026, 8pm PT** · decisions by **11 Dec** | **Apply** — but only if there is revenue or a real retention curve by then. See §9. |
| **100X.VC** | **₹1.25Cr for 15%** via iSAFE | Rolling, two classes/year | **Apply, with eyes open.** ~1,900+ applicants per batch for 17–18 places, response in 7–10 working days, interview in Mumbai. The terms imply a **~₹8.3Cr (~$870K) post-money** — far below the $3.5M cap, and a cohort acceptance would effectively reprice the round. Treat as a fallback if Bands 1–2 stall, not a parallel track. |
| **Axilor Ventures** | ₹20L + 100-day programme | Rolling cohorts | Optional. Useful network, small cheque, non-dilutive to the main round's price at that size. |
| **Antler India** | Residency model | Rolling | Skip — see above. |

---

## 9. YC — Rejected for Fall 2026. What that changes, and the Winter 2027 decision.

**Status: rejected.** Applied 2026-07-27; decision returned. `YC_APPLICATION_FALL2026.md` is now a historical record plus a reusable answer bank, not a live document.

### What it does and does not mean

**It is not a signal, and it does not need managing.** Acceptance runs around 1%. Stripe, Airbnb and a long list of others were rejected before they were accepted. No Indian investor will ask "did you apply to YC," and if one asks directly, the answer is one flat sentence — *"Applied for Fall 2026, didn't get in"* — followed by moving on. Do not volunteer it, do not explain it, do not treat it as something to compensate for.

**What it does change is concrete and limited:** the application was one of three legs holding up the $5.0M cap (§7.1). That leg is gone, and the cap moved accordingly. Every piece of investor material must now be scrubbed of any language that leans on it — "applied to YC," "YC decision pending," "YC-shaped," or the ask slide's old framing of YC standard terms as a comparison point. That scrub is a checklist item in §12, not an optional cleanup.

**If partner feedback came with the rejection, it is the most valuable artifact of the whole exercise.** YC's feedback, when given, is unusually direct about the specific reason. Read it against §3's kill-list. If it names something already on that list, the list is validated and the priority order is confirmed. If it names something *not* on the list, that is new information worth more than the $125K.

### Winter 2027: apply, conditionally

**Deadline 2 November 2026, 8pm PT. Decisions by 11 December.** Batch runs Jan–Mar 2027.

Reapplying is normal and explicitly welcomed — YC funds re-applicants regularly, and the application form asks directly what has changed since last time. **That question is the entire application.** A reapplication that says "same product, more polish" is weaker than the first one; a reapplication that says "we had 60 users and no revenue in August, we have N paying customers and X% weekly retention in November" is a genuinely different company being evaluated.

**The condition, stated plainly: apply only if there is revenue or a real retention curve by 2 November.** Two months is enough for the B2B seat push (`SUBSCRIPTION_MODEL_2026-08-31.md` §4.4 — ~150 conversations to ~40 seats) but not enough for a consumer funnel to produce anything convincing. If 2 November arrives with 60-odd users, no revenue, and no retention data, skip the batch and target Spring 2027 instead — a second rejection on materially unchanged facts is a worse outcome than not applying, because it burns the "what changed" question for the following cycle.

**Cost if the condition is met:** roughly four hours, since the answer bank in `YC_APPLICATION_FALL2026.md` is already written and only the traction answers, the "what's changed" answer and the demo video need replacing.

**The logistics conflict, unchanged and now closer:** three months in San Francisco, Jan–Mar 2027, while production serves an Indian-market product. If accepted, the serving migration (§3.3) stops being optional. That item is already high in the checklist for independent reasons.

### The strategic point

**YC was always the free option, never the plan.** The plan is §8, and §8 does not depend on it. The one thing that must not happen now is a two-month pause pointed at 2 November — the reapplication gets stronger *because of* the same work that closes the round (revenue, retention, full-time commitment), so there is no sequencing conflict and no reason to wait on anything.

---

## 10. Metrics Investors Will Ask For

Rehearse these. "I don't measure that" is the wrong answer to any of them, and right now it is the answer to most.

| Question | Today | Target before outreach |
|---|---|---|
| MAU / DAU | 0 / 0 | 500 / 125 |
| DAU/MAU | n/a | ≥ 25% |
| D7 / D30 retention | unmeasured | ≥ 40% / ≥ 25% |
| Questions per active user per week | unmeasured | ≥ 3 |
| Answer 👍 rate | unmeasured | ≥ 75% |
| Retrieval Recall@5 (golden set) | measured pre-fix, **not rerun** | ≥ 0.80, published |
| MRR | ₹0 | ₹1L+ |
| Paying users / seats | 0 | 20 retail + 30 professional |
| CAC | n/a | ~₹0 organic, one paid data point |
| LLM cost per active user | measured in aggregate | < 20% of ARPU |
| Uptime | untracked | ≥ 99.5%, monitored |
| Sean Ellis "very disappointed" | n/a | ≥ 40% |

The one that matters most in your specific pitch is **Recall@5, published with before/after numbers.** You have a 150-question golden dataset and an eval harness sitting unused. Rerunning it after the retrieval fix is the single number that converts "we built good AI" from a claim into evidence — and no competitor in this market publishes anything comparable. Do it in week 3.

---

## 11. The Narrative

Twelve minutes, six beats. Depth over breadth.

1. **Hook (30s).** "91% of Indian F&O traders lost money last year — ₹1.06 lakh crore. SEBI is pushing 210 million demat accounts toward research. The research tools they'll find are spreadsheets from 2015 or WhatsApp tips."
2. **Insight (1m).** "Retail doesn't need more data. It needs data explained, with the source attached. Screener has the data and no explanation. ChatGPT has the explanation and makes the data up."
3. **Product (3m, live demo).** Ask a hard question about a mid-cap. Show the answer. **Click through to the actual filing.** Then show the "since you last viewed" digest. Nothing else — resist showing all eight surfaces.
4. **Moat (2m).** 584K filings, 1.35M vectors, OCR'd SME PDFs, full-universe XBRL with a repair layer. "This is twelve months of unglamorous data engineering. The chat interface took two weeks. Guess which one competitors can copy."
5. **Traction (2m).** Track C numbers, retention curve, professional seats, the published Recall@5, quotes from three users.
6. **Ask + why now (2m).** ₹3Cr, three hires, 18 months to 15K MAU and ₹15L MRR. Why now: the regulatory tailwind is fresh, the RA framework explicitly contemplates AI tools as of Dec 2024, and AlphaSense at $7.5B proves the category — for institutions only.

**The line to land:** *"AlphaSense is worth $7.5 billion serving 10,000 hedge fund analysts. There are 210 million Indian demat accounts and nobody has built the data layer. I've spent a year building it."*

---

## 12. The Process: Dated Plan to a Closed Round

> **Rewritten 2026-09-03.** The previous timeline was anchored to the YC deadline and the ITR window, both of which have passed. This one is anchored to two things that are still live: the **Vertex model retirement on 16 October** (a hard engineering deadline — production breaks without it) and the **YC Winter 2027 deadline on 2 November** (an optional but dated decision).

### The one rule, restated for the new phase

The old rule was *"no investor outreach before week 9."* It was checklist-gated, and the checklist ran to 36 items — six months of solo work before a single conversation. That is now too slow: Screener has entered the category and the runway is the founder's own salary.

**The replacement rule is revenue-gated and splits the two kinds of outreach, which were previously conflated:**

- **Customer outreach starts immediately.** An RA evaluating a ₹2,999/month seat is not evaluating the company — they are evaluating whether the tool saves them an hour a day. They will forgive rough edges an investor will not. There is no reason to wait, and every reason not to: these conversations *are* the traction plan (§8.0).
- **Investor outreach opens when the first seats are paid,** not when the checklist is clean. One paying customer changes the pitch more than ten fixed issues do.

### Phase 1 — Now to 16 October: unblock, migrate, sell

**Blocking and cheap — do in week one, they gate everything downstream:**
- Read the employment contract's IP-assignment / moonlighting clause. Nothing else matters if this is wrong.
- Fix the cap table — transfer the placeholder family shareholdings. Every investor hits this fact.
- Decide the full-time date and be able to name it in a sentence (§8.0).

**Hard deadline, non-negotiable — 16 October:**
- Migrate off `gemini-2.5-flash` / `-flash-lite` before Vertex retires them. Per `SUBSCRIPTION_MODEL_2026-08-31.md` §3.2 the cheapest successor is 2.5× input and 3.75× output cost, so this is a *unit-economics* change as much as an availability one, and the pricing page cannot be finalised before it lands.

**The trust minimum — the short version of the old TRUST band, cut to what an investor or a paying RA will actually notice:**
- Badge the known-bad numbers (B8 consolidated gaps, B9 suspect quarterly rows) and suppress them from AI answers.
- Render citations in every copilot answer — the single most visible proof of the core claim.
- Get serving off the Mac. A demo that dies mid-call ends the process.
- Ship the provenance memo (already written: `Anvest_Data_Provenance_Memo.pdf` — just keep it current).
- Wire PostHog. Without it there is no retention curve in November, and the retention curve is the entire YC reapplication and half the investor pitch.

**The revenue push, running in parallel from week one:**
- 150 conversations with SEBI-registered RAs, boutique PMS desks and small AMC analysts → target 20–40 paid seats. This is the beachhead argument in `SUBSCRIPTION_MODEL_2026-08-31.md` §4.4, and it is the highest-value activity on this page.
- Billing must exist for this to convert — there is currently no billing code and no plan column on `users`. Scope it small: one plan, one price, Razorpay, manual invoicing if necessary for the first ten seats.
- Sign 2–3 of those RAs as advisors on FAST terms (0.5–1%, 2-year vest, 3-month cliff) while you are already in conversation with them.

### Phase 2 — 16 October to 2 November: the decision point

- **Assess against the gate:** are there ~20 paying seats (~₹60K MRR) or a real retention curve? If yes → apply to YC W2027 (deadline 2 Nov, 8pm PT) and open investor outreach at the same time. If no → skip YC (§9), and open investor outreach anyway, but at the $3.5M cap with no expectation of a fast close.
- **Rebuild the deck from real numbers.** Slide 6 currently says "zero users" and slide 5 says nobody is in the middle of the market. Both are now false. `Anvest_PreSeed_Deck.pptx` needs the traction slide replaced with actuals and the competitive slide rewritten around the Screener comparison in `SUBSCRIPTION_MODEL_2026-08-31.md` §4.2 — which is a *stronger* slide than the one it replaces, because it is a published-price comparison rather than a claim.
- **Scrub every YC reference** from deck, one-pager, emails and tracker (§9).
- **Assemble the data room** — incorporation, cap table, founder IP assignment, statutory filings, demo video, architecture doc, provenance memo, eval results, telemetry export, unit economics, compliance roadmap. Missing IP-assignment paperwork is a startlingly common reason Indian pre-seed rounds stall at the last step.

### Phase 3 — November to January: the raise

| When | Who | What |
|---|---|---|
| Nov, week 1–2 | **Band 1** (§8) | Category B angel conversations — from the same RA list already being sold to. Category C creator angels in parallel. |
| Nov, week 2 | **Eximius Ventures** | Direct approach. Best-matched institutional fit; treat as the anchor attempt. |
| Nov, week 3–4 | **Band 2** | Better Capital, All In, Gemba, Sparrow, Titan, Whiteboard. 15–20 first meetings. AI-lane funds in parallel with the architecture pitch. |
| Nov, week 3+ | **Band 3** | Rainmatter via the integration deck; Kamaths coordinated as one thread; Groww as BD. Run in parallel — do not let the timing depend on them. |
| Dec | All | Second meetings, diligence, negotiate. YC W2027 decision lands 11 Dec if applied. |
| Dec–Jan | — | **Target: $400K committed at the $3.5M cap**, upsized toward $700K if there is demand. |
| Anytime it stalls | 100X.VC | Fallback only, and it reprices the round (§8). Do not run it in parallel with Band 1–2 conversations. |

### The honest read on timing

Nothing about this closes in six weeks. A realistic first cheque is **8–14 weeks from the first serious conversation**, and the first serious conversation should not happen until there is revenue to point at. That puts a closed round in **January–February 2027** on the plan above. If the runway does not reach that, the answer is not to pitch earlier at a worse price — it is to take the 100X.VC-shaped dilution consciously, or to stay employed longer and treat the round as a Q1 event. Both are better than a six-month round that reprices downward in public.

---

## 13. Risks That Kill This Raise

*Revised 2026-09-03. Risk 1 has changed shape; risks 4 and 8 have partly materialised.*

1. **You pitch before there is revenue.** Still the most likely failure mode, and still self-inflicted — but the gate has moved from a checklist to a number (§12). One paying seat is worth more than ten closed tickets.
2. **A wrong number surfaces in diligence.** §3.2 badging is not optional. A partner who spot-checks a symbol against Screener and finds an implausible number ends the process, correctly. Note that Screener AI now makes that spot-check trivially easy for anyone.
3. **The Mac goes down during a demo.** §3.3. Migrate before the first investor call, not before the first user.
4. **A competitor ships good-enough Indian filings chat.** **Partly materialised — Screener has shipped it** (`SUBSCRIPTION_MODEL_2026-08-31.md` §4.2). The defensible response is the one already in hand: they meter theirs at ₹10–30/answer because their cost scales with documents read; ours is ₹0.36/answer because retrieval, not the model, does the reading. That is a pricing-page headline and an investor slide. It is not a reason to panic, but it *is* a reason the round is priced at $3.5M rather than $5.0M.
5. **The 16 October model retirement is missed.** New, and the only risk on this list that breaks production outright rather than costing a meeting. It also invalidates every unit-cost number quoted to an investor until the migration lands.
6. **Data-provenance question you cannot answer.** §3.4. The memo exists; keep it current, and keep its honesty about the un-certified ratio work intact — a broker's diligence team will find that anyway, and finding it disclosed is worth more than finding it hidden.
7. **Scope sprawl reads as a lack of focus.** §3.6. Broker and HFT ambitions stay in the horizons frame (§6.1), never in the ask.
8. **Solo-founder objection goes unmanaged.** §3.5. Name hire #1 with a start date, the RA advisors with signed agreements, and the founder's own full-time date (§8.0). The failure mode isn't being solo — it's being solo *and vague about it*.
9. **The round drags and reprices in public.** New, and the reason §7.1 took the cap down pre-emptively. In a market this networked, a visible down-move costs more than the dilution it was trying to avoid.

---

## 14. If You Do Only Five Things

*Revised 2026-09-03. The old list led with the YC application and the ITR window; both are gone.*

1. **Sell 20 professional seats.** Everything else on this page gets easier the moment money moves — the valuation (§7.1), the YC reapplication (§9), the angel pipeline (§8, Band 1), and the pitch itself. ~150 conversations, per `SUBSCRIPTION_MODEL_2026-08-31.md` §4.4.
2. **Migrate off the retiring Vertex models before 16 October.** Non-negotiable; production and every cost number depend on it.
3. **Badge every known-bad number and render citations everywhere.** Differentiation is trust, and Screener AI has made your numbers trivially checkable by anyone who wants to check them.
4. **Fix the cap table and read the employment IP clause.** Cheap, boring, and each one can kill a closing round on its own.
5. **Sign 2–3 SEBI-registered RAs as advisors** at 0.5–1% on FAST terms — from the same conversations that sell the seats. Cheapest credibility available (§3.5).

Investor outreach is number six, and it stays there until number one has produced its first rupee.

---

## 15. Sources

**Funding landscape:** [Indian WealthTech funding +84% YoY Q1 2026](https://fintech.global/2026/05/22/indian-wealthtech-funding-surged-by-84-yoy-in-q1-amid-renewed-investor-interest/) · [Indian FinTech funding 2.3x QoQ in Q2 2026](https://fintech.global/2026/07/13/indian-fintech-funding-surged-2-3x-qoq-in-q2-driven-by-growth-in-deals-over-100m/) · [India fintech $2bn H1 2026, late-stage led](https://www.business-standard.com/finance/news/india-s-fintech-sector-raises-2-bn-in-h1-2026-led-by-late-stage-funding-126071601258_1.html) · [Indian AI funding tops $1bn H1 2026; seed +18%](https://startupfeed.in/indian-ai-startup-funding-h1-2026/) · [Fintech investors in India by deal count (Tracxn)](https://tracxn.com/d/explore/fintech-startups-in-india/__7DUvpjRYg2icfFp-L5Leb_WDJgbf2y7jQQQQAhbZAjw)

**Investors:** [Blume — India's micro-VC landscape 2026 (cheque sizes, tiers, validated list of ~200 funds)](https://blume.vc/commentaries/indias-micro-vc-landscape-whos-writing-the-first-cheque-in-2026) · [Rainmatter — ₹1,500Cr across 160+ startups](https://www.entrepreneurindia.com/blog/en/news/zerodhas-rainmatter-invests-inr-1500-cr-across-160-startups-nithin-kamath.59855) · [Rainmatter cheque size & approach](https://superscout.co/investor/rainmatter-by-zerodha) · [Rainmatter investor profile (Tracxn)](https://tracxn.com/d/venture-capital/rainmatter/__B1x0diOv9-lz5Gab4w5DV6RqPzlokkzk1JuAKX_v5uM) · [Rainmatter official](https://rainmatter.com/) · [Active angel investors India 2026](https://www.qapita.com/in/blog/top-angel-investors-in-india) · [Angel syndicates India](https://backrr.com/blog/active-angel-syndicates-india) · [Pre-seed investors India 2026](https://www.papermark.com/blog/pre-seed-investors-india) · [Antler India](https://www.antler.co/location/india)

**Valuation benchmarks:** [Seed valuation benchmarks India 2026 (₹15–25Cr pre-money)](https://raiseiq.in/blog/seed-valuation-benchmarks-india/) · [Pre-seed valuations 2026](https://www.zeni.ai/blog/pre-seed-valuations) · [AI seed valuations 2026](https://www.foundra.ai/key-reads/ai-seed-valuations-2026-cap-table-math)

**Comparables:** [AlphaSense $350M at $7.5B, $600M+ ARR](https://www.alpha-sense.com/press/alphasense-raises-350m-at-7-5bn-valuation-and-surpasses-600m-in-annual-recurring-revenue/) · [Rogo $75M Series C at $750M (Sacra)](https://sacra.com/c/rogo/) · [Univest $12.4M / 5 rounds / Bertelsmann India (Tracxn)](https://tracxn.com/d/companies/univest/__rblpONmvuoJz0MnOz3dyd-Ct1BMxQAt9NBIYA1ElEGo) · [Tickertape funding (Tracxn)](https://tracxn.com/d/companies/tickertape/__NCnNzMZ6ZU16HPFfS2xuGGQDlp7F-lfCaRqprJVWIfg)

**YC:** [Apply to YC — Fall 2026, deadline July 27](https://www.ycombinator.com/apply) · [How to Apply (Paul Graham)](https://www.ycombinator.com/howtoapply) · [Fall 2026 terms & timeline](https://beststartup.us/yc-fall-2026-applications-deadline/) · [YC Early Decision](https://www.ycombinator.com/early-decision) · [YC Co-Founder Matching](https://www.ycombinator.com/cofounder-matching)

**Solo founder vs. team, and advisor equity (§3.5):** [Carta Founder Ownership Report 2026](https://carta.com/data/founder-ownership-2026/) · [Solo-founder startups double but raise less](https://www.fundssociety.com/en/news/alternatives/las-startups-dirigidas-por-un-fundador-individual-se-han-mas-que-duplicado-pero-tienen-menos-exito-a-la-hora-de-conseguir-capital-riesgo/) · [Solo vs co-founder outcomes 2026](https://research.mental-momentum.ai/r/startup-outcomes-solo-founders-co-2026-u15ay3) · [FAST Agreement (Founder Institute)](https://fi.co/fast) · [Advisor equity by stage, 2026 data](https://equitymatrix.io/blog/how-much-equity-for-advisors)

**Dilution and founder ownership (§7.0):** [Carta: median founding team ~56% post-seed, ~36% post-Series-A, ~23% post-Series-B](https://carta.com/data/founder-ownership-2026/) · [Equity dilution guide for founders (CRV)](https://www.crv.com/content/equity-dilution) · [Cap table & dilution by round](https://qubit.capital/blog/venture-capital-stages) · [Pre-seed without over-diluting](https://www.spectup.com/resource-hub/pre-seed-funding-stage-of-startups)

**Regulatory & data:** [SEBI RA registration — fees, deposit, NISM-XV](https://www.lawrbit.com/capital-market/sebi-research-analyst-registration-procedure-india/) · [SEBI registered RA 2026 overview](https://univest.in/blogs/sebi-registered-research-analyst-india-2026) · [NSE Data Sharing & Usage Policy](https://www.nseindia.com/static/market-data/nse-data-policy) · [Exchange data licensing for Indian fintech startups](https://openwebsolutions.in/blog/stock-market-software-licensing-for-fintech-startups/) · [ITR deadlines AY 2026-27 — Jul 31 / Aug 31 staggered](https://cleartax.in/last-date-to-file-itr)

**Market context** (F&O losses, demat accounts, broker attrition, SEBI AI-disclosure rules, retail algo framework): see `GTM_PLAN.md` §9 — not duplicated here.

### Sources added 2026-09-03 (post-YC revision)

Investor and market facts in §8, §12 and §7.1 are drawn from:

- Eximius Ventures — fund profile, Fund II ($30M, 25–30 companies, ~$500K initial cheques, fintech named vertical): eximiusvc.com · Entrackr, "Eximius Ventures floats $30 Mn fund for pre-Seed investments" · Tracxn investor profile (34 investments, 4 in trailing 12 months).
- Rainmatter — ₹1,500Cr+ across 160+ startups; sector concentration (climate 44 / health 41 / fintech 37); 2026 investments (Lissun, Arboreal, Immuneel, VoltSeal, Farm Watt): rainmatter.com · Inc42 Rainmatter Capital investments · Entrepreneur India, "Zerodha's Rainmatter Invests INR 1,500 Cr Across 160+ Startups."
- 100X.VC — ₹1.25Cr for 15% via iSAFE, two classes/year, 17–18 per batch, ~1,900+ applicants per batch, 200 portfolio companies: 100x.vc · Tracxn investor profile.
- Fundamentum — Series B/C stage, Fund III ₹2,200Cr with ~₹100Cr initial cheques: Business Standard, "Nilekani-backed Fundamentum launches third fund of ₹2,200 crore" · TechCrunch, Jul 2026.
- India micro-VC landscape — 200–250+ funds, avg size $25–30M, sub-$40M funds lead $500–800K for 8–12%: Blume, "India's Micro VC Landscape: Who's Writing the First Cheque in 2026" (Apr 2026).
- India fintech / wealthtech funding — $2.2B+ across 100+ rounds in H1 2026 (strongest half since H1 2023); $2B across 48 deals in Q2 (2.3x QoQ); wealthtech +84% YoY in Q1 ($560.8M / 18 deals, avg $31.2M); seed-stage $478M in H1 (+18% YoY, median ticket $1M); AI $676M across 57 deals (+317% YoY): FinTech Global (Apr/May/Jul 2026) · Tracxn India FinTech Q1 2026 · Analytics Insight, H1 2026.
- Comparable rounds — Wint Wealth $27M led by Vertex Ventures SEA & India (Eight Roads, 3one4, Arkam, Rainmatter participating); Neo Group $53M led by TVS Capital at $1.1bn; StockGro Series B1 $13M (Bitkraft, Jan 2026): FinTech Global.
- Category comparables — Trendlyne $2.64M total across 5 rounds from 12 investors; Tickertape $5M seed: Crunchbase · Tracxn · PitchBook company profiles.
- YC Winter 2027 — deadline 2 Nov 2026 8pm PT, decisions by 11 Dec: ycombinator.com/apply · Round Funded, "YC Application Deadlines 2026–2027."
- Screener AI pricing, Vertex model retirement, unit costs, and the 60-user measurement: `SUBSCRIPTION_MODEL_2026-08-31.md` §§1, 3.2, 4.2, 4.4 (measured off the running system 2026-08-31).
