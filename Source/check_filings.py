"""Independent source check of revenue and PAT in 50 recent quarterly filings.

Reads a frozen production extract, downloads each cited NSE XBRL, independently
checks context dates, quarter duration, unit and values against stored line items.
No model calls or DB writes. This tests line-item extraction, not full AI answers.
Failures and unavailable sources fail closed. Run with --input PATH --output PATH.
"""
import argparse, concurrent.futures, hashlib, json, urllib.request
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from lxml import etree as E

def check(row):
    result = {k:row[k] for k in ('symbol','period_end_date','filing_date','xbrl_link','is_consolidated')}
    try:
        req=urllib.request.Request(row['xbrl_link'],headers={'User-Agent':'Mozilla/5.0'})
        data=urllib.request.urlopen(req,timeout=30).read()
        root=E.fromstring(data,parser=E.XMLParser(resolve_entities=False,no_network=True))
        result['source_sha256']=hashlib.sha256(data).hexdigest()
        result['checks']={}
        basis=root.xpath('//*[local-name()="NatureOfReportStandaloneConsolidated"]/text()')
        if not basis or any(v.strip().lower()!='consolidated' for v in basis):raise ValueError('source basis is not consolidated')
        for field in ('revenue_operations','pat'):
            prov=row['raw_xbrl_data']['_parser_provenance']['selected_facts'][field]
            context=prov['context_id'];concept=prov['concept']
            facts=root.xpath('//*[local-name()=$concept and @contextRef=$context]',concept=concept,context=context)
            if len(facts)!=1: raise ValueError(f'{field}: expected one source fact, got {len(facts)}')
            fact=facts[0]
            contexts=root.xpath('//*[local-name()="context" and @id=$context]',context=context)
            if len(contexts)!=1:raise ValueError('context missing/ambiguous')
            c=contexts[0];starts=c.xpath('.//*[local-name()="startDate"]/text()');ends=c.xpath('.//*[local-name()="endDate"]/text()')
            if starts!=['2026-07-01'] or ends!=[row['period_end_date']]: raise ValueError(f'{field}: wrong quarter context')
            if c.xpath('.//*[local-name()="explicitMember" or local-name()="typedMember"]'):raise ValueError('dimensional fact')
            unit=root.xpath('//*[local-name()="unit" and @id=$uid]//*[local-name()="measure"]/text()',uid=fact.get('unitRef'))
            if len(unit)!=1 or not unit[0].endswith(':INR'): raise ValueError(f'non-INR unit: {unit}')
            actual=Decimal(fact.text);expected=Decimal(str(row[field]))
            if actual!=expected: raise ValueError(f'{field}: source {actual}, warehouse {expected}')
            result['checks'][field]={'value_inr':str(actual),'concept':concept,'context':context,'unit':unit[0]}
        result['status']='pass'
    except Exception as exc: result.update(status='fail',error=f'{type(exc).__name__}: {exc}')
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--output',required=True);a=p.parse_args()
    rows=json.loads(Path(a.input).read_text())
    if len(rows)!=50 or len({r['symbol'] for r in rows})!=50:raise SystemExit('Expected 50 distinct companies')
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex: results=list(ex.map(check,rows))
    report={'as_of':datetime.now(timezone.utc).isoformat(),'scope':'50 recent consolidated Q2 FY27 NSE XBRL filings, revenue and PAT only; not a live-answer benchmark','sample_rule':'latest filing_date descending, symbol ascending; 50 distinct companies with both line items and XBRL link','passed':sum(r['status']=='pass' for r in results),'total':len(results),'results':results}
    Path(a.output).write_text(json.dumps(report,indent=2)+'\n');print(f"{report['passed']}/{len(results)} source checks passed")
    raise SystemExit(0 if report['passed']==len(results) else 1)
