#!/usr/bin/env python3
"""Convert an earnings-brief Markdown digest into a PDF.

Two backends:
  - fpdf2    : the default. Pure-Python, installs with `pip install fpdf2`,
               needs no system-level binary -- this is what makes PDF export
               work for anyone regardless of what's on their machine. Layout
               is basic but readable. Handles only the small Markdown subset
               this skill's output template actually uses (headers, tables,
               bold, bullets, blockquotes, horizontal rules, plain
               paragraphs) -- it is not a general Markdown-to-PDF converter.
  - pandoc   : optional upgrade for nicer typesetting, only if the user
               already has pandoc (and a PDF engine such as LaTeX/
               wkhtmltopdf) installed. Pass --engine pandoc to use it, or
               --engine auto to prefer it when present without requiring it.

CJK / non-Latin text with the fpdf2 backend requires a Unicode TTF font.
The script looks for a common system font automatically; pass --font to
point at one explicitly if none is found (see the error message for
where to get one). The pandoc backend does not have this limitation as
long as the underlying PDF engine on your system already supports
Unicode (most do).

Usage:
    python export_digest.py digest.md
    python export_digest.py digest.md -o report.pdf
    python export_digest.py digest.md --engine fpdf2 --font /path/to/NotoSansSC-Regular.ttf
    python export_digest.py digest.md --engine pandoc
"""

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

# On Windows, the console's default codepage often can't encode non-ASCII
# characters (e.g. a Chinese folder name in the output path). Without this,
# a perfectly successful export can crash on its own success message and
# report failure. errors="replace" keeps prints from ever raising here.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(errors="replace")

# Common Unicode font locations to try, in order, when --font isn't given.
# .ttc (collection) files are included because they're what Windows/macOS
# ship by default, but fpdf2's TTC support varies by version -- each
# candidate is tried and skipped on failure rather than assumed to work.
FONT_CANDIDATES = [
    r"C:\Windows\Fonts\msyh.ttc",
    r"C:\Windows\Fonts\msyh.ttf",
    r"C:\Windows\Fonts\simsun.ttc",
    r"C:\Windows\Fonts\simhei.ttf",
    r"C:\Windows\Fonts\arialuni.ttf",
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/STHeiti Light.ttc",
    "/Library/Fonts/Arial Unicode.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansSC-Regular.ttf",
]


def find_system_font():
    for path in FONT_CANDIDATES:
        if Path(path).is_file():
            return path
    return None


def has_non_latin1(text):
    """True if text contains characters a core PDF font (Latin-1) can't render."""
    try:
        text.encode("latin-1")
        return False
    except UnicodeEncodeError:
        return True


# ---------------------------------------------------------------------------
# pandoc backend
# ---------------------------------------------------------------------------

