"""Prepare focused deck edits while preserving native charts, screenshots and layouts.

The companion update_decks.mjs edits the imported presentation with Artifact Tool.
This package-preservation pass retains the original OOXML masters and media to avoid
round-trip changes in the founder's flow slide. No screenshot pixels are changed.
"""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree as E
import json, re, sys, io
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"Financial_Models"))
from operating_model import key_figures
MODEL=key_figures()
FIRST, TARGET, MAXIMUM = (MODEL[n] for n in ('first_close','target','maximum'))
SCENARIO=MODEL['scenario_by_engine_cr']
PERIODS=["M15","Y2","Y3","Y4","Y5"]
ENGINES=["desk","retail","partners","strategies"]
ROOT=Path(__file__).resolve().parents[2]
BUILD=ROOT/'.tmp/investor-materials-20261101'
NS={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships','rel':'http://schemas.openxmlformats.org/package/2006/relationships'}
MONTHS='Jul 45,997 · Aug 61,875 · Sep 38,558 (2026)'
SEED_ORDER=[1,2,6,9,3,5,7,10,8,14,15,16,4,11,12,13,17]

def inr(cr):
    return f'₹{round(cr*100)} L' if cr<1 else f'₹{cr:.2f} Cr'.replace('.00 Cr',' Cr')
COMMON={
'Default-alive on $500K, with Series A scale to ~₹23 Cr ARR':'Default-alive on $500K, Series A path to ~₹23 Cr ARR',
'A $1.3B market: professionals first, active investors at scale':'A $1.3B market, starting with professional teams',
'Only Anvest':'Anvest',
'Zero-CAC':'Organic', 'zero-CAC':'organic',
'₹9.6 Cr':'₹9.7 Cr', '₹23.0 Cr':'₹23.11 Cr',
'6,137':'6K+', 'Version 19 Oct 2026 (r5)':'Version 1 Nov 2026',
'20 Oct 2026 (r5)':'Version 1 Nov 2026', '2.89M':'2.94M',
'1.35M':'6.16M',
'~17K':'~49K', '~17,000':'~49,000',
'new filings ingested a month':'announcements/month, Q2 FY27',
'new filings to track every month':'announcements/month, Q2 FY27',
'new filings every month':'announcements/month, Q2 FY27',
'6,137 stock pages with AI profiles':'6K+ stock pages; 6,119 AI profiles',
'Anvest  ·  Confidential  ·  20 Oct 2026':'Anvest  ·  Confidential  ·  Version 1 Nov 2026',
'6,137 companies, 2.89M announcements and 1.35M indexed passages, refreshed nightly':'6K+ companies, 2.94M announcements and 6.16M indexed passages; production snapshot 20 Oct 2026',
'6,137 NSE/BSE companies with filings OCR\'d and indexed: a data-engineering investment your team would otherwise fund.':'6K+ NSE/BSE companies in the warehouse, with structured filings and OCR where available.',
'Professional coverage lists and team workspaces':'Coverage lists; team workspaces planned',
'Product capability (live today)':'Product capability and roadmap',
'Zero-CAC discovery and recurring planning needs':'Organic discovery and recurring planning needs',
'Product-led funnel: free calculators, IPO hub and curated screens bring zero-CAC discovery, converting power users and analysts into Pro and Desk.':'Free calculators, IPO pages and curated screens are an acquisition hypothesis; conversion will be measured.',
'THE PROBLEM':'THE PROBLEM', 'WHY NOW':'WHY NOW', 'THE MOAT':'THE MOAT',
'LIVE TODAY':'LIVE TODAY', 'TRACTION':'TRACTION', 'COMPETITION':'COMPETITION',
'BUSINESS MODEL':'BUSINESS MODEL', 'THE TEAM':'THE TEAM', 'THE ASK':'THE ASK',
'chatbots hallucinate':'general-purpose AI can produce unsupported Indian financial figures',
'tax-adjusted':'costed with Indian trading charges',
'tax-and-fee-adjusted':'costed with Indian trading charges',
'100% extraction match':'50 of 50 extraction match',
}
SEED={
1:{
'Live answer, 19 Oct 2026: revenue and profit match TCS\'s NSE XBRL filing exactly':'Live answer, 19 Oct: Revenue ₹73,188 Cr, PAT ₹13,934 Cr. Operating margin 25.47%, down 67 bps YoY. Cited to NSE filing, 8 Oct 2026.',
'India\'s AI research co-pilot':'Filing-cited research for Indian advisory teams',
'Filing-cited AI answers, tax-adjusted backtests, and portfolio analysis for SEBI-registered advisers and serious investors.':'Cited company-filings answers, transparent stock screens and backtests with Indian trading charges.',
'Seed round, October 2026':'Version 1 Nov 2026 · Seed round',
'Live answer, 19 Oct: net margin = Profit After Tax / total income (₹74,525 cr). Operating margin fell 0.67% YoY.':'TCS Q2 FY27: operating margin 25.47%, down 67 bps YoY; revenue ₹73,188 Cr; PAT ₹13,934 Cr. Source: NSE filing, 8 Oct 2026.',
},
2:{
'Anvest warehouse: 15,718 (Jun) and 17,300 (Jul 2026) new announcements · SEBI intermediary directory, Oct 2026 · NSE Market Pulse, Jul 2026':f'Warehouse, announcement date: {MONTHS} · Q2 FY27 average 48,810/month · extracted 20 Oct 2026',
'Earnings, share pledges, and board notices hit NSE and BSE daily. Analysts, investment advisers, and portfolio managers still read scanned PDFs by hand.':'Exchange filings, summary screeners, backtesters and spreadsheets can leave research teams moving between disconnected sources and tools.',
'Professionals and investors jump between exchange PDFs, ratio screeners, backtesters and spreadsheets, losing hours and context at every hop.':'Important context may sit in filing text or scanned documents. Anvest links answers to indexed source passages and carries research into screens and costed tests.',
'General chatbots sound confident but hallucinate Indian financial figures. Without a verified filings database underneath, their answers cannot be trusted.':'General-purpose language models can produce unsupported figures. Anvest retrieves source passages and applies numerical checks; this reduces risk but does not guarantee error-free answers.',
'3,900 SEBI-registered firms and 13.4 crore investors don\'t lack information. They lack a trustworthy way to turn it into a decision.':'The operating model starts with a 21,750-seat professional segment. Customer demand and willingness to pay remain to be tested.',
},
3:{
'Verified live on 19 Oct 2026: this prompt generated a 516-stock screen (ROE > 15%, D/E < 1), a 1Y costed backtest and a 10-stock paper basket.':'Product replay, 19 Oct 2026: a research prompt generated a 516-stock screen, costed backtest and paper basket. This is a product test, not customer traction.',
'AI translates the question; deterministic code computes the numbers: every figure is exact and links to its source filing.':'The model interprets the request; deterministic code performs calculations. Filing answers link to source evidence, with unsupported coverage stated.',
},
4:{
'One verified filings database powering six live workflows':'Filing research, analysis and planning tools in one product',
'Every module reads from the same verified database—serving as free organic discovery that upgrades users into Individual (Plus/Pro) and Advisory Team (Desk) plans.':'The product connects filing research, screening, costed backtesting, paper trading and planning. Search-led acquisition and paid conversion are hypotheses to measure.',
},
5:{
'Built, verified and live, before any marketing':'Built from first commit to live platform in 12 months with $0 outside capital',
'3 of 3':'50 / 50',
'filing answers matched NSE XBRL exactly; a 4th correctly declined':'recent filings: revenue and PAT matched NSE XBRL (20 Oct 2026)',
'recent company filings: 100% of extracted revenue & profit matched NSE filings (20 Oct 2026)':'consolidated Q2 FY27 NSE XBRL filings: revenue/PAT extraction matched (20 Oct 2026)',
'~100':'418',
'organic sign-ups (Oct 2026), zero marketing spend':'research queries logged across 16 accounts, including internal testing',
'Nightly':'238',
'ingestion of prices, filings, NAVs and news':'saved backtest records, including internal testing',
'Verified end to end on 19 Oct 2026:  ':'Production snapshot, 20 Oct 2026:  ',
'plain-English question → 516-stock screen → 1-year costed backtest → 10-stock paper basket':'31 accounts, 2 saved screens. Usage includes founder/testing. Source checks measure extraction, not AI answer accuracy.',
'filing answers matched NSE XBRL exactly; a 4th correctly declined':'consolidated Q2 FY27 NSE XBRL filings: revenue/PAT extraction matched',
'organic sign-ups (Oct 2026), zero marketing spend':'research rows across 16 accounts; includes internal/testing activity',
'ingestion of prices, filings, NAVs and news':'saved backtest records; includes founder/testing activity',
'Built-in trust & SEBI compliance:  every answer passes a numerical source check before display, flags missing data instead of guessing, and gives zero buy/sell calls.':'Output safeguards include numerical checks against source evidence, explicit coverage limits and no buy/sell recommendations. This is not a compliance certification.',
},
6:{
'Four shifts make this the moment':'Research tools need reliable source links',
'AI can finally read corporate filings':'Filing access and validation',
'Language models can now parse complex disclosures—but financial trust requires a verified, passage-indexed filings database underneath, which Anvest has built.':'Language models can help navigate disclosures. Anvest links filing answers to indexed passages and applies deterministic numerical checks; this does not establish error-free outputs.',
'SEBI\'s new rules favor transparent logic':'Research and algo rules have distinct scopes',
'SEBI\'s April 2026 rules require exchange approval and Research Analyst licensing for opaque "black-box" signals. Because Anvest uses transparent, verifiable rules, it operates live today while licensing is underway.':'SEBI research-analyst rules address disclosure of AI use. Retail-algo requirements apply to broker activity from 1 Apr 2026; black-box providers have specific RA and empanelment requirements. Anvest backtests and paper trading are simulations.',
'Brokers are connecting accounts to AI':'Partner access remains to be scoped',
'Zerodha and peer brokers now let users link AI assistants directly to their brokerage accounts—creating urgent demand for a verified research engine that won\'t hallucinate numbers.':'Broker account access would require a partner-approved method, user consent and agreed data controls. No Anvest broker integration or pilot is agreed.',
'Rising retail & adviser scrutiny':'Initial buyer segment',
'13.4 crore retail investors are on NSE, while 3,900 SEBI-registered firms face stricter rules requiring documented, source-cited research.':'The operating model sizes 3,900 RA, PMS and IA firms for TAM and uses a narrower professional SAM. These counts do not establish customer demand.',
'Proven willingness to pay for verified AI research:  AlphaSense reached $600M+ ARR ($7.5B valuation, Jun 2026) selling filing-cited AI to global institutions. Anvest Desk brings this to Indian advisory teams at ₹2,999/seat/month (~$380/yr).':'Seed-stage model: Anvest Desk list price is ₹2,999/seat/month; Month-15 revenue, customer count and CAC recovery are planning outputs, not observed results.',
'Sources: SEBI algo circulars (Feb & Sep 2025) · Zerodha Kite AI connector · NSE Market Pulse (Jul 2026) · FinTech Global (Jun 2026)':'Sources: SEBI Research Analyst Regulations (Dec 2024 amendments); SEBI retail-algo circulars (Feb and Sep 2025); operating_model.py.',
},
7:{
'Year-5 scenario across all engines: about 1% of SAM':'Conditional Year-5 scenario: ₹23.11 Cr ARR, about 1% of SAM. Requires Series A capital, approvals, partner access, signed contracts and expansion beyond the initial professional segment.',
'Why start with advisory firms:  a concentrated, high-intent market (₹78 Cr SAM) reachable via direct outbound by 2 B2B sales reps—generating revenue from Month 3 and proving institutional credibility before scaling to retail and broker APIs.':'Why start with advisory firms: the model identifies a ₹78 Cr professional SAM and assumes direct sales. Revenue begins in the plan in Month 3; no paid customer or willingness-to-pay evidence is claimed.',
'Annual pricing: Individual (Plus) ₹2,388/yr; Advisory Team (Desk) ₹35,988/seat/yr':'Model list prices: Plus ₹2,388/year; Desk ₹35,988/seat/year. Values are model inputs, not validated willingness to pay.',
},
9:{
# Strengthen the data moat section with quantified evidence
'The chatbot is replaceable; the verified corpus is not':'The chatbot is replaceable; the self-healing verified corpus is not. Indian exchange XBRL mislabels periods and buries annual figures in Q4 footnotes; 10 of 10 tier-1 bank results filed as scanned PDFs.',
'Our moat is the self-healing filings pipeline beneath the AI':'Production pipeline repairs and indexes filing data',
'The chatbot is replaceable; the verified corpus is not':'Repair rules and source lineage reflect accumulated engineering work',
'major bank earnings in Q1 FY27 filed as scanned PDFs needing OCR':'bank filings in a Q1 FY27 sample were scanned PDFs needing OCR',
'historical NSE & BSE corporate filings indexed in our database':'corporate announcements in the warehouse',
'searchable filing passages refreshed daily with audit trails':'indexed filing passages counted on 20 Oct 2026',
'Why competitors can\'t easily bolt this on: screeners built on summary feeds cannot cite exact filing passages. On Indian exchanges, machine-readable filings (XBRL) mislabel reporting periods, bury annual numbers inside Q4 footnotes, and upload bank results as scanned PDFs—taking 12 months of custom repair rules to solve.':'The pipeline combines source ingestion, XBRL repair, OCR, cross-checks and filing lineage. Public-page comparisons are directional and do not establish what competitors can or cannot build.',
'Internal data-quality audits, Jul–Sep 2026':'Production snapshot 20 Oct 2026: 6,155,194 passages / 633,688 distinct doc_ids.',
},
10:{
'SEED STAGE FOCUS (95% OF MONTH-15 REVENUE)':'SEED MODEL MIX (95% OF MONTH-15 ARR)',
'SELF-SERVE & POST-SERIES A EXPANSION':'INDIVIDUALS & POST-SERIES A SCENARIO',
'For SEBI-registered analysts, advisers, portfolio managers & distributors: client stock watchlists, daily filing digests, cited AI research, and shared workspaces. Paying from Month 3.':'For research and advisory teams: filing research, screening and shared workflows. Model revenue starts in Month 3; no paid customers are reported today.',
'Brokers, wealth apps, and AI assistants embed Anvest\'s verified filing answers and screeners via API. Paid pilots launch in weeks; first paying partner goes live in Month 10.':'Brokers and wealth apps could embed filing answers and screeners via API, subject to partner approval and data terms. The model targets two paid partners by Month 15; none are signed.',
'₹199–₹599 / month (Pro ₹4,999 / year) · Free tools drive discovery':'Individual subscriptions · conversion remains to be measured',
'Free calculators, IPO pages, and stock screens drive organic search traffic; active investors upgrade for 150–600 monthly AI queries, costed backtesting, paper trading, and portfolio X-ray.':'Public pages and free tools are an acquisition hypothesis. Search traffic, upgrade rates and feature demand have not been documented in a dated analytics export.',
'₹250 / mo net subscription + broker revenue share (from Month 22)':'₹250 / mo net subscription + broker revenue share (scenario from Month 22)',
'Month-15 ARR run-rate of ₹87 L ($92K) on $500K raise: 75% Advisory Teams (Desk), 20% Broker APIs, 5% Individual Plans. Checkout goes live in Days 1–90.':'$500K model target at Month 15: ₹87 L ARR; 75% Desk, 20% Broker APIs, 5% individual plans. Targets and launch timing are assumptions.',
},
11:{
'Founder-led sales to 3,900 SEBI-registered advisory and research firms (starting with fast-moving 1–5 seat teams) and 3,350 top mutual fund distributors.':'Founder-led outreach is the initial route to the professional segment. The model sizes 3,900 RA/PMS/IA firms plus 3,350 top distributors; the sales list and conversion remain to be validated.',
'6,000+ stock pages, 991 fund pages, IPO hubs, and calculators answer specific filing queries on Google—converting free visitors into Plus, Pro, and Desk subscribers.':'Public stock and fund pages, IPO hubs and calculators are a search-distribution hypothesis. No dated visitor, conversion or device analytics are included.',
'Plug-and-play APIs and AI connectors embed verified research inside retail brokerage apps—reaching thousands of investors with zero paid ad spend.':'Broker and wealth APIs are a partner-distribution hypothesis; access, integration scope, pricing and adoption require partner validation.',
'Every cited answer, screen, and backtest generates a shareable public link; financial educators join on referral terms under SEBI-compliant informational rules.':'Referral and shareable-research channels remain GTM tests; no creator agreements or referral outcomes are claimed.',
'90-DAY FUNNEL & 18-MONTH MILESTONES':'PROPOSED VALIDATION MILESTONES · NOT FORECASTS',
'SEBI-registered advisory firms approached':'target firms for outreach',
'live product demos conducted':'target demos',
'paid Desk team pilots closed':'target paid pilots; none established',
'• M1–6: Checkout & 7K+ pages live; SEBI RA filed (~16 Desk teams)• M7–12: 2nd sales rep (M9); 1st broker API (M10); ~54 Desk teams• M13–18: ~99 Desk teams & 2nd API → ₹1.12 Cr ARR for Series A':'Model milestones: M3 first Desk revenue; M9 second seller; M10 first partner; M15 77 teams / ₹87 L ARR; M18 99 teams / ₹1.12 Cr ARR. These are model targets; the current company is pre-revenue.',
},
12:{
'Retail investing is going algorithmic, and Anvest is the on-ramp':'Research, testing and execution have different approval gates',
'SEBI\'s retail algorithmic rules took effect across all Indian brokers':'Retail-algo rules apply to brokers from this date; specific requirements depend on activity and provider role.',
'Why pre-trade research is the open space: trade execution is already automated, and most exchange algo volume is intraday trading. Anvest owns the transparent, fundamental & filing-driven research layer for long-term portfolios that rebalance periodically—with a clear regulatory path to broker execution in Year 2.':'Anvest currently offers research, backtesting and paper trading. Live strategy deployment is a future scenario requiring legal review, partner controls and applicable registration/empanelment; no approval is represented here.',
},
13:{
'Break-even without new funding, and a path to ~₹23 Cr ARR':'Default-alive on $500K, with Series A scale to ~₹23 Cr ARR',
'SCENARIO CONDITIONS':'SERIES A SCENARIO',
'Exit ARR run-rate, scenario built on the $500K plan. Desk and retail reach ₹13 Cr in year 5; partners and strategies add ₹9.6 Cr as their gates clear. ₹95 = $1.':'No-new-funding path: M42 break-even on $500K. Series A scenario: ₹13.4 Cr Desk/retail + ₹9.7 Cr partners/strategies ≈ ₹23.1 Cr Year-5 ARR. ₹95 = $1.',
'Profitable on $500K alone, with a Series A path to ₹23 Cr ARR':'Model target: M42 break-even on $500K; conditional Series A path to ₹23.11 Cr ARR',
'Advisory firms':'Desk teams',
'*$400K provides 31 months runway; $500K and $700K reach breakeven with zero new funding.':'* $400K case runs out of cash in M31; additional capital is needed before modeled M48 break-even. $500K and $700K cases reach modeled break-even without new funding, under plan assumptions.',
'UNIT ECONOMICS & SERIES A DRIVERS':'UNIT ECONOMICS & CONDITIONAL SERIES A SCENARIO',
'Unit economics: ₹2,245 net/seat/mo; ₹0.73L team CAC (~11-mo payback)Gross margin scales from 46% at Month 15 to 83% at Year-5 scaleSeries A (M18): 15 sales reps, 10 broker APIs & licensed baskets → ₹23.1 Cr ARR':'Model: ₹2,245 net/seat/mo; ₹0.73L team CAC; 10.8-month revenue recovery / 23.3-month gross-profit payback. Gross margin: 46% at M15, 83% at Y5. The Year-5 case assumes 14 sellers, 10 partners and required approvals.',
'Month-15 Net MRR ($500K): ₹5.5L Advisory Desk + ₹1.4L Broker APIs + ₹0.4L Individual Plans = ₹7.3L/mo (₹87L ARR), net of 18% GST (₹95 = $1).':'Month-15 net MRR on $500K: ₹5.5L Desk + ₹1.4L APIs + ₹0.4L individuals = ₹7.3L/mo (₹87L ARR), after modeled GST. Planning FX ₹95/$; all values are operating-model outputs.',
},
14:{
'A founder who has already built the hard part':'Founder-built product; first hires are in the round plan',
'Solo-built Anvest\'s corrupted-filing repair pipeline, verification engine, and 9-module platform in 12 months with zero outside capital':'Built Anvest\'s filing repair pipeline, verification workflows and live product in 12 months without outside capital.',
'Backed by automated nightly health checks, runbooks & SEBI compliance advisers.':'The round plan funds engineering, compliance work and sales hires; no external compliance-adviser bench is represented.',
},
15:{
'Raising $500K to scale advisory team sales and broker API reach':'Raising the modeled $500K target for professional adoption and partner integrations',
'Maintains a ₹51 L+ cash cushion all the way to Month-42 cash-flow breakeven':'Model low point: ₹51 L in M41; modeled cash break-even in M42, subject to sales and cost assumptions.',
'SEBI Research Analyst license secured':'SEBI RA registration target; approval is not assured',
'published AI accuracy benchmark':'published evaluation benchmark (target; not yet run)',
'Series A-ready in Months 15–18 (~₹1.12 Cr ARR run-rate)':'M18 model target: ₹1.12 Cr ARR; Series A timing and financing are not committed.',
},
17:{
'Five-year operating model and Month-15 revenue assumptions':'Five-year operating-model scenario and Month-15 assumptions',
},
17:{'Spot-check, 19 Oct 2026: TCS, HCL Technologies and Wipro answers matched their NSE XBRL filings exactly; Infosys was correctly declined before it reported. Next: a published head-to-head benchmark.':'Source audit, 20 Oct 2026: revenue and PAT matched 50 of 50 recent consolidated NSE XBRL filings. This checks extraction, not full AI answers. End-to-end AI responses governed by deterministic verification gates (see 50-Prompt Golden Evaluation Benchmark). A separate four-question live spot-check and a future independent benchmark cover answer quality.'},
19:{'Sellers include the founder. Built on the $500K plan.':'Sellers include the founder. By Years 3–5, Desk targets broader distributors, family offices and CA/wealth practices, beyond the initial 21,750-seat SAM (4,132 seats would be 19% of it).'},
}
PARTNER={
2:{'Announcement volume: Anvest warehouse, June–July 2026 (15,718 and 17,300) · SEBI F&O studies (FY25, FY26) · SEBI AI-disclosure amendments, Dec 2024':f'Warehouse, announcement date: {MONTHS} · Q2 FY27 average 48,810/month · SEBI AI-disclosure amendments, Dec 2024',
'SEBI\'s studies of retail derivatives losses and its AI-disclosure rules point to explained, accountable research. A cited answer provides that by design.':'SEBI\'s AI-disclosure rules make transparent research important. Anvest links filing answers to their source evidence.'},
3:{'Operating margin 25.47%, from 26.14% a year earlier; revenue ₹73,188 cr and profit ₹13,934 cr (quarter ended 30 Sep 2026, consolidated).':'Operating margin 25.47%, down 67 bps YoY. Revenue ₹73,188 Cr and PAT ₹13,934 Cr. Net margin 18.70% uses total income of ₹74,525 Cr (Q2 FY27, consolidated).'},
6:{
# Add data quality proof metrics to the "WHERE WE ARE" slide
'Ingestion refreshed nightly':'Ingestion refreshed nightly. 50/50 (100%) Q2 FY27 NSE XBRL extraction match. 15,899 corrupted XBRL cash-flow rows repaired.',
},
8:{
# Reframe the proposal slide: remove anti-equity line, add engineering SLAs
'Nothing about equity is part of this proposal.':'Commercial & Strategic Flexibility: Structured initially as a low-friction 8–12 week API/MCP pilot (tiered per-active-user or usage licensing). As we are concurrently opening our $500K Seed round, we also welcome strategic investment discussions with Rainmatter alongside technical evaluation.',
# Keep the proposal's evaluation criteria measurable without implying an agreed SLA.
'Answer quality, repeat use and cost per useful task':'Evaluate citation traceability, source coverage, repeat use and cost per useful task. No latency or privacy SLA is claimed; data scope and controls require partner review.',
},
}
PARTNER[10]={
    'Kite MCP means you are already building for an agent-native brokerage.':'Explore a filing-grounded research layer for Kite MCP.',
    'Anvest is the grounded research layer that future needs.':'Anvest could connect cited research to a partner-approved workflow.',
}

# Evidence-led overrides keep the original slide visuals while removing claims
# that are not supported by the dated product snapshot or operating model.
SEED[1].update({
    'Filing-cited research for Indian advisory teams':'Filing research for Indian teams',
    'Filing-cited AI answers, costed with Indian trading charges backtests, and portfolio analysis for SEBI-registered advisers and serious investors.':'Cited research and Indian-cost backtests for teams.',
    'Harsh Bhardwaj, Founder  ·  harsh@anvest.in  ·  anvest.in  ·  Version 1 Nov 2026 · Seed round':'Harsh Bhardwaj · harsh@anvest.in · anvest.in · Version 1 Nov 2026',
    'India\'s AI research co-pilot':'Filing-cited research for Indian advisory teams',
    'Filing-cited AI answers, tax-adjusted backtests, and portfolio analysis for SEBI-registered advisers and serious investors.':'Cited company-filings answers, transparent stock screens and backtests with Indian trading charges.',
    'Seed round, October 2026':'Version 1 Nov 2026 · Seed round',
    'Live answer, 19 Oct: net margin = Profit After Tax / total income (₹74,525 Cr). Operating margin fell 0.67% YoY.':'TCS Q2 FY27: revenue ₹73,188 Cr; PAT ₹13,934 Cr; net margin uses total income. Operating margin 25.47%, down 67 bps YoY. Source: NSE filing, 8 Oct 2026.',
})
SEED[2].update({
    'Earnings, share pledges, and board notices hit NSE and BSE daily. Analysts, investment advisers, and portfolio managers still read scanned PDFs by hand.':'Exchange filings, summary screeners, backtesters and spreadsheets can leave research teams moving between disconnected sources and tools.',
    'Professionals and investors jump between exchange PDFs, ratio screeners, backtesters and spreadsheets, losing hours and context at every hop.':'Important context may sit in filing text or scanned documents. Anvest links answers to indexed source passages and carries research into screens and costed tests.',
    'General chatbots sound confident but hallucinate Indian financial figures. Without a verified filings database underneath, their answers cannot be trusted.':'General-purpose language models can produce unsupported figures. Anvest retrieves source passages and applies numerical checks; this reduces risk but does not guarantee error-free answers.',
    '3,900 SEBI-registered firms and 13.4 crore investors don\'t lack information. They lack a trustworthy way to turn it into a decision.':'The operating model starts with a 21,750-seat professional segment. Customer demand and willingness to pay remain to be tested.',
})
SEED[3].update({
    'Verified live on 19 Oct 2026: this prompt generated a 516-stock screen (ROE > 15%, D/E < 1), a 1Y costed backtest and a 10-stock paper basket.':'Product replay, 19 Oct 2026: a research prompt generated a 516-stock screen, costed backtest and paper basket. This is a product test, not customer traction.',
    'AI translates the question; deterministic code computes the numbers: every figure is exact and links to its source filing.':'The model interprets the request; deterministic code performs calculations. Filing answers link to source evidence, with unsupported coverage stated.',
})
SEED[4].update({
    'One verified filings database powering six live workflows':'Filing research, analysis and planning tools in one product',
    'Every module reads from the same verified database—serving as free organic discovery that upgrades users into Individual (Plus/Pro) and Advisory Team (Desk) plans.':'The product connects filing research, screening, costed backtesting, paper trading and planning. Search-led acquisition and paid conversion are hypotheses to measure.',
    'Anvest Score, AI profile, financials and filings':'Anvest Score, AI profile, financials and filings; team workspaces planned',
})
SEED[5].update({
    'recent company filings: 100% of extracted revenue & profit matched NSE filings (20 Oct 2026)':'consolidated Q2 FY27 NSE XBRL filings: revenue/PAT extraction matched (20 Oct 2026)',
    'AI research queries logged across 16 pilot and internal test accounts':'research rows across 16 accounts; includes internal/testing activity',
    'historical strategy backtests run and saved across test accounts':'saved backtest records; includes founder/testing activity',
    'Built-in trust & SEBI compliance:  every answer passes a numerical source check before display, flags missing data instead of guessing, and gives zero buy/sell calls.':'Output safeguards include numerical checks against source evidence, explicit coverage limits and no buy/sell recommendations. This is not a compliance certification.',
})
SEED[6].update({
    'Four shifts make this the moment':'Research tools need reliable source links',
    'AI can finally read corporate filings':'Filing access and validation',
    'Language models can now parse complex disclosures—but financial trust requires a verified, passage-indexed filings database underneath, which Anvest has built.':'Language models can help navigate disclosures. Anvest links filing answers to indexed passages and applies deterministic numerical checks; this does not establish error-free outputs.',
    'SEBI\'s new rules favor transparent logic':'Research and algo rules have distinct scopes',
    'SEBI\'s April 2026 rules require exchange approval and Research Analyst licensing for opaque "black-box" signals. Because Anvest uses transparent, verifiable rules, it operates live today while licensing is underway.':'SEBI research-analyst rules address disclosure of AI use. Retail-algo requirements apply to broker activity from 1 Apr 2026; black-box providers have specific RA and empanelment requirements. Anvest backtests and paper trading are simulations.',
    'Brokers are connecting accounts to AI':'Partner access remains to be scoped',
    'Zerodha and peer brokers now let users link AI assistants directly to their brokerage accounts—creating urgent demand for a verified research engine that won\'t hallucinate numbers.':'Broker account access would require a partner-approved method, user consent and agreed data controls. No Anvest broker integration or pilot is agreed.',
    'Rising retail & adviser scrutiny':'Initial buyer segment',
    '13.4 crore retail investors are on NSE, while 3,900 SEBI-registered firms face stricter rules requiring documented, source-cited research.':'The operating model sizes 3,900 RA, PMS and IA firms for TAM and uses a narrower professional SAM. These counts do not establish customer demand.',
    'Proven willingness to pay for verified AI research:  AlphaSense reached $600M+ ARR ($7.5B valuation, Jun 2026) selling filing-cited AI to global institutions. Anvest Desk brings this to Indian advisory teams at ₹2,999/seat/month (~$380/yr).':'Seed-stage model: Anvest Desk list price is ₹2,999/seat/month; Month-15 revenue, customer count and CAC recovery are planning outputs, not observed results.',
    'Sources: SEBI algo circulars (Feb & Sep 2025) · Zerodha Kite AI connector · NSE Market Pulse (Jul 2026) · FinTech Global (Jun 2026)':'Sources: SEBI Research Analyst Regulations (Dec 2024 amendments); SEBI retail-algo circulars (Feb and Sep 2025); operating model.',
})
SEED[7].update({
    'Year-5 scenario across all engines: about 1% of SAM':'Conditional Year-5 scenario: ₹23.11 Cr ARR, about 1% of SAM. Requires Series A capital, approvals, partner access, signed contracts and expansion beyond the initial professional segment, including CA/wealth practices.',
    'Why start with advisory firms:  a concentrated, high-intent market (₹78 Cr SAM) reachable via direct outbound by 2 B2B sales reps—generating revenue from Month 3 and proving institutional credibility before scaling to retail and broker APIs.':'Why start with advisory firms: the model identifies a ₹78 Cr professional SAM and assumes direct sales. Revenue begins in the plan in Month 3; no paid customer or willingness-to-pay evidence is claimed.',
    'Annual pricing: Individual (Plus) ₹2,388/yr; Advisory Team (Desk) ₹35,988/seat/yr':'Model list prices: Plus ₹2,388/year; Desk ₹35,988/seat/year. Values are model inputs, not validated willingness to pay.',
})
SEED[9].update({
    'Our moat is the self-healing filings pipeline beneath the AI':'Production pipeline repairs and indexes filing data',
    'The chatbot is replaceable; the verified corpus is not':'Repair rules and source lineage reflect accumulated engineering work',
    'major bank earnings in Q1 FY27 filed as scanned PDFs needing OCR':'bank filings in a Q1 FY27 sample were scanned PDFs needing OCR',
    'historical NSE & BSE corporate filings indexed in our database':'corporate announcements in the warehouse',
    'searchable filing passages refreshed daily with audit trails':'indexed filing passages counted on 20 Oct 2026',
    'Why competitors can\'t easily bolt this on: screeners built on summary feeds cannot cite exact filing passages. On Indian exchanges, machine-readable filings (XBRL) mislabel reporting periods, bury annual numbers inside Q4 footnotes, and upload bank results as scanned PDFs—taking 12 months of custom repair rules to solve.':'The pipeline combines source ingestion, XBRL repair, OCR, cross-checks and filing lineage. Public-page comparisons are directional and do not establish what competitors can or cannot build.',
    'Internal data-quality audits, Jul–Sep 2026':'Production snapshot 20 Oct 2026: 6,155,194 passages / 633,688 distinct doc_ids.',
})
SEED[8]={
    'Others solve one step; Anvest connects the whole workflow':'Research tools cover different parts of the workflow',
    'Anvest connects the full workflow in one account: from a filing-verified AI answer to an editable stock screen, a costed with Indian trading charges backtest, a virtual paper portfolio, and multi-asset wealth planning.':'Anvest brings filing-linked answers, editable screens, backtests with Indian trading charges, paper portfolios and wealth planning into one research workflow.',
    "Yes = core feature · Partial = limited or adjacent · — = not found on the vendor's public product pages, checked 19 Oct 2026":'Directional category map based on public pages reviewed 19 Oct 2026; not a hands-on feature benchmark.',
}
SEED[10].update({
    'SEED STAGE FOCUS (95% OF MONTH-15 REVENUE)':'SEED MODEL MIX (95% OF MONTH-15 ARR)',
    'SELF-SERVE & POST-SERIES A EXPANSION':'INDIVIDUALS & POST-SERIES A SCENARIO',
    'For SEBI-registered analysts, advisers, portfolio managers & distributors: client stock watchlists, daily filing digests, cited AI research, and shared workspaces. Paying from Month 3.':'For research and advisory teams: filing research, screening and shared workflows. Model revenue starts in Month 3; no paid customers are reported today.',
    'Brokers, wealth apps, and AI assistants embed Anvest\'s verified filing answers and screeners via API. Paid pilots launch in weeks; first paying partner goes live in Month 10.':'Brokers and wealth apps could embed filing answers and screeners via API, subject to partner approval and data terms. The model targets two paid partners by Month 15; none are signed.',
    '₹199–₹599 / month (Pro ₹4,999 / year) · Free tools drive discovery':'Individual subscriptions · conversion remains to be measured',
    'Free calculators, IPO pages, and stock screens drive organic search traffic; active investors upgrade for 150–600 monthly AI queries, costed backtesting, paper trading, and portfolio X-ray.':'Public pages and free tools are an acquisition hypothesis. Search traffic, upgrade rates and feature demand have not been documented in a dated analytics export.',
    '₹250 / mo net subscription + broker revenue share (from Month 22)':'₹250 / mo net subscription + broker revenue share (scenario from Month 22)',
    'Month-15 ARR run-rate of ₹87 L ($92K) on $500K raise: 75% Advisory Teams (Desk), 20% Broker APIs, 5% Individual Plans. Checkout goes live in Days 1–90.':'$500K model target at Month 15: ₹87 L ARR; 75% Desk, 20% Broker APIs, 5% individual plans. Targets and launch timing are assumptions.',
})
SEED[11].update({
    'Founder-led sales to 3,900 SEBI-registered advisory and research firms (starting with fast-moving 1–5 seat teams) and 3,350 top mutual fund distributors.':'Founder-led outreach is the initial route to the professional segment. The model sizes 3,900 RA/PMS/IA firms plus 3,350 top distributors; the sales list and conversion remain to be validated.',
    '6,000+ stock pages, 991 fund pages, IPO hubs, and calculators answer specific filing queries on Google—converting free visitors into Plus, Pro, and Desk subscribers.':'Public stock and fund pages, IPO hubs and calculators are a search-distribution hypothesis. No dated visitor, conversion or device analytics are included.',
    'Plug-and-play APIs and AI connectors embed verified research inside retail brokerage apps—reaching thousands of investors with zero paid ad spend.':'Broker and wealth APIs are a partner-distribution hypothesis; access, integration scope, pricing and adoption require partner validation.',
    'Every cited answer, screen, and backtest generates a shareable public link; financial educators join on referral terms under SEBI-compliant informational rules.':'Referral and shareable-research channels remain GTM tests; no creator agreements or referral outcomes are claimed.',
    '90-DAY FUNNEL & 18-MONTH MILESTONES':'PROPOSED VALIDATION MILESTONES · NOT FORECASTS',
    'SEBI-registered advisory firms approached':'target firms for outreach',
    'live product demos conducted':'target demos',
    'paid Desk team pilots closed':'target paid pilots; none established',
    '• M1–6: Checkout & 7K+ pages live; SEBI RA filed (~16 Desk teams)• M7–12: 2nd sales rep (M9); 1st broker API (M10); ~54 Desk teams• M13–18: ~99 Desk teams & 2nd API → ₹1.12 Cr ARR for Series A':'Model milestones: M3 first Desk revenue; M9 second seller; M10 first partner; M15 77 teams / ₹87 L ARR; M18 99 teams / ₹1.12 Cr ARR. These are model targets; the current company is pre-revenue.',
})
SEED[12].update({
    'Retail investing is going algorithmic, and Anvest is the on-ramp':'Research, testing and execution have different approval gates',
    'SEBI\'s retail algorithmic rules took effect across all Indian brokers':'Retail-algo rules apply to brokers from this date; specific requirements depend on activity and provider role.',
    'Why pre-trade research is the open space: trade execution is already automated, and most exchange algo volume is intraday trading. Anvest owns the transparent, fundamental & filing-driven research layer for long-term portfolios that rebalance periodically—with a clear regulatory path to broker execution in Year 2.':'Anvest currently offers research, backtesting and paper trading. Live strategy deployment is a future scenario requiring legal review, partner controls and applicable registration/empanelment; no approval is represented here.',
})
SEED[13].update({
    'Profitable on $500K alone, with a Series A path to ₹23 Cr ARR':'Model target: M42 break-even on $500K; conditional Series A path to ₹23.11 Cr ARR',
    'Advisory firms':'Desk teams',
    '*$400K provides 31 months runway; $500K and $700K reach breakeven with zero new funding.':'* $400K case runs out of cash in M31; additional capital is needed before modeled M48 break-even. $500K and $700K cases reach modeled break-even without new funding, under plan assumptions.',
    'UNIT ECONOMICS & SERIES A DRIVERS':'UNIT ECONOMICS & CONDITIONAL SERIES A SCENARIO',
    'Unit economics: ₹2,245 net/seat/mo; ₹0.73L team CAC (~11-mo payback)Gross margin scales from 46% at Month 15 to 83% at Year-5 scaleSeries A (M18): 15 sales reps, 10 broker APIs & licensed baskets → ₹23.1 Cr ARR':'Model: ₹2,245 net/seat/mo; ₹0.73L team CAC; 10.8-month revenue recovery / 23.3-month gross-profit payback. Gross margin: 46% at M15, 83% at Y5. The Year-5 case assumes 14 sellers, 10 partners and required approvals.',
    'Month-15 Net MRR ($500K): ₹5.5L Advisory Desk + ₹1.4L Broker APIs + ₹0.4L Individual Plans = ₹7.3L/mo (₹87L ARR), net of 18% GST (₹95 = $1).':'Month-15 net MRR on $500K: ₹5.5L Desk + ₹1.4L APIs + ₹0.4L individuals = ₹7.3L/mo (₹87L ARR), after modeled GST. Planning FX ₹95/$; all values are operating-model outputs.',
})
SEED[14].update({
    'A founder who has already built the hard part':'Founder-built product; first hires are in the round plan',
    'Solo-built Anvest\'s corrupted-filing repair pipeline, verification engine, and 9-module platform in 12 months with zero outside capital':'Built Anvest\'s filing repair pipeline, verification workflows and live product in 12 months without outside capital.',
    'Backed by automated nightly health checks, runbooks & SEBI compliance advisers.':'The round plan funds engineering, compliance work and sales hires; no external compliance-adviser bench is represented.',
})
SEED[15].update({
    'Raising $500K to scale advisory team sales and broker API reach':'Raising the modeled $500K target for professional adoption and partner integrations',
    'Maintains a ₹51 L+ cash cushion all the way to Month-42 cash-flow breakeven':'Model low point: ₹51 L in M41; modeled cash break-even in M42, subject to sales and cost assumptions.',
    'SEBI Research Analyst license secured':'SEBI RA registration target; approval is not assured',
    'published AI accuracy benchmark':'published evaluation benchmark (target; not yet run)',
    'Series A-ready in Months 15–18 (~₹1.12 Cr ARR run-rate)':'M18 model target: ₹1.12 Cr ARR; Series A timing and financing are not committed.',
})
SEED[17].update({
    'Five-year operating model and Month-15 revenue assumptions':'Five-year operating-model scenario and Month-15 assumptions',
    'Spot-check, 19 Oct 2026: TCS, HCL Technologies and Wipro answers matched their NSE XBRL filings exactly; Infosys was correctly declined before it reported. Next: a published head-to-head benchmark.':'Source audit, 20 Oct 2026: revenue and PAT extraction matched 50 of 50 distinct consolidated Q2 FY27 NSE XBRL filings. This does not measure complete AI answer quality. The proposed 50-prompt suite has not been run.',
})
PARTNER[1]={
    'The grounded AI research layer for your users':'Filing-cited research for Indian brokerage users',
    'Cited answers, portfolio-aware research and tested strategies, inside the product your users already trust.':'Cited answers from company filings, with an integration path to scope subject to partner approval.',
    'Prepared for Zerodha':'Prepared for discussion · Version 1 Nov 2026',
}
PARTNER[3].update({
    'A full-universe warehouse, already built':'Production warehouse and source audit',
    '6K+ NSE/BSE companies with filings OCR\'d and indexed: a data-engineering investment your team would otherwise fund.':'Production snapshot, 20 Oct 2026: 6,155,194 indexed passages across 633,688 distinct document IDs. OCR is used where filings are scanned.',
    'Portfolio-aware, on a read-only link':'Potential portfolio-aware workflow',
    'Answers ranked by what the user owns, through your approved API, with token handling agreed with you.':'Could be scoped through a partner-approved access method, user consent and agreed data retention. No broker link is live today.',
    'From answer to action':'From answer to test',
    'Answers link to prepared screens, backtests with real costs and paper trading.':'Answers can lead to editable screens, costed backtests and simulated paper trading. Live execution is not included.',
})
PARTNER[4]={
    'Kite MCP opened the door. Anvest adds the research':'A partner-approved access path would connect holdings to filing research',
    'Kite Connect exposes account data to authorised software, and Kite MCP makes it readable by AI agents. Anvest is built to sit exactly behind that interface.':'This is a proposed integration concept. The access method, data permissions, token handling, retention and security review would be agreed with the partner before any pilot.',
    'Holdings, positions and orders: read-only and user-authorised, on terms agreed with you.':'Any holdings access would be read-only only if approved, user-authorised and scoped in a partner agreement.',
    'Every holding is matched to the filing that explains it, which turns generic research into personal research.':'A scoped product test could evaluate whether linked filing evidence improves research on selected holdings.',
    'An AI agent asks Anvest about a position it already sees and gets a cited answer, not a guess.':'A future approved agent flow could request filing-cited research. No live broker integration or permission is represented.',
}
PARTNER[6].update({
    'Partnering is the faster path to an AI research layer':'A pilot could test a filing-research layer with agreed evidence criteria',
    'A scoped pilot measures exactly this, on answer accuracy, citation quality, coverage of difficult filings and cost per answer, so the decision rests on evidence.':'A proposed pilot could measure answer quality, citation quality, coverage of selected filings, repeat use and cost per useful task. No pilot or success result is established.',
    'Ingestion refreshed nightly':'Ingestion refreshed nightly; 50/50 source-extraction match on revenue and PAT; 15,899 cash-flow rows repaired.',
})
PARTNER[7]={
    'Built, live and ready to pilot':'Built and live; partner scope remains to be agreed',
    'Full-universe filings warehouse, nightly ingestion':'Production filings warehouse; ingestion runs on a schedule',
    'Portfolio X-ray on a read-only broker link':'Portfolio tools; broker access requires an approved partner path',
    'Zerodha and Groww link pattern built; partner access agreed with you':'No broker access agreement; method and approvals remain to be scoped',
    'Next 90 days: live filing alerts  ·  broker-connected portfolios  ·  professional seats':'Potential next steps: filing alerts, an approved broker-access path and professional-seat testing',
}
PARTNER[8].update({
    'Trust you can show':'Reviewable source evidence',
    'Answers traceable to filings, with gaps disclosed. Research your compliance team can stand behind.':'Answers link to filing sources and state coverage gaps. This does not establish regulatory compliance or replace partner review.',
    'Ready for AI agents':'Potential assistant integration',
    'A grounded research layer for Kite MCP and assistants, ahead of the shift to agent-native investing.':'A proposed integration could be evaluated with an approved partner access path; no existing Kite MCP integration is claimed.',
    'A daily reason to open the app':'A research use case to test',
})
PARTNER[9]={
    'Nothing about equity is part of this proposal.':'Commercial terms would follow the pilot evidence. No equity request is part of this proposal.',
    'Answer quality, repeat use and cost per useful task':'Proposed criteria: answer quality and source citations, repeat use and cost per useful task. Access and privacy controls would be agreed and reviewed before any test.',
}

def replace_shape_text(shape,replacements):
    nodes=shape.xpath('.//a:t',namespaces=NS)
    if not nodes:return None
    old=''.join(n.text or '' for n in nodes);new=old
    for a,b in replacements.items():new=new.replace(a,b)
    if old==new:return None
    # Preserve all run formatting when replacement stays within existing runs.
    joined=''.join(n.text or '' for n in nodes)
    for a,b in replacements.items():
        if a not in joined:continue
        if any(a in (n.text or '') for n in nodes):
            for n in nodes:n.text=(n.text or '').replace(a,b)
        else:
            nodes[0].text=''.join(n.text or '' for n in nodes).replace(a,b)
            for n in nodes[1:]:n.text=''
        joined=''.join(n.text or '' for n in nodes)
    ident=shape.find('.//p:cNvPr',NS)
    return {'id':ident.get('id') if ident is not None else None,'old':old,'new':new}

def shape_text(shape):
    return ''.join(shape.xpath('.//a:t/text()',namespaces=NS))

def set_shape_text(tree,ident,value):
    shape=tree.xpath(f'//p:sp[p:nvSpPr/p:cNvPr[@id="{ident}"]]',namespaces=NS)
    if not shape:return
    nodes=shape[0].xpath('.//a:t',namespaces=NS)
    if not nodes:return
    nodes[0].text=str(value)
    for node in nodes[1:]:node.text=''

def set_cell_text(cell,value):
    nodes=cell.xpath('.//a:t',namespaces=NS)
    if not nodes:return
    nodes[0].text=str(value)
    for node in nodes[1:]:node.text=''

def rewrite_competition_table(tree):
    tables=tree.xpath('//a:tbl',namespaces=NS)
    if not tables:return
    values=[
      ['Dimension','Anvest','Summary tools','Filing tools','Technical tools','General LLMs','Review scope'],
      ['Focus','Filing-to-test','Company metrics','Filing discovery','Price/volume','Broad Q&A','Category only'],
      ['Evidence','Passage citations','Varies','Filings','Price data','Prompt context','Public pages'],
      ['Screening','Editable rules','Screener tools','Varies','Technical filters','No market rules','Not tested'],
      ['Testing','Indian charges','Varies','Varies','Strategy tests','No market data','Plan-specific'],
      ['Practice','Paper workflow','Varies','Varies','Varies','Not a simulator','Category only'],
      ['Execution','Not live','Not compared','Not compared','Product-specific','Not compared','No claim'],
      ['Workflow','Ask/cite/screen/test','Product-specific','Product-specific','Product-specific','Prompt-based','Directional'],
      ['Basis','Product snapshot','Public pages, 19 Oct','Public pages, 19 Oct','Public pages, 19 Oct','Category view','Not benchmark'],
    ]
    rows=tables[0].findall('a:tr',NS)
    for r,row in enumerate(rows):
        cells=row.findall('a:tc',NS)
        for c,cell in enumerate(cells):
            if r<len(values) and c<len(values[r]):set_cell_text(cell,values[r][c])
            for run in cell.xpath('.//a:rPr | .//a:defRPr | .//a:endParaRPr',namespaces=NS):
                run.set('sz','1150')
            cell_properties=cell.find('a:tcPr',NS)
            if cell_properties is not None:
                cell_properties.set('marT','22860')
                cell_properties.set('marB','22860')

def reorder_seed_presentation(presentation_xml,rels_xml):
    root=E.fromstring(presentation_xml);rels=E.fromstring(rels_xml)
    target_by_id={x.get('Id'):x.get('Target') for x in rels}
    sld_ids=root.find('p:sldIdLst',NS)
    by_slide={}
    for element in list(sld_ids):
        target=target_by_id.get(element.get('{%s}id'%NS['r']), '')
        match=re.search(r'slide(\d+)\.xml$',target)
        if match:by_slide[int(match.group(1))]=element
    if set(by_slide)!=set(SEED_ORDER):raise RuntimeError(f'Unexpected seed slide parts: {sorted(by_slide)}')
    sld_ids[:]=[by_slide[i] for i in SEED_ORDER]
    return E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)

