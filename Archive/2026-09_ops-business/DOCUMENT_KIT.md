# Anvest — Seed Round Document Kit

> **Revised 2026-09-03, post-YC-rejection.** Terms repriced and all YC references removed. See FUNDING_PLAN.md §7.1 for why.

One checklist, every document, who gets what. Terms are identical everywhere — **$3.5M fixed post-money cap, $400K base raise (11.4%) upsizable to $700K (20%)**, CCD/CCPS or post-money SAFE, ~2% non-cash advisor equity. Only the **narrative** changes by audience (FUNDING_PLAN.md §7.4). Full investor-by-investor detail lives in `Anvest_Investor_Tracker.xlsx` → "Investor Targets" sheet; this file is the document map, not the target list.

---

## 1. Built and ready to send

| Document | File | Covers | Placeholder-ready? |
|---|---|---|---|
| Baseline pitch deck (Narrative A — platform story) | `Anvest_PreSeed_Deck.pptx` | Problem, product, moat, traction, GTM, horizons (incl. the broker/algo/all-in-one ambition), the ask | Yes — no investor name in the deck itself; the email carries the name |
| Strategic integration deck (Narrative B — integration story) | `Anvest_Strategic_Integration_Deck.pptx` | Same product, reframed around Kite Connect/Kite MCP, the Tickertape-overlap objection answered head-on, same $3.5M terms | Yes for Rainmatter/Zerodha. Use only slides 1–8 in a Groww conversation (see §3) |
| One-pager | `Anvest_OnePager.pdf` | One-page leave-behind: snapshot, problem, product, moat, shipped/not-yet, horizons, ask | Yes — `[INVESTOR / FIRM NAME]` is the one field to swap before sending |
| Data provenance memo | `Anvest_Data_Provenance_Memo.pdf` | Where the data comes from, update cadence, grounding architecture, disclosed gaps, **honest current status of the ratio-verification work** (in progress, not certified), regulatory posture | Yes, universal — no investor-specific content |
| Cold outreach emails | `COLD_EMAILS.md` | Template A (generalist), Template B (Rainmatter/Zerodha), Template C (Groww, BD-toned) | Yes — `[FIRST NAME]` and one optional personalization line per template |
| Investor tracker | `Anvest_Investor_Tracker.xlsx` | Target list, priority order, status tracking, round-model math (consistent with the $3.5M cap throughout) | N/A — internal, not sent to investors |

All six live in this folder now. Nothing above needs to be rebuilt per-investor — only the salutation and the one bracketed field.

---

## 2. Who gets what

| Investor | Deck | One-pager | Provenance memo | Email template |
|---|---|---|---|---|
| Tier 1 micro-VCs (Titan, Sparrow, All In, Better, Gemba, Peer, Whiteboard, Inuka, Zeropearl, OTP) and AI-lane funds | `Anvest_PreSeed_Deck.pptx` | Yes | Yes, if diligence gets technical | Template A |
| Angels (RAs, operator angels, Kunal Shah, creators) | `Anvest_PreSeed_Deck.pptx` | Yes | On request | Template A |
| Syndicates (LetsVenture, Mumbai Angels, AngelList India) | `Anvest_PreSeed_Deck.pptx` + one-pager only (syndicate platforms rarely want the full deck in a cold submission) | Yes | On request | Template A, adapted to the platform's own intake form |
| Rainmatter (Zerodha) | `Anvest_Strategic_Integration_Deck.pptx` | Yes | Yes — brokers' diligence will ask about data provenance regardless | Template B |
| Nithin/Nikhil Kamath (personal angel route) | `Anvest_Strategic_Integration_Deck.pptx` | Yes | Yes | Template B — coordinate as one thread with Rainmatter, not two |
| Groww / Lalit Keshre | `Anvest_Strategic_Integration_Deck.pptx`, **slides 1–8 only** (drop the equity ask on slide 9 and close on slide 10 unless the conversation gets there on its own) | **Hold back** until there's a live conversation | Hold back | Template C |
| Tier 3 institutional (Lightspeed, Accel, Bertelsmann, Peak XV, Elevation/Z47/Prime/Blume) | `Anvest_PreSeed_Deck.pptx` | Yes | No — this is a relationship meeting, not a raise pitch (FUNDING_PLAN.md §8) | Not cold email — warm intro only, framed as "not raising" |
| YC (Winter 2027, *if* the revenue gate is met by 2 Nov) | N/A — see `YC_APPLICATION_FALL2026.md`, now an answer bank rather than a live application | N/A | N/A | N/A — this track doesn't use this kit |

