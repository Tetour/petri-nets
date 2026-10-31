# 04–02 – Automat na kávu – údržba po 50 obsluhách

## Zadání

> 1. (10 bodů) Nakreslete Petriho síť pro systém typu M/M/1 s obslužnou linkou "automat na kafe". Automat se po každých 50 cyklech provedené obsluhy přepne do režimu údržby (není k dispozici) na dobu přesně 20 časových jednotek.

Zkouška 2018/19 podle vzpomínky: „Automat na kávu, který po připravení X (40??) káv přejde do režimu údržby na dobu 20 časových jednotek.“

Podobné úlohy:

- [04–06 – Údržba po každé 10. obsluze](<../04–06 - Údržba po každé 10. obsluze/04–06 - Údržba po každé 10. obsluze.md>): údržbu provádí transakce, která linku ještě drží
- [10–01 – Server s údržbou po 1000 požadavcích](<../10–01 - Server s údržbou po 1000 požadavcích/10–01 - Server s údržbou po 1000 požadavcích.md>): stejný čítač, navíc se vyhazuje fronta
- [04–07 – Údržbář na obchůzce](<../04–07 - Údržbář na obchůzce/04–07 - Údržbář na obchůzce.md>)
- [04–01 – Automat na kávu – údržba po nečinnosti](<../04–01 - Automat na kávu – údržba po nečinnosti/04–01 - Automat na kávu – údržba po nečinnosti.md>)

## Interpretace

<details>
<summary>Zobrazit interpretaci (nápověda)</summary>
<br>

- **M/M/1:** *příchody zákazníků* ⇄ `exp(A)` → *fronta* → obsazení *Automatu* → `exp(B)`, které značku automatu vrací → *odchod*. Střední doby příchodů a obsluhy zadání neuvádí, proto `exp(A)` a `exp(B)`.
- **Čítač:** každá dokončená obsluha (`exp(B)`) přidá značku do místa *počet obsluh*. Přechod *do údržby* má z čítače hranu s váhou 50, takže se provede až po 50. obsluze a čítač zároveň vynuluje.
- **Údržba si vezme volný automat:** `exp(B)` vrací značku *Automatu*, *do údržby* si ji hned odebere a přesune do místa *údržba*. Pokud čeká zákazník, je v tu chvíli proveditelné i obsazení. Priorita `p=1` zajistí, že vyhraje údržba, takže přijde opravdu po každé 50. obsluze, ne až po některé další.
- Údržba nepřerušuje obsluhu: začíná vždy jen na volném automatu, tedy hned po 50. obsluze.
- **Údržba trvá 20** (pevná doba): *údržba* → `20` → zpět do *Automatu*. Zákazníci, kteří mezitím přijdou, čekají ve *frontě*.
- Počet 50 je podle fotky zadání 2017/18. Vzpomínka z roku 2018/19 má „X (40??)“, síť je stejná, jen s jinou vahou hrany.
- Zákazník po obsluze **opouští systém** přechodem *odchod*.

</details>

## Petriho síť

<details>
<summary>Zobrazit Petriho síť</summary>
<br>

![Petriho síť – automat na kávu s údržbou po 50 obsluhách](net.svg)

</details>

## Časté chyby

<details>
<summary>Zobrazit časté chyby</summary>
<br>

- Hrana z čítače bez váhy 50 (údržba po každé obsluze), nebo váha jen na testovací hraně, která čítač nevynuluje (údržba po každé obsluze od 50. dál).
- Čítání příchodů místo dokončených obsluh.
- Údržba bez priority: při čekajícím zákazníkovi může automat dostat on a údržba se posune o jednu nebo více obsluh.
- Údržba, která si nevezme značku *Automatu*. Pak automat během údržby dál obsluhuje.

</details>

## SIMLIB

<details>
<summary>Zobrazit SIMLIB kód</summary>
<br>

Model je izomorfní k Petriho síti výše: každé místo, přechod a značka mají svůj protějšek v kódu.

