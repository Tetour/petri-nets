# Seznam úloh

<!-- Generuje `make index` (python3 -m pn.index) z pn/catalog.py; needitovat ručně. -->

Všechny úlohy na Petriho sítě ze studijních materiálů IMS, rozdělené do kategorií: nejdřív základní modely, pak jednotlivé mechanismy jako v krátkých zkouškových otázkách, pak značení v čase t a nakonec celé slovní úlohy jako na půlsemestrálce. V každé kategorii jsou novější úlohy první. Sloupec *Původ* říká, odkud úloha pochází; podrobnosti jsou v poslední části poznámky.

Doporučené pořadí všech úloh je ve [Studijním plánu](<Studijní plán.md>).

Po otevření poznámky je vidět jen zadání. Nejdřív se úlohu pokus vyřešit bez nápovědy, pak otevírej skryté části jednu po druhé: nápovědu, Petriho síť, časté chyby, model v SIMLIB a zdroje. Každá poznámka je vedle i jako PDF.

Celkem 118 úloh.

| Č. | Kategorie | Úloh |
|---|---|---|
| 01 | [Základní modely (přednášky)](<01 - Základní modely/>) | 6 |
| 02 | [Netrpělivost, omezená fronta, opakování](<02 - Netrpělivost a omezená fronta/>) | 5 |
| 03 | [Poruchy a přerušení obsluhy](<03 - Poruchy/>) | 11 |
| 04 | [Údržba, nečinnost, spánek](<04 - Údržba a spánek/>) | 8 |
| 05 | [Řízení podle délky fronty a kapacita](<05 - Délka fronty a kapacita/>) | 10 |
| 06 | [Doba obsluhy podle stavu](<06 - Doba obsluhy podle stavu/>) | 4 |
| 07 | [Priority](<07 - Priority/>) | 6 |
| 08 | [Značení v čase t (D/D/x)](<08 - Značení v čase t/>) | 9 |
| 09 | [Slovní úlohy: obsluha zákazníků](<09 - Obsluha zákazníků/>) | 22 |
| 10 | [Slovní úlohy: počítačové systémy](<10 - Počítačové systémy/>) | 5 |
| 11 | [Slovní úlohy: doprava a dávky](<11 - Doprava a dávky/>) | 14 |
| 12 | [Slovní úlohy: výroba, zdroje a sklady](<12 - Výroba a sklady/>) | 18 |

## Začni tady

Patnáct úloh na začátek: nejdřív každý vzor z [Notace a vzory](<../basics/Notace a vzory.md>) aspoň jednou, pak nejnovější půlsemestrálky.

