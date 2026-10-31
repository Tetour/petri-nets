"""Regenerate the exercise index in README.md from the catalogue.

    python3 -m pn.index

Status: `todo` (no folder yet), `drafted` (net.py exists), `reviewed` (the user confirmed the
interpretation, which is marked by renaming the note's section „Interpretace“ to „Nápověda“).
"""

from pathlib import Path

from .catalog import EXERCISES, TOPICS, folder

ROOT = Path(__file__).resolve().parent.parent
START, END = "<!-- index:start -->", "<!-- index:end -->"
def status(ex_id):
    d = ROOT / "exercises" / folder(ex_id)
    if not (d / "net.py").exists():
        return "todo"
    note = d / f"{folder(ex_id)}.md"
    return "reviewed" if note.exists() and "\n## Nápověda\n" in note.read_text() else "drafted"


def table():
    out = []
    st = [status(i) for i, _, _ in EXERCISES]
    out.append(f"{len(st) - st.count('todo')} of {len(EXERCISES)} exercises drafted, "
               f"{st.count('reviewed')} reviewed.\n")
    for t, title in TOPICS.items():
        out += [f"### {t} {title}", "", "| Id | Úloha | Původ | Status |", "|---|---|---|---|"]
        for i, name, origin in EXERCISES:
            if not i.startswith(t + "–"):
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
