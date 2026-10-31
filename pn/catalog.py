"""Catalogue of all exercises: id, Czech name, origin. Folder = "<id> - <name>".

Ids are TT–NN: topic number and position within the topic. Topics go from
basic models over single mechanisms (exam-style M/M/1 variants) to marking at
time t and full word problems (midterms). Within a topic, newer first.
"""

TOPICS = {
    "01": "Základní modely (přednášky)",
    "02": "Netrpělivost, omezená fronta, opakování",
    "03": "Poruchy a přerušení obsluhy",
    "04": "Údržba, nečinnost, spánek",
    "05": "Řízení podle délky fronty a kapacita",
    "06": "Doba obsluhy podle stavu",
    "07": "Priority",
    "08": "Značení v čase t (D/D/x)",
    "09": "Slovní úlohy: obsluha zákazníků",
    "10": "Slovní úlohy: počítačové systémy",
    "11": "Slovní úlohy: doprava a dávky",
    "12": "Slovní úlohy: výroba, zdroje a sklady",
}

# (id, name, origin)
EXERCISES = [
    ("01–01", "Opravářská dílna", "přednáška, slajdy 157–164"),
    ("01–02", "Samoobsluha", "přednáška, slajdy 195–198"),
    ("01–03", "Zdravotní středisko", "poznámky MSI (stochastické PN)"),
    ("01–04", "Výrobní systém", "poznámky MSI (P/T sítě)"),
    ("01–05", "Kritická sekce", "poznámky MSI (P/T sítě)"),
    ("01–06", "Kravín", "příklad z přednášky (tabule luppo)"),

    ("02–01", "Netrpělivé požadavky", "zkouška 2017/18 1. t. (8H, 7A); 2023/24 1. t. A"),
    ("02–02", "Netrpělivý první ve frontě", "zkouška 2017/18 2. t. A; 2019/20 2. t. Y; 2024/25 2. t. E"),
    ("02–03", "Příklad s netrpělivou transakcí", "zkouška 2019/20 1. opravný; 2020/21 3. t. C"),
    ("02–04", "Fronta omezená na 10", "zkouška 2017/18 1. t. 8C"),
    ("02–05", "MM3 bez fronty s opakováním", "zkouška 2023/24 1. t. B"),

    ("03–01", "Porucha zruší obsluhu", "zkouška 2017/18 1. t. Z"),
    ("03–02", "Porucha vrací transakci do fronty", "zkouška 2019/20 1. opravný, sk. B"),
    ("03–03", "Porucha s opravou, návrat do fronty", "zkouška 2024/25 1. t. A"),
    ("03–04", "Porucha s opravou, transakce odchází", "zkouška 2021/22 1. t. A"),
    ("03–05", "Kritická havárie", "zkouška 2025/26 1. t. C"),
    ("03–06", "Porucha zničí obsluhu nebo počká", "zkouška 2021/22 2. t."),
    ("03–07", "Každá 10. transakce vyvolá poruchu", "zkouška 2021/22 1. t. B"),
    ("03–08", "Porucha prodlouží další obsluhu", "zkouška 2017/18 3. t. A"),
    ("03–09", "Porucha prodlouží obsluhu o 2", "zkouška 2020/21 1. t."),
    ("03–10", "Porucha prodlouží probíhající obsluhu o 5", "zkouška 2020/21 náhradní termín"),
    ("03–11", "Přerušení příliš dlouhé obsluhy", "zkouška 2019/20 2. t. Z"),

    ("04–01", "Automat na kávu – údržba po nečinnosti", "zkouška 2017/18 2. t. B; 2018/19 1. t."),
    ("04–02", "Automat na kávu – údržba po 50 obsluhách", "zkouška 2017/18 2. t. C; 2018/19 1. t."),
    ("04–03", "Automat na kávu – uspání", "zkouška 2017/18 2. t. D"),
    ("04–04", "Údržba při prázdné frontě", "zkouška 2019/20 1. t. D; 2020/21 1. t."),
    ("04–05", "Údržba po dlouhé obsluze", "zkouška 2021/22 1. t. D"),
    ("04–06", "Údržba po každé 10. obsluze", "zkouška 2022/23 1. t. D"),
    ("04–07", "Údržbář na obchůzce", "zkouška 2022/23 1. t. C"),
    ("04–08", "Spánek po nečinnosti", "zkouška 2022/23 2. t. F"),

    ("05–01", "Doba obsluhy podle délky fronty", "zkouška 2019/20 1. t.; 2020/21 1. t."),
    ("05–02", "Dočasně MM2 při dlouhé frontě", "zkouška 2018/19 3. t."),
    ("05–03", "Natrvalo MM3 při dlouhé frontě", "zkouška 2020/21 1. t."),
    ("05–04", "Interval příchodů podle délky fronty", "zkouška 2021/22 1. t. C; 2022/23 1. t. A"),
    ("05–05", "Přerušení příchodů při plné frontě", "zkouška 2024/25 1. t. B"),
    ("05–06", "MM3 – zastavení příchodů", "zkouška 2024/25 1. t. C"),
    ("05–07", "Každá 100. transakce vyprázdní frontu", "zkouška 2022/23 2. t. E"),
    ("05–08", "Sklad s dočasně větší kapacitou", "zkouška 2017/18 3. t. Z"),
    ("05–09", "Údržba zabere celou kapacitu", "zkouška 2025/26 2. t. E"),
    ("05–10", "Pomocník přidá kapacitu", "zkouška 2025/26 2. t. F"),

    ("06–01", "MD1 – prodlužování po 10 obsluhách", "zkouška 2024/25 2. t. F"),
    ("06–02", "MD1 – střídání 2 a 3", "zkouška 2025/26 1. t. A"),
    ("06–03", "MD3 – poslední volné zařízení", "zkouška 2024/25 3. t. H"),
    ("06–04", "MD1 – podle doby od poslední obsluhy", "zkouška 2020/21 1. opravný"),

    ("07–01", "Příklad s prioritou procesu", "zkouška 2019/20 3. t. A"),
    ("07–02", "Každá N-tá s prioritou procesu", "zkouška 2022/23 3. t. G"),
    ("07–03", "Každá 10. s prioritou obsluhy", "zkouška 2022/23 3. t. H"),
    ("07–04", "Dva proudy příchodů", "zkouška 2025/26 1. t. B"),
    ("07–05", "Priorita procesu a obsluhy", "zkouška 2025/26 1. t. C (otázka 3)"),
    ("07–06", "MM3 – prioritní zabírají 2 linky", "zkouška 2018/19 (Řešené výpočetní příklady)"),

    ("08–01", "DD2 FIFO, čas 6,5", "zkouška 2012/13 2. t. C"),
    ("08–02", "DD3 LIFO, čas 10,5", "zkouška 2015/16 3. t. 5-A; 2014/15 1. t. C"),
    ("08–03", "DD2 LIFO obsluha 6, čas 13,5", "zkouška 2015/16 3. t. 5-D"),
    ("08–04", "DD2 LIFO obsluha 5, čas 9,5", "zkouška 2014/15 1. t. B; 2015/16 2. t."),
    ("08–05", "DD2 LIFO obsluha 4, čas 9,5", "zkouška 2015/16 2. t. A"),
    ("08–06", "DD4 LIFO, čas 9,5", "zkouška 2014/15 3. t. D"),
    ("08–07", "DD3 FIFO, čas 9,5", "zkouška 2015/16 1. t. 5H"),
    ("08–08", "DD1 – příchody 2, obsluha 4", "zkouška 2022/23 3. t. G"),
    ("08–09", "DD1 – příchody 3, obsluha 2", "zkouška 2022/23 3. t. H"),

    ("09–01", "Úřad", "půlsemestrálka 2025/26 D"),
    ("09–02", "Obslužné centrum", "půlsemestrálka 2025/26 B"),
    ("09–03", "Psí salon", "půlsemestrálka 2025/26 A"),
    ("09–04", "Centrum MM1 s rychlým režimem", "půlsemestrálka 2024/25 D"),
    ("09–05", "Pizza stánek", "půlsemestrálka 2024/25 B"),
    ("09–06", "Klientské centrum", "půlsemestrálka 2023/24 D"),
    ("09–07", "Automat na kávu", "půlsemestrálka 2023/24 C"),
    ("09–08", "Cestovní kancelář", "půlsemestrálka 2022/23 D"),
    ("09–09", "Trafika", "půlsemestrálka 2022/23 B"),
    ("09–10", "Kopírovací centrum", "půlsemestrálka 2022/23 A"),
    ("09–11", "Kopírovací centrum s poruchami", "půlsemestrálka 2021/22 D"),
    ("09–12", "Pošta", "půlsemestrálky 2014–19, Z19"),
    ("09–13", "Letiště", "půlsemestrálky 2014–19, Z17"),
    ("09–14", "Pekárna", "půlsemestrálky 2014–19, Z14"),
    ("09–15", "Úřad s dodatečnými přepážkami", "půlsemestrálky 2014–19, Z10"),
    ("09–16", "Menza", "půlsemestrálky 2014–19, Z9"),
    ("09–17", "Hudební rádio", "půlsemestrálky 2014–19, Z7"),
    ("09–18", "Nemocniční ambulance", "půlsemestrálky 2014–19, Z6"),
    ("09–19", "Banka se třemi pracovníky", "půlsemestrálka 2013/14 A"),
    ("09–20", "Pražírna kávy", "půlsemestrálka 2010/11"),
    ("09–21", "Banka a lupič", "půlsemestrálka 2010/11"),
    ("09–22", "Telefonní ústředna", "půlsemestrálka (rok neznámý, Studentská skripta 2015/16)"),

    ("10–01", "Server s údržbou po 1000 požadavcích", "půlsemestrálka 2023/24 A"),
    ("10–02", "Výpočetní služba se spánkem", "půlsemestrálka 2023/24 B"),
    ("10–03", "Databázový server", "půlsemestrálky 2014–19, Z22"),
    ("10–04", "Počítačový server", "půlsemestrálka 2013/14 C"),
    ("10–05", "Zvuková karta", "půlsemestrálka (rok neznámý, Příprava 2021/22)"),

    ("11–01", "Výletní autobus", "půlsemestrálka 2025/26 C"),
    ("11–02", "Vyhlídkové lety", "půlsemestrálka 2024/25 C"),
    ("11–03", "Pizzerie s rozvozem", "půlsemestrálka 2022/23 C"),
    ("11–04", "Výletní loď", "půlsemestrálka 2021/22 C"),
    ("11–05", "Překladiště kontejnerů", "půlsemestrálka 2021/22 A"),
    ("11–06", "Festivalový autobus", "půlsemestrálky 2014–19, Z21"),
    ("11–07", "Vyhlídková loď na molu", "půlsemestrálky 2014–19, Z18"),
    ("11–08", "Přepravní firma", "půlsemestrálky 2014–19, Z12"),
    ("11–09", "Překladiště s jeřábem", "půlsemestrálky 2014–19, Z5"),
    ("11–10", "Bagrista a nákladní auta", "půlsemestrálky 2014–19, Z4"),
    ("11–11", "Výletní loď na jezeře", "půlsemestrálky 2014–19, Z1"),
    ("11–12", "Přehrada s přístavišti", "půlsemestrálka 2011/12"),
    ("11–13", "Pošta s doporučenými zásilkami", "půlsemestrálka 2011/12"),
    ("11–14", "Přehrada s vyhlídkovou lodí", "půlsemestrálka (rok neznámý, Příprava 2021/22)"),

    ("12–01", "Zahradnictví a bouřka", "půlsemestrálka 2024/25 A"),
    ("12–02", "Sběrači jahod", "půlsemestrálka 2021/22 B"),
    ("12–03", "Výrobní hala", "půlsemestrálky 2014–19, Z24"),
    ("12–04", "Jahodová farma", "půlsemestrálky 2014–19, Z23"),
    ("12–05", "Spalovna se třemi vozy", "půlsemestrálky 2014–19, Z20"),
    ("12–06", "Moštárna", "půlsemestrálky 2014–19, Z16"),
    ("12–07", "Spalovna", "půlsemestrálky 2014–19, Z15"),
    ("12–08", "Hasiči", "půlsemestrálky 2014–19, Z13"),
    ("12–09", "Přečerpávací elektrárna II", "půlsemestrálky 2014–19, Z11"),
    ("12–10", "Zahradník na FIT", "půlsemestrálky 2014–19, Z8"),
    ("12–11", "Přečerpávací elektrárna", "půlsemestrálky 2014–19, Z3"),
    ("12–12", "Uhelný mlýn", "půlsemestrálky 2014–19, Z2"),
    ("12–13", "Stavba z betonu", "půlsemestrálka 2013/14 D"),
    ("12–14", "Výroba hrášku", "půlsemestrálka 2013/14 B"),
    ("12–15", "Dílna se třemi stroji", "půlsemestrálka 2011/12"),
    ("12–16", "Tunel", "půlsemestrálka 2011/12"),
    ("12–17", "Chmelová brigáda", "půlsemestrálka 2010/11"),
    ("12–18", "Logistická centrála", "půlsemestrálka 2010/11"),
]


def folder(ex_id):
    for i, name, _ in EXERCISES:
        if i == ex_id:
            return f"{i} - {name}"
    raise KeyError(ex_id)


def link(ex_id, from_exercise=True):
    """Markdown link to another exercise's note, relative to a note."""
    f = folder(ex_id)
    prefix = "../" if from_exercise else "exercises/"
    return f"[{ex_id} – {f.split(' - ', 1)[1]}](<{prefix}{f}/{f}.md>)"
