"""Catalogue of all exercises: category, Czech name, origin.

Categories go from basic models over single mechanisms (exam-style M/M/1 variants) to
marking at time t and full word problems (midterms); within a category, newer first.
A category's folder is "<NN> - <short name>" and an exercise's folder and note are
"<NN> - <name>" inside it; the numbers are positions in this file. Exercise names are
unique, so notes refer to another exercise by its name.
"""

import os

# (short name = folder, full name = heading in the exercise list "exercises/Seznam úloh.md", [(name, origin)])
CATEGORIES = [
    ('Základní modely', 'Základní modely (přednášky)', [
        ('Opravářská dílna', 'přednáška, slajdy 157–164'),
        ('Samoobsluha', 'přednáška, slajdy 195–198'),
        ('Zdravotní ordinace', 'poznámky MSI (stochastické PN)'),
        ('Výrobní systém', 'poznámky MSI (P/T sítě)'),
        ('Kritická sekce', 'poznámky MSI (P/T sítě)'),
        ('Kravín', 'příklad z přednášky (studentská tabule)'),
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


# Exercises to start with: every pattern of the notation cheat sheet at least once, then the
# newest midterm word problems. (name, what it practises)
START = [
    ("Opravářská dílna", "generátor, zařízení, pravděpodobnostní větvení, odchod ze systému"),
    ("Samoobsluha", "sklad (vozíky), několik zařízení za sebou, výběr pokladny"),
    ("Netrpělivé požadavky", "netrpělivost (timeout ve frontě)"),
    ("Porucha s opravou, návrat do fronty", "přerušení obsluhy poruchou"),
    ("Údržba po každé 10. obsluze", "čítač: každá N-tá transakce"),
    ("Přerušení příchodů při plné frontě", "test délky fronty, dočasné zastavení příchodů"),
    ("Kopírovací centrum", "půlsemestrálka 2022/23: větvení, netrpělivost; s Hrubého řešením"),
    ("Klientské centrum", "půlsemestrálka 2023/24: zastavení příchodů podle délky fronty"),
    ("Centrum MM1 s rychlým režimem", "půlsemestrálka 2024/25: přepínání režimu podle fronty"),
    ("Pizza stánek", "půlsemestrálka 2024/25: dva zdroje, priorita"),
    ("Zahradnictví a bouřka", "půlsemestrálka 2024/25: proces, který přerušuje jiný proces"),
    ("Vyhlídkové lety", "půlsemestrálka 2024/25: dávka s odjezdem po čase"),
    ("Úřad", "půlsemestrálka 2025/26: dočasné posílení kapacity"),
    ("Obslužné centrum", "půlsemestrálka 2025/26: if–else přes prioritu, den a noc"),
    ("Psí salon", "půlsemestrálka 2025/26: vyprázdnění fronty, zastavení příchodů"),
]


# Study plan "exercises/Studijní plán.md": every exercise once, in the order to learn them.
# (heading, intro, [(name, what it practises)]); the first phase is START.
PLAN = [
    ("Začni tady", "Každý vzor z [Notace a vzory](<../basics/Notace a vzory.md>) aspoň jednou, pak nejnovější "
     "půlsemestrálky. Stejný seznam je v [Seznamu úloh](<Seznam úloh.md#začni-tady>).", START),
    ("Nové mechanismy", "Krátké zkouškové otázky s triky, které vzory přímo neukazují. Nejdřív doba obsluhy "
     "podle stavu a priority, pak varianty poruch, kapacity a nečinnosti.", [
        ("MD1 – střídání 2 a 3", "doba obsluhy podle stavu: dva stavy volné linky"),
        ("MD3 – poslední volné zařízení", "doba obsluhy podle počtu volných linek"),
        ("MD1 – podle doby od poslední obsluhy", "měření nečinnosti od konce obsluhy"),
        ("Dva proudy příchodů", "dva generátory, priorita obsluhy"),
        ("Priorita procesu a obsluhy", "rozdíl mezi prioritou procesu a prioritou obsluhy"),
        ("Každá 10. s prioritou obsluhy", "čítač a priorita obsluhy"),
        ("Kritická havárie", "odstávka linky na pevnou dobu, zrušení rozpracované obsluhy"),
        ("Porucha prodlouží probíhající obsluhu o 5", "porucha obsluhu prodlouží, místo aby ji zrušila"),
        ("Přerušení příliš dlouhé obsluhy", "timeout na obsluze, ne ve frontě"),
        ("Pomocník přidá kapacitu", "dočasná jednotka kapacity navíc"),
        ("Údržba zabere celou kapacitu", "zabrání celé kapacity skladu po jednotkách"),
        ("Každá 100. transakce vyprázdní frontu", "čítač a vyprázdnění fronty"),
        ("Spánek po nečinnosti", "odpočet nečinnosti, probuzení příchodem"),
        ("MM3 bez fronty s opakováním", "odmítnutí a návrat do systému po čase"),
    ]),
    ("Půlsemestrálky 2021/22–2025/26", "Zbylé nové půlsemestrálky, od nejnovější. Řeš je celé na čas a "
     "nápovědu otevři až po nakreslení celé sítě.", [
        ("Výletní autobus", "2025/26: dávka, autobus odjede plný nebo po 20 minutách"),
        ("Automat na kávu", "2023/24: porucha 5–6 h po opravě zasáhne probíhající nebo další obsluhu"),
        ("Server s údržbou po 1000 požadavcích", "2023/24: čítač spustí údržbu"),
        ("Výpočetní služba se spánkem", "2023/24: spánek po nečinnosti, probuzení příchodem"),
        ("Cestovní kancelář", "2022/23: test délky fronty, dvě přepážky navíc na hodinu"),
        ("Trafika", "2022/23: prodavač ve dvou rolích, odchod do skladu po nečinnosti"),
        ("Pizzerie s rozvozem", "2022/23: rozvoz všech hotových objednávek najednou"),
        ("Kopírovací centrum s poruchami", "2021/22: obsluha s kapacitou 10, poruchy"),
        ("Sběrači jahod", "2021/22: sběrači v cyklu, siréna podle délky fronty"),
        ("Výletní loď", "2021/22: čítač nastoupených, odplutí s 20 turisty"),
        ("Překladiště kontejnerů", "2021/22: auto se 3 kontejnery, vlak odjede plný"),
    ]),
    ("Značení v čase t", "Jiná dovednost: síť nekreslíš, ale ručně ji simuluješ (kalendář, fronta, značení). "
     "Nejdřív D/D/1, pak FIFO, nakonec LIFO.", [
        ("DD1 – příchody 3, obsluha 2", "stabilní D/D/1, tabulka stavů"),
        ("DD1 – příchody 2, obsluha 4", "nestabilní D/D/1, fronta roste"),
        ("DD2 FIFO, čas 6,5", "dvě linky, FIFO"),
        ("DD3 FIFO, čas 9,5", "tři linky, FIFO"),
        ("DD2 LIFO obsluha 4, čas 9,5", "LIFO"),
        ("DD2 LIFO obsluha 5, čas 9,5", "LIFO, delší obsluha"),
        ("DD2 LIFO obsluha 6, čas 13,5", "LIFO, události v čase t1"),
        ("DD3 LIFO, čas 10,5", "tři linky, LIFO"),
        ("DD4 LIFO, čas 9,5", "čtyři linky, LIFO"),
    ]),
    ("Další varianty mechanismů", "Opakování ke zkoušce: další varianty už známých mechanismů a zbylé "
     "modely z přednášek.", [
        ("Netrpělivý první ve frontě", "netrpělivý je jen první ve frontě"),
        ("Fronta omezená na 10", "omezená fronta, if–else přes prioritu"),
        ("Příklad s netrpělivou transakcí", "vlastní příklad netrpělivosti"),
        ("Porucha zruší obsluhu", "porucha jen zruší obsluhu"),
        ("Porucha vrací transakci do fronty", "přerušená transakce se vrací do fronty"),
        ("Porucha s opravou, transakce odchází", "oprava, přerušená transakce odchází"),
        ("Porucha zničí obsluhu nebo počká", "porucha počká na další obsluhu"),
        ("Každá 10. transakce vyvolá poruchu", "čítač spustí poruchu"),
        ("Porucha prodlouží další obsluhu", "porucha prodlouží až příští obsluhu"),
        ("Porucha prodlouží obsluhu o 2", "prodloužení probíhající obsluhy"),
        ("Automat na kávu – údržba po nečinnosti", "údržba po nečinnosti"),
        ("Automat na kávu – údržba po 50 obsluhách", "čítač spustí údržbu"),
        ("Automat na kávu – uspání", "uspání po nečinnosti, delší obsluha po probuzení"),
        ("Údržba při prázdné frontě", "test prázdné fronty po obsluze"),
        ("Údržba po dlouhé obsluze", "odpočet během obsluhy rozhodne o údržbě"),
        ("Údržbář na obchůzce", "čítač obsluh, údržbář jako proces"),
        ("Doba obsluhy podle délky fronty", "test délky fronty určí dobu obsluhy"),
        ("Dočasně MM2 při dlouhé frontě", "dočasná druhá linka"),
        ("Natrvalo MM3 při dlouhé frontě", "trvalé přidání linek"),
        ("Interval příchodů podle délky fronty", "generátor se dvěma intervaly"),
        ("MM3 – zastavení příchodů", "zastavení příchodů podle obsazených linek"),
        ("Sklad s dočasně větší kapacitou", "pravidelné rozšíření kapacity skladu"),
        ("MD1 – prodlužování po 10 obsluhách", "čítač mění dobu obsluhy"),
        ("Příklad s prioritou procesu", "vlastní příklad priority procesu"),
        ("Každá N-tá s prioritou procesu", "čítač a priorita procesu"),
        ("MM3 – prioritní zabírají 2 linky", "prioritní transakce zabírá dvě linky"),
        ("Zdravotní ordinace", "kartotéka, laboratoř, lékař, větvení"),
        ("Výrobní systém", "P/T síť, dvě vrtačky jako sklad"),
        ("Kritická sekce", "vzájemné vyloučení dvou procesů"),
        ("Kravín", "zdroje a dávky (konvice do auta)"),
    ]),
    ("Starší půlsemestrálky (2010–2019)", "Delší úlohy pro procvičení, po kategoriích. Ber je podle chuti; "
     "v každé kategorii jsou novější první.", [
        ("Pošta", "řidič se třemi stavy, otevření druhé přepážky"),
        ("Letiště", "priorita přistání, timeout, havárie dráhy"),
        ("Pekárna", "pekař ve dvou rolích, zásoba chleba"),
        ("Úřad s dodatečnými přepážkami", "pracovní doba, přepážky navíc podle fronty"),
        ("Menza", "karanténa: vyprázdnění systému, zastavení příchodů"),
        ("Hudební rádio", "reklama každou hodinu, přerušený rozhovor"),
        ("Nemocniční ambulance", "lékaři odjíždějí se sanitou k zásahu"),
        ("Banka se třemi pracovníky", "vedoucí jako proces, auto s vysokou prioritou"),
        ("Pražírna kávy", "netrpělivý první ve frontě, prodavač mezi prodejnou a dílnou"),
        ("Banka a lupič", "přepadení zastaví příchody, policista"),
        ("Telefonní ústředna", "sklad s kapacitou 20, operátorka, priorita"),
        ("Databázový server", "proces S počítá obsluhy a aktivuje druhý proces"),
        ("Počítačový server", "procesor a síťová linka, úloha drží procesor"),
        ("Zvuková karta", "vyrovnávací paměť, přednost zvukového procesu"),
        ("Festivalový autobus", "autobus sváží po jednom, odpočet 40 minut"),
        ("Vyhlídková loď na molu", "netrpělivost, odplutí plné nebo po 3 minutách"),
        ("Přepravní firma", "rozvoz balíků, nezastižené balíky jedou zpět"),
        ("Překladiště s jeřábem", "pracovní doba, jeřábník na obchůzce"),
        ("Bagrista a nákladní auta", "tři auta v cyklu, úsek po metrech"),
        ("Výletní loď na jezeře", "provozní doba, odjezd plné lodi nebo po 2 minutách"),
        ("Přehrada s přístavišti", "dvě lodě mezi dvěma přístavišti, netrpělivost"),
        ("Pošta s doporučenými zásilkami", "nakládání do kapacity, vykládka po jedné"),
        ("Přehrada s vyhlídkovou lodí", "odjezd plné lodi nebo po 15 minutách"),
        ("Výrobní hala", "odstavení montovny podle fronty k lakovně"),
        ("Jahodová farma", "vaření z 5 bedýnek, prioritní balení"),
        ("Spalovna se třemi vozy", "tři vozy v cyklu, komora s kapacitou 5"),
        ("Moštárna", "lisy, moštaři a sběrači v cyklu"),
        ("Spalovna", "rychlosti jako časy, sklad odpadu"),
        ("Hasiči", "požár zaniká bez hašení, extrémní požár bere všechny vozy"),
        ("Přečerpávací elektrárna II", "voda jako značky, den a noc, havárie"),
        ("Zahradník na FIT", "konvice s vodou, zalévání po částech"),
        ("Přečerpávací elektrárna", "voda jako značky, den a noc, havárie"),
        ("Uhelný mlýn", "havárie, chladnutí a rozehřívání"),
        ("Stavba z betonu", "licí forma jako transakce, zrání betonu"),
        ("Výroba hrášku", "dávka 100 várek, trvanlivost, porucha balení"),
        ("Dílna se třemi stroji", "jeden pracovník pro dva stroje, oprava"),
        ("Tunel", "den a noc, dvě soupravy, tunel jako sklad metrů"),
        ("Chmelová brigáda", "sklad s omezenou kapacitou, procházka"),
        ("Logistická centrála", "dodávka se 100 balíky, pracovník jako proces"),
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


def note_id(f):
    """Number of the exercise in folder `f` (relative to exercises/): "<category>-<exercise>", e.g. "06-02"."""
    cat, ex = f.split("/")
    return f"{cat.split(' - ')[0]}-{ex.split(' - ')[0]}"


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
