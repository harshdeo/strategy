"""Dated read-only snapshot for the November materials. Aggregates only; nothing identifies a user.

Reuses the definitions in product_metrics.py and writes a new file rather than replacing the 20 October
snapshot, because earlier materials cite that result.

    ANVEST_INTERNAL_EMAILS="a@example.com,b@example.com" python3 product_metrics_20261101.py
"""
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import product_metrics as pm

HERE = Path(__file__).parent
IST = timezone(timedelta(hours=5, minutes=30))
STAMP = datetime.now(IST).strftime("%Y%m%d")


def activity_sql():
    internal = pm.internal_clause()
    return f"""
with u as (select id, {internal} as internal, created_at from users),
act as (
  select user_id, created_at as ts, 'research' as w from research_copilot_logs
  union all select user_id, created_at, 'saved_screen' from screener_queries
  union all select user_id, created_at, 'paper_order' from paper_trading_orders
  union all select user_id, created_at, 'planning' from planning_scenarios
  union all select user_id, created_at, 'simulator' from scenario_simulation_runs
  union all select user_id, created_at, 'hypothesis' from hypotheses
),
ext as (select a.* from act a join u on u.id = a.user_id where not u.internal)
select json_build_object(
  'as_of', now(),
  'external_active_last_30d', (select count(distinct user_id) from ext where ts >= now() - interval '30 days'),
  'external_active_last_7d', (select count(distinct user_id) from ext where ts >= now() - interval '7 days'),
  'external_research_rows_last_30d', (select count(*) from ext where w = 'research' and ts >= now() - interval '30 days'),
  'external_research_users_last_30d', (select count(distinct user_id) from ext where w = 'research' and ts >= now() - interval '30 days'),
  'new_external_last_30d', (select count(*) from u where not internal and created_at >= now() - interval '30 days'),
  'new_external_by_day_last_21d', (select json_object_agg(d, n) from (
      select to_char(created_at at time zone 'Asia/Kolkata','YYYY-MM-DD') d, count(*) n from u
      where not internal and created_at >= now() - interval '21 days' group by 1 order by 1) t),
  'external_research_rows_by_ist_month', (select json_object_agg(m, n) from (
      select to_char(ts at time zone 'Asia/Kolkata','YYYY-MM') m, count(*) n from ext where w = 'research' group by 1 order by 1) t),
  'external_research_users_by_ist_month', (select json_object_agg(m, n) from (
      select to_char(ts at time zone 'Asia/Kolkata','YYYY-MM') m, count(distinct user_id) n from ext where w = 'research' group by 1 order by 1) t)
);"""


PEAK_SQL = """
with d as (
  select (announcement_date at time zone 'Asia/Kolkata')::date as day, count(*) n
  from corporate_announcements
  where announcement_date >= '2026-07-01 00:00:00+05:30' and announcement_date < '2026-11-01 00:00:00+05:30'
  group by 1
)
select json_build_object(
  'as_of', now(),
  'top_days', (select json_agg(t) from (select day, n from d order by n desc limit 8) t),
  'median_day', (select percentile_cont(0.5) within group (order by n) from d),
  'by_ist_month', (select json_object_agg(m, n) from (
      select to_char(day,'YYYY-MM') m, sum(n) n from d group by 1 order by 1) t),
  'latest_announcement_ist', (select to_char(max(announcement_date) at time zone 'Asia/Kolkata','YYYY-MM-DD HH24:MI') from corporate_announcements)
);"""

FRESHNESS_SQL = """
select json_build_object(
  'as_of', now(),
  'latest_price_date', (select max(date) from ohlcv_daily where date <= current_date),
  'latest_q2fy27_results_filing', (select max(filing_date) from financials_quarterly where period_end_date = '2026-09-30'),
  'q2fy27_consolidated_or_standalone_rows', (select count(*) from financials_quarterly where period_end_date = '2026-09-30'),
  'q2fy27_distinct_symbols', (select count(distinct symbol_id) from financials_quarterly where period_end_date = '2026-09-30')
);"""


def try_sql(sql):
    try:
        return pm.sql_json(sql)
    except Exception as exc:  # a missing column must not lose the other sections
        return {"error": str(exc)[:300]}


if __name__ == "__main__":
    qdrant = pm.gcloud(pm.QDRANT_SH).split("\n")
    result = {
        "users_and_usage": try_sql(pm.users_sql()),
        "activity": try_sql(activity_sql()),
        "coverage": try_sql(pm.COVERAGE_SQL),
        "announcements": try_sql(pm.ANNOUNCEMENTS_SQL),
        "peak_days": try_sql(PEAK_SQL),
        "freshness": try_sql(FRESHNESS_SQL),
        "public_pages_in_sitemap": pm.sitemap_pages(),
        "qdrant_corporate_announcements": {
            "passages_exact": json.loads(qdrant[0])["result"]["count"],
            "distinct_doc_id": int(qdrant[1]),
            "distinct_ticker": int(qdrant[2]),
        },
    }
    out = HERE / f"product_metrics_snapshot_{STAMP}.json"
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(out)
    print(json.dumps(result, indent=2))
