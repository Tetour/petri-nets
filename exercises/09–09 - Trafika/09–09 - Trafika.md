# 09–09 – Trafika

## Zadání

> Do trafiky přichází zákazníci v intervalech daných exponenciálním rozložením se středem 5 minut. V trafice pracuje jeden prodavač. Doba obsluhy zákazníka se řídí exponenciálním rozložením se středem 2 minuty. Pokud prodavač nemá zákazníky 10 minut, pak odchází do skladu a vrací se po 10 minutách. Příchozí zákazník okamžitě z trafiky odchází, pokud u pultu není přítomen prodavač.
>
> **V modelu jednoznačně ukažte (přechodem) moment, kdy transakce opouští systém.**

Podobné úlohy: [04–01 – Automat na kávu – údržba po nečinnosti](<../04–01 - Automat na kávu – údržba po nečinnosti/04–01 - Automat na kávu – údržba po nečinnosti.md>), [04–08 – Spánek po nečinnosti](<../04–08 - Spánek po nečinnosti/04–08 - Spánek po nečinnosti.md>), [04–04 – Údržba při prázdné frontě](<../04–04 - Údržba při prázdné frontě/04–04 - Údržba při prázdné frontě.md>).

## Interpretace

<details>
<summary>Zobrazit interpretaci (nápověda)</summary>

- **Prodavač má dvě role, a proto dvě místa.** *prodavač* je zařízení pro obsluhu (značka = volný). *přítomen* říká, že stojí u pultu. Jedno místo nestačí: když prodavač obsluhuje, je obsazený, ale přítomný, takže nový zákazník se má postavit do fronty, ne odejít. Stejně to má Hrubý.
- **Vstup zákazníka** je podmínka přes prioritu: přechod `p=1` otestuje *přítomen* (hrana tam a zpět) a pustí zákazníka do *Fronty*. Když prodavač chybí, zbude jen přechod s `p=0` a zákazník hned odchází (vlastní výstupní přechod).
- **„Nemá zákazníky 10 minut“** je časovaný přechod `10 min`, jehož jediným vstupem je *prodavač*. Odpočet začne, jakmile je prodavač volný. Přijde-li zákazník, obsazení mu značku vezme a odpočet zanikne (slajd 139). Když je prodavač volný, je fronta vždy prázdná (obsazení je okamžité), takže značka v *prodavač* znamená přesně „nemá zákazníky“.
- **Odchod do skladu:** po vypršení odpočtu okamžitý přechod *do skladu* vezme i značku *přítomen*. Od té chvíle odcházejí všichni příchozí. Po `10 min` se vrátí obě značky a odpočet nečinnosti běží znovu; když zase nikdo nepřijde, jde prodavač do skladu znovu.
- **Proč `p=2`** (převzato od Hrubého): kdyby zákazník přišel přesně v okamžiku, kdy vyprší 10 minut, musí se nejdřív provést odchod do skladu, jinak by se zákazník zařadil do fronty k nepřítomnému prodavači. Se spojitým rozložením to prakticky nenastane; Hrubý si k tomu poznamenal, že je to velmi hypotetická možnost.
- Ve skladu nikdo nečeká ve frontě: prodavač odchází jen s prázdnou frontou a příchozí během jeho nepřítomnosti hned odcházejí.

</details>

## Petriho síť

<details>
<summary>Zobrazit Petriho síť</summary>

![Petriho síť – trafika](net.svg)

| Požadavek | Prvek sítě |
|---|---|
| příchody exp(5 min) | *generátor* ⇄ `exp(5 min)` → *příchozí* |
| prodavač u pultu → zákazník se zařadí | `p=1` s testem *přítomen* → *Fronta* |
| prodavač chybí → zákazník hned odchází | `p=0` přechod bez výstupu (*není prodavač: odchází*) |
| jeden prodavač, obsluha exp(2 min) | *prodavač* (1 značka), obsazení, `exp(2 min)` vrací značku |
| 10 min bez zákazníků | `10 min` se vstupem jen z *prodavač* → *nikdo nepřišel* |
| odchod do skladu | *do skladu* (`p=2`) bere i *přítomen* → *ve skladu* |
| návrat po 10 min | `10 min` vrací značky do *přítomen* i *prodavač* |
| odchod obslouženého | *obsloužen* → přechod *odchod* bez výstupu |

Kontrola simulací: platí *prodavač* + obsluha + *nikdo nepřišel* + *ve skladu* = 1 a *přítomen* + *ve skladu* = 1. Na 10 000 příchodů jde prodavač zhruba 790× do skladu a asi 1 580 zákazníků (16 %) odejde neobslouženo; fronta zůstává krátká (nejvýš 9).

</details>

## Časté chyby

<details>
<summary>Zobrazit časté chyby</summary>

- Jedno místo pro prodavače, které slouží zároveň jako test přítomnosti. Pak odchází i zákazník, který přijde během obsluhy, přestože prodavač u pultu je.
- Odpočet nečinnosti, který zákazník nepřeruší (např. časovač na samostatném místě, nezávislém na obsluze). „Nemá zákazníky 10 minut“ znamená 10 minut v kuse bez zákazníka.
- Časovač nečinnosti se vstupem z *přítomen*: ten běží i během obsluhy, protože prodavač je přítomen i tehdy.
- Zákazník, který přijde během nepřítomnosti, čeká ve frontě. Podle zadání musí okamžitě odejít, a to přes výstupní přechod.
- Po návratu ze skladu se vrátí jen jedna ze dvou značek (*přítomen* nebo *prodavač*). Trafika pak buď nikoho nepustí dovnitř, nebo nikoho neobslouží.

</details>

## Původ a zdroje

<details>
<summary>Zobrazit původ a zdroje</summary>

**Původ:** půlsemestrální písemka 2022/23, varianta B, 10 bodů.

**Zdroje:**

- `Fitcheats/Půlsemestrálky/Zadání z minulých let/2022-23.pdf`, str. 2 (fotka zadání, spodek listu je zakrytý)
- `Fitcheats/Půlsemestrálky/Zadání z minulých let/2024-25 - Varianta A (fotky).pdf`, str. 5–6 (celé zadání a řešení kreslené na cvičení)
- `Fitcheats/Půlsemestrálky/Hrubý - Řešení 2022-23.pdf`, str. 2 (řešení od Hrubého)

**Existující řešení:**

- **Hrubý (str. 2):** síť výše je jeho řešení překreslené. Místo *přítomen* testuje přechod `p=1` do *Fronty*, z téhož místa vede výstupní přechod pro zákazníka, který prodavače nezastihne. Místo *prodavač* má označené jako „Facility“, z něj vede `10min` (poznámka „nikdo nepřichází“) → místo → `p=2` odchod do skladu (bere *přítomen*) → místo → `10min` návrat, který vrací obě značky. Obsloužený odchází přes vlastní výstupní přechod. Jediný rozdíl: generátor kreslí bez místa.
- **Řešení ze cvičení (fotky 2024/25, str. 6):** stejná stavba. Vstup do *FRONTA* je `p=1` s testem místa přítomnosti (zakroužkované modře), odchod nepřítomnému prodavači je vodorovný výstupní přechod nad místem příchodu. Obsazení *L* má `P=1`. Úsek mezi prvním `10 min` a vysokým okamžitým přechodem je přeškrtaný a zakroužkovaný, takže ho nelze spolehlivě přečíst; písmeno „F“ u tohoto přechodu možná znamená test prázdné fronty. Ten není potřeba, protože při volném prodavači je fronta vždy prázdná.

</details>
