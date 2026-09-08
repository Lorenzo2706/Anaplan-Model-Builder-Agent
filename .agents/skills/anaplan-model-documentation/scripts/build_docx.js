/*
 * Render a model-documentation sections.json (produced by md_to_sections.py)
 * into a Word document.
 *
 * Default visual style mirrors this vault's accumulated house style
 * (originally lifted from a reference Documentatie.docx example, then reused
 * for later models): Arial, heading color #0F4761, plain black-grid tables.
 * Pass a style override JSON as the 5th argument to mirror a different
 * reference document instead - see references/docx-style-guide.md for what's
 * overridable and how to pull the values out of a real .docx via the docx
 * skill's unpack.py.
 *
 * Usage:
 *   node build_docx.js <sections.json> <output.docx> "<Title>" "<Subtitle>" [style.json]
 *
 * Requires the `docx` npm package. If it's not resolved locally, run with:
 *   NODE_PATH="$(npm root -g)" node build_docx.js ...
 */
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, LevelFormat, HeadingLevel, BorderStyle, WidthType,
  ShadingType, PageBreak, TableOfContents,
} = require("docx");
const fs = require("fs");

const [, , sectionsPath, outPath, titleArg, subtitleArg, styleArg] = process.argv;

if (!sectionsPath || !outPath) {
  console.error('Usage: node build_docx.js <sections.json> <output.docx> "<Title>" "<Subtitle>" [style.json]');
  process.exit(1);
}

const DEFAULT_STYLE = {
  font: "Arial",
  headingColor: "0F4761",
  subtitleColor: "595959",
  borderColor: "000000",
  placeholderColor: "C00000",
  noteBar: "8FAADC",
  noteFill: "F2F6FC",
  warnBar: "C9A227",
  warnFill: "FFF8E6",
};
const STYLE = styleArg
  ? { ...DEFAULT_STYLE, ...JSON.parse(fs.readFileSync(styleArg, "utf-8")) }
  : DEFAULT_STYLE;

const CONTENT_WIDTH = 9360; // US Letter, 1" margins
const sections = JSON.parse(fs.readFileSync(sectionsPath, "utf-8"));

// ---------- inline formatting ----------
function runs(text, opts = {}) {
  const out = [];
  const re = /(\*\*.+?\*\*|`.+?`|\[PLACEHOLDER:[^\]]+\])/g;
  let last = 0;
  let m;
  while ((m = re.exec(text)) !== null) {
    if (m.index > last) out.push(new TextRun({ text: text.slice(last, m.index), ...opts }));
    const token = m[0];
    if (token.startsWith("**")) {
      out.push(new TextRun({ text: token.slice(2, -2), bold: true, ...opts }));
    } else if (token.startsWith("`")) {
      out.push(new TextRun({ text: token.slice(1, -1), font: "Consolas", size: (opts.size || 22) - 2, ...opts }));
    } else if (token.startsWith("[PLACEHOLDER")) {
      out.push(new TextRun({ text: token, italics: true, color: STYLE.placeholderColor, ...opts }));
    }
    last = re.lastIndex;
  }
  if (last < text.length) out.push(new TextRun({ text: text.slice(last), ...opts }));
  if (out.length === 0) out.push(new TextRun({ text: "", ...opts }));
  return out;
}

function p(text, opts = {}) {
  return new Paragraph({ spacing: { after: 140 }, children: runs(text, opts) });
}
function h1(text) { return new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun(text)] }); }
function h2(text) { return new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun(text)] }); }
function h3(text) { return new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun(text)] }); }
function h4(text) { return new Paragraph({ heading: HeadingLevel.HEADING_4, children: [new TextRun(text)] }); }
const HFN = { 1: h1, 2: h2, 3: h3, 4: h4 };

function spacer() {
  return new Paragraph({ spacing: { after: 60 }, children: [] });
}

function bullets(items) {
  return items.map(
    (item) =>
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        spacing: { after: 80 },
        children: runs(item),
      })
  );
}

function calloutBlock(text, { bar, fill }) {
  return new Paragraph({
    spacing: { before: 100, after: 140 },
    border: { left: { style: BorderStyle.SINGLE, size: 18, color: bar, space: 8 } },
    shading: { fill, type: ShadingType.CLEAR },
    indent: { left: 100 },
    children: runs(text, { italics: true, color: "444444" }),
  });
}
function note(text) { return calloutBlock(text, { bar: STYLE.noteBar, fill: STYLE.noteFill }); }
function warn(text) { return calloutBlock("Warning: " + text, { bar: STYLE.warnBar, fill: STYLE.warnFill }); }
function placeholderPara(text) {
  return new Paragraph({ spacing: { after: 140 }, children: [new TextRun({ text, italics: true, color: STYLE.placeholderColor })] });
}

