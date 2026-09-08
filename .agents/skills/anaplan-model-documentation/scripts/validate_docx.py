"""
Validate a generated .docx without relying on LibreOffice, pandoc, or
python-docx - none of which are guaranteed to be installed. Checks zip
integrity and XML well-formedness directly, plus a few sanity counts
(heading levels used, table count, mojibake check) that catch the most
common docx-js generation mistakes.

Why not just use the docx skill's validate.py: on at least one Windows
setup, its error-summary print crashed on a Unicode arrow character under
the console's cp1252 codepage, and reported false-positive "can't decode
byte" errors that turned out to be encoding mismatches in *its own* tooling,
not real corruption in the file. This script does the same essential
checks (zip integrity + XML parses) without that failure mode.

Usage:
    python validate_docx.py <path-to.docx>
"""
import sys
import zipfile
import xml.dom.minidom as md

if len(sys.argv) < 2:
    print("Usage: python validate_docx.py <path-to.docx>")
    sys.exit(1)

docx_path = sys.argv[1]
z = zipfile.ZipFile(docx_path)
bad = z.testzip()
print("zip testzip (None=ok):", bad)

ok = bad is None
for name in ["word/document.xml", "word/numbering.xml", "word/styles.xml", "[Content_Types].xml"]:
    data = z.read(name)
    try:
        md.parseString(data)
        print(name, "OK", len(data), "bytes")
    except Exception as e:
        print(name, "FAILED", e)
        ok = False

doc = z.read("word/document.xml").decode("utf-8")
print("Heading1 style refs:", doc.count('w:val="Heading1"'))
print("Heading2 style refs:", doc.count('w:val="Heading2"'))
print("Heading3 style refs:", doc.count('w:val="Heading3"'))
print("Heading4 style refs:", doc.count('w:val="Heading4"'))
print("table count:", doc.count("<w:tbl>"))
mojibake = doc.count("Ã")
print("mojibake check (should be 0):", mojibake)
print("PLACEHOLDER count:", doc.count("PLACEHOLDER"))

if mojibake:
    ok = False

sys.exit(0 if ok else 1)
