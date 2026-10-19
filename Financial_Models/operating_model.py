"""Anvest monthly operating model (revised 20 October 2026).

Single source for every revenue, cost, runway and market-size figure in the investor materials.
Round cases (months 1-18 are the plan this round funds; later months only show runway):
  first_close -- $400K: Desk seats (founder + one seller), retail subscriptions, two paid partners.
  target      -- $500K (the headline ask): first close plus a second seller from month 9.
  maximum     -- $700K: second seller from month 6, more growth spend and a third partner.
Long-term scenario: built on the target case, conditional on a Series A near month 18, SEBI RA
registration, exchange empanelment, a partner broker and signed partner contracts.
Every input is a planning assumption, not measured conversion, usage or contracted revenue.
After changing inputs, rerun and then run ../check_materials.py.

Run:  /opt/homebrew/bin/python3 operating_model.py            # summary
      /opt/homebrew/bin/python3 operating_model.py --json     # key figures for the materials
      /opt/homebrew/bin/python3 operating_model.py --xlsx     # writes Anvest_Operating_Model.xlsx
"""
import json
import sys
from dataclasses import dataclass, field, replace

FX = 95.0                       # INR per USD: spot, USD/INR close 16 Oct 2026 was 95.02
LAKH, CR = 1e5, 1e7

# ---------- Market sizing (annual, list prices) ----------
ACTIVE_NSE_CLIENTS = 4.6 * CR   # NSE Market Pulse, Aug 2026
ACTIVE_TRADERS = 96 * LAKH      # SEBI FY25 study population of individual traders (top 13 brokers)
MFD_PROFESSIONALS = 3.53 * LAKH # valid ARN + EUIN holders, Jun 2026 (Cafemutual)
TOP_MFDS = 3_350                # MFDs recognised as top distributors for FY26 (AMFI ARN committee, via Cafemutual)
SEBI_FIRMS = 2_304 + 539 + 1_057  # SEBI intermediary directory, 19 Oct 2026: RAs + PMS + IAs
PLUS_ANNUAL = 199 * 12
DESK_ANNUAL = 2_999 * 12
SAM_SEATS_PER_FIRM = 3          # average Desk seats per professional firm (1-5 seat plans)


