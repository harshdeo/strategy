// Refresh researched inputs while preserving the six-tab tracker and live CRM fields.
// Run with bundled artifact-tool. This command never sends email or submits a form.
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';
import {FileBlob, SpreadsheetFile} from '/Users/harsh/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const input=process.argv[2] || path.join(root,'Outreach/Anvest_Investor_Tracker.xlsx');
const output=process.argv[3] || input;
const previews=path.resolve(root,'../.tmp/outreach-20261020');
await fs.mkdir(previews,{recursive:true});
const contacts=JSON.parse(await fs.readFile(path.join(root,'Outreach/investor_contacts.json'),'utf8'));
const model=JSON.parse(execFileSync('/Users/harsh/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3',[path.join(root,'Financial_Models/operating_model.py'),'--json'],{encoding:'utf8'}));
const measured=JSON.parse(await fs.readFile(path.join(root,'Source/product_metrics_snapshot.json'),'utf8'));
const usage=measured.users_and_usage;
const w=await SpreadsheetFile.importXlsx(await FileBlob.load(input));
const navy='#203864', pale='#EAF0F8', green='#E2EFDA', yellow='#FFF2CC', gray='#F2F2F2';
const col=n=>{let a='';for(;n;n=Math.floor((n-1)/26))a=String.fromCharCode(65+(n-1)%26)+a;return a};
const date=s=>s ? new Date(s+'T00:00:00Z') : null;
const statuses=['Not started','Intro requested','Sent','Replied','Meeting','Diligence','Committed','Passed','Paused','Research needed','Do not contact'];
const old=w.worksheets.getItem('Investor Targets').getRange('A6:AC100').values;
const history=new Map();
for(const row of old){if(row[28])history.set(row[28],row);}
const oldActions=new Map(w.worksheets.getItem('DO THIS NEXT').getRange('A6:I100').values.filter(r=>r[2]).map(r=>[r[2],[r[5],r[6],r[7]]]));
const oldTimeline=new Map(w.worksheets.getItem('Timeline').getRange('A6:F100').values.filter(r=>r[2]).map(r=>[r[2],[r[3],r[4],r[5]]]));
const roundBefore=w.worksheets.getItem('Round Model');
const priorCapital=history.size?roundBefore.getRange('B13:D14').values:null;
// Preserve original tracker fields as evidence; source workbook is also retained in Git.
// Rebuilding obsolete pre-revenue gates and unit-mislabeled round inputs is intentional.
function prep(name,last,rows,title,subtitle){
 const s=w.worksheets.getItem(name);
 const whole=s.getRange(`A1:${last}${Math.max(rows,100)}`);
 whole.unmerge();whole.clear({applyTo:'all'});whole.dataValidation=null;whole.conditionalFormats.clear();
 const r=s.getRange(`A1:${last}${rows}`);r.format.font={name:'Calibri',size:11,color:'#1F2937'};r.format.wrapText=true;r.format.verticalAlignment='top';r.format.rowHeightPx=68;
 s.mergeCells(`A1:${last}1`);s.getRange('A1').values=[[title]];
 s.getRange(`A1:${last}1`).format={fill:navy,font:{name:'Calibri',size:16,bold:true,color:'#FFFFFF'},rowHeightPx:38};
 s.mergeCells(`A2:${last}2`);s.getRange('A2').values=[[subtitle]];s.getRange(`A2:${last}2`).format.rowHeightPx=42;
 s.getRange(`A3:${last}4`).format.rowHeightPx=15;
 s.freezePanes.unfreeze();s.freezePanes.freezeRows(5);
 return s;
}
function header(s,last,labels){s.getRange(`A5:${last}5`).values=[labels];s.getRange(`A5:${last}5`).format={fill:navy,font:{bold:true,color:'#FFFFFF'},rowHeightPx:40};}
function widths(s,ws){ws.forEach((v,i)=>s.getRange(`${col(i+1)}1:${col(i+1)}100`).format.columnWidthPx=v);}
function write(s,rows){if(rows.length)s.getRange(`A6:${col(rows[0].length)}${rows.length+5}`).values=rows;}
function validate(s,range,list){s.getRange(range).dataValidation={allowBlank:true,list:{inCellDropDown:true,source:list}};}