---

## 3. The one rule that keeps this from becoming a mess

Every investor above gets the **same $3.5M cap, same $400K–$700K range**. What changes is which deck they see and which parts of it get emphasized. Never let a conversation drift into a different number for a different investor — that's the fastest way to blow up diligence later when two term sheets get compared. If an investor pushes on the cap, the answer is the same regardless of who's asking: it's fixed, it's the same for everyone in this round, and it's justified by what's in FUNDING_PLAN.md §7.0–§7.1 (the depth built solo, the category comparables, and for strategics, the integration thesis). **The YC application is no longer part of that justification and must not be mentioned** — see §9.

---

## 4. Not built here, and why

| Document | Status | When it's actually needed |
|---|---|---|
| SAFE / CCD legal instrument (the actual convertible note text) | **Not drafted.** This needs a lawyer, not a template — get one who's done Indian CCD/CCPS conversions before, not a generic SAFE. | Once an investor is ready to commit, not before. Drafting this without counsel risks getting the India-specific mechanics (CCD vs CCPS, FEMA/pricing-guideline compliance for a capped instrument) wrong in a way that's expensive to unwind. |
| Data room (cap table, incorporation docs, IP assignment, financials) | Tracked separately — `Anvest_Investor_Tracker.xlsx` → "DO THIS NEXT" #39 "Assemble the data room." The IP-assignment and cap-table-cleanup items (#1–#2) block this and are already flagged NOW-priority. | Due diligence stage, once an investor is seriously engaged — not sent cold. |
| Pitch deck for Tier 3 relationship meetings | Reuse `Anvest_PreSeed_Deck.pptx` as-is; these are explicitly framed as "not raising," so no separate deck is warranted. | N/A |

---

## 5. Sending checklist, per investor

1. Confirm the correct row in `Anvest_Investor_Tracker.xlsx` → Investor Targets, and which template/deck it points to (columns G/H/O now carry this for Rainmatter, Kamath, and Groww specifically).
2. Swap the bracketed placeholders in the email template.
3. Attach the deck + one-pager per the table in §2 (provenance memo only if the thread already exists or the investor is technical/broker-affiliated).
4. Log the send in the tracker's Status/Owner/Notes columns before moving to the next name.
5. Follow the cadence at the bottom of `COLD_EMAILS.md` — one bump at day 7, then log and move on.

---

## 6. Post-rejection status of each document (2026-09-03)

| Document | State | Action needed before sending |
|---|---|---|
| `COLD_EMAILS.md` | **Updated** — repriced, YC scrubbed, Template D (relationship-only) added | Fill `[N]` users / `[M]` seats |
| `DOCUMENT_KIT.md` | **Updated** — this file | — |
| `Anvest_Investor_Tracker.xlsx` | **Updated** — targets re-ranked by probability, checklist re-sequenced, round model repriced | — |
| `Anvest_Data_Provenance_Memo.pdf` | Still accurate — no YC or valuation content in it | — |
| `Anvest_OnePager.pdf` | **Stale** — shows $5.0M/$500K and a YC line | Regenerate before sending |
| `Anvest_PreSeed_Deck.pptx` | **Stale on three slides** — ask slide (old terms), slide 6 ("zero users"), slide 5 ("nobody in the middle" — Screener now is) | Rebuild once there are real traction numbers; tracked in the checklist PREP band |
| `Anvest_Strategic_Integration_Deck.pptx` | **Stale on the ask slide only** | Update terms before sending to Rainmatter |

**Do not send the decks until the PREP band items are done.** A deck quoting $5.0M against an email quoting $3.5M is the one mistake in this kit that cannot be walked back.
