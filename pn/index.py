"""Generate the exercise list "exercises/Seznam úloh.md" from the catalogue.

    python3 -m pn.index

Status (shown in Czech): `todo` „chybí“ (no folder yet), `drafted` „návrh“ (net.py exists),
`reviewed` „zkontrolováno“ (the user confirmed the interpretation, which is marked by renaming
the note's section „Interpretace“ to „Nápověda“). The list itself is in Czech, like the notes.
"""

from pathlib import Path

from .catalog import START, categories, exercises, folder

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "exercises" / "Seznam úloh.md"

HEAD = """\
# Seznam úloh

<!-- Generuje `make index` (python3 -m pn.index) z pn/catalog.py; needitovat ručně. -->

Všechny úlohy na Petriho sítě ze studijních materiálů IMS, rozdělené do kategorií: nejdřív základní modely, pak jednotlivé mechanismy jako v krátkých zkouškových otázkách, pak značení v čase t a nakonec celé slovní úlohy jako na půlsemestrálce. V každé kategorii jsou novější úlohy první. Sloupec *Původ* říká, odkud úloha pochází; podrobnosti jsou v poslední části poznámky.

Po otevření poznámky je vidět jen zadání. Nejdřív se úlohu pokus vyřešit bez nápovědy, pak otevírej skryté části jednu po druhé: nápovědu, Petriho síť, časté chyby, model v SIMLIB a zdroje. Každá poznámka je vedle i jako PDF.

Stav: *návrh* = síť je hotová a prošla kontrolami (`make check`), výklad zadání ještě nebyl potvrzen (část *Interpretace*); *zkontrolováno* = výklad je potvrzený (část *Nápověda*); *chybí* = úloha ještě není zpracovaná.
"""


LABEL = {"todo": "chybí", "drafted": "návrh", "reviewed": "zkontrolováno"}


def status(folder):
    d = ROOT / "exercises" / folder
    if not (d / "net.py").exists():
        return "todo"
    note = d / f"{d.name}.md"
    return "reviewed" if note.exists() and "\n## Nápověda\n" in note.read_text() else "drafted"


def index():
    cats = list(categories())
    st = [status(f) for f, _, _ in exercises()]
    out = [HEAD, f"Zpracováno {len(st) - st.count('todo')} ze {len(st)} úloh, "
                 f"zkontrolováno {st.count('reviewed')}.\n",
           "| Č. | Kategorie | Úloh | Zkontrolováno |", "|---|---|---|---|"]
    for cat, title, exs in cats:
        n = cat.split(" - ")[0]
        rev = sum(status(f) == "reviewed" for f, _, _ in exs)
        out.append(f"| {n} | [{title}](<{cat}/>) | {len(exs)} | {rev} |")
    out.append("")
    out += ["## Začni tady", "",
            "Patnáct úloh na začátek: nejdřív každý vzor z [Notace a vzory](<../notation/Notace a vzory.md>) aspoň jednou, "
            "pak nejnovější půlsemestrálky.", ""]
    for i, (name, what) in enumerate(START, 1):
        f = folder(name)
        out.append(f"{i}. [{name}](<{f}/{f.split('/')[1]}.md>): {what}")
    out.append("")
    for cat, title, exs in cats:
        out += [f"## {cat.split(' - ')[0]} {title}", "", "| Č. | Úloha | Původ | Stav |", "|---|---|---|---|"]
        for f, name, origin in exs:
            s = status(f)
            cell = f"[{name}](<{f}/{f.split('/')[1]}.md>)" if s != "todo" else name
            out.append(f"| {f.split('/')[1].split(' - ')[0]} | {cell} | {origin} | {LABEL[s]} |")
        out.append("")
    return "\n".join(out)


def main():
    INDEX.write_text(index())


if __name__ == "__main__":
    main()