const targets=contacts.targets;
let s=prep('Investor Targets','AC',targets.length+5,'ANVEST — VERIFIED CONTACTS & OUTREACH PIPELINE','Reviewed 20 Oct 2026 | $500K target; $400K first close; room $700K | Dates are proposed, not sent. Published contacts only; delivery not tested.');
header(s,'AC',['Wave','Name','Type','Published cheque / terms','Lead role','Fit assessment','Why this target','Constraint / verification note','Introduction path','Priority','Status','Owner','Next action','Planned action date','Notes','Contact person','Published email','Best route','Contact / form URL','Primary source URL','Checked on','Suggested personal opener','First sent','Last touch','Follow-ups sent','Reply / outcome','Intro owner','Next follow-up','Record ID']);
const rows=targets.map(t=>{
 const active=['1','2','3'].includes(t.wave), verified=!!t.source;
 const prior=history.get(t.id);
 const status=prior?.[10] || (active||['Network','Program'].includes(t.wave)?'Not started':t.wave==='Later'?'Paused':'Research needed');
 const r=[t.wave,t.name,t.type,t.size,t.lead,active?'Current-round candidate':t.wave,t.fit,t.caveat,'No actual introducer recorded',active?'P'+t.wave:t.wave,status,prior?.[11]||'Harsh',prior?.[12]||t.action,prior?.[13]||date(t.date),prior?.[14]||'',t.person,t.email,t.route,t.url,t.source,verified?date(contacts.reviewed_on):null,t.angle,prior?.[22]||null,prior?.[23]||null,prior?.[24]||0,prior?.[25]||'',prior?.[26]||'',null,t.id];
 return r;
});
write(s,rows);widths(s,[95,225,135,220,160,155,300,370,220,95,135,95,350,145,240,250,255,265,310,310,125,380,130,130,110,230,180,140,95]);
if(!history.size)s.tables.add('A5:AC55',true,'InvestorContacts');
s.freezePanes.freezeColumns(2);
s.getRange('N6:N55').setNumberFormat('dd-mmm-yyyy');s.getRange('U6:U55').setNumberFormat('dd-mmm-yyyy');s.getRange('W6:X55').setNumberFormat('dd-mmm-yyyy');s.getRange('AB6:AB55').setNumberFormat('dd-mmm-yyyy');
validate(s,'K6:K55',statuses);
s.getRange('Y6:Y55').dataValidation={rule:{type:'whole',operator:'between',formula1:0,formula2:2},errorAlert:{style:'stop',title:'Follow-up count',message:'Enter 0, 1 or 2. Pause after two unanswered follow-ups.'}};
for(let i=6;i<=targets.length+5;i++){
 const t=targets[i-6];
 s.getRange(`AB${i}`).formulas=[[`=IF(OR(K${i}="Passed",K${i}="Paused",K${i}="Committed",K${i}="Replied",K${i}="Meeting",K${i}="Diligence",K${i}="Do not contact",K${i}="Research needed",Z${i}<>"",Y${i}>=2,W${i}=""),"",IF(X${i}="",W${i},X${i})+7)`]];
 s.getRange(`A${i}:C${i}`).format.fill=t.wave==='1'?green:t.wave==='2'?yellow:t.wave==='3'?pale:gray;
 s.getRange(`A${i}:AC${i}`).format.rowHeightPx=100;
}
s.getRange('K6:O55').format.font.color='#1D4ED8';s.getRange('W6:AA55').format.font.color='#1D4ED8';

