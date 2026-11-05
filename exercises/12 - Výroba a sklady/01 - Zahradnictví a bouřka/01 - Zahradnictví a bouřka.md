# Zahradnictví a bouřka

## Zadání

> Zahradnictví tvoří 10 záhonků, jeden zahradník a zahradní budka. Zahradník pravidelně vyráží na obchůzku okopávat všechny záhonky. Okopání jednoho záhonku trvá exponenciálně se středem 10 minut. Po okopání všech záhonků zahradník přesně 30 minut odpočívá v zahradní budce. V intervalech exponenciálně se středem 48 hodin začne bouřka, která trvá exponenciálně se středem 1 hodina. Zahradník nevyráží na obchůzku za bouřky. Pokud ho bouřka zastihne při práci, pak se schová v budce, dokud bouřka neskončí. Po bouřce pokračuje zahradník na záhonku, u kterého byl bouřkou přerušen, ovšem **začíná okopávání od začátku**.

Podobné úlohy: [Zahradník na FIT](<../10 - Zahradník na FIT/10 - Zahradník na FIT.md>) (obchůzka po květinách), [Porucha vrací transakci do fronty](<../../03 - Poruchy/02 - Porucha vrací transakci do fronty/02 - Porucha vrací transakci do fronty.md>) (přerušení a opakování od začátku).

## Nápověda

<details>
<summary>Zobrazit nápovědu</summary>
<br>

- Model má tři části: život zahradníka, život bouřky a jejich interakci.
- **Obchůzka:** přechod *vyráží* vezme značku *začátek obchůzky*, vloží 10 značek (váha hrany 10) do *záhonky* a jednu značku do *zahradník*. Transakcí je záhonek.
- **Okopání:** zahradník je zařízení. *okopat* (`p=1`) vezme záhonek a zahradníka do *okopávání*, `exp(10 min)` vrátí jen zahradníka, značka záhonku tím zaniká.
- **Konec obchůzky:** když záhonky dojdou, provede se *obchůzka hotova* (p=0) → *v budce* → `30 min` → *začátek obchůzky*. Priorita zajistí, že obchůzka skončí, až když nic nezbývá.
- **„Pravidelně vyráží“** bez udaného intervalu: po 30 min v budce vyráží hned znovu.
- **„Nevyráží za bouřky“:** *vyráží* testuje místo *není bouřka* (hrana tam a zpět). Za bouřky čeká v *začátku obchůzky*. Bouřka během odpočinku v budce odpočinek neovlivní.
- **Bouřka** je samostatný proces s generátorem: *příchody bouřek* ⇄ `exp(48 h)` → *bouřka začíná* → *začátek bouřky* (`p=1`, vezme *není bouřka*, dá *je bouřka*) → *trvání* → `exp(1 h)` → *skončila* → *konec bouřky* (vezme *je bouřka*, vrátí *není bouřka*).
- **Bouřka za bouřky splyne:** generátor na konec bouřky nečeká, takže nová bouřka může začít během probíhající (průměrně 1 h ze 49 h, tedy zhruba každá padesátá). Pak *začátek bouřky* proveditelný není (*není bouřka* je prázdné) a novou bouřku odebere *splyne* (`p=0`): probíhající bouřka pokračuje a skončí podle svého `exp(1 h)`. Podmínka je přes prioritu, žádný test na *je bouřka* není potřeba.
- Stav bouřky (*není bouřka* / *je bouřka*) je v jiných místech než odpočty `exp(48 h)` a `exp(1 h)`. Testovací hrany tak nikdy neberou značku časovanému přechodu a jeho odpočet se nepřeruší.
- **Interakce:** *schová se* je okamžitý přechod, který testuje *je bouřka*. Vezme značku z *okopávání* (zahradník + rozpracovaný záhonek), takže odpočet `exp(10 min)` zanikne (slajd 139). Značka čeká v *úkrytu*, dokud nepřijde *není bouřka*, a *návrat* ji vrátí do *okopávání*. Tam začne nový odpočet `exp(10 min)`, tedy okopávání **od začátku a na stejném záhonku** (značka záhonku se mezitím nevrátila do *záhonků*).
- **Odchod ze systému:** zahradník ani bouřka systém neopouštějí, jsou to cyklické procesy. Záhonek „odchází“ okopáním: `exp(10 min)` vrací jen značku zahradníka, takže značka záhonku tímto přechodem zaniká. Samostatný výstupní přechod (místo *okopáno* → *odchod*) by nic nepřidal.

