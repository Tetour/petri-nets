# 11–06 – Festivalový autobus

## Zadání

> Městský festivalový autobus sváží návštěvníky z jejich domovů do areálu festivalu. Kapacita autobusu je 20 míst. Návštěvníci registrují svůj požadavek na odvoz v intervalech daných exp(5min). Autobus při své jízdě po jednom nabírá registrované návštěvníky. Každá jízda autobusu (z areálu k návštěvníkovi, mezi návštěvníky, zpět do areálu) se řídí exp(3min). Autobus se vrací do areálu buď po naplnění kapacity, nebo pokud je již na svozové jízdě déle než 40 minut. Po příjezdu do areálu vyloží návštěvníky (dobu zanedbáváme) a vyráží na další svozovou jízdu. Festival trvá 12 hodin. Čtyři hodiny před koncem festivalu už se návštěvníci neregistrují ke svozu, a pokud už není koho svážet, tak končí i činnost autobusu.
>
> *Zadaný systém modelujte formou Petriho sítě s vyznačením všech potřebných parametrů.*

Věta „V modelu jednoznačně ukažte (přechodem) moment, kdy transakce opouští systém“ v tehdejších zadáních ještě nebyla. Výstupní přechod je v síti přesto, dnes se vyžaduje.

Podobné úlohy: [11–01 – Výletní autobus](<../11–01 - Výletní autobus/11–01 - Výletní autobus.md>), [11–08 – Přepravní firma](<../11–08 - Přepravní firma/11–08 - Přepravní firma.md>), [11–07 – Vyhlídková loď na molu](<../11–07 - Vyhlídková loď na molu/11–07 - Vyhlídková loď na molu.md>).

## Interpretace

<details>
<summary>Zobrazit interpretaci (nápověda)</summary>

- **Transakce** jsou návštěvníci: registrace → *Registrovaní* → vyzvednutí → *V autobusu* → vyložení v areálu → *odchod*. Autobus je jedna značka, která obíhá stavy *Areál* → *na svozu* → *vrací se* → *v areálu* → *Areál*.
- **Jízdy:** každé vyzvednutí je jedna jízda `exp(3 min)` (z areálu k prvnímu návštěvníkovi, pak mezi návštěvníky). Okamžitý přechod vyzvednutí (`p=1`) vezme registrovaného návštěvníka, volné místo a autobus. Po jízdě je návštěvník *V autobusu* a autobus je znovu *na svozu*, kde se rozhoduje o dalším kroku. Návrat do areálu je další jízda `exp(3 min)`.
- **Kapacita:** *Volná místa* (20) se berou při vyzvednutí a vrací při vyložení. „Plno“ testuje 20 návštěvníků *V autobusu* hranami s váhou 20 tam i zpět.
- **40 minut:** výjezd spustí samostatný *odpočet* (časovaný přechod `40 min`), který běží nezávisle na jízdách. Časovač přímo na místě *na svozu* by nešel, protože autobus to místo při každé jízdě opouští a odpočet by začínal znovu. Po uplynutí se autobus vrátí, jakmile je *na svozu*: rozjetou jízdu k návštěvníkovi dokončí. Priorita `p=2` zajistí, že návrat vyhraje nad dalším vyzvednutím. Při návratu kvůli zaplnění si přechod *plno* odpočet vezme, takže zanikne.
- **Když není koho vyzvednout**, autobus čeká *na svozu*. Zadání zná jen dva důvody k návratu (plno, 40 min), proto se nevrací dřív.
- **Vyložení** (`p=1`) bere po jednom všechny návštěvníky *V autobusu* a testuje, že je autobus *v areálu*. Pak přechod *vyloženo* (`p=0`) vrátí autobus do *Areálu*.
- **Výjezd** (`p=1`) testuje, že je někdo registrovaný. Autobus tedy z areálu nevyjíždí naprázdno, odpočet 40 minut začne až s výjezdem. Je to výklad zadání („vyráží na další svozovou jízdu“), jinak by autobus po uzávěrce jezdil prázdné okruhy.
- **Konec festivalu:** po `8 h` (12 h − 4 h) přechod *konec registrací* odebere značku generátoru. *Konec činnosti* (`p=0`) se provede, když je autobus v *Areálu*, registrace jsou uzavřené a nikdo nečeká (jinak vyhraje výjezd s `p=1`). Samotný konec festivalu ve 12 h modelovat není potřeba: autobus skončí dřív (v simulaci zhruba v 8,1–8,5 h).
- **Plno prakticky nenastane:** 20 jízd po `exp(3 min)` trvá v průměru 60 minut, svoz ale končí po 40. Přechod *plno* je přesto nutný, zadání ho výslovně uvádí.