const actions=[
 ['1','Today','Use INV01 and INV02 for first two personalized pitches','Eximius + All In are current-round candidates. Review PDF links and demo before each send.','45 min','Not started',null,'One recipient/route per fund. No bulk BCC.','OUTREACH_PLAYBOOK.md'],
 ['2','Next 48 hours','Send INV03–INV05','Titan, Inuka, Gemba; use researched opener and actual published route.','60 min','Not started',null,'Full pitch now; no artificial paid-pilot prerequisite.','Investor Targets'],
 ['3','This week','Ask real mutual contacts for Better / Prime introductions','Record introducer name in AA and intro requested status; do not invent an alumni relationship.','30 min','Not started',null,'Wait up to 48 hours, then use appropriate official contact route.','INV13 / INV16'],
 ['4','Before a call','Record a real 3-minute product walkthrough','Use current anvest.in pages and disclose dated evidence. Replay signed-out mobile screen.','60 min','Not started',null,'Latest backlog closes four broker bugs; cold-run latency and virtual-cash tile remain.','PRODUCT_DATA_BUG_BACKLOG_2026-10-20.md'],
 ['5','This week','Prepare verified company and financing answers','Cap table, legal entity, IP assignment/employment position, instrument advice, founder full-time from close.','1–2 hours','Not started',null,'Existing tracker’s assumed family ownership is not verified legal evidence.','Round Model'],
 ['6','23–29 Oct','Work wave 2, two targeted pitches per workday','India Quotient, Zeropearl, Whiteboard, z21, First Cheque, Rainmatter, SenseAI, Better, 3one4.','30–60 min/day','Not started',null,'Check form access and pitch wording; preserve a submission confirmation.','Investor Targets'],
 ['7','30 Oct–6 Nov','Work wave 3 after reviewing objections','Twelve additional funds; fit and round-size exceptions are explicit.','30–60 min/day','Not started',null,'Refine clarity, not numbers. No response-rate promises.','Investor Targets'],
 ['8','Parallel','Interview 10 named professional prospects','Sell the research workflow; record customer objections, actual use and paid willingness.','Daily sales block','Not started',null,'Customer pipeline is separate from investor pipeline. No pilots claimed until started.','GTM_PLAN.md'],
 ['9','Within 24 hours of meeting','Send requested evidence and record next step','Keep investor-specific questions, next owner and due date.','15 min','Not started',null,'Diligence files on request; do not attach internal tracker.','Anvest_Outreach_Emails.md'],
 ['10','Day 7 after send','Follow up in same thread','One concise message; Next follow-up column calculates from actual send/touch dates.','10 min/day','Not started',null,'Do not create a second form submission to chase a reply.','Investor Targets AB'],
 ['11','Day 14 after send','Send final useful follow-up, then pause','Two follow-ups maximum without a reply. Later updates only with real progress.','10 min/day','Not started',null,'No fabricated urgency, allocation or other investor interest.','Investor Targets Y / Z'],
 ['12','By 30 Oct','Decide YC application separately','Official Winter 2027 deadline 2 Nov 8pm PT = 3 Nov 9:30am IST; in-person SF Jan–Mar.','Founder decision','Not started',null,'An application is optional; no assumed commitment to relocate.','INV30'],
 ['13','Weekly','Review replies and update qualified pipeline','Count actual sends, meetings, diligence and commitments separately; update date-sensitive claims.','30 min','Not started',null,'No send or commitment has been logged by this refresh.','Metrics Gate'],
 ['14','Before using parked rows','Confirm missing routes and mandates','Axilor site errors, Atoms intake, Mumbai Angels transition, operator angels and broker partnership contacts.','As relevant','Not started',null,'Blank email is deliberate. Do not infer addresses.','CONTACT_RESEARCH_NOTES.md'],
 ['15','Before attaching PDFs','Reconcile corpus counts across investor PDFs','Latest product audit has 6,155,194 passages / 633,688 distinct doc_ids on VM, not 1.35M / 584K.','Materials check','Not started',null,'Confirm corrected exported PDF before attachment. Intro requests can start now.','CONTACT_RESEARCH_NOTES.md']
];
s=prep('DO THIS NEXT','I',actions.length+5,'ANVEST — DO THIS NEXT','20 Oct 2026 | Start suitable pre-seed funds now, in measured batches. This is a preparation and tracking workbook; nothing has been sent.');
for(const row of actions){const prior=oldActions.get(row[2]);if(prior){row[5]=prior[0];row[6]=prior[1];row[7]=prior[2]||row[7];}}
header(s,'I',['#','When','Do this','Why / what it unblocks','Effort','Status','Done date','Notes','Reference']);write(s,actions);widths(s,[55,150,360,420,140,135,140,420,300]);validate(s,'F6:F20',['Not started','In progress','Done','Blocked']);s.getRange('G6:G20').setNumberFormat('dd-mmm-yyyy');