def update_financial_plan(tree):
    display={
      507:f"${FIRST['raise_usd_k']}K",508:f"${TARGET['raise_usd_k']}K",509:f"${MAXIMUM['raise_usd_k']}K",
      511:inr(FIRST['arr_cr']),512:inr(TARGET['arr_cr']),513:inr(MAXIMUM['arr_cr']),
      515:FIRST['teams'],516:TARGET['teams'],517:MAXIMUM['teams'],
      519:FIRST['partners'],520:TARGET['partners'],521:MAXIMUM['partners'],
      523:f"₹{FIRST['net_burn_m15_lakh']:.1f} L",524:f"₹{TARGET['net_burn_m15_lakh']:.1f} L",525:f"₹{MAXIMUM['net_burn_m15_lakh']:.1f} L",
      527:f"M{FIRST['breakeven_month']}*",528:f"M{TARGET['breakeven_month']}",529:f"M{MAXIMUM['breakeven_month']}",
    }
    target_mrr=TARGET['rev_lakh'];scenario=MODEL['scenario_by_engine_cr']['Y5']
    display.update({
      504:f"Model target: M{TARGET['breakeven_month']} break-even on ${TARGET['raise_usd_k']}K; conditional Series A path to {inr(scenario['total'])} ARR",
      530:f"* ${FIRST['raise_usd_k']} case runs out of cash in M{FIRST['cash_out_month']}; further capital is needed before modeled M{FIRST['breakeven_month']} break-even. ${TARGET['raise_usd_k']}K and ${MAXIMUM['raise_usd_k']}K cases reach modeled break-even without new funding, under plan assumptions.",
      532:(f"Model: ₹{MODEL['pricing']['desk_net_seat_month_inr']:,.0f} net/seat/mo; ₹{TARGET['desk_cac_lakh']:.2f}L team CAC; "
          f"{TARGET['desk_payback_months_revenue']:g}-month revenue recovery / {TARGET['desk_payback_months_gm']:g}-month gross-profit payback. "
          f"Gross margin: {TARGET['gross_margin_pct']}% at M15, {MODEL['scenario_y5_gross_margin_pct']}% at Y5. Year-5 ARR: "
          f"₹{MODEL['scenario_y5_core_cr']:.1f} Cr core + ₹{MODEL['scenario_y5_conditional_cr']:.1f} Cr conditional = "
          f"{inr(scenario['total'])}; assumes {MODEL['scenario_drivers']['Y5']['sellers']} sellers, "
          f"{MODEL['scenario_drivers']['Y5']['partners']} partners and required approvals."),
      533:(f"Month-15 net MRR on ${TARGET['raise_usd_k']}K: ₹{target_mrr['desk']:.1f}L Desk + ₹{target_mrr['partners']:.1f}L APIs + "
          f"₹{target_mrr['retail']:.1f}L individuals = ₹{TARGET['mrr_lakh']:.1f}L/mo ({inr(TARGET['arr_cr'])} ARR), after modeled GST. "
          f"Planning FX ₹{MODEL['fx']:g}/$; values are operating-model outputs."),
    })
    for ident,value in display.items():set_shape_text(tree,ident,value)

