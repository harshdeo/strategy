// Seed deck. Every model figure comes from model.json (operating_model.py --json); traffic and usage come from
// the frozen snapshots in Source/. finish_deck.py then adds the founder's flow screenshots and the native charts.
const path = require("path");
const { C, SERIF, SANS, W, MX, CW, VERSION, IMG, newDeck, T, lead, cap, src, rule, table, pic } = require("./lib");
const M = require("./model.json");
const AN = require("../analytics_snapshot_20261101.json");
const US = require("../product_metrics_snapshot.json").users_and_usage;
const OUT = process.argv[2] || "seed.pptx";

const F = M.first_close, P = M.target, X = M.maximum, SD = M.scenario_drivers, MK = M.market;
const lakh = (cr) => `₹${Math.round(cr * 100)} lakh`;
const crore = (cr) => `₹${String(+cr.toFixed(2))} crore`;
const money = (cr) => (cr < 1 ? lakh(cr) : crore(cr));
const short = (cr) => (cr < 1 ? `₹${Math.round(cr * 100)} L` : `₹${String(+cr.toFixed(2))} Cr`);
const n = (x) => Math.round(x).toLocaleString("en-IN");
const U = P.use_of_funds_usd_k;
const pct = (v) => Math.round((v / P.raise_usd_k) * 100);
const sens = Object.fromEntries(M.sensitivity.map((r) => [r.case, r]));
const fate = (r) => (r.cash_out_month ? `Cash to month ${r.cash_out_month}` : `Break-even month ${r.breakeven_month}`);
const IN = AN.by_country[0];
const inOS = Object.fromEntries(AN.by_country_os.filter((r) => r.country === "IN").map((r) => [r.os, r]));
const allV = AN.by_country.reduce((a, r) => a + r.visitors, 0), allP = AN.by_country.reduce((a, r) => a + r.pageviews, 0);
const phone = Math.round(((inOS.Android.visitors + inOS.iOS.visitors) / IN.visitors) * 100);
const searchTotal = Object.values(AN.search_referred.daily_visitors).reduce((a, b) => a + b, 0);
const searchIN = ["google.com", "bing.com", "android_google_search", "search.brave.com", "duckduckgo.com", "search.yahoo.com", "in.search.yahoo.com"].reduce((a, k) => a + AN.india_referrers[k], 0);
const home = Math.round((AN.search_referred.landing_pages["/"] / searchTotal) * 100);
const W_ = AN.india_weekly;
const R = US.workflows.research;
const reach = SD.Y5.mau + SD.Y5.partner_users;

const pres = newDeck({ title: "Anvest seed deck, November 2026", footer: "Seed round" });
const page = () => pres.addSlide({ masterName: "Claim and evidence" });
const head = (s, t) => s.addText(t, { placeholder: "title" });

// ---------------------------------------------------------------- 1 Opening
let s = pres.addSlide({ masterName: "Opening page" });
T(s, "Anvest", MX, 0.55, 4, 0.6, { fontSize: 30, bold: true, color: C.violet, name: "Company name" });
T(s, "The research tools institutions use, in plain language, for every Indian investor.", MX, 1.5, 6.15, 2.0, { fontFace: SERIF, fontSize: 31, bold: true, color: C.ink, name: "Thesis", lineSpacingMultiple: 1.04 });
T(s, "Ask Anvest Intelligence a question in ordinary words. It answers from exchange filings, builds the screen, tests the idea with Indian trading costs and helps you plan the money. A first-time investor can start here. A SEBI-registered analyst can open the filing behind the answer.", MX, 3.72, 5.95, 1.5, { fontSize: 14.5, color: C.body, lineSpacingMultiple: 1.1, name: "What it does" });
pic(s, "cover_home.jpg", 7.1, 1.5, 5.63, 3.52, "Anvest home page, signed out, 1 November 2026");
T(s, "anvest.in, signed out, 1 Nov 2026", 7.1, 5.08, 5.63, 0.25, { fontSize: 9, color: C.mute, name: "Screenshot caption" });
rule(s, MX, 5.62, CW, C.ink, 0.75);
[[n(6086), "listed symbols in the warehouse"], ["2.94 million", "corporate announcements"], ["5×", "India weekly visitors in October, no marketing spend"], ["$500K", "seed round, $3.5M post-money cap"]].forEach(([a, b], i) => {
  const x = MX + i * 3.08;
  T(s, a, x, 5.74, 2.9, 0.42, { fontSize: 21, bold: true, color: C.ink, name: `Fact ${i + 1}` });
  T(s, b, x, 6.17, 2.75, 0.45, { fontSize: 10.5, color: C.body, name: `Fact ${i + 1} label` });
});
T(s, `Harsh Bhardwaj, founder  |  harsh@anvest.in  |  anvest.in  |  ${VERSION}  |  Confidential`, MX, 7.0, CW, 0.26, { fontSize: 9, color: C.mute, name: "Contact line" });
s.addNotes("Anvest gives ordinary investors the tools an institutional desk takes for granted: filings that have been checked, screens, cost-adjusted backtests and planning, through a conversation. We start selling to SEBI-registered professionals because they pay today and catch mistakes quickly. The aim is the public.");

// ---------------------------------------------------------------- 2 Problem
s = page();
head(s, "Institutions have analysts, terminals and quant desks. Everyone else has a PDF and a tip.");
cap(s, "The same four jobs, on either side of the divide", MX, 1.5, CW);
table(s, [
  ["The job", "At an institution", "For a retail investor or a small adviser today"],
  ["Find out what a company actually reported", "Analysts and paid filing search", `Exchange PDFs read by hand, many of them scans. NSE and BSE carried ${n(61875)} announcements in August 2026 alone.`],
  ["Find companies that fit an idea", "Terminal screens on cleaned data", "Ratio screeners that expect a query language, or a stock name in a messaging group"],
  ["Test the idea before risking money", "A quant team with cost models", "A spreadsheet, or a strategy tool built around price charts"],
  ["See what it does to my money", "A portfolio system and a wealth manager", "Generic calculators, and advice from whoever is selling the product"],
], { y: 1.82, colW: [3.5, 3.35, 5.28], rowH: [0.34, 0.68, 0.68, 0.5, 0.5], boldFirst: true, fontSize: 12.5, name: "Divide table" });
T(s, "A first-time investor and a two-person advisory firm have the same problem. Neither can afford the desk.", MX, 4.92, 7.1, 1.1, { fontFace: SERIF, fontSize: 21, bold: true, color: C.violet, name: "Takeaway", lineSpacingMultiple: 1.05 });
[["13.4 crore", "unique investors registered with NSE"], ["4.6 crore", "active NSE clients"], [n(MK.sebi_firms), "SEBI-registered research, advisory and PMS firms"]].forEach(([a, b], i) => {
  const y = 4.9 + i * 0.54;
  T(s, a, 8.35, y, 1.65, 0.44, { fontSize: 17, bold: true, color: C.ink, name: `Population ${i + 1}` });
  T(s, b, 10.05, y + 0.03, 2.68, 0.46, { fontSize: 10.5, name: `Population ${i + 1} label` });
});
src(s, "Anvest warehouse by announcement date, snapshot 20 Oct 2026. NSE Market Pulse, Jul and Aug 2026. SEBI intermediary directory, 19 Oct 2026.");
s.addNotes("The divide is about tools, not intelligence. An analyst at a fund starts the day with cleaned data and someone to check it. A retail investor starts with an exchange PDF. A small adviser is on the same side as the retail investor, which is why one product can serve both.");