1. [Opravářská dílna](<01 - Základní modely/01 - Opravářská dílna/01 - Opravářská dílna.md>): generátor, zařízení, pravděpodobnostní větvení, odchod ze systému
2. [Samoobsluha](<01 - Základní modely/02 - Samoobsluha/02 - Samoobsluha.md>): sklad (vozíky), několik zařízení za sebou, výběr pokladny
3. [Netrpělivé požadavky](<02 - Netrpělivost a omezená fronta/01 - Netrpělivé požadavky/01 - Netrpělivé požadavky.md>): netrpělivost (timeout ve frontě)
4. [Porucha s opravou, návrat do fronty](<03 - Poruchy/03 - Porucha s opravou, návrat do fronty/03 - Porucha s opravou, návrat do fronty.md>): přerušení obsluhy poruchou
5. [Údržba po každé 10. obsluze](<04 - Údržba a spánek/06 - Údržba po každé 10. obsluze/06 - Údržba po každé 10. obsluze.md>): čítač: každá N-tá transakce
6. [Přerušení příchodů při plné frontě](<05 - Délka fronty a kapacita/05 - Přerušení příchodů při plné frontě/05 - Přerušení příchodů při plné frontě.md>): test délky fronty, dočasné zastavení příchodů
7. [Kopírovací centrum](<09 - Obsluha zákazníků/10 - Kopírovací centrum/10 - Kopírovací centrum.md>): půlsemestrálka 2022/23: větvení, netrpělivost; s Hrubého řešením
8. [Klientské centrum](<09 - Obsluha zákazníků/06 - Klientské centrum/06 - Klientské centrum.md>): půlsemestrálka 2023/24: zastavení příchodů podle délky fronty
9. [Centrum MM1 s rychlým režimem](<09 - Obsluha zákazníků/04 - Centrum MM1 s rychlým režimem/04 - Centrum MM1 s rychlým režimem.md>): půlsemestrálka 2024/25: přepínání režimu podle fronty
10. [Pizza stánek](<09 - Obsluha zákazníků/05 - Pizza stánek/05 - Pizza stánek.md>): půlsemestrálka 2024/25: dva zdroje, priorita
11. [Zahradnictví a bouřka](<12 - Výroba a sklady/01 - Zahradnictví a bouřka/01 - Zahradnictví a bouřka.md>): půlsemestrálka 2024/25: proces, který přerušuje jiný proces
12. [Vyhlídkové lety](<11 - Doprava a dávky/02 - Vyhlídkové lety/02 - Vyhlídkové lety.md>): půlsemestrálka 2024/25: dávka s odjezdem po čase
13. [Úřad](<09 - Obsluha zákazníků/01 - Úřad/01 - Úřad.md>): půlsemestrálka 2025/26: dočasné posílení kapacity
14. [Obslužné centrum](<09 - Obsluha zákazníků/02 - Obslužné centrum/02 - Obslužné centrum.md>): půlsemestrálka 2025/26: if–else přes prioritu, den a noc
15. [Psí salon](<09 - Obsluha zákazníků/03 - Psí salon/03 - Psí salon.md>): půlsemestrálka 2025/26: vyprázdnění fronty, zastavení příchodů

## 01 Základní modely (přednášky)

| Č. | Úloha | Původ |
|---|---|---|
| 01 | [Opravářská dílna](<01 - Základní modely/01 - Opravářská dílna/01 - Opravářská dílna.md>) | přednáška, slajdy 157–164 |
| 02 | [Samoobsluha](<01 - Základní modely/02 - Samoobsluha/02 - Samoobsluha.md>) | přednáška, slajdy 195–198 |
| 03 | [Zdravotní ordinace](<01 - Základní modely/03 - Zdravotní ordinace/03 - Zdravotní ordinace.md>) | poznámky MSI (stochastické PN) |
| 04 | [Výrobní systém](<01 - Základní modely/04 - Výrobní systém/04 - Výrobní systém.md>) | poznámky MSI (P/T sítě) |
| 05 | [Kritická sekce](<01 - Základní modely/05 - Kritická sekce/05 - Kritická sekce.md>) | poznámky MSI (P/T sítě) |
| 06 | [Kravín](<01 - Základní modely/06 - Kravín/06 - Kravín.md>) | příklad z přednášky (studentská tabule) |

## 02 Netrpělivost, omezená fronta, opakování

| Č. | Úloha | Původ |
|---|---|---|
| 01 | [Netrpělivé požadavky](<02 - Netrpělivost a omezená fronta/01 - Netrpělivé požadavky/01 - Netrpělivé požadavky.md>) | zkouška 2017/18 1. t. (8H, 7A); 2023/24 1. t. A |
| 02 | [Netrpělivý první ve frontě](<02 - Netrpělivost a omezená fronta/02 - Netrpělivý první ve frontě/02 - Netrpělivý první ve frontě.md>) | zkouška 2017/18 2. t. A; 2019/20 2. t. Y; 2024/25 2. t. E |
| 03 | [Příklad s netrpělivou transakcí](<02 - Netrpělivost a omezená fronta/03 - Příklad s netrpělivou transakcí/03 - Příklad s netrpělivou transakcí.md>) | zkouška 2019/20 1. opravný; 2020/21 3. t. C |
| 04 | [Fronta omezená na 10](<02 - Netrpělivost a omezená fronta/04 - Fronta omezená na 10/04 - Fronta omezená na 10.md>) | zkouška 2017/18 1. t. 8C |
| 05 | [MM3 bez fronty s opakováním](<02 - Netrpělivost a omezená fronta/05 - MM3 bez fronty s opakováním/05 - MM3 bez fronty s opakováním.md>) | zkouška 2023/24 1. t. B |

