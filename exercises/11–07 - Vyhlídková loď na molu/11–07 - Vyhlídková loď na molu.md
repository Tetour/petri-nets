# 11–07 – Vyhlídková loď na molu

## Zadání

> Na nástupní molo pro vyhlídkové jízdy lodí přichází cestující v intervalech daných exp(5min). Jízdy provádí jedna výletní loď. Každý cestující po 30 minutách svého čekání ve frontě z fronty odchází. Pokud je k molu přistavena loď, cestující po jednom nastupují. Nastoupení jednoho trvá 1 minutu. Loď od mola vyráží, pokud nastane jedna ze dvou okolností: 1) nastoupilo 20 cestujících (naplněna kapacita lodi), 2) od nastoupení posledního uběhly 3 minuty (prázdná fronta). Vyhlídková trasa trvá 1 hodinu, a pak se loď vrací k molu. Dobu vystupování cestujících neuvažujeme.
>
> *Zadaný systém modelujte formou Petriho sítě s vyznačením všech potřebných parametrů.*

Věta „V modelu jednoznačně ukažte (přechodem) moment, kdy transakce opouští systém“ přibyla až v roce 2022/23. Výstupní přechody jsou v síti přesto, dnes se vyžadují.

Podobné úlohy: [11–04 – Výletní loď](<../11–04 - Výletní loď/11–04 - Výletní loď.md>) (stejný typ, s Hrubého řešením), [11–11 – Výletní loď na jezeře](<../11–11 - Výletní loď na jezeře/11–11 - Výletní loď na jezeře.md>), [11–14 – Přehrada s vyhlídkovou lodí](<../11–14 - Přehrada s vyhlídkovou lodí/11–14 - Přehrada s vyhlídkovou lodí.md>), [02–01 – Netrpělivé požadavky](<../02–01 - Netrpělivé požadavky/02–01 - Netrpělivé požadavky.md>).

## Interpretace

<details>
<summary>Zobrazit interpretaci (nápověda)</summary>

- **Loď u mola** je zařízení pro nástup „po jednom“ (jako v [11–04 – Výletní loď](<../11–04 - Výletní loď/11–04 - Výletní loď.md>)), jen má dva stavy: *prázdná* (nikdo ještě nenastoupil) a *s cestujícími*. Nástup jde z obou stavů a po `1 min` vrátí loď vždy do stavu *s cestujícími*; cestující přibude do *Na palubě*.
- **3 minuty od posledního nástupu:** časovaný přechod `3 min` na místě *s cestujícími*. Odpočet začne po každém nástupu. Když je někdo ve frontě (nebo během 3 min přijde), obsazení lodi vezme značku a odpočet zanikne (slajd 139); po jeho nástupu začne nový. Přechod se tedy provede jen při prázdné frontě, přesně 3 min po posledním nástupu.
- Prázdná loď na odpočet nemá: dokud nikdo nenastoupil, není od čeho počítat, a loď čeká na prvního cestujícího. Proto dva stavy lodi.
- **20 cestujících:** okamžitý přechod `p=1` s testem 20 na *Na palubě* (hrany s váhou 20 tam i zpět). Priorita zajistí vyplutí dřív, než by začal nastupovat 21. cestující.
- **Cestující zůstávají v *Na palubě* po celou jízdu** a ze systému odcházejí po návratu (dobu vystupování neuvažujeme). Jejich počet je 1 až 20, proto výstup není hrana s váhou, ale smyčka `p=1` na místě *návrat*; teprve pak (`p=0`) je loď znovu prázdná u mola. Hrubý v 11–04 bere 20 turistů hranou s váhou 20, tady počet není pevný.
- **Netrpělivost:** časovaný `30 min` přímo na *Frontě*, každý čekající má vlastní odpočet. Na rozdíl od 11–04 se fronta při vyplutí nevyprazdňuje; čekající odcházejí jen po 30 min.
- Na počátku je prázdná loď u mola.

</details>

## Petriho síť

<details>
<summary>Zobrazit Petriho síť</summary>

![Petriho síť – vyhlídková loď na molu](net.svg)

| Požadavek | Prvek sítě |
|---|---|
| cestující po exp(5 min) | *generátor* ⇄ `exp(5 min)` → *Fronta* |
| po 30 min čekání odchází | `30 min` z *Fronty* → *odchod* |
| nástup po jednom, 1 min | obsazení *Lodi u mola* (prázdné, nebo s cestujícími), `1 min` → *Na palubě* a loď *s cestujícími* |
| 20 cestujících → vyplutí | `p=1` *plná loď*: test 20 na *Na palubě* + loď → *Plavba* |
| 3 min od posledního nástupu → vyplutí | `3 min` z *Lodi u mola (s cestujícími)* → *Plavba* |
| trasa 1 h, návrat k molu | *Plavba* → `1 h` → *návrat* |
| vystupování (nulová doba) | smyčka `p=1` *výstup* → *konec* → *odchod*; pak *přistavení* (`p=0`) → loď prázdná u mola |

Kontrola simulací: loď je vždy v jednom stavu (prázdná u mola + s cestujícími + nástup + *Plavba* + *návrat* = 1), *Na palubě* je nejvýš 20. Loď skoro vždy vyplouvá po 3 minutách (v průměru s 8–9 cestujícími), plná je jen výjimečně. Asi 40 % cestujících odejde po 30 min, hlavně ti, kdo přijdou během jízdy.

</details>

## Časté chyby

<details>
<summary>Zobrazit časté chyby</summary>

- Odpočet 3 min, který se nezruší, když někdo nastoupí (např. přechod `3 min` na místě, které nástup nebere). Pak loď odpluje 3 min po prvním nástupu, ne po posledním.
- Odpočet 3 min i u prázdné lodi: loď by jezdila prázdná.
- Vyplutí při 20 cestujících bez `p=1`: může začít nastupovat 21.
- Výstup po návratu hranou s váhou 20: při vyplutí po 3 min je cestujících méně a přechod by se nikdy neprovedl.
- Netrpělivost jako jeden společný odpočet pro celou frontu místo vlastního pro každého cestujícího.
- Zapomenutý návrat lodi k molu po jízdě.

</details>

## Původ a zdroje

<details>
<summary>Zobrazit původ a zdroje</summary>

**Původ:** půlsemestrálky 2014–19 (přehled zadání), úloha Z18.

**Zdroje:**

- `Fitcheats/Půlsemestrálky/Zadání z minulých let/Přehled zadání 2014-19.pdf`, str. 4–5 (zadání; řešení v materiálech není)

**Existující řešení:**

- Řešení této úlohy v materiálech není. Síť vychází z Hrubého řešení příbuzné [11–04 – Výletní loď](<../11–04 - Výletní loď/11–04 - Výletní loď.md>): loď u mola jako zařízení pro nástup, čítač nastoupených, vyplutí `p=1` s hranou váhy 20.

</details>