// ---------------------------------------------------------------- 3 Insight
s = page();
head(s, "Indian filings are not machine-ready. A model pointed at them inherits every error.");
cap(s, "Four failures found while building the warehouse, with real cases", MX, 1.5, CW);
table(s, [
  ["What the source does", "A real case", "How far it goes"],
  ["XBRL dates every column with the quarter, even the full-year figures. There is no separate annual file.", "RELIANCE Q4 filing: the quarter and full-year contexts both say January to March. The true period sits in other facts in the file.", "Q4 and annual filings from FY23 onward"],
  ["Cash flow is filed half-yearly and year-to-date, often under a context a parser rejects.", `Recovered only when the four lines close their own identity. TCS FY21 operating cash flow of ₹38,802 Cr ties to its annual report.`, `${n(15899)} rows recovered, none failing reconciliation`],
  ["A secondary source and the filing disagree for the same period.", `ADANIPORTS FY25 profit: ₹1,09,197 Cr in a secondary source, ₹11,092 Cr as filed.`, `${n(3608)} conflicts across ${n(1022)} companies; ${n(1521)} are about 10× out`],
  ["Bank results arrive as scans, with a hidden text layer that can be wrong in place.", "City Union Bank Q1 FY27: capital adequacy reads 21.73 on the page and 27.73 in the text layer. Right row, right column, plausible value.", "10 of 10 tier-1 bank results in a 21-filing sample were scans"],
], { y: 1.82, colW: [4.45, 5.0, 2.68], rowH: [0.34, 0.74, 0.74, 0.52, 0.74], fontSize: 12, name: "Filing failures table" });
T(s, [
  { text: "This is why the product took a year, and why the work keeps its value: ", options: { bold: true, color: C.ink } },
  { text: "a repair made once stays made for every later filing. Inside Anvest the model reads the question and writes the sentence. Code reads the filing and does the arithmetic. When the data is missing, the answer says so." },
], MX, 5.2, CW, 0.95, { fontSize: 14.5, lineSpacingMultiple: 1.1, name: "So what" });
src(s, "Anvest data audits, Jul to Sep 2026. The City Union Bank figure was corroborated against the bank's own press release. Sample: 21 NSE filings from 9 banks, Q1 FY27.");
s.addNotes("This is what I learned by doing the work. People assume you can connect a model to the exchange feeds. You can, and it will answer confidently from a mislabelled period or a misread scan. The hard part of this company sits under the model.");

// ---------------------------------------------------------------- 4 Flow (screenshots added by finish_deck.py)
s = page();
head(s, "From a question to a tested strategy, in one flow");
[
  ["1  Ask", "Ask in plain English", "“Find profitable companies with high ROE and low debt.”"],
  ["2  Screen", "AI builds the screen", "Plain English becomes visible, editable filters across 6,000+ stocks, with a one-click backtest."],
  ["3  Backtest", "Test it on history", "Brokerage, STT, stamp duty and slippage built in; alpha, drawdown and Sharpe reported, with every rule shown."],
  ["4  Practise", "Practise, then act", "Paper-trade the strategy with virtual cash and review every decision in a journal."],
].forEach(([tag, h1, b], i) => {
  const x = [0.64, 3.695, 7.027, 10.072][i];
  T(s, tag, x, 1.62, 2.6, 0.3, { fontSize: 13, bold: true, color: C.violet, name: `Step ${i + 1} label` });
  T(s, h1, x, 3.72, 2.75, 0.3, { fontSize: 14, bold: true, color: C.ink, name: `Step ${i + 1} heading` });
  T(s, b, x, 4.04, 2.72, 0.95, { fontSize: 11.5, name: `Step ${i + 1} detail` });
});
T(s, [
  { text: "Product test on the live site, 19 Oct 2026: ", options: { bold: true, color: C.ink } },
  { text: "this prompt produced a 516-stock screen (534 on 1 Nov as filings came in), a one-year costed backtest and a 10-stock paper basket. The model reads the request and code does the arithmetic." },
], MX, 5.2, 10.1, 0.75, { fontSize: 13, name: "Test note" });
s.addImage({ path: path.join(IMG, "qr_screen.png"), x: 11.53, y: 5.12, w: 1.2, h: 1.2, altText: "QR code to the live screen on anvest.in", objectName: "QR code to live screen" });
T(s, "Try the screen, no sign-in", 10.75, 6.36, 1.98, 0.22, { fontSize: 9, color: C.mute, align: "right", name: "QR caption" });
s.addNotes("This is one continuous path on the live site. The prompt becomes a formula you can read and edit, the formula becomes a backtest with real Indian charges, and the backtest becomes a paper portfolio. The QR code opens the same screen without signing in, so you can try it while we talk.");

// ---------------------------------------------------------------- 5 Novice
s = page();
head(s, "A first-time investor gets the same engine, in words they already use");
pic(s, "sim.jpg", MX, 1.5, 6.5, 4.06, "Portfolio simulator on anvest.in, signed out");
T(s, `Portfolio simulator, live without sign-in. ₹10 lakh in a balanced mix under “prices rise faster” becomes ₹9,32,000, with a low of ₹9,11,600. A hypothetical scenario, with its assumptions on the page.`, MX, 5.62, 6.5, 0.6, { fontSize: 10.5, color: C.mute, name: "Simulator caption" });
const nov = [
  ["Ask in ordinary words. ", "“How is ITC doing?” “Is TCS expensive right now?” Answers draw on filings, financials, shareholding and market data."],
  ["Plan retirement. ", `Tested on 19 Oct: age 32, retiring at 60, spending ₹60,000 a month, ₹5 lakh saved, ₹20,000 a month going in. Anvest answered “Save ₹14,626 more each month”, showed its assumptions and solved five ways to close the gap.`],
  ["Look inside a fund or an IPO. ", "991 schemes compared on cost, return and risk. IPO pages carry the band, size and dates from the prospectus."],
  ["Practise before spending. ", "Virtual cash, real prices, and a journal that asks why you bought."],
];
let yy = 1.5;
nov.forEach(([a, b], i) => {
  const h = [0.68, 1.08, 0.68, 0.48][i];
  T(s, lead(a, b), 7.45, yy, 5.28, h, { fontSize: 12.5, name: `Beginner task ${i + 1}` });
  yy += h + 0.1;
});
rule(s, 7.45, 4.9, 5.28);
T(s, lead("Being built now: ", "one conversation across all of these. Free-text wealth questions will run through the same cash-flow engine, and that build ships once it clears evaluation."), 7.45, 5.0, 5.28, 0.72, { fontSize: 12, name: "Next step" });
T(s, "Anvest shows the arithmetic and the assumptions. It does not tell anyone what to buy.", 7.45, 5.78, 5.28, 0.5, { fontSize: 12.5, bold: true, color: C.violet, name: "Boundary" });
src(s, "Simulator captured signed out, 1 Nov 2026. Retirement test run in a signed-in session on the live site, 19 Oct 2026. Calculators and planners need a free account.");
s.addNotes("This is the part of the company I care about most. Nobody needs to know what a drawdown is to use the simulator: it says prices rise faster and shows what happens to ten lakh rupees. The planning tools do the arithmetic and show their assumptions. Choosing securities for someone is advice, and we stay on the right side of that line until we hold the registration for it.");