@dataclass(frozen=True)
class Plan:
    name: str = "first_close"
    months: int = 18
    raise_usd: float = 400_000
    # Retail: organic search, launch and creators bring monthly active users (MAU)
    launch_month: int = 2
    mau_at_launch: float = 2_000
    mau_growth_y1: float = 0.15          # monthly, until month 12
    mau_growth_later: float = 0.08       # monthly, from month 13 (until scale_from in the scenario)
    scale_from: int = 999                # first month of Series A-funded growth (scenario only)
    mau_growth_scale: float = 0.08       # monthly MAU growth from scale_from to month 36
    mau_growth_late: float = 0.06        # monthly, after month 36
    paid_conversion: float = 0.003       # share of MAU converting to paid each month
    retail_churn: float = 0.05
    retail_net: float = 200              # Rs/month per subscriber after GST and launch discounts
    # Desk: 1-5 seat plans for RAs, IAs, PMS desks and distributors
    seller_starts: tuple = ((3, 4.0),)   # (start month, new teams/month once ramped); ramp: half for two months
    founder_teams_from: int = 3          # founder sells after the first paid pilots convert
    founder_teams_pm: float = 1.0
    seats_per_team: float = 3.0          # average new team: mix of solo practitioners and 5-seat desks
    team_churn: float = 0.02
    seat_expansion: float = 0.01         # monthly seat growth inside retained teams
    seat_net: float = 2_245              # Rs/seat-month (list Rs 2,999 incl. GST, after discounts)
    # Partners: paid integrations, tiered per active integrated user
    partner_live: tuple = ((10, 4_000), (14, 4_000))  # (month a paid partner goes live, users at launch)
    partner_user_growth: float = 0.06    # monthly
    partner_growth_after_scale: float | None = None
    partner_tiers: tuple = ((10_000, 15.0), (50_000, 10.0), (float("inf"), 6.0))  # Rs/user/month by band
    # Strategies: subscriptions after RA registration, exchange empanelment and a partner broker
    strategy_launch: int = 0             # 0 = not in this plan
    strategy_net: float = 250            # Rs/month to Anvest after broker revenue share
    strategy_adopt_partner: float = 0.004  # share of integrated partner users subscribing per month
    strategy_adopt_retail: float = 0.02    # share of retail subscribers adding strategies per month
    strategy_churn: float = 0.06
    # Costs (Rs/month unless noted)
    founder_salary: float = 2.0 * LAKH
    hires: tuple = ((2, 2.75 * LAKH), (3, 3.25 * LAKH), (6, 2.75 * LAKH))  # growth lead, data engineer, full-stack/quant
    overhead: float = 0.10               # benefits, hiring, equipment on salaries
    infra_fixed: tuple = ((1, 0.6 * LAKH), (10, 1.5 * LAKH))  # serving, backups, hosting; scaled serving from m10
    cost_per_answer: float = 0.75        # Rs per AI answer (planning value)
    answers_free_mau: float = 3
    answers_retail: float = 40
    answers_seat: float = 300
    answers_partner_user: float = 2
    data_licence: tuple = ((4, 1.25 * LAKH),)  # exchange data licence estimate
    compliance_once: tuple = ((2, 3 * LAKH), (3, 3 * LAKH), (4, 2 * LAKH))  # RA registration and counsel
    compliance_monthly: float = 0.4 * LAKH  # from month 6
    marketing: tuple = ((2, 1.5 * LAKH), (7, 3.0 * LAKH))
    tools_misc: float = 0.5 * LAKH
    commission: float = 0.05             # of Desk revenue
    seller_cost: float = 2.75 * LAKH     # monthly salary per seller (the growth lead is the first)
    payment_fee: float = 0.0236          # of gross subscription receipts
    reserve_share: float = 0.175         # of the raise, held back from planned spend


FIRST_CLOSE = Plan()
TARGET = replace(FIRST_CLOSE, name="target", raise_usd=500_000,
                 seller_starts=((3, 4.0), (9, 4.0)), hires=FIRST_CLOSE.hires + ((9, 2.5 * LAKH),))
MAXIMUM = replace(FIRST_CLOSE, name="maximum", raise_usd=700_000, mau_growth_y1=0.18,
                  seller_starts=((3, 4.0), (6, 4.0)), hires=FIRST_CLOSE.hires + ((6, 2.5 * LAKH),),
                  partner_live=((9, 4_000), (12, 4_000), (15, 4_000)),
                  marketing=((2, 2.5 * LAKH), (7, 4.5 * LAKH)))
SCENARIO = replace(
    TARGET, name="scenario", months=60,
    # Series A near month 18 funds sellers: three more in year 2, then about three a year.
    seller_starts=TARGET.seller_starts + tuple((m, 4.0) for m in (20, 22, 24, 27, 30, 33, 36, 40, 44, 48, 52, 56)),
    scale_from=19, mau_growth_scale=0.11, mau_growth_late=0.06,
    partner_live=TARGET.partner_live + tuple((m, 10_000) for m in (20, 24, 28, 32, 38, 44, 50, 56)),
    partner_growth_after_scale=0.05,
    strategy_launch=22,
    hires=TARGET.hires + tuple((m, TARGET.seller_cost) for m in (20, 22, 24, 27, 30, 33, 36, 40, 44, 48, 52, 56)),
    marketing=TARGET.marketing + ((19, 6 * LAKH), (37, 10 * LAKH)),
)
CASES = (FIRST_CLOSE, TARGET, MAXIMUM)


def at(schedule, m):
    v = 0
    for start, val in schedule:
        if m >= start:
            v = val
    return v


def partner_fee(users, tiers):
    fee, lower = 0.0, 0.0
    for upper, price in tiers:
        band = max(0.0, min(users, upper) - lower)
        fee += band * price
        lower = upper
        if users <= upper:
            break
    return fee