def export_with_pandoc(input_path, output_path):
    if shutil.which("pandoc") is None:
        return False, "pandoc not found on PATH"
    result = subprocess.run(
        ["pandoc", str(input_path), "-o", str(output_path)],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        return False, result.stderr.strip() or "pandoc exited with an error"
    return True, None


# ---------------------------------------------------------------------------
# fpdf2 backend -- minimal Markdown renderer for this skill's own template
# ---------------------------------------------------------------------------

def export_with_fpdf2(input_path, output_path, font_path):
    try:
        from fpdf import FPDF
    except ImportError:
        return False, "fpdf2 is not installed. Run: pip install fpdf2"

    text = Path(input_path).read_text(encoding="utf-8")

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    family = "Helvetica"
    if font_path:
        try:
            pdf.add_font("Body", "", font_path)
            pdf.add_font("Body", "B", font_path)  # same face; not a true bold cut
            family = "Body"
        except Exception as exc:
            return False, f"could not load font '{font_path}': {exc}"
    elif has_non_latin1(text):
        return False, (
            "This digest contains non-Latin characters (e.g. Chinese), but no "
            "Unicode font was found or given. Either install pandoc for the "
            "--engine pandoc backend, or pass a TTF font explicitly, e.g.\n"
            "  --font \"C:\\Windows\\Fonts\\msyh.ttc\"   (Windows)\n"
            "  --font \"/System/Library/Fonts/PingFang.ttc\"   (macOS)\n"
            "  --font /usr/share/fonts/truetype/noto/NotoSansSC-Regular.ttf   (Linux)\n"
            "A free, redistributable option if none of those are on your system: "
            "Noto Sans SC (https://fonts.google.com/noto/specimen/Noto+Sans+SC)."
        )

    def write_run(line, size, bold_default=False):
        """Write one line, honoring **bold** spans."""
        pdf.set_font(family, "" , size)
        parts = re.split(r"(\*\*.*?\*\*)", line)
        for part in parts:
            if part.startswith("**") and part.endswith("**"):
                pdf.set_font(family, "B", size)
                pdf.write(size * 0.5, part[2:-2])
            else:
                pdf.set_font(family, "B" if bold_default else "", size)
                pdf.write(size * 0.5, part)
        pdf.ln(size * 0.7)

    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()

        if not line:
            pdf.ln(3)
            i += 1
            continue

        if line.startswith("### "):
            write_run(line[4:], 13, bold_default=True)
        elif line.startswith("## "):
            pdf.ln(2)
            write_run(line[3:], 15, bold_default=True)
        elif line.startswith("# "):
            write_run(line[2:], 18, bold_default=True)
        elif line.strip() in ("---", "***"):
            y = pdf.get_y()
            pdf.line(pdf.l_margin, y, pdf.w - pdf.r_margin, y)
            pdf.ln(4)
        elif line.startswith("> "):
            pdf.set_font(family, "", 10)
            pdf.set_text_color(90, 90, 90)
            pdf.multi_cell(0, 5, line[2:])
            pdf.set_text_color(0, 0, 0)
            pdf.ln(1)
        elif line.startswith("- ") or line.startswith("* "):
            pdf.set_font(family, "", 11)
            pdf.write(5.5, "  \u2022 ")
            write_run(line[2:], 11)
        elif line.strip() == "```chart-data":
            # A fenced block of "label: value" lines (optionally preceded by
            # "title: ..."), meant only for this script -- it turns into an
            # actual bar chart here instead of literal text. Keeping it as a
            # plain, clearly-labeled fenced block means the .md file is still
            # readable on its own (as data), while the PDF gets a real chart.
            title, entries = None, []
            i += 1
            while i < len(lines) and lines[i].strip() != "```":
                raw = lines[i].strip()
                if raw:
                    key, _, value = raw.partition(":")
                    key, value = key.strip(), value.strip()
                    if key.lower() == "title":
                        title = value
                    else:
                        try:
                            entries.append((key, float(re.sub(r"[^0-9.\-]", "", value))))
                        except ValueError:
                            pass  # skip a line that isn't parseable as label: number
                i += 1
            render_bar_chart(pdf, title, entries, family)
        elif line.lstrip().startswith("|"):
            # Collect the whole table block, skip the "|---|---|" separator row.
            table_rows = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                row = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not re.fullmatch(r"-+", row[0].replace(":", "")):
                    table_rows.append(row)
                i += 1
            i -= 1
            if table_rows:
                render_table(pdf, table_rows, family)
        else:
            write_run(line, 11)

        i += 1

    pdf.output(str(output_path))
    return True, None


def render_bar_chart(pdf, title, entries, family):
    """Simple vertical bar chart from [(label, value), ...] -- no charting
    library needed, just rectangles fpdf2 can already draw. Meant for a
    handful of bars (a quarterly/annual trend), not dense data."""
    if not entries:
        return

    if title:
        pdf.set_font(family, "B", 11)
        pdf.multi_cell(0, 6, title)
        pdf.ln(1)

    chart_width = pdf.w - pdf.l_margin - pdf.r_margin
    chart_height = 40
    bar_gap = 4
    n = len(entries)
    bar_width = (chart_width - bar_gap * (n - 1)) / n
    max_value = max(value for _, value in entries) or 1

    top_y = pdf.get_y() + 6  # headroom for the value label above the tallest bar
    baseline_y = top_y + chart_height
    x = pdf.l_margin

    pdf.set_font(family, "", 8)
    pdf.set_fill_color(90, 130, 200)
    for label, value in entries:
        bar_h = max((value / max_value) * chart_height, 1)
        bar_y = baseline_y - bar_h
        pdf.rect(x, bar_y, bar_width, bar_h, style="F")
        pdf.set_xy(x - 2, bar_y - 5)
        pdf.cell(bar_width + 4, 5, format(value, "g"), align="C")
        pdf.set_xy(x - 2, baseline_y + 1)
        pdf.cell(bar_width + 4, 5, label, align="C")
        x += bar_width + bar_gap

    pdf.set_draw_color(0, 0, 0)
    pdf.line(pdf.l_margin, baseline_y, pdf.l_margin + chart_width, baseline_y)
    pdf.set_y(baseline_y + 8)


def render_table(pdf, rows, family):
    # fpdf2's built-in table() handles both things the earlier hand-rolled
    # pdf.cell()-per-column version got wrong: it wraps long cell text onto
    # multiple lines instead of overflowing past the cell border, and with
    # markdown=True it renders **bold** spans inside cells for real instead
    # of leaving the literal ** markers in the text.
    pdf.set_font(family, "", 10)
    n_cols = len(rows[0])
    with pdf.table(text_align="LEFT", markdown=True, col_widths=[1] * n_cols) as table:
        for data_row in rows:
            row = table.row()
            for c in range(n_cols):
                row.cell(data_row[c] if c < len(data_row) else "")
    pdf.ln(3)


# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("input", help="Path to the digest's Markdown file")
    parser.add_argument("-o", "--output", help="Output PDF path (default: same name, .pdf)")
    parser.add_argument("--engine", choices=["fpdf2", "pandoc", "auto"], default="fpdf2",
                         help="Which backend to use (default: fpdf2 -- needs no system-level install; "
                              "pass 'pandoc' if you already have it for nicer typesetting, or 'auto' to "
                              "prefer pandoc when present and fall back to fpdf2 otherwise)")
    parser.add_argument("--font", help="Path to a Unicode .ttf font (fpdf2 backend only; auto-detected if omitted)")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.is_file():
        sys.exit(f"error: input file not found: {input_path}")
    output_path = Path(args.output) if args.output else input_path.with_suffix(".pdf")

    font_path = args.font or find_system_font()

    if args.engine in ("auto", "pandoc"):
        ok, err = export_with_pandoc(input_path, output_path)
        if ok:
            print(f"Wrote {output_path} (pandoc)")
            return
        if args.engine == "pandoc":
            sys.exit(f"error: pandoc export failed: {err}")
        print(f"note: pandoc unavailable ({err}), falling back to fpdf2", file=sys.stderr)

    ok, err = export_with_fpdf2(input_path, output_path, font_path)
    if not ok:
        sys.exit(f"error: {err}")
    print(f"Wrote {output_path} (fpdf2{', font: ' + font_path if font_path else ''})")


if __name__ == "__main__":
    main()
