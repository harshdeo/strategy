# YC Fall 2026 Application — Anvest Fintech Private Limited

**Deadline: July 27, 2026, 8:00pm PT** (= July 28, 8:30am IST). Decision by ~Aug 28. Batch Oct–Dec 2026, in-person San Francisco. Demo Day Dec 2.
**Terms:** $125K for 7% (post-money SAFE) + $375K uncapped MFN SAFE.
**Form:** https://apply.ycombinator.com — this file mirrors the exact section order and questions on your live application as of today.

> **How to use this file.** These are drafts, not copy-paste. Every answer follows Paul Graham's stated guidance: matter-of-fact, no marketing language, flaws disclosed rather than concealed, specifics over adjectives. Fill every `[TODO]` — those are things only you know. Read the whole thing aloud once before you paste it in; anything that sounds like a press release, cut.

---

## ✅ STATUS: Submitted, 2026-07-27. Cannot be edited.

The application is in. This section is now a reference for **if YC follows up** — a screening call, an interview invite, or a clarifying email — not a to-do list for the form itself.

**The one action item that survives regardless of YC's decision:** the cap table. As submitted, the founder holds 0% of Anvest Fintech Pvt Ltd; two family members hold 99%/1% as placeholder shareholders from incorporation, with a transfer to the founder described as pending. This needs to be executed for real — Form SH-4, board resolution, updated register of members — via a CA/CS, this week, independent of anything YC decides. Every future investor conversation hits the same fact.

**If you get a call: the consistent version of the answers that had internal contradictions in the submitted form.** Use these, not the submitted text, if asked to elaborate on any of the following:

| Question | What the submitted form said | What to say if asked |
|---|---|---|
| Looking for a cofounder? | "Not yet" — then immediately said "I've chosen to stay solo" | Just: "No — I've chosen to stay solo and hire rather than co-found." One consistent answer. |
| How long have you worked on this? | "A year" in two places, "the last few months" in a third | Pick the true number once and use it everywhere. Say it plainly if the discrepancy comes up: "the honest number is X — I was inconsistent in the written form." |
| What's the core product insight? | Two different answers: the proactive digest (in "what will you make"), and a risk-matched trading-idea generator with backtesting, paper trading, and eventual DRL auto-evolution (in "competitors") | The digest is the real one — it's buildable now, it's the retention mechanism, and it's what's actually next on the build list. The trading-idea/DRL vision is a real long-term direction but describing it as *the* differentiator alongside the digest makes the pitch read as two different companies. If asked, lead with the digest; mention the later vision only if pressed, and frame it explicitly as later, gated on trust in the numbers being established first. |
| Where does this go long-term? | "Guided action and algo trading, and then becoming broker ourselves" — named explicitly | Soften on the spot if it comes up live: "the near-term destination is closing the loop from research into some form of guided action; a broker license is a much later, separately-capitalized decision, not something I'm building toward now." Naming the broker license unprompted invites "why would we fund a research company aiming to become a bank" — don't reintroduce it if it doesn't come up. |
| Where would the company expand to next? | "Most likely the USA, biggest economy, ample opportunities" | If asked: emerging markets with mandatory structured filings and no incumbent doing the data work — Southeast Asia, UAE/Saudi — not the US. AlphaSense, Rogo, and Fiscal.ai already occupy the US research-AI category; naming it as "next" invites an unwinnable comparison. |
| How will you make money, and how much? | Three retail tiers, no ceiling estimate, no B2B mention | Add it verbally if asked: "~$24M ARR ceiling from 1% of India's active retail researchers at Ultra pricing, but the faster near-term revenue is a professional tier for SEBI-registered research analysts — higher ARPU, faster sales cycle, and it's where I'm actually starting." |

Everything else in the submitted form is fine as-is and doesn't need a correction.

---

## ⚠️ Original pre-submission notes (kept for the record — no longer actionable)

You mentioned you're still working at a firm while building this. That single fact touches three separate fields below (**"how much of that has been full-time," "are any founders covered by an IP agreement," "where would the company be based after YC"**), and it's worth getting right before you write a word, because half-answering it in three places is worse than answering it once, directly.

