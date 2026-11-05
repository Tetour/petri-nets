"""Generate the exercise list "exercises/Seznam úloh.md" and the study plan
"exercises/Studijní plán.md" from the catalogue.

    python3 -m pn.index

The list is in Czech, like the notes.
"""

from pathlib import Path

from .catalog import PLAN, START, categories, exercises, folder

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "exercises" / "Seznam úloh.md"
PLAN_FILE = ROOT / "exercises" / "Studijní plán.md"

HEAD = """\
# Seznam úloh

<!-- Generuje `make index` (python3 -m pn.index) z pn/catalog.py; needitovat ručně. -->

Všechny úlohy na Petriho sítě ze studijních materiálů IMS, rozdělené do kategorií: nejdřív základní modely, pak jednotlivé mechanismy jako v krátkých zkouškových otázkách, pak značení v čase t a nakonec celé slovní úlohy jako na půlsemestrálce. V každé kategorii jsou novější úlohy první. Sloupec *Původ* říká, odkud úloha pochází; podrobnosti jsou v poslední části poznámky.

Doporučené pořadí všech úloh je ve [Studijním plánu](<Studijní plán.md>).

Po otevření poznámky je vidět jen zadání. Nejdřív se úlohu pokus vyřešit bez nápovědy, pak otevírej skryté části jednu po druhé: nápovědu, Petriho síť, časté chyby, model v SIMLIB a zdroje. Každá poznámka je vedle i jako PDF.
"""


def index():
    cats = list(categories())
    out = [HEAD, f"Celkem {len(list(exercises()))} úloh.\n", "| Č. | Kategorie | Úloh |", "|---|---|---|"]
    for cat, title, exs in cats:
        out.append(f"| {cat.split(' - ')[0]} | [{title}](<{cat}/>) | {len(exs)} |")
    out.append("")
    out += ["## Začni tady", "",
            "Patnáct úloh na začátek: nejdřív každý vzor z [Notace a vzory](<../basics/Notace a vzory.md>) aspoň jednou, "
            "pak nejnovější půlsemestrálky.", ""]
    for i, (name, what) in enumerate(START, 1):
        f = folder(name)
        out.append(f"{i}. [{name}](<{f}/{f.split('/')[1]}.md>): {what}")
    out.append("")
    for cat, title, exs in cats:
        out += [f"## {cat.split(' - ')[0]} {title}", "", "| Č. | Úloha | Původ |", "|---|---|---|"]
        for f, name, origin in exs:
            out.append(f"| {f.split('/')[1].split(' - ')[0]} | [{name}](<{f}/{f.split('/')[1]}.md>) | {origin} |")
        out.append("")
    return "\n".join(out)


PLAN_HEAD = """\
# Studijní plán

<!-- Generuje `make index` (python3 -m pn.index) z pn/catalog.py; needitovat ručně. -->

Všech {n} úloh v pořadí, ve kterém se je vyplatí řešit: nejdřív vzory a nejnovější půlsemestrálky, pak mechanismy, které vzory přímo neukazují, zbylé nové půlsemestrálky, značení v čase t, a nakonec opakování a starší úlohy. Číslování běží přes celý plán, takže stačí si pamatovat číslo poslední vyřešené úlohy. Úlohy podle kategorií jsou v [Seznamu úloh](<Seznam úloh.md>).

Než začneš, projdi [Notace a vzory](<../basics/Notace a vzory.md>) a [Jak síť funguje](<../basics/Jak síť funguje.md>).
"""


def plan():
    names = [name for _, _, items in PLAN for name, _ in items]
    every = [name for _, name, _ in exercises()]
    assert sorted(names) == sorted(every), (
        f"missing: {set(every) - set(names)}, extra: {set(names) - set(every)}, "
        f"twice: {set(n for n in names if names.count(n) > 1)}")
    out = [PLAN_HEAD.format(n=len(every))]
    i = 0
    for p, (heading, intro, items) in enumerate(PLAN, 1):
        out += [f"## {p}. {heading} ({i + 1}–{i + len(items)})", "", intro, ""]
        for name, what in items:
            i += 1
            f = folder(name)
            out.append(f"{i}. [{name}](<{f}/{f.split('/')[1]}.md>): {what}")
        out.append("")
    return "\n".join(out)


def main():
    INDEX.write_text(index())
    PLAN_FILE.write_text(plan())


if __name__ == "__main__":
    main()