</details>

## Řešení

<details>
<summary>Zobrazit řešení</summary>

![Petriho síť – festivalový autobus](net.svg)

| Požadavek | Prvek sítě |
|---|---|
| registrace exp(5 min) | *generátor* ⇄ `exp(5 min)` → *Registrovaní* |
| kapacita 20 míst | *Volná místa* (20), vyzvednutí bere, vyložení vrací |
| nabírání po jednom, každá jízda exp(3 min) | vyzvednutí `p=1` (*Registrovaní* + volné místo + autobus *na svozu*) → `exp(3 min)` → *V autobusu* a zpět *na svozu* |
| výjezd z areálu | *výjezd* `p=1`: *Areál* + test *Registrovaní* → *na svozu* + *odpočet* |
| návrat po naplnění | *plno*: *na svozu* + *odpočet* + test 20 *V autobusu* → *vrací se* |
| návrat po 40 min | *odpočet* → `40 min` → *40 min uplynulo*; *po 40 min* `p=2` → *vrací se* |
| jízda zpět exp(3 min), vyložení | `exp(3 min)` → *v areálu*; vyložení `p=1` → *na festivalu* → *odchod*; *vyloženo* → *Areál* |
| po 8 h konec registrací | *festival* → `8 h` → *konec registrací* bere značku *generátoru* → *uzavřeno* |
| není koho svážet → konec | *konec činnosti* (`p=0`): *Areál* + test *uzavřeno* → *autobus skončil* |

Kontrola simulací: autobus je vždy právě v jednom stavu, *Volná místa* + jedoucí pro návštěvníka + *V autobusu* = 20 a odpočet běží (nebo uplynul) právě tehdy, když je autobus na svozu. Za 8 h se zaregistruje asi 80–110 návštěvníků, autobus udělá asi 10–11 okruhů, vždy se vrací po 40 minutách (v autobusu nejvýš asi 14 lidí). Pak všechny rozveze a síť se zastaví. Přechod *plno* jsem ověřil zvlášť se zrychlenými registracemi.

</details>

## Časté chyby

<details>
<summary>Zobrazit časté chyby</summary>

- Odpočet 40 min jako časovaný přechod na místě, které autobus při každé jízdě opouští (např. *na svozu*). Odpočet se pak s každým vyzvednutím spouští znovu a měří jen čekání na dalšího návštěvníka.
- Odpočet, který po návratu kvůli zaplnění zůstane v síti: uplyne během další jízdy a autobus pošle zpět příliš brzy.
- Kapacita jako hrana s váhou 20 při výjezdu bez vrácení volných míst při vyložení, nebo nabrání 20 lidí najednou. Návštěvníci se nabírají po jednom a každý stojí jednu jízdu.
- Vyložení jedním přechodem s hranou s váhou 20. V autobusu bývá méně lidí, proto vyložení po jednom ve smyčce s prioritou.
- Zastavení registrací po 12 h místo po 8 h, nebo zastavení autobusu hned po 8 h, i když ještě někdo čeká na odvoz.
- Chybějící priorita u návratu po 40 min: autobus by mohl dál nabírat, i když čas vypršel.

</details>

## Původ a zdroje

**Původ:** půlsemestrálky 2014–19 (přehled zadání), úloha Z21. Rok, varianta ani body nejsou známé.

**Zdroje:**

- `Fitcheats/Půlsemestrálky/Zadání z minulých let/Přehled zadání 2014-19.pdf`, str. 5 (zadání, bez řešení)

**Existující řešení:**

<details>
<summary>Zobrazit existující řešení</summary>

- K této úloze v materiálech žádné řešení není. Nejbližší je výletní autobus z roku 2025/26 ([11–01](<../11–01 - Výletní autobus/11–01 - Výletní autobus.md>)), který také odjíždí buď plný, nebo po uplynutí času, s kapacitou jako místem s 20 značkami.

</details>
