# Jak Petriho síť funguje

Jak se síť v notaci IMS „hýbe“: kdy se přechod provede, jak běží čas a co se stane, když si dva přechody berou značky ze stejného místa. Podle přednášek (`IMS - Prezentace.pdf`, slajdy 128–139). Kde slajdy mlčí, je uvedeno, jak to řeší simulátor tohoto repozitáře ([pn/sim.py](../pn/sim.py)), kterým se kontrolují všechny sítě. Jak se prvky kreslí, je v [Notace a vzory](<Notace a vzory.md>).

## Základ: značení a provedení přechodu

- **Značení** (rozmístění značek v místech) je stav systému. Síť se mění jen provedením přechodu.
- Přechod je **proveditelný**, když má každé vstupní místo aspoň tolik značek, kolik je váha hrany (implicitně 1). Inhibiční hrana naopak vyžaduje, aby značek bylo **méně**, než je její váha.
- **Provedení** je okamžité a nedělitelné: ze vstupních míst odebere tolik značek, kolik jsou váhy hran, a do výstupních míst přidá podle vah výstupních hran.
- **Konflikt:** dva přechody sdílejí vstupní místo a značek nestačí pro oba. Provede se jen jeden a druhý přestane být proveditelný.
- **Značky jsou nerozlišitelné** (černobílá síť). Síť neví, která značka je „Petr“ a která přišla dřív; ví jen, kolik jich v místě je.

## Okamžité přechody

- Provedou se v nulovém čase. **Dokud je proveditelný nějaký okamžitý přechod, čas se neposune.**
- Je-li proveditelných víc najednou, vyhraje **nejvyšší priorita** (`p=1` před implicitním `p=0`). Mezi stejnými prioritami rozhodne **pravděpodobnost** (`30 %` / `70 %`), bez parametrů se vybírá náhodně (nedeterministicky).
- Priorita se porovnává jen mezi přechody, které **právě jsou** proveditelné. Proto funguje podmínka přes prioritu: přechod `p=1` se provede, *pokud může*, jinak přijde na řadu `p=0` (if–else, sl. 153).
- **Cyklus samých okamžitých přechodů** by se v nulovém čase prováděl donekonečna (simulátor to hlásí jako *livelock*). Činnost, která trvá, musí končit časovaným přechodem, viz [Kritická sekce](<../exercises/01 - Základní modely/05 - Kritická sekce/05 - Kritická sekce.md>).

## Časované přechody

Časovaný přechod modeluje **činnost, která trvá**: obsluhu, akci, interval mezi příchody. Má jen čas (`exp(10)`, `5`, `uniform(10,15)`), žádnou prioritu ani pravděpodobnost (sl. 135). U `exp(X)` je X **střední hodnota**.

1. **Odpočet začne, jakmile se přechod stane proveditelným.** V tu chvíli se vylosuje doba z rozdělení a spustí se hodiny.
2. **Během odpočtu zůstávají značky ve vstupních místech** (sl. 137). Přechod si zatím nic nevzal.
3. **Na konci odpočtu se přechod provede:** teprve teď odebere vstupní značky a přidá výstupní, obojí najednou.
4. **Okamžité přechody mají vždy přednost** (sl. 139). Protože značky během odpočtu leží ve vstupním místě, může si je okamžitý přechod vzít. Časovaný přechod tím přestane být proveditelný a **jeho odpočet zanikne**.
5. **Bez paměti:** když se přechod později znovu stane proveditelným, začne **nový odpočet od nuly**. Uplynulá část starého odpočtu se nikam nepočítá.

Na rušení odpočtu stojí **přerušení obsluhy poruchou** (porucha s prioritou vezme značku obsluhy), **netrpělivost** (kdo se dostane k lince, tomu odpočet „odchodu z fronty“ zanikne) a **zastavení příchodů** (okamžitý přechod vezme značku generátoru).

**Činnost = místo + časovaný přechod za ním.** Značka v místě *A1* znamená „proces právě dělá A1“ a časovaný přechod za místem je okamžik, kdy A1 skončí.

## Víc značek: kolik odpočtů běží

Běžný časovaný přechod **neomezuje počet současně běžících odpočtů** (sl. 138). Chová se jako neomezený počet paralelních obsluhujících.

- Počet odpočtů = **stupeň proveditelnosti**: kolikrát by šel přechod provést z aktuálních značek. Pro každé vstupní místo se spočítá ⌊značky / váha hrany⌋, rozhoduje nejmenší z těchto čísel.
- **Přijde-li nová značka**, rozběhne se pro ni **nový, samostatný odpočet** s vlastní vylosovanou dobou. Odpočty, které už běží, se nezmění: nerestartují se, nezrychlí ani nezpomalí. Pořadí se může prohodit: později příchozí značka skončí dřív, když si vylosuje kratší dobu.

| Situace | Co nová značka udělá |
|---|---|
| jedno vstupní místo, váha 1 | každá značka má vlastní odpočet |
| váha hrany 2 | dvě značky = jeden odpočet; třetí nic nepřidá, čtvrtá přidá druhý |
| dvě vstupní místa: fronta + volná linka (1 značka) | stupeň je nejvýš 1, nová značka čeká bez odpočtu |
| přechod s kapacitou (`kap. 2`) | běží nejvýš 2 odpočty, ostatní značky čekají v místě |