## 03 Poruchy a přerušení obsluhy

| Č. | Úloha | Původ |
|---|---|---|
| 01 | [Porucha zruší obsluhu](<03 - Poruchy/01 - Porucha zruší obsluhu/01 - Porucha zruší obsluhu.md>) | zkouška 2017/18 1. t. Z |
| 02 | [Porucha vrací transakci do fronty](<03 - Poruchy/02 - Porucha vrací transakci do fronty/02 - Porucha vrací transakci do fronty.md>) | zkouška 2019/20 1. opravný, sk. B |
| 03 | [Porucha s opravou, návrat do fronty](<03 - Poruchy/03 - Porucha s opravou, návrat do fronty/03 - Porucha s opravou, návrat do fronty.md>) | zkouška 2024/25 1. t. A |
| 04 | [Porucha s opravou, transakce odchází](<03 - Poruchy/04 - Porucha s opravou, transakce odchází/04 - Porucha s opravou, transakce odchází.md>) | zkouška 2021/22 1. t. A |
| 05 | [Kritická havárie](<03 - Poruchy/05 - Kritická havárie/05 - Kritická havárie.md>) | zkouška 2025/26 1. t. C |
| 06 | [Porucha zničí obsluhu nebo počká](<03 - Poruchy/06 - Porucha zničí obsluhu nebo počká/06 - Porucha zničí obsluhu nebo počká.md>) | zkouška 2021/22 2. t. |
| 07 | [Každá 10. transakce vyvolá poruchu](<03 - Poruchy/07 - Každá 10. transakce vyvolá poruchu/07 - Každá 10. transakce vyvolá poruchu.md>) | zkouška 2021/22 1. t. B |
| 08 | [Porucha prodlouží další obsluhu](<03 - Poruchy/08 - Porucha prodlouží další obsluhu/08 - Porucha prodlouží další obsluhu.md>) | zkouška 2017/18 3. t. A |
| 09 | [Porucha prodlouží obsluhu o 2](<03 - Poruchy/09 - Porucha prodlouží obsluhu o 2/09 - Porucha prodlouží obsluhu o 2.md>) | zkouška 2020/21 1. opravný (11:00) |
| 10 | [Porucha prodlouží probíhající obsluhu o 5](<03 - Poruchy/10 - Porucha prodlouží probíhající obsluhu o 5/10 - Porucha prodlouží probíhající obsluhu o 5.md>) | zkouška 2020/21 náhradní termín |
| 11 | [Přerušení příliš dlouhé obsluhy](<03 - Poruchy/11 - Přerušení příliš dlouhé obsluhy/11 - Přerušení příliš dlouhé obsluhy.md>) | zkouška 2019/20 2. t. Z |

## 04 Údržba, nečinnost, spánek

| Č. | Úloha | Původ |
|---|---|---|
| 01 | [Automat na kávu – údržba po nečinnosti](<04 - Údržba a spánek/01 - Automat na kávu – údržba po nečinnosti/01 - Automat na kávu – údržba po nečinnosti.md>) | zkouška 2017/18 2. t. B; 2018/19 1. t. |
| 02 | [Automat na kávu – údržba po 50 obsluhách](<04 - Údržba a spánek/02 - Automat na kávu – údržba po 50 obsluhách/02 - Automat na kávu – údržba po 50 obsluhách.md>) | zkouška 2017/18 2. t. C; 2018/19 1. t. |
| 03 | [Automat na kávu – uspání](<04 - Údržba a spánek/03 - Automat na kávu – uspání/03 - Automat na kávu – uspání.md>) | zkouška 2017/18 2. t. D |
| 04 | [Údržba při prázdné frontě](<04 - Údržba a spánek/04 - Údržba při prázdné frontě/04 - Údržba při prázdné frontě.md>) | zkouška 2019/20 1. t. D; 2020/21 1. t. |
| 05 | [Údržba po dlouhé obsluze](<04 - Údržba a spánek/05 - Údržba po dlouhé obsluze/05 - Údržba po dlouhé obsluze.md>) | zkouška 2021/22 1. t. D |
| 06 | [Údržba po každé 10. obsluze](<04 - Údržba a spánek/06 - Údržba po každé 10. obsluze/06 - Údržba po každé 10. obsluze.md>) | zkouška 2022/23 1. t. D |
| 07 | [Údržbář na obchůzce](<04 - Údržba a spánek/07 - Údržbář na obchůzce/07 - Údržbář na obchůzce.md>) | zkouška 2022/23 1. t. C |
| 08 | [Spánek po nečinnosti](<04 - Údržba a spánek/08 - Spánek po nečinnosti/08 - Spánek po nečinnosti.md>) | zkouška 2022/23 2. t. F |

