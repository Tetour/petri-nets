# 11–09 – Překladiště s jeřábem

## Zadání

> Životní cyklus překladiště se skládá z osmihodinové pracovní doby a 16 hodin odpočinku. Auta s nákladem přijíždí na rampu překladiště pouze během pracovní doby v intervalech daných exp. rozložením se středem 10 minut. Auto je přistaveno na rampu a čeká dokud z něj jeřáb nevyloží 1 jednotku nákladu. Jeřábník přesouvá jednotku nákladu z auta do místa určení dobu danou exponenciálním rozložením se středem 3 minuty. Pokud nemá 10 minut co přesouvat (na rampě není auto), pak jeřábník vyráží na obchůzku po překladišti, která trvá 5-10 minut rovnoměrně.
>
> *Zadaný systém modelujte formou Petriho sítě s vyznačením všech potřebných parametrů.*

Podobné úlohy: [04–07 – Údržbář na obchůzce](<../04–07 - Údržbář na obchůzce/04–07 - Údržbář na obchůzce.md>), [04–08 – Spánek po nečinnosti](<../04–08 - Spánek po nečinnosti/04–08 - Spánek po nečinnosti.md>), [09–15 – Úřad s dodatečnými přepážkami](<../09–15 - Úřad s dodatečnými přepážkami/09–15 - Úřad s dodatečnými přepážkami.md>) (pracovní doba 8 h / 16 h), [11–10 – Bagrista a nákladní auta](<../11–10 - Bagrista a nákladní auta/11–10 - Bagrista a nákladní auta.md>).

## Interpretace

<details>
<summary>Zobrazit interpretaci (nápověda)</summary>

- **Transakce** jsou auta. *Rampa* je fronta, na které může stát víc aut. *Jeřábník* je jedno zařízení: obsazení, `exp(3 min)` a vrácení značky. Vyložené auto odjíždí (výstupní přechod).
- **Pracovní doba** jsou hodiny *pracovní doba* → `8 h` → *konec směny* → *odpočinek* → `16 h` → *pracovní doba*. Příchody se zastaví tak, že okamžitý přechod *zastavení příchodů* vezme značku *generátoru* (odpočet `exp(10 min)` zanikne). Přechod `16 h` značku generátoru vrátí a příchody začnou znovu.
- **Auta, která na rampě stojí v okamžiku konce směny,** se vyloží. Zadání omezuje jen příjezdy aut, ne práci jeřábu.
- **Nečinnost 10 min:** časovaný přechod `10 min` se vstupem *Jeřábník*. Odpočet běží, kdykoli je jeřábník volný. Když přijede auto, obsazení si značku vezme a odpočet zanikne (slajd 139). Testovat „na rampě není auto“ zvlášť netřeba: s autem na rampě volný jeřábník nikdy nezůstane, okamžité obsazení má přednost.
- **Obchůzka** `5–10 min` (rovnoměrně) vrací jeřábníka. Auta, která mezitím přijedou, čekají na rampě. Když po obchůzce stále nic není, za dalších 10 min jde jeřábník znovu.
- **Obchůzky během odpočinku:** zadání to výslovně neomezuje, takže jeřábník chodí na obchůzky i v noci. Kdo chce, aby v době odpočinku nepracoval ani jeřábník, musí ho na konci směny „uspat“ (vzít mu značku stejně jako generátoru) a dořešit auta, která na rampě zbyla. Zadání o tom nic neříká.

</details>

## Petriho síť

<details>
<summary>Zobrazit Petriho síť</summary>

![Petriho síť – překladiště s jeřábem](net.svg)

| Požadavek | Prvek sítě |
|---|---|
| příjezdy exp(10 min) | *generátor* ⇄ `exp(10 min)` → *Rampa* |
| jen v pracovní době (8 h / 16 h) | *pracovní doba* → `8 h` → *konec směny* → *zastavení příchodů* (bere *generátor*) → *odpočinek* → `16 h` → *pracovní doba* + *generátor* |
| jeřáb vyloží 1 jednotku, exp(3 min) | *Jeřábník* (1), obsazení, `exp(3 min)` vrací značku → *vyloženo* → *odjezd* |
| 10 min bez auta → obchůzka 5–10 min | *Jeřábník* → `10 min` → *obchůzka* → `5–10 min` → *Jeřábník* |

Kontrola simulací (213 dní): jeřábník je vždy právě v jednom stavu (*Jeřábník* + vykládka + *obchůzka* = 1), *generátor* + *odpočinek* = 1, tedy příchody jen v pracovní době. Za den přijede v průměru 48 aut (8 h po 10 min), na rampě čekají nejvýš 7. Obchůzek je asi 68 denně, většina v noci.

</details>

## Časté chyby

<details>
<summary>Zobrazit časté chyby</summary>

- Časovač `10 min` jako samostatný proces, který se nezruší příjezdem auta. Jeřábník pak odejde na obchůzku, i když auto stojí na rampě.
- Hodiny 8 h / 16 h, které příchody jen „testují“ přímo na místě hodin: smyčka generátoru by při každém příjezdu zrušila odpočet `8 h` (slajd 139). Proto zastavení příchodů odebráním značky generátoru, nebo samostatná stavová místa.
- Zastavení příchodů odebráním značky z *Rampy* místo z *generátoru*.
- Obchůzka bez návratu značky jeřábníka.

</details>

## Původ a zdroje

**Původ:** půlsemestrálky 2014–19 (přehled zadání), úloha Z5. Přesný rok a varianta nejsou známé.

**Zdroje:**

- `Fitcheats/Půlsemestrálky/Zadání z minulých let/Přehled zadání 2014-19.pdf`, str. 2 (zadání)
- `Fitcheats/Půlsemestrálky/FIT - Příprava 2021-22.pdf`, str. 9 (studentské řešení)
- `Fitcheats/Příprava na zkoušku/luppo - Tabule.png` (nedokončené studentské řešení na tabuli)

**Existující řešení:**

<details>
<summary>Zobrazit existující řešení</summary>

- **Studentské řešení (Příprava 2021/22, str. 9, souhlasí 1):** stejné hodiny se signálními místy a stavovými místy *práce* / *volno* (`8h`, `16h`), generátor `exp(10m)` s testem na *práce*. Navíc místo *volná rampa*, obsazení jeřábu `P=1`, `exp(3m)`, časovač `10min` a obchůzka `5-10m`. U hrany z *práce* k časovači `10min` si autor připsal „extra?“, tedy také váhal, jestli mají být obchůzky jen v pracovní době.
- **Tabule luppo:** hodiny *Rest* / *Work* (`8h`, `16h`) s místy *Rest check* / *Work check*, *Auto* ⇄ `Exp(10)` → *Rampa* → *Je auto* → `Exp(3)`, *Jeřáb*, *Čekání* `10min`, *Obchůzka* `Rov(5-10)`. Nedokončené, v červeně ohraničené části tabule.
- Hrubého řešení ani řešení ze cvičení v materiálech není.

</details>