```cpp
// 04–02 Automat na kávu – údržba po 50 obsluhách – model v SIMLIB/C++
#include "simlib.h"

const double A = 10;                   // střední interval příchodů (zadání ho neuvádí)
const double B = 6;                    // střední doba obsluhy (zadání ji neuvádí)

Facility Automat("Automat");           // místo „Automat“ (1 značka) + fronta
Histogram Doba("Doba zákazníka v systému [č. j.]", 0, 5, 20);
int pocet = 0;                         // místo „počet obsluh“ (čítač)
int udrzeb = 0;                        // počet provedených údržeb

class Udrzba : public Process {        // přechod „do údržby“ → údržba → 20
  void Behavior() {
    Seize(Automat, 1);                 // p=1: automat dostane dřív než čekající zákazník
    udrzeb++;                          //   (zákazníka, kterému ho Release právě předal, vytlačí)
    Wait(20);                          // časovaný přechod 20 ...
    Release(Automat);                  // ... vrací značku do místa Automat
  }
};

class Zakaznik : public Process {      // transakce = značka, která prochází sítí
  void Behavior() {
    double prichod = Time;
    Seize(Automat);                    // fronta + obsazení
    Wait(Exponential(B));              // časovaný přechod exp(B) přidá značku do čítače
    if (++pocet == 50) {               // hrana s váhou 50: přechod „do údržby“
      pocet = 0;                       //   čítač vynuluje; údržba je naplánovaná před
      (new Udrzba)->Activate();        //   Release, poběží dřív než zákazník,
    }                                  //   kterému Release předá automat
    Release(Automat);                  // exp(B) vrací značku automatu
    Doba(Time - prichod);
  }                                    // konec Behavior = přechod „odchod“
};

class Generator : public Event {       // místo „příchody zákazníků“ ve smyčce s exp(A)
  void Behavior() {
    (new Zakaznik)->Activate();        // nová značka v místě „fronta“
    Activate(Time + Exponential(A));   // další příchod
  }
};

int main() {
  Init(0, 100000);                     // modelový čas v časových jednotkách
  (new Generator)->Activate();
  Run();
  Automat.Output();                    // vytížení = obsluha + údržba
  Doba.Output();
  Print("Počet údržeb: %d\n", udrzeb);
}
```

| Petriho síť | SIMLIB |
|---|---|
| *příchody zákazníků* ⇄ `exp(A)` | událost `Generator`, která se znovu plánuje za `Exponential(A)` |
| značka (zákazník) | proces `Zakaznik` |
| *fronta* + obsazení automatu | `Seize(Automat)` (fronta je vnitřní fronta zařízení) |
| časovaný přechod `exp(B)` se sloučeným uvolněním | `Wait(Exponential(B)); Release(Automat);` |
| místo *Automat* (1 značka) | `Facility Automat` |
| místo *počet obsluh*, hrana s váhou 50 | `int pocet`, `if (++pocet == 50) pocet = 0;` |
| *do údržby* (`p=1`) | proces `Udrzba`, `Seize(Automat, 1)` (priorita obsluhy) |
| *údržba* → `20` → *Automat* | `Wait(20); Release(Automat);` |
| přechod *odchod* | konec metody `Behavior()` |

**Kontrola simulací.** Petriho síť: *Automat* + obsluha + *údržba* = 1, v čítači je nejvýš 50 značek, údržba proběhla přesně po každé 50. obsluze (198 údržeb na 9 900 obsluh), fronta zůstává krátká (`make check`). SIMLIB model: v jednom běhu (100 000 č. j.) proběhlo 10 027 obsluh a 200 údržeb (10 027 / 50 = 200). Automat byl obsazený 64 % času; teoreticky 60 % obsluha (B/A = 6/10) a 4 % údržba (20 jednotek na 50 × 10 = 500 jednotek provozu). Ve 119 případech už automat po uvolnění dostal čekající zákazník a údržba ho vytlačila dřív, než jeho obsluha začala; ten pak čekal přesně 20 (fronta přerušených obsluh `Q2`), stejně jako by v síti čekal ve *frontě* (`make simlib`).

</details>

## Původ a zdroje

<details>
<summary>Zobrazit původ a zdroje</summary>
<br>

**Původ:** zkouška 2017/18, 2. termín, skupina C (hlavička je na fotce useknutá), otázka 1, 10 bodů. Stejná úloha (podle vzpomínky studenta, počet káv nejistý): zkouška 2018/19, 1. termín, otázka 1, 10 bodů.

**Původní znění:**

> 1. (10 bodů) Nakreslete Petriho síť pro systém typu M/M/1 s obslužnou linkou "automat na kafe". Automat se po každých 50 cyklech provedené obsluhy přepne do režimu údržby (není k dispozici) na dobu 20 časových jednotek.

**Zdroje:**

- `Fitcheats/Zkoušky z minulých let/2017-18 - 2. termín C.pdf`, str. 1 (fotka zadání)
- `Fitcheats/Zkoušky z minulých let/2018-19 - 1. termín.txt` (druhá vzpomínka v souboru)

**Existující řešení:**

- Ve zdrojích není žádné řešení. Stejný čítač s váhou hrany je v řešení půlsemestrálky [10–01 – Server s údržbou po 1000 požadavcích](<../10–01 - Server s údržbou po 1000 požadavcích/10–01 - Server s údržbou po 1000 požadavcích.md>).

</details>