## 05 Řízení podle délky fronty a kapacita

| Č. | Úloha | Původ |
|---|---|---|
| 01 | [Doba obsluhy podle délky fronty](<05 - Délka fronty a kapacita/01 - Doba obsluhy podle délky fronty/01 - Doba obsluhy podle délky fronty.md>) | zkouška 2019/20 1. t.; 2020/21 1. t. |
| 02 | [Dočasně MM2 při dlouhé frontě](<05 - Délka fronty a kapacita/02 - Dočasně MM2 při dlouhé frontě/02 - Dočasně MM2 při dlouhé frontě.md>) | zkouška 2018/19 3. t. |
| 03 | [Natrvalo MM3 při dlouhé frontě](<05 - Délka fronty a kapacita/03 - Natrvalo MM3 při dlouhé frontě/03 - Natrvalo MM3 při dlouhé frontě.md>) | zkouška 2020/21 1. t. |
| 04 | [Interval příchodů podle délky fronty](<05 - Délka fronty a kapacita/04 - Interval příchodů podle délky fronty/04 - Interval příchodů podle délky fronty.md>) | zkouška 2021/22 1. t. C; 2022/23 1. t. A |
| 05 | [Přerušení příchodů při plné frontě](<05 - Délka fronty a kapacita/05 - Přerušení příchodů při plné frontě/05 - Přerušení příchodů při plné frontě.md>) | zkouška 2024/25 1. t. B |
| 06 | [MM3 – zastavení příchodů](<05 - Délka fronty a kapacita/06 - MM3 – zastavení příchodů/06 - MM3 – zastavení příchodů.md>) | zkouška 2024/25 1. t. C |
| 07 | [Každá 100. transakce vyprázdní frontu](<05 - Délka fronty a kapacita/07 - Každá 100. transakce vyprázdní frontu/07 - Každá 100. transakce vyprázdní frontu.md>) | zkouška 2022/23 2. t. E |
| 08 | [Sklad s dočasně větší kapacitou](<05 - Délka fronty a kapacita/08 - Sklad s dočasně větší kapacitou/08 - Sklad s dočasně větší kapacitou.md>) | zkouška 2017/18 3. t. Z |
| 09 | [Údržba zabere celou kapacitu](<05 - Délka fronty a kapacita/09 - Údržba zabere celou kapacitu/09 - Údržba zabere celou kapacitu.md>) | zkouška 2025/26 2. t. E |
| 10 | [Pomocník přidá kapacitu](<05 - Délka fronty a kapacita/10 - Pomocník přidá kapacitu/10 - Pomocník přidá kapacitu.md>) | zkouška 2025/26 2. t. F |

## 06 Doba obsluhy podle stavu

| Č. | Úloha | Původ |
|---|---|---|
| 01 | [MD1 – prodlužování po 10 obsluhách](<06 - Doba obsluhy podle stavu/01 - MD1 – prodlužování po 10 obsluhách/01 - MD1 – prodlužování po 10 obsluhách.md>) | zkouška 2024/25 2. t. F |
| 02 | [MD1 – střídání 2 a 3](<06 - Doba obsluhy podle stavu/02 - MD1 – střídání 2 a 3/02 - MD1 – střídání 2 a 3.md>) | zkouška 2025/26 1. t. A |
| 03 | [MD3 – poslední volné zařízení](<06 - Doba obsluhy podle stavu/03 - MD3 – poslední volné zařízení/03 - MD3 – poslední volné zařízení.md>) | zkouška 2024/25 3. t. H |
| 04 | [MD1 – podle doby od poslední obsluhy](<06 - Doba obsluhy podle stavu/04 - MD1 – podle doby od poslední obsluhy/04 - MD1 – podle doby od poslední obsluhy.md>) | zkouška 2020/21 1. opravný |