@dataclass
class Month:
    m: int
    mau: float = 0
    retail_subs: float = 0
    teams: float = 0
    seats: float = 0
    partners: int = 0
    partner_users: float = 0
    strategy_subs: float = 0
    new_teams: float = 0
    sellers: int = 0
    rev: dict = field(default_factory=dict)
    cost: dict = field(default_factory=dict)
    cash: float = 0

    @property
    def mrr(self):
        return sum(self.rev.values())

    @property
    def spend(self):
        return sum(self.cost.values())


def run(p: Plan, months=None):
    months = months or p.months
    cash = p.raise_usd * FX
    mau = subs = teams = seats = strat = 0.0
    out = []
    for m in range(1, months + 1):
        if m == p.launch_month:
            mau = p.mau_at_launch
        elif m > p.launch_month:
            g = (p.mau_growth_y1 if m <= 12 else p.mau_growth_later if m < p.scale_from
                 else p.mau_growth_scale if m <= 36 else p.mau_growth_late)
            mau *= 1 + g
        subs = subs * (1 - p.retail_churn) + mau * p.paid_conversion
        new_teams = p.founder_teams_pm if m >= p.founder_teams_from else 0
        for start, rate in p.seller_starts:
            if m >= start + 2:
                new_teams += rate
            elif m >= start:
                new_teams += rate / 2
        teams = teams * (1 - p.team_churn) + new_teams
        seats = seats * (1 - p.team_churn) * (1 + p.seat_expansion) + new_teams * p.seats_per_team
        live = [(s, u) for s, u in p.partner_live if m >= s]
        def partner_users(start, initial):
            if p.partner_growth_after_scale is None:
                return initial * (1 + p.partner_user_growth) ** (m - start)
            early = max(0, min(m, p.scale_from - 1) - start)
            late = max(0, m - max(start, p.scale_from - 1))
            return initial * (1 + p.partner_user_growth) ** early * (1 + p.partner_growth_after_scale) ** late
        users_each = [partner_users(s, u) for s, u in live]
        pusers = sum(users_each)
        if p.strategy_launch and m >= p.strategy_launch:
            strat = strat * (1 - p.strategy_churn) + pusers * p.strategy_adopt_partner + subs * p.strategy_adopt_retail
        rev = {
            "retail": subs * p.retail_net,
            "desk": seats * p.seat_net,
            "partners": sum(partner_fee(u, p.partner_tiers) for u in users_each),
            "strategies": strat * p.strategy_net,
        }
        hired = sum(sal for start, sal in p.hires if m >= start)
        answers = (mau * p.answers_free_mau + subs * p.answers_retail + seats * p.answers_seat
                   + pusers * p.answers_partner_user)
        gross_subs = (rev["retail"] + rev["desk"] + rev["strategies"]) * 1.18
        cost = {
            "salaries": (p.founder_salary + hired) * (1 + p.overhead),
            "infrastructure": at(p.infra_fixed, m) + answers * p.cost_per_answer,
            "data_and_compliance": at(p.data_licence, m) + sum(v for s, v in p.compliance_once if s == m)
                                   + (p.compliance_monthly if m >= 6 else 0),
            "growth": at(p.marketing, m) + rev["desk"] * p.commission,
            "other": p.tools_misc + gross_subs * p.payment_fee,
        }
        cash += sum(rev.values()) - sum(cost.values())
        sellers = sum(1 for start, _ in p.seller_starts if m >= start)
        out.append(Month(m, mau, subs, teams, seats, len(live), pusers, strat, new_teams, sellers, rev, cost, cash))
    return out


def unit_economics(p: Plan, rows, m=15):
    """Gross margin at month m, and Desk CAC payback over months 1..m."""
    r = rows[m - 1]
    cogs = r.cost["infrastructure"] + (r.cost["other"] - p.tools_misc) + at(p.data_licence, m)
    gm = 1 - cogs / r.mrr if r.mrr else 0
    sm = sum(x.sellers * p.seller_cost * (1 + p.overhead) + x.rev["desk"] * p.commission for x in rows[:m])
    won = sum(x.new_teams for x in rows[:m])
    cac = sm / won if won else 0
    team_monthly = p.seats_per_team * p.seat_net
    return gm, cac, cac / team_monthly, cac / (team_monthly * max(gm, 0.0001))


