# Studijní plán

<!-- Generuje `make index` (python3 -m pn.index) z pn/catalog.py; needitovat ručně. -->

Všech 118 úloh v pořadí, ve kterém se je vyplatí řešit: nejdřív vzory a nejnovější půlsemestrálky, pak mechanismy, které vzory přímo neukazují, zbylé nové půlsemestrálky, značení v čase t, a nakonec opakování a starší úlohy. Číslování běží přes celý plán, takže stačí si pamatovat číslo poslední vyřešené úlohy. Úlohy podle kategorií jsou v [Seznamu úloh](<Seznam úloh.md>).

Než začneš, projdi [Notace a vzory](<../basics/Notace a vzory.md>) a [Jak síť funguje](<../basics/Jak síť funguje.md>).

## 1. Začni tady (1–15)

Každý vzor z [Notace a vzory](<../basics/Notace a vzory.md>) aspoň jednou, pak nejnovější půlsemestrálky. Stejný seznam je v [Seznamu úloh](<Seznam úloh.md#začni-tady>).

1. [Opravářská dílna](<01 - Základní modely/01 - Opravářská dílna/01 - Opravářská dílna.md>) (01/01): generátor, zařízení, pravděpodobnostní větvení, odchod ze systému
2. [Samoobsluha](<01 - Základní modely/02 - Samoobsluha/02 - Samoobsluha.md>) (01/02): sklad (vozíky), několik zařízení za sebou, výběr pokladny
3. [Netrpělivé požadavky](<02 - Netrpělivost a omezená fronta/01 - Netrpělivé požadavky/01 - Netrpělivé požadavky.md>) (02/01): netrpělivost (timeout ve frontě)
4. [Porucha s opravou, návrat do fronty](<03 - Poruchy/03 - Porucha s opravou, návrat do fronty/03 - Porucha s opravou, návrat do fronty.md>) (03/03): přerušení obsluhy poruchou
5. [Údržba po každé 10. obsluze](<04 - Údržba a spánek/06 - Údržba po každé 10. obsluze/06 - Údržba po každé 10. obsluze.md>) (04/06): čítač: každá N-tá transakce
6. [Přerušení příchodů při plné frontě](<05 - Délka fronty a kapacita/05 - Přerušení příchodů při plné frontě/05 - Přerušení příchodů při plné frontě.md>) (05/05): test délky fronty, dočasné zastavení příchodů
7. [Kopírovací centrum](<09 - Obsluha zákazníků/10 - Kopírovací centrum/10 - Kopírovací centrum.md>) (09/10): půlsemestrálka 2022/23: větvení, netrpělivost; s Hrubého řešením
8. [Klientské centrum](<09 - Obsluha zákazníků/06 - Klientské centrum/06 - Klientské centrum.md>) (09/06): půlsemestrálka 2023/24: zastavení příchodů podle délky fronty
9. [Centrum MM1 s rychlým režimem](<09 - Obsluha zákazníků/04 - Centrum MM1 s rychlým režimem/04 - Centrum MM1 s rychlým režimem.md>) (09/04): půlsemestrálka 2024/25: přepínání režimu podle fronty
10. [Pizza stánek](<09 - Obsluha zákazníků/05 - Pizza stánek/05 - Pizza stánek.md>) (09/05): půlsemestrálka 2024/25: dva zdroje, priorita
11. [Zahradnictví a bouřka](<12 - Výroba a sklady/01 - Zahradnictví a bouřka/01 - Zahradnictví a bouřka.md>) (12/01): půlsemestrálka 2024/25: proces, který přerušuje jiný proces
12. [Vyhlídkové lety](<11 - Doprava a dávky/02 - Vyhlídkové lety/02 - Vyhlídkové lety.md>) (11/02): půlsemestrálka 2024/25: dávka s odjezdem po čase
13. [Úřad](<09 - Obsluha zákazníků/01 - Úřad/01 - Úřad.md>) (09/01): půlsemestrálka 2025/26: dočasné posílení kapacity
14. [Obslužné centrum](<09 - Obsluha zákazníků/02 - Obslužné centrum/02 - Obslužné centrum.md>) (09/02): půlsemestrálka 2025/26: if–else přes prioritu, den a noc
15. [Psí salon](<09 - Obsluha zákazníků/03 - Psí salon/03 - Psí salon.md>) (09/03): půlsemestrálka 2025/26: vyprázdnění fronty, zastavení příchodů

## 2. Nové mechanismy (16–29)

Krátké zkouškové otázky s triky, které vzory přímo neukazují. Nejdřív doba obsluhy podle stavu a priority, pak varianty poruch, kapacity a nečinnosti.

16. [MD1 – střídání 2 a 3](<06 - Doba obsluhy podle stavu/02 - MD1 – střídání 2 a 3/02 - MD1 – střídání 2 a 3.md>) (06/02): doba obsluhy podle stavu: dva stavy volné linky
17. [MD3 – poslední volné zařízení](<06 - Doba obsluhy podle stavu/03 - MD3 – poslední volné zařízení/03 - MD3 – poslední volné zařízení.md>) (06/03): doba obsluhy podle počtu volných linek
18. [MD1 – podle doby od poslední obsluhy](<06 - Doba obsluhy podle stavu/04 - MD1 – podle doby od poslední obsluhy/04 - MD1 – podle doby od poslední obsluhy.md>) (06/04): měření nečinnosti od konce obsluhy
19. [Dva proudy příchodů](<07 - Priority/04 - Dva proudy příchodů/04 - Dva proudy příchodů.md>) (07/04): dva generátory, priorita obsluhy
20. [Priorita procesu a obsluhy](<07 - Priority/05 - Priorita procesu a obsluhy/05 - Priorita procesu a obsluhy.md>) (07/05): rozdíl mezi prioritou procesu a prioritou obsluhy
21. [Každá 10. s prioritou obsluhy](<07 - Priority/03 - Každá 10. s prioritou obsluhy/03 - Každá 10. s prioritou obsluhy.md>) (07/03): čítač a priorita obsluhy
22. [Kritická havárie](<03 - Poruchy/05 - Kritická havárie/05 - Kritická havárie.md>) (03/05): odstávka linky na pevnou dobu, zrušení rozpracované obsluhy
23. [Porucha prodlouží probíhající obsluhu o 5](<03 - Poruchy/10 - Porucha prodlouží probíhající obsluhu o 5/10 - Porucha prodlouží probíhající obsluhu o 5.md>) (03/10): porucha obsluhu prodlouží, místo aby ji zrušila
24. [Přerušení příliš dlouhé obsluhy](<03 - Poruchy/11 - Přerušení příliš dlouhé obsluhy/11 - Přerušení příliš dlouhé obsluhy.md>) (03/11): timeout na obsluze, ne ve frontě
25. [Pomocník přidá kapacitu](<05 - Délka fronty a kapacita/10 - Pomocník přidá kapacitu/10 - Pomocník přidá kapacitu.md>) (05/10): dočasná jednotka kapacity navíc
26. [Údržba zabere celou kapacitu](<05 - Délka fronty a kapacita/09 - Údržba zabere celou kapacitu/09 - Údržba zabere celou kapacitu.md>) (05/09): zabrání celé kapacity skladu po jednotkách
27. [Každá 100. transakce vyprázdní frontu](<05 - Délka fronty a kapacita/07 - Každá 100. transakce vyprázdní frontu/07 - Každá 100. transakce vyprázdní frontu.md>) (05/07): čítač a vyprázdnění fronty
28. [Spánek po nečinnosti](<04 - Údržba a spánek/08 - Spánek po nečinnosti/08 - Spánek po nečinnosti.md>) (04/08): odpočet nečinnosti, probuzení příchodem
29. [MM3 bez fronty s opakováním](<02 - Netrpělivost a omezená fronta/05 - MM3 bez fronty s opakováním/05 - MM3 bez fronty s opakováním.md>) (02/05): odmítnutí a návrat do systému po čase

## 3. Půlsemestrálky 2021/22–2025/26 (30–40)

Zbylé nové půlsemestrálky, od nejnovější. Řeš je celé na čas a nápovědu otevři až po nakreslení celé sítě.

30. [Výletní autobus](<11 - Doprava a dávky/01 - Výletní autobus/01 - Výletní autobus.md>) (11/01): 2025/26: dávka, autobus odjede plný nebo po 20 minutách
31. [Automat na kávu](<09 - Obsluha zákazníků/07 - Automat na kávu/07 - Automat na kávu.md>) (09/07): 2023/24: porucha 5–6 h po opravě zasáhne probíhající nebo další obsluhu
32. [Server s údržbou po 1000 požadavcích](<10 - Počítačové systémy/01 - Server s údržbou po 1000 požadavcích/01 - Server s údržbou po 1000 požadavcích.md>) (10/01): 2023/24: čítač spustí údržbu
33. [Výpočetní služba se spánkem](<10 - Počítačové systémy/02 - Výpočetní služba se spánkem/02 - Výpočetní služba se spánkem.md>) (10/02): 2023/24: spánek po nečinnosti, probuzení příchodem
34. [Cestovní kancelář](<09 - Obsluha zákazníků/08 - Cestovní kancelář/08 - Cestovní kancelář.md>) (09/08): 2022/23: test délky fronty, dvě přepážky navíc na hodinu
35. [Trafika](<09 - Obsluha zákazníků/09 - Trafika/09 - Trafika.md>) (09/09): 2022/23: prodavač ve dvou rolích, odchod do skladu po nečinnosti
36. [Pizzerie s rozvozem](<11 - Doprava a dávky/03 - Pizzerie s rozvozem/03 - Pizzerie s rozvozem.md>) (11/03): 2022/23: rozvoz všech hotových objednávek najednou
37. [Kopírovací centrum s poruchami](<09 - Obsluha zákazníků/11 - Kopírovací centrum s poruchami/11 - Kopírovací centrum s poruchami.md>) (09/11): 2021/22: obsluha s kapacitou 10, poruchy
38. [Sběrači jahod](<12 - Výroba a sklady/02 - Sběrači jahod/02 - Sběrači jahod.md>) (12/02): 2021/22: sběrači v cyklu, siréna podle délky fronty
39. [Výletní loď](<11 - Doprava a dávky/04 - Výletní loď/04 - Výletní loď.md>) (11/04): 2021/22: čítač nastoupených, odplutí s 20 turisty
40. [Překladiště kontejnerů](<11 - Doprava a dávky/05 - Překladiště kontejnerů/05 - Překladiště kontejnerů.md>) (11/05): 2021/22: auto se 3 kontejnery, vlak odjede plný

## 4. Značení v čase t (41–49)

Jiná dovednost: síť nekreslíš, ale ručně ji simuluješ (kalendář, fronta, značení). Nejdřív D/D/1, pak FIFO, nakonec LIFO.

41. [DD1 – příchody 3, obsluha 2](<08 - Značení v čase t/09 - DD1 – příchody 3, obsluha 2/09 - DD1 – příchody 3, obsluha 2.md>) (08/09): stabilní D/D/1, tabulka stavů
42. [DD1 – příchody 2, obsluha 4](<08 - Značení v čase t/08 - DD1 – příchody 2, obsluha 4/08 - DD1 – příchody 2, obsluha 4.md>) (08/08): nestabilní D/D/1, fronta roste
43. [DD2 FIFO, čas 6,5](<08 - Značení v čase t/01 - DD2 FIFO, čas 6,5/01 - DD2 FIFO, čas 6,5.md>) (08/01): dvě linky, FIFO
44. [DD3 FIFO, čas 9,5](<08 - Značení v čase t/07 - DD3 FIFO, čas 9,5/07 - DD3 FIFO, čas 9,5.md>) (08/07): tři linky, FIFO
45. [DD2 LIFO obsluha 4, čas 9,5](<08 - Značení v čase t/05 - DD2 LIFO obsluha 4, čas 9,5/05 - DD2 LIFO obsluha 4, čas 9,5.md>) (08/05): LIFO
46. [DD2 LIFO obsluha 5, čas 9,5](<08 - Značení v čase t/04 - DD2 LIFO obsluha 5, čas 9,5/04 - DD2 LIFO obsluha 5, čas 9,5.md>) (08/04): LIFO, delší obsluha
47. [DD2 LIFO obsluha 6, čas 13,5](<08 - Značení v čase t/03 - DD2 LIFO obsluha 6, čas 13,5/03 - DD2 LIFO obsluha 6, čas 13,5.md>) (08/03): LIFO, události v čase t1
48. [DD3 LIFO, čas 10,5](<08 - Značení v čase t/02 - DD3 LIFO, čas 10,5/02 - DD3 LIFO, čas 10,5.md>) (08/02): tři linky, LIFO
49. [DD4 LIFO, čas 9,5](<08 - Značení v čase t/06 - DD4 LIFO, čas 9,5/06 - DD4 LIFO, čas 9,5.md>) (08/06): čtyři linky, LIFO

## 5. Další varianty mechanismů (50–79)

Opakování ke zkoušce: další varianty už známých mechanismů a zbylé modely z přednášek.

50. [Netrpělivý první ve frontě](<02 - Netrpělivost a omezená fronta/02 - Netrpělivý první ve frontě/02 - Netrpělivý první ve frontě.md>) (02/02): netrpělivý je jen první ve frontě
51. [Fronta omezená na 10](<02 - Netrpělivost a omezená fronta/04 - Fronta omezená na 10/04 - Fronta omezená na 10.md>) (02/04): omezená fronta, if–else přes prioritu
52. [Příklad s netrpělivou transakcí](<02 - Netrpělivost a omezená fronta/03 - Příklad s netrpělivou transakcí/03 - Příklad s netrpělivou transakcí.md>) (02/03): vlastní příklad netrpělivosti
53. [Porucha zruší obsluhu](<03 - Poruchy/01 - Porucha zruší obsluhu/01 - Porucha zruší obsluhu.md>) (03/01): porucha jen zruší obsluhu
54. [Porucha vrací transakci do fronty](<03 - Poruchy/02 - Porucha vrací transakci do fronty/02 - Porucha vrací transakci do fronty.md>) (03/02): přerušená transakce se vrací do fronty
55. [Porucha s opravou, transakce odchází](<03 - Poruchy/04 - Porucha s opravou, transakce odchází/04 - Porucha s opravou, transakce odchází.md>) (03/04): oprava, přerušená transakce odchází
56. [Porucha zničí obsluhu nebo počká](<03 - Poruchy/06 - Porucha zničí obsluhu nebo počká/06 - Porucha zničí obsluhu nebo počká.md>) (03/06): porucha počká na další obsluhu
57. [Každá 10. transakce vyvolá poruchu](<03 - Poruchy/07 - Každá 10. transakce vyvolá poruchu/07 - Každá 10. transakce vyvolá poruchu.md>) (03/07): čítač spustí poruchu
58. [Porucha prodlouží další obsluhu](<03 - Poruchy/08 - Porucha prodlouží další obsluhu/08 - Porucha prodlouží další obsluhu.md>) (03/08): porucha prodlouží až příští obsluhu
59. [Porucha prodlouží obsluhu o 2](<03 - Poruchy/09 - Porucha prodlouží obsluhu o 2/09 - Porucha prodlouží obsluhu o 2.md>) (03/09): prodloužení probíhající obsluhy
60. [Automat na kávu – údržba po nečinnosti](<04 - Údržba a spánek/01 - Automat na kávu – údržba po nečinnosti/01 - Automat na kávu – údržba po nečinnosti.md>) (04/01): údržba po nečinnosti
61. [Automat na kávu – údržba po 50 obsluhách](<04 - Údržba a spánek/02 - Automat na kávu – údržba po 50 obsluhách/02 - Automat na kávu – údržba po 50 obsluhách.md>) (04/02): čítač spustí údržbu
62. [Automat na kávu – uspání](<04 - Údržba a spánek/03 - Automat na kávu – uspání/03 - Automat na kávu – uspání.md>) (04/03): uspání po nečinnosti, delší obsluha po probuzení
63. [Údržba při prázdné frontě](<04 - Údržba a spánek/04 - Údržba při prázdné frontě/04 - Údržba při prázdné frontě.md>) (04/04): test prázdné fronty po obsluze
64. [Údržba po dlouhé obsluze](<04 - Údržba a spánek/05 - Údržba po dlouhé obsluze/05 - Údržba po dlouhé obsluze.md>) (04/05): odpočet během obsluhy rozhodne o údržbě
65. [Údržbář na obchůzce](<04 - Údržba a spánek/07 - Údržbář na obchůzce/07 - Údržbář na obchůzce.md>) (04/07): čítač obsluh, údržbář jako proces
66. [Doba obsluhy podle délky fronty](<05 - Délka fronty a kapacita/01 - Doba obsluhy podle délky fronty/01 - Doba obsluhy podle délky fronty.md>) (05/01): test délky fronty určí dobu obsluhy
67. [Dočasně MM2 při dlouhé frontě](<05 - Délka fronty a kapacita/02 - Dočasně MM2 při dlouhé frontě/02 - Dočasně MM2 při dlouhé frontě.md>) (05/02): dočasná druhá linka
68. [Natrvalo MM3 při dlouhé frontě](<05 - Délka fronty a kapacita/03 - Natrvalo MM3 při dlouhé frontě/03 - Natrvalo MM3 při dlouhé frontě.md>) (05/03): trvalé přidání linek
69. [Interval příchodů podle délky fronty](<05 - Délka fronty a kapacita/04 - Interval příchodů podle délky fronty/04 - Interval příchodů podle délky fronty.md>) (05/04): generátor se dvěma intervaly
70. [MM3 – zastavení příchodů](<05 - Délka fronty a kapacita/06 - MM3 – zastavení příchodů/06 - MM3 – zastavení příchodů.md>) (05/06): zastavení příchodů podle obsazených linek
71. [Sklad s dočasně větší kapacitou](<05 - Délka fronty a kapacita/08 - Sklad s dočasně větší kapacitou/08 - Sklad s dočasně větší kapacitou.md>) (05/08): pravidelné rozšíření kapacity skladu
72. [MD1 – prodlužování po 10 obsluhách](<06 - Doba obsluhy podle stavu/01 - MD1 – prodlužování po 10 obsluhách/01 - MD1 – prodlužování po 10 obsluhách.md>) (06/01): čítač mění dobu obsluhy
73. [Příklad s prioritou procesu](<07 - Priority/01 - Příklad s prioritou procesu/01 - Příklad s prioritou procesu.md>) (07/01): vlastní příklad priority procesu
74. [Každá N-tá s prioritou procesu](<07 - Priority/02 - Každá N-tá s prioritou procesu/02 - Každá N-tá s prioritou procesu.md>) (07/02): čítač a priorita procesu
75. [MM3 – prioritní zabírají 2 linky](<07 - Priority/06 - MM3 – prioritní zabírají 2 linky/06 - MM3 – prioritní zabírají 2 linky.md>) (07/06): prioritní transakce zabírá dvě linky
76. [Zdravotní ordinace](<01 - Základní modely/03 - Zdravotní ordinace/03 - Zdravotní ordinace.md>) (01/03): kartotéka, laboratoř, lékař, větvení
77. [Výrobní systém](<01 - Základní modely/04 - Výrobní systém/04 - Výrobní systém.md>) (01/04): P/T síť, dvě vrtačky jako sklad
78. [Kritická sekce](<01 - Základní modely/05 - Kritická sekce/05 - Kritická sekce.md>) (01/05): vzájemné vyloučení dvou procesů
79. [Kravín](<01 - Základní modely/06 - Kravín/06 - Kravín.md>) (01/06): zdroje a dávky (konvice do auta)

## 6. Starší půlsemestrálky (2010–2019) (80–118)

Delší úlohy pro procvičení, po kategoriích. Ber je podle chuti; v každé kategorii jsou novější první.

80. [Pošta](<09 - Obsluha zákazníků/12 - Pošta/12 - Pošta.md>) (09/12): řidič se třemi stavy, otevření druhé přepážky
81. [Letiště](<09 - Obsluha zákazníků/13 - Letiště/13 - Letiště.md>) (09/13): priorita přistání, timeout, havárie dráhy
82. [Pekárna](<09 - Obsluha zákazníků/14 - Pekárna/14 - Pekárna.md>) (09/14): pekař ve dvou rolích, zásoba chleba
83. [Úřad s dodatečnými přepážkami](<09 - Obsluha zákazníků/15 - Úřad s dodatečnými přepážkami/15 - Úřad s dodatečnými přepážkami.md>) (09/15): pracovní doba, přepážky navíc podle fronty
84. [Menza](<09 - Obsluha zákazníků/16 - Menza/16 - Menza.md>) (09/16): karanténa: vyprázdnění systému, zastavení příchodů
85. [Hudební rádio](<09 - Obsluha zákazníků/17 - Hudební rádio/17 - Hudební rádio.md>) (09/17): reklama každou hodinu, přerušený rozhovor
86. [Nemocniční ambulance](<09 - Obsluha zákazníků/18 - Nemocniční ambulance/18 - Nemocniční ambulance.md>) (09/18): lékaři odjíždějí se sanitou k zásahu
87. [Banka se třemi pracovníky](<09 - Obsluha zákazníků/19 - Banka se třemi pracovníky/19 - Banka se třemi pracovníky.md>) (09/19): vedoucí jako proces, auto s vysokou prioritou
88. [Pražírna kávy](<09 - Obsluha zákazníků/20 - Pražírna kávy/20 - Pražírna kávy.md>) (09/20): netrpělivý první ve frontě, prodavač mezi prodejnou a dílnou
89. [Banka a lupič](<09 - Obsluha zákazníků/21 - Banka a lupič/21 - Banka a lupič.md>) (09/21): přepadení zastaví příchody, policista
90. [Telefonní ústředna](<09 - Obsluha zákazníků/22 - Telefonní ústředna/22 - Telefonní ústředna.md>) (09/22): sklad s kapacitou 20, operátorka, priorita
91. [Databázový server](<10 - Počítačové systémy/03 - Databázový server/03 - Databázový server.md>) (10/03): proces S počítá obsluhy a aktivuje druhý proces
92. [Počítačový server](<10 - Počítačové systémy/04 - Počítačový server/04 - Počítačový server.md>) (10/04): procesor a síťová linka, úloha drží procesor
93. [Zvuková karta](<10 - Počítačové systémy/05 - Zvuková karta/05 - Zvuková karta.md>) (10/05): vyrovnávací paměť, přednost zvukového procesu
94. [Festivalový autobus](<11 - Doprava a dávky/06 - Festivalový autobus/06 - Festivalový autobus.md>) (11/06): autobus sváží po jednom, odpočet 40 minut
95. [Vyhlídková loď na molu](<11 - Doprava a dávky/07 - Vyhlídková loď na molu/07 - Vyhlídková loď na molu.md>) (11/07): netrpělivost, odplutí plné nebo po 3 minutách
96. [Přepravní firma](<11 - Doprava a dávky/08 - Přepravní firma/08 - Přepravní firma.md>) (11/08): rozvoz balíků, nezastižené balíky jedou zpět
97. [Překladiště s jeřábem](<11 - Doprava a dávky/09 - Překladiště s jeřábem/09 - Překladiště s jeřábem.md>) (11/09): pracovní doba, jeřábník na obchůzce
98. [Bagrista a nákladní auta](<11 - Doprava a dávky/10 - Bagrista a nákladní auta/10 - Bagrista a nákladní auta.md>) (11/10): tři auta v cyklu, úsek po metrech
99. [Výletní loď na jezeře](<11 - Doprava a dávky/11 - Výletní loď na jezeře/11 - Výletní loď na jezeře.md>) (11/11): provozní doba, odjezd plné lodi nebo po 2 minutách
100. [Přehrada s přístavišti](<11 - Doprava a dávky/12 - Přehrada s přístavišti/12 - Přehrada s přístavišti.md>) (11/12): dvě lodě mezi dvěma přístavišti, netrpělivost
101. [Pošta s doporučenými zásilkami](<11 - Doprava a dávky/13 - Pošta s doporučenými zásilkami/13 - Pošta s doporučenými zásilkami.md>) (11/13): nakládání do kapacity, vykládka po jedné
102. [Přehrada s vyhlídkovou lodí](<11 - Doprava a dávky/14 - Přehrada s vyhlídkovou lodí/14 - Přehrada s vyhlídkovou lodí.md>) (11/14): odjezd plné lodi nebo po 15 minutách
103. [Výrobní hala](<12 - Výroba a sklady/03 - Výrobní hala/03 - Výrobní hala.md>) (12/03): odstavení montovny podle fronty k lakovně
104. [Jahodová farma](<12 - Výroba a sklady/04 - Jahodová farma/04 - Jahodová farma.md>) (12/04): vaření z 5 bedýnek, prioritní balení
105. [Spalovna se třemi vozy](<12 - Výroba a sklady/05 - Spalovna se třemi vozy/05 - Spalovna se třemi vozy.md>) (12/05): tři vozy v cyklu, komora s kapacitou 5
106. [Moštárna](<12 - Výroba a sklady/06 - Moštárna/06 - Moštárna.md>) (12/06): lisy, moštaři a sběrači v cyklu
107. [Spalovna](<12 - Výroba a sklady/07 - Spalovna/07 - Spalovna.md>) (12/07): rychlosti jako časy, sklad odpadu
108. [Hasiči](<12 - Výroba a sklady/08 - Hasiči/08 - Hasiči.md>) (12/08): požár zaniká bez hašení, extrémní požár bere všechny vozy
109. [Přečerpávací elektrárna II](<12 - Výroba a sklady/09 - Přečerpávací elektrárna II/09 - Přečerpávací elektrárna II.md>) (12/09): voda jako značky, den a noc, havárie
110. [Zahradník na FIT](<12 - Výroba a sklady/10 - Zahradník na FIT/10 - Zahradník na FIT.md>) (12/10): konvice s vodou, zalévání po částech
111. [Přečerpávací elektrárna](<12 - Výroba a sklady/11 - Přečerpávací elektrárna/11 - Přečerpávací elektrárna.md>) (12/11): voda jako značky, den a noc, havárie
112. [Uhelný mlýn](<12 - Výroba a sklady/12 - Uhelný mlýn/12 - Uhelný mlýn.md>) (12/12): havárie, chladnutí a rozehřívání
113. [Stavba z betonu](<12 - Výroba a sklady/13 - Stavba z betonu/13 - Stavba z betonu.md>) (12/13): licí forma jako transakce, zrání betonu
114. [Výroba hrášku](<12 - Výroba a sklady/14 - Výroba hrášku/14 - Výroba hrášku.md>) (12/14): dávka 100 várek, trvanlivost, porucha balení
115. [Dílna se třemi stroji](<12 - Výroba a sklady/15 - Dílna se třemi stroji/15 - Dílna se třemi stroji.md>) (12/15): jeden pracovník pro dva stroje, oprava
116. [Tunel](<12 - Výroba a sklady/16 - Tunel/16 - Tunel.md>) (12/16): den a noc, dvě soupravy, tunel jako sklad metrů
117. [Chmelová brigáda](<12 - Výroba a sklady/17 - Chmelová brigáda/17 - Chmelová brigáda.md>) (12/17): sklad s omezenou kapacitou, procházka
118. [Logistická centrála](<12 - Výroba a sklady/18 - Logistická centrála/18 - Logistická centrála.md>) (12/18): dodávka se 100 balíky, pracovník jako proces
