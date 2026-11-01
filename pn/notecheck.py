"""Check every exercise note against the rules in notation/Note.md.

    python3 -m pn.notecheck [PATH ...]

Prints one line per problem (note, line, what is wrong) and exits with 1 if there is any.
"""

import re
import sys
from pathlib import Path
from urllib.parse import unquote

from .catalog import exercises
from .notes import find

ROOT = Path(__file__).resolve().parent.parent

# section heading -> text of its toggle; Zadání has no toggle
SECTIONS = [
    ("Zadání", None),
    (("Interpretace", "Nápověda"), None),
    ("Petriho síť", "Zobrazit Petriho síť"),
    ("Časté chyby", "Zobrazit časté chyby"),
    ("SIMLIB", "Zobrazit SIMLIB kód"),
    ("Původ a zdroje", "Zobrazit původ a zdroje"),
]
SUMMARY = {"Interpretace": "Zobrazit interpretaci (nápověda)", "Nápověda": "Zobrazit nápovědu"}

# time wordings that Note.md replaces by „exponenciálně se středem …“, „rovnoměrně …“, „přesně …“
OLD_TIMES = [r"rozložen", r"rozdělen", r"střední hodnot", r"\bexp\.", r"\buniform\(", r"\bExp\("]
# lines that only say what to produce (Note.md: left out of Zadání)
INSTRUCTIONS = [
    r"Zadaný systém modelujte",
    r"Modelujte zadaný systém",
    r"V modelu jednoznačně ukažte",
    r"Vyznačte přechodem, kde transakce opouští systém",
    r"^\\?\+ SIMLIB",
    r"Napište program v SIMLIBU? pro systém z předchozího",
]
# an exercise id of the old TT–NN scheme used as a reference
OLD_ID = re.compile(r"\[\d\d–\d\d[\] ]|\b(?:úloh\w*|[vV]iz) \d\d–\d\d\b|\bv \d\d–\d\d(?=[\s:.,)])(?! ?(?:min|s\b|h\b|minut|sekund|hodin))")
LINK = re.compile(r"\]\((<)?([^)>\s]+|[^>]+)(?(1)>)\)")


def check(note: Path):
    problems = []
    text = note.read_text()
    lines = text.split("\n")

    def bad(line_no, msg):
        problems.append(f"{note.parent.name}:{line_no}: {msg}")

    name = note.parent.name.split(" - ", 1)[1]
    if lines[0] != f"# {name}":
        bad(1, f"the heading must be „# {name}“")

    heads = [(i + 1, l[3:]) for i, l in enumerate(lines) if l.startswith("## ")]
    names = [h for _, h in heads]
    expected = [s if isinstance(s, str) else (names[1] if len(names) > 1 and names[1] in s else s[0])
                for s, _ in SECTIONS]
    if names != expected:
        bad(heads[0][0] if heads else 1, f"sections {names} instead of {expected}")
        return problems

    bounds = [n for n, _ in heads] + [len(lines) + 1]
    body = {h: lines[bounds[k]:bounds[k + 1] - 1] for k, (_, h) in enumerate(heads)}
    start = {h: bounds[k] for k, (_, h) in enumerate(heads)}

    for h in names[1:]:
        b, s = body[h], start[h]
        summary = SUMMARY.get(h) or dict((n, t) for n, t in SECTIONS if isinstance(n, str))[h]
        want = ["", "<details>", f"<summary>{summary}</summary>", "<br>", ""]
        if b[:5] != want:
            bad(s + 1, f"„{h}“ must start with <details>, <summary>{summary}</summary>, <br> and an empty line")
        tail = [l for l in b if l.strip()][-1:]
        if tail != ["</details>"]:
            bad(s, f"„{h}“ must end with </details>")

    net = [l for l in body["Petriho síť"][5:] if l.strip() and l != "</details>"]
    if len(net) != 1 or not re.fullmatch(r"!\[Petriho síť – [^\]]+\]\(net\.svg\)", net[0]):
        bad(start["Petriho síť"], "„Petriho síť“ must hold only the image ![Petriho síť – …](net.svg)")

    for i, l in enumerate(body["Zadání"]):
        n = start["Zadání"] + 1 + i
        if not l.startswith(">"):
            continue
        for p in OLD_TIMES:
            if re.search(p, l, re.I):
                bad(n, f"time not in the Note.md form („{re.search(p, l, re.I).group(0)}“)")
        for p in INSTRUCTIONS:
            if re.search(p, l[1:].strip().strip("*")):
                bad(n, "instruction-only line in Zadání (move it to Původní znění)")

    original = "\n".join(body["Původ a zdroje"])
    m = re.search(r"\*\*Původní znění:\*\*[^\n]*\n\n((?:>.*\n?)+)", original)
    zadani = "\n".join(l for l in body["Zadání"] if l.startswith(">"))
    if m and m.group(1).strip() == zadani.strip():
        bad(start["Původ a zdroje"], "Původní znění is identical to Zadání (drop it)")

    if not re.search(r"```cpp\n", "\n".join(body["SIMLIB"])):
        bad(start["SIMLIB"], "SIMLIB has no ```cpp code block")

    in_code = False
    for i, l in enumerate(lines, 1):
        if l.startswith("```"):
            in_code = not in_code
        if in_code:
            continue
        if OLD_ID.search(l):
            bad(i, f"old exercise id „{OLD_ID.search(l).group(0).strip()}“: refer to the exercise by name")
        for mm in LINK.finditer(l):
            t = mm.group(2).split("#")[0]
            if not t or re.match(r"[a-z]+:", t):
                continue
            if not (note.parent / (t if mm.group(1) else unquote(t))).exists():
                bad(i, f"broken link „{t}“")
    return problems


def main():
    notes = find(sys.argv[1:])
    problems = [p for n in notes for p in check(n)]
    if not sys.argv[1:]:
        have = {n.parent.relative_to(ROOT / "exercises").as_posix() for n in notes}
        problems += [f"{f}: listed in pn/catalog.py but has no note" for f, _, _ in exercises() if f not in have]
    for p in problems:
        print(p)
    print(f"{len(notes)} notes, {len(problems)} problems")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
