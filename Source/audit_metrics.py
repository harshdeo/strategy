"""Read-only production metrics. No account identifiers or question text are exported."""
import json, shlex, subprocess
from pathlib import Path
SQL = """select json_build_object('as_of',now(),
'announcement_months',(select json_agg(t) from (select to_char(announcement_date at time zone 'Asia/Kolkata','YYYY-MM') as month_key,count(*) as n from corporate_announcements where announcement_date >= '2026-07-01 00:00:00+05:30' and announcement_date < '2026-10-01 00:00:00+05:30' group by 1 order by 1)t),
'announcements',(select count(*) from corporate_announcements),
'dashboard_symbols',(select count(distinct symbol) from stock_dashboard_cache),
'profiles',(select count(distinct symbol) from stock_profiles where nullif(trim(short_summary),'') is not null),
'users',(select count(*) from users), 'queries',(select count(*) from research_copilot_logs),
'query_accounts',(select count(distinct user_id) from research_copilot_logs),
'saved_screens',(select count(*) from screener_queries),'saved_backtests',(select count(*) from backtests),
'financials',(select json_agg(t) from (select s.symbol,f.period_end_date,f.is_consolidated,f.filing_date,f.source,f.revenue_operations,f.total_revenue,f.operating_profit,f.pat,f.xbrl_link from financials_quarterly f join symbols s on s.id=f.symbol_id where s.symbol='TCS' and f.period_end_date in ('2026-09-30','2025-09-30') order by f.period_end_date desc,f.is_consolidated desc)t));"""
def remote_sql(sql):
    remote = 'sudo docker exec -e ' + shlex.quote('PGOPTIONS=-c default_transaction_read_only=on -c statement_timeout=30000') + ' anvest-cloud-stage-postgres-1 psql -U postgres -d anvest_import_20261013 -X -Atc ' + shlex.quote(sql)
    return subprocess.check_output(['gcloud','compute','ssh','anvest-gcp-stage','--project=anvest-505415','--zone=asia-south1-a','--tunnel-through-iap','--command='+remote],text=True)
if __name__ == '__main__':
    result = json.loads(remote_sql(SQL))
    Path(__file__).with_name('evidence_snapshot.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