// ---------------------------------------------------------------- 6 Traction
s = page();
head(s, "With no marketing spend, weekly visitors from India rose fivefold in October");
cap(s, "Organic visitors from India per week, with page views underneath", MX, 1.5, 7.4);
// native chart added by finish_deck.py at MX, 1.8, 7.4 x 3.3
const facts = [
  [`${(IN.pageviews / IN.visitors).toFixed(1)} pages`, `per visitor from India over 31 days (${n(IN.pageviews)} views, ${n(IN.visitors)} visitors)`],
  [`${phone}%`, "of those visitors are on a phone. This is the public, not only desks."],
  ["1 to 13 a day", `arriving from search, before 24 Oct and since 27 Oct. ${searchIN} of ${searchTotal} came from India; ${home}% landed on the home page, so most were looking for Anvest by name.`],
];
yy = 1.5;
facts.forEach(([a, b], i) => {
  T(s, a, 8.3, yy, 4.43, 0.42, { fontSize: 20, bold: true, color: C.violet, name: `Traction fact ${i + 1}` });
  T(s, b, 8.3, yy + 0.43, 4.43, i === 2 ? 0.82 : 0.5, { fontSize: 11.5, name: `Traction fact ${i + 1} detail` });
  yy += i === 2 ? 1.3 : 1.0;
});
T(s, lead("What they opened: ", `screener ${AN.india_paths["/screener"]}, stock list ${AN.india_paths["/stocks"]}, Anvest Intelligence ${AN.india_paths["/research"]}, strategy ${AN.india_paths["/strategy"]}, sign-up ${AN.india_paths["/register"]} (visitors from India).`), 8.3, 4.82, 4.43, 0.5, { fontSize: 11, name: "Pages opened" });
rule(s, MX, 5.38, CW, C.ink, 0.75);
T(s, lead("Accounts, 20 Oct snapshot: ", `${US.registered} registered, ${US.internal} of them ours. Of the ${US.external} outside accounts, ${US.activated_external} used a workflow and ${R.external_users} asked ${R.external_rows} of the ${R.rows} logged research questions (the other ${R.rows - R.external_rows} were internal testing). ${R.external_repeat_users} asked more than once, and ${US.retained_external_2plus_weeks} came back in a later week.`), MX, 5.44, CW, 0.46, { fontSize: 11.5, name: "Accounts line" });
T(s, lead("Revenue: ", "none yet. Checkout is not live, so nobody has been asked to pay. That is what this round tests."), MX, 5.9, CW, 0.26, { fontSize: 11.5, name: "Revenue line" });
src(s, `Vercel Web Analytics, exported 1 Nov 2026, India only. Vercel counts a visitor per day, so someone returning on two days counts twice. All-country totals were ${n(allV)} visitors and ${n(allP)} views; we leave out the other ${n(allV - IN.visitors)} visitors because most are one-page Windows and Linux sessions from Singapore, the US and China that behave like crawlers. Marketing spend to date is zero (founder).`, 6.2, 0.76);
s.addNotes("Visits jumped on 24 to 26 October, mostly from Indian phones and mostly from people arriving via Google on the home page. The level settled at about five times where it had been. We filter the numbers ourselves: a large block of one-page traffic from Singapore and the US looks automated, so it is not in this chart. Accounts are still small and revenue is zero, and I would rather you heard that from me.");

// ---------------------------------------------------------------- 7 Why now
s = page();
head(s, "Since December 2024 advisers answer for their AI output, and since April 2026 retail algos have a legal route");
table(s, [
  ["When", "What changed", "What it means for Anvest"],
  ["Dec 2024", "SEBI's research-analyst and investment-adviser amendments: disclose AI use to clients and stay solely responsible for its output. Existing clients by 30 Apr 2025.", "An adviser needs answers that can be checked against the filing before they reach a client."],
  ["2025", "Zerodha's Kite MCP lets a user connect their account to an AI agent.", "The agent can see the portfolio. It still needs checked Indian research behind it."],
  ["2025–26", "Language models became cheap and good enough to answer in plain words.", "At a planning cost of ₹0.75 an answer, a free tier for the public is affordable."],
  ["Apr 2026", "SEBI's retail algo framework applies to all brokers. Black-box providers need RA registration and exchange empanelment.", "Rules a user can read get a lighter path. Anvest's are visible, and testing comes before execution."],
  ["Jun 2026", "AlphaSense reached $600M+ ARR at a $7.5B valuation selling source-cited AI research to institutions.", "The category is proven at the top. Anvest Desk is ₹2,999 a seat a month (about $380 a year), and Plus is ₹199 a month."],
], { y: 1.55, colW: [1.0, 5.9, 5.23], rowH: [0.34, 0.92, 0.66, 0.66, 0.92, 0.92], fontSize: 13, boldFirst: true, name: "Why now table" });
src(s, "SEBI (Research Analysts) (Third Amendment) Regulations 2024; SEBI (Investment Advisers) (Second Amendment) Regulations 2024; SEBI circulars of 4 Feb and 30 Sep 2025; Zerodha; fintech.global, Jun 2026; Anvest operating model (₹0.75 is a planning value, re-measured with each model change).");
s.addNotes("Each of these changes something specific. The SEBI amendments make the adviser personally answerable for what an AI tool says, which turns citations into a need rather than a feature. The algo framework gives retail strategies a legal route. Cheap models make a free plain-language tier possible for the first time.");