</details>

## Petriho síť

<details>
<summary>Zobrazit Petriho síť</summary>
<br>

![Petriho síť – zahradnictví a bouřka](net.svg)

</details>

## Časté chyby

<details>
<summary>Zobrazit časté chyby</summary>
<br>

- Testování bouřky přímo na místě, které je vstupem časovaného přechodu bouřky. Testovací hrana značku vezme a hned vrátí, a tím by odpočet přerušila (slajd 139). Proto stav bouřky (*je/není bouřka*) a její odpočty patří do různých míst.
- Po bouřce vrátit záhonek do *záhonky k okopání* místo do *okopávání*. Pak by zahradník mohl začít jiný záhonek, ale zadání chce ten přerušený.
- Navázat přerušení i na odpočinek v budce nebo na čekání před obchůzkou. Bouřka mění jen práci na záhonku.
- Konec obchůzky bez priority: přechod *obchůzka hotova* by mohl předběhnout okopání a obchůzka by skončila s neokopanými záhonky.
- Generátor bez *splyne*: bouřka, která přijde za bouřky, by čekala v *bouřka začíná* a začala by hned po konci předchozí, takže by se bouřky řadily do fronty. Totéž by udělal *splyne* bez nižší priority než *začátek bouřky*: mohl by odebrat i bouřku, která má začít.

</details>

## SIMLIB

<details>
<summary>Zobrazit SIMLIB kód</summary>
<br>

Model je izomorfní k Petriho síti výše: každé místo, přechod a značka mají svůj protějšek v kódu.

