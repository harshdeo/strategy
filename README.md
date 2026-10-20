# Anvest Strategy — File Guide

**Organised by use case, 14 October 2026. Current investor materials: 20 Oct 2026.**

## Folder map

| Folder | Purpose | Contents |
|---|---|---|
| [Investor_Materials](Investor_Materials/) | Presenting the company and supporting diligence | Seed deck and partner deck (editable `.pptx` and send-ready `.pdf`), one-pager and provenance memo |
| [Outreach](Outreach/) | Preparing messages and tracking conversations | Email templates and investor tracker |
| [Internal_Strategy](Internal_Strategy/) | Deciding what to fund, sell and prioritise | Pitch review, funding plan, GTM plan, investor targeting/Q&A and broker/data strategy |
| [Financial_Models](Financial_Models/) | Revenue, cost and runway | Monthly operating model (`.py` plus a generated `.xlsx`) and the dated pricing and unit-economics reference |
| [Source](Source/) | Rebuilding and auditing materials | Document templates, unchanged source screenshot, read-only metric queries, source audit, deck patcher and export scripts |
| [Brand](Brand/) | Reusing Anvest's visual identity | Brand guide and three backgrounds |
| [Archive](Archive/) | Superseded files, never sent | 14 October originals, external review files, superseded calculators, the old brand template and a Keynote duplicate |
| [check_materials.py](check_materials.py) | Consistency check | Confirms every material matches the operating model and carries one version label |

## Investor and partner materials

| File | Use |
|---|---|
| [Seed deck](Investor_Materials/Anvest_Seed_Deck.pptx) ([PDF](Investor_Materials/Anvest_Seed_Deck.pdf)) | Seed pitch: 16 main slides and 5 appendix slides, with speaker notes. "India's AI research co-pilot": problem, solution (the founder's flow slide), product, traction, why now, market, task-based competition, moat, business model, go-to-market, future of trading, financial plan, team, the $500K ask and close |
| [Strategic integration deck](Investor_Materials/Anvest_Strategic_Integration_Deck.pptx) ([PDF](Investor_Materials/Anvest_Strategic_Integration_Deck.pdf)) | Scoped read-only broker pilot (no equity). The cover, slide 4 and the closing slide are Zerodha/Kite-specific |
| [One-pager](Investor_Materials/Anvest_OnePager.pdf) | Investor overview to attach to the first email |
| [Data provenance memo](Investor_Materials/Anvest_Data_Provenance_Memo.pdf) | Diligence memo, on request |

The `.pptx` files are the editable masters, with speaker notes. The `.pdf` files are the copies to send: they render the same everywhere and leave out the notes. Each PDF carries the same version label as its master.

The story in one line: **India's AI research co-pilot: cited filing answers, costed backtests and portfolio impact, for SEBI-registered professionals and serious investors.** Desk seats and partner API/MCP licences carry this round; retail subscriptions are self-serve upside. The ask leads with $500K (first close $400K, room to $700K). Exchange-registered strategies belong to the long-term scenario, after approvals. ITR is deliberately left out while it is in progress.

## Working documents

- Use the [product and data bug backlog](Internal_Strategy/PRODUCT_DATA_BUG_BACKLOG_2026-10-20.md) for separate follow-up. Each issue records evidence, status and what closes it; the [correction register](Internal_Strategy/ISSUES_AND_FIXES_2026-10-20.md) lists fixes already made in the investor-materials task.

- Read the [pitch review](Internal_Strategy/PITCH_REVIEW_2026-10-19.md) first. It covers the objective, the evidence behind each claim, the competitor sources, what is verified and what is not, the model, and the checklist to complete before sending.
- [operating_model.py](Financial_Models/operating_model.py) is the single source for every revenue, cost, runway and market-size figure. Run it for a summary; run it with `--xlsx` to regenerate [Anvest_Operating_Model.xlsx](Financial_Models/Anvest_Operating_Model.xlsx). The [pricing reference](Financial_Models/PRICING_AND_UNIT_ECONOMICS.md) is the dated tier-design and unit-cost analysis.
- Use the [funding plan](Internal_Strategy/FUNDING_PLAN.md), [GTM plan](Internal_Strategy/GTM_PLAN.md) and [targeting plan](Internal_Strategy/INVESTOR_TARGETING_PLAN.md) for priorities and diligence preparation.
- The [broker/data strategy](Internal_Strategy/LIVE_DATA_AND_BROKER_STRATEGY.md) preserves a dated 9 October audit; it is not a fresh production certification.
- Prepare personalised messages with the [email templates](Outreach/Anvest_Outreach_Emails.md), and log conversations in the [investor tracker](Outreach/Anvest_Investor_Tracker.xlsx).
- The [brand guide](Brand/BRAND_GUIDE.md) maps the palette and backgrounds; the current seed deck is the visual reference.

## After any change

1. Update the model inputs or the `.pptx` master. Keep the date consistent in every footer; internal draft identifiers never appear in materials sent to investors.
2. Re-export each changed deck to PDF (PowerPoint or Keynote: File → Export → PDF).
3. Run the check; it must print PASS:

```bash
/opt/homebrew/bin/python3 /Users/harsh/anvest/Strategy/check_materials.py
```

This folder is its own git repository (split out of `ops/business/Strategy` on 20 October 2026; the earlier history stays in `ops`). After edits, commit here: `git add <your files> && git commit`. A deck's `.pptx` master and its exported `.pdf` go in the same commit. There is no remote yet; pushing remains a separate decision. Agent rules are in [CLAUDE.md](CLAUDE.md).

## Before sending

Send the PDFs, not the .pptx files. Complete the "Verify before sending" checklist in the pitch review: the user count, the vendor pages and the launch-pricing labels. Fill in every email placeholder and the partner name, and adapt the Zerodha-specific partner slides for other brokers. Keep the tracker, strategy documents and financial models internal; share the operating-model workbook only in a data room.