const metrics=[
 ['Contact provenance','Published first-party sources checked 20 Oct','Suitable email or official pitch/social route','Source links in Investor Targets / Sources','Ready for researched routes','Publication verified; inbox deliverability and form submission are untested.'],
 ['Headline round','Proposed, not raised','$500K target; $400K first close; $700K room',500000,'Ready','$3.5M post-money cap proposed; exact instrument subject to counsel.'],
 ['Registered accounts','Production aggregate, 20 Oct 12:51 IST','Disclose scope; not active users',usage.registered,'Scoped evidence',`${usage.internal} internal; ${usage.external} external under documented account filter.`],
 ['Logged research queries','Production aggregate, same snapshot','Disclose scope; not accuracy',418,'Scoped evidence','Across 16 accounts, includes founder/testing.'],
 ['Saved backtest records','Production aggregate, same snapshot','Disclose scope; not successful runs',238,'Scoped evidence','Not a count of distinct external users or completed backtests.'],
 ['Saved screens','Production aggregate, same snapshot','Disclose scope',2,'Scoped evidence','Includes founder/testing; not screen executions.'],
 ['MRR / paid customers','Documented pre-revenue position','Measure first paid demand',0,'Early stage','Zero MRR is disclosed. Paid customer count not independently queried here.'],
 ['Extraction audit','20 Oct source audit','Keep line-item scope explicit','50 / 50 filings','Scoped evidence','Revenue/PAT extraction against consolidated Q2 FY27 NSE XBRL; not 50 AI answers.'],
 ['Live answer evaluation','19 Oct spot-check','Broader independent answer evaluation','4 questions: 3 answers; 1 decline','Incomplete benchmark','Do not certify a broad answer-accuracy rate.'],
 ['External accounts with workflow','20 Oct; account filter + workflow-table union','At least one recorded workflow row',usage.activated_external,'Scoped evidence','15 of 26 external accounts have recorded workflow activity. Not all attempts/success rates are recorded.'],
 ['External activity in 2+ weeks','20 Oct; distinct IST calendar weeks','Historical repeat activity, not cohort retention',usage.retained_external_2plus_weeks,'Scoped evidence','5 external accounts active in at least 2 IST weeks. Not D7/D30 or consecutive-week retention.'],
 ['External research use','20 Oct; research log attribution','Queries / users / repeat users',`${usage.workflows.research.external_rows} / ${usage.workflows.research.external_users} / ${usage.workflows.research.external_repeat_users}`,'Scoped evidence','Repeat = at least 2 recorded research rows ever; not a retention rate.'],
 ['Cohort retention / task success','No attempt/failure denominator','Measure complete external cohorts',null,'Unknown','238 stored backtests are marked COMPLETED; failed requests are not stored, and 158 lack a strategy owner.'],
 ['Cost per answered task','No fresh production cohort supplied','Measure actual cost and helpfulness',null,'Unknown','Operating-model costs are assumptions.'],
 ['Safe live-demo route','20 Oct dated production replay','Recheck before each call','Four broker bugs replayed / closed','Recheck on call day','Backlog records current replay evidence. Cold first-run latency and cash-added tile remain; do not certify every journey.'],
 ['Corpus count in PDFs','20 Oct VM source recount','6,155,194 passages / 633,688 distinct doc_ids','Prior material figure is stale','Check before PDF send','Reconcile every attached investor PDF against latest source evidence. Contact refresh preserves concurrent deck changes.'],
 ['Company / IP / cap table','Records not inspected in this refresh','Founder provides verified documents',null,'Needs documents','Do not quote family ownership or signed IP assignment without actual documents.'],
 ['Outreach started','No send actions authorized or performed','Log real sends and meetings',null,'Not started','Sending dates stay blank until user actually sends.']
];
s=prep('Metrics Gate','F',metrics.length+5,'ANVEST — EVIDENCE & READINESS','20 Oct 2026 | Early-stage outreach can start with honest disclosures. These are evidence states, not invented MAU/revenue hurdles.');
header(s,'F',['Item','Evidence date / basis','What to communicate / measure','Verified value / current state','Readiness','Definition / limitation']);write(s,metrics);widths(s,[215,290,320,245,185,490]);
s.getRange('D7').setNumberFormat('"$"#,##0');s.getRange('D8:D12').setNumberFormat('#,##0');

