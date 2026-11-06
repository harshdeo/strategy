# Material sources and evidence

## Decks
`deck/` builds both `.pptx` masters from scratch. `seed.js` and `partner.js` hold the slide content, `lib.js` the house style, and `finish_deck.py` adds the founder's flow screenshots (bytes in `deck/img_flow`, crops and positions in `deck/flow_images.json`, never edited), the native charts and the document properties.

```bash
export NODE_MODULES_DIR=<folder with pptxgenjs> PY_LIBS=<folder with python-pptx>
Source/deck/build.sh                 # model.json, seed.pptx, partner.pptx
Source/deck/render.sh seed           # Keynote PDF and page images
Source/deck/render.sh partner
/opt/homebrew/bin/python3 Source/deck/install.py   # copies masters and PDFs to Investor_Materials
```

`capture_public.mjs` and `capture_tiles.mjs` take the signed-out product screenshots. Earlier patching scripts are in `Archive/2026-11-01_superseded_build/`.

## Documents
`render_documents.py` fills `onepager.html` from the operating model and prints it and `provenance.html` to PDF, then sets the PDF properties.

## Evidence
Never replace a cited result. Write a new dated file.

- `analytics_snapshot_20261101.json`: Vercel Web Analytics figures behind the traction page, with the definition of a visitor.
- `product_metrics_snapshot.json`: read-only production aggregates, 20 Oct 2026. `product_metrics_20261101.py` takes a new dated snapshot; the run needs the owner's approval because it reads production.
- `evidence_snapshot.json`, `filing_selection.json`, `filing_check.json`: the 50-filing source audit. It tests extraction, not AI answers.
- `GOLDEN_EVALUATION_BENCHMARK.md`: the proposed 50-question evaluation. It has not been run.
- `update_outreach.mjs` refreshes the outreach tracker; `check_materials.py --outreach` checks it.

## Checks
`../check_materials.py` must print PASS. It reconciles every material with the model, rejects stale or unsupported claims and bad PDF properties, and runs `style_audit.py`, a plain-language lint. The lint does not detect AI authorship.

Nothing here authorises publication, model calls, warehouse writes or a production deploy.
