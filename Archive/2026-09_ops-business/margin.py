FX=95.69; Q=0.360   # INR per copilot question (3-flash, 10% fast-path)
GST=1.18; PAY=0.02*1.18   # 2% gateway + 18% GST on the fee

def net(gross):        return gross/GST
def payfee(gross):     return gross*PAY

TIERS = {
 # name: (monthly_price, annual_price, typical_q_per_mo, cap_q_per_mo)
 "Plus": (199, 1799, 20, 150),
 "Pro":  (599, 4999, 80, 600),
 "Desk (B2B seat)": (2999, 29990, 400, 2000),
}
print("=== Per-subscriber unit economics (GST-inclusive prices, 70% annual mix) ===\n")
print(f"{'Tier':16s} {'eff/mo':>8s} {'net rev':>8s} {'pay fee':>8s} {'LLM typ':>8s} {'LLM cap':>8s} {'CM typ':>8s} {'CM% typ':>8s} {'CM% cap':>8s}")
unit={}
for t,(m,a,tq,cq) in TIERS.items():
    eff = 0.70*(a/12) + 0.30*m           # blended effective monthly gross
    nr, pf = net(eff), payfee(eff)
    llm_t, llm_c = tq*Q, cq*Q
    cm_t, cm_c = nr-pf-llm_t, nr-pf-llm_c
    unit[t]=(eff,nr,pf,llm_t,cm_t)
    print(f"{t:16s} {eff:8.0f} {nr:8.0f} {pf:8.1f} {llm_t:8.1f} {llm_c:8.0f} {cm_t:8.0f} {100*cm_t/nr:7.1f}% {100*cm_c/nr:7.1f}%")

print("\n=== Free-tier drag: LLM cost of non-paying MAU, per PAYING subscriber ===")
for conv in (0.02,0.03,0.05,0.08):
    free_per_paid = (1-conv)/conv
    for fq in (3,6):
        drag = free_per_paid*fq*Q
        print(f"  conv {conv:.0%}  ({free_per_paid:5.1f} free/paid)  {fq} free q/mo -> INR {drag:6.0f}/mo drag"
              f"   = {100*drag/unit['Plus'][1]:5.1f}% of Plus net rev")

print("\n=== Blended P&L at scale (infra config B = $479.61/mo, fixed AI/OCR $36.80/mo) ===")
INFRA = (479.61+36.80)*FX
# subscriber mix assumption: 75% Plus, 22% Pro, 3% Desk seats
def pnl(nsub, conv=0.03, free_q=3, team_inr=0):
    mix = {"Plus":0.75,"Pro":0.22,"Desk (B2B seat)":0.03}
    nr=pf=llm=0
    for t,w in mix.items():
        e,n,p,l,_ = unit[t]; k=nsub*w
        nr+=k*n; pf+=k*p; llm+=k*l
    free = nsub*((1-conv)/conv)*free_q*Q
    cogs = pf+llm+free+INFRA
    gm = nr-cogs
    op = gm-team_inr
    return nr,cogs,gm,op,free

print(f"{'subs':>6s} {'net MRR':>12s} {'COGS':>10s} {'  free-LLM':>10s} {'gross m':>11s} {'GM%':>7s}")
for n in (100,250,500,1000,2500,5000,10000):
    nr,cogs,gm,op,free = pnl(n)
    print(f"{n:6d} {nr:12,.0f} {cogs:10,.0f} {free:10,.0f} {gm:11,.0f} {100*gm/nr:6.1f}%")

print("\n=== Break-even vs team cost (operating margin >= 50%) ===")
# Team: founder + 3 hires, India market rates
team_options = {
 "Solo founder only (INR 2.0L/mo)": 200000,
 "Founder + 2 eng (INR 6.5L/mo)":   650000,
 "Founder + 3 hires (INR 9.5L/mo)": 950000,
}
for label,team in team_options.items():
    print(f"\n  {label}")
    for n in (1000,2500,5000,10000,20000,35000):
        nr,cogs,gm,op,_ = pnl(n, team_inr=team)
        print(f"    {n:6d} subs  net MRR {nr:11,.0f}  GM {100*gm/nr:5.1f}%  OP {op:11,.0f}  OP% {100*op/nr:6.1f}%")

def solve(target, team=0, lo=50, hi=200000):
    while lo<hi:
        mid=(lo+hi)//2
        nr,c,gm,op,_=pnl(mid,team_inr=team)
        if (op if team else gm)/nr >= target: hi=mid
        else: lo=mid+1
    return lo
print("\n=== Threshold subscriber counts ===")
print(f"  Gross margin  >= 50%: {solve(0.50):,} subs")
print(f"  Gross margin  >= 70%: {solve(0.70):,} subs")
for label,team in team_options.items():
    print(f"  Operating >= 50%, {label:32s}: {solve(0.50,team):,} subs")
    nr,c,gm,op,_=pnl(solve(0.0001,team),team_inr=team)
    print(f"  Cash break-even,  {label:32s}: {solve(0.0001,team):,} subs")

print("\n=== Sensitivity: what if we land on a pricier model / heavier usage ===")
import copy
base_unit=copy.deepcopy(unit)
for label,qcost,mult in [("3-flash, typical usage (base)",0.360,1.0),
                         ("3-flash, 2x usage",0.360,2.0),
                         ("3.5-flash (INR 1.20/q), typical",1.201*0.9,1.0),
                         ("3.5-flash, 2x usage",1.201*0.9,2.0),
                         ("3.1-flash-lite (INR 0.20/q)",0.200*0.9,1.0)]:
    for t,(m,a,tq,cq) in TIERS.items():
        e,n,p,_,_=base_unit[t]; l=tq*mult*qcost
        unit[t]=(e,n,p,l,n-p-l)
    nr,c,gm,op,fr=pnl(2500)
    n2,c2,gm2,op2,_=pnl(10000)
    print(f"  {label:34s} GM@2.5k {100*gm/nr:5.1f}%   GM@10k {100*gm2/n2:5.1f}%   50%GM at {solve(0.50):,} subs")
unit=base_unit

print("\n=== The real lever: free-tier AI allowance x model choice (GM% at 2,500 subs, 3% conv) ===")
print(f"{'free q/mo':>10s} " + " ".join(f"{n:>14s}" for n in ["3.1-lite .20","3-flash .40","3.5-flash 1.20"]))
for fq in (0,1,3,5,10):
    row=[]
    for qc in (0.200*0.9, 0.360, 1.201*0.9):
        for t,(m,a,tq,cq) in TIERS.items():
            e,n,p,_,_=base_unit[t]; l=tq*qc; unit[t]=(e,n,p,l,n-p-l)
        nr,c,gm,op,_=pnl(2500, free_q=fq)
        row.append(f"{100*gm/nr:13.1f}%")
    print(f"{fq:>10d} " + " ".join(row))
unit=base_unit
print("\n=== Annual vs monthly mix effect on Plus (cash + fee efficiency) ===")
for amix in (0.0,0.5,0.7,0.9):
    m,a,tq,cq = TIERS["Plus"]
    eff=amix*(a/12)+(1-amix)*m; nr=eff/GST; pf=eff*PAY
    print(f"  {amix:.0%} annual -> effective INR {eff:6.0f}/mo, net INR {nr:6.0f}, fee INR {pf:5.2f}, "
          f"CM INR {nr-pf-tq*Q:6.0f} ({100*(nr-pf-tq*Q)/nr:.1f}%)")
