# 09–05 – Pizza stánek

## Zadání

> ⚠️ **Parafráze.** Oficiální text varianty B v materiálech chybí. V koláži je místo něj přepis od studenta (podepsaný „credits to mav_“), který zachycuje čísla, ale ne přesné znění. Text níže je ten přepis beze změn.
>
> stánek s pizzou, jeden pizzař to celé řídí, zákazníci chodí exp(10') a co zákazník to objednávka pizzy, pizzař ho obslouží 3-5' (zahrnuje objednávku, přípravu pizzy a vložení pizzy do peci), je tam pec která má 4 místa, pizza se pak peče 4' a zákazník mezitím čeká, k pečení neni třeba pizzaře (ten mezitím obsluhuje další zákazníky), peče se 4' a pak pizzař vyndá pizzu a dá ji zákazníkovi, což trvá 1' a má prioritu před obsluhou nových zákazníků (credits to mav_)

Ostatní varianty téhož termínu mají na konci větu „V modelu jednoznačně ukažte (přechodem) moment, kdy transakce opouští systém.“, takže ji počítej i tady.

Podobné úlohy: [11–03 – Pizzerie s rozvozem](<../11–03 - Pizzerie s rozvozem/11–03 - Pizzerie s rozvozem.md>) (2022/23).

## Interpretace

<details>
<summary>Zobrazit interpretaci (nápověda)</summary>

- **Transakce** je zákazník spolu se svou pizzou: čeká u stánku, dokud pizzu nedostane, pak odchází.
- **Pizzař** je jedno zařízení, které se zabírá dvakrát: na přípravu (3–5 min) a na vyndání a předání (1 min). Mezi tím ho pizza nepotřebuje, pečení je časovaný přechod bez pizzaře.
- **Pec** je sklad se 4 značkami. Místo v peci se zabírá **už při zahájení přípravy** spolu s pizzařem (Hrubý: „Dává smysl alokovat si prostor v peci hned na začátku.“). Pizzař tak nikdy nezačne připravovat pizzu, kterou by pak neměl kam dát. Vrací se až po vyndání.
- **Pečení 4 min** je obyčejný časovaný přechod. Každá pizza v místě *v peci* má vlastní odpočet (slajd 138) a souběh omezuje jen pec.
- **Priorita vyndání:** obsazení pizzaře pro vyndání má `p=1`, obsazení pro nového zákazníka `p=0`. Když se pizzař uvolní a čeká upečená pizza i zákazník ve frontě, jde nejdřív k peci. Probíhající přípravu priorita nepřerušuje.

</details>

## Petriho síť

<details>
<summary>Zobrazit Petriho síť</summary>

![Petriho síť – pizza stánek](net.svg)

| Požadavek | Prvek sítě |
|---|---|
| zákazníci exp(10 min) | *generátor* ⇄ `exp(10 min)` → *Fronta* |
| pizzař obslouží 3–5 min, pizza do pece | obsazení *Pizzaře* + místa v *Peci* → *příprava* → `3–5 min` vrací *Pizzaře* |
| pec se 4 místy, pečení 4 min | *Pec* (4 značky); *v peci* → `4 min` → *upečeno* |
| vyndání a předání 1 min, přednost před novými | `p=1`: *upečeno* + *Pizzař* → *vyndávání* → `1 min` vrací *Pizzaře* i místo v *Peci* |
| zákazník odchází s pizzou | *hotovo* → *odchod* |

Kontrola simulací: *Pizzař* + *příprava* + *vyndávání* = 1, *Pec* + pizzy od přípravy po vyndání = 4. Fronta zůstává krátká (nejvýš kolem 9), pizzař je vytížen asi na 50 %.

</details>

## Časté chyby

<details>
<summary>Zobrazit časté chyby</summary>

- Pizzař držený i během pečení (hrana zpět do *Pizzaře* až po vyndání). Zadání výslovně říká, že mezitím obsluhuje další zákazníky.
- Pec jako jedno zařízení místo skladu se 4 značkami, nebo časovaný přechod pečení s kapacitou 4 bez místa *Pec*.
- Priorita `p=1` na špatném přechodu: patří k obsazení pizzaře pro vyndání, ne k časovanému přechodu (ten parametr priority mít nemůže).
- Zákazník odchází hned po objednávce. Podle zadání čeká, než pizzu dostane, takže odchod je až po předání.

</details>

## Původ a zdroje

**Původ:** půlsemestrální písemka 2024/25, varianta B, 10 bodů (bodování podle ostatních variant téhož termínu).

**Zdroje:**

- `Fitcheats/Půlsemestrálky/Zadání z minulých let/2024-25.pdf`, str. 1 (koláž zadání; varianta B jen jako studentská parafráze)
- `Fitcheats/Půlsemestrálky/Hrubý - Řešení 2024-25.pdf`, str. 2 (řešení od Hrubého)

**Existující řešení:**

<details>
<summary>Zobrazit existující řešení</summary>

- **Hrubý (str. 2):** stejná síť. Generátor kreslí jako přechod `exp(10min)` bez místa. Na časovaných přechodech má jen názvy (*příprava*, *pečení*, *vytažení*), časy 3–5, 4 a 1 min nedopsal. Místa *obsluha* (pizzař) a *kapacita pece* (4) jdou do společného obsazení, vytažení má `p=1` a vrací obojí.
- **Hrubý, „Alternativně“ (str. 2 dole):** pec se zabírá až po přípravě. Pizza čeká v místě *Fronta na pec* a pec obsadí přechod s `p=1`. Je to také přípustné, ale pizza pak může čekat „mimo pec“, dokud se místo neuvolní. Hrubý proto doporučuje první variantu.

</details>