def update_ask(tree):
    terms=MODEL['round_terms'];u=TARGET['use_of_funds_usd_k']
    share=lambda value:round(value/(terms['target_raise_usd']/1000)*100)
    values={
      573:f"Raising the modeled ${terms['target_raise_usd']//1000}K target for professional adoption and partner integrations",
      574:f"${terms['post_money_cap_usd']/1e6:g}M post-money valuation cap · Convertible Debentures / Preference Shares (CCD/CCPS), subject to counsel · First close ${terms['first_close_usd']//1000}K, room to ${terms['maximum_raise_usd']//1000}K",
      576:f"${u['team']}K",577:f"{share(u['team'])}%",
      581:f"${u['compliance_infra']}K",582:f"{share(u['compliance_infra'])}%",
      583:'Compliance, exchange data and cloud',
      584:'Counsel, registration and any required exchange data; permissions and approvals remain subject to review.',
      586:f"${u['growth_founder']}K",587:f"{share(u['growth_founder'])}%",
      591:f"${u['reserve_runway']}K",592:f"{share(u['reserve_runway'])}%",
      594:f"Model low point: ₹{TARGET['cash_low_cr']*100:.0f} L in M{TARGET['cash_low_month']}; modeled cash break-even M{TARGET['breakeven_month']}, subject to assumptions.",
      596:'MONTH-15 MODEL TARGETS ON THE $500K CASE',597:inr(TARGET['arr_cr']),
      598:f"modeled ARR run-rate (~${TARGET['arr_usd_k']}K; ₹{TARGET['mrr_lakh']:.1f}L net MRR)",
      599:f"{TARGET['teams']} teams",600:f"modeled Desk teams (~{TARGET['seats']} seats); not current customers",
      601:f"{TARGET['partners']} partners",602:'model target; no signed broker or wealth-app partner',
      603:'SEBI RA',604:'registration target; approval is not assured',
      605:'Evaluation',606:'50-prompt suite proposed; not yet run',
      607:f"M{TARGET['breakeven_month']}",608:'modeled cash break-even under plan assumptions',
      609:(f"${terms['first_close_usd']//1000}K case: {inr(FIRST['arr_cr'])} M15 ARR; cash-out M{FIRST['cash_out_month']} · "
          f"${terms['maximum_raise_usd']//1000}K case: {inr(MAXIMUM['arr_cr'])} M15 ARR; M{MAXIMUM['breakeven_month']} break-even"),
      610:f"M18 model target: {inr(TARGET['arr_m18_cr'])} ARR; Series A timing and financing are not committed.",
    }
    for ident,value in values.items():set_shape_text(tree,ident,value)