def runway(p: Plan, horizon=72):
    """Cash runway from close if the month-18 team and spend continue with no new funding.

    Revenue keeps compounding on the same drivers; no hires after the plan. Returns the month cash
    runs out (None if it never does within the horizon) and the first month revenue covers spend.
    """
    rows = run(p, months=horizon)
    out = next((r.m for r in rows if r.cash < 0), None)
    breakeven = next((r.m for r in rows if r.mrr >= r.spend), None)
    return out, breakeven, rows


def market():
    retail_tam = ACTIVE_NSE_CLIENTS * PLUS_ANNUAL
    pro_tam = (MFD_PROFESSIONALS + SEBI_FIRMS) * DESK_ANNUAL
    retail_sam = ACTIVE_TRADERS * PLUS_ANNUAL
    pro_sam = (SEBI_FIRMS + TOP_MFDS) * SAM_SEATS_PER_FIRM * DESK_ANNUAL
    return retail_tam, pro_tam, retail_sam, pro_sam


def key_figures():
    tam_r, tam_p, sam_r, sam_p = market()
    out = {"fx": FX}

    def arr(rows, m):
        return {k: round(v * 12 / CR, 2) for k, v in rows[m - 1].rev.items()} | {"total": round(rows[m - 1].mrr * 12 / CR, 2)}

    for p in CASES:
        rows = run(p)
        r15 = rows[14]
        gm, cac, pay_rev, pay_gm = unit_economics(p, rows)
        cash_out, breakeven, long_rows = runway(p)
        low = min(long_rows, key=lambda r: r.cash)
        founder18 = p.founder_salary * (1 + p.overhead) * 18
        cat = {k: sum(r.cost[k] for r in rows) for k in rows[0].cost}
        uses = {"team": cat["salaries"] - founder18,
                "compliance_infra": cat["infrastructure"] + cat["data_and_compliance"],
                "growth_founder": cat["growth"] + cat["other"] + founder18}
        uses = {k: round(v / FX / 5e3) * 5 for k, v in uses.items()}
        uses["reserve_runway"] = round(p.raise_usd / 1e3) - sum(uses.values())
        spend18 = sum(r.spend for r in rows)
        rev18 = sum(r.mrr for r in rows)
        out[p.name] = {
            "raise_usd_k": round(p.raise_usd / 1e3),
            "mrr_lakh": round(r15.mrr / LAKH, 1), "arr_cr": round(r15.mrr * 12 / CR, 2),
            "arr_usd_k": round(r15.mrr * 12 / FX / 1e3),
            "teams": round(r15.teams), "seats": round(r15.seats), "teams_m6": round(rows[5].teams),
            "teams_m12": round(rows[11].teams), "retail_subs": round(r15.retail_subs), "mau": round(r15.mau),
            "arr_m12_cr": round(rows[11].mrr * 12 / CR, 2), "arr_m18_cr": round(rows[17].mrr * 12 / CR, 2),
            "teams_m18": round(rows[17].teams), "partners_m12": rows[11].partners,
            "partners": r15.partners, "rev_lakh": {k: round(v / LAKH, 2) for k, v in r15.rev.items()},
            "net_burn_m15_lakh": round((r15.spend - r15.mrr) / LAKH, 1),
            "spend_m1_18_cr": round(spend18 / CR, 2), "spend_m1_18_usd_k": round(spend18 / FX / 1e3),
            "revenue_m1_18_cr": round(rev18 / CR, 2),
            "cash_m18_cr": round(rows[17].cash / CR, 2), "cash_m18_usd_k": round(rows[17].cash / FX / 1e3),
            "cash_out_month": cash_out, "breakeven_month": breakeven,
            "gross_margin_pct": round(gm * 100), "desk_cac_lakh": round(cac / LAKH, 2),
            "desk_payback_months_revenue": round(pay_rev, 1), "desk_payback_months_gm": round(pay_gm, 1),
            "spend_by_category_usd_k": {k: round(sum(r.cost[k] for r in rows) / FX / 1e3) for k in rows[0].cost},
            "cash_low_cr": round(low.cash / CR, 2), "cash_low_month": low.m,
            "use_of_funds_usd_k": uses,
        }
    sc = run(SCENARIO)
    y5_gm, _, _, _ = unit_economics(SCENARIO, sc, 60)
    out["scenario_additional_capital_floor_cr"] = round(max(0, -min(r.cash for r in sc)) / CR, 2)
    labels = (("M15", 15), ("Y2", 24), ("Y3", 36), ("Y4", 48), ("Y5", 60))
    out["scenario_arr_cr"] = {k: arr(sc, m)["total"] for k, m in labels}
    out["scenario_by_engine_cr"] = {k: arr(sc, m) for k, m in labels}
    out["scenario_drivers"] = {k: {"sellers": sc[m - 1].sellers, "mau": round(sc[m - 1].mau), "seats": round(sc[m - 1].seats),
                                   "partners": sc[m - 1].partners, "partner_users": round(sc[m - 1].partner_users),
                                   "strategy_subs": round(sc[m - 1].strategy_subs), "retail_subs": round(sc[m - 1].retail_subs),
                                   "arr_cr": round(sc[m - 1].mrr * 12 / CR, 2)} for k, m in labels}
    y5 = out["scenario_by_engine_cr"]["Y5"]
    out["scenario_y5_usd_m"] = round(y5["total"] * CR / FX / 1e6, 1)
    out["scenario_y5_core_cr"] = round(y5["retail"] + y5["desk"], 1)
    out["scenario_y5_conditional_cr"] = round(y5["partners"] + y5["strategies"], 1)
    out["scenario_y5_gross_margin_pct"] = round(y5_gm * 100)
    out["market"] = {
        "tam_cr": round((tam_r + tam_p) / CR), "tam_usd_b": round((tam_r + tam_p) / FX / 1e9, 1),
        "tam_retail_cr": round(tam_r / CR), "tam_pro_cr": round(tam_p / CR),
        "sam_cr": round((sam_r + sam_p) / CR), "sam_usd_m": round((sam_r + sam_p) / FX / 1e6),
        "sam_retail_cr": round(sam_r / CR), "sam_pro_cr": round(sam_p / CR),
        "sebi_firms": SEBI_FIRMS, "top_mfds": TOP_MFDS,
        "initial_professional_seats": (SEBI_FIRMS + TOP_MFDS) * SAM_SEATS_PER_FIRM,
        "y5_initial_professional_seat_share_pct": round(sc[59].seats / ((SEBI_FIRMS + TOP_MFDS) * SAM_SEATS_PER_FIRM) * 100, 1),
        "som_share_pct": round(out["scenario_arr_cr"]["Y5"] / ((sam_r + sam_p) / CR) * 100, 1),
    }
    return out


