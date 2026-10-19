# Anvest — Brand Reference

**Reusable assets, organised 14 October 2026.**

Use the current seed deck (`../Investor_Materials/Anvest_Seed_Deck.pptx`) as the visual reference for layouts and pitch content. The earlier `Anvest_Brand_Template.pptx` is in `../Archive/2026-10-19_superseded/`; its sample figures are not current business facts.

## Assets in this folder

- `Anvest_Brand_Background_Hero.png`: title and closing backgrounds.
- `Anvest_Brand_Background_Dark.png`: dark content backgrounds.
- `Anvest_Brand_Background_Light.png`: light document or appendix backgrounds.

## Palette and type

| Use | Colour |
|---|---|
| Ink | #0B0E26 |
| Navy | #1E2761 |
| Violet | #4A3699 |
| Amber accent | #F5A623 |
| Light body text | #C9D3F0 |
| Muted text | #7C88B0 |
| Slate body text | #434B6B |
| Light background | #F4F7FC |

The 19 October decks use Arial for display and Calibri for body text on a 16:9 canvas, with left-aligned text. They follow a sandwich structure: Hero and Dark backgrounds for the cover, "why now", moat, algo, ask and closing slides, and the Light background for content. Violet carries numbers and icons on light slides, and amber is reserved for dark slides and highlights; amber text on white fails contrast. Product screenshots sit in a dark browser-window frame. Body text stays at 12–16pt and numbers at 20–44pt. Charts must be native PowerPoint charts preserved as native editable objects; Keynote does not render pptxgenjs charts. Keynote drops all data labels in a chart series when single labels are deleted, so hide small segment labels with a number format such as `[<1]"";"₹"0.0`. Avoid symbol glyphs such as ●◐○ in tables, because the PDF export can drop them; use text labels. Every slide footer carries the date ("20 Oct 2026"). Keep internal draft numbers out of investor copies. Preserve editable content and check for wrapping or overlap after changes.

The obsolete deck generators have been removed from this working folder because they rebuild earlier claims and pitch terms. The dated cleanup snapshot in Trash retains the original authoring files if they are needed later. Edit current presentations directly using the current content rather than rerunning those old generators.