```cpp
// Zahradnictví a bouřka – model v SIMLIB/C++
#define I_REALLY_KNOW_HOW_TO_USE_WAITUNTIL   // SIMLIB zpřístupní WaitUntil jen s tímto makrem
#include "simlib.h"

Facility Zahradnik("Zahradník");      // místo „zahradník“ (jedna značka během obchůzky)
bool bourka = false;                  // místa „není bouřka“ (false) / „je bouřka“ (true)
Process *okopavany = nullptr;         // značka v místě „okopávání“ (záhonek se zahradníkem)
bool prerusen = false;                // přechod „schová se“ právě vzal značku z „okopávání“
int zbyva = 0;                        // záhonky této obchůzky, které ještě neodešly
long bourek = 0, splynulo = 0, preruseni = 0, okopano = 0;
Histogram Doba("Doba od začátku obchůzky do okopání záhonku [min]", 0, 30, 20);

class Zahonek : public Process {      // transakce = záhonek k okopání
  double start;
 public:
  Zahonek(double t) : start(t) {}
  void Behavior() {
    Seize(Zahradnik);                 // „okopat“ (p=1): záhonek + zahradník
    do {
      okopavany = this;               // místo „okopávání“
      prerusen = false;
      Wait(Exponential(10));          // exp(10 min); bouřka odpočet zruší (Activate)
      okopavany = nullptr;
      if (prerusen)                   // „schová se“ → „úkryt“
        WaitUntil(!bourka);           // „návrat“ testuje „není bouřka“
    } while (prerusen);               // zpět do „okopávání“: nový odpočet od začátku
    Release(Zahradnik);               // exp(10 min) vrací značku zahradníka
    okopano++;
    Doba(Time - start);
    zbyva--;                          // značka záhonku zanikla (exp(10 min) vrátil jen zahradníka)
  }
};

class Obchuzky : public Process {     // cyklus zahradníka: začátek obchůzky → … → v budce
  void Behavior() {
    for (;;) {
      WaitUntil(!bourka);             // „vyráží“ testuje „není bouřka“
      zbyva = 10;                     // hrana s váhou 10 do „záhonky“
      for (int i = 0; i < 10; i++)
        (new Zahonek(Time))->Activate();
      WaitUntil(zbyva == 0);          // „obchůzka hotova“ (p=0): záhonky došly
      Wait(30);                       // „v budce“ → 30 min → „začátek obchůzky“
    }
  }
};

class Bourka : public Process {       // jedna bouřka: „začátek bouřky“ → trvání → „konec bouřky“
  void Behavior() {
    bourka = true;                    // „začátek bouřky“ (p=1): „není bouřka“ → „je bouřka“
    bourek++;
    if (okopavany) {                  // „schová se“: vezme značku z „okopávání“,
      prerusen = true;                // takže odpočet exp(10 min) zanikne
      okopavany->Activate();
      preruseni++;
    }
    Wait(Exponential(60));            // „trvání“ → exp(1 h) → „skončila“
    bourka = false;                   // „konec bouřky“: „je bouřka“ → „není bouřka“
  }
};

class GenBourek : public Event {      // místo „příchody bouřek“ ve smyčce s exp(48 h)
  void Behavior() {
    if (bourka)                       // „splyne“ (p=0): za bouřky nová bouřka zanikne
      splynulo++;
    else
      (new Bourka)->Activate();       // „bouřka začíná“ → „začátek bouřky“
    Activate(Time + Exponential(48 * 60));  // další bouřka
  }
};

int main() {
  Init(0, 1000 * 24 * 60);            // modelový čas v minutách: 1000 dní
  (new Obchuzky)->Activate();
  (new GenBourek)->Activate(Exponential(48 * 60));  // první bouřka po exp(48 h)
  Run();
  Zahradnik.Output();
  Doba.Output();
  Print("Bouřek: %ld (dalších %ld splynulo s probíhající), zastihlo zahradníka při okopávání: %ld\n",
        bourek, splynulo, preruseni);
  Print("Okopaných záhonků: %ld\n", okopano);
}
```

| Petriho síť | SIMLIB |
|---|---|
| značka záhonku (transakce) | proces `Zahonek` |
| *začátek obchůzky* → *vyráží* (test *není bouřka*) → 10 značek do *záhonky* | proces `Obchuzky`: `WaitUntil(!bourka)`, pak 10× `new Zahonek` |
| *zahradník* (1 značka) + *okopat* `p=1` | `Facility Zahradnik`, `Seize(Zahradnik)`; čekající záhonky jsou ve frontě zařízení |
| *okopávání* → `exp(10 min)`, který vrací zahradníka | `Wait(Exponential(10)); … Release(Zahradnik);` |
| *obchůzka hotova* (p=0) → *v budce* → `30 min` | `WaitUntil(zbyva == 0); Wait(30);` |
| *příchody bouřek* ⇄ `exp(48 h)` → *bouřka začíná* | událost `GenBourek`, která se znovu plánuje za `Exponential(48 * 60)` |
| *začátek bouřky* (`p=1`) | `(new Bourka)->Activate();`, v procesu `Bourka` pak `bourka = true;` |
| *splyne* (`p=0`) | větev `if (bourka) splynulo++;` v `GenBourek` |
| *trvání* → `exp(1 h)` → *konec bouřky* | `Wait(Exponential(60)); bourka = false;` |
| *není bouřka* / *je bouřka* | `bool bourka` |
| *schová se* (zruší odpočet `exp(10 min)`) | `prerusen = true; okopavany->Activate();` (předčasně ukončí `Wait`) |
| *úkryt* → *návrat* (test *není bouřka*) → *okopávání* | `WaitUntil(!bourka)` a nové `Wait(Exponential(10))` v cyklu `do … while` |
| zánik značky záhonku v `exp(10 min)` | konec metody `Behavior()` záhonku |

