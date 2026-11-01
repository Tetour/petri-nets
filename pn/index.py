"""Regenerate the exercise index in README.md from the catalogue.

    python3 -m pn.index

Status: `todo` (no folder yet), `drafted` (net.py exists), `reviewed` (the user confirmed the
interpretation, which is marked by renaming the note's section „Interpretace“ to „Nápověda“).
"""

from pathlib import Path

from .catalog import categories, exercises

ROOT = Path(__file__).resolve().parent.parent
START, END = "<!-- index:start -->", "<!-- index:end -->"


def status(folder):
    d = ROOT / "exercises" / folder
    if not (d / "net.py").exists():
        return "todo"
    note = d / f"{d.name}.md"
    return "reviewed" if note.exists() and "\n## Nápověda\n" in note.read_text() else "drafted"


def table():
    out = []
    st = [status(f) for f, _, _ in exercises()]
    out.append(f"{len(st) - st.count('todo')} of {len(st)} exercises drafted, "
               f"{st.count('reviewed')} reviewed.\n")
    for cat, title, exs in categories():
        out += [f"### {cat.split(' - ')[0]} {title}", "", "| Č. | Úloha | Původ | Status |", "|---|---|---|---|"]
        for f, name, origin in exs:
            s = status(f)
            note = f"exercises/{f}/{f.split('/')[1]}.md"
            cell = f"[{name}](<{note}>)" if s != "todo" else name
            out.append(f"| {f.split('/')[1].split(' - ')[0]} | {cell} | {origin} | {s} |")
        out.append("")
    return "\n".join(out)


def main():
    readme = ROOT / "README.md"
    s = readme.read_text()
    a, b = s.index(START) + len(START), s.index(END)
    readme.write_text(s[:a] + "\n" + table() + s[b:])


if __name__ == "__main__":
    main()
