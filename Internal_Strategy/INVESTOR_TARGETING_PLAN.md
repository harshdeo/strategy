# Anvest — Who to Target First, and How to Sequence the Round

**INTERNAL — not for sharing.** Contacts, sequencing and current evidence revised 20 Oct 2026. The researched [outreach playbook](../Outreach/OUTREACH_PLAYBOOK.md) and [tracker](../Outreach/Anvest_Investor_Tracker.xlsx) are the current contact and action references. Companion to `FUNDING_PLAN.md` (current round), `GTM_PLAN.md` (customer execution) and `../README.md` (file map).

This version ranks investors on **observable criteria** — stage fit, cheque size, relevant investments, introduction access and conflicts — not on probabilities. Any probability I could give would be a guess; the order below is a reasoned priority, not a forecast.

## 1. The financing arithmetic comes first

The headline ask is **$500K**, with a first close at $400K and room to $700K. At ₹95/USD, **$400K ≈ ₹3.8 Cr**, **$500K ≈ ₹4.75 Cr** and **$700K ≈ ₹6.65 Cr**.

- 4–6 angels at ₹10–25L each raise ₹40L–₹1.5 Cr. That is **well short of the first close**.
- To close $400K the realistic routes are: (a) one institutional lead of roughly $250–500K plus angels filling the rest; (b) a smaller first close from angels (for example ₹1–1.5 Cr) with a stated plan to add a lead; or (c) larger angel cheques (₹25–50L) from a handful of strong-conviction angels.
- Decide which route you are running before Wave 1, because it determines how many conversations you need and whom you ask first.
- Keep the cap table short. Pool cheques under about ₹10L through one syndicate or SPV rather than taking them directly; a long list of small holders slows every later round.

## 2. Targets and contact routes

The tracker contains 50 individual entries, including 26 funds/programs in the first three proposed waves. It also preserves networks, later-stage funds, duplicate personal routes and unnamed prospecting pools, clearly marked. Eighteen entries have a published email, including general and historical routes whose limits are recorded; other entries use official forms or verified social routes. No email is guessed. Publication checks do not establish delivery or available capital.

| Sequence | Targets | Why / how |
|---|---|---|
| 20–22 Oct | Eximius, All In, Titan, Inuka, Gemba | Current-round candidates with published pitch or investment-team contact routes. Send the full seed pitch now. |
| 23–29 Oct | India Quotient, Zeropearl, Whiteboard, z21, First Cheque, Rainmatter, SenseAI, Better, 3one4 | Suitable early-stage or relevant thesis routes; use official forms where preferred. Actual introductions in parallel. |
| 30 Oct–6 Nov | WaterBridge, Prime, Elevation, Z47, Surge, Grayscale, Antler Direct, Neon, FortyTwo, 100X, OTP, Huddle | Assess specific stage/thesis constraints. Do not invent global traction, frontier-model research or open program intake. |
| Separate processes | IAN, LVX, AngelList India | Networks or financing administration need actual investors/sponsors, not just platform registration. |
| Later / verify | Sparrow, Blume, Bertelsmann, Fundamentum, Vertex, Arkam, Lightspeed, Atoms, BoldCap, Axilor, Mumbai Angels, Backrr | Published cheque/stage mismatch, unclear fit, inaccessible route or current intake needing verification. See the row-specific notes rather than blanket exclusions. |

[Contact research notes](../Outreach/CONTACT_RESEARCH_NOTES.md) record sources and open questions. Antler's current India site offers Direct outside residency; the old residency-only exclusion was wrong. Several large funds offer day-zero routes, so size alone does not make a fund relationship-only. Conversely, Sparrow's $1M–$2M range and Blume's published traction guidance make them lower priorities for this $500K pre-revenue round. These are fit judgments, not predictions.

Groww is a separate potential commercial partnership, with no equity mandate or direct contact verified. Sanjay/Prime and Nithin/Rainmatter should be coordinated conversations, not multiple independent leads. Other operator angels need actual introductions. Professional and creator categories remain prospecting pools until named prospects and suitable contacts are established.

## 3. Sequencing, aligned to evidence

Start suitable pre-seed investors now, while selling to professional customers in parallel. A paid pilot is useful evidence, not a blanket requirement to email a fund whose stated mandate includes pre-revenue founders. Do not broadcast to every tracker row.

Use one personalized first contact per fund. Ask a real mutual for an introduction where useful; wait at most 48 hours before using a suitable official route. Send the seed PDF and a clear $500K ask, with founder full-time from close and pre-revenue status disclosed. The current drafts are in [Anvest_Outreach_Emails.md](../Outreach/Anvest_Outreach_Emails.md).