s=prep('Round Model','F',39,'ANVEST — PROPOSED ROUND TERMS','20 Oct 2026 | Proposed target, not committed capital. USD and INR units are explicit. See operating_model.py for the full monthly plan.');
header(s,'F',['Input / calculation','Target','First close','Maximum','Unit','Basis / limitation']);
const round=[
 ['Raise',model.target.raise_usd_k*1000,model.first_close.raise_usd_k*1000,model.maximum.raise_usd_k*1000,'USD','Proposed amounts; no investor commitment implied.'],
 ['Post-money cap',3500000,3500000,3500000,'USD','Proposed financing cap; exact instrument subject to counsel.'],
 ['Planning exchange rate',model.fx,model.fx,model.fx,'INR / USD','From Financial_Models/operating_model.py; not a live FX quote.'],
 ['Raise at planning FX',null,null,null,'INR crore','USD raise × INR/USD ÷ 10,000,000.'],
 ['Simple raise / cap ratio',null,null,null,'%','Illustrative ratio only; not an actual cap-table dilution calculation.'],
 ['Instrument','Counsel to confirm','Counsel to confirm','Counsel to confirm','','CCD/CCPS referenced in materials; signed terms do not exist here.'],
 ['Founder commitment','Full-time from close','Full-time from close','Full-time from close','','Notice period/date and IP position require actual records.'],
 ['Capital committed',null,null,null,'USD','Unknown: enter only signed/confirmed amounts; blank is not zero.'],
 ['Capital received',null,null,null,'USD','Unknown: enter only cleared funds; blank is not zero.'],
 ['','','','','',''],
 ['TARGET USE OF FUNDS','USD','Share of target','','','Investor-deck allocation; not monthly expense categories.'],
 ['Team',model.target.use_of_funds_usd_k.team*1000,null,'','','Target use-of-funds allocation from operating model.'],
 ['Compliance & infrastructure',model.target.use_of_funds_usd_k.compliance_infra*1000,null,'','','Target use-of-funds allocation.'],
 ['Growth & founder',model.target.use_of_funds_usd_k.growth_founder*1000,null,'','','Target use-of-funds allocation.'],
 ['Reserve & runway',model.target.use_of_funds_usd_k.reserve_runway*1000,null,'','','Target use-of-funds allocation.'],
 ['Total',null,null,'','','Sum must equal target raise.'],
 ['Difference vs target',null,'','','USD','Zero means allocation equals target raise.'],
 ['','','','','',''],
 ['MODEL OUTPUTS','Target','First close','Maximum','Unit','Planning scenarios; not current revenue.'],
 ['Month-15 ARR',model.target.arr_cr*1e7,model.first_close.arr_cr*1e7,model.maximum.arr_cr*1e7,'INR / year','Rounded from monthly operating model; see primary model for exact values.'],
 ['Month-15 Desk teams',model.target.teams,model.first_close.teams,model.maximum.teams,'Teams','Planning output, not current contracts.'],
 ['Month-15 Desk seats',model.target.seats,model.first_close.seats,model.maximum.seats,'Seats','Teams average 3 seats on acquisition; expansion adds seats.'],
 ['Month-15 partners',model.target.partners,model.first_close.partners,model.maximum.partners,'Paid partners','Planning output; no pilot/contract claim.'],
 ['Break-even month',model.target.breakeven_month,model.first_close.breakeven_month,model.maximum.breakeven_month,'Month','First-close case runs out of cash before its break-even; target avoids cash-out under assumptions.'],
 ['Cash-out month',model.target.cash_out_month??'None in model',model.first_close.cash_out_month??'None in model',model.maximum.cash_out_month??'None in model','Month','No guaranteed runway. Target break-even depends on modeled sales, churn and cost.'],
 ['Target cash low point',model.target.cash_low_cr*1e7,'','','INR','₹0.51 Cr ≈ ₹51L; value below displayed in lakh with formula.'],
 ['Target cash low point (lakh)',null,'','','INR lakh','Links preceding input; no second independent amount.'],
 ['','','','','',''],
 ['Source','Financial_Models/operating_model.py','','','','Snapshot 20 Oct 2026. Use this source for all updated revenue/cost/runway assumptions.'],
 ['Proposed terms source','Outreach/Anvest_Outreach_Emails.md','','','','Target amounts and proposed cap. No founder ownership is assumed.'],
 ['Diligence note','Verified cap table required','','','','Never infer founder ownership as 1 minus raise/cap. ESOPs, existing holders and instrument mechanics matter.'],
 ['Model caution','Default-alive is conditional','','','','Month-42 break-even is the target bootstrap case; later scale assumes a separate Series A.'],
 ['Contact sizing','Fund cheque is not round total','','','','A smaller cheque can join a lead; a published range is not an investor offer.'],
 ['Do not send this tracker','Internal only','','','','Share seed PDF first; model goes to diligence on request.']
];
write(s,round);widths(s,[305,225,225,225,145,520]);
if(priorCapital)s.getRange('B13:D14').values=priorCapital;
for(const c of ['B','C','D']){s.getRange(`${c}9`).formulas=[[`=${c}6*${c}8/10000000`]];s.getRange(`${c}10`).formulas=[[`=${c}6/${c}7`]];s.getRange(`${c}6:${c}8`).format.font.color='#0000FF';s.getRange(`${c}10`).setNumberFormat('0.0%');s.getRange(`${c}9`).setNumberFormat('0.00');}
s.getRange('B6:D8').setNumberFormat('#,##0');s.getRange('B17:B20').setNumberFormat('"$"#,##0');
for(let r=17;r<=20;r++){s.getRange(`C${r}`).formulas=[[`=B${r}/$B$6`]];s.getRange(`C${r}`).setNumberFormat('0.0%');}
s.getRange('B21').formulas=[['=SUM(B17:B20)']];s.getRange('C21').formulas=[['=SUM(C17:C20)']];s.getRange('C21').setNumberFormat('0.0%');s.getRange('B21').setNumberFormat('"$"#,##0');s.getRange('B22').formulas=[['=B21-B6']];s.getRange('B22').setNumberFormat('#,##0.00;(#,##0.00);0.00');
// Low point is ₹0.51 crore = ₹5.1M = ₹51 lakh.
s.getRange('B32').formulas=[['=B31/100000']];s.getRange('B32').setNumberFormat('0.0');s.getRange('B25:D31').setNumberFormat('#,##0');
for(const r of [16,24])s.getRange(`A${r}:F${r}`).format={fill:navy,font:{bold:true,color:'#FFFFFF'}};

