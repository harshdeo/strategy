// Partner proposal, same house style. It describes a proposed pilot; no integration or agreement exists.
const { C, SERIF, W, MX, CW, VERSION, newDeck, T, lead, cap, src, rule, table } = require("./lib");
const OUT = process.argv[2] || "partner.pptx";
const n = (x) => Math.round(x).toLocaleString("en-IN");
const pres = newDeck({ title: "Anvest: proposed partner pilot", footer: "Prepared for Zerodha" });
const page = () => pres.addSlide({ masterName: "Claim and evidence" });
const head = (s, t) => s.addText(t, { placeholder: "title" });

let s = pres.addSlide({ masterName: "Opening page" });
T(s, "Anvest", MX, 0.55, 4, 0.6, { fontSize: 30, bold: true, color: C.violet, name: "Company name" });
T(s, "A checked Indian filings layer for the questions your users ask about what they own", MX, 1.5, 9.6, 1.7, { fontFace: SERIF, fontSize: 32, bold: true, color: C.ink, name: "Thesis", lineSpacingMultiple: 1.04 });
T(s, "A proposal for a small, read-only pilot with an opted-in group of Kite users. Nothing here is live on Kite, and no agreement exists. This is an invitation to test one specific idea.", MX, 3.45, 8.4, 1.0, { fontSize: 15, lineSpacingMultiple: 1.1, name: "Proposal" });
rule(s, MX, 5.0, CW, C.ink);
[[n(6086), "listed symbols in the warehouse"], ["2.94 million", "corporate announcements"], ["50 of 50", "recent filings matched on revenue and profit extraction, 20 Oct 2026"]].forEach(([a, b], i) => {
  const x = MX + i * 4.1;
  T(s, a, x, 5.12, 3.8, 0.42, { fontSize: 21, bold: true, color: C.ink, name: `Fact ${i + 1}` });
  T(s, b, x, 5.55, 3.7, 0.5, { fontSize: 11, name: `Fact ${i + 1} label` });
});
T(s, `Harsh Bhardwaj, founder  |  harsh@anvest.in  |  anvest.in  |  Prepared for Zerodha  |  ${VERSION}`, MX, 7.0, CW, 0.26, { fontSize: 9, color: C.mute, name: "Contact line" });
s.addNotes("This is a proposal to test one idea with a small group of opted-in users. There is no integration today. I would like your engineers to judge it on accuracy, latency and cost.");

s = page();
head(s, "Kite already has fundamentals, strategies and an AI connection. This tests the piece between them.");
table(s, [
  ["Layer", "What exists in your ecosystem", "What Anvest would add", "What we are not claiming"],
  ["Fundamentals", "Tijori powers the Kite fundamentals widget and the Console timeline. Zerodha invested about $5M in Tijori (Nov 2025).", "Answers in words from the filing behind a number, for the holdings a user owns.", "Tijori is your partner and is adding AI of its own. It may do this too. A pilot would show whether the gap is real."],
  ["Strategies", "Streak: no-code rules on price and technical indicators, with live deployment.", "Rules that combine fundamentals and technicals, backtested with STT, stamp duty, brokerage and slippage.", "Anvest does not execute. Live strategies need separate approvals."],
  ["AI access", "Kite MCP lets a user connect an AI assistant to their account.", "Checked Indian research that assistant could call, with the filing it came from.", "No Anvest connection to Kite or Kite MCP exists."],
], { y: 1.55, colW: [1.4, 3.75, 3.6, 3.38], rowH: [0.34, 1.3, 0.98, 0.8], fontSize: 12.5, boldFirst: true, name: "Ecosystem table" });
T(s, lead("The question for the pilot: ", "“What did the companies I hold disclose this week, and did anything change?” Today that means opening PDFs one at a time. In the July to September quarter, NSE and BSE carried an average of 48,810 announcements a month."), MX, 5.2, CW, 0.9, { fontSize: 14, lineSpacingMultiple: 1.08, name: "Pilot question" });
src(s, "Zerodha Z-Connect on the Tijori fundamentals widget and Console timeline; press reports on the Tijori investment, Nov 2025; Zerodha on Streak and Rainmatter. Announcement counts: Anvest warehouse, snapshot 20 Oct 2026.");
s.addNotes("You will ask why this is needed when Tijori and Streak are already in your ecosystem. That is the right question. Tijori covers structured fundamentals and the timeline, Streak covers rule-based trading. The pilot tests whether users value answers from filings about their own holdings. If they do not, we will both know quickly.");

