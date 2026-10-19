# Seed-round revenue plan, 19 October 2026: the numbers behind the seed deck's
# "Path to Rs 50 Cr ARR" slide, the Month-15 bridge and the one-pager.
# Every input below is a planning assumption, not measured conversion or contracted revenue.
# Change an input, rerun, and copy the printed figures into the deck appendix.
# Run: /opt/homebrew/bin/python3 revenue_plan.py
FX = 95.69                      # INR/USD, same rate as the rest of the folder (30 Aug 2026)
CR, LAKH = 1e7, 1e5

# Net monthly revenue per unit after 18% GST and launch discounts (see PRICING_AND_UNIT_ECONOMICS.md)
RETAIL_NET_PM = 200             # blended Plus/Pro subscriber, Rs/month
DESK_NET_PM = 2245              # Desk seat at Rs 2,999 list, Rs/month

# Each milestone: retail subscribers, Desk seats, paying partners x annual licence (Rs),
# strategy subscribers x annual fee (Rs). Strategies start only after SEBI RA registration
# and exchange empanelment, so Month 15 carries none.
PLAN = [
    ("Month 15", dict(retail=900,    seats=200,  partners=2,  partner_fee=12 * LAKH,  algo=0,      algo_fee=0)),
    ("Year 2",   dict(retail=4_000,  seats=600,  partners=4,  partner_fee=25 * LAKH,  algo=2_000,  algo_fee=3_000)),
    ("Year 3",   dict(retail=12_000, seats=1_500, partners=6, partner_fee=50 * LAKH,  algo=8_000,  algo_fee=4_000)),
    ("Year 4",   dict(retail=25_000, seats=3_000, partners=8, partner_fee=75 * LAKH,  algo=18_000, algo_fee=4_500)),
    ("Year 5",   dict(retail=45_000, seats=5_000, partners=10, partner_fee=100 * LAKH, algo=35_000, algo_fee=5_000)),
]

# Market sizing inputs (sources in the deck footnotes)
ACTIVE_NSE_CLIENTS = 4.6 * CR   # NSE Market Pulse, Aug 2026
FNO_TRADERS = 96 * LAKH         # SEBI FY25 F&O study, top 13 brokers
MFD_PROFESSIONALS = 3.53 * LAKH # valid ARN + EUIN holders, Jun 2026 (Cafemutual)
SEBI_FIRMS = 2_304 + 539 + 1_057  # SEBI directory, 19 Oct 2026: research analysts + portfolio managers + investment advisers
PLUS_ANNUAL = 199 * 12          # Plus list price per year, Rs
DESK_ANNUAL = 2_999 * 12        # Desk list price per seat-year, Rs


def arr(m):
    retail = m["retail"] * RETAIL_NET_PM * 12
    desk = m["seats"] * DESK_NET_PM * 12
    partners = m["partners"] * m["partner_fee"]
    algo = m["algo"] * m["algo_fee"]
    return retail, desk, partners, algo


def fmt_cr(x):
    return f"Rs {x / CR:6.2f} Cr  (${x / FX / 1e6:5.2f}M)"


print("=== Exit ARR run-rate by milestone (Rs Cr) ===")
print(f"{'Milestone':10s} {'Retail':>8s} {'Desk':>8s} {'Partners':>9s} {'Strategies':>11s} {'Total':>8s}  USD")
for name, m in PLAN:
    r, d, p, a = arr(m)
    t = r + d + p + a
    print(f"{name:10s} {r / CR:8.2f} {d / CR:8.2f} {p / CR:9.2f} {a / CR:11.2f} {t / CR:8.2f}  ${t / FX / 1e6:.2f}M")

name, m = PLAN[0]
r, d, p, a = arr(m)
print(f"\n=== {name} bridge (monthly) ===")
print(f"Retail:    {m['retail']:,} subscribers x Rs {RETAIL_NET_PM} = Rs {r / 12 / LAKH:.2f} L/month")
print(f"Desk:      {m['seats']:,} seats ({m['seats'] // 5} teams x 5) x Rs {DESK_NET_PM:,} = Rs {d / 12 / LAKH:.2f} L/month")
print(f"Partners:  {m['partners']} x Rs {m['partner_fee'] / 12 / LAKH:.2f} L/month = Rs {p / 12 / LAKH:.2f} L/month")
mrr = (r + d + p + a) / 12
print(f"Total MRR: Rs {mrr / LAKH:.2f} L  ->  ARR run-rate {fmt_cr(mrr * 12)}")
print(f"Retail subscribers imply ~{m['retail'] / 0.03:,.0f} monthly users at 3% paid conversion")
print(f"Desk teams = {100 * (m['seats'] // 5) / SEBI_FIRMS:.1f}% of SEBI RA/PMS/IA firms")

print("\n=== Market size (annual, list prices) ===")
tam = ACTIVE_NSE_CLIENTS * PLUS_ANNUAL + (MFD_PROFESSIONALS + SEBI_FIRMS) * DESK_ANNUAL
sam = FNO_TRADERS * PLUS_ANNUAL + SEBI_FIRMS * 5 * DESK_ANNUAL
som = sum(arr(PLAN[-1][1]))
print(f"TAM: every active NSE client on Plus + every advice/distribution professional on Desk: {fmt_cr(tam)}")
print(f"SAM: India's active traders on Plus + RA/PMS/IA firms at 5 Desk seats:               {fmt_cr(sam)}")
print(f"SOM: Year-5 plan ARR:                                                               {fmt_cr(som)}  = {100 * som / sam:.1f}% of SAM")