**Kontrola simulací.** Petriho síť: zahradník je vždy právě v jednom stavu (*začátek obchůzky* + *zahradník* + *okopávání* + *úkryt* + *v budce* = 1), *není bouřka* + *je bouřka* = 1, trvá nejvýš jedna bouřka (*není bouřka* + *trvání* + *skončila* = 1), v *záhonkách* nikdy není víc než 10 značek a všechny přechody se provádějí (`make check`). Za 500 simulovaných dní přišlo 234 bouřek (zhruba po 48 h), 4 z nich splynuly s probíhající a 169 zastihlo zahradníka při okopávání. To odpovídá tomu, že okopáváním tráví asi 100 ze 130 minut cyklu. SIMLIB model: za 1000 dní přišlo 500 bouřek (teoreticky 24 000 h / 48 h = 500), 17 z nich splynulo s probíhající (teoreticky asi 2 %, bouřka trvá průměrně 1 h ze 49 h) a 381 ze zbylých 483 (79 %) zastihlo zahradníka při okopávání; zahradník byl vytížen na 77 %, teoreticky 100 / 130 = 77 % (`make simlib`).

</details>

## Původ a zdroje

<details>
<summary>Zobrazit původ a zdroje</summary>
<br>

**Původ:** půlsemestrální písemka 2024/25, varianta A, 10 bodů.

**Původní znění:**

> Zahradnictví tvoří 10 záhonků, jeden zahradník a zahradní budka. Zahradník pravidelně vyráží na obchůzku okopávat všechny záhonky. Okopání jednoho záhonku se řídí exponenciálním rozložením (EXP) se středem 10 minut. Po okopání všech záhonků zahradník 30 minut odpočívá v zahradní budce. V intervalech EXP(48hod) začne bouřka, jejíž délka se řídí EXP(1h). Zahradník nevyráží na obchůzku za bouřky. Pokud ho bouřka zastihne při práci, pak se schová v budce, dokud bouřka neskončí. Po bouřce pokračuje zahradník na záhonku, u kterého byl bouřkou přerušen, ovšem **začíná okopávání od začátku**.
>
> Zadaný systém modelujte formou Petriho sítě s vyznačením všech potřebných parametrů. **V modelu jednoznačně ukažte (přechodem) moment, kdy transakce opouští systém.**

**Zdroje:**

- `Fitcheats/Půlsemestrálky/Zadání z minulých let/2024-25.pdf`, str. 1 (koláž zadání všech čtyř variant)
- `Fitcheats/Půlsemestrálky/Hrubý - Řešení 2024-25.pdf`, str. 1 (řešení od Hrubého)

**Existující řešení:**

- **Hrubý (str. 1):** síť výše má stejnou strukturu; model si rozdělil na tři části: život zahradníka, život bouřky a jejich interakci. Po odpočinku v budce vyráží zahradník hned znovu. Místa *začátek* a *není bouřka* vedou do přechodu, který dá 10 značek do *práce* a značku zahradníkovi. Dál `p=1` → `exp(10m)` zpět k zahradníkovi, přechod do *hotovo* → `30m v budce` → *začátek*. Bouřka: `exp(48h)` → *je bouřka* + *proces bouřky* → `exp(1h)` → *konec*. Interakce: *je bouřka* + okopávání → *čekám na konec* → po bouřce zpět do místa před `exp(10m)`. Rozdíl: záhonek u něj zmizí už při zahájení okopávání (*práce* + zahradník → okopávání), tady až koncem okopání (`exp(10 min)` vrací jen zahradníka). Samostatný výstupní přechod nemá ani jedna síť. Hrubý vrací značku *příchodů bouřek* až koncem bouřky, takže se bouřky nepřekrývají; tady má generátor vlastní smyčku a bouřka, která přijde za bouřky, splyne s probíhající.

</details>

## Reference

- [Jak síť funguje](<../../../basics/Jak síť funguje.md>)
- [Notace a vzory](<../../../basics/Notace a vzory.md>)

<!-- -->

- [Studijní plán](<../../Studijní plán.md>)
- [Seznam úloh](<../../Seznam úloh.md>)
