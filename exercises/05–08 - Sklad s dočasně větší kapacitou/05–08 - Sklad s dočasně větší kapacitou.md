# 05–08 – Sklad s dočasně větší kapacitou

## Zadání

⚠️ Fotka je malá a rozmazaná. Text níže je čtení po zvětšení výřezu. Jistá jsou čísla (500, 3, M/M/4, 100, 1) a většina slov. Méně jistá jsou slova na začátcích řádků vlevo a to, zda před „500“ nestojí „Exp“ (na fotce ho vidět není).

> 3. (10 bodů) Nakreslete Petriho síť pro systém typu M/M/1 s linkou typu Sklad. V intervalech daných 500 časových jednotek dojde k události, která obslužnou kapacitu linky rozšíří o 3 (tj. systém se změní na M/M/4) na dobu 100 časových jednotek (pak se kapacita vrátí na 1). Po ukončení doby 100 č.j. rozpracované obsluhy mohou normálně dokončit obsluhu.

Podobné úlohy: [05–10 – Pomocník přidá kapacitu](<../05–10 - Pomocník přidá kapacitu/05–10 - Pomocník přidá kapacitu.md>) (+1 jednotka na 20 č. j.), [05–02 – Dočasně MM2 při dlouhé frontě](<../05–02 - Dočasně MM2 při dlouhé frontě/05–02 - Dočasně MM2 při dlouhé frontě.md>) (rozšíření podle délky fronty), [09–08 – Cestovní kancelář](<../09–08 - Cestovní kancelář/09–08 - Cestovní kancelář.md>) (dvě přepážky navíc na 1 h).

## Interpretace

<details>
<summary>Zobrazit interpretaci (nápověda)</summary>

- **Linka typu Sklad** = místo s počtem značek rovným kapacitě (na začátku 1). Transakce bere jednu jednotku a obsluha ji vrací. Sklad tu zadání zmiňuje proto, že v SIMLIBu jde měnit kapacitu skladu (`SetCapacity`), v Petriho síti se kreslí stejně jako zařízení.
- **„V intervalech daných 500“** = konstanta: *generátor rozšíření* ve smyčce s přechodem `500`. Každé jeho provedení přidá do *Skladu* 3 značky (hrana s váhou 3) a značku do *M/M/4*.
- **Po 100 č. j.** přejdou 3 značky do *vrátit*. Každou z nich *odeber* (`p=1`) spáruje s jednou volnou jednotkou *Skladu* a obě zaniknou. Jednotky se tedy odebírají po jedné, jak se uvolňují: rozpracované obsluhy se dokončí („mohou normálně dokončit obsluhu“) a priorita `p=1` zajistí, že uvolněnou jednotku nestihne obsadit další transakce.
- *Odeber* nemá výstup: kapacita zanikne. Nejde o transakci, proto to není výstupní přechod. Stejně dobře by se jednotky mohly vracet do místa „rezerva“.
- Příchody a obsluhu zadání neuvádí, proto `exp(A)` a `exp(B)`.

</details>

## Řešení

<details>
<summary>Zobrazit řešení</summary>

![Petriho síť – sklad s dočasně větší kapacitou](net.svg)

| Požadavek | Prvek sítě |
|---|---|
| M/M/1 s linkou typu Sklad | *generátor* ⇄ `exp(A)` → *Fronta* → *Sklad* (1 značka) → `exp(B)` (vrací jednotku) → *odchod* |
| každých 500 č. j. kapacita +3 | *generátor rozšíření* ⇄ `500` → 3 značky do *Skladu* + *M/M/4* |
| na 100 č. j. | *M/M/4* → `100` → 3 značky do *vrátit* |
| návrat na kapacitu 1, rozpracované obsluhy doběhnou | *odeber* (`p=1`): *vrátit* + volná jednotka *Skladu* |
| transakce opouští systém | *odchod* |

Kontrola simulací (A = 10, B = 8): *Sklad* + obsluhované = 1 + 3 · *M/M/4* + *vrátit*. Rozšíření proběhne každých 500 č. j. a po každém se odeberou právě 3 jednotky.

</details>

## Časté chyby

<details>
<summary>Zobrazit časté chyby</summary>

- Odebrání všech tří jednotek najednou (hrana s váhou 3 ze *Skladu*): přechod čeká, až budou volné tři současně, a mezitím je dál obsazují nové transakce.
- Odebrání bez priority: uvolněnou jednotku může dřív obsadit čekající transakce a M/M/4 se protahuje.
- Přerušení rozpracovaných obsluh po 100 č. j. Zadání výslovně říká, že doběhnou.
- `exp(500)` místo konstanty 500 (zadání mluví o intervalech daných 500 časovými jednotkami).

</details>

## Původ a zdroje

**Původ:** zkouška 2017/18, 3. termín, skupina Z, otázka 3, 10 bodů (počet bodů je na fotce špatně čitelný).

**Zdroje:**

- `Fitcheats/Zkoušky z minulých let/2017-18 - 3. termín Z.pdf`, str. 1 (rozmazaná fotka zadání, 438 × 720 px)

**Existující řešení:**

<details>
<summary>Zobrazit existující řešení</summary>

- K této úloze v materiálech žádné řešení není.

</details>