## 07 Priority

| Č. | Úloha | Původ |
|---|---|---|
| 01 | [Příklad s prioritou procesu](<07 - Priority/01 - Příklad s prioritou procesu/01 - Příklad s prioritou procesu.md>) | zkouška 2019/20 3. t. A |
| 02 | [Každá N-tá s prioritou procesu](<07 - Priority/02 - Každá N-tá s prioritou procesu/02 - Každá N-tá s prioritou procesu.md>) | zkouška 2022/23 3. t. G |
| 03 | [Každá 10. s prioritou obsluhy](<07 - Priority/03 - Každá 10. s prioritou obsluhy/03 - Každá 10. s prioritou obsluhy.md>) | zkouška 2022/23 3. t. H |
| 04 | [Dva proudy příchodů](<07 - Priority/04 - Dva proudy příchodů/04 - Dva proudy příchodů.md>) | zkouška 2025/26 1. t. B |
| 05 | [Priorita procesu a obsluhy](<07 - Priority/05 - Priorita procesu a obsluhy/05 - Priorita procesu a obsluhy.md>) | zkouška 2025/26 1. t. C (otázka 3) |
| 06 | [MM3 – prioritní zabírají 2 linky](<07 - Priority/06 - MM3 – prioritní zabírají 2 linky/06 - MM3 – prioritní zabírají 2 linky.md>) | zkouška 2018/19 (Řešené výpočetní příklady) |

## 08 Značení v čase t (D/D/x)

| Č. | Úloha | Původ |
|---|---|---|
| 01 | [DD2 FIFO, čas 6,5](<08 - Značení v čase t/01 - DD2 FIFO, čas 6,5/01 - DD2 FIFO, čas 6,5.md>) | zkouška 2012/13 2. t. C |
| 02 | [DD3 LIFO, čas 10,5](<08 - Značení v čase t/02 - DD3 LIFO, čas 10,5/02 - DD3 LIFO, čas 10,5.md>) | zkouška 2015/16 3. t. 5-A; 2014/15 1. t. C |
| 03 | [DD2 LIFO obsluha 6, čas 13,5](<08 - Značení v čase t/03 - DD2 LIFO obsluha 6, čas 13,5/03 - DD2 LIFO obsluha 6, čas 13,5.md>) | zkouška 2015/16 3. t. 5-D |
| 04 | [DD2 LIFO obsluha 5, čas 9,5](<08 - Značení v čase t/04 - DD2 LIFO obsluha 5, čas 9,5/04 - DD2 LIFO obsluha 5, čas 9,5.md>) | zkouška 2014/15 1. t. B; 2015/16 2. t. |
| 05 | [DD2 LIFO obsluha 4, čas 9,5](<08 - Značení v čase t/05 - DD2 LIFO obsluha 4, čas 9,5/05 - DD2 LIFO obsluha 4, čas 9,5.md>) | zkouška 2015/16 2. t. A |
| 06 | [DD4 LIFO, čas 9,5](<08 - Značení v čase t/06 - DD4 LIFO, čas 9,5/06 - DD4 LIFO, čas 9,5.md>) | zkouška 2014/15 3. t. D |
| 07 | [DD3 FIFO, čas 9,5](<08 - Značení v čase t/07 - DD3 FIFO, čas 9,5/07 - DD3 FIFO, čas 9,5.md>) | zkouška 2015/16 1. t. 5H |
| 08 | [DD1 – příchody 2, obsluha 4](<08 - Značení v čase t/08 - DD1 – příchody 2, obsluha 4/08 - DD1 – příchody 2, obsluha 4.md>) | zkouška 2022/23 3. t. G |
| 09 | [DD1 – příchody 3, obsluha 2](<08 - Značení v čase t/09 - DD1 – příchody 3, obsluha 2/09 - DD1 – příchody 3, obsluha 2.md>) | zkouška 2022/23 3. t. H |