Follow up on day 7 and, if useful, day 14 on the same thread, then pause without a reply. After a reply or meeting, agree an explicit next action and date. Never manufacture urgency, investor commitments or pilot activity. All tracker sent/touch fields remain blank until a real send is logged.

Customer interviews, paid-pilot offers, activation/retention measurement and product reliability work continue daily. They generate substantive updates for investors. The broker pilot remains a separate commercial conversation with its own tailored materials.

## 4. Before broad outreach, close these gaps

1. **Use the dated user evidence:** 31 registered accounts in the 20 October production snapshot, including founder/testing. The later 12:51 IST audit identifies 26 external accounts, 15 with a recorded workflow and five active in at least two IST calendar weeks. These are historical activity measures, not D7/D30 cohort retention.
2. **Operational facts:** verify the production broker authentication path and remove the unofficial session-token fallback (the partner deck says "no unofficial access", so this must be true before it goes to any broker); confirm whether Kite Connect keys are configured in production; separate historical symbol coverage from current ingestion freshness (BSE ingestion is blocked under a renewed exception to 1 Dec 2026); document token handling and permissions.
3. **Data-use rights:** confirm NSE/BSE licence terms for the actual commercial use before any partner pilot. The provenance memo says data-quality corrections "are published as they are found"; make sure a public corrections log exists, or reword that line, before the memo goes out.
4. **Counsel:** confirm the financing instrument (the current materials say "convertible instrument (CCD/CCPS)") and the product's regulatory position before registration.
5. **Full-time commitment:** decided — full-time on Anvest from the close of this round. Have the employment notice period and the date ready.
6. **Company hygiene:** inspect the actual cap table, founder IP assignment and employment/outside-work clauses with counsel. Current ownership, signed assignment and employer clearance were not verified by this refresh. Do not treat old tracker assumptions as company records or prescribe a share transfer without checking them.
7. **Unit costs after the model migration:** measure current inference cost rather than assuming an increase or decrease. Re-measure cost per answer and Desk-seat margin before quoting ₹0.36 or any margin figure. The decks no longer quote a margin.
8. **Demo resilience:** make a real 3-minute recording and test current production routes before calls. Serving now uses Vercel/GCP; verify actual availability rather than repeating the old Mac-hosting dependency. Use the latest resolution table in the dedicated backlog: four broker bugs have production replay closure; cold-run latency and the cash-added tile remain. Reconcile the corpus-count discrepancy before attaching PDFs.
9. **Product matches the deck:** the deck covers AI across research, screening, backtesting, paper trading, wealth tools and calculators. Check demo routes, coverage disclosures and current product wording. The Anvest Score and tax compiler are outside the main pitch; their actual behaviour still needs to match the stated product scope.

## 5. Why this round is plausible, and its limits

- The round is small, so a lead plus angels can fill it.
- The $3.5M proposed post-money cap is consistent across the materials. A fund's actual valuation and instrument terms are not yet agreed; do not claim it is below a verified market benchmark.
- The shortlist has current first-party evidence of pre-seed, fintech and software mandates. A mandate is not evidence that a fund will invest in Anvest.
- The honest limit: the product is early, pre-revenue and has 31 registered accounts in the 20 October snapshot, including founder/testing. Expect investors to weight paid pilots and retention heavily, and expect the round to take weeks.

---

# Internal diligence Q&A: truthful answers, framed well

**These answers reflect the documented position and dated observations. Confirm current facts before using them. Do not shorten them into something misleading. If a number is asked for, give the verified one.**

**Q: How many users do you have?**
The 20 October production snapshot records 31 registered accounts, including founder/testing. It also records 418 logged research queries across 16 accounts, 238 saved backtest records and 2 saved screens. The later 12:51 IST audit identifies 26 external accounts, 15 with a recorded workflow and five active across at least two IST calendar weeks. External research has 268 rows across 13 users, seven with repeat rows. These definitions do not establish D7/D30 cohort retention or workflow success rates; failed attempts are not recorded.

**Q: Revenue?**
Pre-revenue. Launch pricing is set (Free / Plus ₹199 / Pro ₹599 a month / Desk ₹2,999 per seat, 1–5+ seats). Paid professional pilots are the first thing I'm selling; checkout goes live in the first 90 days after close.

**Q: How big is the first segment?**
SEBI's intermediary directory (checked 19 Oct 2026) lists 2,304 research analysts, 1,057 investment advisers and 539 portfolio managers: about 3,900 regulated firms, with about 3.5 lakh mutual fund distribution professionals (ARN and EUIN holders, Jun 2026) beyond them. The $500K plan's 77 paying teams at month 15 is about 2% of those firms. Market sizing at list prices: TAM about $1.3B a year, SAM about $250M a year, of which professionals are about ₹78 Cr (3 seats per firm) and active investors about ₹2,292 Cr (see `../Financial_Models/operating_model.py`). Professionals are the entry; active investors and partner distribution are the scale.