def print_summary():
    k = key_figures()
    print(f"FX Rs {k['fx']}/USD")
    for name in ("first_close", "target", "maximum"):
        c = k[name]
        print(f"{name.upper():12s} ${c['raise_usd_k']}K | M15 MRR Rs {c['mrr_lakh']} L (ARR Rs {c['arr_cr']} Cr, ${c['arr_usd_k']}K) | "
              f"teams M6/M12/M15 {c['teams_m6']}/{c['teams_m12']}/{c['teams']} ({c['seats']} seats) | partners {c['partners']} | "
              f"M15 net burn Rs {c['net_burn_m15_lakh']} L/mo | spend M1-18 Rs {c['spend_m1_18_cr']} Cr (${c['spend_m1_18_usd_k']}K) | "
              f"cash M18 Rs {c['cash_m18_cr']} Cr | cash-out month {c['cash_out_month']} | breakeven month {c['breakeven_month']} | low Rs {c['cash_low_cr']} Cr at M{c['cash_low_month']}")
        print("             use of funds $K:", c["use_of_funds_usd_k"])
        print("             M15 revenue (Rs L/mo):", c["rev_lakh"], "| spend by category $K:", c["spend_by_category_usd_k"])
        print(f"             GM {c['gross_margin_pct']}% | Desk CAC Rs {c['desk_cac_lakh']} L | payback {c['desk_payback_months_revenue']} mo revenue / {c['desk_payback_months_gm']} mo GM")
    print("SCENARIO ARR (Rs Cr):", k["scenario_arr_cr"], f"Y5 ${k['scenario_y5_usd_m']}M; core {k['scenario_y5_core_cr']} + conditional {k['scenario_y5_conditional_cr']}; Y5 GM {k['scenario_y5_gross_margin_pct']}%")
    for y, v in k["scenario_drivers"].items():
        print("  ", y, v)
    print("Market:", k["market"])


