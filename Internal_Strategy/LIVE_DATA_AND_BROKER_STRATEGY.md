> **INTERNAL — audit snapshot, not current production certification.** The substantive audit below is dated 9 October 2026. This cleanup updates file references only. Verify operational status, broker terms, data rights and regulatory conclusions before relying on them. The current partner deck proposes a scoped read-only research pilot; it does not promise execution.

# Anvest — Live Data, Broker Sign-in & Order Placement: Strategy

**Date:** 2026-10-09 · **Status:** research + code audit complete, nothing built or changed
**Companions:** `FUNDING_PLAN.md` (current funded scope), `../Investor_Materials/Anvest_Strategic_Integration_Deck.pptx`, `../Financial_Models/PRICING_AND_UNIT_ECONOMICS.md`
**Not legal advice.** The SEBI and licensing points below are my reading of public circulars and NSE's published price list; get counsel to confirm before building the order path.

---

## 0. The answer in five lines

1. **"Live data" is three different problems with three different costs.** Conflating them is why it feels hard. Live *filings* cost only engineering. Live *prices for a logged-in user's own holdings* cost almost nothing. Live *prices shown to everyone* need an NSE licence.
2. **Start with live filings.** It is the one live-data feature that is also your differentiator, needs no exchange licence, and turns a 24-hour-old product into a same-hour one for the thing Anvest is actually about.
3. **Broker sign-in already exists but is not investor-grade.** The Zerodha path falls back to an unofficial session-token scraper. Replace it before any Zerodha/Rainmatter conversation.
4. **Do not build direct order placement now.** Since 1 April 2026 it runs into SEBI's algo framework (static IP, Algo-ID, broker empanelment), your research-only RA posture, and a production server on a Mac. Route orders through the user's own broker session instead.
5. **Everything above is H1 work except direct execution, which stays H2** — consistent with the horizons in the deck. Don't promise orders inside this round.

---

## 1. Where Anvest actually is (read from the code and docs, 2026-10-09)

| Area | Current state | Source |
|---|---|---|
| Data cadence | One batch: **19:00 IST**, catch-up 06:30. Nothing intraday. Prices are the exchange's end-of-day files. | `ops/docs/DEPLOY_ON_MAC.md` |
| Announcements | NSE healthy. **BSE blocked (403)** — decided policy since 29 Sep: no circumvention; the accepted exception lapses **1 Dec 2026**, after which nights fail by design. | `docs/fix-task-4-…`, `docs/implementation-review-2026-10-07-status.md` |
| Zerodha sign-in | Kite Connect redirect **only if** `ZERODHA_API_KEY` is configured. Otherwise falls back to a pasted **`enctoken`** and calls undocumented `kite.zerodha.com/oms/...` endpoints with a spoofed browser User-Agent. No Kite key appears in `ops/local-hosting/local-backend.env` — **verify what production actually runs.** | `data-platform/app/integrations/zerodha.py`, `zerodha_unofficial.py`, `broker_service.py` |
| Groww sign-in | Official Groww Trading API, but the user pastes an access token by hand. | `integrations/groww.py` |
| What is fetched | Holdings and positions, read-only. **No order code. No quote or websocket code.** Source comments still say "for this POC". | same |

**Two things to fix regardless of the roadmap.** The `enctoken` path asks users to paste a live brokerage session token into your product and drives an undocumented internal API. That is a security liability and exactly what a Zerodha diligence team will find first. The earlier provenance memo's unverified licensing claim has been removed from the retained memo. Data-use rights still require confirmation for the actual commercial use.

---

## 2. Live data: three problems, three costs

### A. Live filings and announcements — do first
- **What:** poll NSE announcements every 5–10 minutes during market hours instead of once at 19:00, embed and index them as they land, and push an alert to anyone holding or watching the company.
- **Why first:** public statutory disclosures, no price-data licence, and it is the part of the product competitors cannot copy quickly. A user told within minutes what a company *just filed* has a reason to open the app on a quiet day — it is also the DAU/MAU mechanism in `GTM_PLAN.md`.
- **Cost:** engineering only. The existing pipeline already parses, OCRs and embeds these; the change is cadence and a small intraday queue.
- **Gate:** BSE stays blocked. Decide before **1 Dec** whether to accept NSE-only intraday (my recommendation: yes, and say so in the product) or pursue an authorised BSE route.