## 09 Slovní úlohy: obsluha zákazníků

| Č. | Úloha | Původ |
|---|---|---|
| 01 | [Úřad](<09 - Obsluha zákazníků/01 - Úřad/01 - Úřad.md>) | půlsemestrálka 2025/26 D |
| 02 | [Obslužné centrum](<09 - Obsluha zákazníků/02 - Obslužné centrum/02 - Obslužné centrum.md>) | půlsemestrálka 2025/26 B |
| 03 | [Psí salon](<09 - Obsluha zákazníků/03 - Psí salon/03 - Psí salon.md>) | půlsemestrálka 2025/26 A |
| 04 | [Centrum MM1 s rychlým režimem](<09 - Obsluha zákazníků/04 - Centrum MM1 s rychlým režimem/04 - Centrum MM1 s rychlým režimem.md>) | půlsemestrálka 2024/25 D |
| 05 | [Pizza stánek](<09 - Obsluha zákazníků/05 - Pizza stánek/05 - Pizza stánek.md>) | půlsemestrálka 2024/25 B |
| 06 | [Klientské centrum](<09 - Obsluha zákazníků/06 - Klientské centrum/06 - Klientské centrum.md>) | půlsemestrálka 2023/24 D |
| 07 | [Automat na kávu](<09 - Obsluha zákazníků/07 - Automat na kávu/07 - Automat na kávu.md>) | půlsemestrálka 2023/24 C |
| 08 | [Cestovní kancelář](<09 - Obsluha zákazníků/08 - Cestovní kancelář/08 - Cestovní kancelář.md>) | půlsemestrálka 2022/23 D |
| 09 | [Trafika](<09 - Obsluha zákazníků/09 - Trafika/09 - Trafika.md>) | půlsemestrálka 2022/23 B |
| 10 | [Kopírovací centrum](<09 - Obsluha zákazníků/10 - Kopírovací centrum/10 - Kopírovací centrum.md>) | půlsemestrálka 2022/23 A |
| 11 | [Kopírovací centrum s poruchami](<09 - Obsluha zákazníků/11 - Kopírovací centrum s poruchami/11 - Kopírovací centrum s poruchami.md>) | půlsemestrálka 2021/22 D |
| 12 | [Pošta](<09 - Obsluha zákazníků/12 - Pošta/12 - Pošta.md>) | půlsemestrálky 2014–19, Z19 |
| 13 | [Letiště](<09 - Obsluha zákazníků/13 - Letiště/13 - Letiště.md>) | půlsemestrálky 2014–19, Z17 |
| 14 | [Pekárna](<09 - Obsluha zákazníků/14 - Pekárna/14 - Pekárna.md>) | půlsemestrálky 2014–19, Z14 |
| 15 | [Úřad s dodatečnými přepážkami](<09 - Obsluha zákazníků/15 - Úřad s dodatečnými přepážkami/15 - Úřad s dodatečnými přepážkami.md>) | půlsemestrálky 2014–19, Z10 |
| 16 | [Menza](<09 - Obsluha zákazníků/16 - Menza/16 - Menza.md>) | půlsemestrálky 2014–19, Z9 |
| 17 | [Hudební rádio](<09 - Obsluha zákazníků/17 - Hudební rádio/17 - Hudební rádio.md>) | půlsemestrálky 2014–19, Z7 |
| 18 | [Nemocniční ambulance](<09 - Obsluha zákazníků/18 - Nemocniční ambulance/18 - Nemocniční ambulance.md>) | půlsemestrálky 2014–19, Z6 |
| 19 | [Banka se třemi pracovníky](<09 - Obsluha zákazníků/19 - Banka se třemi pracovníky/19 - Banka se třemi pracovníky.md>) | půlsemestrálka 2013/14 A |
| 20 | [Pražírna kávy](<09 - Obsluha zákazníků/20 - Pražírna kávy/20 - Pražírna kávy.md>) | půlsemestrálka 2010/11 |
| 21 | [Banka a lupič](<09 - Obsluha zákazníků/21 - Banka a lupič/21 - Banka a lupič.md>) | půlsemestrálka 2010/11 |
| 22 | [Telefonní ústředna](<09 - Obsluha zákazníků/22 - Telefonní ústředna/22 - Telefonní ústředna.md>) | půlsemestrálka (rok neznámý, Studentská skripta 2015/16) |

