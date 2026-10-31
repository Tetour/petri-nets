"""Render every exercise note to a PDF next to it (an alternative to the Markdown preview).

    python3 -m pn.notes [-j N] [PATH ...]

The collapsed sections are expanded in the PDF, but the hint and the net each start on a
new page, so the first page shows only the task. Links to other exercises point to their
PDFs; the diagram is embedded as net.pdf (vector).
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

PANDOC = [
    "pandoc", "-f", "markdown-smart-implicit_figures",
    "-V", "mainfont=DejaVu Sans", "-V", "monofont=DejaVu Sans Mono",
    "-V", "fontsize=10pt", "-V", "geometry:margin=2cm", "-V", "lang=cs",
    "-V", "colorlinks=true", "-V", "linkcolor=blue", "-V", "urlcolor=blue",
    "-V", "pagestyle=plain", "-V", "papersize=a4",
]

NEW_PAGE_BEFORE = ("## Interpretace", "## Nápověda", "## Petriho síť")


def prepare(md: str) -> str:
    md = md.replace("️", "")                                   # emoji variation selector
    md = re.sub(r"(?m)^<details>\n<summary>[^<]*</summary>\n(<br>\n)?", "", md)
    md = re.sub(r"(?m)^</details>\n", "", md)
    md = md.replace("](net.svg)", "](net.pdf)")
    md = re.sub(r"\]\(<([^>]+)\.md>\)", r"](<\1.pdf>)", md)          # links to other notes
    for h in NEW_PAGE_BEFORE:
        md = md.replace(f"\n{h}\n", f"\n\\newpage\n\n{h}\n")
    return md


def render(note: Path):
    """Pandoc writes LaTeX, xelatex runs in a fixed directory: with a fixed date this makes
    the PDF byte-identical between builds (pandoc's own temporary directory would not)."""
    out = BUILD / note.parent.name
    out.mkdir(parents=True, exist_ok=True)
    md = prepare(note.read_text()).replace("](net.pdf)", f"](<{note.parent / 'net.pdf'}>)")
    (out / "note.md").write_text(md)
    r = subprocess.run(PANDOC + ["-s", "note.md", "-o", "note.tex"], cwd=out, capture_output=True, text=True)
    if r.returncode:
        return note.parent.name, r.stderr.strip()
    env = dict(os.environ, SOURCE_DATE_EPOCH="0", FORCE_SOURCE_DATE="1")
    r = subprocess.run(["xelatex", "-interaction=nonstopmode", "-halt-on-error", "note.tex"],
                       cwd=out, capture_output=True, text=True, env=env)
    if r.returncode:
        return note.parent.name, "\n".join(l for l in r.stdout.splitlines() if l.startswith("!"))[:1000]
    shutil.copy(out / "note.pdf", note.with_suffix(".pdf"))
    return note.parent.name, ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-j", "--jobs", type=int, default=os.cpu_count())
    ap.add_argument("paths", nargs="*")
    args = ap.parse_args()
    dirs = [Path(p).resolve() for p in args.paths] or sorted((ROOT / "exercises").iterdir())
    notes = [d / f"{d.name}.md" for d in dirs if (d / f"{d.name}.md").exists()]
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
