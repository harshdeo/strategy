# Anvest — Who to Target First, and How to Sequence the Round

**INTERNAL — not for sharing.** Revised 14 Oct 2026 to restore product breadth while keeping the financing plan focused; round, numbers and Q&A updated 19 Oct 2026 for the 20 October 2026 materials. Companion to `FUNDING_PLAN.md` (current round), `GTM_PLAN.md` (customer execution) and `../README.md` (file map).

This version ranks investors on **observable criteria** — stage fit, cheque size, relevant investments, introduction access and conflicts — not on probabilities. Any probability I could give would be a guess; the order below is a reasoned priority, not a forecast.

## 1. The financing arithmetic comes first

The headline ask is **$500K**, with a first close at $400K and room to $700K. At ₹95/USD, **$400K ≈ ₹3.8 Cr**, **$500K ≈ ₹4.75 Cr** and **$700K ≈ ₹6.65 Cr**.

- 4–6 angels at ₹10–25L each raise ₹40L–₹1.5 Cr. That is **well short of the first close**.
- To close $400K the realistic routes are: (a) one institutional lead of roughly $250–500K plus angels filling the rest; (b) a smaller first close from angels (for example ₹1–1.5 Cr) with a stated plan to add a lead; or (c) larger angel cheques (₹25–50L) from a handful of strong-conviction angels.
- Decide which route you are running before Wave 1, because it determines how many conversations you need and whom you ask first.
- Keep the cap table short. Pool cheques under about ₹10L through one syndicate or SPV rather than taking them directly; a long list of small holders slows every later round.

## 2. Targets, ranked by observable criteria

| Priority | Target | Typical cheque | Why it ranks here (observable) | Main constraint |
|---|---|---|---|---|
| 1 | Category B angels: SEBI-registered RAs, PMS and advisory founders, ex-brokerage product heads | ₹10–50L each | They are the target customer, can judge the product directly, and the pilot and cheque conversations are the same relationship | Cheques are small; need several, or a lead alongside |
| 2 | **Eximius Ventures** | Up to ~$500K (published) | Fintech is a named vertical; its published positioning includes pre-product and early-traction investments; Fund II is deploying | Institutional diligence will test commitment (full-time) and early evidence |
| 3 | **Better Capital** | Pre-seed cheques | Very high volume pre-seed fund backing technical first-time founders; short process | Evidence of customer pull will matter |
| 4 | Category C angels: fundamentals-focused creators | ₹5–25L (pooled, see §1) | Distribution and capital together | SEBI's finfluencer rules bar registered entities from associating with unregistered creators who give advice or claim returns. Anvest will be bound once RA-registered, so any referral or rev-share terms need counsel sign-off now, or they will have to be unwound later |
| 5 | India micro-VCs under ~$40M: All In, Gemba, Whiteboard, Inuka, Zeropearl, OTP, Sparrow | $250–800K | Stage and cheque match; the $3.5M cap is below typical entry prices | Many are generalist; fintech nuance varies |
| 6 | Titan Capital; WaterBridge, India Quotient, Huddle | $250–600K | Pre-seed and seed funds with fintech in the book | Slower; second wave |
| 7 | AI-lane funds: Z21, Neon, Bold, Grayscale.vc, FortyTwo, Sense AI | $150–500K | Can evaluate the grounded-retrieval architecture | Less Indian retail-fintech context; lead with measured results |
| 8 | **Rainmatter / Zerodha-adjacent** | Varies | Fintech is within its stated scope; no board seats | Zerodha owns Tickertape, so overlap must be addressed in meeting one; keep the pilot conversation separate |
| 9 | Larger funds (Accel, Lightspeed, Peak XV, Elevation, Z47, Prime, Blume, Arkam, 3one4) | n/a now | Active in fintech | Stage mismatch today; relationship-building only |

**Not a target for the equity round:** Groww (partnership conversation only, Template C), Fundamentum (Series B/C), Antler (residency model).