## 10 Slovní úlohy: počítačové systémy

| Č. | Úloha | Původ |
|---|---|---|
| 01 | [Server s údržbou po 1000 požadavcích](<10 - Počítačové systémy/01 - Server s údržbou po 1000 požadavcích/01 - Server s údržbou po 1000 požadavcích.md>) | půlsemestrálka 2023/24 A |
| 02 | [Výpočetní služba se spánkem](<10 - Počítačové systémy/02 - Výpočetní služba se spánkem/02 - Výpočetní služba se spánkem.md>) | půlsemestrálka 2023/24 B |
| 03 | [Databázový server](<10 - Počítačové systémy/03 - Databázový server/03 - Databázový server.md>) | půlsemestrálky 2014–19, Z22 |
| 04 | [Počítačový server](<10 - Počítačové systémy/04 - Počítačový server/04 - Počítačový server.md>) | půlsemestrálka 2013/14 C |
| 05 | [Zvuková karta](<10 - Počítačové systémy/05 - Zvuková karta/05 - Zvuková karta.md>) | půlsemestrálka (rok neznámý, Příprava 2021/22) |

## 11 Slovní úlohy: doprava a dávky

| Č. | Úloha | Původ |
|---|---|---|
| 01 | [Výletní autobus](<11 - Doprava a dávky/01 - Výletní autobus/01 - Výletní autobus.md>) | půlsemestrálka 2025/26 C |
| 02 | [Vyhlídkové lety](<11 - Doprava a dávky/02 - Vyhlídkové lety/02 - Vyhlídkové lety.md>) | půlsemestrálka 2024/25 C |
| 03 | [Pizzerie s rozvozem](<11 - Doprava a dávky/03 - Pizzerie s rozvozem/03 - Pizzerie s rozvozem.md>) | půlsemestrálka 2022/23 C |
| 04 | [Výletní loď](<11 - Doprava a dávky/04 - Výletní loď/04 - Výletní loď.md>) | půlsemestrálka 2021/22 C |
| 05 | [Překladiště kontejnerů](<11 - Doprava a dávky/05 - Překladiště kontejnerů/05 - Překladiště kontejnerů.md>) | půlsemestrálka 2021/22 A |
| 06 | [Festivalový autobus](<11 - Doprava a dávky/06 - Festivalový autobus/06 - Festivalový autobus.md>) | půlsemestrálky 2014–19, Z21 |
| 07 | [Vyhlídková loď na molu](<11 - Doprava a dávky/07 - Vyhlídková loď na molu/07 - Vyhlídková loď na molu.md>) | půlsemestrálky 2014–19, Z18 |
| 08 | [Přepravní firma](<11 - Doprava a dávky/08 - Přepravní firma/08 - Přepravní firma.md>) | půlsemestrálky 2014–19, Z12 |
| 09 | [Překladiště s jeřábem](<11 - Doprava a dávky/09 - Překladiště s jeřábem/09 - Překladiště s jeřábem.md>) | půlsemestrálky 2014–19, Z5 |
| 10 | [Bagrista a nákladní auta](<11 - Doprava a dávky/10 - Bagrista a nákladní auta/10 - Bagrista a nákladní auta.md>) | půlsemestrálky 2014–19, Z4 |
| 11 | [Výletní loď na jezeře](<11 - Doprava a dávky/11 - Výletní loď na jezeře/11 - Výletní loď na jezeře.md>) | půlsemestrálky 2014–19, Z1 |
| 12 | [Přehrada s přístavišti](<11 - Doprava a dávky/12 - Přehrada s přístavišti/12 - Přehrada s přístavišti.md>) | půlsemestrálka 2011/12 |
| 13 | [Pošta s doporučenými zásilkami](<11 - Doprava a dávky/13 - Pošta s doporučenými zásilkami/13 - Pošta s doporučenými zásilkami.md>) | půlsemestrálka 2011/12 |
| 14 | [Přehrada s vyhlídkovou lodí](<11 - Doprava a dávky/14 - Přehrada s vyhlídkovou lodí/14 - Přehrada s vyhlídkovou lodí.md>) | půlsemestrálka (rok neznámý, Příprava 2021/22) |