const timeline=[
 ['20–22 Oct','Wave 1','5 suitable funds: Eximius, All In, Titan, Inuka, Gemba','Not started',null,'Personalize each email. Batch limits are workload recommendations, not expected conversion rates.'],
 ['23–29 Oct','Wave 2','9 funds; official forms and genuinely accessible introductions','Not started',null,'Learn from first calls. Do not wait for paid pilots as a blanket condition.'],
 ['30 Oct–6 Nov','Wave 3','12 additional funds after refining explanation of buyer and source quality','Not started',null,'Keep facts consistent; selectively prioritize strong warm intros sooner.'],
 ['By 30 Oct','Optional program','Decide and prepare YC Winter 2027 application','Not started',null,'Official on-time deadline 3 Nov 09:30 IST; SF in-person program.'],
 ['Day 7 / Day 14','Follow-ups','At most 2 unanswered follow-ups, in the existing thread','Not started',null,'Set actual sent date, last touch and count. Replies/pass/commitment stop automated due dates.'],
 ['Every working day','Customer evidence','Separate professional sales block alongside fundraising','Not started',null,'Log real interviews, paid demand and usage; none assumed by this schedule.'],
 ['Weekly','Pipeline review','Review meetings, objections, diligence, terms and next owners','Not started',null,'Do not count platform profiles or repeated fund contacts as independent leads.'],
 ['After real progress','Later / parked','Update relevant later-stage funds and verify unavailable routes','Not started',null,'Use measured progress; no fabricated urgency. No blanket broadcast to all 50 entries.']
];
s=prep('Timeline','F',timeline.length+5,'ANVEST — PRACTICAL OUTREACH SEQUENCE','Proposed start 20 Oct 2026 | Parallel customer learning and investor conversations. Exact dates may be edited; no messages have been sent.');
for(const row of timeline){const prior=oldTimeline.get(row[2]);if(prior){row[3]=prior[0];row[4]=prior[1];row[5]=prior[2]||row[5];}}
header(s,'F',['When','Track','Deliverable','Status','Done date','Notes']);write(s,timeline);widths(s,[160,165,500,145,140,530]);validate(s,'D6:D13',['Not started','In progress','Done','Blocked']);s.getRange('E6:E13').setNumberFormat('dd-mmm-yyyy');