// ---------------------------------------------------------------- 8 Market and first buyers
s = page();
head(s, "The market is the investing public. The first paying customers are on a list SEBI publishes.");
cap(s, "Sized bottom-up, at list prices", MX, 1.5, 7.6);
table(s, [
  ["Segment", "Who", "How many", "Price a year", "Value a year"],
  ["Every active investor", "Active NSE clients", "4.6 crore", "₹2,388", `₹${n(MK.tam_retail_cr)} Cr`],
  ["Active traders", "SEBI FY25 study population", "96 lakh", "₹2,388", `₹${n(MK.sam_retail_cr)} Cr`],
  ["All professionals", "SEBI firms and ARN holders", "3.55 lakh seats", "₹35,988", `₹${n(MK.tam_pro_cr)} Cr`],
  [{ text: "First buyers" }, `${n(MK.sebi_firms)} SEBI firms and ${n(MK.top_mfds)} top distributors, 3 seats each`, `${n(MK.initial_professional_seats)} seats`, "₹35,988", `₹${MK.sam_pro_cr} Cr`],
], { y: 1.82, w: 7.6, colW: [1.75, 2.5, 1.25, 1.0, 1.1], rowH: [0.34, 0.42, 0.42, 0.42, 0.62], fontSize: 11.5, align: ["left", "left", "right", "right", "right"], emphasise: [4], name: "Market table" });
T(s, lead(`Total market ₹${n(MK.tam_cr)} Cr ($${MK.tam_usd_b}B). Reachable ₹${n(MK.sam_cr)} Cr ($${MK.sam_usd_m}M). `, `The year-5 scenario of about ₹23 crore is about ${MK.som_share_pct.toFixed(0)}% of the reachable market. AIFs, family offices and CA wealth practices are left out of these counts.`), MX, 4.62, 7.6, 0.8, { fontSize: 12, name: "Market summary" });
T(s, "Search is the public's way in, and it is now being tested properly: " + n(4533) + " stock pages are in the sitemap. So far most search visitors look for Anvest by name, so stock-page search is unproven.", MX, 5.45, 7.6, 0.75, { fontSize: 12, name: "Search note" });
T(s, "Why professionals come first", 8.7, 1.5, 4.03, 0.3, { fontSize: 11.5, bold: true, color: C.ink, name: "Right heading" });
T(s, "They buy tools for their work, they can be listed by name, and they will spot a wrong number faster than anyone. A product that survives them is ready for a beginner.", 8.7, 1.82, 4.03, 1.25, { fontSize: 13, lineSpacingMultiple: 1.05, name: "Why professionals" });
T(s, lead(`${P.seats} seats `, `by month 15 is what the plan needs: about ${((P.seats / MK.initial_professional_seats) * 100).toFixed(0)}% of the first-buyer list.`), 8.7, 3.12, 4.03, 0.62, { fontSize: 13, name: "Penetration" });
rule(s, 8.7, 3.86, 4.03, C.ink);
T(s, "First 90 days after close: the targets", 8.7, 3.94, 4.03, 0.3, { fontSize: 11.5, bold: true, color: C.ink, name: "Funnel heading" });
[["200", "firms contacted, from the SEBI directory"], ["40", "live demos"], ["10", "paid Desk pilots"]].forEach(([a, b], i) => {
  const y = 4.28 + i * 0.5;
  T(s, a, 8.7, y, 0.75, 0.44, { fontSize: 21, bold: true, color: C.violet, name: `Funnel ${i + 1}` });
  T(s, b, 9.5, y + 0.09, 3.2, 0.34, { fontSize: 12, name: `Funnel ${i + 1} label` });
});
T(s, "Also: checkout live, and a first broker pilot scoped. Outreach starts at close.", 8.7, 5.82, 4.03, 0.5, { fontSize: 11, color: C.mute, name: "Funnel note" });
src(s, "NSE Market Pulse, Aug 2026. SEBI FY25 study of individual traders. SEBI directory, 19 Oct 2026. Cafemutual: ARN and EUIN holders, Jun 2026; top distributors, FY26. List prices: Plus ₹199 a month, Desk ₹2,999 a seat a month. Sitemap counted 1 Nov 2026.");
s.addNotes("The public is the market and professionals are the way in. At Indian prices the professional segment alone is small, and I would rather say so than stretch it. Its value is that it pays early, it is reachable by name and it hardens the product. Scale comes from the public, through search and later through brokers.");

// ---------------------------------------------------------------- 9 Business model and plan
s = page();
head(s, `Professionals pay first, which keeps the public tools open. On plan, $500K reaches break-even in month ${P.breakeven_month}.`);
cap(s, "Who pays, and when (launch pricing; checkout goes live after close)", MX, 1.5, 7.05);
table(s, [
  ["Plan", "For whom, and what", "Price", "Month-15 revenue"],
  ["Free", "Everyone: public pages, screener, simulator, and a small allowance of AI questions with an account", "₹0", "Reach"],
  ["Plus, Pro", "Individuals: 150 to 600 AI questions a month, backtests, alerts, planning", "₹199–₹599 a month", `${Math.round((P.rev_lakh.retail / P.mrr_lakh) * 100)}%`],
  ["Desk", "Advisory, research and PMS teams, 1 to 5+ seats. Team workspace and coverage digests are built with this round", "₹2,999 a seat a month", `${Math.round((P.rev_lakh.desk / P.mrr_lakh) * 100)}%`],
  ["Partner API", "Brokers and wealth apps, once a partner signs. Nothing signed; first paid pilot planned for month 10", "₹15, ₹10, ₹6 a user a month by volume", `${Math.round((P.rev_lakh.partners / P.mrr_lakh) * 100)}%`],
  ["Baskets", "Rule-based baskets through brokers, after RA registration and empanelment", "₹250 a month net, plus share", "After Series A"],
], { y: 1.82, w: 7.05, colW: [0.95, 3.4, 1.5, 1.2], rowH: [0.42, 0.56, 0.56, 0.74, 0.74, 0.56], fontSize: 11, boldFirst: true, name: "Pricing table" });
T(s, lead("Per team: ", `3 seats on average at ₹${n(M.pricing.desk_net_seat_month_inr)} net a seat. CAC is ₹${P.desk_cac_lakh.toFixed(2)} lakh a team, repaid by about ${Math.round(P.desk_payback_months_revenue)} months of team revenue. Gross margin is ${P.gross_margin_pct}% at month 15 and about ${M.scenario_y5_gross_margin_pct}% at year-5 scale. All are model inputs until pilots replace them.`), MX, 5.68, 7.05, 0.8, { fontSize: 11, name: "Unit economics" });
cap(s, "If one assumption misses ($500K plan, costs unchanged)", 8.0, 1.5, 4.73);
const sensRows = [["Plan as modelled", "Plan as modelled"], ["No paying partner", "No paying partner"], ["Sellers close 3 teams a month, not 4", "Sellers close 3 teams, not 4"], ["Sellers close 2 teams a month, not 4", "Sellers close 2 teams, not 4"], ["Teams average 2 seats, not 3", "Teams average 2 seats, not 3"], ["First Desk sales slip three months", "First sales slip 3 months"], ["No partner, 3 teams a month, 2 seats", "All of: no partner, 3 teams, 2 seats"]];
table(s, [["Case", "Month-15 ARR", "Outcome"], ...sensRows.map(([k, label]) => [label, short(sens[k].arr_m15_cr), fate(sens[k])])], { x: 8.0, y: 1.82, w: 4.73, colW: [2.25, 0.78, 1.7], rowH: [0.42, 0.42, 0.42, 0.42, 0.42, 0.42, 0.42, 0.42], fontSize: 11, align: ["left", "right", "left"], emphasise: [1], name: "Sensitivity table" });
T(s, "Any single miss still leaves at least 33 months of cash. The combined case leaves 29.", 8.0, 5.3, 4.73, 0.62, { fontFace: SERIF, fontSize: 15, bold: true, color: C.violet, name: "Sensitivity takeaway" });
src(s, `Anvest operating model, a monthly build of users, conversion, churn, seller capacity, partner usage, salaries, serving, data and compliance. ARR is net of 18% GST. ₹95 = $1. Plan: ${short(P.arr_cr)} at month 15, ${short(P.arr_m18_cr)} at month 18, cash low ₹${Math.round(P.cash_low_cr * 100)} lakh in month ${P.cash_low_month}.`);
s.addNotes("Professional seats carry the early revenue, and that is what lets the public pages stay open. The table on the right is the one I would ask for as an investor. On plan we reach break-even without another round. If any one assumption misses we do not reach it in this round's cash, but we still have about three years to fix it.");