function tcell(text, { width, header = false }) {
  return new TableCell({
    width: { size: width, type: WidthType.DXA },
    margins: { top: 80, bottom: 80, left: 120, right: 120 },
    borders: {
      top: { style: BorderStyle.SINGLE, size: 4, color: STYLE.borderColor },
      bottom: { style: BorderStyle.SINGLE, size: 4, color: STYLE.borderColor },
      left: { style: BorderStyle.SINGLE, size: 4, color: STYLE.borderColor },
      right: { style: BorderStyle.SINGLE, size: 4, color: STYLE.borderColor },
    },
    children: [new Paragraph({ spacing: { after: 0 }, children: runs(text, header ? { bold: true } : {}) })],
  });
}

function mdTable(headers, rows) {
  // Defense in depth: a table with zero columns produces a <w:tblGrid/>
  // with no <w:gridCol> and a header <w:tr> with no <w:tc> - both invalid
  // OOXML. Word doesn't just skip a bad table like that, it refuses to
  // open the WHOLE document. md_to_sections.py is supposed to filter these
  // out before they ever reach here, but silently dropping one here too if
  // it somehow slips through is far cheaper than a corrupt deliverable.
  const ncols = headers.length;
  if (ncols === 0 || headers.every((h) => !String(h || "").trim())) {
    console.warn("Skipping a table block with no real header columns");
    return [];
  }

  let widths;
  if (ncols === 2) widths = [Math.round(CONTENT_WIDTH * 0.28), CONTENT_WIDTH - Math.round(CONTENT_WIDTH * 0.28)];
  else if (ncols === 3) widths = [Math.round(CONTENT_WIDTH * 0.24), Math.round(CONTENT_WIDTH * 0.24), CONTENT_WIDTH - 2 * Math.round(CONTENT_WIDTH * 0.24)];
  else widths = Array(ncols).fill(Math.floor(CONTENT_WIDTH / ncols));
  const fallbackWidth = Math.floor(CONTENT_WIDTH / ncols);

  const headerRow = new TableRow({ tableHeader: true, children: headers.map((hh, i) => tcell(hh, { width: widths[i] ?? fallbackWidth, header: true })) });
  // Ragged rows (more/fewer cells than the header) have been observed in
  // real research-agent markdown - pad short rows and truncate long ones
  // to the header's column count so every row always matches tblGrid.
  const bodyRows = rows.map((row) => {
    const padded = row.slice(0, ncols);
    while (padded.length < ncols) padded.push("");
    return new TableRow({ children: padded.map((c, i) => tcell(c || "", { width: widths[i] ?? fallbackWidth })) });
  });
  return [
    new Table({ width: { size: CONTENT_WIDTH, type: WidthType.DXA }, columnWidths: widths, rows: [headerRow, ...bodyRows] }),
    spacer(),
  ];
}

function renderBlock(block) {
  switch (block.type) {
    case "para": return [p(block.text)];
    case "bullets": return bullets(block.items);
    case "table": return mdTable(block.headers, block.rows);
    case "callout": return [block.kind === "warning" ? warn(block.text) : note(block.text)];
    case "placeholder": return [placeholderPara(block.text)];
    default: return [];
  }
}

// ---------- document body ----------
const body = [];
body.push(new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun(titleArg || "Model Documentation")] }));
body.push(
  new Paragraph({
    children: [new TextRun({ text: subtitleArg || "Model documentation", italics: true, color: STYLE.subtitleColor, size: 28 })],
  })
);
body.push(new Paragraph({ children: [new PageBreak()] }));
body.push(h1("Table of Contents"));
body.push(new TableOfContents("Table of Contents", { hyperlink: true, headingStyleRange: "1-4" }));
body.push(new Paragraph({ children: [new PageBreak()] }));

for (const sec of sections) {
  const level = sec.target_level || 1;
  const hfn = HFN[level] || h4;
  body.push(hfn(sec.heading));
  for (const block of sec.blocks || []) {
    body.push(...renderBlock(block));
  }
}

const doc = new Document({
  styles: {
    default: { document: { run: { font: STYLE.font, size: 22 } } },
    paragraphStyles: [
      { id: "Title", name: "Title", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: STYLE.font, bold: true, size: 56, color: "000000" },
        paragraph: { spacing: { after: 80 } } },
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: STYLE.font, bold: true, size: 40, color: STYLE.headingColor },
        paragraph: { spacing: { before: 360, after: 120 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: STYLE.font, bold: true, size: 32, color: STYLE.headingColor },
        paragraph: { spacing: { before: 260, after: 100 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: STYLE.font, bold: true, size: 28, color: STYLE.headingColor },
        paragraph: { spacing: { before: 200, after: 90 }, outlineLevel: 2 } },
      { id: "Heading4", name: "Heading 4", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: STYLE.font, italics: true, bold: true, size: 22, color: STYLE.headingColor },
        paragraph: { spacing: { before: 160, after: 80 }, outlineLevel: 3 } },
    ],
  },
  numbering: {
    config: [
      { reference: "bullets",
        levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    ],
  },
  sections: [
    {
      properties: {
        page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } },
      },
      children: body,
    },
  ],
});

Packer.toBuffer(doc).then((buffer) => {
  fs.writeFileSync(outPath, buffer);
  console.log("Written:", outPath, buffer.length, "bytes");
});
