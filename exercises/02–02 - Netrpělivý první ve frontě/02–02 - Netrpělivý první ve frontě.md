# 02–02 – Netrpělivý první ve frontě

## Zadání

> Mějme SHO typu M/M/1. Fronta k lince má to specifikum, že transakce, která je první ve frontě, je netrpělivá, takže po 4 časových jednotkách čekání frontu (a systém celkově) opouští. Systém modelujte Petriho sítí.

2019/20, skupina Y: „Systém typu M/M/1 s tím specifikem, že vždy transakce, která je prvním prvkem fronty, je netrpělivá a po X časových jednotkách čekání opouští systém.“

⚠️ Zadání 2017/18 je jen ze vzpomínky studenta (slovensky): „Petriho siet m/m/1 (automat na kafe). Fronta bola specificka tym, ze vzdy jej prvy clen je netrpezlivy, a ak nedostane linku do 5 casovych jednotiek, opusta system. (bola tam napoveda, ze sa da fronta rozlozit do 2 miest PS).“

Podobné úlohy: [02–01 – Netrpělivé požadavky](<../02–01 - Netrpělivé požadavky/02–01 - Netrpělivé požadavky.md>) (netrpěliví jsou všichni čekající), [09–20 – Pražírna kávy](<../09–20 - Pražírna kávy/09–20 - Pražírna kávy.md>) (stejný mechanismus ve slovní úloze).

## Interpretace

<details>
<summary>Zobrazit interpretaci (nápověda)</summary>
<br>

- **M/M/1:** *příchody transakcí* ⇄ `exp(A)` → *Fronta* → … → obsazení *Linky* → `exp(B)`, který *Linku* vrací → *konec* → *odchod*. Příchody a obsluha nemají čísla, proto `exp(A)` a `exp(B)`.
- **Fronta rozdělená do dvou míst** (nápověda z roku 2017/18): *Fronta* pro ostatní čekající a *První* pro transakci v čele. Přechod *postup* přesouvá transakci z *Fronty* do *První*. Časovaný přechod `4` visí jen na místě *První*. Kdyby visel na *Frontě*, měl by vlastní odpočet každý čekající (slajd 138) a šlo by o [02–01](<../02–01 - Netrpělivé požadavky/02–01 - Netrpělivé požadavky.md>).
- **Doplněk *1. místo volné*** (1 značka) zajistí, že v *První* je nejvýš jedna transakce. *Postup* jeho značku bere; bez něj by *postup* přesunul do *První* celou frontu.
- Značku doplňku vrací **obsazení linky** (obsluhovaná transakce už ve frontě není a v čele je hned další) a **netrpělivý odchod**.
- **Odpočet začíná, až se transakce dostane do čela.** Na „4 časové jednotky čekání“ se počítá jen čekání v čele, předchozí čekání ve *Frontě* ne. Jiné čtení (celková doba čekání) se v Petriho síti modeluje špatně a nápověda o dvou místech míří na toto řešení.
- Když je linka volná, transakce projde *První* a obsadí linku ve stejném okamžiku. Odpočet se vůbec nerozběhne.
- **Po 4 jednotkách v čele** přechod *netrpělivost* vezme transakci z *První*, vrátí značku *1. místo volné* a transakce opouští systém vlastním výstupním přechodem *odchod bez obsluhy*. Vést netrpělivost do místa *konec* a odejít společným přechodem *odchod* by bylo také správně, jen by se v nákresu musely křížit hrany.
- Doba je pevná: `4` (2017/18: `5`, 2019/20: `X`).

</details>

## Petriho síť

<details>
<summary>Zobrazit Petriho síť</summary>
<br>

![Petriho síť – netrpělivý první ve frontě](net.svg)

</details>

## Časté chyby

<details>
<summary>Zobrazit časté chyby</summary>
<br>

- Časovač přímo na *Frontě*: netrpěliví jsou pak všichni čekající, ne jen první.
- Místo *První* bez doplňku: do čela se přesune celá fronta a odpočet běží všem.
- Značka doplňku vrácená až koncem obsluhy: během obsluhy pak v čele nikdo není a čekající nejsou netrpěliví vůbec.
- Netrpělivý odchod, který nevrátí značku doplňku: čelo fronty se zablokuje a síť se zastaví.
- Časovač za obsazením linky (omezuje obsluhu, ne čekání).

</details>

## SIMLIB

<details>
<summary>Zobrazit SIMLIB kód</summary>
<br>

Model je izomorfní k Petriho síti výše: každé místo, přechod a značka mají svůj protějšek v kódu. Hodnoty `A = 5` a `B = 4` jsou doplněné, zadání je nedává.

