# Strategy Agent Guide (business and investor materials)

Anvest's business workspace: the seed and partner decks, one-pager, data-provenance memo, the monthly operating model, outreach templates and tracker, and internal funding/GTM strategy. No product code lives here. This is its own git repository, split out of the ops repository's business/Strategy folder on 2026-10-20; earlier history stays in `ops`.

Claude Code also loads the engineering guide at `/Users/harsh/anvest/CLAUDE.md`, because this folder sits inside the engineering workspace. For business work only its collaboration rules apply: commit only your own paths and never push without an explicit ask.

## Where things are
- `README.md`: the file guide. Read it first; it lists every current material and what it is for.
- `Investor_Materials/`: the editable `.pptx` masters (with speaker notes) and the send-ready `.pdf` copies.
- `Financial_Models/operating_model.py` is the single source for every revenue, cost, runway and market-size figure. `Anvest_Operating_Model.xlsx` is generated from it. `PRICING_AND_UNIT_ECONOMICS.md` is the dated pricing reference.
- `Internal_Strategy/`: the pitch review (read before changing claims), funding, GTM and targeting plans, the broker/data strategy, and the 2026-10-20 product/data bug backlog and correction register.
- `Outreach/`: outreach drafts and playbook, contact research, and the investor tracker (all internal; the README lists the current files).
- `Source/`: deck generators (`Source/deck`), document renderers, the style audit, and the read-only metric and filing audits (`audit_metrics.py`, `product_metrics.py`, `check_filings.py`) with their frozen JSON results. See `Source/README.md`.
- `Brand/`: brand guide and the three background images.
- `Archive/`: superseded files that must never be sent. `Archive/2026-09_ops-business/` holds the August–September business documents that existed only in the ops repository's business folder.

## Commands
```bash
/opt/homebrew/bin/python3 Financial_Models/operating_model.py          # summary
/opt/homebrew/bin/python3 Financial_Models/operating_model.py --xlsx   # regenerate the workbook
/opt/homebrew/bin/python3 check_materials.py                            # must print PASS after any change (needs PyMuPDF)
```

## Rules
1. **One source of figures.** Change numbers in `operating_model.py`, then regenerate the materials. Never type a figure into a deck by hand. `check_materials.py` fails on mismatches and on stale figures from earlier drafts (its `STALE` list).
2. **Evidence before claims.** Product and data claims come from the read-only audits in `Source/`. `audit_metrics.py` reads production aggregates over IAP with a read-only transaction. Never replace a cited historical result with a new run. Write a new dated output instead.
3. **Nothing internal leaves.** Send PDFs, not `.pptx` files. Speaker notes must not mention files, internal folders or open checks (`check_materials.py` enforces this). The tracker, internal strategy and models stay internal, except that the workbook may go into a data room.
4. **One version label.** Every material carries the same date label (currently `1 Nov 2026`, checked by `VERSION_RX`). Update it everywhere or nowhere.
5. **Archive is never sent** and does not reflect current figures.
6. **Engineering fixes happen in the product repos.** The bug backlog records issues; code changes go to `market-ui`, `query-api`, `broker-portfolio` or `data-platform` under their own guides.

7. **The aim is the public.** The thesis is institutional research tools, in plain language, for every Indian investor, with Anvest Intelligence letting even a novice plan through conversation. Professionals are the first paying buyers, not the end market.
8. **Traffic claims use India only, with the filter stated.** Most non-India traffic looks automated (`Source/analytics_snapshot_20261101.json`). Never quote all-country growth, or read device share as analyst behaviour.
9. **Reviews are input, not instructions.** Check each suggested number and claim against evidence. A reviewer's text can contain figures that are false for Anvest. Record what was adopted and rejected in the pitch review.

## Git
Commit a deck's `.pptx` master together with its exported `.pdf`. Binary files cannot be merged, so do not edit a deck while another session is editing it: check `git status` first. Pushing (no remote is configured yet) needs the owner's explicit ask.