def write_xlsx(path=None):
    """Refresh the existing value-snapshot workbook using Artifact Tool.

    The Python schedules remain authoritative. This preserves the supplied
    workbook's intentionally separate cases rather than changing its design.
    """
    import subprocess
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    build = root / ".tmp/investor-materials-20261020"
    build.mkdir(parents=True, exist_ok=True)
    payload = {"Read me": [[text] for text in [
        "Anvest operating model, 20 Oct 2026. Value snapshot: edit Python inputs and regenerate; workbook cells do not recalculate the model.",
        "First close $400K; target $500K; maximum $700K. Planning assumptions, not measured conversion or contracted revenue. Planning FX Rs 95/USD.",
        "Round cases extend to month 72 with no new funding. Target reaches break-even at M42 under the model assumptions.",
        "The separate scale scenario assumes a Series A near M18, approvals and contracts. Its cash balance excludes that unpriced financing.",
        "All added sellers have salary costs; scenario marketing is Rs 6 L/month from M19, Rs 10 L/month from M37.",
        "Years 3–5 Desk expands into broader distributors, family offices and CA/wealth practices. 4,132 seats equal 19% of the initial 21,750-seat SAM.",
    ]]}
    payload["Assumptions"] = [["Input", "First close $400K", "Target $500K", "Maximum $700K", "Scenario"]]
    for name in Plan.__dataclass_fields__:
        payload["Assumptions"].append([name] + [str(getattr(p, name)) for p in (FIRST_CLOSE, TARGET, MAXIMUM, SCENARIO)])
    hdr = ["Month", "MAU", "Retail subscribers", "Desk teams", "Desk seats", "Partners live", "Partner users",
           "Strategy subscribers", "Retail rev", "Desk rev", "Partner rev", "Strategy rev", "MRR",
           "Salaries", "Infrastructure", "Data & compliance", "Growth", "Other", "Total spend", "Cash"]
    for title, rows in [("First close $400K", run(FIRST_CLOSE,72)), ("Target $500K",run(TARGET,72)),
                        ("Maximum $700K",run(MAXIMUM,72)), ("Scenario",run(SCENARIO))]:
        payload[title] = [hdr] + [[r.m,round(r.mau),round(r.retail_subs),round(r.teams,1),round(r.seats),r.partners,
            round(r.partner_users),round(r.strategy_subs),*(round(r.rev[k]) for k in ("retail","desk","partners","strategies")),round(r.mrr),
            *(round(r.cost[k]) for k in ("salaries","infrastructure","data_and_compliance","growth","other")),round(r.spend),round(r.cash)] for r in rows]
    data = build / "workbook_payload.json"
    data.write_text(json.dumps(payload))
    output = Path(path).resolve() if path else Path(__file__).with_name("Anvest_Operating_Model.xlsx")
    subprocess.run(["/Users/harsh/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node",
        str(root / "Strategy/Source/update_workbook.mjs"),str(data),str(output)],check=True)


if __name__ == "__main__":
    if "--json" in sys.argv:
        print(json.dumps(key_figures(), indent=1))
    elif "--xlsx" in sys.argv:
        write_xlsx()
    else:
        print_summary()
