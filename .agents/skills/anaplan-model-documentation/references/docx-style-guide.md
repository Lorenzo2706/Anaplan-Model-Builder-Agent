# Visual style guide

`scripts/build_docx.js` ships with a default style baked in - Arial body
text, `#0F4761` heading color (dark teal-blue), plain black single-line
"Table Grid" borders on every table, US Letter page size with 1" margins.
This is not an arbitrary choice: it's the style that was extracted from a
real example document a user provided during this skill's first run, on the
theory that Word's own default "Office" theme
(which that document used untouched) reads as more native and less
"generated" than a custom color scheme invented from scratch. Reuse the
default unless the user gives you a specific reason not to.

## When to override

Override the default when the user hands you a reference document and asks
you to match it - e.g. "make this look like the doc I attached" or "use our
house style from `<file>.docx`". In that case:

1. Unpack the reference doc with the `docx` skill's `unpack.py` (or plain
   Python `zipfile`, if the docx skill isn't available) to get at
   `word/styles.xml` and `word/theme/theme1.xml`.
2. Pull out the values that matter:
   - `w:styleId="Heading1"` (and 2/3/4) → `<w:color w:val="XXXXXX">` for the
     heading color, `<w:sz w:val="NN">` for size (half-points - divide by 2
     for pt).
   - `w:styleId="Title"` → font/size for the title.
   - `w:styleId="TableGrid"` → border style/color (usually a plain black
     single line unless the source doc customized it).
   - `theme1.xml`'s `<a:majorFont>`/`<a:minorFont>` → the actual font name
     behind `majorHAnsi`/`minorHAnsi` theme references, if the source uses
     theme fonts rather than hardcoded ones.
3. Write a small JSON file with only the keys you want to change (anything
   omitted falls back to the default):

   ```json
   { "headingColor": "1F3864", "font": "Calibri" }
   ```

4. Pass it as the 5th argument to `build_docx.js`.

Don't try to reverse-engineer *every* stylistic detail of a reference doc -
matching heading color, font, and table border style gets you 90% of the
"looks like the same house style" effect for a fraction of the effort of a
pixel-perfect clone, and the extra effort chasing paragraph spacing or theme
minutiae rarely changes whether the output reads as "matching."

## Full override key list

| Key | Default | Meaning |
|---|---|---|
| `font` | `"Arial"` | Body and heading font family |
| `headingColor` | `"0F4761"` | Hex color (no `#`) for Heading 1-4 |
| `subtitleColor` | `"595959"` | Hex color for the subtitle line under the title |
| `borderColor` | `"000000"` | Hex color for table borders |
| `placeholderColor` | `"C00000"` | Hex color for `[PLACEHOLDER: ...]` text |
| `noteBar` / `noteFill` | `"8FAADC"` / `"F2F6FC"` | Left-border and background color for `> [!note]` callouts |
| `warnBar` / `warnFill` | `"C9A227"` / `"FFF8E6"` | Left-border and background color for `> [!warning]` callouts |

Note callouts aren't part of that original reference document's own style
(it has no callout convention at all) - they were added in this skill's default
because model documentation genuinely benefits from visually flagging
caveats (suspected bugs, unconfirmed renames, data-quality warnings) rather
than burying them in plain prose. Keep them even when mirroring a plainer
reference document, unless the user specifically objects.