// ---------------------------------------------------------------- 10 Competition
s = page();
head(s, "Good tools exist for each step. We found none that runs from filing to tested idea to plan in one account.");
table(s, [
  ["Product", "What it does well", "Where the user still has to leave"],
  ["Screener.in", "Fast ratio data and custom screens; AI over company documents, sold as credits", "Backtesting and planning are not on its Premium page"],
  ["Tijori", "Natural-language screener, filing timeline, stock and fund tracking. Powers Kite's fundamentals; Zerodha invested about $5M (Nov 2025)", "No backtests or planning shown on its site"],
  ["Trendlyne", "The closest broad alternative: AI screener creation, concall summaries, screener backtests, baskets", "Paper trading and planning are not listed"],
  ["Multibagg (Iris)", "Plain-English answers from filings, broker-connected portfolio, WhatsApp alerts, free calculators", "Backtesting and paper trading are not mentioned"],
  ["Streak", "Technical-rule strategies, backtests, paper and live trading through Zerodha", "Built around price rules, with no filing research"],
  ["Perplexity Finance, ChatGPT or Claude with Kite MCP", "Free or cheap, broad, and improving fast. Perplexity carries live Indian earnings-call transcripts", "No costed Indian backtest, and no repaired filings warehouse behind the answer"],
  [{ text: "Anvest" }, "Filing answer to editable screen to costed backtest to paper trade, plus plain-language simulators and planners", "Behind on: broker links and execution (none), page-level citations (filing level today), concall answers (thin), paying customers (none)"],
], { y: 1.5, colW: [2.2, 5.5, 4.43], rowH: [0.32, 0.5, 0.68, 0.5, 0.5, 0.5, 0.68, 0.68], fontSize: 11.5, boldFirst: true, emphasise: [7], name: "Competition table" });
src(s, "Vendors' public product pages, read 19 Oct and 1 Nov 2026; Zerodha and press reports on Tijori and Perplexity. A feature not shown publicly may still exist, and we have not run paid hands-on trials yet.");
s.addNotes("These are good products and some of them are moving quickly. Trendlyne and Multibagg are the closest. Our case is the connected flow on a checked data layer, in language a beginner can use. The last row is where we are behind today. Hands-on paid trials of each competitor are on my list before the partner meetings.");

// ---------------------------------------------------------------- 11 Team
s = page();
head(s, "One engineer built this in twelve months. The round turns that into a team.");
T(s, "Harsh Bhardwaj", MX, 1.5, 6.3, 0.48, { fontFace: SERIF, fontSize: 22, bold: true, color: C.ink, name: "Founder name" });
T(s, "Founder. Full-time at first close.", MX, 1.98, 6.3, 0.3, { fontSize: 13, bold: true, color: C.violet, name: "Founder role" });
T(s, [
  { text: "B.Tech, Electronics and Communication, IIT Guwahati, 2015–19", options: { bullet: { indent: 12 }, breakLine: true } },
  { text: "Seven years on high-throughput backends and distributed systems at New Relic, Shiprocket, Weave and Jaguar Land Rover", options: { bullet: { indent: 12 }, breakLine: true } },
  { text: "Senior engineering lead on production multi-agent AI systems", options: { bullet: { indent: 12 }, breakLine: true } },
  { text: "Wrote the XBRL repair, the OCR trust rules and the verification code behind the cases on page 3, with no outside capital", options: { bullet: { indent: 12 } } },
], MX, 2.42, 6.3, 2.05, { fontSize: 13, paraSpaceAfter: 6, name: "Founder background" });
rule(s, MX, 4.62, 6.3);
T(s, "Why me: the failures on page 3 are data engineering at scale, which is what I have done for seven years. What I have not done is sell to advisers, so that is the first hire.", MX, 4.72, 6.3, 1.1, { fontSize: 13.5, lineSpacingMultiple: 1.06, color: C.ink, name: "Founder fit" });
cap(s, "Hires funded by this round", 7.5, 1.5, 5.23);
table(s, [
  ["Month", "Role", "Job"],
  ["2", "Growth and partnerships lead", "Sells Desk pilots, runs broker conversations"],
  ["3", "Data engineer", "Owns ingestion, OCR quality and freshness"],
  ["6", "Full-stack and quant engineer", "Team workspace, alerts, strategy tools"],
  ["9", "Second seller (from $500K)", "Scales Desk sales to 8 new teams a month"],
], { x: 7.5, y: 1.82, w: 5.23, colW: [0.6, 2.2, 2.43], rowH: [0.34, 0.56, 0.56, 0.56, 0.56], fontSize: 11.5, name: "Hiring table" });
T(s, "Compliance and capital-markets advisers are being appointed this round. None is named yet.", 7.5, 4.72, 5.23, 0.6, { fontSize: 12, color: C.body, name: "Advisers" });
src(s, "Hiring months and team counts come from the operating model.");
s.addNotes("I go full-time at first close. I built everything so far alone, which is the proof of speed and also a key-person risk, and I would rather say that first. The first hire covers what I have not done, which is sell to advisers.");

// ---------------------------------------------------------------- 12 Risks
s = page();
head(s, "Six reasons to pass, and what we are doing about each");
table(s, [
  ["Risk", "Where it stands", "What we do about it"],
  ["Nobody has paid yet", `Pre-revenue. ${R.external_users} outside accounts were asking questions by 20 Oct.`, "10 paid pilots is the first test. If 200 firms produce fewer than 3, we change the buyer or the price before hiring the second seller."],
  ["A wrong number reaches a beginner", "Numeric checks run before display. Revenue and profit matched on 50 of 50 audited filings; end-to-end answers have no published benchmark yet.", "New AI builds stay held until they pass an evaluation they have not seen. A public benchmark is due by month 6."],
  ["The line between information and advice", "No buy, sell or hold calls, no target prices. Planning is arithmetic on the user's own inputs.", "RA registration is funded, and counsel reviews planning features before release. Personal portfolio advice would need separate adviser registration."],
  ["Data rights and source access", "Filings are public, but redistribution terms need confirming. BSE's API and MCX's feed block us today.", "$65K covers counsel, licence and serving. Stale data is hidden rather than shown."],
  ["Bigger players move in", "Zerodha backs Tijori and Streak. Perplexity gives Indian transcripts away. Screener sells AI credits.", "Sell directly to advisers, depend on no single broker, and compete on checked data and the connected flow."],
  ["One founder, not yet full-time", "Everything so far is one person's work.", "Full-time at first close. Three hires by month 6. Runbooks and scheduled jobs are documented."],
], { y: 1.32, colW: [2.55, 4.7, 4.88], rowH: [0.32, 0.76, 0.92, 0.92, 0.76, 0.76, 0.56], fontSize: 11.5, boldFirst: true, name: "Risk table" });
s.addNotes("Better that you hear these from me. The first one matters most, and it has a stop rule: if the outreach does not produce pilots we change the buyer or the price before spending on a second seller. The second is why new AI builds are held behind an evaluation they have not seen.");

