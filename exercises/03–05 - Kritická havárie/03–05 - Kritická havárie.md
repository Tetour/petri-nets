# 03–05 – Kritická havárie

## Zadání

> Zadaný systém modelujte prostředky Petriho sítě s vyznačením atributů na přechodech a místech. Vyznačte přechodem, kde transakce opouští systém.
>
> Uvažujme systém typu M/M/1. V intervalech exp(100) č.j. se na lince projeví kritická havárie, která linku na 10 č.j. zcela odstaví. Případná rozpracovaná obsluha je bez náhrady ukončena.

Podobné úlohy:

- [03–04 – Porucha s opravou, transakce odchází](<../03–04 - Porucha s opravou, transakce odchází/03–04 - Porucha s opravou, transakce odchází.md>): stejná úloha se symboly (2021/22)
- [03–03 – Porucha s opravou, návrat do fronty](<../03–03 - Porucha s opravou, návrat do fronty/03–03 - Porucha s opravou, návrat do fronty.md>): přerušená transakce se vrací do fronty
- [03–01 – Porucha zruší obsluhu](<../03–01 - Porucha zruší obsluhu/03–01 - Porucha zruší obsluhu.md>): bez odstávky

## Interpretace

<details>
<summary>Zobrazit interpretaci (nápověda)</summary>

- **„Linku na 10 č.j. zcela odstaví“:** havárie si vezme značku *Linky* a vrátí ji po 10 č.j., ať linka zrovna obsluhuje, nebo ne.
- **„Rozpracovaná obsluha je bez náhrady ukončena“:** přerušená transakce se neobslouží a odchází ze systému. Zadání chce vyznačit odchod přechodem, a odchody jsou tu dva: *odchod* po obsluze a *odchod bez obsluhy*.
- **Dva kroky:** přechod `p=1` dole ukončí obsluhu, vrátí *Linku* a havárii nechá v místě *havárie* (hrana tam a zpět). Přechod `p=1` nahoře pak havárii spojí s volnou *Linkou* a začne odstávka. Při volné lince se provede rovnou horní přechod. Priorita nahoře zajistí, že linku nezabere transakce čekající ve *Frontě*.
- **Havárie během odstávky** počká a linku odstaví znovu hned po skončení odstávky. Při exp(100) a odstávce 10 je to vzácné. Pokud by měla zaniknout, přidá se přechod *porucha bez účinku* s `p=0` jako v 03–02.
- Časy příchodů a obsluhy zadání neuvádí, proto `exp(A)` a `exp(B)`. „Atributy na místech“ jsou názvy míst a počáteční značky.

</details>

## Petriho síť

<details>
<summary>Zobrazit Petriho síť</summary>

![Petriho síť – kritická havárie](net.svg)

| Požadavek | Prvek sítě |
|---|---|
| M/M/1 | *generátor* ⇄ `exp(A)` → *Fronta* → obsazení *Linky* → `exp(B)` (vrací *Linku*) → *odchod* |
| havárie v intervalech exp(100) | *generátor havárií* ⇄ `exp(100)` → *havárie* |
| rozpracovaná obsluha je bez náhrady ukončena | `p=1` dole: *havárie* (zůstává) + obsluhovaná transakce → *Linka* + *zrušená* → *odchod bez obsluhy* |
| linka je na 10 č.j. odstavena | `p=1` nahoře: *havárie* + *Linka* → *odstávka* → `10` → *Linka* |
| kde transakce opouští systém | *odchod*, *odchod bez obsluhy* |

Kontrola simulací: *Linka* + obsluhovaná transakce + *odstávka* = 1, každá havárie vede k jedné odstávce a zhruba polovina havárií ukončí rozpracovanou obsluhu.

</details>

## Časté chyby

<details>
<summary>Zobrazit časté chyby</summary>

- Havárie jen ukončí obsluhu, ale linku neodstaví (chybí doba 10).
- Odstávka jen při obsazené lince: volnou linku havárie neodstaví a hned může začít další obsluha.
- Ukončená transakce se vrací do fronty: to by byla náhrada (úloha 03–03).
- Chybí výstupní přechod pro ukončenou transakci (zadání ho výslovně chce).
- Linka se po odstávce nevrátí.

</details>

## Původ a zdroje

**Původ:** zkouška 2025/26, 1. termín (13. 1. 2026), skupina C, otázka 1, 10 bodů.

**Zdroje:**

- `Fitcheats/Zkoušky z minulých let/2025-26 - 1. termín C.pdf`, str. 1 (fotka zadání)

**Existující řešení:**

<details>
<summary>Zobrazit existující řešení</summary>

- K tomuto zadání žádné řešení není. Stejnou úlohu se symboly řeší fifinas (str. 2), viz [03–04 – Porucha s opravou, transakce odchází](<../03–04 - Porucha s opravou, transakce odchází/03–04 - Porucha s opravou, transakce odchází.md>).

</details>