**Two things to do before you submit, not after:**

1. **Re-read your employment contract's IP-assignment and moonlighting clauses tonight.** Most Indian tech employment agreements assign the company any IP you create "during your employment" or "using company time/resources/confidential information" — some are scoped narrowly to your job duties, some are broad enough to reach a side project built entirely on your own laptop and your own time. You need to know which kind of clause you signed **before** you tell YC (or any investor) that you own 100% of Anvest. This is not optional due diligence — it is the single fastest way this raise dies later if it's wrong.
2. **Decide your resignation timing now, on paper, even if you don't act on it yet.** If accepted, the batch is in-person in San Francisco, October–December — full-time attendance is expected. There is no version of this where you do YC while staying employed. Have the honest date in your head: "I resign within X weeks of acceptance."

The answers below are written honestly around a **part-time-until-acceptance** framing, because that is the truthful, common, and *fundable* situation — a large fraction of YC founders apply while still employed. What is not fundable is discovering later that a former employer has a claim on the code. Get the contract read this week; it costs nothing and it's the one item on this list a lawyer, not an LLM, should confirm.

---

## Founders

**Who writes code, or does other technical work on your product? Was any of it done by a non-founder? Please explain.**

> I write all of it. Every layer — the data warehouse and XBRL ingestion pipeline, the OCR queue, the vector index and retrieval system, the synthesis and verification loops, the frontend, and a separate deterministic tax-return compiler — is my own code. No non-founder, contractor, or agency has touched the codebase. [TODO: if you used any AI coding assistant heavily — Claude Code, Cursor, Copilot, etc. — say so plainly in the tech-stack answer below; YC now asks this directly and there's no reason to hide it, most applicants use one.]

**Are you looking for a cofounder?**

> No. [See the full reasoning in the "why solo" answer below — keeping it here per the form's structure, but it's one decision, stated once.]
>
> I've chosen to stay solo and hire rather than split equity with a co-founder at this stage. What I've built alone in the last year — a full-universe financial data warehouse, an OCR and vector pipeline over 584,000 filings, a grounded retrieval system with verification loops, a production frontend, and a deterministic tax compiler that emits schema-valid government JSON — is the evidence that I can execute without one. What I'm hiring for, not co-founding for, is distribution: someone who has taken an Indian consumer product from zero to real usage. That's a different skill from the one I have, and I'd rather buy it with a salary and equity than a 30–50% co-founder stake I can't take back.

---

## Accomplishments

**Please tell us about a time you most successfully hacked some (non-computer) system to your advantage.**

> [TODO — this is Paul Graham's own wildcard question, and he's said a good answer here alone has earned people interviews. It must be **non-computer**: a time you got what you wanted out of a rule, process, institution, or bureaucracy through cleverness rather than authority or money. Nothing on your resume tells me this story — it's not the kind of thing that goes on a resume — so this has to come from you. A few angles from your actual life that might hold a real story, worth five minutes of thought each before you write:
>
> - **JEE prep or the exam itself** (AIR 1,825 out of 1.5M) — did you find an unconventional approach to the prep grind, the coaching-institute system, or the exam-day logistics that most aspirants didn't?
> - **CAT 2020** (99.22 percentile) — same question, especially since you sat it *while already working full-time* as an engineer, which is itself an unusual constraint most CAT takers don't have.
> - **Moving through five employers in seven years while climbing from Software Engineer to Senior Engineering Lead** — was there ever a negotiation, a leveling conversation, an internal process, or a hiring loop you read differently from how it was designed to be read, and won?
> - **IIT Guwahati specifically** — hostel allocation, course registration, a professor's grading system, a club or fest — the institute systems every IIT student has at least one story about.
>
> Write the real one. Specific and concrete beats impressive-sounding — PG's stated advice is that these answers read as fake the moment they're vague.]

**Please tell us in one or two sentences about the most impressive thing other than this startup that you have built or achieved.**

> I built Weave's Analytics Platform from zero to one as lead engineer on a 6-person team — real-time Kafka and NSQ pipelines ingesting millions of daily events — and ran it in production for 18 months with zero critical incidents while it served 25,000+ US small-business customers. Separately, I placed in the top 0.12% of 1.5 million JEE Advanced candidates nationally (All India Rank 1,825), which is the exam that got me into IIT Guwahati.
>
> *(Both are true and on your resume, so no TODO here. If you have a sharper, more personal story that isn't on paper anywhere, it will beat this — PG's guidance is explicit that this question is not about your startup, and the best answers are often something a resume can't capture.)*

**Tell us about things you've built before. For example apps you've built, websites, open source contributions. Include URLs if possible.**

> Everything I've built professionally so far has been inside a company, not in the open — I don't currently have a public GitHub, personal site, or open-source contribution to link, which I'd rather say plainly than pad the answer. What I have built:
>
> - **An agentic LLM system in production at New Relic** that reads natural-language permission-change requests and autonomously generates and raises the GitHub PRs needed to fulfill them — cut permission-change turnaround from hours to minutes. (Function calling, MCP, GitHub API, Python.) Proprietary, no public URL.
> - **Weave's Analytics Platform, 0→1**, as lead engineer on a 6-person team — the real-time engagement-insights product referenced above. Proprietary; Weave is public (NASDAQ: WEAV) but the platform itself isn't externally demo-able.
> - **A secure Software-Over-The-Air update framework for Jaguar Land Rover vehicles** — remote software delivery at fleet scale, replacing physical dealership updates. Proprietary automotive OEM software.
> - **An ML/image-recognition HMI test-and-validation pipeline at JLR** that automated manual in-vehicle UI validation, more than doubling testing throughput.
> - **An AR-based, secure, personalized Android authentication system** built during a Samsung R&D internship — ranked #1 of all summer interns that cohort. Proprietary, Samsung IP.
> - **Two academic ML projects at IIT Guwahati:** a network intrusion detector trained on the NSL-KDD dataset (F1 score 0.923), and a real-time human-activity classifier from raw accelerometer data (97.8% accuracy). [TODO: if either of these lives in a personal or university GitHub repo, link it here — these are the two most likely to actually have a URL, and it's worth five minutes checking an old account before you write "no URL available."]
> - **Anvest itself** — the subject of the rest of this application, and by a wide margin the largest thing on this list. Covered in full elsewhere in the form, so not repeated here.
>
> [TODO: if you have *any* small personal project outside work — a script, a tool, a Chrome extension, a Kaggle notebook, anything with a URL — add it. This question explicitly rewards a public artifact, and right now every real thing on this list is behind a company's login.]

**List any competitions/awards you have won, or papers you have published.**

> - **JEE Advanced 2015** — All India Rank 1,825 out of ~1.5 million candidates (top 0.12% nationally).
> - **CAT 2020** — 99.22 percentile.
> - **Samsung R&D Best Internship Project, Summer 2018** — ranked #1 across all summer interns, for the AR-based Android authentication system above.
>
> No papers published.

---

## Founder Video

**Please record a one minute video introducing the founder(s).**

[TODO — record this yourself, on camera, unscripted-sounding even if you rehearse it. Guidance:]

- **Say your name, IIT Guwahati, and 7 years as a software engineer** in the first 15 seconds — it's the fastest way to establish technical credibility to a partner who has 60 seconds to form an impression.
- **Say what Anvest does in one sentence**, the same one you use in the "what is your company going to make" answer below — consistency across the application matters more than eloquence.
- **Say you built it solo, currently part-time alongside a full-time engineering job**, and that you'd go full-time immediately if accepted. Do not let the video and the written form say different things.
- **Do not read a script on screen.** A partner can tell. Practice out loud five times, then record without notes.
- Keep it under a minute. One minute means one minute — this is filtered by partners who watch dozens of these; going long reads as not respecting the constraint.

---

## Company

**Company name:** Anvest Fintech Private Limited

**Describe what your company does in 50 characters or less.**

> `AI research analyst for Indian stocks` (38 characters)
>
> Alternates if you want a different emphasis — count characters before you paste, YC enforces the limit:
> - `Grounded AI equity research for India` (38)
> - `Ask any Indian stock a question, cited` (39)

**Company URL, if any:** https://anvest.in

**If you have a demo, attach it below.** (limit 3 minutes / 100MB)

[TODO — record a 2–3 minute screen capture. Full script in the "Demo video script" section at the end of this file. Do this after the written form is done; the writing matters more than the video, and the video matters more than the polish of either.]

**Please provide a link to the product, if any.** https://anvest.in

**If login credentials are required for the link above, enter them here.**

> [TODO — if the copilot/AI surfaces require sign-in, either (a) ship the "3 free anonymous questions" feature from your task list before submitting, so a partner can actually try it without an account, or (b) provide a demo login here. Option (a) is strictly better — a partner who can't click around themselves discounts the whole application.]

**What is your company going to make? Please describe your product and what it does or will do.**

> Today, Anvest lets you ask any question about any of India's 6,137 publicly listed companies and get an answer sourced from that company's actual regulatory filings — not a hallucinated guess. Ask something concrete, like why a company's operating margin fell last quarter, and it answers from the company's own filed results, links the exact page the number came from, and says plainly when the data was never filed rather than inventing a plausible one. Every answer is also grounded in the Anvest Score and other metrics we calculate ourselves from established formulas, so the model is reasoning over numbers we've already verified, not just quoting a paragraph of text.
>
> We can do this because of a year spent on the layer competitors have skipped: parsing and extracting historical exchange announcements, fixing known errors in how India's exchanges publish structured filing data, and indexing all of it so retrieval finds the right passage instead of a keyword match. The model itself is never allowed to calculate a number — everything a user sees is read from a database we built, not generated by the LLM.
>
> What we're building next turns Anvest from something you ask into something that tells you. A daily digest will surface what changed on the companies someone follows before they think to check — a promoter's holding moved, a filing landed, a metric crossed a threshold. A read-only link to a user's broker account makes every answer specific to what they actually own, and is also what upgrades our data from end-of-day — refreshed nightly today — to live, since that same link carries a live price feed. Longer term, once trust in the numbers is established beyond doubt, the destination is to close the loop from research into guided action.

*(One-line version, for the founder video and anywhere else you need a single sentence — not a separate form field on the current app, but keep it consistent wherever you use it: "Ask any question about any Indian stock, get an answer sourced from the actual filing — not a hallucinated number.")*

**Where do you live now, and where would the company be based after YC?**
*(format: City A, Country A / City B, Country B)*

> [TODO — your current city], India / [TODO — your current city], India
>
> Note for the field just below: the company's market and data pipeline are India-specific, so HQ stays in India regardless of batch location — the "after YC" city here should be where the company is based, not where you personally sit during the batch (that's covered next).

**Explain your decision regarding location.**

> Anvest's product, data sources, regulatory path (SEBI), and entire user base are India-specific — the XBRL dialect, the exchange filing conventions, and the customer segment (Indian retail investors and SEBI-registered research analysts) don't travel. The company is and stays headquartered in India.
>
> For the batch itself: YC Fall 2026 is in-person in San Francisco, October–December. I would relocate for those three months to attend in person, then return to run the company from India, where the team, the data infrastructure, and the customers are.

---

## Progress

**How far along are you?**

> The product is live at anvest.in and works. I've built, alone: the full data warehouse and XBRL ingestion pipeline with a repair layer for the exchange's own malformed filings, an OCR queue and vector index over years of corporate announcement PDFs, a research copilot with retrieval, synthesis, and self-verification loops, the frontend, and a separate deterministic Indian tax-return compiler that emits schema-valid government JSON.
>
> What I don't have is users. I spent the year on the data layer, which couldn't be faked or outsourced, and under-invested in getting strangers to use it. Zero MAU, zero revenue, no engagement telemetry yet. Production runs in Docker on my own Mac behind a Cloudflare tunnel — total infrastructure spend to date is roughly zero, plus free GCP credits.
>
> I'm closing that gap on a short timeline, not waiting on YC's decision: engagement telemetry ships this week, a free tier for India's income-tax filing season goes live before the August 31 deadline for derivatives traders — which brings in users who arrive already holding their own portfolio data — and I'm signing the first SEBI-registered research analysts as paying seats. The next product milestone is the proactive digest described in the answer above: the feature that turns Anvest from a tool people open occasionally into one they check daily.

**How long have each of you been working on this? How much of that has been full-time? Please explain.**

> [TODO — fill in the exact start date.] I've been building this for about [TODO — X months], solo. Almost all of that time has been part-time — evenings and weekends around a full-time job as a software engineer — with [TODO — if there were any full-time stretches, e.g. a sabbatical, vacation days used as a block, say so here; if none, say "no full-time stretches yet"].
>
> I'm not going to overstate this: a part-time solo build is why the product is deep but the distribution is at zero. If accepted, I would resign from my current role and go full-time immediately — I'm not asking YC to fund a side project, I'm telling you honestly what stage of commitment I'm at today so the "how far along are you" answer above is read in the right context.

**What tech stack are you using, or planning to use, to build this product? Include AI models and AI coding tools you use.**

> Backend: Python (FastAPI) across two services — a read-only market-data API and an auth/portfolio/copilot service. Postgres as the single warehouse of numeric truth (financials, shareholding, OHLCV, announcements metadata). Redis for evidence caching and job queues. Qdrant as the vector store, holding 1.35M+ chunks from parsed filings, embedded with a self-hosted bge-m3 model — deliberately not a hosted embedding API, because query and corpus embeddings must share one vector space.
>
> LLM layer: Google Vertex AI, gemini-2.5-flash and -flash-lite, for retrieval synthesis, the NL-to-DSL screener, and verification/self-repair loops — chosen for latency and cost at this stage over a larger model, with an evidence cache bounding token spend. Google Cloud Vision for OCR on scanned small-cap filings.
>
> Frontend: Next.js on Vercel. Ingestion and enrichment run as scheduled jobs (launchd) against the exchanges' own end-of-day bhavcopy files and filing feeds.
>
> [TODO — AI coding tools: name whichever you actually used to help build this — Claude Code, Cursor, GitHub Copilot, etc. — and roughly how much of the codebase leaned on one. YC asks this directly now; there's no penalty for a real answer and there's real signal in explaining what you used AI for versus what you designed yourself, e.g. "I used [tool] for boilerplate and test scaffolding; the XBRL repair logic and the retrieval architecture are hand-designed after finding the specific failure modes in production."]

**Are people using your product?**

> No.

**Do you have revenue?**

> No.

**If you are applying with the same idea as a previous batch, did anything change? If you applied with a different idea, why did you pivot and what did you learn from the last idea?**

> [TODO — if this is your first YC application, say: "This is my first application to YC." If you've applied before with anything, say what, and what's different now — be specific about what you learned, not just what you built since.]

**If you have already participated or committed to participate in an incubator, "accelerator" or "pre-accelerator" program, please tell us about it.**

> None.

---

## Idea

**Why did you pick this idea to work on? Do you have domain expertise in this area? How do you know people need what you're making?**

> I've been an Indian retail investor for [TODO — years]. The tools available are either dense fundamental tables that assume you already know what to ask (Screener.in, Trendlyne) or WhatsApp tip channels with no accountability. I kept doing the same manual thing myself: opening a company's filings on the exchange site, reading a 40-page PDF, and extracting three facts by hand. It's tedious, and most people simply don't do it — which is a real reason 91% of individual F&O traders lost money last year in India, ₹1.06 lakh crore net, per SEBI's own FY25 study. People aren't avoiding research because they don't want to invest well; they're avoiding it because the tools assume expertise they don't have.
>
> The domain expertise I have is specific and unusual, and it's a byproduct of building this alone: I know what actually breaks in Indian financial data. NSE's post-FY23 filings carry malformed XBRL context dates. There is no separate annual XBRL filing — annual consolidated figures have to be mined out of Q4 filings. A naive parse produces Reliance's FY22 profit exceeding its revenue. Roughly 78% of NSE equities had a wrong market cap in my own cache until I found and backfilled it. None of this is documented anywhere public. I know it because I served real queries against real filings and got embarrassed by wrong answers often enough to go fix the root cause each time. On top of the equity research background, I also have 7 years as a software engineer (IIT Guwahati) — which is why I've been able to build the entire warehouse, parser, OCR pipeline, and retrieval system alone rather than needing to hire it out.

**Who are your competitors? What do you understand about your business that they don't?**

> Three camps, and I fear one of them:
>
> - **Screener.in, Trendlyne, Tickertape, StockEdge** — excellent tables, zero interpretation. They serve maybe 5 million of India's 210 million demat accounts, the ones who already know what ROCE means.
> - **Univest and the advisory apps** — "buy X, target Y." Black box, no source. Trust collapses with the first bad call, and it's regulatorily heavier than a research product.
> - **Perplexity Finance and ChatGPT** — fluent, and confidently wrong on Indian numbers. No point-in-time Indian XBRL warehouse, no OCR'd small-cap filings, no accountability for a hallucinated figure. This is the one I fear, because they have vastly more capital and the interaction model I'm betting on is the same one they're already shipping. What I don't think they'll do is the unglamorous part: run an OCR queue over scanned Indian small-cap PDFs, discover that one exchange's XBRL context dates are malformed after one specific fiscal year, and mine annual figures out of quarterly filings because the annual ones don't exist. That's twelve months of engineering with zero demo value until it works, for one country's market — not the kind of thing a generalist search company prioritizes. A broker's in-house team might (Zerodha owns Tickertape), but broker apps have historically optimized for execution, not research depth. My realistic window before someone ships good-enough is six to nine months.
>
> What I understand that they don't: research tools have structurally bad retention, and almost nobody in this category treats it as the central problem. A user opens a research tool when they've already decided to research something — a few times a month at best. That ceiling is a property of the interaction model, not of execution quality. The fix isn't a better answer, it's the unprompted one: "since you last viewed this company, Q1 beat on margins, promoter holding unchanged, two analyst meets scheduled." That's the difference between a monthly tool and a daily habit, and it's the single highest-leverage feature on my build list right now.

**How do or will you make money? How much could you make?**

> Subscription, two tiers.
>
> Retail: free tier with a daily question limit; Pro at ~$3/month. Deliberately under Screener.in (~$52/year) and Trendlyne (up to ~$61/year), while offering a category — grounded conversational AI — neither has.
>
> Professional: seats for SEBI-registered research analysts and boutique portfolio managers at ~$35/month. These people read filings manually every day; it's their actual bottleneck. Forty seats is ~$1,400 MRR from roughly 150 sales conversations — faster and higher-ARPU than the equivalent consumer-acquisition effort, which is why I'm starting there rather than with retail growth.
>
> Ceiling: 210 million demat accounts in India, of whom perhaps 20 million actively research before investing. One percent of that group at ~$25/year is roughly $46M ARR from retail alone — before professional seats, and before any execution-layer revenue that becomes available once there's a trust base (SEBI's retail-algo framework, live since Oct 2025, defines exactly how that would work with a licensed broker as principal).

**If you had any other ideas you considered applying with, please list them.**

> [TODO — this is a real question, not a formality; YC's own guidance says they sometimes fund people to build something listed *here* rather than in the main application. Think honestly about 2–3 adjacent ideas you seriously considered or could pivot into, and replace these placeholders with your actual ones. Starting points, drawn from what you've already half-built, in case they're genuinely on your list:]
>
> - A standalone compliance/research productivity tool for SEBI-registered RAs and boutique PMS desks — bulk Q&A over filings, event monitors, at a B2B seat price — essentially Anvest's professional tier as its own company rather than a channel.
> - A point-in-time, survivorship-bias-free Indian market dataset and backtesting API, sold to quant researchers and fintech builders — productizing the data warehouse and repair layer directly rather than the consumer research product built on top of it.
> - A standalone Indian tax-filing product (the ITR compiler on its own) — deterministic capital-gains reconciliation and government-schema JSON generation as a focused SaaS, independent of the research platform.

---

## Equity

**Have you formed ANY legal entity yet?**

> Yes — Anvest Fintech Private Limited, incorporated in India. [TODO: incorporation date, CIN number.]

**Have you taken any investment yet?**

> No. Fully bootstrapped; the only outside resource has been free GCP credits from Google.

**Are you currently fundraising?**

> Yes. Targeting a $500K pre-seed — YC's standard deal if accepted, in parallel with early conversations with Indian angels and micro-VCs. No term sheet signed.

---

## Curious

**What convinced you to apply to Y Combinator? Did someone encourage you to apply? Have you been to any YC events?**

> [TODO — one or two honest, specific sentences beat anything strategic-sounding. If a person, a blog post, a specific YC company's story, or a specific piece of advice pushed you to apply, name it. If nobody encouraged you and you haven't been to an event, say that plainly — it's a fine answer; PG has said flattery and manufactured enthusiasm are transparent to experienced readers.]

**How did you hear about Y Combinator?**

> [TODO — the real, specific answer. "I've known about YC for years" is fine if true; a specific source is better if there is one.]

---

## Batch Preference

**What batch do you want to apply for?**

> Fall 2026.

*(If rejected from Fall 2026: apply again via YC's Early Decision program for Winter 2027 once you have real usage numbers — see the note at the end of this file.)*

---

## Demo video script (2–3 minutes, screen recording, your voice)

Record on the live site. No slides, no intro music, no logo animation. Talk while you click.

| Time | What's on screen | What you say |
|---|---|---|
| 0:00–0:15 | anvest.in, a mid-cap or small-cap stock page — **not** Reliance or TCS. Something obscure enough to be a real test. | "This is Anvest. I'm going to ask it something you can't ask any other Indian investing product." |
| 0:15–0:50 | Type a genuinely hard question about a specific quarter's margins or a segment. Let it stream. | "This answer is being assembled from the company's actual filings. The model isn't calculating anything — every number comes out of a Postgres warehouse." |
| 0:50–1:20 | **Click the citation. Land on the filing PDF.** Hold on it. | "This is the source. Every claim links back. If we don't have coverage, it tells you instead of guessing." |
| 1:20–1:50 | The proactive digest, if shipped by recording time. Otherwise the NL screener with a plain-English query. | "And it tells you things you didn't ask — what changed on the companies you follow, since the last time you looked." |
| 1:50–2:15 | Cut to a terminal or a plain slide with four numbers: 6,137 symbols · 584K filings · 1.35M vectors · 5,405 profiles. | "Six thousand companies, two years of filings, OCR'd and indexed. One person, part-time, one laptop. That's the part that's hard to copy — the chat interface took two weeks." |

**Recording notes:** ship it slightly rough rather than polished-and-late — YC applications with a demo video are materially more likely to get an interview. Do not run the demo against a stock whose data you haven't spot-checked in the last hour; pick the company, verify the numbers against Screener yourself, *then* record.

---

## Pre-submit checklist

- [ ] **Read your employment contract's IP/moonlighting clause** — this week, ideally with a lawyer. Do this before anything else on this list.
- [ ] Decide, concretely, when you'd resign if accepted — have the real answer in your head, not just on the form.
- [ ] Every `[TODO]` filled, including the IIT Guwahati / 7-years-SWE detail worked into the founder video and the domain-expertise answer
- [ ] Read the whole thing aloud once — anything that sounds like a press release, cut
- [ ] Company description is under 50 characters — count it, don't estimate it
- [ ] "Other ideas" answer reflects things you've *actually* considered, not filler
- [ ] Flaws disclosed plainly: zero users, solo, part-time-until-now, prod-on-a-laptop, known data gaps
- [ ] Founder video recorded, under 1 minute, matches the written form's facts exactly
- [ ] Demo video recorded and attached, against a stock you verified today, under 3 minutes
- [ ] anvest.in is up, and up on mobile — a partner will open it on a phone
- [ ] Login credentials provided if the product requires sign-in — or ship anonymous sample questions first so it doesn't
- [ ] Submitted before **July 27, 8:00pm PT** (= July 28, 8:30am IST)

**If Fall is a no:** apply again via YC's Early Decision program for Winter 2027 once Track C has landed. A rejection now with 0 users and a reapplication in a few months with real users, revenue, and a published retention curve is a genuinely different application — and YC gives written feedback on interview decisions.
