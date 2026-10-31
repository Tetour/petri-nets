"""Regenerate the exercise index in README.md from the catalogue.

    python3 -m pn.index

Status: `todo` (no folder yet), `drafted` (net.py exists), `reviewed` (in REVIEWED).
"""

from pathlib import Path

from .catalog import EXERCISES, TOPICS, folder

ROOT = Path(__file__).resolve().parent.parent
START, END = "<!-- index:start -->", "<!-- index:end -->"
REVIEWED = set()


def status(ex_id):
    if ex_id in REVIEWED:
        return "reviewed"
    return "drafted" if (ROOT / "exercises" / folder(ex_id) / "net.py").exists() else "todo"


def table():
    out = []
    done = sum(status(i) != "todo" for i, _, _ in EXERCISES)
    out.append(f"{done} of {len(EXERCISES)} exercises drafted.\n")
    for t, title in TOPICS.items():
        out += [f"### {t} {title}", "", "| Id | Úloha | Původ | Status |", "|---|---|---|---|"]
        for i, name, origin in EXERCISES:
            if not i.startswith(t + "."):
                continue
            st = status(i)
            cell = f"[{name}](<exercises/{folder(i)}/{folder(i)}.md>)" if st != "todo" else name
            out.append(f"| {i} | {cell} | {origin} | {st} |")
        out.append("")
    return "\n".join(out)


def main():
    readme = ROOT / "README.md"
    s = readme.read_text()
    a, b = s.index(START) + len(START), s.index(END)
    readme.write_text(s[:a] + "\n" + table() + s[b:])


if __name__ == "__main__":
    main()