## 12 Slovní úlohy: výroba, zdroje a sklady

| Č. | Úloha | Původ |
|---|---|---|
| 01 | [Zahradnictví a bouřka](<12 - Výroba a sklady/01 - Zahradnictví a bouřka/01 - Zahradnictví a bouřka.md>) | půlsemestrálka 2024/25 A |
| 02 | [Sběrači jahod](<12 - Výroba a sklady/02 - Sběrači jahod/02 - Sběrači jahod.md>) | půlsemestrálka 2021/22 B |
| 03 | [Výrobní hala](<12 - Výroba a sklady/03 - Výrobní hala/03 - Výrobní hala.md>) | půlsemestrálky 2014–19, Z24 |
| 04 | [Jahodová farma](<12 - Výroba a sklady/04 - Jahodová farma/04 - Jahodová farma.md>) | půlsemestrálky 2014–19, Z23 |
| 05 | [Spalovna se třemi vozy](<12 - Výroba a sklady/05 - Spalovna se třemi vozy/05 - Spalovna se třemi vozy.md>) | půlsemestrálky 2014–19, Z20 |
| 06 | [Moštárna](<12 - Výroba a sklady/06 - Moštárna/06 - Moštárna.md>) | půlsemestrálky 2014–19, Z16 |
| 07 | [Spalovna](<12 - Výroba a sklady/07 - Spalovna/07 - Spalovna.md>) | půlsemestrálky 2014–19, Z15 |
| 08 | [Hasiči](<12 - Výroba a sklady/08 - Hasiči/08 - Hasiči.md>) | půlsemestrálky 2014–19, Z13 |
| 09 | [Přečerpávací elektrárna II](<12 - Výroba a sklady/09 - Přečerpávací elektrárna II/09 - Přečerpávací elektrárna II.md>) | půlsemestrálky 2014–19, Z11 |
| 10 | [Zahradník na FIT](<12 - Výroba a sklady/10 - Zahradník na FIT/10 - Zahradník na FIT.md>) | půlsemestrálky 2014–19, Z8 |
| 11 | [Přečerpávací elektrárna](<12 - Výroba a sklady/11 - Přečerpávací elektrárna/11 - Přečerpávací elektrárna.md>) | půlsemestrálky 2014–19, Z3 |
| 12 | [Uhelný mlýn](<12 - Výroba a sklady/12 - Uhelný mlýn/12 - Uhelný mlýn.md>) | půlsemestrálky 2014–19, Z2 |
| 13 | [Stavba z betonu](<12 - Výroba a sklady/13 - Stavba z betonu/13 - Stavba z betonu.md>) | půlsemestrálka 2013/14 D |
| 14 | [Výroba hrášku](<12 - Výroba a sklady/14 - Výroba hrášku/14 - Výroba hrášku.md>) | půlsemestrálka 2013/14 B |
| 15 | [Dílna se třemi stroji](<12 - Výroba a sklady/15 - Dílna se třemi stroji/15 - Dílna se třemi stroji.md>) | půlsemestrálka 2011/12 |
| 16 | [Tunel](<12 - Výroba a sklady/16 - Tunel/16 - Tunel.md>) | půlsemestrálka 2011/12 |
| 17 | [Chmelová brigáda](<12 - Výroba a sklady/17 - Chmelová brigáda/17 - Chmelová brigáda.md>) | půlsemestrálka 2010/11 |
| 18 | [Logistická centrála](<12 - Výroba a sklady/18 - Logistická centrála/18 - Logistická centrála.md>) | půlsemestrálka 2010/11 |