def update_appendix(tree):
    drivers=MODEL['scenario_drivers'];periods=['M15','Y2','Y3','Y4','Y5']
    table=tree.xpath('//a:tbl',namespaces=NS)
    if table:
        rows=table[0].findall('a:tr',NS)
        if rows:set_cell_text(rows[0].findall('a:tc',NS)[1],'Sellers (incl. founder)')
        for idx,period in enumerate(periods,1):
            if idx>=len(rows):break
            d=drivers[period];cells=rows[idx].findall('a:tc',NS)
            values=[
              rows[idx].findall('a:tc',NS)[0].xpath('string(.)'),str(d['sellers']),indian(d['mau']),str(d['retail_subs']),
              f"{indian(d['seats'])} ({MODEL['target']['teams'] if period=='M15' else ''}{' teams' if period=='M15' else ''})" if period=='M15' else indian(d['seats']),
              f"{d['partners']} ({indian(d['partner_users'])})",
              f"— (post-license)" if d['strategy_subs']==0 else indian(d['strategy_subs']),inr(d['arr_cr'])]
            for c,value in enumerate(values):
                if c<len(cells):set_cell_text(cells[c],value)
    m=drivers['M15'];y5=drivers['Y5'];rev=TARGET['rev_lakh']
    for ident,value in {
      626:'Version 1 Nov 2026 · Five-year operating-model scenario and Month-15 assumptions',
      630:(f"₹{rev['desk']:.1f}L Desk + ₹{rev['partners']:.1f}L Broker APIs + ₹{rev['retail']:.1f}L Individual Plans = "
           f"₹{TARGET['mrr_lakh']:.1f}L net MRR after modeled GST. $400K: ₹{FIRST['mrr_lakh']:.1f}L; $700K: ₹{MAXIMUM['mrr_lakh']:.1f}L."),
      633:(f"Model assumption: 4 new teams/rep/month after ramp, 3 seats/team, 2% churn. Desk team CAC ₹{TARGET['desk_cac_lakh']:.2f}L; "
           f"{TARGET['desk_payback_months_revenue']:g}-month revenue recovery and {TARGET['desk_payback_months_gm']:g}-month gross-profit payback."),
      636:(f"Year-5 case: {indian(y5['seats'])} seats = {MODEL['market']['y5_initial_professional_seat_share_pct']:g}% of the initial "
           f"{MODEL['market']['initial_professional_seats']:,}-seat SAM. Desk expands into CA/wealth practices; assumes {y5['sellers']} sellers, "
           f"{y5['partners']} partners and model portfolios at ₹{MODEL['pricing']['strategy_net_month_inr']}/mo from M{MODEL['pricing']['strategy_launch_month']}, "
           "subject to funding, contracts and applicable approvals."),
    }.items():set_shape_text(tree,ident,value)

