# 08–06 – D/D/4 s LIFO frontou, obsluha 7 s, značení v čase 9,5

## Zadání

> ⚠️ Jen studentská vzpomínka, původní zadání v podkladech není.

> pseudokód Next-event (-5b pokud chybí)
>
> D/D/4 s LIFO, doba obsluhy = 7s
>
> \- nakreslit diagram +
>
> a) seznam všech událostí v čase 7 (ve správném pořadí)\
> b) obsah kalendáře v čase t = 9,5 (-5b pokud chybí)\
> c) obsah LIFO v čase t = 9,5\
> d) petriho síť v čase t = 9,5

Podobné úlohy: [08–02 – DD3 LIFO, čas 10,5](<../08–02 - DD3 LIFO, čas 10,5/08–02 - DD3 LIFO, čas 10,5.md>), [08–07 – DD3 FIFO, čas 9,5](<../08–07 - DD3 FIFO, čas 9,5/08–07 - DD3 FIFO, čas 9,5.md>), [08–04 – DD2 LIFO obsluha 5, čas 9,5](<../08–04 - DD2 LIFO obsluha 5, čas 9,5/08–04 - DD2 LIFO obsluha 5, čas 9,5.md>). Zkouška 2014/15, 2. termín měla „D/D/4 klasika“ s popisem událostí v čase 4 včetně plánování; čísla ani síť vzpomínka neuvádí.

## Interpretace

<details>
<summary>Zobrazit interpretaci (nápověda)</summary>

- **Interval příchodů ve vzpomínce chybí.** Předpokládá se šablona ostatních zadání: příchody od času 0 po **1 s**, požadavky číslované od P0, zařízení Z0–Z3 obsazovaná prioritně (nižší číslo dřív), všechny události se stejnou prioritou.
- **Petriho síť zachycuje jen počty**, ne pořadí ve frontě. LIFO se v síti neprojeví, projeví se jen v seznamu událostí a v obsahu fronty.
- **Zařízení obsazovaná prioritně:** čtyři okamžité přechody s prioritami `p=3` (Z0), `p=2` (Z1), `p=1` (Z2) a `p=0` (Z3, implicitní).
- **Pořadí událostí ve stejném čase:** dřív se provede událost, která byla **dřív naplánována**. V čase 7 nejdřív končí obsluha P0 (naplánovaná v čase 0), až pak přichází P7 (naplánovaný v čase 6). Proto Z0 dostane P6 a P7 jde do fronty.

</details>

## Petriho síť

<details>
<summary>Zobrazit Petriho síť</summary>

### Časový diagram (obsazení zařízení)

| zařízení | obsluhy |
|---|---|
| Z0 | P0 0–7, P6 7–14 |
| Z1 | P1 1–8, P7 8–15 |
| Z2 | P2 2–9, P8 9–16 |
| Z3 | P3 3–10 |

Fronta: P4 a P5 čekají od 4 a 5 (pod nimi se střídají novější). P6 jde v 7 na Z0, P7 v 8 na Z1, P8 v 9 na Z2, P9 čeká od 9.

### Události provedené v čase 7

1. P0 uvolňuje Z0 a odchází
2. P6 vystupuje z fronty (LIFO – poslední) a obsazuje Z0; plánuje konec obsluhy P6 na Z0 v čase 14
3. příchod P7; plánuje příchod P8 v čase 8
4. P7 jde do fronty

Proč toto pořadí: konec obsluhy P0 byl naplánován v čase 0, příchod P7 až v čase 6. Při stejné prioritě rozhoduje pořadí naplánování.

### Kalendář v čase 9,5

| čas | událost |
|---|---|
| 10 | konec obsluhy P3 na Z3 (naplánováno v čase 3) |
| 10 | příchod P10 (naplánováno v čase 9) |
| 14 | konec obsluhy P6 na Z0 |
| 15 | konec obsluhy P7 na Z1 |
| 16 | konec obsluhy P8 na Z2 |

Obsah LIFO v čase 9,5 (od dna): P4, P5, P9 (na vrcholu P9, ten půjde ven první). Zařízení: Z0 – P6, Z1 – P7, Z2 – P8, Z3 – P3.

### Petriho síť se značením v čase 9,5

![Petriho síť – D/D/4 v čase 9,5](net.svg)

- *generátor*: 1 značka (příchod P10 se právě odpočítává)
- *Fronta*: 3 značky (P4, P5, P9)
- *Z0* až *Z3*: 0 značek (všechna zařízení obsazená)
- místa obsluhy: po 1 značce (P6, P7, P8, P3)

Kontrola (`make check`): síť se odsimuluje od času 0 (P0 ve frontě, zařízení volná) do času 9,5 a výsledné značení se musí shodovat s nakresleným. Výpočet událostí a kalendáře: `python3 -m pn.dd 4 lifo 1 7 7 9.5`.

</details>

## Časté chyby

<details>
<summary>Zobrazit časté chyby</summary>

- Zapomenutý P3 na Z3: obsluha 3–10 v čase 9,5 ještě běží, takže v kalendáři je jeho konec v čase 10.
- V kalendáři obráceně dvě události v čase 10. Konec obsluhy P3 byl naplánován v čase 3, příchod P10 v čase 9.
- Opačné pořadí v čase 7 (nejdřív příchod P7). Pak by P7 obsadil Z0 a ve frontě by zůstal P6.
- Stejná priorita na všech přechodech obsazení. Pak síť nevyjadřuje, že se zařízení obsazují od Z0.

</details>

## Původ a zdroje

<details>
<summary>Zobrazit původ a zdroje</summary>

**Původ:** zkouška 2014/15, 3. termín, skupina D (podle studenta „asi“), otázka 1, 15 bodů.

**Zdroje:**

- `Fitcheats/Zkoušky z minulých let/2014-15 - 3. termín.txt`, otázka 1 (studentská vzpomínka)

**Existující řešení:**

- K této úloze řešení v podkladech není. Síť má stejný tvar jako studentská řešení úlohy [08–02](<../08–02 - DD3 LIFO, čas 10,5/08–02 - DD3 LIFO, čas 10,5.md>), jen se čtyřmi zařízeními a prioritami 3, 2, 1, 0.

</details>
