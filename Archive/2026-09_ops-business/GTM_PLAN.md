# Anvest — Product-Market Fit & Go-To-Market Plan

**Date:** 2026-07-26 · **status re-verified 2026-07-29** (§1 and Phase 0 updated against the running system)
**Companion docs:** `plan.md` (engineering roadmap + gap inventory — this doc does not duplicate it), `docs/architecture.md`, `financial_parsing.md`.
**Scope:** where we are → what the Indian market actually lacks → the wedge Anvest owns → phased GTM with compliance path, pricing, compute/resource mapping, KPIs, and a 90-day calendar.

---

## 1. Where Anvest Actually Is (accomplished as of 2026-07-26)

### Shipped and working
| Area | Status |
|---|---|
| **Data warehouse** | 6,128 active NSE/BSE symbols; annual + quarterly financials (XBRL-parsed, consolidated/standalone), derived QoQ/YoY metrics, shareholding, **2.67M corporate announcements**, daily OHLCV via 7pm launchd job |
| **Filings corpus (the moat)** | 1.70M bge-m3 chunks in Qdrant over 403,759 documents; OCR pipeline (migrated Apple Vision → Google Cloud Vision); incremental daily parsing. **Do not quote a bigger number**: it read 8.47M until 2026-07-29, when an audit found 6.77M of those were junk fragments from a chunker bug (`docs/retrieval_corpus_health_2026-07-29.md`). Chunk count was never the moat — document coverage is. |
| **Research Copilot** | Planner → providers → compression → synthesis with telemetry, Redis evidence cache, SSE streaming; **generate→verify→self-repair loop** across screener/alert/planning/strategy copilots; question-aware cache; LLM gateway dedup |
| **AI surfaces** | Stock page AI summary + profile, NL→DSL screener with self-correction, wealth copilot, watchlist AI, portfolio X-ray, strategy analysis, global chat; unified `.ai-surface` gradient design language |
| **Company profiles** | 4,385/4,399 active equities + 592/594 SME + all active `-RE` rights entitlements; **fund-style cards for 542/544 ETFs and 313/313 mutual funds** (AUM, TER, index tracked, AMC, manager). Missing CEO/founding-year facts topped up from our own filings corpus, each with the verbatim evidence phrase and source `doc_id`s |
| **Scoring & technicals** | Calibrated sector-aware Anvest Score (no neutral-default inflation), Wilder RSI/ATR, D/E fallback fixes |
| **Data-quality wars won** | Market-cap cache corruption fixed + backfilled (was wrong for ~78% of NSE equities); 15,899 cash-flow rows recovered; quarter-sum repair; cache warmer rebuilt on XBRL annual rows; instrument-search ranking with delisted-successor handling |
| **ITR module (new)** | Tax-return compilation workspace (ITR-1/2), AIS/26AS parsing, persistence + test suite — a wedge no research competitor has |
| **Production** | anvest.in — Vercel frontend; query-api :18000 + broker-portfolio :18001 + Qdrant + Redis on the Mac behind cloudflared; daily ingestion + reparser + OCR as supervised launchd jobs |

### Known open gaps (see `plan.md` §2 for full inventory)

*Re-verified against the live system on 2026-07-29 — several items below had already closed.*

**Closed since this doc was written:** B8 serving-layer honesty (gap periods are omitted, not
faked — `query-api/tests/test_financials_consolidated_gap_omission.py`) · B9 row flagging
(`quality_flag: pat_pbt_tax_discrepancy` served by query-api, badged in `CompanyFinancialsV2`) ·
citations rendered in `ChatWidget` · D2 engagement telemetry (self-hosted
`product_analytics_service` + `useAnalytics`, with the AI-surface event set, rather than PostHog) ·
D3 anonymous copilot (guest path, `is_guest` in the query log) · B7 sentiment provider ·
programmatic SEO (sitemaps, JSON-LD, ISR) · **B4, and with it a chunker bug that had made 97% of
the reparsed corpus junk — see `docs/retrieval_corpus_health_2026-07-29.md`**.

