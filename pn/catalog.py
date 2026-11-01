"""Catalogue of all exercises: category, Czech name, origin.

Categories go from basic models over single mechanisms (exam-style M/M/1 variants) to
marking at time t and full word problems (midterms); within a category, newer first.
A category's folder is "<NN> - <short name>" and an exercise's folder and note are
"<NN> - <name>" inside it; the numbers are positions in this file. Exercise names are
unique, so notes refer to another exercise by its name.
"""

import os

# (short name = folder, full name = heading in the exercise index exercises/Readme.md, [(name, origin)])
CATEGORIES = [
    ('Základní modely', 'Základní modely (přednášky)', [
        ('Opravářská dílna', 'přednáška, slajdy 157–164'),
        ('Samoobsluha', 'přednáška, slajdy 195–198'),
        ('Zdravotní ordinace', 'poznámky MSI (stochastické PN)'),
        ('Výrobní systém', 'poznámky MSI (P/T sítě)'),
        ('Kritická sekce', 'poznámky MSI (P/T sítě)'),
        ('Kravín', 'příklad z přednášky (tabule luppo)'),
    ]),
    ('Netrpělivost a omezená fronta', 'Netrpělivost, omezená fronta, opakování', [
        ('Netrpělivé požadavky', 'zkouška 2017/18 1. t. (8H, 7A); 2023/24 1. t. A'),
        ('Netrpělivý první ve frontě', 'zkouška 2017/18 2. t. A; 2019/20 2. t. Y; 2024/25 2. t. E'),
        ('Příklad s netrpělivou transakcí', 'zkouška 2019/20 1. opravný; 2020/21 3. t. C'),
        ('Fronta omezená na 10', 'zkouška 2017/18 1. t. 8C'),
        ('MM3 bez fronty s opakováním', 'zkouška 2023/24 1. t. B'),
    ]),
    ('Poruchy', 'Poruchy a přerušení obsluhy', [
        ('Porucha zruší obsluhu', 'zkouška 2017/18 1. t. Z'),
        ('Porucha vrací transakci do fronty', 'zkouška 2019/20 1. opravný, sk. B'),
        ('Porucha s opravou, návrat do fronty', 'zkouška 2024/25 1. t. A'),
        ('Porucha s opravou, transakce odchází', 'zkouška 2021/22 1. t. A'),
        ('Kritická havárie', 'zkouška 2025/26 1. t. C'),
        ('Porucha zničí obsluhu nebo počká', 'zkouška 2021/22 2. t.'),
        ('Každá 10. transakce vyvolá poruchu', 'zkouška 2021/22 1. t. B'),
        ('Porucha prodlouží další obsluhu', 'zkouška 2017/18 3. t. A'),
        ('Porucha prodlouží obsluhu o 2', 'zkouška 2020/21 1. opravný (11:00)'),
        ('Porucha prodlouží probíhající obsluhu o 5', 'zkouška 2020/21 náhradní termín'),
        ('Přerušení příliš dlouhé obsluhy', 'zkouška 2019/20 2. t. Z'),
    ]),
    ('Údržba a spánek', 'Údržba, nečinnost, spánek', [
        ('Automat na kávu – údržba po nečinnosti', 'zkouška 2017/18 2. t. B; 2018/19 1. t.'),
        ('Automat na kávu – údržba po 50 obsluhách', 'zkouška 2017/18 2. t. C; 2018/19 1. t.'),
        ('Automat na kávu – uspání', 'zkouška 2017/18 2. t. D'),
        ('Údržba při prázdné frontě', 'zkouška 2019/20 1. t. D; 2020/21 1. t.'),
        ('Údržba po dlouhé obsluze', 'zkouška 2021/22 1. t. D'),
        ('Údržba po každé 10. obsluze', 'zkouška 2022/23 1. t. D'),
        ('Údržbář na obchůzce', 'zkouška 2022/23 1. t. C'),
        ('Spánek po nečinnosti', 'zkouška 2022/23 2. t. F'),
    ]),
    ('Délka fronty a kapacita', 'Řízení podle délky fronty a kapacita', [
        ('Doba obsluhy podle délky fronty', 'zkouška 2019/20 1. t.; 2020/21 1. t.'),
        ('Dočasně MM2 při dlouhé frontě', 'zkouška 2018/19 3. t.'),
        ('Natrvalo MM3 při dlouhé frontě', 'zkouška 2020/21 1. t.'),
        ('Interval příchodů podle délky fronty', 'zkouška 2021/22 1. t. C; 2022/23 1. t. A'),
        ('Přerušení příchodů při plné frontě', 'zkouška 2024/25 1. t. B'),
        ('MM3 – zastavení příchodů', 'zkouška 2024/25 1. t. C'),
        ('Každá 100. transakce vyprázdní frontu', 'zkouška 2022/23 2. t. E'),
        ('Sklad s dočasně větší kapacitou', 'zkouška 2017/18 3. t. Z'),
        ('Údržba zabere celou kapacitu', 'zkouška 2025/26 2. t. E'),
        ('Pomocník přidá kapacitu', 'zkouška 2025/26 2. t. F'),
    ]),
    ('Doba obsluhy podle stavu', 'Doba obsluhy podle stavu', [
        ('MD1 – prodlužování po 10 obsluhách', 'zkouška 2024/25 2. t. F'),
        ('MD1 – střídání 2 a 3', 'zkouška 2025/26 1. t. A'),
        ('MD3 – poslední volné zařízení', 'zkouška 2024/25 3. t. H'),
        ('MD1 – podle doby od poslední obsluhy', 'zkouška 2020/21 1. opravný'),
    ]),
    ('Priority', 'Priority', [
        ('Příklad s prioritou procesu', 'zkouška 2019/20 3. t. A'),
        ('Každá N-tá s prioritou procesu', 'zkouška 2022/23 3. t. G'),
        ('Každá 10. s prioritou obsluhy', 'zkouška 2022/23 3. t. H'),
        ('Dva proudy příchodů', 'zkouška 2025/26 1. t. B'),
        ('Priorita procesu a obsluhy', 'zkouška 2025/26 1. t. C (otázka 3)'),
        ('MM3 – prioritní zabírají 2 linky', 'zkouška 2018/19 (Řešené výpočetní příklady)'),
    ]),
    ('Značení v čase t', 'Značení v čase t (D/D/x)', [
        ('DD2 FIFO, čas 6,5', 'zkouška 2012/13 2. t. C'),
        ('DD3 LIFO, čas 10,5', 'zkouška 2015/16 3. t. 5-A; 2014/15 1. t. C'),
        ('DD2 LIFO obsluha 6, čas 13,5', 'zkouška 2015/16 3. t. 5-D'),
        ('DD2 LIFO obsluha 5, čas 9,5', 'zkouška 2014/15 1. t. B; 2015/16 2. t.'),
        ('DD2 LIFO obsluha 4, čas 9,5', 'zkouška 2015/16 2. t. A'),
        ('DD4 LIFO, čas 9,5', 'zkouška 2014/15 3. t. D'),
        ('DD3 FIFO, čas 9,5', 'zkouška 2015/16 1. t. 5H'),
        ('DD1 – příchody 2, obsluha 4', 'zkouška 2022/23 3. t. G'),
        ('DD1 – příchody 3, obsluha 2', 'zkouška 2022/23 3. t. H'),
    ]),
    ('Obsluha zákazníků', 'Slovní úlohy: obsluha zákazníků', [
        ('Úřad', 'půlsemestrálka 2025/26 D'),
        ('Obslužné centrum', 'půlsemestrálka 2025/26 B'),
        ('Psí salon', 'půlsemestrálka 2025/26 A'),
        ('Centrum MM1 s rychlým režimem', 'půlsemestrálka 2024/25 D'),
        ('Pizza stánek', 'půlsemestrálka 2024/25 B'),
        ('Klientské centrum', 'půlsemestrálka 2023/24 D'),
        ('Automat na kávu', 'půlsemestrálka 2023/24 C'),
        ('Cestovní kancelář', 'půlsemestrálka 2022/23 D'),
        ('Trafika', 'půlsemestrálka 2022/23 B'),
        ('Kopírovací centrum', 'půlsemestrálka 2022/23 A'),
        ('Kopírovací centrum s poruchami', 'půlsemestrálka 2021/22 D'),
        ('Pošta', 'půlsemestrálky 2014–19, Z19'),
        ('Letiště', 'půlsemestrálky 2014–19, Z17'),
        ('Pekárna', 'půlsemestrálky 2014–19, Z14'),
        ('Úřad s dodatečnými přepážkami', 'půlsemestrálky 2014–19, Z10'),
        ('Menza', 'půlsemestrálky 2014–19, Z9'),
        ('Hudební rádio', 'půlsemestrálky 2014–19, Z7'),
        ('Nemocniční ambulance', 'půlsemestrálky 2014–19, Z6'),
        ('Banka se třemi pracovníky', 'půlsemestrálka 2013/14 A'),
        ('Pražírna kávy', 'půlsemestrálka 2010/11'),
        ('Banka a lupič', 'půlsemestrálka 2010/11'),
        ('Telefonní ústředna', 'půlsemestrálka (rok neznámý, Studentská skripta 2015/16)'),
    ]),
    ('Počítačové systémy', 'Slovní úlohy: počítačové systémy', [
        ('Server s údržbou po 1000 požadavcích', 'půlsemestrálka 2023/24 A'),
        ('Výpočetní služba se spánkem', 'půlsemestrálka 2023/24 B'),
        ('Databázový server', 'půlsemestrálky 2014–19, Z22'),
        ('Počítačový server', 'půlsemestrálka 2013/14 C'),
        ('Zvuková karta', 'půlsemestrálka (rok neznámý, Příprava 2021/22)'),
    ]),
    ('Doprava a dávky', 'Slovní úlohy: doprava a dávky', [
        ('Výletní autobus', 'půlsemestrálka 2025/26 C'),
        ('Vyhlídkové lety', 'půlsemestrálka 2024/25 C'),
        ('Pizzerie s rozvozem', 'půlsemestrálka 2022/23 C'),
        ('Výletní loď', 'půlsemestrálka 2021/22 C'),
        ('Překladiště kontejnerů', 'půlsemestrálka 2021/22 A'),
        ('Festivalový autobus', 'půlsemestrálky 2014–19, Z21'),
        ('Vyhlídková loď na molu', 'půlsemestrálky 2014–19, Z18'),
        ('Přepravní firma', 'půlsemestrálky 2014–19, Z12'),
        ('Překladiště s jeřábem', 'půlsemestrálky 2014–19, Z5'),
        ('Bagrista a nákladní auta', 'půlsemestrálky 2014–19, Z4'),
        ('Výletní loď na jezeře', 'půlsemestrálky 2014–19, Z1'),
        ('Přehrada s přístavišti', 'půlsemestrálka 2011/12'),
        ('Pošta s doporučenými zásilkami', 'půlsemestrálka 2011/12'),
        ('Přehrada s vyhlídkovou lodí', 'půlsemestrálka (rok neznámý, Příprava 2021/22)'),
    ]),
    ('Výroba a sklady', 'Slovní úlohy: výroba, zdroje a sklady', [
        ('Zahradnictví a bouřka', 'půlsemestrálka 2024/25 A'),
        ('Sběrači jahod', 'půlsemestrálka 2021/22 B'),
        ('Výrobní hala', 'půlsemestrálky 2014–19, Z24'),
        ('Jahodová farma', 'půlsemestrálky 2014–19, Z23'),
        ('Spalovna se třemi vozy', 'půlsemestrálky 2014–19, Z20'),
        ('Moštárna', 'půlsemestrálky 2014–19, Z16'),
        ('Spalovna', 'půlsemestrálky 2014–19, Z15'),
        ('Hasiči', 'půlsemestrálky 2014–19, Z13'),
        ('Přečerpávací elektrárna II', 'půlsemestrálky 2014–19, Z11'),
        ('Zahradník na FIT', 'půlsemestrálky 2014–19, Z8'),
        ('Přečerpávací elektrárna', 'půlsemestrálky 2014–19, Z3'),
        ('Uhelný mlýn', 'půlsemestrálky 2014–19, Z2'),
        ('Stavba z betonu', 'půlsemestrálka 2013/14 D'),
        ('Výroba hrášku', 'půlsemestrálka 2013/14 B'),
        ('Dílna se třemi stroji', 'půlsemestrálka 2011/12'),
        ('Tunel', 'půlsemestrálka 2011/12'),
        ('Chmelová brigáda', 'půlsemestrálka 2010/11'),
        ('Logistická centrála', 'půlsemestrálka 2010/11'),
    ]),
]


def categories():
    """(category folder, full name, [(exercise folder relative to exercises/, name, origin)])"""
    for c, (short, title, exercises) in enumerate(CATEGORIES, 1):
        cat = f"{c:02d} - {short}"
        yield cat, title, [(f"{cat}/{e:02d} - {n}", n, o) for e, (n, o) in enumerate(exercises, 1)]


def exercises():
    """(exercise folder relative to exercises/, name, origin) of every exercise"""
    for _, _, exs in categories():
        yield from exs


def folder(name):
    """Folder of the exercise called `name`, relative to exercises/."""
    for f, n, _ in exercises():
        if n == name:
            return f
    raise KeyError(name)


def link(name, base="exercises/_/_"):
    """Markdown link to an exercise's note from a file in `base` (relative to the repo
    root); the default is another exercise's folder."""
    f = folder(name)
    note = f"exercises/{f}/{f.split('/')[1]}.md"
    return f"[{name}](<{os.path.relpath(note, base)}>)"
