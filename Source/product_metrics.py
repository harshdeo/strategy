"""Read-only product and data metrics with one written definition per figure (DATA-01..06).

Aggregates only: no email, user id, question text or filing content leaves the database, and the
snapshot written next to this file never contains the internal-account list.

    ANVEST_INTERNAL_EMAILS="founder@example.com,other@example.com" python3 product_metrics.py

Internal accounts are the addresses in ANVEST_INTERNAL_EMAILS, any @anvest.in address and any
address that looks like an automated-test account (e2e, playwright, +test, @example.). Anything else is
external. Set the variable at run time; it is not stored.

Definitions (each is also in PRODUCT_DATA_BUG_BACKLOG_2026-10-20.md):
  registered   a row in users now. Deleted accounts leave no row; users_id_seq shows how many ids were ever issued.
  external     registered and not internal.
  activated    external with at least one row in a workflow table (a question answered, a backtest
               stored, a screen saved, a paper order, a planning scenario, a simulation, a hypothesis).
  retained     activated with workflow activity on two or more IST calendar weeks.
  attempts     not recorded for most workflows. Only completed work is stored: backtests.status is
               COMPLETED on every row and a failed request leaves no row, so success rate is unknowable.
               Most stored backtests (158 of 238) have no strategy owner, so they cannot be attributed to a user.
  page         a stock URL in the public sitemap (the SEO directory), counted over HTTPS.
  profile      a stock_profiles row with a non-empty short_summary, joined to a page by symbol.
  announcement a corporate_announcements row, counted by announcement_date in IST; ingested rows are
               counted separately by created_at, and distinct attachment URLs separately again.
  passage      one Qdrant point in collection corporate_announcements; filing = distinct doc_id.
"""
import json
import os
import re
import shlex
import subprocess
import urllib.request
from pathlib import Path

HERE = Path(__file__).parent
PG = "anvest-cloud-stage-postgres-1"
DB = "anvest_import_20261013"


def gcloud(command):
    return subprocess.check_output(
        ["gcloud", "compute", "ssh", "anvest-gcp-stage", "--project=anvest-505415", "--zone=asia-south1-a",
         "--tunnel-through-iap", "--quiet", "--command=" + command],
        text=True,
    )


def sql_json(sql):
    env = shlex.quote("PGOPTIONS=-c default_transaction_read_only=on -c statement_timeout=60000")
    out = gcloud(f"sudo docker exec -e {env} {PG} psql -U postgres -d {DB} -X -Atc {shlex.quote(sql)}")
    return json.loads(out)


def internal_clause():
    raw = [e.strip().lower() for e in os.environ.get("ANVEST_INTERNAL_EMAILS", "").split(",") if e.strip()]
    for e in raw:
        if not re.fullmatch(r"[a-z0-9._+\-]+@[a-z0-9.\-]+", e):
            raise SystemExit(f"not an email address: {e!r}")
    listed = "array[" + ",".join("'" + e + "'" for e in raw) + "]::text[]" if raw else "array[]::text[]"
    return (f"(lower(email) = any({listed}) or email ilike '%@anvest.in' "
            "or email ~* '(e2e|playwright|\\+test|@example\\.)')")


def users_sql():
    internal = internal_clause()
    return f"""
with u as (select id, {internal} as internal, auth_provider, email_verified, created_at from users),
act as (
  select user_id, created_at as ts, 'research' as w from research_copilot_logs
  union all select s.user_id, b.created_at at time zone 'UTC', 'backtest' from backtests b join strategies s on s.id = b.strategy_id
  union all select user_id, created_at, 'saved_screen' from screener_queries
  union all select user_id, created_at, 'paper_order' from paper_trading_orders
  union all select user_id, created_at, 'planning' from planning_scenarios
  union all select user_id, created_at, 'simulator' from scenario_simulation_runs
  union all select user_id, created_at, 'hypothesis' from hypotheses
),
per_user as (
  select user_id, min(ts) first_ts, max(ts) last_ts,
         count(distinct date_trunc('week', ts at time zone 'Asia/Kolkata')) weeks
  from act where user_id is not null group by 1
)
select json_build_object(
  'as_of', now(),
  'registered', (select count(*) from u),
  'ids_ever_issued', (select last_value from users_id_seq),
  'ids_without_a_row_now', (select last_value from users_id_seq) - (select count(*) from u),
  'by_provider', (select json_object_agg(coalesce(auth_provider,'none'), n) from (select auth_provider, count(*) n from u group by 1) t),
  'email_verified', (select count(*) from u where email_verified),
  'internal', (select count(*) from u where internal),
  'external', (select count(*) from u where not internal),
  'created_by_ist_month', (select json_object_agg(m, n) from (select to_char(created_at at time zone 'Asia/Kolkata','YYYY-MM') m, count(*) n from u group by 1 order by 1) t),
  'activated_external', (select count(*) from per_user p join u on u.id = p.user_id where not u.internal),
  'retained_external_2plus_weeks', (select count(*) from per_user p join u on u.id = p.user_id where not u.internal and p.weeks >= 2),
  'activated_internal', (select count(*) from per_user p join u on u.id = p.user_id where u.internal),
  'external_with_no_workflow_row', (select count(*) from u where not internal and id not in (select user_id from per_user)),
  'workflows', (select json_object_agg(w, json_build_object(
      'rows', rows, 'users', users, 'external_rows', ext_rows, 'external_users', ext_users, 'external_repeat_users', ext_repeat)) from (
      select a.w, count(*) rows, count(distinct a.user_id) users,
             count(*) filter (where not u.internal) ext_rows,
             count(distinct a.user_id) filter (where not u.internal) ext_users,
             (select count(*) from (select a2.user_id from act a2 join u u2 on u2.id=a2.user_id where a2.w=a.w and not u2.internal group by 1 having count(*) >= 2) r) ext_repeat
      from act a join u on u.id = a.user_id group by a.w) t),
  'backtests', json_build_object('rows', (select count(*) from backtests),
      'statuses', (select json_object_agg(status, n) from (select status, count(*) n from backtests group by 1) t),
      'with_trades', (select count(*) from backtests where total_trades > 0),
      'zero_trades', (select count(*) from backtests where coalesce(total_trades,0) = 0),
      'no_strategy_owner', (select count(*) from backtests where strategy_id is null),
      'linked_to_a_hypothesis', (select count(*) from backtests where hypothesis_id is not null),
      'by_created_month', (select json_object_agg(m, n) from (select to_char(created_at,'YYYY-MM') m, count(*) n from backtests group by 1 order by 1) t)),
  'product_events', (select json_object_agg(event_name, json_build_object('events', n, 'users', us)) from (
      select event_name, count(*) n, count(distinct user_id) us from product_events group by 1) t),
  'research_log_rows_with_response', (select count(*) from research_copilot_logs where response_json is not null)
);"""


