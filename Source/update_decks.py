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
PERIODS=["M15","Y2","Y3","Y4","Y5"]
ENGINES=["desk","retail","partners","strategies"]
ROOT=Path(__file__).resolve().parents[2]
BUILD=ROOT/'.tmp/investor-materials-20261020'
NS={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main'}
MONTHS='Jul 45,997 · Aug 61,875 · Sep 38,558 (2026)'
COMMON={
'Default-alive on $500K, with Series A scale to ~₹23 Cr ARR':'Default-alive on $500K, Series A path to ~₹23 Cr ARR',
'A $1.3B market: professionals first, active investors at scale':'A $1.3B market, starting with professional teams',
'Only Anvest':'Anvest',
'Zero-CAC':'Organic',
'zero-CAC':'organic',
'₹9.6 Cr':'₹9.7 Cr',
'₹23.0 Cr':'₹23.1 Cr',
'6,137':'6K+',
'Version 19 Oct 2026 (r5)':'20 Oct 2026',
'2.89M':'2.94M',
'~17K':'~49K',
'new filings ingested a month':'announcements/month, Q2 FY27',
'~17,000':'~49,000',
'new filings to track every month':'announcements/month, Q2 FY27',
'new filings every month':'announcements/month, Q2 FY27',
'6,137 stock pages with AI profiles':'6K+ stock pages; 6,119 AI profiles',
'6,137 companies, 2.89M announcements and 1.35M indexed passages, refreshed nightly':'6K+ companies, 2.94M announcements and 1.35M indexed passages; nightly ingestion',
'6,137 NSE/BSE companies with filings OCR\'d and indexed: a data-engineering investment your team would otherwise fund.':'6K+ NSE/BSE companies in the warehouse, with structured filings and OCR where available.',
'Professional coverage lists and team workspaces':'Coverage lists; team workspaces planned',
'Product capability (live today)':'Product capability and roadmap',
'Zero-CAC discovery and recurring planning needs':'Organic discovery and recurring planning needs',
'Product-led funnel: free calculators, IPO hub and curated screens bring zero-CAC discovery, converting power users and analysts into Pro and Desk.':'Free calculators, IPO pages and curated screens support organic discovery. Conversion into Pro and Desk will be measured after launch.',
}
SEED={
1:{
'Live answer, 19 Oct 2026: revenue and profit match TCS\'s NSE XBRL filing exactly':'Live answer, 19 Oct: net margin = PAT / total income (₹74,525 Cr). Operating margin fell 67 bps YoY.',
},
2:{'Anvest warehouse: 15,718 (Jun) and 17,300 (Jul 2026) new announcements · SEBI intermediary directory, Oct 2026 · NSE Market Pulse, Jul 2026':f'Warehouse, announcement date: {MONTHS} · Q2 FY27 average 48,810/month · extracted 20 Oct 2026'},
5:{
'Built, verified and live, before any marketing':'Built and live, with auditable source checks',
'3 of 3':'50 / 50',
'filing answers matched NSE XBRL exactly; a 4th correctly declined':'recent filings: revenue and PAT matched NSE XBRL (20 Oct 2026)',
'~100':'418',
'organic sign-ups (Oct 2026), zero marketing spend':'research queries logged across 16 accounts, including internal testing',
'Nightly':'238',
'ingestion of prices, filings, NAVs and news':'saved backtest records, including internal testing',
'Verified end to end on 19 Oct 2026:  ':'Production snapshot, 20 Oct 2026:  ',
'plain-English question → 516-stock screen → 1-year costed backtest → 10-stock paper basket':'31 accounts, 2 saved screens. Usage includes founder/testing. Source checks measure extraction, not AI answer accuracy.',
},
7:{'Year-5 scenario across all engines: about 1% of SAM':'Year-5 scenario across all engines: ~1% of SAM. Desk expands beyond the initial professional segment.'},
13:{
'Break-even without new funding, and a path to ~₹23 Cr ARR':'Default-alive on $500K, with Series A scale to ~₹23 Cr ARR',
'SCENARIO CONDITIONS':'SERIES A SCENARIO',
'Exit ARR run-rate, scenario built on the $500K plan. Desk and retail reach ₹13 Cr in year 5; partners and strategies add ₹9.6 Cr as their gates clear. ₹95 = $1.':'No-new-funding path: M42 break-even on $500K. Series A scenario: ₹13.4 Cr Desk/retail + ₹9.6 Cr partners/strategies ≈ ₹23.0 Cr Year-5 ARR. ₹95 = $1.',
},
17:{'Spot-check, 19 Oct 2026: TCS, HCL Technologies and Wipro answers matched their NSE XBRL filings exactly; Infosys was correctly declined before it reported. Next: a published head-to-head benchmark.':'Source audit, 20 Oct 2026: revenue and PAT matched 50 of 50 recent consolidated NSE XBRL filings. This checks extraction, not full AI answers. A separate four-question live spot-check and a future independent benchmark cover answer quality.'},
19:{'Sellers include the founder. Built on the $500K plan.':'Sellers include the founder. By Years 3–5, Desk targets broader distributors, family offices and CA/wealth practices, beyond the initial 21,750-seat SAM (4,132 seats would be 19% of it).'},
}
PARTNER={
2:{'Announcement volume: Anvest warehouse, June–July 2026 (15,718 and 17,300) · SEBI F&O studies (FY25, FY26) · SEBI AI-disclosure amendments, Dec 2024':f'Warehouse, announcement date: {MONTHS} · Q2 FY27 average 48,810/month · SEBI AI-disclosure amendments, Dec 2024',
'SEBI\'s studies of retail derivatives losses and its AI-disclosure rules point to explained, accountable research. A cited answer provides that by design.':'SEBI\'s AI-disclosure rules make transparent research important. Anvest links filing answers to their source evidence.'},
3:{'Operating margin 25.47%, from 26.14% a year earlier; revenue ₹73,188 cr and profit ₹13,934 cr (quarter ended 30 Sep 2026, consolidated).':'Operating margin 25.47%, down 67 bps YoY. Revenue ₹73,188 Cr and PAT ₹13,934 Cr. Net margin 18.70% uses total income of ₹74,525 Cr (Q2 FY27, consolidated).'},
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

def prepare(name,edits):
    source=ROOT/'Strategy/Investor_Materials'/f'{name}.pptx'
    candidate=BUILD/f'{name}.preserved.pptx';spec=[]
    with ZipFile(source) as z,ZipFile(candidate,'w',ZIP_DEFLATED) as out:
        for n in z.namelist():
            b=z.read(n)
            if re.match(r'ppt/(slides|slideLayouts|notesSlides)/[^/]+\.xml$',n):
                tree=E.fromstring(b);m=re.match(r'ppt/slides/slide(\d+)\.xml$',n)
                slide=int(m[1]) if m else None
                repl={**COMMON,**edits.get(slide,{})}
                for shape in tree.xpath('//p:sp',namespaces=NS):
                    change=replace_shape_text(shape,repl)
                    if change and slide:spec.append({'slide':slide,**change})
                if slide==19:
                    for shape in tree.xpath('//p:sp',namespaces=NS):
                        text=''.join(shape.xpath('.//a:t/text()',namespaces=NS))
                        if text.startswith('Sellers include the founder. By Years'):
                            shape.find('.//a:ext',NS).set('cx','11094415')
                            shape.find('.//a:ext',NS).set('cy','329184')
                if slide==19:
                    changed={'2 (9,305)':'2 (9,593)','4 (36,590)':'4 (37,466)','6 (92,641)':'6 (94,213)','8 (1,94,813)':'8 (1,97,638)','10 (3,78,301)':'10 (3,83,373)','352':'362','2,761':'2,810','7,194':'7,296','15,158':'15,349','₹23.0 Cr':'₹23.1 Cr'}
                    for node in tree.xpath('//a:t',namespaces=NS):
                        if node.text in changed:node.text=changed[node.text]
                # Table cells also carry investor copy and must follow the same corrections.
                for node in tree.xpath('//a:tbl//a:t',namespaces=NS):
                    value=node.text or ''
                    for old,new in repl.items():value=value.replace(old,new)
                    node.text=value
                if name=='Anvest_Strategic_Integration_Deck' and slide==2:
                    for node in tree.xpath('//a:t',namespaces=NS):
                        if node.text=='research is where regulation is heading':node.text='research backed by sources'
                if name=='Anvest_Strategic_Integration_Deck' and slide==3:
                    for node in tree.xpath('//a:t',namespaces=NS):
                        if node.text=='LIVE ANSWER  ·  19 OCT 2026':node.text='SOURCE-CHECKED RESULTS · Q2 FY27'
                # Speaker-note claims are refreshed separately without internal work logs.
                for node in tree.xpath('//a:t',namespaces=NS):
                    t=node.text or ''
                    t=re.sub(r'Version 19 Oct 2026 \(r5\)','20 Oct 2026',t)
                    t=t.replace('2.89M','2.94M')
                    if n.startswith('ppt/notesSlides/'):
                        t=t.replace('About 100 people signed up with no marketing;','Production snapshot, 20 October: 31 registered accounts and 418 queries across 16 accounts, including founder and test activity;')
                        t=t.replace('₹13 Cr','₹13.4 Cr').replace('₹9.6 Cr','₹9.7 Cr').replace('₹23.0 Cr','₹23.1 Cr')
                    node.text=t
                if n=='ppt/notesSlides/notesSlide5.xml':
                    texts=tree.xpath('//a:t',namespaces=NS)
                    if texts:
                        texts[0].text='Production snapshot, 20 October 2026: 31 registered accounts, 418 logged research queries across 16 accounts, 238 saved backtest records and 2 saved screens. These totals include founder and testing activity and do not establish retention or paying demand. Revenue and PAT matched the original NSE XBRL for 50 recent consolidated results. The audit measures source-data extraction, not 50 complete AI answers. The earlier four-question live spot-check remains separate.'
                        for x in texts[1:]:x.text=''
                if n=='ppt/notesSlides/notesSlide19.xml':
                    texts=tree.xpath('//a:t',namespaces=NS)
                    if texts and 'By Years 3–5' not in (texts[0].text or ''):texts[0].text=(texts[0].text or '')+' By Years 3–5 the Desk sales assumption expands beyond the initial 7,250 firms into broader distributors, family offices and CA/wealth practices. 4,132 seats equal 19% of the initial 21,750-seat segment, so this expansion is a condition of the scenario. The model includes salaries for all added sellers and higher marketing spend. Scenario cash excludes an unpriced Series A.'
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
                    if node.text:node.text=node.text.replace('₹23.0 Cr','₹23.1 Cr')
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
                                if node.text:node.text=node.text.replace('₹23.0 Cr','₹23.1 Cr')
                            data=E.tostring(xml,xml_declaration=True,encoding='UTF-8',standalone=True)
                        dest.writestr(part,data)
                b=buffer.getvalue()
            out.writestr(n,b)
    spec_path=BUILD/f'{name}.edits.json';spec_path.write_text(json.dumps(spec,indent=2)+'\n')
    print(name,len(spec),'edited shapes')
if __name__=='__main__':
    BUILD.mkdir(parents=True,exist_ok=True)
    prepare('Anvest_Seed_Deck',SEED);prepare('Anvest_Strategic_Integration_Deck',PARTNER)