// ---------------------------------------------------------------- 13 Ask
s = page();
head(s, "Raising $500K to prove that advisers will pay and that beginners will stay");
T(s, "$3.5M post-money cap. CCD or CCPS, to be settled with counsel. Same terms for every investor. First close $400K, room to $700K.", MX, 1.4, CW, 0.3, { fontSize: 13, color: C.ink, name: "Terms" });
cap(s, "Where the $500K goes", MX, 1.78, 5.9);
table(s, [
  ["Amount", "Use", "What it pays for"],
  [`$${U.team}K (${pct(U.team)}%)`, "Team", "Growth lead, data engineer, full-stack and quant engineer, second seller from month 9"],
  [`$${U.compliance_infra}K (${pct(U.compliance_infra)}%)`, "Compliance, data, serving", "RA registration, counsel, exchange data licence, hosting and inference"],
  [`$${U.growth_founder}K (${pct(U.growth_founder)}%)`, "Growth and founder", "Pilots, launch, acquisition tests, founder salary"],
  [`$${U.reserve_runway}K (${pct(U.reserve_runway)}%)`, "Runway after month 18", `Pays the burn from month 19 to break-even in month ${P.breakeven_month} if no new round comes`],
], { y: 2.04, w: 5.9, colW: [1.05, 1.4, 3.45], rowH: [0.32, 0.56, 0.56, 0.42, 0.56], fontSize: 11.5, boldFirst: true, name: "Use of funds table" });
cap(s, "What it should prove (targets from the model)", 6.85, 1.78, 5.88);
table(s, [
  ["By", "Target", "Why it matters"],
  ["Month 3", "10 paid Desk pilots, checkout live", "Someone pays"],
  ["Month 6", `~${P.teams_m6} teams, public benchmark, RA application filed`, "Accuracy is checkable from outside"],
  ["Month 12", `~${P.teams_m12} teams, ${short(P.arr_m12_cr)} ARR, first paid partner`, "Selling is repeatable"],
  ["Month 15", `${P.teams} teams, ${P.seats} seats, ${short(P.arr_cr)} ARR`, "Unit economics replace assumptions"],
  ["Month 18", `~${P.teams_m18} teams, ${short(P.arr_m18_cr)} ARR, retention measured`, "The evidence a Series A asks for"],
], { x: 6.85, y: 2.04, w: 5.88, colW: [0.9, 2.95, 2.03], rowH: [0.32, 0.44, 0.44, 0.44, 0.44, 0.44], fontSize: 11.5, boldFirst: true, name: "Milestone table" });
T(s, lead("Other amounts: ", `$400K gives ${short(F.arr_cr)} ARR at month 15 and cash to month ${F.cash_out_month}. $700K gives ${short(X.arr_cr)}, with the second seller from month 6.`), MX, 4.82, CW, 0.3, { fontSize: 12, name: "Other amounts" });
rule(s, MX, 5.2, CW, C.ink);
T(s, `If it works, the public gets the tools and the company gets reach. The long-term scenario is about ₹23 crore ARR and about ${Math.round(reach / 100000)} lakh monthly users across anvest.in and broker partners by year 5. It depends on a Series A and on approvals.`, MX, 5.3, 9.8, 0.95, { fontFace: SERIF, fontSize: 15.5, bold: true, color: C.violet, lineSpacingMultiple: 1.05, name: "Ambition" });
T(s, "harsh@anvest.in\nanvest.in", 10.8, 5.32, 1.93, 0.6, { fontSize: 13, bold: true, color: C.ink, align: "right", name: "Contact" });
src(s, `Anvest operating model; ₹95 = $1. Long-term scenario built on the $500K plan: ${n(SD.Y5.mau)} site users and ${n(SD.Y5.partner_users)} partner users a month. Targets, not forecasts.`);
s.addNotes("We are raising five hundred thousand dollars on a three and a half million post-money cap, with a first close at four hundred. The last line of use of funds is not idle cash: it pays the burn from month nineteen to break-even if there is no new round. Each milestone is there because it removes a specific doubt.");

// ================================================================ Appendix
// A1 Bridge
s = page();
head(s, "Appendix. How the plan reaches month-15 revenue");
table(s, [
  ["Line", "Drivers", "$400K", "$500K", "$700K"],
  ["Desk", "Founder 1 team a month from month 3. Each seller 4 teams a month once ramped, half rate for two months. 3 seats a team. 2% monthly churn, 1% seat growth. ₹2,245 net a seat.", `₹${F.rev_lakh.desk.toFixed(1)} L`, `₹${P.rev_lakh.desk.toFixed(1)} L`, `₹${X.rev_lakh.desk.toFixed(1)} L`],
  ["Partners", "Paid from months 10 and 14 ($700K: 9, 12, 15). 4,000 active users each, growing 6% a month. ₹15, then ₹10, then ₹6 a user by volume band.", `₹${F.rev_lakh.partners.toFixed(1)} L`, `₹${P.rev_lakh.partners.toFixed(1)} L`, `₹${X.rev_lakh.partners.toFixed(1)} L`],
  ["Individuals", `${n(P.mau)} monthly users at month 15. 0.3% convert each month, 5% monthly churn, ₹200 net a subscriber.`, `₹${F.rev_lakh.retail.toFixed(1)} L`, `₹${P.rev_lakh.retail.toFixed(1)} L`, `₹${X.rev_lakh.retail.toFixed(1)} L`],
  ["Net MRR, month 15", "After 18% GST and launch discounts", `₹${F.mrr_lakh.toFixed(1)} L`, `₹${P.mrr_lakh.toFixed(1)} L`, `₹${X.mrr_lakh.toFixed(1)} L`],
  ["ARR run-rate", "Net MRR × 12", short(F.arr_cr), short(P.arr_cr), short(X.arr_cr)],
  ["Desk teams (seats)", "", `${F.teams} (${F.seats})`, `${P.teams} (${P.seats})`, `${X.teams} (${X.seats})`],
  ["Net burn a month", "Month 15", `₹${F.net_burn_m15_lakh} L`, `₹${P.net_burn_m15_lakh} L`, `₹${X.net_burn_m15_lakh} L`],
  ["Spend, months 1–18", "", `₹${F.spend_m1_18_cr.toFixed(2)} Cr`, `₹${P.spend_m1_18_cr.toFixed(2)} Cr`, `₹${X.spend_m1_18_cr.toFixed(2)} Cr`],
  ["With no new funding", "Same team and spend continue", `Cash to month ${F.cash_out_month}`, `Break-even month ${P.breakeven_month}`, `Break-even month ${X.breakeven_month}`],
], { y: 1.2, colW: [2.1, 5.53, 1.5, 1.5, 1.5], rowH: [0.3, 0.72, 0.56, 0.42, 0.36, 0.36, 0.36, 0.36, 0.36, 0.36], fontSize: 11, boldFirst: true, align: ["left", "left", "right", "right", "right"], emphasise: [5], name: "Bridge table" });
src(s, "Anvest operating model. Every driver is a planning assumption until pilot data replaces it. The workbook is available in the data room. ₹95 = $1.");

