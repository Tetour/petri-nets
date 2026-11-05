"""Render every exercise note to a PDF next to it (an alternative to the Markdown preview).

    python3 -m pn.notes [-j N] [PATH ...]

The collapsed sections are expanded in the PDF, but the hint and the net each start on a
new page, so the first page shows only the task. Links to other exercises point to their
PDFs; the diagram is embedded as net.pdf (vector). The closing Reference links are left out.
The look (a mathematics textbook: Latin Modern, numbered sections, rounded boxes) is in
note-style.tex.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build" / "notes"

# ## headings become numbered \section; the note's # title is set by TITLE instead
PANDOC = [
    "pandoc", "-f", "markdown-smart", "--shift-heading-level-by=-1",
    "-V", "fontsize=11pt", "-V", "lang=cs",
    "-V", "geometry:a4paper,textwidth=14.5cm,top=3cm,bottom=3cm,headsep=0.8cm",
]

NEW_PAGE_BEFORE = ("## Nápověda", "## Petriho síť")

STYLE = Path(__file__).with_name("note-style.tex")

TITLE = r"""```{{=latex}}
\renewcommand{{\notenumber}}{{Úloha {number}}}
\thispagestyle{{plain}}
\begin{{flushleft}}
{{\scshape\color{{accent}} Úloha {number}}}\\[3pt]
{{\LARGE {title}}}\\[6pt]
{{\color{{rulegray}}\rule{{\linewidth}}{{0.8pt}}}}
\end{{flushleft}}
\vspace{{1ex}}
```
"""


def prepare(md: str, base: Path | None = None) -> str:
    md = md.replace("️", "")                                   # emoji variation selector
    md = re.sub(r"(?m)^<details>\n<summary>[^<]*</summary>\n(<br>\n)?", "", md)
    md = re.sub(r"(?m)^</details>\n", "", md)
    md = md.replace("](net.svg)", "](net.pdf)")
    # links to other notes point to their PDFs; other Markdown files (no PDF) stay as they are
    md = re.sub(r"\]\(<([^>]+)\.md>\)",
                lambda m: f"](<{m.group(1)}.pdf>)" if base is None or (base / f"{m.group(1)}.pdf").exists()
                else m.group(0), md)
    for h in NEW_PAGE_BEFORE:
        md = md.replace(f"\n{h}\n", f"\n\\newpage\n\n{h}\n")
    md = md.split("\n## Reference\n")[0]                     # links to the basics and the plan
    m = re.match(r"# (.+)\n\nÚloha (\S+)\n", md)
    if m:
        md = TITLE.format(title=m.group(1), number=m.group(2)) + md[m.end():]
    return md


def render(note: Path):
    """Pandoc writes LaTeX, xelatex runs in a fixed directory: with a fixed date this makes
    the PDF byte-identical between builds (pandoc's own temporary directory would not)."""
    out = BUILD / note.parent.name
    out.mkdir(parents=True, exist_ok=True)
    md = prepare(note.read_text(), note.parent).replace("](net.pdf)", f"](<{note.parent / 'net.pdf'}>)")
    (out / "note.md").write_text(md)
    shutil.copy(STYLE, out / "header.tex")
    r = subprocess.run(PANDOC + ["-s", "-H", "header.tex", "note.md", "-o", "note.tex"],
                       cwd=out, capture_output=True, text=True)
    if r.returncode:
        return note.parent.name, r.stderr.strip()
    env = dict(os.environ, SOURCE_DATE_EPOCH="0", FORCE_SOURCE_DATE="1")
    r = subprocess.run(["xelatex", "-interaction=nonstopmode", "-halt-on-error", "note.tex"],
                       cwd=out, capture_output=True, text=True, env=env)
    if r.returncode:
        return note.parent.name, "\n".join(l for l in r.stdout.splitlines() if l.startswith("!"))[:1000]
    shutil.copy(out / "note.pdf", note.with_suffix(".pdf"))
    return note.parent.name, ""


def find(paths):
    """Notes in the given folders (an exercise, a category, exercises/); default all.
    A note is the Markdown file named like its folder."""
    roots = [Path(p).resolve() for p in paths] or [ROOT / "exercises"]
    return [n for r in roots for n in sorted(r.rglob("*.md")) if n.stem == n.parent.name]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-j", "--jobs", type=int, default=os.cpu_count())
    ap.add_argument("paths", nargs="*")
    args = ap.parse_args()
    notes = find(args.paths)
    failed = 0
    with ProcessPoolExecutor(max_workers=args.jobs) as pool:
        for name, err in pool.map(render, notes):
            print(f"{'FAIL' if err else 'ok':4}  {name}", flush=True)
            if err:
                print("        " + err.replace("\n", "\n        ")[:2000])
                failed += 1
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
