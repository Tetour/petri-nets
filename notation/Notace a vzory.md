# Notace a vzory Petriho sítí (IMS)

Podle přednášek (Hrubý, `IMS - Prezentace.pdf`, slajdy 123–164 a 186–198) a Hrubého ručně kreslených řešení půlsemestrálek. Poznámky MSI (Vojnar) používají jinou konvenci (okamžitý přechod jako černá čárka, exponenciální jako bílý obdélník); u IMS ji nepoužívat.

## Prvky

| Prvek | Jak se kreslí | Zdroj |
|---|---|---|
| místo | kružnice; značky jako tečky, nebo číslo či symbol uvnitř (`50`, `N`); název vedle | sl. 128, 131, 197 |
| okamžitý přechod | tenký bílý obdélník (Hrubý rukou: tenká čárka) | sl. 132–164 |
| časovaný přechod | šedý (vyplněný) obdélník, čas pod ním: `exp(10)`, `5`, `uniform(10,15)`, `exp(4h)`; parametr `exp` je **střední hodnota** | sl. 136, 139, 151 |
| priorita | `p=1` u okamžitého přechodu; vyšší číslo = vyšší priorita, implicitně `p=0` | sl. 132 |
| pravděpodobnost | `30 %` u okamžitého přechodu; součet ve větvení = 100 % | sl. 134 |
| váha hrany | číslo u hrany, implicitně 1 | sl. 129 |
| inhibiční hrana | hrana zakončená prázdným kolečkem. Hrubý: „poslední roky bojuju proti těmto inhibičním hranám“, místo ní použij podmínku přes prioritu | sl. 133 |
| kapacita místa | nepoužívat; zdroj modeluj jako místo se značkami | studentská skripta |

**Jeden parametr na přechod** (sl. 135): časovaný přechod má jen čas. Okamžitý má buď prioritu, nebo pravděpodobnost, nikdy obojí. Parametr patří přechodu, ne hraně.

**U zkoušky a půlsemestrálky** se od roku 2022 vyžaduje: „V modelu jednoznačně ukažte (přechodem) moment, kdy transakce opouští systém“ a „s vyznačením atributů na přechodech a místech“. Každá síť tedy potřebuje výstupní přechod bez výstupních hran a pojmenovaná místa.

## Sémantika časovaného přechodu

- Odpočet začne, když se přechod stane proveditelným. **Během odpočtu zůstávají značky ve vstupních místech** a přesunou se až na jeho konci (sl. 137).
- Okamžitý přechod má vždy přednost před časovaným (sl. 139). Když si okamžitý přechod během odpočtu vezme značku, odpočet zanikne. **Na tom stojí přerušení obsluhy (poruchy) i netrpělivost.**
- Běžný časovaný přechod **neomezuje počet současně čekajících** (sl. 138): každá značka ve vstupním místě má vlastní odpočet. Kapacitu (frontu u přechodu) je potřeba připsat poznámkou.

## Vzory

### Generátor a odchod

![generátor a odchod](patterns/01-generator/net.svg)

a) Místo se značkou ve smyčce s časovaným přechodem (přednášející: „mírně korektnější“, místo je explicitně vidět). b) Zkrácený tvar: přechod bez vstupu. c) Odchod ze systému: okamžitý přechod bez výstupních hran.

### Zařízení (Facility)

![zařízení](patterns/02-zarizeni/net.svg)

Nahoře plný tvar ze slajdu 154 (Seize – obsluha – Release), dole zkrácený tvar ze slajdu 164, kde je uvolnění sloučené s časovaným přechodem. Oba jsou správně. Hlídej, aby se značka linky **vždy** vrátila.

### Sklad (Store)

![sklad](patterns/03-sklad/net.svg)

Místo s N značkami. Transakce, která potřebuje víc jednotek najednou, má hranu s váhou (zabere i vrátí stejný počet).

### Podmínka přes prioritu (if–else)

![neblokující obsazení](patterns/04-neblokujici/net.svg)

Přechod `p=1` se provede, pokud může (linka je volná); jinak přijde na řadu přechod s `p=0`. Takhle Hrubý modeluje podmínky místo inhibičních hran (sl. 153).

### Pravděpodobnostní větvení

![pravděpodobnost](patterns/05-pravdepodobnost/net.svg)

### Netrpělivost (timeout ve frontě)

![timeout](patterns/06-timeout/net.svg)

Časovaný přechod přímo na místě *Fronta*. Každý čekající má vlastní odpočet; kdo se dostane k lince dřív, tomu odpočet zanikne.

### Přerušení obsluhy (porucha)

![přerušení](patterns/07-preruseni/net.svg)

Okamžitý přechod s prioritou vezme značku čekající v časovaném přechodu obsluhy (sl. 139). Porucha, která přijde, když se nic neobsluhuje, musí zaniknout (`p=0`), jinak se poruchy hromadí.

### Čítač – každá N-tá transakce

![čítač](patterns/08-citac/net.svg)

Každá transakce přidá značku do *čítače*. Hrana s váhou 10 se provede, až je jich 10, a zároveň čítač vynuluje (odebere všech 10).

### Test délky fronty

![test fronty](patterns/09-test-fronty/net.svg)

Dvojice hran s váhou k (do přechodu a zpět) otestuje, že je ve frontě aspoň k transakcí, a nic z ní neodebere. Pozor na rozdíl mezi „dosáhne 5“ (váha 5) a „přesáhne 5“ (váha 6).

### Dočasné zastavení příchodů

![zastavení příchodů](patterns/10-zastaveni-prichodu/net.svg)

Okamžitý přechod odebere značku *generátoru*, takže odpočet příchodu zanikne. Po uplynutí doby se značka vrátí.
