"""Fill the public document templates from the operating model, then render PDFs."""
import json,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'Strategy/Financial_Models'))
from operating_model import key_figures
k=key_figures();f,t,x,sc,mk=[k[n] for n in ['first_close','target','maximum','scenario_arr_cr','market']];u=t['use_of_funds_usd_k'];rt=k['round_terms'];price=k['pricing']
def inr(cr):return f'₹{round(cr*100)} L' if cr<1 else f'₹{cr:.2f} Cr'.replace('.00 Cr',' Cr')
mix=t['rev_lakh'];mix_total=sum(mix.values())
tok={'VERSION':'1 Nov 2026','TAM_USD_B':mk['tam_usd_b'],'SAM_USD_M':mk['sam_usd_m'],'SEBI_FIRMS':f"{mk['sebi_firms']:,}",
'SAM_RETAIL_CR':f"{mk['sam_retail_cr']:,}",'SAM_PRO_CR':mk['sam_pro_cr'],'SAM_PRO_SEATS':f"{mk['initial_professional_seats']:,}",
'SC_Y5_USD':k['scenario_y5_usd_m'],'SC_Y5_SHARE':mk['som_share_pct'],'SC_Y5_ROUND':f"{sc['Y5']:.2f}",
'SC_Y5_CR':f"{sc['Y5']:.2f}",'T_ARR':inr(t['arr_cr']),'T_TEAMS':t['teams'],'T_SEATS':t['seats'],'T_PARTNERS':t['partners'],'T_BE':t['breakeven_month'],'X_ARR':inr(x['arr_cr']),
'X_RAISE_K':x['raise_usd_k'],'FX':f"{k['fx']:g}",
'U_TEAM':u['team'],'U_COMP':u['compliance_infra'],'U_GROW':u['growth_founder'],'U_RES':u['reserve_runway'],
'U_TEAM_SHARE':round(u['team']/(rt['target_raise_usd']/1000)*100),'U_COMP_SHARE':round(u['compliance_infra']/(rt['target_raise_usd']/1000)*100),
'U_GROW_SHARE':round(u['growth_founder']/(rt['target_raise_usd']/1000)*100),'U_RES_SHARE':round(u['reserve_runway']/(rt['target_raise_usd']/1000)*100),
'ROUND_TARGET_K':rt['target_raise_usd']//1000,'ROUND_FIRST_K':rt['first_close_usd']//1000,'ROUND_MAX_K':rt['maximum_raise_usd']//1000,
'ROUND_CAP_M':f"{rt['post_money_cap_usd']/1e6:g}",'DESK_LIST':int(price['desk_list_seat_month_inr']),
'DESK_SHARE':round(mix['desk']/mix_total*100),'PARTNER_SHARE':round(mix['partners']/mix_total*100),'RETAIL_SHARE':round(mix['retail']/mix_total*100),
'DESK_CAC':f"{t['desk_cac_lakh']:.2f}",'PAY_REV':f"{t['desk_payback_months_revenue']:g}",'PAY_GP':f"{t['desk_payback_months_gm']:g}",
'STRATEGY_PRICE':int(price['strategy_net_month_inr']),'STRATEGY_M':price['strategy_launch_month']}
s=(HERE/'onepager.html').read_text()
for a,b in tok.items():s=s.replace('%%'+a+'%%',str(b))
assert '%%' not in s
build=ROOT/'.tmp/investor-materials-20261101';build.mkdir(exist_ok=True,parents=True)
# Absolute image URL points at the unchanged screenshot asset, not generated pixels.
s=s.replace('assets/answer_tcs.jpg',(HERE/'assets/answer_tcs.jpg').as_uri())
(build/'onepager.html').write_text(s)
subprocess.run(['/Users/harsh/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node',str(HERE/'render_pdf.mjs'),str(build/'onepager.html'),str(ROOT/'Strategy/Investor_Materials/Anvest_OnePager.pdf')],check=True)
subprocess.run(['/Users/harsh/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node',str(HERE/'render_pdf.mjs'),str(HERE/'provenance.html'),str(ROOT/'Strategy/Investor_Materials/Anvest_Data_Provenance_Memo.pdf')],check=True)
