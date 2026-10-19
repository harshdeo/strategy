# Issues found and fixed, 20 October 2026

For separate product/data work, use the [bug and data-issue backlog](PRODUCT_DATA_BUG_BACKLOG_2026-10-20.md). It distinguishes confirmed bugs, investigations, mitigations and already shipped fixes.

| Issue | Resolution | Remaining limit |
|---|---|---|
| TCS net-margin denominator was unclear; repeated company/period header; omitted YoY basis-point change | Captions define PAT / total income; broker code names denominator, computes −67 bps and uses one header | Local response-code fix is not deployed. The real 19 October screenshot is preserved. |
| ~17K monthly filing volume used old ingestion dates | Replaced with Q2 FY27 announcement-date counts: Jul 45,997, Aug 61,875, Sep 38,558, average 48,810/month | Announcement records, not a deduplicated PDF count |
| Four-query spot-check was oversized as traction proof | 50/50 original NSE XBRL checks for revenue/PAT, with sample, currency, context, source hashes and fail-closed checker | Extraction check, not a fifty-answer AI benchmark |
| 6,137 pages were described as all having AI profiles | 6K+ page/coverage framing; 6,119 distinct non-empty warehouse AI profiles, with scope stated | Current dashboard scope is 6,086 symbols |
| ~100 sign-ups lacked evidence | 31 production accounts; 418 queries across 16 accounts; 238 saved backtests; 2 saved screens | Includes founder/testing; does not measure external retention or paying demand |
| Year-5 Desk demand implied 19% of initial professional seats | Added broader distributor, family-office and CA/wealth expansion in Years 3–5 | Sales expansion remains an assumption |
| Financial title mixed no-funding and Series A paths | Explicit default-alive M42 case versus separate Series A scale scenario | Both depend on planning assumptions |
| Scale model added sellers without salaries | Added every scenario seller salary and increased scale marketing | No specified Series A proceeds are added to cash |
| Scale model changed partner growth before the round's funded period ended | Target and scenario now match exactly through M18; later growth changes at M19 | Detailed Year-5 ARR becomes ₹23.11 Cr, shown as ~₹23 Cr. Rounded mix ₹13.4 Cr + ₹9.7 Cr = ₹23.1 Cr |
| Draft labels, exclusivity and zero-CAC claims added no evidence | Removed from current investor materials and active narrative; team workspaces marked planned | Historical archives remain unchanged |
| Negative chart-axis ids and missing master overrides could break import | Repaired package metadata while preserving native chart/table objects and screenshot bytes | Native PowerPoint application behavior was not tested |
| Strategy had no Git recovery and document source lived in a temporary folder | Added Strategy snapshot mapping; recovered document templates and reproducible source/audit/export scripts | Local recovery only; no remote push |
| Closing QR destination needed checking | Decoded QR and replayed signed-out iPhone 13 browser flow: HTTP 200, 533 matches, no page errors or horizontal document overflow | Browser emulation, not a physical phone scan |
| Backend demo fixes remain held | Confirmed separate reviewed hotfix branch and release decision; no analyst-gate bypass | Backtest first-run error and paper-return fix still require an approved broker release. |

Deck/PDF and model consistency checks, 60 isolated broker tests, and 11 workspace-sync tests pass. No screenshot pixels were altered. See the pitch review for evidence, source links and release constraints.
