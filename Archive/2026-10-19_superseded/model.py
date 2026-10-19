# Historical planning calculator: assumptions from 31 August 2026.
# See PRICING_AND_UNIT_ECONOMICS.md. Provider prices, model availability and FX are not live quotes.
# ANVEST_ALLOW_MODEL_ID_LITERALS: this is a price table. The model ids below
# are the subject of the comparison, not a selection -- nothing here chooses
# which model runs. See broker-portfolio/tests/test_no_legacy_gemini_models.py.
FX = 95.69  # INR/USD, 2026-08-30

# ---------- LLM unit cost ----------
# Measured: $0.0030/question on gemini-2.5-flash ($0.30/M in, $2.50/M out)
# Solve for token mix assuming ~700 output tokens (ANVEST_AI_MAX_OUTPUT_TOKENS=700)
OUT = 700
out_cost_25f = 2.50*OUT/1e6
IN = (0.0030 - out_cost_25f)/(0.30/1e6)
print(f"Inferred prompt mix: {IN:,.0f} input + {OUT} output tokens/question")

models = {
 "gemini-2.5-flash (today, retires ~16 Oct 2026)": (0.30, 2.50),
 "gemini-2.5-flash-lite (today, router)":          (0.10, 0.40),
 "gemini-3.1-flash-lite":                          (0.25, 1.50),
 "gemini-3-flash":                                 (0.50, 3.00),
 "gemini-3.5-flash":                               (1.50, 9.00),
}
print("\nPer-question cost by model (same prompt shape):")
q = {}
for m,(i,o) in models.items():
    c = i*IN/1e6 + o*OUT/1e6
    q[m] = c
    print(f"  {m:48s} ${c:.5f}  = INR {c*FX:6.3f}")

# cached-input variant for gemini-3-flash (cached $0.05/M): evidence reuse
c_cached = 0.05*IN/1e6*0.7 + 0.50*IN/1e6*0.3 + 3.00*OUT/1e6
print(f"  {'gemini-3-flash w/ 70% context-cache hit':48s} ${c_cached:.5f}  = INR {c_cached*FX:6.3f}")

BASE = q["gemini-3-flash"]          # planning assumption post-migration
FASTPATH = 0.10                     # measured fast-path rate, zero LLM cost
EFF = BASE*(1-FASTPATH)
print(f"\nPlanning unit cost (3-flash, 10% fast-path): INR {EFF*FX:.3f}/question")

# ---------- infra ----------
print("\n=== GCP asia-south1 monthly (1yr CUD where noted) ===")
cfg = {
 "A. Minimum viable (Mac still batch)": {
    "app+PG+Redis+sidecar e2-standard-8 CUD":148.06,
    "400GB pd-balanced":400*0.12,
    "Qdrant e2-standard-2 CUD":37.02,
    "Qdrant 100GB pd-balanced":12.0,
    "egress ~100GB":12.0, "snapshots/backup":15.0, "Vercel Pro":20.0},
 "B. Production-grade split (Mac still batch)": {
    "app+Redis+sidecar e2-standard-4 CUD":74.03,
    "Postgres n2-standard-8 CUD":214.55,
    "PG 300GB pd-balanced (post-prune)":300*0.12,
    "Qdrant e2-standard-4 CUD":74.03,
    "Qdrant 100GB pd-balanced":12.0,
    "egress ~200GB":24.0, "snapshots/backup":25.0, "Vercel Pro":20.0},
 "C. Full cloud, Mac retired": {
    "(all of B)":74.03+214.55+36+74.03+12+24+25+20,
    "batch e2-standard-8 spot":70.0,
    "L4 burst amortised":30.0},
}
infra = {}
for name,items in cfg.items():
    t = sum(items.values()); infra[name]=t
    print(f"\n{name}: ${t:,.2f}/mo = INR {t*FX:,.0f}/mo")
    for k,v in items.items(): print(f"    {k:44s} ${v:8.2f}")

# platform-fixed AI (not per-user)
enrich = 0.79*4.33/FX      # measured INR 0.79/week weekly enrichment
profiles = 750*(1700*0.50/1e6 + 500*3.00/1e6)  # 25 symbols/day delta refresh on 3-flash
ocr = 35.0                 # ~17k announcements/mo, ~30% scanned x3pp @ $1.50/1000
fixed_ai = enrich+profiles+ocr
print(f"\nPlatform-fixed AI/OCR: ${fixed_ai:.2f}/mo (enrich ${enrich:.2f}, profiles ${profiles:.2f}, OCR ${ocr:.2f})")