**Still open:**
- **Data trust:** B8 *source* gap (consolidated genuinely missing for ~4,517 symbol-FY periods —
  the serving layer is now honest about it, but the data is still absent) and B9's parser-level
  fix (`financial_parsing.md` §6). Flagging contains them; it does not fix them.
- **Not wired in:** trader quant library (C6).
- **Infra:** single-Mac production with OOM history (D1) — Qdrant died mid-audit under normal
  batch load on 2026-07-29, which is exactly the launch risk §7.5 names; Vertex 429s (D4).
- **Golden-dataset eval (B5):** rerun 2026-07-29 post-cleanup — see §6a below. Note the suite is
  **30 questions, not 150**; expanding it is a prerequisite for treating the number as a gate.

**Honest assessment:** the platform is a strong *product*, but it is pre-PMF: zero external users, no telemetry on what people actually use, unproven willingness to pay, and a data-quality tail that hasn't been stress-tested by strangers.

---

## 2. The Indian Market: Size, Shift, Tailwind

- **~210M demat accounts** (Oct 2025), ~3M new accounts/month at peaks — the funnel keeps growing.
- **The F&O crackdown is the macro tailwind.** SEBI's FY25 study: **91% of individual F&O traders lost money, ₹1.06 lakh crore net losses (+41% YoY)**. Top-4 brokers (Groww, Zerodha, Angel One, Upstox) lost ~2M active investors in H1 2025 as margin rules, fewer expiries, and taxes bit. Regulators are actively herding retail from speculation → investing/research. A **trustworthy research product is positioned exactly where the puck is going.**
- **Retail pays for research when it's credible:** Univest hit ₹7Cr/month revenue with 3L+ subscribers; Screener.in charges ₹4,999/yr; Trendlyne ₹2,190–5,900/yr; Tickertape Pro ₹2,399/yr; smallcase fees ₹299–999/yr per basket. The subscription market exists and is under-served on the AI axis.
- **Regulatory clarity arrived (this de-risks us):** RA Regulations amendments (effective Dec 2024) explicitly contemplate AI tools — with disclosure duties and full accountability on the registered entity. The retail algo framework (Circular SEBI/HO/MIRSD/MIRSD-PoD/P/CIR/2025/0000013, live since Oct 1, 2025) defines exactly how Phase-4 execution must work (broker = principal, exchange algo-IDs, provider empanelment). The rules are now known, not speculative.

---

## 3. Competitive Landscape & The Gap

### Feature matrix (2026)

