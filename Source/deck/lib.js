// House style for Anvest decks: a white page, one serif for claims, one sans for evidence, hairline tables.
const path = require("path");
const pptxgen = require("pptxgenjs");

const C = {
  ink: "14182B", body: "363C50", mute: "6A7084", rule: "C9CDD6", hair: "E2E4E9",
  tint: "F4F4F0", violet: "3A2C88", amber: "B4690E", white: "FFFFFF",
};
const SERIF = "Georgia", SANS = "Helvetica Neue";
const W = 13.333, H = 7.5, MX = 0.6, CW = W - 2 * MX;
const VERSION = "Version 1 Nov 2026";
const IMG = path.join(__dirname, "img");

function newDeck({ title, footer }) {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";
  pres.author = "Harsh Bhardwaj";
  pres.company = "Anvest Fintech Private Limited";
  pres.title = title;
  pres.theme = { headFontFace: SERIF, bodyFontFace: SANS };
  const titlePh = { placeholder: { options: { name: "title", type: "title", x: MX, y: 0.42, w: CW, h: 1.02, fontFace: SERIF, fontSize: 25, bold: true, color: C.ink, margin: 0, valign: "top", align: "left" }, text: "" } };
  const foot = [
    { line: { x: MX, y: 7.0, w: CW, h: 0, line: { color: C.hair, width: 0.75 } } },
    { text: { text: `Anvest  |  ${footer}  |  ${VERSION}`, options: { x: MX, y: 7.05, w: 8.5, h: 0.26, fontFace: SANS, fontSize: 9, color: C.mute, margin: 0, align: "left" } } },
  ];
  const num = { x: W - MX - 0.6, y: 7.05, w: 0.6, h: 0.26, fontFace: SANS, fontSize: 9, color: C.mute, align: "right", margin: 0 };
  pres.defineSlideMaster({ title: "Claim and evidence", background: { color: C.white }, objects: [titlePh, ...foot], slideNumber: num });
  pres.defineSlideMaster({ title: "Opening page", background: { color: C.white }, objects: [] });
  return pres;
}

let counter = 0;
const nm = (name) => name || `Text ${++counter}`;

function T(s, text, x, y, w, h, o = {}) {
  const { name, ...rest } = o;
  s.addText(text, { x, y, w, h, margin: 0, valign: "top", isTextBox: true, fontFace: SANS, fontSize: 13, color: C.body, objectName: nm(name), ...rest });
}

// Bold lead-in followed by plain text, as one paragraph.
const lead = (a, b, o = {}) => [{ text: a, options: { bold: true, color: C.ink, ...o } }, { text: b, options: { ...o } }];

function cap(s, text, x, y, w) {
  T(s, text, x, y, w, 0.28, { fontSize: 11.5, bold: true, color: C.ink, name: "Exhibit caption" });
}
function src(s, text, y = 6.62, h = 0.34, x = MX, w = CW) {
  T(s, text, x, y, w, h, { fontSize: 9, color: C.mute, name: "Source note", valign: "bottom" });
}
function rule(s, x, y, w, color = C.rule, width = 0.75) {
  s.addShape("line", { x, y, w, h: 0, line: { color, width }, objectName: "Rule" });
}

const none = { type: "none" };
const line = (color = C.hair, pt = 0.75) => ({ type: "solid", pt, color });

// Hairline table: rule under the header and between rows, no verticals, no fills unless asked.
function table(s, rows, o) {
  const { x = MX, y, w = CW, colW, rowH, fontSize = 11.5, headFont = 10.5, align = [], boldFirst = false, emphasise = [], name = "Table" } = o;
  const out = rows.map((r, ri) => r.map((c, ci) => {
    const cell = typeof c === "object" && !Array.isArray(c) && c !== null ? c : { text: c };
    const head = ri === 0;
    const em = emphasise.includes(ri);
    return {
      text: cell.text,
      options: {
        fontFace: SANS,
        fontSize: head ? headFont : fontSize,
        bold: head || em || (boldFirst && ci === 0) || cell.bold || false,
        color: head ? C.mute : (em || (boldFirst && ci === 0) ? C.ink : C.body),
        align: align[ci] || "left",
        valign: head ? "bottom" : "top",
        fill: em ? { color: C.tint } : undefined,
        border: [head ? none : none, none, head ? line(C.ink, 0.75) : line(), none],
        margin: [3, 7, 3, 3],
        ...(cell.options || {}),
      },
    };
  }));
  // Cells keep a 3pt inset; pull the table left so the text, not the cell edge, sits on the page margin.
  s.addTable(out, { x: x - 3 / 72, y, w: w + 3 / 72, colW: colW && [colW[0] + 3 / 72, ...colW.slice(1)], rowH, fontFace: SANS, objectName: name, autoPage: false });
}

function pic(s, file, x, y, w, h, alt) {
  s.addImage({ path: path.join(IMG, file), x, y, w, h, altText: alt, objectName: alt });
  s.addShape("rect", { x, y, w, h, fill: { type: "none" }, line: { color: C.rule, width: 0.75 }, objectName: `${alt} border` });
}

module.exports = { C, SERIF, SANS, W, H, MX, CW, VERSION, IMG, newDeck, T, lead, cap, src, rule, table, pic, line, none };