const sources=targets.filter(t=>t.source).map(t=>[t.id,t.name,t.source,t.url,date(contacts.reviewed_on),t.email||'No suitable public email verified',t.caveat]);
sources.push(['MODEL','Round / financial outputs','Financial_Models/operating_model.py','',date(contacts.reviewed_on),'Internal source','Planning assumptions; rounded outputs. Proposed cap comes from current funding materials.']);
sources.push(['METRICS','Production usage snapshot','Source/product_metrics_snapshot.json','',date(contacts.reviewed_on),'Internal evidence','Founder/testing included; registered accounts are not active external users.']);
sources.push(['AUDIT','50-filing extraction audit','Source/filing_check.json','',date(contacts.reviewed_on),'Internal evidence','Revenue/PAT extraction, not broad live-answer benchmark.']);
s=prep('Sources','G',sources.length+5,'ANVEST — CONTACT SOURCES & LIMITS','Public sources reviewed 20 Oct 2026. Primary-source publication verified; SMTP delivery, investor availability and completed form submission remain untested.');
header(s,'G',['Record','Target / evidence','Primary source','Contact route URL','Checked on','Email / evidence type','Scope / limitation']);write(s,sources);widths(s,[95,270,440,400,140,295,550]);s.getRange(`E6:E${sources.length+5}`).setNumberFormat('dd-mmm-yyyy');

// Recalculation checks exercise date changes, reply handling and follow-up cap, then restore blank actuals.
const crm=w.worksheets.getItem('Investor Targets');
const originalStatus=crm.getRange('K6').values;
const originalActuals=crm.getRange('W6:AA6').values;
crm.getRange('K6').values=[['Sent']];
crm.getRange('W6:AA6').values=[[date('2026-10-20'),null,0,'','']];w.recalculate();
const due=crm.getRange('AB6').values[0][0];
if(due!==46322)throw Error(`Follow-up date is incorrect: ${due}`);
await fs.writeFile(path.join(previews,'followup-check.json'),JSON.stringify({firstSent:'2026-10-20',expectedDue:'2026-10-27',computedDue:due}));
crm.getRange('Z6').values=[['Reply received']];w.recalculate();
if(crm.getRange('AB6').values[0][0]!=='')throw Error('Reply failed to stop follow-up');
crm.getRange('Z6').values=[['']];crm.getRange('K6').values=[['Replied']];w.recalculate();
if(crm.getRange('AB6').values[0][0]!=='')throw Error('Replied status failed to stop follow-up');
crm.getRange('K6').values=[['Sent']];
crm.getRange('Z6').values=[['']];crm.getRange('Y6').values=[[2]];w.recalculate();
if(crm.getRange('AB6').values[0][0]!=='')throw Error('Follow-up cap failed');
crm.getRange('W6:AA6').values=originalActuals;crm.getRange('K6').values=originalStatus;
w.recalculate();
const errors=await w.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:100},maxChars:2000});
await fs.writeFile(path.join(previews,'formula-errors.ndjson'),errors.ndjson);
for(const [sheetName,range] of [['Investor Targets','A5:H10'],['Investor Targets','P5:V10'],['DO THIS NEXT','A5:F10'],['Metrics Gate','A5:F11'],['Round Model','A5:F13'],['Round Model','A16:F22'],['Timeline','A5:F10'],['Sources','A5:G9']]){
 const b=await w.render({sheetName,range,scale:1.2});await fs.writeFile(path.join(previews,`final-${sheetName.replaceAll(' ','_')}-${range.split(':')[0]}.png`),new Uint8Array(await b.arrayBuffer()));
}
await (await SpreadsheetFile.exportXlsx(w)).save(output);
console.log(JSON.stringify({output,targets:targets.length,publishedEmails:targets.filter(t=>t.email).length,firstThreeWaves:targets.filter(t=>['1','2','3'].includes(t.wave)).length,errors:errors.ndjson}));