// A2 Sensitivity
s = page();
head(s, "Appendix. What happens to the $500K plan when an assumption misses");
table(s, [["Case (costs stay as planned)", "ARR, month 15", "ARR, month 18", "Teams, month 15", "Cash low", "Outcome with no new funding"],
  ...M.sensitivity.map((r) => [r.case, short(r.arr_m15_cr), short(r.arr_m18_cr), String(r.teams_m15), r.cash_low_cr >= 0 ? `₹${Math.round(r.cash_low_cr * 100)} L` : "Below zero", r.cash_out_month ? `Cash runs out in month ${r.cash_out_month}; revenue covers costs by month ${r.breakeven_month}` : `Break-even in month ${r.breakeven_month}`])],
{ y: 1.5, colW: [3.5, 0.95, 0.95, 0.95, 1.0, 4.78], rowH: [0.46, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4], fontSize: 11.5, align: ["left", "right", "right", "right", "right", "left"], emphasise: [1], name: "Full sensitivity table" });
T(s, "We would not run these cases to zero. Hiring the second seller depends on pilot evidence, so spending falls if Desk selling is slow. Holding costs fixed makes this table harsher than the real decision.", MX, 5.5, CW, 0.7, { fontSize: 13, name: "Reading note" });
src(s, "Anvest operating model, function sensitivities(). ₹95 = $1.");

// A3 Long-term scenario (chart added by finish_deck.py)
s = page();
head(s, "Appendix. Long-term scenario: about ₹23 crore ARR in year 5, if a Series A and approvals come through");
cap(s, "Exit ARR by revenue line, ₹ crore", MX, 1.5, 6.4);
table(s, [["", "Sellers*", "Site users", "Paying users", "Desk seats", "Partners (users)", "ARR"],
  ...[["M15", "Month 15"], ["Y2", "Year 2"], ["Y3", "Year 3"], ["Y4", "Year 4"], ["Y5", "Year 5"]].map(([k, l]) => {
    const d = SD[k];
    return [l, String(d.sellers + 1), n(d.mau), n(d.retail_subs), n(d.seats), `${d.partners} (${n(d.partner_users)})`, short(d.arr_cr)];
  })], { x: 7.2, y: 1.55, w: 5.53, colW: [0.78, 0.62, 0.78, 0.68, 0.6, 1.17, 0.9], rowH: [0.5, 0.36, 0.36, 0.36, 0.36, 0.36], fontSize: 10.5, align: ["left", "right", "right", "right", "right", "right", "right"], boldFirst: true, name: "Scenario table" });
T(s, [
  { text: "What has to be true", options: { bold: true, color: C.ink, breakLine: true } },
  { text: "A Series A near month 18 funds sellers and marketing; monthly users grow 11% a month to month 36, then 6%.", options: { bullet: { indent: 12 }, breakLine: true } },
  { text: "Eight more partners sign from month 20, at 10,000 users each and tiered prices.", options: { bullet: { indent: 12 }, breakLine: true } },
  { text: "Baskets start in month 22 only after RA registration, exchange empanelment and a partner broker.", options: { bullet: { indent: 12 }, breakLine: true } },
  { text: `Desk and individuals alone reach ₹${M.scenario_y5_core_cr} crore; partners and baskets add ₹${M.scenario_y5_conditional_cr} crore.`, options: { bullet: { indent: 12 } } },
], 7.2, 3.95, 5.53, 2.4, { fontSize: 12, paraSpaceAfter: 4, name: "Scenario conditions" });
src(s, "Anvest operating model, built on the $500K plan. *Including the founder. A scenario, not a forecast. ₹95 = $1.");

// A4 Product
s = page();
head(s, "Appendix. What a visitor can open today without signing in");
[["cap_stock.jpg", "Stock page", "Score, financials, shareholding, filings"], ["cap_ipo.jpg", "IPO page", "Jio Platforms: dates from DRHP to listing, subscription by category"], ["cap_mf.jpg", "Mutual funds", "991 schemes compared on return, cost and risk"], ["cap_bonds.jpg", "Bonds", "Government bonds by yield, price and rating; yield calculator"], ["cap_screens.jpg", "Curated screens", "Ready-made rules such as promoter pledge and FII accumulation, each editable"], ["cap_research.jpg", "Anvest Intelligence", "Ask in plain English (questions need a free account)"]].forEach(([f, h1, b], i) => {
  const x = MX + (i % 3) * 4.15, y = 1.2 + Math.floor(i / 3) * 2.82;
  pic(s, f, x, y, 3.83, 2.0, `${h1} on anvest.in, 1 November 2026`);
  T(s, h1, x, y + 2.05, 3.83, 0.25, { fontSize: 12, bold: true, color: C.ink, name: `${h1} heading` });
  T(s, b, x, y + 2.3, 3.83, 0.4, { fontSize: 10.5, name: `${h1} detail` });
});

// A5 Answer pipeline
s = page();
head(s, "Appendix. How an answer is produced, and what is not done yet");
table(s, [
  ["Step", "What happens", "Evidence or limit"],
  ["Interpret", "The model classifies the question and resolves the company and period.", "Bad resolution fails closed: the answer asks or declines."],
  ["Retrieve", "Evidence comes from the warehouse and the filing index, through the same services the pages use.", `${n(6155194)} passages across ${n(633688)} document IDs, 20 Oct 2026.`],
  ["Compute", "Code does the arithmetic. The model does not calculate.", "Costs in backtests: brokerage, STT, stamp duty, slippage."],
  ["Validate", "Numeric checks compare each figure with the retrieved values before display.", "Reduces risk; it does not prove an answer correct."],
  ["Cite", "Answers link to the filing behind the figure.", "Filing-level today. Page-level citation is not live. Screening answers show the rule, not a citation."],
], { y: 1.2, colW: [1.3, 6.1, 4.73], rowH: [0.3, 0.46, 0.46, 0.46, 0.46, 0.62], fontSize: 11.5, boldFirst: true, name: "Pipeline table" });
T(s, lead("Source audit, 20 Oct 2026: ", "revenue and profit extraction matched 50 of 50 recent consolidated Q2 FY27 NSE XBRL filings, chosen by a fixed rule and rechecked from the source files. This tests extraction. It is not a score for AI answers."), MX, 4.15, CW, 0.62, { fontSize: 12.5, name: "Audit note" });
T(s, lead("Live spot-check, 19 Oct 2026: ", "September-quarter answers for TCS, HCL Technologies and Wipro matched their NSE filings on revenue and profit; Infosys was correctly declined because it had not reported. Four questions are not a benchmark."), MX, 4.82, CW, 0.62, { fontSize: 12.5, name: "Spot check note" });
T(s, lead("Release gate: ", "new AI builds must pass a sealed evaluation before release. The current production build is from 21 October, and later builds are held until they pass. A public 50-question benchmark is a month-6 target."), MX, 5.49, CW, 0.62, { fontSize: 12.5, name: "Gate note" });
src(s, "Anvest source audit and product tests. The full method is in the data provenance memo.");

