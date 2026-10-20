# Outreach research notes and corrections

**Internal · 20 Oct 2026.** Publication checks only. No SMTP test, email send, application submission, private address enrichment or contact-provider purchase was performed. Rankings reflect stage, thesis, round size and access, not guessed funding probabilities.

## Corrected in this refresh

- The old workbook was a September plan under an October filename. It used a $400K headline, unsupported user/traction assumptions, grouped several unrelated funds into one row, had no contact columns and ranked by guessed probability. It now uses the $500K target and individual records with provenance.
- `Round Model` mislabeled USD amounts as rupees, computed monthly burn in USD under an INR label and implied founder ownership as one minus dilution. It now labels currencies explicitly, reconciles target allocations and requires a verified cap table rather than inferring one.
- Arbitrary MAU/revenue/retention hurdles no longer block all outreach. Official early-stage mandates support approaching several funds pre-revenue. Current usage evidence is dated and includes founder/testing.
- Antler is no longer categorically excluded as residency-only: its current India site offers a Direct route. Full-time and program requirements still require confirmation for the chosen track. [Source](https://www.antler.co/location/india).
- LetsVenture's founder page redirects to LVX. AngelList India and Backrr are treated as platforms rather than promised cheques. The US AngelList startup sales form expressly does not accept funding applications. [LVX](https://www.letsventure.com/founders), [AngelList India](https://www.angellistindia.com/), [US sales form](https://www.angellist.com/contact/startups), [Backrr](https://backrr.com/startup).
- Professional/creator categories are preserved as prospecting pools, not counted as named investors. No cheque, follower count, warm connection, founder ownership or ongoing pilot is invented.

## Open contact and mandate questions

| Entry | Observation | Practical next step |
|---|---|---|
| Gemba | Search-indexed `team.php` returned 404. Current `partner.php` visibly invites founders through info@gembacapital.in. Legacy team emails also remain in HTML; that alone does not establish a current role. | Use the visible current founder inbox. Old named-team suggestions were not carried into the send list. [Current source](https://gembacapital.in/partner.php). |
| All In | Homepage publishes $250K–$600K while application FAQ says $250K–$500K. | Confirm current range rather than choosing the larger figure. [Homepage](https://www.allincapital.vc/), [FAQ](https://www.allincapital.vc/apply_now). |
| First Cheque | Homepage says up to $500K; FAQ still says standard ₹75L. Older duplicate site pages contain different fixed ownership terms. | Ask current cheque and terms. Do not state a fixed 5% offer. Distinct from firstcheques.com. [Current site](https://www.firstcheque.vc/). |
| India Quotient | Official FAQ links a Google form; research fetch returned 401. The site publishes a firstname email convention, not a verified named recipient. | Try official form signed in; if blocked, use official team/social route. No guessed email recorded. [Source](https://www.indiaquotient.in/). |
| Rainmatter / Zeropearl | Official sites link application forms, but provider redirects could not be fetched by the research browser. | Open via the official site before submitting. Published route is verified; completed submission is not. [Rainmatter](https://rainmatter.com/), [Zeropearl](https://zeropearl.vc/). |
| Huddle India | Official site HTML loaded with Apply now link; research browser returned 403. | Open form from huddle.work and verify current fit. Do not use unrelated huddleventures.co or Huddle collaboration-software contacts. [Source](https://huddle.work/). |
| Axilor | Homepage/contact returned 520; cached official pages describe a seed fund. | Confirm current seed intake via restored site or genuine introduction. Old accelerator amounts/duration not reused. [Official source](https://www.axilor.com/category/axilor/). |
| Accel Atoms | Current homepage offers future-cohort notification, not a visible open application. | Confirm intake or use genuine India-team introduction; do not label newsletter signup a funding application. [Source](https://atoms.accel.com/). |
| Mumbai Angels | Official LinkedIn says the page is winding down into 360 ONE Asset. Old pitch post contains pitch@mumbaiangels.com; current About text has `.con` typo. | Verify the current parent-team funding route before using legacy mailbox. No address silently corrected and marked current. [Official page](https://www.linkedin.com/company/mumbaiangels/). |
| 100X.VC | Pitch address is in older founder posts; current homepage no longer exposes it or current class terms. | Short intake enquiry first; confirm current cheque, terms and process. [Founder post](https://www.linkedin.com/posts/mehta-sanjay_email-details-to-pitch100xvc-activity-6824043496412852224-bK6o), [current site](https://www.100x.vc/). |
| Better Capital | Day-zero thesis and official LinkedIn link verified; no suitable public pitch email found. | Use genuine referral or officially linked profile. Avoid guessed betterlabs inboxes and unrelated UK Better Capital fund. [Source](https://www.bettercapital.vc/). |
| Blume | Official FAQ has stage/revenue guidance, prefers individual investor contact and says common pitch inbox/form removed. | Lower priority; find genuine intro or verified individual public contact, not LP/media/finance inbox. [Source](https://blume.vc/). |
| BoldCap / Neon / FortyTwo | Current theses emphasize frontier AI or global enterprise markets; Anvest currently has an India professional-research wedge. | Treat fit as conditional; do not invent frontier-model work or contracted overseas demand. [BoldCap](https://www.boldcap.com/), [Neon](https://neon.fund/fund-application-page/), [FortyTwo](https://www.fortytwo.vc/). |
| Personal angels / Groww | Suitable direct emails and current personal mandates were not verified for Kunal Shah, Ramakant Sharma, Nikhil Kamath or Lalit Keshre. | Named introductions needed; do not route personal funding asks to company customer support. Nithin/Rainmatter and Sanjay/Prime are coordinated routes rather than duplicate leads. |

## Remaining business evidence gaps

Actual cap table, signed founder IP assignment, employment/IP clearance, notice period and exact financing instrument are not verified by this contact refresh. The old tracker is not evidence of these facts. Establish these from actual documents for diligence; do not let unknowns turn into claims in pitch emails.

The later 20 October 12:51 IST audit identifies 26 external accounts, 15 with a recorded workflow and five active in at least two IST calendar weeks. External research has 268 rows across 13 users; seven have at least two research rows. These are historical activity definitions, not cohort D7/D30 retention. Aggregate totals include founder/testing and many stored backtests have no owner; attempts and failures are not logged, so a success rate cannot be calculated. Current demo/data status is in `../Internal_Strategy/PRODUCT_DATA_BUG_BACKLOG_2026-10-20.md`; this research did not deploy or certify product fixes.

## Newly found material discrepancy — fix before PDF attachment

The later product audit recounts **6,155,194 passages** and **633,688 distinct doc_ids** on the production VM (20 Oct, about 12:50 IST). Both current deck masters still contain **1.35M passages**. The backlog's DATA-06 records this discrepancy and the approximately 584K filing figure as stale. The exact passage count is established; the distinct-doc facet result has a different counting method and should be described with its scope. `Source/product_metrics.py` and its frozen snapshot document that method.

Reconcile seed/partner decks, one-pager, provenance memo and their exports before attaching them. The deck masters and exports already had uncommitted changes from another session when outreach work began, so this refresh preserves those files and records the concrete required correction here and in the tracker. Intro requests and contact preparation can proceed immediately; the draft attachment instruction is conditional on correction. No screenshots were created or changed.

Validation also found the seed PDF older than its PowerPoint master. The full materials checker therefore remains red for that export; the separate outreach consistency check passes. Re-export the corrected master and rerun the full check before attachment. This refresh does not claim the PDFs are send-ready.

The same later audit records **BUG-01–04 closed on production** with dated replay evidence. Outstanding product items include a roughly 38-second cold backtest and the virtual-cash-added tile after withdrawals (source fix not deployed). Do not repeat the older blanket claim that all four broker fixes await release.