**Proto má fronta před jednou linkou okamžitý přechod *Seize*:** zabere značku linky a přesune transakci do místa „obsluhuje se“, ze kterého teprve čte časovaný přechod obsluhy. Bez zdroje by se obsluhovaly všechny transakce ve frontě najednou.

**Generátor** (časovaný přechod ve smyčce s místem s jednou značkou) má stupeň vždy 1: provedení značku vezme a hned vrátí, takže začne další odpočet = další interval mezi příchody. Zkrácený tvar bez vstupního místa je proveditelný pořád, se stejným výsledkem.

## Který odpočet zanikne

Když stupeň proveditelnosti klesne (jiný přechod vezme značku), musí zaniknout tolik odpočtů, o kolik klesl. **Který z nich, slajdy neříkají** (značky jsou nerozlišitelné). Simulátor ruší **nejstarší** odpočet: odpovídá to frontě FIFO, kde k lince odchází ten, kdo čeká nejdéle, a jemu má zaniknout i odpočet netrpělivosti.

- **Na volbě nezáleží, když je doba exponenciální.** Exponenciální rozdělení nemá paměť: odpočet, který běží 6 minut, má zbývající dobu rozdělenou stejně jako úplně nový. Všechny běžící odpočty jsou proto statisticky stejné.
- **Při konstantní nebo rovnoměrné době na volbě záleží** a přechod se může **nikdy neprovést**, přestože je pořád proveditelný.

**Příklad vyhladovění.** Značky přicházejí každé 4 min, jiný přechod odebere nejstarší značku 6 min po jejím příchodu, časovaný přechod T trvá konstantně 10 min:

| čas | značek v místě | odpočty přechodu T |
|---|---|---|
| 0 | 1 | začne odpočet A (skončil by v 10) |
| 4 | 2 | začne odpočet B (14) |
| 6 | 1 | A zanikne |
| 8 | 2 | začne odpočet C (18) |
| 10 | 1 | B zanikne |
| … | 1–2 | každý odpočet zanikne 6 min po startu |

Místo nikdy není prázdné, a přesto se T neprovede: žádná značka v něm nevydrží 10 min. To je **správně**, když T znamená „značka čekala 10 min“ (netrpělivost: nikdo nečekal 10 min, nikdo neodejde). Když má T znamenat „místo je neprázdné 10 min“, dej mu **kapacitu 1** (`kap. 1`): běží jediný odpočet a zanikne, až když se místo vyprázdní. V příkladu by se pak T provedlo v čase 10.

### Odpočet zaniká hned, i když se místo doplní ve stejném okamžiku

Odpočet zanikne v okamžiku, kdy přechod přišel o značku, i kdyby se značka do místa vrátila hned v tomtéž čase. Vrácená značka znamená nové zapnutí a nový odpočet.

**Past: testovací hrana** (vezmi a vrať, např. test „je ve frontě aspoň 5“) na místě, ze kterého čte i časovaný přechod, jeho odpočet pokaždé restartuje. Když to nemá nastat, drž testovaný stav v **samostatném místě**, viz [Banka a lupič](<../exercises/09 - Obsluha zákazníků/21 - Banka a lupič/21 - Banka a lupič.md>) (přítomnost policisty a stav loupeže jsou v oddělených místech).

## Souběh časovaných přechodů

Sdílejí-li dva časované přechody vstupní místo, běží odpočty obou a **vyhraje ten, kterému skončí dřív** (závod). Jeho provedení vezme značku a odpočet druhého zanikne. Tak funguje netrpělivost jako závod obsluhy s odchodem.

## Shrnutí jednoho kroku simulace

1. Prováděj okamžité přechody (podle priority, pak pravděpodobnosti), dokud nějaký jde.
2. U každého časovaného přechodu srovnej počet běžících odpočtů se stupněm proveditelnosti (a kapacitou): přebývající zruš (nejstarší), chybějící spusť s dobou vylosovanou teď.
3. Posuň čas na nejbližší konec odpočtu a proveď ten přechod.
4. Opakuj od 1.

## Odpovídající konstrukce v SIMLIB

| Petriho síť | SIMLIB |
|---|---|
| místo + časovaný přechod za ním (činnost) | `Wait(doba)` v `Behavior()` procesu |
| generátor (časovaný přechod ve smyčce) | `Event` s `Activate(Time + Exponential(…))` |
| linka (místo s 1 značkou) + *Seize* + vrácení | `Facility`, `Seize` / `Release`; čekání před *Seize* je fronta zařízení |
| sklad (místo s N značkami), hrana s váhou | `Store`, `Enter(sklad, váha)` / `Leave` |
| okamžité větvení s pravděpodobností | `if (Random() < 0.3) …` |
| zrušení odpočtu (porucha, netrpělivost) | přerušení procesu jiným procesem nebo událostí (`Cancel`, `Passivate`, vyjmutí z fronty) |