def indian(value):
    value=str(int(value));last=value[-3:];rest=value[:-3]
    groups=[]
    while rest:groups.insert(0,rest[-2:]);rest=rest[:-2]
    return (','.join(groups)+',' if groups else '')+last

NOTES={
1:'Anvest provides filing-cited research with screening and costed backtesting. The TCS image is a dated product example tied to the NSE filing dated 8 Oct 2026.',
2:'The operating model defines the 21,750-seat initial professional segment. This is a market-sizing assumption, not a count of interested prospects or customers.',
3:'Product replay dated 19 Oct 2026: a prompt produced a 516-stock screen, costed backtest and paper basket. This is a product test, not evidence of customer use.',
4:'Live product modules are described from the product snapshot. Organic discovery and paid conversion remain hypotheses; no web analytics export was available.',
5:'Production snapshot, 20 Oct 2026: 31 accounts, 418 research rows across 16 accounts, 238 saved backtest records and 2 saved screens. Counts include founder/testing. Revenue and PAT extraction matched 50 of 50 distinct consolidated Q2 FY27 NSE XBRL filings; this is not a complete-answer benchmark.',
6:'SEBI research-analyst AI disclosure and retail-algo rules have distinct scopes. Anvest backtesting and paper trading are simulations. No regulatory approval or broker pilot is claimed.',
7:'All market size, pricing, customer, ARR and payback outputs come from the operating model. The Year-5 scenario requires later funding, approvals, partner access, contracts and expansion beyond the initial professional segment.',
8:'Public product pages were reviewed on 19 Oct 2026. The category map is directional, not a hands-on feature benchmark; a feature not shown publicly is not assumed unavailable.',
9:'Production snapshot, 20 Oct 2026: 6,155,194 indexed passages across 633,688 distinct document IDs. Pipeline audit recorded 15,899 recovered cash-flow rows and 3,608 conflicting figures flagged across 1,022 companies.',
10:'The $500K case is a model plan, not current revenue. No paid Desk customers, partner contracts or checkout launch are claimed. Individual upgrades and partner integrations remain to be measured.',
11:'The sales counts are proposed validation milestones, not a forecast. Web analytics are omitted because no dated export was supplied.',
12:'Live strategy execution is a future scenario. Any implementation would require legal review, an approved partner path and applicable registrations and exchange permissions.',
13:'The $500K case reaches modeled M42 break-even with a ₹0.51 Cr cash low point in M41. The $400K case runs out of cash in M31. The Year-5 case assumes Series A funding near M18.',
14:'The founder is currently employed and plans to work full-time on Anvest from round close. The compliance-adviser bench is not represented as assembled.',
15:'Use of funds follows the operating model: $185K team, $65K compliance/infrastructure, $100K growth/founder and $150K reserve. Month-15 milestones are targets, not current outcomes.',
16:'The QR code opens a public screen for a product walkthrough. The deck makes no live-execution or investor-usage claim.',
17:'The Year-5 scenario expands Desk beyond the initial professional segment; 4,132 seats equal 19% of the initial 21,750-seat SAM. The scenario requires the stated funding, commercial and regulatory gates.',
}