COVERAGE_SQL = """
with s as (select distinct symbol from symbols where is_active),
     d as (select distinct symbol from stock_dashboard_cache),
     p as (select distinct symbol from stock_profiles where nullif(trim(short_summary), '') is not null)
select json_build_object(
  'as_of', now(),
  'active_symbols', (select count(*) from s),
  'dashboard_symbols', (select count(*) from d),
  'profile_symbols', (select count(*) from p),
  'dashboard_and_profile', (select count(*) from d join p using (symbol)),
  'dashboard_without_profile', (select count(*) from d where symbol not in (select symbol from p)),
  'profile_not_on_dashboard', (select count(*) from p where symbol not in (select symbol from d)),
  'active_not_on_dashboard', (select count(*) from s where symbol not in (select symbol from d)),
  'dashboard_not_active', (select count(*) from d where symbol not in (select symbol from s)),
  'active_with_profile', (select count(*) from s join p using (symbol))
);"""

ANNOUNCEMENTS_SQL = """
select json_build_object(
  'as_of', now(),
  'total_rows', (select count(*) from corporate_announcements),
  'by_announcement_date_ist', (select json_object_agg(m, n) from (
      select to_char(announcement_date at time zone 'Asia/Kolkata','YYYY-MM') m, count(*) n from corporate_announcements
      where announcement_date >= '2026-06-01 00:00:00+05:30' and announcement_date < '2026-11-01 00:00:00+05:30' group by 1 order by 1) t),
  'ingested_by_created_at_ist', (select json_object_agg(m, n) from (
      select to_char(created_at at time zone 'Asia/Kolkata','YYYY-MM') m, count(*) n from corporate_announcements
      where created_at >= '2026-06-01 00:00:00+05:30' group by 1 order by 1) t),
  'distinct_attachment_urls_jul_sep', (select count(distinct attachment_url) from corporate_announcements
      where announcement_date >= '2026-07-01 00:00:00+05:30' and announcement_date < '2026-10-01 00:00:00+05:30' and attachment_url is not null),
  'rows_without_attachment_jul_sep', (select count(*) from corporate_announcements
      where announcement_date >= '2026-07-01 00:00:00+05:30' and announcement_date < '2026-10-01 00:00:00+05:30' and attachment_url is null)
);"""

QDRANT_SH = r"""
Q=http://127.0.0.1:16333
curl -s -X POST $Q/collections/corporate_announcements/points/count -H 'content-type: application/json' -d '{"exact":true}'
echo
curl -s -X POST $Q/collections/corporate_announcements/facet -H 'content-type: application/json' \
  -d '{"key":"doc_id","limit":2000000,"exact":false}' | python3 -c 'import sys,json;h=json.load(sys.stdin)["result"]["hits"];print(len(h))'
curl -s -X POST $Q/collections/corporate_announcements/facet -H 'content-type: application/json' \
  -d '{"key":"ticker","limit":100000,"exact":false}' | python3 -c 'import sys,json;h=json.load(sys.stdin)["result"]["hits"];print(len(h))'
"""


def sitemap_pages():
    """Stock URLs in the public sitemap: the definition of a page."""
    total = 0
    for i in range(0, 20):
        try:
            with urllib.request.urlopen(f"https://anvest.in/sitemaps/stocks-{i}.xml", timeout=60) as r:
                total += len(re.findall(r"<loc>https://anvest\.in/stocks/", r.read().decode()))
        except Exception:
            break
    return total


if __name__ == "__main__":
    qdrant = gcloud(QDRANT_SH).split("\n")
    result = {
        "users_and_usage": sql_json(users_sql()),
        "coverage": sql_json(COVERAGE_SQL),
        "announcements": sql_json(ANNOUNCEMENTS_SQL),
        "public_pages_in_sitemap": sitemap_pages(),
        "qdrant_corporate_announcements": {
            "passages_exact": json.loads(qdrant[0])["result"]["count"],
            "distinct_doc_id": int(qdrant[1]),
            "distinct_ticker": int(qdrant[2]),
        },
    }
    (HERE / "product_metrics_snapshot.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
