"""Compile and run the SIMLIB code of every note that has a SIMLIB section.

    python3 -m pn.simlib [-j N] [PATH ...]

The C++ block of the section is extracted to build/simlib/<exercise>/model.cc, compiled
with g++ against SIMLIB (provided by the Nix dev shell) and run; it must exit with 0.
"""

import argparse
import os
import re
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build" / "simlib"


def code(note: Path):
    s = note.read_text()
    m = re.search(r"\n## SIMLIB\n(.*?)(?=\n## |\Z)", s, re.S)
    if not m:
        return None
    blocks = re.findall(r"```cpp\n(.*?)```", m.group(1), re.S)
    return "\n".join(blocks) if blocks else None


def check(note: Path):
    out = BUILD / note.parent.name
    out.mkdir(parents=True, exist_ok=True)
    (out / "model.cc").write_text(code(note))
    r = subprocess.run(["g++", "-std=c++17", "-O2", "-Wall", "-Wextra", "-o", "model", "model.cc", "-lsimlib"],
                       cwd=out, capture_output=True, text=True)
    if r.returncode:
        return note.parent.name, "compilation failed:\n" + r.stderr[-2000:]
    warnings = r.stderr.strip()
    try:
        r = subprocess.run(["./model"], cwd=out, capture_output=True, text=True, timeout=300)
    except subprocess.TimeoutExpired:
        return note.parent.name, "the model did not finish within 300 s"
    (out / "output.txt").write_text(r.stdout)
    if r.returncode:
        return note.parent.name, f"the model exited with {r.returncode}:\n" + r.stderr[-2000:]
    return note.parent.name, ("compiler warnings:\n" + warnings) if warnings else ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-j", "--jobs", type=int, default=os.cpu_count())
    ap.add_argument("paths", nargs="*")
    args = ap.parse_args()
    dirs = [Path(p).resolve() for p in args.paths] or sorted((ROOT / "exercises").iterdir())
    # a folder that is not itself an exercise (e.g. exercises/) stands for all exercises in it
    dirs = [e for d in dirs for e in ([d] if (d / f"{d.name}.md").exists() else sorted(d.iterdir()))]
    notes = [d / f"{d.name}.md" for d in dirs if (d / f"{d.name}.md").exists()]
    notes = [n for n in notes if code(n)]
    failed = 0
    with ProcessPoolExecutor(max_workers=args.jobs) as pool:
        for name, problem in pool.map(check, notes):
            print(f"{'FAIL' if problem else 'ok':4}  {name} (SIMLIB)", flush=True)
            if problem:
                print("        " + problem.replace("\n", "\n        "))
                failed += 1
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