**Q: What are the month-15 targets?**
From the monthly operating model (`../Financial_Models/operating_model.py`). $500K target: ₹87 L ARR run-rate (₹7.3 lakh net MRR), 77 Desk teams (~243 seats), 2 paying partner integrations and ~186 retail subscribers; break-even about month 42 without new funding. $400K first close: ₹68 L ARR and 55 teams, with cash to about month 31. $700K (second seller from month 6): ₹1.06 Cr ARR, 88 teams and 3 partners. Also SEBI RA registration and a published head-to-head benchmark. The drivers are planning assumptions: seller productivity (4 teams a month once ramped, the founder 1), 3 seats per team, churn, conversion and partner usage priced ₹15 → ₹10 → ₹6 per user. They will be replaced by measured pilot data. The long-term scenario reaches about ₹23 Cr ARR in year 5. It is conditional on a Series A, approvals and partner contracts; Desk plus retail account for ₹13.4 Cr of it.

**Q: Where does production run?**
The frontend runs on Vercel, with public backends and warehouse services on GCP, per the current operations guide. This is topology, not a fresh availability or end-to-end certification. State dated checks and open issues accurately; do not describe the old Mac production dependency as current.

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
Provide the actual signed founder IP assignment and the counsel-reviewed employment/IP position. These records were not inspected in this refresh. Do not assert company ownership or employer clearance based on the old tracker.

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
It is the proposed $3.5M post-money cap used consistently in the materials, sized against the round and month-15 milestones. Final instrument and financing terms are subject to agreement; no market valuation benchmark was established here. We make no forecast of the next round's size or valuation.


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

**Q: Why so many tools with only 31 registered accounts, including testing?**
The build demonstrates execution, but we do not claim every tool has product-market fit. We now need to narrow commercial execution, measure workflow use and renewals, and stop investing in modules that do not earn customer use.

**Q: Are algo trading, brokerage and HFT in this round?**
This round funds the foundation for algo strategies: SEBI RA registration, which SEBI's retail algo framework requires of black-box strategy providers, plus the live backtesting and paper-trading stack. Live strategies run through partner brokers once exchange empanelment is in place, so they are a post-seed revenue engine. Brokerage and HFT are not part of the plan. The budget and revenue milestones remain tied to the existing platform and paid research use.


**Home-screen verification, 14 Oct 2026:** A natural-language request for profitable companies with ROCE above 20% and debt-to-equity below 0.5 produced a screener link carrying `roce > 20 AND debt_to_equity < 0.5 AND profit_margin > 0`. The AI response reported that matching stocks could not be loaded in that attempt. Opening the generated link then loaded the requested formula in the screener and displayed 420 matches. This confirms intent-to-query routing and results-page loading for that request, not numerical correctness of the entire warehouse. The initial chat retrieval fallback should be checked before an investor demo.

## Market expansion and funding paths (20 October 2026)

The $500K target case reaches month-42 break-even without new funding under the model assumptions. The separate Series A scenario scales to approximately ₹23.1 Cr Year-5 ARR: ₹13.4 Cr from Desk and retail plus ₹9.7 Cr from conditional partner and strategy revenue, rounded. Years 3–5 expand Desk into broader distribution professionals, family offices and CA/wealth practices. The 4,132 Year-5 seats would equal 19% of the initial 21,750-seat professional SAM, so the initial segment alone is not the growth plan. The broader ₹1,284 Cr professional TAM is a list-price opportunity, not a count of signed customers or unique firms: ARN and EUIN holders are people/registrations.

Scenario expenses now include every added seller's salary and higher marketing from months 19 and 37. Scenario cash excludes an unspecified Series A amount and is an unfunded balance, not a funded runway promise. Revenue remains a planning scenario. No later approvals or contracts are presumed complete.

Production snapshot, 20 October 2026: 31 registered accounts; 418 logged research queries across 16 accounts; 238 saved backtest records; 2 saved screens. These include founder and testing activity. They are not paid-customer, retention, completed-run or external-user metrics. Source audit: revenue and PAT matched 50 of 50 recent consolidated Q2 FY27 NSE XBRL filings; this measures line-item extraction, not full AI answer accuracy.

Outreach attachment check (later 20 October audit): VM corpus counts are 6,155,194 passages / 633,688 distinct doc_ids; both current deck masters still contain 1.35M passages. Reconcile all attached exports before sending, preserving other sessions' deck edits. See `../Outreach/CONTACT_RESEARCH_NOTES.md`.
