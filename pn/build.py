"""Build and check nets.

    python3 -m pn.build [--check-only] [PATH ...]

Every directory under exercises/ and notation/ containing a `net.py` is a net.
For each one: lint + simulation checks, then TikZ -> PDF -> SVG (next to
net.py) and a PNG preview in build/.
"""

import argparse
import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path

from . import lint, sim, tikz

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"


def find(paths):
    roots = [Path(p).resolve() for p in paths] or [ROOT / "exercises", ROOT / "notation"]
    for r in roots:
        if r.is_file():
            yield r
        else:
            yield from sorted(r.rglob("net.py"))


def load(path):
    spec = importlib.util.spec_from_file_location(f"net_{abs(hash(path))}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.net


def render(net, src):
    out = BUILD / src.parent.relative_to(ROOT)
    out.mkdir(parents=True, exist_ok=True)
    (out / "net.tex").write_text(tikz.document(net))
    r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "net.tex"],
                       cwd=out, capture_output=True, text=True)
    if r.returncode:
        err = [l for l in r.stdout.splitlines() if l.startswith("!")][:3]
        raise RuntimeError(f"pdflatex failed: {err} (see {out / 'net.log'})")
    shutil.copy(out / "net.pdf", src.parent / "net.pdf")
    subprocess.run(["pdftocairo", "-svg", "net.pdf", str(src.parent / "net.svg")], cwd=out, check=True)
    subprocess.run(["pdftoppm", "-png", "-r", "110", "-singlefile", "net.pdf", "net"], cwd=out, check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-only", action="store_true")
    ap.add_argument("paths", nargs="*")
    args = ap.parse_args()
    failed = 0
    for src in find(args.paths):
        name = src.parent.relative_to(ROOT)
        try:
            net = load(src)
            problems = lint.lint(net) + sim.check(net)
            if not args.check_only:
                render(net, src)
        except Exception as e:  # report and continue with the other nets
            problems = [f"{type(e).__name__}: {e}"]
        status = "ok" if not problems else "FAIL"
        print(f"{status:4}  {name}")
        for p in problems:
            print(f"        - {p}")
        failed += bool(problems)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