### B. Live prices for a signed-in user's own holdings — do second
- **What:** after the user connects their broker, stream quotes for *their* instruments over the broker's websocket for that session, and compute live portfolio value and P&L.
- **Why it is cheap:** the data flows from the user's own authorised broker session, not from Anvest redistributing exchange data. Kite Connect is ₹500/month per app and includes real-time data; Angel One, Upstox, Dhan and Fyers APIs are free.
- **Rules to hold to:** per-session and ephemeral. Do not store ticks, do not show them to anyone else, do not show them on logged-out pages. Check each broker's terms before relying on this.
- **Gate:** Kite Connect for a *multi-user* product needs Zerodha's approval — the forum guidance is to email kiteconnect@zerodha.com. That is a concrete ask for the Rainmatter conversation, not a blocker you solve alone.

### C. Live prices shown to everyone — buy the cheap delayed licence, skip real-time
This is redistribution and needs NSE Data & Analytics. From NSE's published domestic price list (effective **1 April 2026**):

| Product | Cost |
|---|---|
| Real-time Level 1, open website | ₹29.2L / year per website; mobile ₹23.45L / year per app |
| Real-time via data-vendor route | ₹25.5L fixed + ₹875–1,145 per domestic user per month |
| Snapshot, 1-minute | ₹16L / year per medium |
| Snapshot, 5-minute | ₹4.2L / year per medium |
| **Snapshot, 1-minute, 15-minute delayed** | **₹1.2L / year per medium** |
| **End-of-day data (Capital Market)** | **₹1L / year per site, per medium** |

- **Recommendation:** 15-minute delayed at ₹1.2L per medium — web plus app is about **₹2.4L a year (~$2.5K)**. Cheap, and enough for a research product. Real-time at ₹25L+ is a Series A decision, not a pre-seed one.
- **The EOD flag (correction to my own earlier wording):** an earlier provenance memo said bhavcopy-based prices carry no licensing dependency; the retained memo no longer makes that claim. NSE lists EOD data as a *paid* product for display, ₹1L per medium per year. Whether displaying bhavcopy-derived prices needs it is for NSE to confirm in writing (marketdata@nse.co.in). At ₹2L a year the safe move is probably to buy it — then reword the memo. **Do not send the provenance memo to Rainmatter until this is settled.**
- BSE pricing is not researched here; it is blocked in practice anyway.
- Vendor resale (e.g. authorised data vendors) is the alternative to a direct licence. I did not price vendors; get two quotes before choosing.

---

## 3. Broker sign-in and portfolio fetch

**Principle:** official OAuth-style login only, read-only scope, tokens encrypted at rest, one adapter per broker behind the existing `BrokerClient` interface.

| Step | Action |
|---|---|
| 1 | **Remove the `enctoken` path** from `broker_service.py` / `zerodha_unofficial.py`. No pasted session tokens, ever. |
| 2 | Get **Kite Connect keys configured** for production, then request multi-user access from Zerodha. |
| 3 | Replace Groww's paste-a-token with whatever official login flow Groww offers; until then label it clearly as manual. |
| 4 | Add **Upstox and Dhan** directly — both publish free APIs with a standard login flow, so they are quick to add. |
| 5 | Evaluate **smallcase Gateway** as the broad route (see §4) — one integration reaching 19 brokers including Kite, Upstox, Angel One, Dhan, Groww, ICICI, HDFC and Kotak. |

Read-only holdings sync does not trigger the algo framework. This whole section is low-regulatory-risk and is what unlocks portfolio-aware answers, the digest, X-ray and tax (see the customer-workflow hypotheses in `GTM_PLAN.md`).

---

## 4. Placing orders — what stands in the way

Three independent gates. All three must clear for direct execution.

**Gate 1 — SEBI's retail algo framework (full effect 1 April 2026).** API orders must come from a registered app ID bound to a **whitelisted static IP**, carry an exchange-issued **Algo-ID**, and third-party algo providers must be **empanelled via a trading member**. Providers operating through a broker's API are treated as the broker's agent, and open APIs are not permitted — access is by vendor-specific key and static IP. Production today runs on a Mac behind a Cloudflare tunnel, with no static IP.

**Gate 2 — your research posture.** Anvest is not yet a registered Research Analyst. A research answer sitting next to an order ticket invites "advice" treatment. SEBI's RA rules also segregate research from distribution (Reg. 26C). **Rule to follow: earn nothing per order** — no brokerage share, no referral per trade — and monetise only through subscriptions. Counsel to confirm.

**Gate 3 — broker access.** Kite's order-placement APIs have been free since March 2025, but multi-user platforms need Zerodha's approval. Note **Kite MCP is read-only, with GTT orders as the sole exception** — the "AI assistant places orders" story is not available through it today, which matters for how hard you lean on it in the integration pitch.