## 3. Sequencing, aligned to evidence

| Timing | Priority | Evidence to produce |
|---|---|---|
| Week 1 (from 14 Oct) | Correct claims, verify the user number, fix operational gaps (see below), reconcile the revenue bridge | Consistent materials with dated evidence |
| Days 8–30 | Interview and sell to one professional segment; start Wave 1 conversations in parallel (angels who are also customers) | Paid pilots and documented objections |
| Days 31–60 | Improve the workflow customers actually repeat | Retention, renewals, quality and cost-per-task measurements |
| Days 61–90 | Expand the channel that shows results; advance selected investors | Repeatable sales evidence and a credible financing plan |

**Wave 1 (weeks 1–3):** Category B angels (build a list of ~40 from the SEBI RA register and LinkedIn; open with a demo and a pilot, not a pitch). Pilot outreach has not started yet (19 Oct 2026); do not tell investors it is underway. For Eximius and Better Capital, send a relationship note in the style of Template D now, with no deck.
**Wave 2 (from the first paid pilot):** the full pitch to Eximius, Better Capital and the micro-VCs, then Category C creators, AI-lane funds and the Rainmatter conversation. These are the likeliest leads, and a "no" given at zero revenue is hard to reverse; one paid pilot changes the meeting. If no pilot has closed by mid-November, open Wave 2 anyway with the measured activation and repeat-use numbers.
**Throughout:** Template D to large funds (no deck, no ask); the broker pilot (Template C) runs separately.

## 4. Before broad outreach, close these gaps

1. **Verify the user number:** registered vs activated vs monthly active, as-of date, internal and test accounts excluded.
2. **Operational facts:** verify the production broker authentication path and remove the unofficial session-token fallback (the partner deck says "no unofficial access", so this must be true before it goes to any broker); confirm whether Kite Connect keys are configured in production; separate historical symbol coverage from current ingestion freshness (BSE ingestion is blocked under a renewed exception to 1 Dec 2026); document token handling and permissions.
3. **Data-use rights:** confirm NSE/BSE licence terms for the actual commercial use before any partner pilot. The provenance memo says data-quality corrections "are published as they are found"; make sure a public corrections log exists, or reword that line, before the memo goes out.
4. **Counsel:** confirm the financing instrument (the current materials say "convertible instrument (CCD/CCPS)") and the product's regulatory position before registration.
5. **Full-time commitment:** decided — full-time on Anvest from the close of this round. Have the employment notice period and the date ready.
6. **Company hygiene (if not already done):** transfer the placeholder family shareholdings, sign the founder IP assignment to Anvest Fintech Private Limited, and read the New Relic employment contract's IP and outside-work clauses. Any one of these can stall a close at the last step.
7. **Unit costs after 16 Oct:** the Vertex model migration raises inference cost. Re-measure cost per answer and Desk-seat margin before quoting ₹0.36 or any margin figure. The decks no longer quote a margin.
8. **Demo resilience:** a recorded 3-minute demo, and serving that survives the laptop being offline, before the first investor call.
9. **Product matches the deck:** the deck covers AI across research, screening, backtesting, paper trading, wealth tools and calculators. Check demo routes, coverage disclosures and current product wording. The Anvest Score and tax compiler are outside the main pitch; their actual behaviour still needs to match the stated product scope.

## 5. Why this round is plausible, and its limits

