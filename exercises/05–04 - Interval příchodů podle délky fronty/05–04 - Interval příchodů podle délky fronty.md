# 05–04 – Interval příchodů podle délky fronty

## Zadání

> Nakreslete Petriho síť pro systém M/M/1, kde se po každé nově příchozí transakci přehodnotí interval mezi příchody transakcí do systému podle následujícího předpisu: 1) pokud je aktuální délka fronty (včetně nově příchozího) větší nebo rovna počtu C, pak je střední doba mezi příchody nastavena na A časových jednotek, 2) jinak B časových jednotek. S využitím notace knihovny SIMLIB napište pseudokód všech nezbytných částí simulačního modelu. Dbejte na izomorfní vztah mezi oběma modely.

⚠️ 2021/22, skupina C, jen ze vzpomínky (slovensky): „M/M/1. Ak je vo fronte aspon C transakcii, tak generuje transakcie s exp(A), inak s exp(B). + SIMLIB.“

Podobné úlohy: [05–05 – Přerušení příchodů při plné frontě](<../05–05 - Přerušení příchodů při plné frontě/05–05 - Přerušení příchodů při plné frontě.md>) (příchody se při dlouhé frontě zastaví), [05–01 – Doba obsluhy podle délky fronty](<../05–01 - Doba obsluhy podle délky fronty/05–01 - Doba obsluhy podle délky fronty.md>) (podle fronty se mění obsluha).

## Interpretace

<details>
<summary>Zobrazit interpretaci (nápověda)</summary>

- **Kdy se rozhoduje:** jen při příchodu („po každé nově příchozí transakci“). Zvolený interval platí až do dalšího příchodu, i když se fronta mezitím zkrátí. Značka generátoru proto po příchodu přejde do místa *po příchodu* a odtud jedním ze dvou přechodů do *intervalu A*, nebo do *intervalu B*. Každý z nich má svůj časovaný přechod (jeden přechod = jeden čas).
- **„Fronta ≥ C“** testuje dvojice hran s váhou C (do přechodu a zpět). *Jinak* (`p=0`) žádný test nepotřebuje, provede se, jen když *fronta ≥ C* (`p=1`) proveditelná není. Inhibiční hrana tu tedy není potřeba.
- **„Včetně nově příchozího“:** časovaný příchod dá značku do *Fronty* a do *po příchodu* zároveň, takže se nově příchozí do fronty počítá. Priorita `p=1` navíc zajistí, že test proběhne dřív než obsazení linky (`p=0`).
- Na začátku je fronta prázdná, proto je značka generátoru v *intervalu B*.
- Doba obsluhy v zadání není, proto `exp(S)`.
- Přepis z roku 2021/22 by šel číst i tak, že se rychlost generátoru přepíná průběžně podle aktuální fronty. Oficiální znění z roku 2022/23 to vyjasňuje: rozhoduje se jen při příchodu.
- SIMLIB část otázky tu není řešená.

</details>

## Petriho síť

<details>
<summary>Zobrazit Petriho síť</summary>

![Petriho síť – interval příchodů podle délky fronty](net.svg)

| Požadavek | Prvek sítě |
|---|---|
| po každém příchodu přehodnotit interval | `exp(A)` i `exp(B)` vracejí značku generátoru do *po příchodu* |
| fronta (včetně nově příchozího) ≥ C → střední doba A | *fronta ≥ C* (`p=1`, test C na *Frontě*) → *interval A* ⇄ `exp(A)` |
| jinak B | *jinak* (`p=0`) → *interval B* ⇄ `exp(B)` |
| M/M/1 | *Fronta* → obsazení *Linky* → `exp(S)` (vrací *Linku*) → *odchod* |
| transakce opouští systém | *odchod* |

Kontrola simulací (A = 20, B = 5, C = 5, S = 8): *Linka* + obsluhovaná transakce = 1, značka generátoru je vždy právě v jednom ze tří míst. Pomalejší příchody `exp(A)` se volí asi u čtvrtiny příchodů. Fronta zůstává omezená, i když by ji samotné příchody `exp(B)` při obsluze `exp(8)` neudržely.

</details>

## Časté chyby

<details>
<summary>Zobrazit časté chyby</summary>

- Jeden časovaný přechod se dvěma časy (`exp(A)` / `exp(B)`). Časovaný přechod má jen jeden čas, proto jsou tu dva.
- Přepínání režimu generátoru průběžně, testem fronty kdykoli (i mezi příchody). Rozhodnutí patří jen k okamžiku příchodu.
- Test fronty jen hranou dovnitř: rozhodnutí by z fronty odebralo C transakcí.
- Větev *jinak* bez nižší priority: při dlouhé frontě by se náhodně volil i interval B.

</details>

## Původ a zdroje

<details>
<summary>Zobrazit původ a zdroje</summary>

**Původ:** zkouška 2022/23, 1. termín, skupina A, otázka 1, 15 bodů. Stejná úloha (jen ze vzpomínky): zkouška 2021/22, 1. termín, skupina C, otázka 1.

**Zdroje:**

- `Fitcheats/Zkoušky z minulých let/2022-23 - 1. termín A.pdf`, str. 1 (fotky zadání)
- `Fitcheats/Zkoušky z minulých let/2021-22 - 1. termín.txt`, skupina C, otázka 1 (studentský přepis zadání)
- `Fitcheats/Příprava na zkoušku/fifinas - Tabule ze streamu.pdf`, str. 4 (síť a kód v SIMLIBu na tabuli)

**Existující řešení:**

- **fifinas, str. 4:** dva generátory (černé místo se značkou a `Exp(b)`, zelené místo s `Exp(a)`), mezi nimiž se značka přesouvá. K tomu červené a modré přechody s prioritami `p=2` a `p=1` a hranami s váhou C na frontě. Tabule je silně přemalovaná a přesné napojení hran se nedá spolehlivě přečíst. Kód v SIMLIBu volí interval v chování generátoru: aktivuje novou transakci, otestuje délku fronty linky `>= C` a podle toho se naplánuje za `Exp(A)`, nebo `Exp(B)`. Rozhoduje tedy jen při příchodu, jako tady. Nově aktivovaná transakce se ale do fronty zařadí až po skončení chování generátoru, takže se do délky fronty nezapočítá. Podmínka „včetně nově příchozího“ by vyžadovala test `>= C - 1`.

</details>