| Capability | Screener.in | Trendlyne | Tickertape | StockEdge | Univest / advisory apps | Broker apps (Zerodha/Groww/Angel) | Perplexity Finance / ChatGPT | **Anvest** |
|---|---|---|---|---|---|---|---|---|
| Deep fundamentals tables | ✅ best-in-class | ✅ | ✅ | ✅ | ❌ | partial | ❌ shallow | ✅ (once B8/B9 close) |
| Screeners | ✅ formula | ✅ 1,400+ params, realtime | ✅ | ✅ | ❌ | partial | ❌ | ✅ **NL→DSL with self-repair** |
| Proprietary score | ❌ | ✅ DVM | ✅ MMI | ✅ | ✅ opaque | ❌ | ❌ | ✅ **explainable, sector-calibrated** |
| Conversational AI over *filings corpus* | ❌ | ❌ (scores only) | ❌ | ❌ | ❌ | ❌ | ⚠️ generic web, no Indian XBRL warehouse | ✅ **grounded, cited, verified numbers** |
| Announcements parsed & searchable (2yr, OCR'd) | ❌ | partial (feeds) | ❌ | partial | ❌ | ❌ | ❌ | ✅ **1.35M chunks — unique dataset** |
| Portfolio-aware AI (X-ray, "since you last looked") | ❌ | partial alerts | partial | ❌ | ✅ push tips | ❌ | ⚠️ watchlists | ✅ |
| Strategy/backtest lab | ❌ | partial | ❌ | ❌ | ❌ | Streak (paid, separate) | ❌ | 🔜 Phase 3 |
| Tax (ITR) integration | ❌ | ❌ | ❌ | ❌ | ❌ | P&L reports only | ❌ | ✅ **only player** |
| Trust artifacts (citations, "grounded or silent") | n/a | ❌ | ❌ | ❌ | ❌ black-box tips | n/a | ⚠️ web citations | ✅ **core invariant** |

### The gap Anvest fills

Every incumbent sits in exactly one of three camps:

1. **Tables without conversation** (Screener, Trendlyne, Tickertape, StockEdge): dense data, zero interpretation. The user must already know what ROCE means and what to ask. Serves the top ~5% of investors.
2. **Tips without transparency** (Univest, MarketsMojo, advisory apps): "Buy X, target Y" — black-box, trust erodes with the first bad call, regulatorily heavy.
3. **Conversation without a warehouse** (Perplexity Finance, ChatGPT): fluent answers, but no point-in-time Indian XBRL warehouse, no OCR'd SME filings, hallucinated or stale numbers, no accountability. Perplexity's India expansion (earnings transcripts, watchlists) proves demand for the interaction model while lacking the data layer.

**The unoccupied position: a grounded AI equity research analyst for Indian retail — conversational like Perplexity, numerically trustworthy like Screener, explainable unlike Univest.** The moat is the pipeline nobody else has bothered to build: full-universe XBRL parsing with quality repair, 2 years of OCR'd announcement PDFs vectorized, and an architecture where **LLMs never do arithmetic and cite everything or stay silent**. Copying this is 12+ months of unglamorous data engineering, not a prompt.

**Positioning statement:** *"Ask anything about any Indian stock. Get an answer with the filing it came from."* — Bloomberg-grade grounding, WhatsApp-simple interface.

### Target segments (in order)
1. **The DIY fundamental investor** (Screener/Trendlyne user, 25–45, ₹5L–1Cr portfolio): already pays ₹2–5K/yr, frustrated by table-only UX. Beachhead — they evangelize on X/Reddit.
2. **The F&O refugee**: burnt trader converting to investing; needs guidance, distrusts tip-sellers; the Anvest Score + explainers + copilot is their on-ramp.
3. **The professional (B2B, later):** RAs/RIAs/PMS analysts who'd pay 10× for research productivity (bulk Q&A over filings, event monitors). Also the SEO/API play.

---

## 4. GTM Phases

### Phase 0 — Make it trustworthy & measurable (Weeks 1–3) — *prerequisite to showing anyone*
The product's single promise is trust. One wrong PAT number screenshotted on X ends the launch.

*Status 2026-07-29: items 1–7 are done. What replaced them is item 8, which nobody had scoped.*

1. ✅ `plan.md` §10 leftovers — all deployed; launchd installed; all containers on `unless-stopped`.
2. ✅ **B8 serving-layer honesty** — gap periods are omitted rather than substituted, with regression tests; the UI badges any standalone row served under a consolidated request.
3. ✅ **B9 containment** — `quality_flag` computed at serve time, badged in the financials table.
4. ✅ **Citations rendered in every copilot answer** — including sources with no `url`, which fall back to the stock page.
5. ✅ **Telemetry (D2)** — built in-house (`product_analytics_service` + `useAnalytics`) instead of PostHog: same event funnel, no third-party data egress, and it joins directly to `ResearchCopilotLog`.
6. ✅ **Golden-dataset eval rerun** — §6a. Caveat: 30 questions, and its Precision/Recall measure *entity resolution*, not document Recall@5. Treat the ≥0.8 gate as unmet until the suite is expanded and a retrieval-level metric exists.
7. ✅ **Anonymous sample questions (D3)** — guest path live.
8. ✅ **The one that mattered most, and was invisible:** 97.2% of the reparsed filings corpus was junk fragments from a chunker runaway. Every copilot answer had been retrieving against a corpus where ~97 of every 100 candidate passages were meaningless. Fixed, 6.77M points deleted, standing audit added. `docs/retrieval_corpus_health_2026-07-29.md`.

**Exit:** zero known-wrong numbers served unbadged ✅ · citations visible ✅ · telemetry flowing ✅ · Recall@5 ≥ 0.8 — **not yet provable**; needs the expanded suite and a retrieval-level metric.

#### §6a — Phase-0 eval result (2026-07-29)

Full write-up: `docs/copilot_eval_2026-07-29.md`. Headline: Precision **0.90** / Recall **0.90**,
grounding **0.969**, citation **0.955**, cost **$0.0030/question**, 21 of 24 retrieval-scored
questions perfect.

**Do not report this as clearing the gate.** The harness scores *entity resolution*, not
document retrieval — there is no Recall@5 in it — and the suite is 30 questions, not the 150
`plan.md` assumed. Hallucination rate (0.015 → 0.0345) and completeness (0.89 → 0.79) both
regressed on judge scores, though one answer moves either several points at this sample size.
Phase-0's retrieval gate stands at **unmet — unmeasured** until the suite is expanded and a
document-level metric exists.

### Phase 1 — Closed alpha (Weeks 3–10): 25–50 real users
- **Recruit:** 10 personal-network investors + 15–25 from r/IndiaInvestments, X fintwit DMs, Screener.in power users. Ask nothing but usage + a weekly 15-min call with 5 of them.
- **Instrument the "aha":** hypothesis — first grounded answer with a citation on a stock they own. Measure time-to-first-question, questions/user/week, 👍 rate, D7 return.
- **Ship the retention feature:** proactive **"Since you last viewed X"** digest (evidence builder + cache reuse; `plan.md` §3 1.2) — converts ask-driven to insight-driven. This is the highest-leverage build of the alpha.
- **Portfolio import (read-only) via broker OAuth** (Kite Connect first): makes the digest and X-ray personal. Read-only scope = no execution compliance burden yet.
- Weekly triage of worst-rated answers feeds the eval set (flywheel).
- **Alpha exit criteria:** ≥40% of cohort active in a market week · ≥3 questions/user/week · 👍 ≥ 75% · ≥5 users say they'd pay (Sean Ellis "very disappointed" ≥ 40%).

### Phase 2 — Public beta + monetization test (Months 3–5)
- **Serving off the Mac first** (D1): query-api + broker-portfolio + Postgres replica → e2-standard-4 (~$100/mo) or Hetzner (~€40/mo). Mac becomes batch node. A public launch on a laptop behind a tunnel is an outage story waiting to happen.
- **Vertex quota raise filed now** (free, takes days); evidence cache + flash-tier keeps unit cost ≈ ₹2–6/user/day at beta scale.
- **Delayed live quotes** (Phase-2 step 1 of `plan.md`): 1–5 min polling for top ~500 symbols → Redis. "Delayed" label. Enough for research use-cases; no vendor feed cost.
- **Pricing (launch):**
  - **Free:** all pages, delayed data, 5 copilot questions/day, 2 watchlists, score visible.
  - **Pro — ₹249/mo or ₹1,999/yr:** unlimited copilot, proactive digest, portfolio X-ray, unlimited screeners + alerts, exports. Deliberately undercuts Trendlyne StratQ (₹5,900) and Screener (₹4,999) while offering a category they don't have.
  - Annual-only discount + 14-day trial; UPI autopay (Razorpay).
- **Distribution (zero-ad-budget):**
  1. **Programmatic SEO — the sleeping giant:** 6,137 stock pages with unique AI summaries, pros/cons, score explanations = long-tail queries ("is X a good stock", "X share analysis") that Screener's bare tables can't answer. Add ISR/SSG on market-ui, structured data, sitemap. Highest ROI channel by far.
  2. **Fintwit/X + Reddit:** daily "what the filings actually said" posts auto-drafted from the announcements corpus (human-reviewed) — content nobody else can generate.
  3. **YouTube/finfluencer partnerships** (revenue share on Pro referrals) — 2–3 mid-tier (50–300K subs) fundamentals-focused creators.
  4. **ITR season hook (Jun–Sep):** "file your capital-gains ITR free" → import portfolio → convert to research user. Counter-seasonal acquisition no competitor has.
- **Beta exit criteria:** 2,000 MAU · free→pay ≥ 3% · CAC ≈ ₹0 organic · answer cost < 20% of ARPU · uptime ≥ 99.5%.

### Phase 3 — Compliance + strategy lab (Months 5–9)
- **RA registration decision point.** Until registered, product stays strictly informational: no buy/sell/hold, no target prices, score framed as data summary, disclaimers everywhere. SEBI has ruled "educational" disclaimers do NOT exempt actionable signals. When conviction + revenue justify: **corporate RA ₹5.5L + GST** (individual ₹15K if going solo first), revised NISM-XV (post-Jan-2026 syllabus), RAASB FD-lien deposit, and the Dec-2024 **AI-use disclosure obligations** (disclose AI extent to clients; firm is 100% accountable for AI output — our "grounded or silent" gate is literally the compliance architecture).
- **Strategy lab / paper trading** (`plan.md` §5): point-in-time correctness, trader-library merge (C6), NL→strategy DSL, walk-forward with Indian costs (STT, stamp, slippage). Paper trading is also the retention feature for the F&O-refugee segment.
- **B2B pilot:** 3–5 RAs/boutique PMS on a research-seat plan (₹2–5K/seat/mo) — validates the professional tier and funds the RA registration.

### Phase 4 — Execution layer (Months 9–15, gated on Phase-3 traction)
Per the SEBI retail-algo framework (live Oct 2025): broker is principal, Anvest empanels with exchanges as algo provider, exchange-issued algo-IDs on every API order, OPS < 10/s stays in the standard-API lane, mandatory kill-switch + pre-trade risk checks + immutable audit logs. Architecture already envisioned in `plan.md` §6 (paper → shadow → live ladder, per-user caps, drawdown kill-switches). Monetize as autopilot subscription (₹599–999/mo tier). **Only enter with ≥6 months of paper/shadow data and ≥5K paying research subscribers** — execution without a trust base is the Univest model, not ours.

---

## 5. Resource → Task Mapping (most-efficient compute for each part)

| Workload | Where | Why / cost |
|---|---|---|
| Interactive copilot synthesis, screener NL→DSL | **Vertex gemini-2.5-flash/-lite** | Latency + no GPU ops burden; evidence cache bounds cost. File quota raise now (D4). |
| Serving APIs, Postgres, Redis, Qdrant (beta onward) | **Small GCP VM (e2-standard-4) or Hetzner** | ~$40–100/mo; retires single-Mac risk (D1) before public traffic. |
| Daily ingestion (7pm), incremental reparse, cache warmers, dev | **M5 Pro Mac (24GB)** | Already built + supervised via launchd; near-zero cost; keep OOM sources (IDE) closed in market hours. |
| bge-m3 query embedding | **Mac sidecar :6390** (move a replica to serving VM at beta) | 1024-d contract; must never switch to Vertex embeddings (different vector space). |
| **Announcement backfill remainder (~430K docs) + bulk re-embedding** | **Spot L4 VM (g2-standard-8, ~$0.7–0.9/hr)** | Mac does ~0.1 docs/s ≈ 45+ days; L4 burst finishes the ≥1-yr window in ~1–2 days for **$25–50 total**. Checkpointed script already resumable — spot-safe. |
| Bulk LLM extraction (profile facts from corpus B1, exceptional-items extraction for B9, sentiment scoring backfill) | **Spot L4 + vLLM (Qwen2.5-14B/32B-AWQ class)** | Vertex 429s cap batch jobs; self-hosted batch is 5–10× cheaper per token at this volume and quota-free. Keep Vertex for interactive only. |
| Factor-zoo / gradient-boosting research (Phase 3) | **Mac first** (CPU/MPS fine for GBM on ~6K symbols) → **L4** when sweeps grow | Don't rent GPUs for XGBoost-scale work. |
| DRL execution/sizing experiments (Phase 3–4) | **Spot A100 bursts ($1.2–1.8/hr spot)** | Episodic training only; gate: must beat deterministic baseline out-of-sample after costs before more spend. |
| Fine-tuning a small extraction/Q&A model on our filings corpus (optional, Phase 3) | **A100 (LoRA, 1–2 days)** | Only if flash-tier evals show quality gaps; distill from logged copilot traffic. |
| OCR | **Google Cloud Vision** (already migrated) | Per-page pricing beats maintaining Apple-Vision worker fragility; keep the queue/worker pattern. |
| Frontend | **Vercel** (free tier → Pro $20/mo at beta) | Already the deploy path; add ISR for programmatic SEO pages. |

**Standing rule (unchanged from `plan.md`):** Mac-local first → spot GPU for batch → managed cloud only where a user-facing SLA demands it. Never an always-on GPU.

**Steady-state cost projection:** alpha ≈ $30–80/mo (Vertex + one-off L4 backfill) · public beta ≈ $150–250/mo (VM + Vertex + Vercel Pro) · Phase 3 ≈ +$50–150/mo research bursts. Break-even at roughly **100–150 Pro subscribers**.

---

## 6. KPIs (the only numbers that matter per phase)

| Phase | North star | Guardrails |
|---|---|---|
| 0 | Recall@5 ≥ 0.8 on golden set | 0 unbadged known-bad numbers; citation render rate 100% |
| 1 (alpha) | ≥3 copilot questions/user/week | 👍 ≥75%; D7 ≥40%; Sean-Ellis ≥40% |
| 2 (beta) | Free→paid ≥3% | MAU 2K+; LLM cost <20% ARPU; uptime 99.5%; SEO impressions trend |
| 3 | 100+ Pro subs (break-even) & paper-trading WAU | B2B pilot ≥3 paying seats; zero compliance incidents |
| 4 | Autopilot conversions | Implementation shortfall within model; kill-switch drills pass |

---

## 7. Top Risks & Mitigations

1. **A wrong number goes viral.** *Mitigation:* Phase 0 badging (B8/B9), ingestion-time validation, "grounded or silent," a visible data-corrections changelog (turns bugs into trust theater).
2. **Perplexity/broker apps ship "good-enough" AI chat.** *Mitigation:* our defensibility is the warehouse + filings corpus + verification loop, not the chat UI. Ship the proactive digest + portfolio-awareness fast — interaction depth they can't copy without the data layer. Speed matters: 6–9 month window.
3. **Regulatory drift into "advice."** *Mitigation:* hard product rules (no buy/sell/target-price outputs) until RA registration; legal review of all AI-surface copy before public beta; track SEBI AI-governance consultation.
4. **Single-founder bandwidth.** *Mitigation:* this plan intentionally sequences ONE growth motion per phase (alpha cohort → SEO → creators); everything else is cut. Agent-assisted eng for data-quality batch work.
5. **Mac-prod fragility during launch.** *Mitigation:* serving migration is a hard gate before any public link is posted.
6. **Vertex quota ceiling at beta.** *Mitigation:* quota raise filed in Phase 0; vLLM-on-L4 fallback path proven during batch jobs.

---

## 8. 90-Day Calendar

| Week | Deliverables |
|---|---|
| 1 | Deploy all pending fixes (copilot, market-ui, query-api); launchd install; redis restart policy; PostHog wired |
| 2 | B8 substitution badges; B9 row flagging + AI suppression; citations rendered; anonymous sample questions |
| 3 | L4 spot VM: finish 1-yr announcement backfill (~$50); rerun golden eval, publish numbers; stale-Qdrant cleanup (B4) |
| 4 | Proactive "since you last viewed" digest v1; alpha cohort recruiting (25 users); weekly-call cadence starts |
| 5–6 | Kite read-only portfolio import; digest v2 (portfolio-aware); B1 profile-facts corpus extraction on L4 |
| 7–8 | Alpha iteration from telemetry; sentiment provider into copilot (B7); hygiene C1–C3 (commit/venv/tests) |
| 9 | Serving migration to VM; Vertex quota raise confirmed; delayed-quotes poller for top 500 symbols |
| 10 | Programmatic SEO: ISR stock pages + structured data + sitemap; payments integration (Razorpay) |
| 11 | Pricing page + Pro gating; 14-day trial flow; content engine v1 (filings-digest posts, human-reviewed) |
| 12 | **Public beta launch** (Reddit/X/creators); alpha exit report vs criteria; RA-registration go/no-go memo |

---

## 9. Sources

- [Trendlyne vs StockEdge vs Tickertape vs Screener.in](https://help.trendlyne.com/support/solutions/articles/84000396310-trendlyne-vs-stockedge-vs-tickertape-vs-screener-in) · [Trendlyne review/pricing](https://www.stockmaniacs.net/trendlyne-review/) · [Fundamental analysis tools India 2026](https://www.winvesta.in/blog/investors/fundamental-analysis-tools-and-screeners-2026-guide) · [StockEdge vs Tickertape vs Trendlyne](https://slashdot.org/software/comparison/StockEdge-vs-Tickertape-vs-Trendlyne/)
- [Univest scale & model (YourStory)](https://yourstory.com/2025/04/how-univest-is-rewriting-the-rules-of-retail-investors-india) · [Smallcase pricing & model](https://joinfingrad.com/blog/should-you-invest-in-smallcase/) · [AI stock advisory India (Univest)](https://univest.in/blogs/ai-stock-market-advisory) · [Top AI tools for Indian markets](https://www.pocketful.in/blog/trading/best-ai-tools-for-stock-market-analysis/)
- [Demat accounts 210M (Business Standard)](https://www.business-standard.com/markets/news/sebi-mulls-overhaul-of-investment-advisor-and-research-analyst-rules-124080601527_1.html) · [Brokers lose 2M active investors H1 2025](https://www.business-standard.com/markets/news/groww-zerodha-see-big-drop-as-2-million-active-investors-exit-top-brokers-125071000537_1.html) · [F&O losses ₹1.06 lakh crore FY25](https://www.whalesbook.com/news/English/economy/Sebis-FandO-Crackdown-Fails-Retail-Investor-Frenzy-and-Massive-Losses-Continue-in-Indias-Derivatives-Market/6942855ec477b37db06b5847) · [SEBI F&O safeguards](https://www.motilaloswal.com/learning-centre/2025/8/derivatives-market-decline-what-sebi-wants-retail-investors-to-know)
- [SEBI RA guidelines incl. AI disclosure (Jan 2025)](https://mehta-mehtaadvisory.com/sebi-update-guidelines-for-research-analysts/) · [SEBI: regulated entities responsible for AI output](https://www.lexology.com/library/detail.aspx?g=f2e36044-cc40-4c8f-8e74-79141d32031e) · [RA registration costs & 2025 deposit changes](https://lawyervikasgupta.com/blog/step-by-step-guide-for-sebi-research-analyst-registration/) · [Revised NISM-XV (Jan 2026)](https://www.nismexams.in/blog/sebis-2025-amendment-decoding-the-new-rules-for-research-analysts-and-their-certification-requirements/1074)
- [SEBI retail algo circular Feb 2025](https://www.cse-india.com/upload/upload/Feb_042025.pdf) · [Algo framework deadline Oct 1, 2025](https://algobulls.com/blog/industry-insights-and-updates/sebi-new-algotrading-regulations-for-retail-investors-2026) · [uTrade explainer](https://www.utradealgos.com/blog/decoding-sebis-new-algo-trading-rules-for-retail-investors-all-you-need-to-know)
- [Perplexity Finance India expansion](https://sidsaladi.substack.com/p/perplexity-finance-101-the-complete) · [Groww 14M active clients / IPO](https://www.business-standard.com/markets/ipo/groww-founders-eye-1-9-billion-wealth-boost-as-online-broker-heads-for-ipo-125103100318_1.html)