- The round is small, so a lead plus angels can fill it.
- The cap is below typical micro-VC entry prices, and terms are identical for every investor.
- Category activity is high (Indian fintech funding in H1 2026, AI as a funding theme, StockGro's Dec 2025 round and Sep 2026 IPO filing).
- The honest limit: the product is early, pre-revenue and has about 100 registered users. Expect investors to weight paid pilots and retention heavily, and expect the round to take weeks.

---

# Internal diligence Q&A: truthful answers, framed well

**These answers reflect the documented position and dated observations. Confirm current facts before using them. Do not shorten them into something misleading. If a number is asked for, give the verified one.**

**Q: How many users do you have?**
About 100 registered users, all organic, no paid marketing. *(Confirm against the database before each call: registered vs activated vs monthly active, as-of date, test accounts excluded.)* Give activation and week-4 return if you have them. It is a starting point, not product-market fit.

**Q: Revenue?**
Pre-revenue. Launch pricing is set (Free / Plus ₹199 / Pro ₹599 a month / Desk ₹2,999 per seat, 1–5+ seats). Paid professional pilots are the first thing I'm selling; checkout goes live in the first 90 days after close.

**Q: How big is the first segment?**
SEBI's intermediary directory (checked 19 Oct 2026) lists 2,304 research analysts, 1,057 investment advisers and 539 portfolio managers: about 3,900 regulated firms, with about 3.5 lakh mutual fund distribution professionals (ARN and EUIN holders, Jun 2026) beyond them. The $500K plan's 77 paying teams at month 15 is about 2% of those firms. Market sizing at list prices: TAM about $1.3B a year, SAM about $250M a year, of which professionals are about ₹78 Cr (3 seats per firm) and active investors about ₹2,292 Cr (see `../Financial_Models/operating_model.py`). Professionals are the entry; active investors and partner distribution are the scale.

**Q: What are the month-15 targets?**
From the monthly operating model (`../Financial_Models/operating_model.py`). $500K target: ₹87 L ARR run-rate (₹7.3 lakh net MRR), 77 Desk teams (~243 seats), 2 paying partner integrations and ~186 retail subscribers; break-even about month 42 without new funding. $400K first close: ₹68 L ARR and 55 teams, with cash to about month 31. $700K (second seller from month 6): ₹1.06 Cr ARR, 88 teams and 3 partners. Also SEBI RA registration and a published head-to-head benchmark. The drivers are planning assumptions: seller productivity (4 teams a month once ramped, the founder 1), 3 seats per team, churn, conversion and partner usage priced ₹15 → ₹10 → ₹6 per user. They will be replaced by measured pilot data. The long-term scenario reaches about ₹23 Cr ARR in year 5. It is conditional on a Series A, approvals and partner contracts; Desk plus retail account for ₹13.4 Cr of it.

**Q: Where does production run?**
On infrastructure I operate today, in containers with a public tunnel, with nightly pipelines and backups. Part of this round is moving to scaled managed hosting. Don't call it "production-grade".

**Q: How fresh is the data?**
Daily: evening batch plus a morning catch-up, current to the previous trading day. BSE ingestion is subject to an exception that is renewed to 1 Dec 2026. Live filing alerts are next; live prices would come through each user's own broker and, for public pages, a licensed delayed feed.

**Q: Can users trade through Anvest?**
Not yet. A read-only broker link pattern is built. Execution is not part of this round.

**Q: Is the data accurate?**
Raw figures are cited to the filing. Derived ratios are in a verification program; a corrected formula version has passed internal gates and is moving through certification to production. Gaps (~4,500 company-years the exchange never filed) are flagged in the product, not estimated.

**Q: How accurate are the AI answers?**
Spot-check on 19 Oct 2026: September-quarter answers for TCS, HCL Technologies and Wipro matched their NSE XBRL filings exactly, and Infosys was correctly declined because it had not yet reported. That is a four-question spot-check, not a benchmark: say so. The published head-to-head benchmark is a month-15 milestone. Never claim "100% accuracy" or "100% traceability".

**Q: Solo founder, still employed?**
Full-time on Anvest from the close of this round; give the notice period and date. Until then, say plainly that you are employed. The first hires add a growth lead, a data engineer and a full-stack/quant engineer; the adviser bench is being built, with no names to give yet.

**Q: Who owns the IP? Does your employer have a claim?**
Anvest Fintech Private Limited owns it under a signed founder IP assignment, and the employment contract has been checked. *(Both must be true before you say this; see §4.6.)*

**Q: What's your minimum close?**
First close at $400K: it funds the three hires, RA registration and launch, with cash to about month 31 on the model. Lead with $500K, which reaches break-even around month 42 without new funding.

**Q: Isn't the Anvest Score a recommendation?**
It is presented as a data summary: no buy/sell/hold, no target price, sources shown. Counsel reviews it with the RA registration. *(Confirm the live wording first; see §4.9.)*

**Q: SEBI registered?**
Not yet; RA registration is funded in this round. Until then the product is designed to avoid buy/sell/hold, target prices and personalised advice, and counsel will confirm its position.

**Q: What if Screener, Tickertape or StockGro build this?**
Each already covers part of the task, per their own pages (19 Oct 2026). Screener Premium includes ₹500 of AI document credits. Trendlyne offers AI screener creation, screener backtesting, portfolio reports and basket execution, which makes it the closest broad alternative. StockGro's Stoxo offers AI research and a strategy builder with backtests, but no paper trading. Tijori offers a natural-language screener and a filing timeline; Streak runs technical-rule strategies with paper and live trading through Zerodha. Anvest's reason to be chosen is the connected task: cited evidence → editable screen → costed backtest → paper trade, with fund, bond and retirement planning in the same account. We will publish a head-to-head on the same tasks (accuracy, coverage, effort, latency and cost) rather than assert an advantage. Screener's per-answer charge is a price; our cost per answer is a model input to re-measure after the October migration.

**Q: Did you apply to YC?**
"Applied for Fall 2026, didn't get in." One sentence, then move on.

**Q: Why this cap?**
It is below typical micro-VC entry prices, identical for every investor, and sized so that month-15 milestones can be judged on evidence. We make no forecast of the next round's size or valuation.


## 6. Product breadth and expansion: how to pitch it

**Company positioning (revised 20 Oct 2026):** Anvest is India's AI research co-pilot: cited filing answers, costed backtests and portfolio impact, for SEBI-registered professionals and serious investors. It spans research, discovery, strategy simulation and financial planning. AI is the shared interaction layer across the tools: it interprets natural-language intent, explains results and links into relevant workflows. A home-screen request can produce a prepared stock screen. The warehouse and calculation engines supply the data and arithmetic. Filing research for professional teams is the first revenue test. It is the entry point into a broader platform.

**Live today:** filing-grounded research, AI screener, portfolio X-ray, strategy backtesting, paper trading, wealth planning, calculators and educational guides. Founder confirmed the live tool status on 14 Oct 2026. A signed-in site review observed strategy templates with cached backtest metrics, a paper-trading workspace, wealth and retirement pages, and guides. This was a feature inventory, not a numerical correctness audit or an end-to-end certification of every tool.

### What the investor should understand

1. Existing breadth demonstrates what has been built. It does not establish demand for every module.
2. Research, screening and portfolio context are the near-term professional workflow. Sell one recurring customer job first.
3. Backtesting and paper trading let users test assumptions and practise. Simulated returns are not forecasts or proof of an execution edge.
4. Wealth tools and calculators support educational scenarios. They do not establish an advisory business, advisory permissions or assets under management.
5. Guides exist today. Deeper courses, education distribution and professional training remain hypotheses until demand and economics are measured.

### Why the breadth might matter economically

The hypothesis is that adjacent tasks increase retention and paid conversion, and that some professional users pay for a broader workflow. Measure it rather than crediting it automatically: research-to-screen usage, screen-to-backtest use, backtest-to-paper progression, planning revisit rates, paid conversion, renewal and support cost by segment. The existing revenue bridge remains unchanged. Do not add course, brokerage, algo or wealth-service revenue without a separate model.

### Expansion gates

| Opportunity | Connection to today | Evidence required before a commitment | Pitch placement |
|---|---|---|---|
| Deeper education | Existing guides, explanations and simulated practice | Completion, useful task outcomes, repeat use and willingness to pay | Main roadmap, after retention |
| Deeper wealth planning | Existing wealth and retirement scenarios, calculators | Retained use, paid demand, data handling and counsel-reviewed scope | Main roadmap, after retention |
| Exchange-registered strategies (algo) | Existing backtests with Indian costs, paper trading and white-box rules | SEBI RA registration (funded this round), exchange empanelment, a partner broker, risk validation and real demand | Main deck: "future of trading" slide, marked NEXT; revenue engine 4 from Year 2 |
| Brokerage or licensed wealth services | Existing research and portfolio context | Separate economics, specialist team, regulatory approvals and capital plan | Longer-term option |
| International markets | Reusable ingestion and research architecture | India retention and economics, local data rights, coverage and customer need | Optional expansion |
| Advanced quant / HFT | Founder ambition; a substantially different operating model | Separate research edge, talent, market access, infrastructure, risk governance and capital | Appendix or a direct answer only |

**HFT is not a seed-round deliverable.** Avoid presenting it as the inevitable next step from end-of-day research or paper trading. The 19 October deck does not name HFT; its appendix roadmap mentions "advanced quant research for professional desks" as H3. Answer HFT questions directly if asked.

### Diligence answers on breadth

**Q: Is this a research product or a broader investing platform?**
A broader platform is live: research and screening, backtesting and paper trading, wealth tools and calculators. We are testing professional filing research as the first recurring revenue workflow. Paid demand determines how we expand.

**Q: Why so many tools with about 100 registrations?**
The build demonstrates execution, but we do not claim every tool has product-market fit. We now need to narrow commercial execution, measure workflow use and renewals, and stop investing in modules that do not earn customer use.

**Q: Are algo trading, brokerage and HFT in this round?**
This round funds the foundation for algo strategies: SEBI RA registration, which SEBI's retail algo framework requires of black-box strategy providers, plus the live backtesting and paper-trading stack. Live strategies run through partner brokers once exchange empanelment is in place, so they are a post-seed revenue engine. Brokerage and HFT are not part of the plan. The budget and revenue milestones remain tied to the existing platform and paid research use.


**Home-screen verification, 14 Oct 2026:** A natural-language request for profitable companies with ROCE above 20% and debt-to-equity below 0.5 produced a screener link carrying `roce > 20 AND debt_to_equity < 0.5 AND profit_margin > 0`. The AI response reported that matching stocks could not be loaded in that attempt. Opening the generated link then loaded the requested formula in the screener and displayed 420 matches. This confirms intent-to-query routing and results-page loading for that request, not numerical correctness of the entire warehouse. The initial chat retrieval fallback should be checked before an investor demo.

## Market expansion and funding paths (20 October 2026)

The $500K target case reaches month-42 break-even without new funding under the model assumptions. The separate Series A scenario scales to approximately ₹23.1 Cr Year-5 ARR: ₹13.4 Cr from Desk and retail plus ₹9.7 Cr from conditional partner and strategy revenue, rounded. Years 3–5 expand Desk into broader distribution professionals, family offices and CA/wealth practices. The 4,132 Year-5 seats would equal 19% of the initial 21,750-seat professional SAM, so the initial segment alone is not the growth plan. The broader ₹1,284 Cr professional TAM is a list-price opportunity, not a count of signed customers or unique firms: ARN and EUIN holders are people/registrations.

Scenario expenses now include every added seller's salary and higher marketing from months 19 and 37. Scenario cash excludes an unspecified Series A amount and is an unfunded balance, not a funded runway promise. Revenue remains a planning scenario. No later approvals or contracts are presumed complete.

Production snapshot, 20 October 2026: 31 registered accounts; 418 logged research queries across 16 accounts; 238 saved backtest records; 2 saved screens. These include founder and testing activity. They are not paid-customer, retention, completed-run or external-user metrics. Source audit: revenue and PAT matched 50 of 50 recent consolidated Q2 FY27 NSE XBRL filings; this measures line-item extraction, not full AI answer accuracy.
