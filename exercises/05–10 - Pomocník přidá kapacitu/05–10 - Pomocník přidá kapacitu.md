# 05–10 – Pomocník přidá kapacitu

## Zadání

> Mějme systém M/M/1. V intervalech exponenciálně se středem 100 časových jednotek přichází dobrotivý správce linky, který na dobu 20 časových jednotek pomáhá s obsluhou tak, že poskytuje lince další jednu jednotku kapacity (systém je pak M/M/2). Zadaný systém modelujte prostředky Petriho sítě.

Podobné úlohy: [05–09 – Údržba zabere celou kapacitu](<../05–09 - Údržba zabere celou kapacitu/05–09 - Údržba zabere celou kapacitu.md>) (sesterská skupina E téhož termínu), [05–08 – Sklad s dočasně větší kapacitou](<../05–08 - Sklad s dočasně větší kapacitou/05–08 - Sklad s dočasně větší kapacitou.md>) (+3 jednotky na 100 č. j.), [05–02 – Dočasně MM2 při dlouhé frontě](<../05–02 - Dočasně MM2 při dlouhé frontě/05–02 - Dočasně MM2 při dlouhé frontě.md>).

## Interpretace

<details>
<summary>Zobrazit interpretaci (nápověda)</summary>
<br>

- **M/M/1:** *příchody zákazníků* ⇄ `exp(A)` → *Fronta* → obsazení *Linky* → `exp(B)`, který jednotku vrací → *konec* → *odchod*. Příchody a obsluhu zákazníků zadání neuvádí, proto `exp(A)` a `exp(B)`.
- **Správce je jeden člověk:** jedna značka koluje mezi *správce jinde*, *pomáhá* a *končí*. Další příchod tak nastane až poté, co odejde, a systém je nejvýš M/M/2, jak zadání říká. Generátor ve smyčce by mohl poslat druhého správce, zatímco první ještě pomáhá (vzniklo by M/M/3). Interval `exp(100)` se tu proto měří od jeho odchodu.
- **Pomoc = jednotka kapacity navíc:** příchod správce přidá do *Linky* druhou značku. Obsluha je pořád `exp(B)`, jen mohou běžet dvě najednou.
- **Konec pomoci po 20 č. j.:** *pomáhá* → `20` → *končí*. Jednotku nejde vzít, dokud na ní běží obsluha. *Odchod správce* (`p=1`) proto vezme první volnou jednotku dřív, než ji obsadí další transakce, a vrátí správce do *správce jinde*. Rozpracovaná obsluha se normálně dokončí. Zadání to výslovně neříká, ale odejít uprostřed obsluhy by znamenalo vrátit zákazníka do fronty a to by zadání asi zmínilo.
- Jednotky kapacity se nerozlišují, správce tedy „odnese“ kteroukoli volnou.

</details>

## Petriho síť

<details>
<summary>Zobrazit Petriho síť</summary>
<br>

![Petriho síť – pomocník přidá kapacitu](net.svg)

</details>

## Časté chyby

<details>
<summary>Zobrazit časté chyby</summary>
<br>

- Časovaný přechod `20` se vstupem z *Linky*: jednotka by během odpočtu čekala v *Lince*, první zákazník by ji obsadil a odpočet zrušil.
- Odebrání jednotky bez priority: uvolněnou jednotku může dřív obsadit čekající zákazník a pomoc se protáhne.
- Přidání jednotky bez jejího odebrání (kapacita roste s každým příchodem správce).
- Generátor správce ve smyčce: při překryvu dvou návštěv vznikne M/M/3.

</details>

## SIMLIB

<details>
<summary>Zobrazit SIMLIB kód</summary>
<br>

Model je izomorfní k Petriho síti výše: každé místo, přechod a značka mají svůj protějšek v kódu. Hodnoty `A = 5` a `B = 4` jsou doplněné, zadání je nedává. Linka je `Store` s pevnou kapacitou 2 a druhou jednotku má u sebe proces `Spravce`, když je jinde. Přesně tak to říká invariant sítě *Linka* + obsluhovaní + *správce jinde* = 2. `SetCapacity` tu nestačí: kapacitu nezmenší, dokud někdo čeká ve frontě (SIMLIB skončí chybou), a po zvětšení čekající sama nepustí.