### The path I recommend: let the user's own broker session place the order

| Phase | Mechanism | When |
|---|---|---|
| **A — hand-off** | "Act on this" opens the user's broker with the instrument prefilled; the user confirms inside the broker's own app. Anvest never sends an order. | With the broker sign-in work |
| **B — smallcase Gateway** | User-initiated transactions through an aggregator that already has the broker integrations and compliance. Each action needs the user's own login — it **cannot place server-to-server orders on a user's behalf**, which is precisely what keeps you out of algo-provider territory. Moneycontrol and Kuvera use it. Commercial terms are not public; negotiate. | After RA registration and counsel sign-off |
| **C — direct integration** | A partnership with a broker (the Zerodha/Rainmatter route in `FUNDING_PLAN.md`), under their empanelment. Needs static-IP infra off the Mac, RA registration, and a legal structure. | H2, funded by the seed — not this round |

Phase B is the realistic "place orders inside Anvest" answer for the next 12 months. Phase C is the destination, and it is correctly an H2 story.

---

## 5. Phased plan

| Phase | When | Work | Cash cost | Gate |
|---|---|---|---|---|
| **0 — no-regret** | Now → 16 Oct | Kill `enctoken`; confirm what prod runs for Kite; ask NSE about EOD licence; decide BSE stance | ~0 | Do before any Zerodha conversation |
| **1 — live filings + real login** | Oct → Nov | Intraday NSE announcements, holdings-triggered alerts; official Kite/Upstox/Dhan login; Kite multi-user request | ~0 (+ ₹500/mo Kite) | BSE decision by 1 Dec |
| **2 — live prices** | Nov → Jan | Per-session live portfolio quotes; 15-min delayed licence for public pages; EOD licence if NSE says so | ~₹2–5L / year | Licence signed |
| **3 — act on research** | After RA registration | Order hand-off (A), then smallcase Gateway (B) | Gateway terms TBD | RA registered + counsel opinion |
| **4 — direct execution** | H2 | Broker partnership, static-IP infra, empanelment | Seed-funded | Rainmatter / Zerodha conversation |

**Sequencing logic:** each phase is useful on its own and none depends on the next. If the round slips, Phases 0–2 still ship and cost almost nothing.

---

## 6. What this changes in the pitch

- **Say:** *"End-of-day prices today; live filings and live portfolio next quarter; execution routed through the user's own broker, with a partnership route funded by the seed."* It matches the deck's horizons and cannot be caught out.
- **Don't say** "real-time" anywhere until Phase 2 has shipped, and don't promise order placement inside the 18-month plan.
- **Strategic deck, slide 5:** keep the Kite MCP hook but don't imply it places orders — it doesn't.
- **A new concrete ask for Rainmatter:** multi-user Kite Connect access. It converts a vague "integration" conversation into something Zerodha can say yes to in a week.

---

## 7. Decisions needed from you

1. **Remove the `enctoken` path now?** (Recommended: yes. Any user who already connected through it needs a clear re-connect notice.)
2. **BSE:** accept NSE-only intraday announcements, or pursue an authorised BSE route, before 1 Dec?
3. **NSE:** write to marketdata@nse.co.in to confirm whether EOD display needs the ₹1L licence, and buy it if so.
4. **Is Kite Connect configured in production?** I could not tell from the files I can read; the answer decides whether the Zerodha flow is official or the scraper.
5. **Execution scope:** are you comfortable with "hand-off now, Gateway after RA registration, direct in H2" as the public line?

---

### Sources
- NSE Data & Analytics, *Market Data Pricing – Domestic*, effective 1 April 2026: nsearchives.nseindia.com (NSE_Pricing_file_-_Domestic_clients_20260309171343.pdf)
- SEBI retail algo framework and 1 April 2026 timeline: Business Standard (30 Sep 2025), Upstox news, Fyers community blog, SEBI circular SEBI/HO/MIRSD/MIRSD-PoD/P/CIR/2025/0000013 as quoted by third parties
- Kite Connect pricing and multi-user access: Zerodha support and kite.trade developer forum
- Kite MCP scope (read-only except GTT): Zerodha Z-Connect and support pages
- smallcase Gateway behaviour and supported brokers: developers.gateway.smallcase.com
- RA Regulation 26C segregation: SEBI RA regulations commentary (KS&K, Enterslice, LKS)
- Code facts: `data-platform/app/integrations/*`, `broker-portfolio/broker_portfolio/services/broker_service.py`, `ops/docs/DEPLOY_ON_MAC.md`
