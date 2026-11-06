"""Fill the one-pager from the operating model, render both documents to PDF and set their properties."""
import json
import subprocess
import sys
from pathlib import Path

import fitz

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "Financial_Models"))
from operating_model import key_figures  # noqa: E402

k = key_figures()
t, x, mk, rt, price = k["target"], k["maximum"], k["market"], k["round_terms"], k["pricing"]
u = t["use_of_funds_usd_k"]
mix = t["rev_lakh"]
total = sum(mix.values())
share = lambda v: round(v / (rt["target_raise_usd"] / 1000) * 100)


def inr(cr):
    return f"₹{round(cr * 100)} L" if cr < 1 else f"₹{cr:.2f} Cr".replace(".00 Cr", " Cr")


tok = {
    "VERSION": "1 Nov 2026", "TAM_USD_B": mk["tam_usd_b"], "SAM_USD_M": mk["sam_usd_m"], "SEBI_FIRMS": f"{mk['sebi_firms']:,}",
    "SAM_RETAIL_CR": f"{mk['sam_retail_cr']:,}", "SAM_PRO_CR": mk["sam_pro_cr"], "SAM_PRO_SEATS": f"{mk['initial_professional_seats']:,}",
    "T_ARR": inr(t["arr_cr"]), "T_TEAMS": t["teams"], "T_SEATS": t["seats"], "T_BE": t["breakeven_month"], "X_ARR": inr(x["arr_cr"]),
    "FX": f"{k['fx']:g}", "U_TEAM": u["team"], "U_COMP": u["compliance_infra"], "U_GROW": u["growth_founder"], "U_RES": u["reserve_runway"],
    "U_TEAM_SHARE": share(u["team"]), "U_COMP_SHARE": share(u["compliance_infra"]), "U_GROW_SHARE": share(u["growth_founder"]), "U_RES_SHARE": share(u["reserve_runway"]),
    "ROUND_TARGET_K": rt["target_raise_usd"] // 1000, "ROUND_FIRST_K": rt["first_close_usd"] // 1000, "ROUND_MAX_K": rt["maximum_raise_usd"] // 1000,
    "ROUND_CAP_M": f"{rt['post_money_cap_usd'] / 1e6:g}", "DESK_LIST": f"{int(price['desk_list_seat_month_inr']):,}",
    "DESK_SHARE": round(mix["desk"] / total * 100), "PARTNER_SHARE": round(mix["partners"] / total * 100), "RETAIL_SHARE": round(mix["retail"] / total * 100),
}
html = (HERE / "onepager.html").read_text()
for a, b in tok.items():
    html = html.replace(f"%%{a}%%", str(b))
assert "%%" not in html, "unfilled token"
build = HERE / "deck"
filled = build / "onepager_filled.html"
filled.write_text(html)

jobs = [(filled, ROOT / "Investor_Materials/Anvest_OnePager.pdf", "Anvest investor overview, November 2026"),
        (HERE / "provenance.html", ROOT / "Investor_Materials/Anvest_Data_Provenance_Memo.pdf", "Anvest data provenance and methodology")]
for src, out, title in jobs:
    subprocess.run(["node", str(HERE / "render_pdf.mjs"), str(src), str(out)], check=True)
    d = fitz.open(out)
    d.set_metadata({"title": title, "author": "Harsh Bhardwaj", "subject": "", "keywords": "", "creator": "", "producer": d.metadata.get("producer", "")})
    d.save(str(out) + ".part", garbage=3, deflate=True)
    d.close()
    Path(str(out) + ".part").replace(out)
    print(out.name, fitz.open(out).page_count, "pages")