```cpp
// 05–10 Pomocník přidá kapacitu – model v SIMLIB/C++
#include "simlib.h"

const double A = 5;                    // střední interval příchodů exp(A), zadání ho nedává
const double B = 4;                    // střední doba obsluhy exp(B), zadání ji nedává

Store Linka("Linka", 2);               // místo Linka: 2 jednotky, jednu má správce u sebe
int navstev = 0;                       // počet provedení přechodu exp(100)

class Spravce : public Process {       // značka správce: jinde → pomáhá → končí → jinde
  void Behavior() {
    Enter(Linka, 1);                   // správce jinde: druhá jednotka není v Lince
    for (;;) {
      Wait(Exponential(100));          // správce jinde → exp(100)
      navstev++;
      Leave(Linka, 1);                 // přidá jednotku do Linky (M/M/2), pomáhá
      Wait(20);                        // pomáhá → 20 → končí
      Enter(Linka, 1);                 // odchod správce (p=1): první volná jednotka
    }
  }
 public:
  Spravce() : Process(1) {}            // priorita 1: ve frontě Linky předběhne zákazníky
};

class Zakaznik : public Process {      // transakce = značka, která prochází sítí
  void Behavior() {
    Enter(Linka, 1);                   // Fronta + obsazení (bere jednotku Linky)
    Wait(Exponential(B));              // časovaný přechod exp(B) ...
    Leave(Linka, 1);                   // ... který jednotku vrací
  }                                    // konec Behavior = konec + odchod
};

class Generator : public Event {       // místo „příchody zákazníků“ ve smyčce s exp(A)
  void Behavior() {
    (new Zakaznik)->Activate();        // nová značka ve Frontě
    Activate(Time + Exponential(A));   // další příchod
  }
};

int main() {
  Init(0, 1000000);                    // modelový čas v časových jednotkách
  (new Spravce)->Activate();           // nejdřív správce, ať si vezme druhou jednotku
  (new Generator)->Activate();
  Run();
  Linka.Output();                      // obsazenost včetně jednotky u správce
  Print("Návštěv správce: %d (jednou za %.1f časových jednotek)\n", navstev, Time / navstev);
}
```

| Petriho síť | SIMLIB |
|---|---|
| *příchody zákazníků* ⇄ `exp(A)` | událost `Generator`, která se znovu plánuje za `Exponential(A)` |
| značka (zákazník) | proces `Zakaznik` |
| místo *Linka* (1 značka, se správcem 2) | `Store Linka("Linka", 2)`, druhou jednotku drží `Spravce`, když je jinde |
| *Fronta* + obsazení | `Enter(Linka, 1)` (fronta je vnitřní fronta skladu) |
| `exp(B)` se sloučeným uvolněním | `Wait(Exponential(B)); Leave(Linka, 1);` |
| značka správce (*jinde*, *pomáhá*, *končí*) | proces `Spravce` (jen jeden) |
| *správce jinde* → `exp(100)` → jednotka do *Linky* + *pomáhá* | `Wait(Exponential(100)); Leave(Linka, 1);` |
| *pomáhá* → `20` → *končí* | `Wait(20)` |
| *odchod správce* (`p=1`): *končí* + volná jednotka → *správce jinde* | `Enter(Linka, 1)` s prioritou procesu 1 (ve frontě skladu je první) |
| *konec* → *odchod* | konec metody `Behavior()` zákazníka |

**Kontrola simulací.** Petriho síť: *Linka* + obsluhovaní + *správce jinde* = 2 a správce je vždy právě v jednom ze tří míst; všechny přechody se provádějí (`make check`). Pomáhá asi 400krát za 10 000 transakcí, tedy zhruba jednou za 120 č. j. SIMLIB model: v jednom běhu (10⁶ časových jednotek) přišel správce 8357krát, jednou za 120 časových jednotek (100 jinde + 20 pomoc + krátké čekání na volnou jednotku). Fronta měla nejvýš 27 a průměrně 1,7 čekajících (`make simlib`).

</details>

## Původ a zdroje

<details>
<summary>Zobrazit původ a zdroje</summary>
<br>

**Původ:** zkouška 2025/26, 2. termín (27. 1. 2026), skupina F, otázka 1, 10 bodů.

**Původní znění:**

> Mějme systém M/M/1. V intervalech exp(100 č.j.) přichází dobrotivý správce linky, který na dobu 20 č.j. pomáhá s obsluhou tak, že poskytuje lince další jednu jednotku kapacity (systém je pak M/M/2). Zadaný systém modelujte prostředky Petriho sítě.

**Zdroje:**

- `Fitcheats/Zkoušky z minulých let/2025-26 - 2. termín F.pdf`, str. 1 (fotka zadání, bez řešení)

**Existující řešení:**

- K této úloze v materiálech žádné řešení není.

</details>