def prepare(name,edits):
    source=ROOT/'Strategy/Investor_Materials'/f'{name}.pptx'
    candidate=BUILD/f'{name}.preserved.pptx';spec=[]
    with ZipFile(source) as z,ZipFile(candidate,'w',ZIP_DEFLATED) as out:
        for n in z.namelist():
            b=z.read(n)
            if n=='ppt/presentation.xml' and name=='Anvest_Seed_Deck':
                b=reorder_seed_presentation(b,z.read('ppt/_rels/presentation.xml.rels'))
            elif re.match(r'ppt/(slides|slideLayouts|notesSlides)/[^/]+\.xml$',n):
                tree=E.fromstring(b);m=re.match(r'ppt/slides/slide(\d+)\.xml$',n)
                slide=int(m[1]) if m else None
                repl={**COMMON,**edits.get(slide,{})}
                before={shape.find('.//p:cNvPr',NS).get('id'):shape_text(shape)
                        for shape in tree.xpath('//p:sp',namespaces=NS) if shape.find('.//p:cNvPr',NS) is not None}
                for shape in tree.xpath('//p:sp',namespaces=NS):
                    replace_shape_text(shape,repl)
                for node in tree.xpath('//a:tbl//a:t',namespaces=NS):
                    value=node.text or ''
                    for old,new in repl.items():value=value.replace(old,new)
                    node.text=value
                if name=='Anvest_Seed_Deck' and slide==8:
                    rewrite_competition_table(tree)
                if name=='Anvest_Seed_Deck' and slide==13:
                    update_financial_plan(tree)
                if name=='Anvest_Seed_Deck' and slide==15:
                    update_ask(tree)
                if name=='Anvest_Seed_Deck' and slide==17:
                    update_appendix(tree)
                if n.startswith('ppt/notesSlides/'):
                    note_match=re.search(r'notesSlide(\d+)\.xml$',n)
                    note_number=int(note_match.group(1)) if note_match else None
                    texts=tree.xpath('//a:t',namespaces=NS)
                    if texts and note_number in NOTES:
                        texts[0].text=NOTES[note_number]
                        for x in texts[1:]:x.text=''
                if slide is not None:
                    new_by_id={shape.find('.//p:cNvPr',NS).get('id'):shape_text(shape)
                               for shape in tree.xpath('//p:sp',namespaces=NS) if shape.find('.//p:cNvPr',NS) is not None}
                    new_index=(SEED_ORDER.index(slide)+1) if name=='Anvest_Seed_Deck' else slide
                    for ident,old_text in before.items():
                        new_text=new_by_id.get(ident,old_text)
                        if new_text!=old_text:spec.append({'slide':new_index,'source_slide':slide,'id':ident,'old':old_text,'new':new_text})
                b=E.tostring(tree,xml_declaration=True,encoding='UTF-8',standalone=True)
            elif n=='[Content_Types].xml':
                tree=E.fromstring(b)
                for item in list(tree):
                    target=item.get('PartName')
                    if target and target.lstrip('/') not in z.namelist():tree.remove(item)
                b=E.tostring(tree,xml_declaration=True,encoding='UTF-8',standalone=True)
            elif n.startswith('ppt/charts/') and n.endswith('.xml'):
                # Axis ids are unsigned 32-bit in OOXML. Preserve their relationships.
                b=re.sub(rb'(val=")(-\d+)(")',lambda m:m[1]+str(int(m[2])%2**32).encode()+m[3],b)
                chart=E.fromstring(b);cns={'c':'http://schemas.openxmlformats.org/drawingml/2006/chart'}
                for series,engine in zip(chart.xpath('//c:ser',namespaces=cns),ENGINES):
                    for node,period in zip(series.xpath('./c:val//c:pt/c:v',namespaces=cns),PERIODS):
                        node.text=str(MODEL['scenario_by_engine_cr'][period][engine])
                for node in chart.xpath('//c:cat//c:v',namespaces=cns):
                    if node.text:node.text=node.text.replace('₹23.0 Cr',inr(MODEL['scenario_arr_cr']['Y5']))
                b=E.tostring(chart,xml_declaration=True,encoding='UTF-8',standalone=True)
            elif n=='ppt/embeddings/Microsoft_Excel_Sheet1.xlsx':
                buffer=io.BytesIO()
                with ZipFile(io.BytesIO(b)) as workbook,ZipFile(buffer,'w',ZIP_DEFLATED) as dest:
                    for part in workbook.namelist():
                        data=workbook.read(part)
                        if part=='xl/worksheets/sheet1.xml':
                            sheet=E.fromstring(data);sns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
                            for col,engine in zip('BCDE',ENGINES):
                                for row,period in enumerate(PERIODS,2):
                                    cell=sheet.find(f'.//s:c[@r="{col}{row}"]/s:v',sns)
                                    if cell is not None:cell.text=str(MODEL['scenario_by_engine_cr'][period][engine])
                            data=E.tostring(sheet,xml_declaration=True,encoding='UTF-8',standalone=True)
                        if part.endswith('.xml'):
                            xml=E.fromstring(data)
                            for node in xml.xpath('//*[local-name()="t"]'):
                                if node.text:node.text=node.text.replace('₹23.0 Cr',inr(MODEL['scenario_arr_cr']['Y5']))
                            data=E.tostring(xml,xml_declaration=True,encoding='UTF-8',standalone=True)
                        dest.writestr(part,data)
                b=buffer.getvalue()
            out.writestr(n,b)
    spec_path=BUILD/f'{name}.edits.json';spec_path.write_text(json.dumps(spec,indent=2)+'\n')
    print(name,len(spec),'edited shapes')
if __name__=='__main__':
    BUILD.mkdir(parents=True,exist_ok=True)
    prepare('Anvest_Seed_Deck',SEED);prepare('Anvest_Strategic_Integration_Deck',PARTNER)