```cpp
// 02–02 Netrpělivý první ve frontě – model v SIMLIB/C++
#include "simlib.h"

const double A = 5;                    // střední interval příchodů exp(A)
const double B = 4;                    // střední doba obsluhy exp(B)
const double TRPELIVOST = 4;           // přechod „netrpělivost“ (pevná doba)

Facility Linka("Linka");               // místo Linka s jednou značkou
Store Celo("1. místo volné", 1);       // doplněk místa První (1 značka)
int obslouzeno = 0, netrpelivych = 0;  // počty provedení přechodů odchod a odchod bez obsluhy

class Netrpelivost : public Event {    // časovaný přechod „netrpělivost“ na místě První
  Process *transakce;                  // čí odpočet to je
 public:
  Netrpelivost(Process *t) : transakce(t) { Activate(Time + TRPELIVOST); }
  void Behavior() {
    netrpelivych++;
    transakce->Cancel();               // vezme značku z místa První (vyjme ji z fronty Linky): odchod bez obsluhy
    Celo.Leave(1);                     // ... a vrací značku do místa 1. místo volné
  }
};

class Transakce : public Process {     // transakce = značka, která prochází sítí
  void Behavior() {
    Enter(Celo, 1);                    // Fronta + postup (bere značku 1. místo volné) → místo První
    Event *netrp = new Netrpelivost(this);  // odpočet 4 běží jen v místě První
    Seize(Linka);                      // obsazení (bere značku Linky) ...
    delete netrp;                      // ... vzalo značku z místa První, odpočet zaniká
    Leave(Celo, 1);                    // ... a vrací značku do 1. místo volné
    Wait(Exponential(B));              // časovaný přechod exp(B) ...
    Release(Linka);                    // ... který vrací značku Lince
    obslouzeno++;
  }                                    // konec Behavior = místo konec + přechod odchod
};

class Generator : public Event {       // místo „příchody transakcí“ ve smyčce s exp(A)
  void Behavior() {
    (new Transakce)->Activate();       // nová značka v místě Fronta
    Activate(Time + Exponential(A));   // další příchod
  }
};

int main() {
  Init(0, 1000000);                    // modelový čas v časových jednotkách
  (new Generator)->Activate();
  Run();
  Celo.Output();                       // fronta Store = místo Fronta
  Linka.Output();                      // fronta Facility = místo První
  Print("Obslouženo: %d, odešlo bez obsluhy: %d (%.1f %%)\n", obslouzeno, netrpelivych,
        100.0 * netrpelivych / (obslouzeno + netrpelivych));
}
```

| Petriho síť | SIMLIB |
|---|---|
| *příchody transakcí* ⇄ `exp(A)` | událost `Generator`, která se znovu plánuje za `Exponential(A)` |
| značka (transakce) | proces `Transakce` |
| *1. místo volné* (1 značka) | `Store Celo(1)`; `Store`, ne `Facility`, protože značku vrací i událost netrpělivosti, ne jen proces, který ji vzal |
| *Fronta* + *postup* | `Enter(Celo, 1)` (*Fronta* je vnitřní fronta skladu `Celo`) |
| místo *První* + obsazení *Linky* | `Seize(Linka)` (*První* je vnitřní fronta linky, díky `Celo` v ní je nejvýš jedna transakce) |
| odpočet *netrpělivost* `4` pro značku v *První* | událost `Netrpelivost`, naplánovaná po vstupu do *První* |
| obsazení vezme značku z *První* a vrací doplněk | `delete netrp; Leave(Celo, 1);` hned po `Seize` |
| provedení *netrpělivosti* | `transakce->Cancel(); Celo.Leave(1);` |
| místo *Linka* (1 značka), `exp(B)` se sloučeným uvolněním | `Facility Linka`, `Wait(Exponential(B)); Release(Linka);` |
| *konec* → *odchod*, *odchod bez obsluhy* | konec `Behavior()`, resp. `Cancel()`; počítadla `obslouzeno`, `netrpelivych` |

**Kontrola simulací.** Petriho síť: *Linka* + obsluhovaná transakce = 1, *1. místo volné* + *První* = 1, všechny přechody se provádějí (`make check`); při `A = 5`, `B = 4` odešlo bez obsluhy 22,8 % transakcí. SIMLIB model: v jednom běhu (10⁶ časových jednotek) také 22,8 %, ve frontě linky (místo *První*) nikdy nečekala víc než jedna transakce a linka byla vytížena na 61,7 %, což odpovídá 0,2 · (1 − 0,228) · 4 = 61,8 % (`make simlib`).

</details>

## Původ a zdroje

<details>
<summary>Zobrazit původ a zdroje</summary>
<br>

**Původ:** zkouška 2024/25, 2. termín (20. 1. 2025), skupina E, otázka 3, 10 bodů. Stejná úloha (jiná čísla): zkouška 2019/20, 2. termín, skupina Y, otázka 3, 10 bodů (X č. j.) a zkouška 2017/18, 2. termín, skupina A, otázka 1, 10 bodů (automat na kávu, 5 jednotek).

**Původní znění** (2019/20, skupina Y):

> Systém typu M/M/1 s tím specifikem, že vždy transakce, která je prvním prvkem fronty, je netrpělivá a po X č.j. čekání opouští systém.

**Zdroje:**

- `Fitcheats/Zkoušky z minulých let/2024-25 - 2. termín E.pdf`, str. 2 (fotka zadání se studentským řešením)
- `Fitcheats/Zkoušky z minulých let/2019-20 - 2. termín Y.pdf`, str. 2 (fotka zadání)
- `Fitcheats/Zkoušky z minulých let/2017-18 - 2. termín A.txt` (vzpomínka studenta, otázka 1)

**Existující řešení:**

- **Studentské řešení na zkouškovém archu 2024/25 E** (bez bodového hodnocení): stejná struktura jako tady. Fronta je rozdělená do dvou míst, místo se značkou pod přechodem *postup* funguje jako *1. místo volné* a vrací se z obsazení linky i z přechodu `4 jč.`. Netrpělivý odchod vede do místa před výstupním přechodem. Výhrady jsou jen k notaci: všechny přechody jsou nakreslené stejně jako tenké čárky, takže časované (`EXP(x)`, `EXP(Y)`, `4 jč.`) jdou poznat jen podle popisku, a místa nemají názvy.
- K zadáním 2017/18 a 2019/20 žádné řešení není.

</details>