s = page();
head(s, "The hard part is the data underneath, which is what took a year");
table(s, [
  ["What the source does", "A real case", "How far it goes"],
  ["XBRL dates every column with the quarter, even the full-year figures.", "RELIANCE Q4 filing: quarter and full-year contexts both say January to March.", "Q4 and annual filings from FY23 onward"],
  ["Cash flow is filed half-yearly and year-to-date, often under a context a parser rejects.", "Recovered only when the four lines close their own identity.", `${n(15899)} rows recovered, none failing reconciliation`],
  ["A secondary source and the filing disagree for the same period.", "ADANIPORTS FY25 profit: ₹1,09,197 Cr in a secondary source, ₹11,092 Cr as filed.", `${n(3608)} conflicts across ${n(1022)} companies`],
  ["Bank results arrive as scans, with a hidden text layer that can be wrong in place.", "City Union Bank Q1 FY27: capital adequacy 21.73 on the page, 27.73 in the text layer.", "10 of 10 tier-1 bank results in a 21-filing sample"],
], { y: 1.3, colW: [4.6, 4.75, 2.78], rowH: [0.34, 0.6, 0.6, 0.6, 0.6], fontSize: 12.5, name: "Filing failures table" });
T(s, lead("Live on anvest.in today: ", "a filings warehouse, answers linked to the filing, natural-language screens, backtests with Indian costs and paper trading. The model reads the question; code does the arithmetic. If the data is missing, the answer says so."), MX, 4.5, CW, 0.7, { fontSize: 13, name: "Live" });
T(s, lead("Not built yet, and needed for a pilot: ", "partner keys and an endpoint, a digest of filings by holding, and page-level citations (citations are at filing level today). We would build these to a scope you agree."), MX, 5.25, CW, 0.7, { fontSize: 13, name: "Not built" });
src(s, "Anvest data audits, Jul to Sep 2026, and source audit, 20 Oct 2026. The source audit covers revenue and profit extraction on 50 filings; it does not score AI answers. No end-to-end benchmark is published yet.");
s.addNotes("This is what you would otherwise have to rediscover. It is also where we have a real head start. I have listed what is not built so you can size the work.");

s = page();
head(s, "A small pilot, judged the way your engineers would judge it");
T(s, "8 to 12 weeks. A small group of opted-in users. Read-only access through a path you approve. Criteria agreed before it starts.", MX, 1.2, CW, 0.32, { fontSize: 14, color: C.ink, name: "Pilot terms" });
table(s, [
  ["What we measure", "How", "Threshold"],
  ["Accuracy and citations", "A sample of answers on real holdings, each figure checked against the filing by your reviewers", "Agreed up front. Unsupported figures count as failures"],
  ["Latency", "p95 end to end, and retrieval alone, logged per request", "Agreed up front. We will measure before quoting a number"],
  ["Cost", "Rupees per answered question, at pilot volume and projected to your scale", "Agreed up front"],
  ["Data handling", "Least-privilege, user-authorised access. Retention, identity and token handling set by your security review", "Pass or fail, by your team"],
  ["Repeat use", "Weekly return of the opted-in group, compared with a control if you want one", "Agreed up front"],
], { y: 1.72, colW: [2.5, 6.1, 3.53], rowH: [0.34, 0.62, 0.46, 0.46, 0.62, 0.46], fontSize: 12.5, boldFirst: true, name: "Pilot metrics table" });
T(s, lead("If the results justify it: ", "a per-active-user licence, usage pricing or a white-label layer. If they do not, we stop, and you keep the findings."), MX, 5.2, CW, 0.4, { fontSize: 13.5, name: "After pilot" });
src(s, "Proposed terms. No pilot, permission or commercial agreement exists.");
s.addNotes("I would rather you set the thresholds than have me quote them. Measure it however your team normally would. If it fails, you have lost a few weeks and learned something.");

s = page();
head(s, "Suggested next step: thirty minutes with your engineers on the pipeline and the live product");
T(s, [
  { text: "What I would like to learn from you", options: { bold: true, color: C.ink, breakLine: true } },
  { text: "Whether answers from filings on a user's own holdings are a question your users actually ask", options: { bullet: { indent: 12 }, breakLine: true } },
  { text: "What an approved, read-only access path would look like, and what your security review needs", options: { bullet: { indent: 12 }, breakLine: true } },
  { text: "Whether Tijori's roadmap already covers this, in which case I would like to know", options: { bullet: { indent: 12 } } },
], MX, 1.6, CW, 2.0, { fontSize: 15, paraSpaceAfter: 8, name: "Questions" });
rule(s, MX, 3.85, CW);
T(s, "Separately, Anvest is raising a seed round. This pilot does not depend on it, and it is not part of this proposal. If Rainmatter would like to look at it, I am happy to share the investor material on its own track.", MX, 4.0, 10.8, 1.0, { fontSize: 14, lineSpacingMultiple: 1.08, name: "Round note" });
T(s, "Harsh Bhardwaj  |  harsh@anvest.in  |  anvest.in", MX, 5.3, CW, 0.3, { fontSize: 14, bold: true, color: C.violet, name: "Contact" });
s.addNotes("Thank you for reading this far. The commercial pilot and the round are separate conversations, and either can go ahead without the other.");

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote", OUT));