// A6 Regulatory
s = page();
head(s, "Appendix. Regulatory position");
table(s, [
  ["Area", "Position today", "Next step"],
  ["Advice boundary", "Product rules, not only disclaimers: no buy, sell or hold calls, no target prices, no personalised investment advice.", "Counsel reviews planning and portfolio features before each release."],
  ["Research analyst", "Not registered.", "RA application is funded and targeted by month 6. Approval is SEBI's decision."],
  ["Investment adviser", "Not registered. Planning tools do arithmetic on the user's inputs and do not name securities.", "Personal portfolio recommendations would need adviser registration and a separate decision."],
  ["AI in research", "SEBI requires registered RAs and IAs to disclose AI use and holds them solely responsible for its output.", "Sources and assumptions shown so a registered customer can do that review."],
  ["Retail algos", "Backtests and paper trading are simulations. No live algo is offered.", "Live strategies need legal review, partner-broker controls, empanelment and, for black-box logic, RA registration."],
  ["Exchange data", "Filings are public disclosures. Public access does not settle redistribution rights.", "Confirm exchange terms and budget the licence before paid redistribution."],
], { y: 1.2, colW: [1.9, 5.5, 4.73], rowH: [0.3, 0.62, 0.46, 0.62, 0.62, 0.62, 0.46], fontSize: 11.5, boldFirst: true, name: "Regulatory table" });
src(s, "SEBI RA and IA amendments, Dec 2024; SEBI retail algo circulars, 4 Feb and 30 Sep 2025. Position to be confirmed by counsel.");

// A7 Rule-based investing
s = page();
head(s, "Appendix. Where rule-based investing goes, and where Anvest fits");
[["54%", "of NSE cash-market turnover is algorithmic"], ["67%", "of equity-derivatives turnover (73% in stock futures)"], ["1 Apr 2026", "SEBI's retail algo framework applies to all brokers"]].forEach(([a, b], i) => {
  const y = 1.3 + i * 1.3;
  T(s, a, MX, y, 3.9, 0.62, { fontFace: SERIF, fontSize: i === 2 ? 28 : 36, bold: true, color: C.violet, name: `Algo fact ${i + 1}`, valign: "bottom" });
  T(s, b, MX, y + 0.66, 3.9, 0.5, { fontSize: 12, name: `Algo fact ${i + 1} label` });
});
table(s, [
  ["Stage", "What the user does", "Status"],
  ["Idea", "Ask an investing question in plain English", "Live"],
  ["Rules", "Readable rules on fundamentals and technicals (P/E, ROE, RSI, SMA)", "Live"],
  ["Evidence", "Backtest with Indian costs and periodic rebalancing", "Live"],
  ["Practice", "Forward-test with virtual cash and a decision journal", "Live"],
  ["Deploy", "Rebalance baskets through partner brokers, after RA registration and empanelment", "Later"],
], { x: 4.9, y: 1.35, w: 7.83, colW: [1.1, 5.7, 1.03], rowH: [0.32, 0.46, 0.46, 0.46, 0.46, 0.62], fontSize: 12.5, boldFirst: true, name: "Algo path" });
T(s, "Exchange algo volume is mostly intraday and high-frequency. That is context, not retail demand. Anvest's lane is slower: filing-aware rules, tested and rebalanced periodically, for people who are not day traders.", 4.9, 4.55, 7.83, 0.95, { fontSize: 13, lineSpacingMultiple: 1.06, name: "Algo reading" });
src(s, "NSE Market Pulse, Dec 2025 (turnover share, FY26 to November). SEBI circulars of 4 Feb and 30 Sep 2025.");

// A8 Traffic detail
s = page();
head(s, "Appendix. How we read the traffic, and what we leave out");
const seg = (c, o) => AN.by_country_os.find((r) => r.country === c && r.os === o);
const row = (l, r, read) => [l, n(r.visitors), n(r.pageviews), (r.pageviews / r.visitors).toFixed(1), read];
table(s, [
  ["Segment, 2 Oct to 1 Nov", "Visitors", "Views", "Pages each", "How we read it"],
  row("India, Android", seg("IN", "Android"), "Real people on phones"),
  row("India, Windows", seg("IN", "Windows"), "Real people on desktops"),
  row("India, Mac", seg("IN", "Mac"), "May include the founder's own use"),
  row("India, iPhone", seg("IN", "iOS"), "Real people on phones"),
  row("Singapore, Windows", seg("SG", "Windows"), "One page each: looks automated. Excluded"),
  row("US, Windows", seg("US", "Windows"), "One page each: looks automated. Excluded"),
  row("US, Linux", seg("US", "GNU/Linux"), "Linux desktop share this high is unusual. Excluded"),
  row("China, Windows", seg("CN", "Windows"), "One page each: looks automated. Excluded"),
], { y: 1.2, w: 8.0, colW: [2.1, 0.75, 0.7, 0.8, 3.65], rowH: [0.32, 0.36, 0.36, 0.36, 0.36, 0.36, 0.36, 0.36, 0.36], fontSize: 11, align: ["left", "right", "right", "right", "left"], boldFirst: true, name: "Traffic table" });
T(s, [
  { text: "What these numbers are not", options: { bold: true, color: C.ink, breakLine: true } },
  { text: "Not a sign-up funnel. Six signed-in paths redirect to /login, so /login views are not intent.", options: { bullet: { indent: 12 }, breakLine: true } },
  { text: "Not stock-page SEO yet. 85% of search visitors landed on the home page.", options: { bullet: { indent: 12 }, breakLine: true } },
  { text: "Not unique people. Vercel counts a visitor per day.", options: { bullet: { indent: 12 }, breakLine: true } },
  { text: "The 24 to 26 Oct jump was 360 India visitors, mostly Android, mostly from Google to the home page. The level since is about five times the earlier one.", options: { bullet: { indent: 12 } } },
], 8.95, 1.2, 3.78, 3.9, { fontSize: 12, paraSpaceAfter: 6, name: "Traffic reading" });
src(s, "Vercel Web Analytics, project anvest.in, exported 1 Nov 2026. Account and workflow counts in the deck come from a separate read-only production snapshot, 20 Oct 2026.");

// A9 Milestones
s = page();
head(s, "Appendix. Eighteen months of milestones, and what comes after");
table(s, [
  ["When", "Product and data", "Commercial", "Team and regulatory"],
  ["Months 1–6", "Team workspace and coverage digests. Conversational wealth planning released. Public benchmark.", `Checkout. 10 paid pilots, then ~${P.teams_m6} Desk teams. Self-serve Plus and Pro.`, "Growth lead, data engineer, full-stack and quant engineer. RA application filed."],
  ["Months 7–12", "Filing alerts. Partner endpoint built to a signed scope.", `~${P.teams_m12} teams, ${short(P.arr_m12_cr)} ARR. First paid partner in month 10.`, "Second seller in month 9. RA approval targeted."],
  ["Months 13–18", "Page-level citations. Concall coverage.", `~${P.teams_m18} teams, ${short(P.arr_m18_cr)} ARR at month 18. Second partner.`, "Series A conversations, on measured retention and CAC."],
  ["After", "One conversation across research, testing and planning, for every holding.", "More partners, and team plans for distributors.", "Baskets through brokers after approvals."],
], { y: 1.2, colW: [1.5, 4.2, 3.4, 3.03], rowH: [0.32, 0.96, 0.8, 0.8, 0.8], fontSize: 12, boldFirst: true, name: "Roadmap table" });
src(s, "Anvest operating model and founder plan. Targets, not forecasts. Regulatory timing is SEBI's decision.");

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote", OUT));
