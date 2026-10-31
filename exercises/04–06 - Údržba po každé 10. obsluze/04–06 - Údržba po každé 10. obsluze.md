# 04–06 – Údržba po každé 10. obsluze

## Zadání

⚠️ Fotka zadání je hodně rozmazaná. Znění je přečtené z ní a ověřené ručním přepisem na str. 4 („M/M/1, kde transakce po každé 10 dokončené obsluze navíc zařadí blok údržby linky trvající C časových jednotek.“).

> 1. (15 bodů) Nakreslete Petriho síť pro systém M/M/1, kde transakce po každé desáté dokončené obsluze navíc zařadí blok údržby linky trvající C časových jednotek. S využitím notace knihovny SIMLIB napište pseudokód všech nezbytných částí simulačního modelu. Dbejte na izomorfní vztah mezi oběma modely.

Podobné úlohy:

- [04–02 – Automat na kávu – údržba po 50 obsluhách](<../04–02 - Automat na kávu – údržba po 50 obsluhách/04–02 - Automat na kávu – údržba po 50 obsluhách.md>): údržbu dělá automat po uvolnění
- [03–07 – Každá 10. transakce vyvolá poruchu](<../03–07 - Každá 10. transakce vyvolá poruchu/03–07 - Každá 10. transakce vyvolá poruchu.md>)
- [04–07 – Údržbář na obchůzce](<../04–07 - Údržbář na obchůzce/04–07 - Údržbář na obchůzce.md>): stejný termín, skupina C
- [10–01 – Server s údržbou po 1000 požadavcích](<../10–01 - Server s údržbou po 1000 požadavcích/10–01 - Server s údržbou po 1000 požadavcích.md>)

## Interpretace

<details>
<summary>Zobrazit interpretaci (nápověda)</summary>

- **Údržbu „zařadí transakce“:** desátá transakce po své obsluze linku neuvolní, ale drží ji ještě C jednotek na údržbu a teprve pak ji uvolní a odchází. V SIMLIBu by tedy transakce po obsluze započítala obsluhu a při desáté čekala C ještě před uvolněním linky. Izomorfní síť proto má uvolnění linky jako samostatný přechod *uvolnění* až po rozhodnutí o údržbě.
- **Čítač:** `exp(B)` dává značku do *počtu obsluh*. Přechod *10. obsluha* má z čítače hranu s váhou 10, takže se provede po každé desáté obsluze a čítač vynuluje.
- **Priorita `p=1`:** po obsluze je proveditelné i *uvolnění*. Priorita zajistí, že desátá transakce opravdu půjde do údržby.
- Po údržbě se transakce vrátí do místa *obslouženo*. Čítač je už prázdný, takže proběhne *uvolnění* a *odchod*.
- Druhá přípustná varianta: `exp(B)` vrací *Linku* jako obvykle a údržbu jako samostatný přechod s `p=1` spustí čítač (jako v [04–02](<../04–02 - Automat na kávu – údržba po 50 obsluhách/04–02 - Automat na kávu – údržba po 50 obsluhách.md>)). Linka je pak stejně dlouho mimo provoz, jen desátá transakce odchází hned. Izomorfní SIMLIB je ale složitější (proces údržby, který linku obsadí dřív než čekající transakce).
- C je konstanta, střední doby příchodů a obsluhy nejsou zadány, proto `exp(A)` a `exp(B)`. SIMLIB část otázky tu není řešená.

</details>

## Petriho síť

<details>
<summary>Zobrazit Petriho síť</summary>

![Petriho síť – údržba po každé 10. obsluze](net.svg)

| Požadavek | Prvek sítě |
|---|---|
| M/M/1 | *generátor* ⇄ `exp(A)` → *Fronta* → obsazení *Linky* → `exp(B)` → *obslouženo* → *uvolnění* (vrací *Linku*) → *odchod* |
| počítání dokončených obsluh | `exp(B)` → *počet obsluh* |
| po každé 10. obsluze údržba C | *10. obsluha* (`p=1`): *obslouženo* + 10 × *počet obsluh* → *údržba* → `C` → *obslouženo* |
| transakce opouští systém | *odchod* |

Kontrola simulací: *Linka* + obsluha + *obslouženo* + *údržba* = 1, v čítači je nejvýš 10 značek. Údržba proběhla přesně po každé desáté obsluze (9 523 údržeb na 95 237 obsluh).

</details>

## Časté chyby

<details>
<summary>Zobrazit časté chyby</summary>

- Hrana z čítače bez váhy 10, nebo jen testovací hrana s váhou 10, která čítač nevynuluje.
- Údržba bez priority vůči uvolnění (nebo vůči obsazení ve variantě s vracením linky): údržba se může posunout k pozdější obsluze.
- Linka vrácená z `exp(B)` a zároveň držená během údržby: vzniknou dvě značky linky.
- SIMLIB, který neodpovídá síti (např. údržba až po uvolnění linky, kdy už ji drží další transakce, zatímco síť ji drží během údržby).

</details>

## Původ a zdroje

**Původ:** zkouška 2022/23, 1. termín (11. 1. 2023), skupina D, otázka 1, 15 bodů.

**Zdroje:**

- `Fitcheats/Zkoušky z minulých let/2022-23 - 1. termín D.pdf`, str. 1 (malá rozmazaná fotka zadání) a str. 4 (ručně psaný přepis celé písemky)

**Existující řešení:**

<details>
<summary>Zobrazit existující řešení</summary>

- Ve zdrojích není žádné řešení této otázky.

</details>
