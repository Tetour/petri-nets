# Petri net inventory: IMS midterm materials (Půlsemestrálky)

Base folder: `/home/adam/Documents/Knowledge/Vzdělání/FIT/6. semestr/IMS - Modelování a simulace/Fitcheats/Půlsemestrálky/` (called BASE below).

I checked every page of every PDF (15 files) by looking at it. Where a text layer existed I also extracted it, and for unclear photos I ran OCR through pipes only, so no files were written.

**Overall result:**
- Almost every exercise is category (a): model a described system as a timed/stochastic Petri net with all parameters. The 2021/22 tasks and all later ones are 10 points each; the 2022/23 tasks and later add "V modelu jednoznačně ukažte (přechodem) moment, kdy transakce opouští systém".
- There are **no** category (b) exercises (marking or trace at time t) and **no** category (c) exercises (reachability, boundedness, invariants) anywhere.
- The only (d) item is a 4-point theory question (2013/14 D): "Definujte sémantiku časovaného přechodu u Petriho sítí".

**Notation in the drawn solutions:**
- Hatched or filled rectangle = timed transition.
- Thin bar = immediate transition.
- "p=N" = priority.
- A place with no input feeding a hatched transition, or a token place with a self-loop on a timed transition = generator.
- "Seize/Release" = facility pattern: a resource place with tokens, an immediate transition that takes the token, a timed transition that returns it.

**Legibility limit:** every solution is a handwritten sketch: photos, scans, whiteboard or tablet screenshots. The Read renderer gives about 850 px per page and I could not crop or zoom without writing files. Wiring details marked "(?)" are my best reading and should be checked against the original.

---

## 1. `BASE/Zadání z minulých let/2010-11.pdf` (2 pages, text layer, LaTeX)

No points or variant labels. There is no explicit "model as PN" line, but task 3's note refers to a "místo v Petriho síti", so these are PN modelling tasks, category (a). No solution exists in the materials.

**1 Banka (p1):** "Do banky přichází klienti v intervalech daných exponenciálním rozložením se středem 10 minut. V bance je jedna přepážka. Doba obsluhy klienta u přepážky se řídí exponenciálním rozložením se středem 5 minut. Po obsloužení opouští klient banku. V intervalech daných exponenciálním rozložením se středem 1 měsíc přepadne banku lupič. V okamžiku přepadení opouští případný klient u přepážky banku, všichni klienti ve frontě na přepážku opouští banku a po dobu přepadení nepřichází žádní další klienti. Přepadení banky trvá rovnoměrně 5 až 10 minut. V systému se pohybuje jeden policista, který v intervalech daných exponenciálním rozložením se středem 2 hodiny prochází kolem banky. U banky se zdrží vždy 3-5 minut rovnoměrně. Pokud uvidí přicházející lupič policistu u banky, opouští systém. Pokud policista přijde v době, kdy je banka v přepadení, lupiče okamžitě zlikviduje. Po deseti minutách po ukončení přepadení banky (nebo po zlikvidování lupiče) se v bance obnoví normální provoz. Poznámka: Po dobu přepadení banky je proces příchodů transakcí přerušen."

**2 Logisticka centrala (p1):** "Do logistické centrály přijíždí dodávky v intervalech daných exponenciálním rozložením se středem 2 hodiny. Dodávka přistupuje k centrále přes jednu nakládací/vykládací rampu. Dodávka přiveze 100 balíků ke zpracování. Dobu vyložení balíků zanedbáváme. Zpracováním přivezených balíků se zabývá jeden pracovník. Doba zpracování každého jednotlivého balíku se řídí exponenciálním rozložením se středem 1 minuta. Zpracované balíky jsou umístěny v centrále. Kapacitu centrály pro uložení přivezených nebo zpracovaných balíků nezkoumáme. Polovina dodávek po vyložení balíků nakládá zpracované balíky až po svou kapacitu 100 balíků, druhá polovina po vyložení okamžitě opouští systém. Doba naložení každého jednotlivého balíku se řídí exponenciálním rozložením se středem 1 minuta. Po plném naložení dodávka odjíždí a další její chování nezkoumáme. Poznámka: Pracovník zpracovávající přivezené balíky je nezávislý proces."

**3 Chmel (p1):** "Na chmelové brigádě je 100 sběračů chmele. Doba sběru chmele do košíku se řídí exponenciálním rozložením se středem 20 minut. Po naplnění košíku jde sběrač košík uložit do skladu s kapacitou 20 košíků. Pokud ve skladu není aktuálně volné místo pro uložení košíku, sběrač se vydá s košíkem na 10-15 minut na procházku. Po návratu opět zkoumá volnou kapacitu skladu (počet procházek je neomezený). V případě volné kapacity skladu zabere uložení košíku do skladu 1-2 minuty rovnoměrně. Po uložení plného košíku s nasbíraným chmelem obdrží sběrač volný košík a vrací se ke sběru. Počty košíků v systému nesledujeme a zanedbáváme i doby přesunu sběrače mezi polem a skladištěm (tzn. není tam sklad volných košíků). V systému pracuje jedna přepravní dodávka s kapacitou 10 košíků. Naložení každého jednotlivého košíku do dodávky trvá dobu, která se řídí exponenciálním rozložením se středem 2 minuty. Okamžikem započetí nakládání košíku dodávkou se uvolňuje jedna pozice ve skladu. Po plném naložení dodávka odjíždí a vrací se prázdná za jednu hodinu. Poznámka: Kapacitu skladu plných košíků lze modelovat místem v Petriho síti se zadanou kapacitou."

**4 Prazirna kavy (p2):** "Do pražírny kávy příchází zákazníci v intervalech daných exponenciálním rozložením se středem 1 hodina. V pražírně pracuje jeden prodavač. Prodavač se přemisťuje mezi prodejnou a dílnou na pražení kávy. Zákazníci se řadí do fronty a čekají na prodavače s tím specifikem, že vždy první ve frontě po minutě čekání opouští prodejnu neobsloužen (tzn. netrpělivý je pouze první zákazník ve frontě). Pokud je prodavač v prodejně, obsluhuje zákazníky do vyčerpání fronty. Pokud je prodavač v prodejně, pak po 10 minutách čekání na zákazníka odchází do dílny, kde praží kávu. Doba pražení se řídí exponenciálním rozložením se středem 1 hodina. Po dokončení práce se prodavač vrací do prodejny (doby přesunu zanedbáváme). Zákazník si kupuje 0 až 5 balíčků kávy. Výběr a zakoupení každého jednotlivého balíčku mu zabere dobu, která se řídí exponenciálním rozložením se středem 1 minuta. Poznámka: Zákazník tedy provede právě 5 iterací nákupu, kde každý z nich je pravděpodobnostní."

## 2. `BASE/Zadání z minulých let/2011-12.pdf` (1 page, text layer)

Four tasks. Each ends "Modelujte zadaný systém ve formě Petriho sítě s vyznačením všech potřebných parametrů." No points are given. Category (a). No solutions exist.

**1 Příklad:** "Mezi místy A a B je třeba vykopat 1000 metrů dlouhý tunel. Z každé strany kope jiná vrtná souprava (souprava A/B). Souprava B vždy vrtá úsek jednoho metru dobu 1-3 hodiny. Souprava A je extrémně hlučná a proto musí v nočních hodinách vrtat pomalu (3-5 hodin na metr) a v denních hodinach smí pracovat běžnou rychlostí 1-3 hodiny na metr. Pokud v libovolném okamžiku vrtání běžnou rychlostí u soupravy A denní doba přejde z denních do nočních hodin, vrtání se přeruší a dále se rozpracovaný metrový úsek od počátku znovu opakuje v pomalém módu. Vrtné soupravy postupují proti sobě, přesto se však nesmí srazit. Práce se ukončí v okamžiku, kdy se soupravy potkají. Vyznačte v Petriho síti místo, které bude obsahovat informaci o počtu metrů od startovního místa A, kde dojde k setkání obou souprav. Noční doba trvá 8 hodin. Zvolte si vhodně počáteční čas."

**2 Příklad:** "Poštovní pobočka má každý den rozvézt 100 nových doporučených zásilek. K dispozici má jeden poštovní vůz s doručovatelem. Poštovní vůz za dobu 10-15 minut nabere najednou zásilky až po svou kapacitu 20 zásilek. Pak vyrazí do terénu. Každý úsek trasy (z pošty k zákazníkovi, od zákazníka k jinému zákazníkovi, od zákazníka zpět na poštu) trvá dobu exp(2min). Po příjezdu k zákazníkovi je pravděpodobnost 20 procent, že zákazník nebude zastižen. Pokud je zastižen, pak je doba vyřizování 3-5 minut, jinak je 1 minutu. Vůz se po posledním zákazníkovi vrací na pobočku, kde vyloží jednotlivě nedoručené zásilky, které se uloží pro přímý odběr zákazníky. Vyložení každé jednotlivé nedoručené zásilky trvá exp(2min). Zákazníci přichází na pobočku pro nedoručené balíky v intervalech exp(10min) a čekají ve frontě libovolně dlouho. K dispozici mají 3 poštovní přepážky, každou s jedním pracovníkem pošty. Obsluha zákazníka trvá 1-2 minuty. Při nakládání a vykládání vozu asistuje doručovateli vždy jeden z pracovníků na přepážce."

**3 Příklad:** "Na přehradě jsou přístaviště A a B, každé s kapacitou jedna pro přistavení lodi. Mezi přístavišti A a B jezdí dvě vyhlídkové lodě s kapacitou 50 turistů. Na přístaviště A přichází turisti v intervalech exp(2min). Každý jednotlivý turista je ochoten čekat na příjezd lodi nejvýše 20 minut, pak opouští systém. Po přistavení lodi k molu přístaviště začnou turisti po jednom nastupovat. Nastoupení každého trvá 20-30 sekund. Loď z přístaviště odjíždí po naplnění svojí kapacity, nejpozději však po 15 minutách od přistavené k molu (aktuálně nastupující turista smí dokončit nastupování). Neobsloužení turisti po odplutí lodi opouští systém. Vyhlídková jízda lodě trvá 30-40 minut a končí v přístavišti B, kde během 5 minut všichni turisti najednou vystoupí. V přístavišti B žádní cestující nenastupují a loď se vrací po vyprázdnění do přístaviště A. Cesta z B do A jí trvá 20 minut. V počátečním stavu sítě platí, že každá z lodí se poprvé do přístaviště A dostane po době dané exp(3 hodiny)."

**4 Příklad:** "V dílně jsou tři stroje - A, B a C. Stroje A a B obsluhuje jeden pracovník, stroj C pracuje samostatně. Ke strojům A a B přistupuje pracovník s rovnoměrnou pravděpodobností. Obsluha stroje spočívá v přípravě výrobní operace, která zabere 3-5 min u stroje A a 4-6 min u stroje B. Po přípravě operace stroje už operaci dokončí samy v době 10 min u stroje A a 15 min u stroje B. Výsledkem výrobní operace na A a B je 20 kusů mezivýrobku, které jsou umístěny ve výstupním kontejneru stroje s neomezenou kapacitou. Stroj C v každém cyklu bere současně mezivýrobek z A a B z výstupních kontejnerů operací. Pokud nemá tyto mezivýrobky, dojde u něj k poruše, která vyžaduje okamžitou opravu pracovníkem. Obsluha opravy zabere exp(20 min). Pracovník obnoví po návratu z opravy poruchy svou předchozí činnost od jejího počátku. Výrobní cyklus stroje C trvá vždy 1 minutu."

## 3. `BASE/Zadání z minulých let/2013-14.pdf` (3 pages, text layer)

- Pages 1–2 hold four system descriptions labelled A–D.
- Page 3 is the exam header "Půlsemestrální písemka IMS, Varianta D, akad. rok 2013/14":
  - "Otázka (4 body): Definujte pojmy model, modelování, simulace a modelový čas. Definujte sémantiku časovaného přechodu u Petriho sítí." This is category (d), theory.
  - "Příklad (6 bodů): Zadaný systém modelujte formou Petriho sítě s vyznačením všech potřebných parametrů." The header applies to each of the variants A–D, so each is a 6-point task in category (a).
- No solutions exist.

**A) (p1):** "Do bankovní pobočky přicházejí klienti v intervalech daných exponenciálním rozložením se středem 5 minut. V pobočce pracují tři pracovníci na přepážce a jeden vedoucí pobočky. Klient si po příchodu do pobočky vezme lístek ze stroje pro evidenci pořadí. Použití stroje zabere 30-60 sekund rovnoměrně. Deset procent klientů požaduje speciální poradenství, které vykonává vedoucí pobočky. Ostatní klienti jsou obsluhováni na přepážkách. Obsluha na přepážce i speciální poradenství trvají dobu danou exponenciálním rozložením se středem 5 minut. Vedoucí pobočky je v počátečním stavu na své přepážce. Pokud je k jeho přepážce fronta klientů prázdná již 30 minut, vydává se na kontrolu pobočky, která mu zabere 10-20 minut. V intervalech daných exponenciálním rozložením se středem 5 hodin přijíždí do pobočky vozidlo s převozem hotovosti, které má pro vedoucího vysokou prioritu. Pokud momentálně neobsluhuje klienta, musí svou činnost přerušit a obsloužit auto. Pokud momentálně obsluhuje klienta, dokončí nejprve obsluhu klienta a pak započne obsluhu auta. Obsluha auta zabere 10-15 minut. Po obsluze auta se vrací k přepážce."

**B) (p1):** "Automatizovaná výrobní linka na výrobu konzervovaného hrášku má charakter pásové výroby a je složena ze třech výrobních operací: příprava, tepelná úprava a balení. K lince přijíždí v intervalech daných exponenciálním rozložením se středem 3 hodiny dodávka sklizeného hrášku. Stroj na přípravu hrášku dodávku zpracovává 30-50 minut a výsledkem operace je 100 přepravních várek polotovaru. Přepravní várky dále postupují linkou samostatně. Následuje zpracování polotovaru na stroji pro tepelnou úpravu polotovaru, který má kapacitu 50 přepravních várek. Tepelné zpracování přepravní várky trvá 1 hodinu. Posledním v řetězci je stroj na balení s kapacitou 1 přepravní várka. Balení jedné várky trvá 1 minutu. V intervalech daných exponenciálním rozložením se středem 10 hodin dochází na balícím stroji k poruše, která se projeví během jeho balící činnosti. Odstranění poruchy trvá 30-80 minut. Během poruchy nevstupují nové přepravní várky do operace tepelné úpravy. Aktuální várka v balícím stroji je znehodnocena. Přepravní várky čekající na balení mají trvanlivost 1 hodinu. Po uplynutí doby trvanlivosti jsou znehodnoceny. Během poruchy balícího stroje pokračuje rozpracovaná operace tepelné úpravy. V modelu evidujte jedním místem počet znehodnocených přepravních várek."

**C) (p1–2):** "Počítačový server obsahuje jeden procesor a síťovou linku pro spojení s okolím. Operační systém počítače umožňuje multi-tasking úloh. V systému existuje 10 uživatelských úloh a speciální úloha provozující databázovou službu. Síťová linka počítače je v počítači samostatné zařízení obsahující vstupní a výstupní buffery s neomezenou kapacitou. Linka může v jednom okamžiku buď přijímat zprávu z okolí do vstupního bufferu nebo odesílat zprávu z výstupního bufferu. V okolním prostředí vznikají požadavky na databázovou službu serveru v intervalech daných exponenciálním rozložením se středem 1 sekunda. Plánovač operačního systému přiděluje v 90 procentech případů procesor jedné z uživatelských úloh a v 10 procentech případů úloze databázové služby. Kromě toho se databázová úloha aktivuje ještě v případě, že ve vstupním bufferu je více než 100 požadavků — v takové případě může být přerušena uživatelská úloha, které se odebere zcela přidělený procesor. Časové kvantum přidělené uživatelské úloze na procesoru je vždy 10 milisekund. Databázová úloha drží přidělený procesor, dokud nezpracuje veškeré požadavky ze vstupního bufferu. Zpracování jednoho požadavku trvá dobu danou exponenciálním rozložením se středem 1 milisekunda. Výsledek požadavku je umístěn do výstupního bufferu síťové linky."

**D) (p2):** "Pro dokončení stavby budovy z betonu je třeba provést 100 elementárních betonových stavebních částí. Na stavbě pracuje jedna parta bednářů a jedna parta betonářů. Pro zbudování jedné stavební části je třeba 1) připravit licí formu pro lití betonu (dělají bednáři, trvá 3-5 hodin), 2) do formy nalít beton (dělají betonáři, trvá 30-60 minut), 3) beton nechat uzrát 10 dní a 4) licí formu odstranit (dělají bednáři, trvá 2-3 hodiny). Na stavbě je k dispozici 10 licích forem. V situaci, kdy lze někde licí formu zbudovat a jinde licí formu po vyzrání betonu odstranit, bednáři přednostně vykonávají odstraňování forem. Po dokončení přípravy licí formy se odešle požadavek na dodávku betonu. Dodávka dorazí za dvě hodiny po zavolání. Pokud nemají betonáři dodávku betonu pro lití do zbudované formy, pak se na jeden úkon (příprava nebo odstranění formy) přidávají k bednářům."

## 4. `BASE/Zadání z minulých let/Přehled zadání 2014-19.pdf` (6 pages, typeset)

Compilation "Přehled zadání příkladů na půlsemestrálních písemkách IMS za roky 2014-19 cca." with the instruction "Zadaný systém modelujte formou Petriho sítě s vyznačením všech potřebných parametrů." It holds Z1–Z24. No years, variants or points are given. All are category (a). Solutions are cross-referenced as follows:
- **DC** = `BASE/Democvičení 2020-21 - Z4 zadání a řešení.pdf`, an official-looking demo session in red/blue/green tablet ink.
- **PREP** = `BASE/FIT - Příprava 2021-22.pdf`, student solutions with vote counts and comments.
- **FOTO** = `BASE/Zadání z minulých let/2024-25 - Varianta A (fotky).pdf`, projector photos.

- **Z1 (p1):** "Po jezeře jezdí jedna výletní loď s kapacitou 50 cestujících. Provozní doba lodi začíná ráno u nástupního mola pro cestující. Provozní doba lodi trvá 10 hodin. Cestující přichází na molo v intervalech daných exponenciálním rozložením se středem 5 minut. Pokud cestující příjde po ukončení provozní doby, okamžitě systém opouští. Cestující nastupují na loď jednotlivě. Nástup jednoho cestujícího na loď trvá dobu danou exp. rozložením se středem 30 sekund. Loď odjíždí od mola na výletní jízdu, pokud nastane jeden z těchto dvou případů (nastupování cestujícího se vždy dokončí): 1) loď je naplněna cestujícími, 2) uplynuly 2 minuty od nastoupení posledního cestujícího z fronty (tj. loď na molu čeká) Výlet trvá jednu hodinu a končí vždy na molu. Po ukončení provozní doby loď dokončí případné nabírání cestujících dle výše uvedených pravidel a vyrazí na výlet. Pokud se přistaví k molu po dokončení provozní doby, cestující už nenabírá a přesune se do depa. Cestovní doby mezi molem a depem neuvažujeme. Také neuvažujeme dobu vystupování cestujících po návratu z výletu. Modelujte jeden den provozu výletní lodi." → Two student solutions in PREP p3 and p4.
- **Z2 (p1):** "Do kotle uhelné elektrárny přikládá uhlí uhelný mlýn zabezpečující přísun a zpracování paliva pro kotel. V režimu běžného provozu vhazuje mlýn do kotle dávku paliva v intervalu 1 minuta. V intervalech daných exponenciálním rozložením se středem 100 dní dochází v elektrizační soustavě k havárii, která si vynutí okamžité odstavení elektrárny. Během odstávky mlýn nedodává kotli palivo a kotel 5 hodin chládne. Po vychladnutí kotle lze elektrárnu opět zapojit. Opětovný start elektrárny zabere dalších 5 hodin pomalého rozehřívání, kdy mlýn vhazuje dávku paliva v intervalech 5 minut. Po dokončení rozehřívací fáze může mlýn začít zásobovat kotel dle intervalu běžného režimu. Interval mezi haváriemi se počítá od posledního naběhnutí elektrárny do běžného režimu nebo od počátku modelového času." → PREP p5 and p6.
- **Z3 (p1):** "Přečerpávací vodní elektrárna je složena ze dvou nádrží A a B. Každá nádrž má kapacitu 1000 jednotek vody. V počátečním stavu jsou obě naplněny 500 jednotkami vody. Elektrizační soustava pracuje v běžném denním provozu 16 hodin a v nočním provozu 8 hodin. V běžném denním provozu se spouští voda z nádrže A do nádrže B rychlostí jednotka vody za 4 minuty. V běžném nočním provozu se čerpá z B zpátky do A rychlostí jednotka vody za 1 minutu až do vyprázdnění nádrže B. V intervalech daných exponenciálním rozložením se středem 100 dní dochází k havárii v soustavě. Pokud tato havárie nastane v běžném denním provozu, pak elektrárna zvýší produkci tím, že spouští vodu z A do B rychlostí jednotka vody za 1 minutu do vyčerpání zásob, nejvýše však 3 hodiny. Potom se vrací do režimu dle denní doby." → PREP p7.
- **Z4 (p2):** "Bagrista má odstranit zeminu z 1000 metrů dlouhého úseku pro stavbu silnice. Zeminu ukládá na jedno aktuálně přistavené nákladní auto. V systému jsou 3 nákladní auta, která jsou v počátečním stavu přítomna na stavbě. Jedno auto pojme zeminu z úseku 3 metrů stavby. Bagrování jednoho metru úseku trvá dobu danou exponenciálním rozložením se středem 5 minut. Naložené auto odjíždí a vrací se prázdné za dobu danou expenciálním rozložením se středem 1 hodina. Pokud bagrista nemá přistaveno nákladní auto, přeruší práci a odchází na dobu 10 minut do nedalekého stánku s občerstvením." → DC p1, the separate DC řešení file, and PREP p8.
- **Z5 (p2):** "Životní cyklus překladiště se skládá z osmihodinové pracovní doby a 16 hodin odpočinku. Auta s nákladem přijíždí na rampu překladiště pouze během pracovní doby v intervalech daných exp. rozložením se středem 10 minut. Auto je přistaveno na rampu a čeká dokud z něj jeřáb nevyloží 1 jednotku nákladu. Jeřábník přesouvá jednotku nákladu z auta do místa určení dobu danou exponenciálním rozložením se středem 3 minuty. Pokud nemá 10 minut co přesouvat (na rampě není auto), pak jeřábník vyráží na obchůzku po překladišti, která trvá 5-10 minut rovnoměrně." → PREP p9.
- **Z6 (p2):** "Do nemocniční ambulace přicházejí stále pacienti v intervalech daných exp. rozložením se středem 20 minut. Po příchodu jsou registrováni u přepážky objednávání a registrace pacientů (1-2 minuty). Ambulance obsahuje dva lékaře, kteří vyšetřují čekající pacienty. Doba vyšetření se řídí exp. rozložením se středem 10 minut. V intervalech daných exp. rozložením se středem 5 hodin sanita přiveze do nemocnice dodávku urgentních pacientů. Oba lékaři přeruší svou případnou práci v ambulanci a opouští ordinace na dobu 3-4 hodiny k urgentnímu zásahu. Aktuálně rozpracovaní pacienti u registrační přepážky prioritně provedou přeobjednání (1-2 minuty) a opuští systém. Ostatní pacienti v čekárně čekají dále." → DC p2 and PREP p10.
- **Z7 (p2):** "Hudební rádio pouští písničky, reklamy a rozhovory s posluchači, kteří si přejí přehrát oblíbenou písničku. Písnička hraje po dobu 3-5 minut. Redaktor rádia přehrává písničky ze svého seznamu a kromě toho musí každou hodinu začít přehrávat reklamní stopu o délce 5 minut. Posluchači volají do rádia v intervalech daných exp. rozložením se středem 20 minut. Posluchač je vpuštěn do vysílání až potom, kdy dohraje písnička, případně reklama (reklama má přednost před posluchačem). Rozhovor s posluchačem trvá 1-2 minuty. Reklama přeruší přehrávání písničky i rozhovor s posluchačem. Přerušená písnička se neopakuje. Přerušený rozhovor se opakuje od začátku." → DC p3 and PREP p11.
- **Z8 (p2):** "Zahradník na FIT má každý den zalít 30 květin v květináčích. Květiny obchází s konvicí o kapacitě 10 jednotek vody. Květina s pravděpodobností 20% vyžaduje 3 jednotky vody, jinak 4 jednotky vody. Zahradník napustí konvici do plné kapacity za 60 sekund. Cesta mezi zdrojem vody a libovolným květináčem nechť je 2-5 minut. Cesta mezi květináči nechť je dána exp. rozložením se středem 1 minuta. Pokud u květináče zahradník zjistí, že daná květina vyžaduje více vody než má aktuálně v konvici, pak se vrací vodu (cesta ke zdroji a zpět) v konvici doplnit. Zalití květiny trvá vždy 20 sekund. Zahradník je na počátku u zdroje vody a má naplněnou konvici. Modelujte jeden den práce zahradníka." → PREP p12.
- **Z9 (p3):** "Do školní menzy přichází studenti v intervalech exp(3 min). Jídlo vydává 5 kuchařek. Doba obsluhy jednoho studenta kuchařkou se řídí exp(1min). Po obdržení jídla student konzumuje po dobu 10-15 minut rovnoměrně. V intervalech exp(100 dní) dostává menza hlášení o žloutenkové karanténě. Po příchodu hlášení se ukončí okamžitě všechny činnosti (výdej, konzumace) a úplně všichni studenti opustí menzu. Po odchodu všech studentů z menzy se zahájí karanténa trvající 10 dní. Příchodem hlášení se zastaví proces příchodu studentů do menzy." → PREP p13.
- **Z10 (p3):** "Pracovní doba úřadu je 8 hodin, po kterých následuje 16 hodin volna. Do úřadovny přichází klienti v období pracovní doby v intervalech exp(10min). Agendu klientů vyřizují úředníci na třech přepážkách. Zpracování jednoho klienta trvá dobu exp(15min). Pokud počet klientů ve frontě k přepážkám dosáhne počtu 10 klientů, úřad na dobu 2 hodin otevře tři další dodatečné přepážky. Po ukončení pracovní doby opouští všichni klienti ve frontě úřad (rozpracovaní klienti jsou dokončeni) a po uvolnění klientem se taky okamžitě uzavřou případné dodatečné přepážky." → PREP p14, which the comments call "100% špatně".
- **Z11 (p3):** "Systém vodní přečerpávací elektrárny je tvořen dvěma nádržemi A a B, obě s kapacitou 600 jednotek vody. Režim systému se dělí na: 1) denní etapu výroby (16 hodin), kdy se voda spouští z elektrárny B do A rychlostí 1 jednotka vody za 2 minuty do vyčerpání zásob a na 2) noční etapu spotřeby, kdy se voda z A čerpá do B rychlostí 1 jednotka za 1 minutu. V intervalech daných exp(10 dní) dochází v elektrizační soustavě k havárii vyžadující zvýšenou spotřebu elektřiny. Havárie trvá 1 hodinu. Pokud k havárii dojde v noční etapě, pak se na dobu havárie práce elektrárny přepne do denního (výrobního) režimu. Po dokončení havárie pokračuje systém v práci dle aktuální denní doby. V počátečním stavu začíná denní etapa a stav v nádržích je A: 0, B: 600." → No solution.
- **Z12 (p3):** "Do centrály přepravní firmy přichází balíky k rozvozu v intervalech exp(20min). Firma zaměstnává jednoho řidiče, který balíky z centrály rozváží autem o kapacitě 20 balíků. V systému rozlišujeme nově podané A-balíky a B-balíky, u kterých se zatím nepodařilo zastihnout adresáta. Řidič vyráží z centrály po plném naložení auta A-balíky. Dobu nakládání balíku zanedbáváme. Doba každé cesty (z centrály k adresátovi, mezi adresáty, zpět do centrály) se řídí exp(10min). Zastávka u každého adresáta trvá rovnoměrně 3-5 minut. Adresát je s pravděpodobností 20% nezastižen a balík se tudíž vrací do centrály. Balíky s nezastiženým adresátem (tzv. B-balíky) se odkládají na další pokusy o doručení. Dobu vykládání B-balíků zanedbáváme. B-balík se stává A-balíkem po 24 hodinách. V počátečním stavu nejsou v systému žádné B-balíky." → PREP p15.
- **Z13 (p3):** "V regionu dochází ke vzniku požárů v intervalech daných exponenciálním rozložením se středem 8 hodin. Centrála hasičů dostává hlášení o novém požáru okamžitě po jeho vzniku. Nehašený požár trvá 2-3 hodiny, tj. po uplynutí této doby žádost o pomoc hasičů zaniká. Hasičská centrála má 5 hasičských vozů. K běžnému požáru je třeba výjezd jednoho vozu. Doba cesty vozu ke každému požáru se řídí exp 10 minut (symetricky cesta zpátky). Hašení požáru trvá 30-60 minut. V intervalech daných exp rozložením se středem 1 týden dochází k požáru extrémního rozsahu, která vyžaduje výjezd všech dostupných požárních vozů (všechny vozy dostupné v centrále, všechny vozy po návratu z běžného požáru). Extrémní požár po 10 hodinách skončí, tj. pak se vozy vrací." → PREP p16.
- **Z14 (p4):** "Uvažujme pekárnu spojenou s obchodem, ve které pracuje jeden pekař. Pekař buď vyrábí chleba nebo se věnuje zákazníkům u pultu. Do obchodu přichází zákazníci v intervalech daných exp 20 minut. Každý zákazník kupuje jeden chleba. V počátečním stavu je na pultě obchodu 20 bochníků chleba a pekař je přítomen u pultu. Obsluha jednoho zákazníka zabere 1-2 minuty. Pokud se na počátku obsluhy zákazníka ukáže, že na pultě došel chleba, pak se pekař přesune do výrobny a peče chleba. Doba pečení chleba je 2 hodiny. Rozpracovaný zákazník a všichni zákazníci ve frontě odejdou z obchodu. Výsledkem pečení chleba je 20 bochníků na pult prodejny. Po upečení chleba se pekař vrací k pultu. V průběhu pečení chleba nově příchozí zákazníci okamžitě opouští obchod." → PREP p17.
- **Z15 (p4):** "Do městské spalovny vozí odpad auta s kapacitou 1 kubík odpadu. Dovážka odpadu do spalovny probíhá rychlostí 10 kubíků odpadu za hodinu. Kapacita vstupního skladu přivezeného odpadu je 100 kubíků (sklad na počátku obsahuje 50 kubíků odpadu). Pokud není volná kapacita vstupního skladu, pak auto odjíždí nevyloženo. Vyložení auta trvá 2 minuty. Linka s pracovní kapacitou 1 kubík odpadu spaluje odpad rychlostí 15 kubíků za hodinu. V intervalech daných exponenciálním rozložením se středem 3 dny dochází na lince k poruše (porucha nepřeruší právě prováděné spalování jednotkového kubíku), jejíž oprava zabere 5 hodin. Po opravě se obnoví provoz linky a linka následujících 5 hodin zvýší rychlost spalování na 30 kubíků za hodinu." → PREP p18.
- **Z16 (p4):** "Dílna na produkci jablečného moštu (moštárna) leží vedle jablečného sadu. Moštárna obsahuje 5 poloautomatických lisů, sběrnou nádobu na mošt a jednu lahvovací linku. Ve firmě pracují dva moštaři a pět sběračů jablek. Sběrač v intervalech daný exponenciálním rozložením se středem 30 minut přináší do moštárny jednu bedýnku jablek. Každý moštař pracuje nezávisle a provádí dvě činnosti: 1) plnění lisů jablky, 2) lahvování. Lis pracuje dávkově s kapacitou danou obsahem jedné bedýnky jablek. Plnění lisu moštařem zabere 5-7 minut. Po naplnění lisu dále lis pracuje samostatně. Lisování zabere 30-40 minut a výsledkem je mošt o objemu na 20 lahví. Lisovaný mošt ze všech lisů jde do centrální záchytné nádoby (kapacitu neuvažujeme). Pokud je v záchytné nádobě nějaký mošt, pak moštař přednostně provádí lahvování dokud je nádoba neprázdná. Naplnění jedné lahve moštařem na lahvovací lince zabere 1-2 minuty." → DC p4 and PREP p19.
- **Z17 (p4):** "Letiště má k dispozici jednu dráhu, která slouží pro starty a přistání letadel. V intervalech daných exp(10min) požádá o přistání nové letadlo. Přistávající letadla mají prioritu v přístupu na dráhu před startujícími letadly. Pokud letadlo nezíská dráhu pro přistání do 30 minut od žádosti, pak systém opouští. Letadlo po přistání vymění cestující (za 20-30 minut) a žádá o dráhu pro start. V 10% případů přistávající letadlo havaruje, což způsobí odstávku dráhy na 8 hodin. V případě odstávky dráhy všechna letadla čekající na přistání odletí a v průběhu odstávky nová k letišti nepřilétají. Doba přistání i startu se řídí exponenciálním rozložením se středem 3 minuty." → DC p5 and PREP p20.
- **Z18 (p4–5):** "Na nástupní molo pro vyhlídkové jízdy lodí přichází cestující v intervalech daných exp(5min). Jízdy provádí jedna výletní loď. Každý cestující po 30 minutách svého čekání ve frontě z fronty odchází. Pokud je k molu přistavena loď, cestující po jednom nastupují. Nastoupení jednoho trvá 1 minutu. Loď od mola vyráží, pokud nastane jedna ze dvou okolností: 1) nastoupilo 20 cestujících (naplněna kapacita lodi), 2) od nastoupení posledního uběhly 3 minuty (prázdná fronta). Vyhlídková trasa trvá 1 hodinu, a pak se loď vrací k molu. Dobu vystupování cestujících neuvažujeme." → No solution.
- **Z19 (p5):** "Do pobočky pošty přichází klienti podat zásilku v intervalech daných exp. rozložením se středem 5 minut. Pobočka má dvě podací přepážky (A a B) a dva zaměstnance (pošťáka a řidiče). Pošťák obsluhuje přepážku A. Řidič je primárně určen pro náklad a odvážení podaných zásilek do Centrály. Doba obsluhy jednoho klienta se řídí exp(3min). Po překročení počtu 100 podaných zásilek řidič zásilky naloží do auta (trvá 30 minut) a veze je do Centrály. Vrací se po dvou hodinách. Pokud fronta k přepážkám dosáhne délky 3 klienti, pak řidič otevře přepážku B a obsluhuje ji, dokud se fronta nevyprázdní (tj. přepážku opustí po vyprázdnění fronty k přepážkám nebo když se naplní kapacita 100 pro odvoz podaných zásilek)." → PREP p21.
- **Z20 (p5):** "V provozu městské spalovny pracují tři svozové vozy a jedna spalovací komora. Svozové vozy přijíždí v intervalech exp(1h) s jednotkovým balíkem odpadu, balík vyloží do fronty ke spalovací komoře a za normálních okolností odjíždí na další sběrnou trasu. Kapacita spalovací komory je pět balíků. Doba spalování jednoho balíku se řídí exp(2h). Pokud se naplní kapacita komory a stále je její fronta neprázdná, pak se systém přepne do výjimečného stavu, kdy svozové vozy po vyložení balíku čekají na místě do jeho odvolání. Výjimečný stav se odvolá až po tom, co se veškerá spalovací práce v komoře a ve frontě dokončí." → DC p6.
- **Z21 (p5):** "Městský festivalový autobus sváží návštěvníky z jejich domovů do areálu festivalu. Kapacita autobusu je 20 míst. Návštěvníci registrují svůj požadavek na odvoz v intervalech daných exp(5min). Autobus při své jízdě po jednom nabírá registrované návštěvníky. Každá jízda autobusu (z areálu k návštěvníkovi, mezi návštěvníky, zpět do areálu) se řídí exp(3min). Autobus se vrací do areálu buď po naplnění kapacity, nebo pokud je již na svozové jízdě déle než 40 minut. Po příjezdu do areálu vyloží návštěvníky (dobu zanedbáváme) a vyráží na další svozovou jízdu. Festival trvá 12 hodin. Čtyři hodiny před koncem festivalu už se návštěvníci neregistrují ke svozu, a pokud už není koho svážet, tak končí i činnost autobusu." → No solution.
- **Z22 (p5):** "Do databázového serveru přichází vstupní požadavky v intervalech exp(1s). Požadavky obsluhuje databázový proces A, případně i proces B. Doba vyřízení požadavku se řídí exp(0.5s). Nezávislý systémový proces S v cyklech: po dobu jedné minuty čítá počet dokončených obsluh na procesu A, a pak podle potřeb zapojuje do práce dočasně druhý proces B. Pokud za uplynulou minutu proces A obsloužil 70 a více vstupních požadavků, pak systémový proces S naplánuje aktivaci procesu B. Proces B obsluhuje požadavky po dobu jedné minuty, pak čeká na další naplánování procesem S. Proces B lze naplánovat, i když momentálně běží." → No solution.
- **Z23 (p5–6):** "Na jahodové farmě pracuje 10 sběračů jahod a dva vařiči marmelády. Dále je v systému 5 strojů na vaření marmelády a jedna balící linka. Sběr jedné bedýnky a transport do varny sběrači zabere dobu exp(15min). Vařič zahajuje proces vaření na stroji, když je k dispozici 5 potřebných bedýnek jahod (tj. 1 vaření = 5 bedýnek). Příprava vaření zabere 10-15 minut. Pak stroj bez potřeby obsluhy samostatně vaří 60-70 minut. Výsledkem vaření je 20 jednotek marmelády, kterou je třeba prioritně zabalit do sklenic. Pokud je nějaká uvařená marmeláda, pak jeden z vařičů nastartuje balící linku (zabere 10 minut) a lahvuje marmeládu, dokud existuje z libovolné varny nějaká nezabalená vyprodukovaná marmeláda. Lahvování jedné jednotky marmelády trvá 1-2 minuty." → No solution.
- **Z24 (p6):** "Výrobní hala se skládá z montovny a lakovny. Obě linky mají výrobní kapacitu jedna. Do haly přichází požadavky na výrobu jednoho produktu v intervalech daných exponenciálním rozložením se středem 30 minut. Každý požadavek musí projít nejprve montovnou a pak lakovnou. Montování produktu trvá 10-15 minut. Montovaný meziprodukt vstupuje do fronty lakovny. Lakování trvá 15-20 minut. Pokud dosáhne délka fronty k lakování počtu 3 čekající meziprodukty, pak se montážní linka odstaví, případná rozpracovaná výroba se vyhodí a požadavek se vrací do fronty. Montovna se opět uvede do provozu až potom, co se zcela vyprázdní fronta Lakovny." → DC p7 and FOTO p9–10.

## 5. `BASE/Zadání z minulých let/2021-22.pdf` (4 pages, typeset)

Each page is one variant: "Příklad (10 bodů)", category (a), ending "Zadaný systém modelujte formou Petriho sítě s vyznačením všech potřebných parametrů." The solutions are in `BASE/Hrubý - Řešení 2021-22.pdf`, pages 1–4 (see §11).

- **A (p1):** "Do překladiště přijíždí nákladní auta v intervalech daných exponenciálním rozložením se středem 20 minut. Každé auto veze 3 kontejnery. Překládání kontejnerů z aut do přistaveného vlaku zajišťuje jeden jeřáb. Vykládka jednoho kontejneru zabere 8 minut exponenciálně. Vlak má kapacitu 20 kontejnerů. Po naplnění vlaku vlak odjíždí a vrací se po jedné hodině. Během nepřítomnosti vlaku v překladišti je vykládka z aut pozastavena. Na počátku stojí v překladišti prázdný vlak."
- **B (p2):** "Na poli pracuje 5 sběračů jahod. Každému sběrači zabere dobu danou exponenciálním rozložením se středem 20 minut nasbírat bedýnku jahod a donést ji do sběrného místa. Ve sběrném místě pracuje jedna balicí linka. Lince zabere 5-7 minut rovnoměrně zabalit obsah jedné bedýnky. Pokud fronta k lince dosáhne délky alespoň 10 bedýnek, pak linka hlásí sirénou přeplněnost. Na signál sirény si všichni sběrači dají pauzu v práci na dobu 60 minut a pak obnoví činnost od počátku."
- **C (p3):** "Na molo výletní lodi přichází turisté v intervalech daných exponenciálním rozložením se středem 5 minut. Turisté nastupují na přistavenou loď po jednom. Doba nástupu jednoho turisty je 1 minuta exponenciálně. Po nastoupení dvacátého turisty loď ukončuje nástup, zvedá kotvu a vyjíždí na okružní jízdu trvající 1 hodinu. S okamžikem vyplutí lodi opouští všichni čekající turisté molo."
- **D (p4):** "Do kopírovacího centra přichází požadavky v intervalech daných exponenciálním rozložením se středem 2 minuty. Požadavky jsou nejprve registrovány u přepážky, což zabere 2-3 minuty rovnoměrně. Pak čekají ve frontě na obsluhu. Kapacita obsluhy je 10 požadavků. Doba obsluhy je exponenciálně 20 minut. V intervalech 8 hodin exponenciálně dochází v centru k poruše, která nenávratně zničí všechny rozpracované obsluhy, které systém okamžitě opouští. Po zničení všech rozpracovaných obsluh systém normálně pokračuje v práci."

## 6. `BASE/Zadání z minulých let/2022-23.pdf` (3 phone photos)

All three are "Příklad (10 bodů)", category (a), with the added bold line "V modelu jednoznačně ukažte (přechodem) moment, kdy transakce opouští systém." Solutions: `BASE/Hrubý - Řešení 2022-23.pdf` (§12) and FOTO (§9).

- **A (p1):** "Do kopírovacího centra přichází klienti v intervalech daných exponenciálním rozložením se středem 3 minuty. U přepážky registrují svůj požadavek, což zabere 1-2 minuty rovnoměrně. V centru jsou dva kopírovací stroje: stroj pro normální zakázky (A) a stroj pro speciální zakázky. 70% zakázek směřuje na stroj A. Klienti se speciální zakázkou jsou však netrpěliví, proto po 10 minutách čekání ve frontě na stroj B opouští systém. Doba zpracování na obou strojích se řídí exponenciálním rozložením se středem 3 minuty."
- **B (p2):** "Do trafiky přichází zákazníci v intervalech daných exponenciálním rozložením se středem 5 minut. V trafice pracuje jeden prodavač. Doba obsluhy zákazníka se řídí exponenciálním rozložením se středem 2 minuty. Pokud prodavač nemá zákazníky 10 minut, pak odchází do skladu a vrací se po 10 minutách. Příchozí zákazník okamžitě z trafiky odchází, pokud u pultu není přítomen prodavač."
  - Legibility: the bottom of the sheet is covered by another paper in this photo. The full text is in FOTO p5.
- **C (p3):** "Do pizzerie s rozvozem volají zákazníci v intervalech daných exponenciálním rozložením se středem 5 minut. Vyřízení jedné objednávky (rozhovor, výroba pizzy) zabere dobu danou exponenciálním rozložením se středem 10 minut. V pizzerii jsou 3 pracovníci pro obsluhu volajících a jeden pracovník pro rozvoz. Rozvozový pracovník vyráží na trasu rozvozu se všemi hotovými objednávkami, pokud je splněna jedna z podmínek: A) buď je hotových objednávek alespoň 10, nebo B) je hotová alespoň nějaká a on už čeká 15 minut. Kompletní rozvoz trvá rovnoměrně 30-50 minut."
- **D:** not in this file. The text is in FOTO p7 (cestovní kancelář, see §9). Hrubý labels its solution "D cestovka".

## 7. `BASE/Zadání z minulých let/2023-24.pdf` (4 small images)

All are category (a).

- **p1, "Zadání A":** a Discord screenshot (a student, 01.11.2023), marked "(upraveno)", so it is a student's paraphrase: "Zadání A: V intervalu exp(100ms) přicházejí požadavky a čekají ve fronte na obsloužení serverem. Ten má kapacitu 1 a požadavky obsluhuje rychlostí exp(70ms). Ihned po obsloužení každeho 1000. požadavku se přepne server do režimu údržby kde je 100s. V režimu údržby jsou všechny transakce z fronty i nově příchozí vyhozeny bez obsluhy." No points shown and no solution.
- **p2, unlabelled variant (probably B):** a handwritten rewrite of the assignment plus a student's sketch solution. Text: "Do výpočetní služby přichází požadavky v intervalech daných exponenciálním rozložením se středem 100s. Server má kapacitu jedna pro obsluhu požadavků. Doba obsluhy se řídí exp. rozložením se středem 5s. Pokud je služba nečinná po dobu 200s, pak je převedena do spacího režimu. Z režimu spánku službu probere až nově příchozí požadavek. Po probuzení však služba potřebuje 5s na iniciační proceduru, a až po jejím dokončení může zahájit obsluhu požadavku."
  - Sketch, top row: generator (token place with a self-loop on transition exp(100s)) → place "Příchozí" → immediate transition (seize) → place → timed transition "řešení exp(5s)" → place → exit bar "Odchod".
  - Sketch, second row: from "Příchozí" a pair of arcs ↓↑ (a test arc) to a wake transition → place → transition "Procedura 5s" → place "Služba" (1 token).
  - "Služba" feeds the top seize transition, and "řešení" returns its token to "Služba".
  - "Služba" → transition "200s" → place "spící služba" → back to the wake transition.
  - Small and blurry. The direction of the ↓↑ arcs and the role of the shaded box are unclear.
- **p3, Varianta C:** a crooked photo, confirmed by OCR and by FOTO p3: "K automatu na kávu přichází zákazníci v intervalech daných exponenciálním rozložení se středem 10 minut. Doba obsluhy se řídí exponenciálním rozložením se středem 2 minuty. V automatu se cyklicky projevuje porucha, a to vždy rovnoměrně 5-6 hodin od okamžiku poslední opravy poruchy (nebo od počátku času). Porucha se projeví na právě probíhající obsluze nebo na další následující transakci. Požadavek zasažený poruchou opouští systém bez obsluhy. Oprava poruchy zabere 1 hodinu." It is 10 points and has the bold transakce line. Solution in FOTO p4.
- **p4, Varianta D:** a very small, blurry photo, read with OCR: "Do klientského centra přichází klienti v intervalech daných exponenciálním rozložením se středem 20 minut. Požadavky obsluhuje jedna pracovnice. Doba obsluhy se řídí exponenciálním rozložením se středem 10 minut. Pokud fronta k obsluze dosáhne délky 10 čekajících, pak centrum vyhlásí dočasný "stop stav", během kterého se zastaví proces příchodu požadavků. Stop stav trvá 4 hodiny." It is 10 points. No solution.

## 8. `BASE/Zadání z minulých let/2024-25.pdf` (1 collage page, "IMS půlsemka 2024/2025 (14. 11. 2024)")

All four are 10 points and category (a). A, C and D carry the bold transakce line. Solutions: `BASE/Hrubý - Řešení 2024-25.pdf` (§13).

- **A:** "Zahradnictví tvoří 10 záhonků, jeden zahradník a zahradní budka. Zahradník pravidelně vyráží na obchůzku okopávat všechny záhonky. Okopání jednoho záhonku se řídí exponenciálním rozložením (EXP) se středem 10 minut. Po okopání všech záhonků zahradník 30 minut odpočívá v zahradní budce. V intervalech EXP(48hod) začne bouřka, jejíž délka se řídí EXP(1h). Zahradník nevyráží na obchůzku za bouřky. Pokud ho bouřka zastihne při práci, pak se schová v budce, dokud bouřka neskončí. Po bouřce pokračuje zahradník na záhonku, u kterého byl bouřkou přerušen, ovšem začíná okopávání od začátku."
- **B:** a student paraphrase, not the official text: "stánek s pizzou, jeden pizzař to celé řídí, zákazníci chodí exp(10') a co zákazník to objednávka pizzy, pizzař ho obslouží 3-5' (zahrnuje objednávku, přípravu pizzy a vložení pizzy do peci), je tam pec která má 4 místa, pizza se pak peče 4' a zákazník mezitím čeká, k pečení neni třeba pizzaře (ten mezitím obsluhuje další zákazníky), peče se 4' a pak pizzař vyndá pizzu a dá ji zákazníkovi, což trvá 1' a má prioritu před obsluhou nových zákazníků (credits to [a student])"
- **C:** "Do Centra vyhlídkových letů přichází zákazníci v intervalech daných exponenciálním rozložením se středem 5 min a čekají na nástup do vyhlídkového letadla. Centrum obsahuje jedno vyhlídkové letadlo, které po naložení zákazníků odlétá na vyhlídkovou trasu trvající 50-60 minut. Cestující nastupují do letadla jednotlivě. Nastoupení jednoho zabere 1-2 minuty rovnoměrně. Kapacita letadla je 20 cestujících. Letadlo odlétá na trasu, pokud nastane jedna z okolností: 1) letadlo je naplněno, 2) od nastoupení posledního cestujícího uběhlo 5 minut (tj fronta se vyčerpala, nikdo další nejde a **v letadle už někdo sedí**). Vystupování cestujících po návratu letadla nemodelujeme."
- **D:** "Zákazníci přichází do obslužného Centra typu M/M/1 v intervalech daných exponenciálním rozložením (EXP) se středem 5 minut. Doba obsluhy se v běžném režimu řídí EXP(7min). Pokud však délka fronty dosáhne 5 čekajících zákazníků, pak se Centrum přepne do zrychleného režimu, ve kterém provádí obsluhu v době EXP(3min), což se projeví na nově zahájené obsluze. Centrum setrvá ve zrychleném režimu, dokud se fronta nevyprázdní."

## 9. `BASE/Zadání z minulých let/2024-25 - Varianta A (fotky).pdf` (10 photos of a projected tablet)

Despite its name, this file is a review session covering five older tasks. Odd pages show the assignment; even pages show the solution net drawn live.

**p1–2: 2022/23 A, kopírovací centrum** (text identical to §6 A).

Solution p2:
- Generator: token place with a self-loop on timed transition "exp(3 min)" → queue place.
- Registration: immediate transition taking the queue token and the "přepážka" resource (top token place) → place → timed "1-2 min", which returns the přepážka token.
- → place → two transitions "70%" and "30%".
- **Machine A row**, entered by an arc labelled "z 70": place → immediate seize (with token place "stroj A", label hard to read) → place → "exp(3 min)" (returns stroj A) → place → exit transition.
- **Machine B row**, entered by "30": queue place →
  1. timed "10 min" (timeout) → place → exit transition;
  2. immediate seize with a token place (stroj B, bottom left) → place → "exp(3min)" (returns stroj B) → place → exit transition.

**p3–4: 2023/24 C, automat na kávu.** Solution p4:
- Top row: generator token place with a loop on "exp(10min)" → queue place → immediate seize, which also takes the token place "automat" → "in service" place → "exp(2 min)" → place → red exit mark.
  - Arc from exp(2min) back to "automat".
- Bottom row: token place → "Rovn(5-6 hodin)" → place ("porucha čeká") → immediate transition whose inputs are that place and the in-service place (arc down from it).
  - Red output arc to the final exit place: the hit request leaves without service.
  - Second output → place → "1 hod." transition. This returns a token to the failure-cycle start (long bottom arc) and to "automat" (arc up-left).
  - Because the failure transition is immediate and keeps waiting, it also catches "the next transaction" when the machine is idle.

**p5–6: 2022/23 B, trafika** (full text). Solution p6, red ink with blue additions:
- Generator: token place ↔ "exp(5min)" → arrival place.
- From the arrival place:
  - a bold immediate transition, blue "p=1", which requires the "prodavač present" token place (bottom left, circled in blue). Read arc: input plus return arc. It outputs to the place "FRONTA".
  - a blue horizontal bar drawn above the arrival place (a "T" shape) = the exit transition for customers who cannot enter (lower priority).
- FRONTA → bold immediate "P=1" (seize "L" = prodavač at counter, token) → place → "exp(2min)" → place → exit arrow. exp(2min) returns the token to L.
- Idle logic, from L: timed transition "10 min" → (black-circled area shows a small arc with a circle head, likely an inhibitor "fronta prázdná" (?)) → tall immediate bar, which takes the "present" token from bottom left → place → timed "10 min" (warehouse).
  - This returns tokens to L and to the "present" place via long bottom arcs.
- An "F" mark near the bottom of the tall bar suggests an inhibitor from FRONTA (?).
- Partly ambiguous: overlapping strokes and arrowheads.

**p7–8: 2022/23 D, cestovní kancelář.** This is the only copy of the task text in the materials: "Do pobočky cestovní kanceláře přichází klienti v intervalech daných exponenciálním rozložením se středem 10 minut. Pobočka má 3 přepážky pro obsluhu klientů. Doba obsluhy klienta se řídí exponenciálním rozložením se středem 8 minut. Pokud je ve frontě alespoň 5 čekajících klientů, pak kancelář na dobu 1 hodiny otevře dvě další přepážky, tj. tyto dodatečné přepážky se po hodině (a dokončení rozpracovaného klienta) opět uzavřou." It is "Příklad (10 bodů)" with the bold transakce line.

Solution p8:
- Generator token ↔ "exp(10) min" → queue "F.".
- Immediate seize, which takes from the top place "přepážky" (3 tokens) → place → "exp(8) min" (returns přepážka) → place → exit bar.
- Control place (1 token, bottom left) → immediate "open" transition. It has an arc weight 5 from F and weight 5 back (test ≥5) and adds 2 tokens to "přepážky" (arc "2").
  - It also outputs → place → timed "1h" → arc weight 2 → place → immediate "p:1" transition, which also takes a token from "přepážky" (long dashed arc) → place → transition with input weight 2 → back to the control place.

**p9–10: Z24.** Solution p10:
- Generator token ↔ "exp 30min" → request-queue place → immediate seize, which takes the montovna token from the place below-left → place (in montage) → "10-15 min" (returns montovna) → place "fronta lakovny" → "pr1" seize (lakovna token place below) → place → "15-20 min" (returns lakovna) → place → exit.
- Stop logic: a horizontal immediate transition with arcs weight 3 in and 3 out on fronta lakovny (test ≥3) plus a control token place → output place → large bottom transition.
  - The bottom transition takes the in-montage token, returns the request to the queue and gives back the montovna token (long arcs). It also removes the montovna token if it is free (?).
- A tall right transition restores the control token when fronta lakovny is empty (inhibitor, ?).
- Whiteboard scrawl: the exact arc ends are uncertain.

## 10. `BASE/Democvičení 2020-21 - Z4 zadání a řešení.pdf` (7 pages) and `BASE/Democvičení 2020-21 - Z4 řešení.pdf` (1 page)

Each page of the 7-page file has "Zadání" (the overview text, identical to §4) plus "Řešení", a tablet drawing in red/blue/green. The 1-page file is a downscaled long-scroll duplicate of all 7 solutions with two extra notes:
- under Z7: "P.S. Necasovany prechod ma automaticky vetsi priopitu nez casovany(m)";
- under Z17: "P.S. Zadani neosetruje co se stane s letadlem co (se) shavarovalo".

**Z4 (p1):**
- Red place "1000" (meters left).
- Place "Bagr" (bagrista, 1 token, blue).
- Place "Auta" ("..." = 3 tokens).
- Blue immediate "p=1": Bagr + Auto → place (bagr with car) plus weight 3 → place (car capacity).
- Red immediate "p=1": 1000 + capacity + bagr-with-car → place → "exp(5m)" → back to bagr-with-car.
- Red bold transition when capacity is exhausted (?) → returns Bagr, and → place → "exp(1h)" → back to Auta.
- Blue: Bagr → immediate (lower priority) → place → "10m" → back to Bagr.

**Z6 (p2):**
- Red: generator "exp(20m)" → "Fp" → seize registration token "P" → place → "1-2m" (returns P) → "F" → seize "Lékaři" (2 tokens) → place → "exp(10)" (returns) → place → exit.
- Blue: generator "exp(5h)" → sanita place.
  - p=1 transitions: one takes the in-registration patient → "Přeobjednat" place → timed transition → exit (top right).
  - Another takes the in-examination patient (?) and frees the doctor.
  - A transition takes 2 doctors (weight "2") → place → "3-4h" → returns 2 doctors.
- Dense; the routing of interrupted examinations is unclear.

**Z7 (p3):**
- Place "Redaktor" (token) → "3-5min" (song) → green place/arc back.
- Generator "exp(20m)" → place → immediate "P=1" (needs the redaktor/after-song token) → place "Rozh" → "1-2m" → back to redaktor.
- Ads: generator "1h" → place → immediate that takes the redaktor → "PP" → "5m" → back.
- Blue: when an ad interrupts an interview, a transition takes the "Rozh" token → "DP" → "5m" → back to "Rozh" (interview repeated).

**Z16 (p4):**
- Red: sběrači "5" ↔ "exp(30m)" → "Fbed" (box queue) → seize "5 Lis" + "2 Moštař" → place → "5-7m" (returns moštař) → place → "30-40m" (returns lis) → weight "20" → place "Nádoba".
- Blue: "Lah" (bottling line, token) + moštař + nádoba → "p=1" immediate → place → "1-2m" → loop. A second "p=1" handles continuation while the nádoba is non-empty, and the moštař/linka are returned when it is empty.

**Z17 (p5):**
- Red: generator "exp(10m)" → place with "30m" timeout (to exit "T") → "p=1" seize runway (token "dráha") → place → "exp(3m)" (landing) → "90%" → place → "20-30m" → place → start transition → place → exit "T".
- Blue: "10%" → crash place → transitions removing the runway for "8h"; "OK" place with test arcs blocks the generator; p=1 flush of waiting landing requests.

**Z20 (p6):**
- Vozy "3" → "exp(1h)" → "Fronta" → "p=1" immediate into the chamber (capacity "5 Volné") → place (in chamber) → "exp(2h)" → place "Zařazení" (returns Volné).
- Normal state: place "Nor" (token).
  - A truck returns to the vozy place via a transition that tests Nor.
  - In "Výjim." state the truck waits.
- A switch transition (test: Volné empty and Fronta non-empty) moves Nor to "Výjim.".
- A transition with weight-5 arcs on Volné (all free) and empty Fronta returns Výjim. to Nor and releases waiting trucks.

**Z24 (p7):**
- Red: "exp(30m)" generator → queue → seize montovna token → place → "10-15m" (returns) → "FL" → green "p=1" seize lakovna → place → "20-25m" (sic) → place → exit.
- Blue: test-3 transition (arcs "3" in and out on FL) takes the montovna/OP token → place "OP" (odstaveno). Another blue transition discards the in-progress montage and returns the request to the queue.
- Green: a transition with an inhibitor-like arc from FL restores the montovna token.

## 11. `BASE/Hrubý - Řešení 2021-22.pdf` (4 scanned squared-paper pages)

Solutions to §5 A–D. Blue pen with red teacher notes. Small strokes; read carefully.

**p1 (A, překladiště):**
- Generator "exp(20min)" → place "Fronta aut" → "Seize" (place "Jeřáb", token) → place (car at crane) plus output weight "3" to a counter place. Red note: "TŘI CYKLY VYKLÁDKY (anebo čítač v systému)".
- Red bar "p=1 …" (caption illegible) leads to the unloading cycle → place → "Seize" of place "Vlak" (token) → place → "exp(8min)". This returns Vlak, loops back to the car for the next container, and adds a token to the place "Složeno" (?).
- Immediate "p=1" with input weight "20" from Složeno and the Vlak token → place "Odjezd" → "1h" → back to Vlak. Red note: "Chování vlaku".
- "Release" arc back to Jeřáb after the 3 cycles.
- Note: "Pozn.: Transakce je AUTO, ne kontejner!"

**p2 (B, jahody):**
- "Sběrači" (5 tokens) ↔ "exp(20min)" → place "Fronta beden" → seize "Linka" (token) → place → "5-7min" → release.
- Fronta beden has weight-10 arcs in and out (test) to the "p=1" transition "Spouštěcí podmínka (jednou proveditelné)". It also needs the red-circled place "Pracuje" (token; earlier misread as "Reakce", checked at 500 dpi).
- → place → transition "odvolání sběračů (přerušení práce)", which takes 5 sběrači (arc weight 5) → place → "1h pauza" → weight 5 back to Sběrači and back to Pracuje.
- "Alternativně" (same page): Sběrači(5) → exp → Fronta; a transition tests 10/10 on Fronta with an inhibitor-style red "(5)" → place → "1h" → 5 back. Note "jen na JEDNOU" (fires only once).

**p3 (C, loď):**
- Generator "exp(5min)" → "Fronta na molu" → seize "Loď je k nástupu" (token) → place → "exp(1min) NÁSTUP" (returns the loď token) → "Počet nastoupených".
- Immediate "20" (weight 20), "p=1 (trigger)" → "Vyjíždí".
- From Vyjíždí: "p=1" loop "Vyčisti frontu", which takes Fronta tokens one at a time. Note: "S okamžikem vyplutí opouští všichni čekající turisté molo".
- Lower-priority transition → "na cestě" → "1h" → "návrat" to the loď token.

**p4 (D, kopírovací centrum):**
- Generator "exp(2min)" → "Fronta" → seize "Přepážka" → place → "2-3min" → release → "Fronta" → red bar seize from "Obsluhe" (10 tokens). The bar also needs "SYSTÉM JE OK" (token, read arc) → place → "exp(20min)" → "release" back to Obsluhe.
- Failure: generator "exp(8h)" → place "Vznik poruchy" → red "p=1" ("vyprázdni systém"), which takes SYSTÉM JE OK → place → "p=1" loop "Ničení transakcí v obsluze" ("dokud je co ničit"). The loop takes in-service tokens and returns their Obsluhe tokens.
- Lower-priority "Obnovení" returns SYSTÉM JE OK.

## 12. `BASE/Hrubý - Řešení 2022-23.pdf` (6 pages)

Solutions to §6 and to 2022/23 D (task text in FOTO p7).

**p1 (A, COPY-CENTRUM):**
- Generator "exp(3min)" → "Fronta" → seize "Přepážka" (token, note "jedno zařízení") → place → "1-2min" → release → "Fronta – rozdělování" → two immediate transitions "70%" and "30%".
- 70% → "Fronta A" → seize "Stroj A" → place → "exp(3min)" → release → "konec" → exit bar.
- 30% → "Fronta B" →
  1. seize "Stroj B" → place → "exp(3min)" → release → konec;
  2. timed "10min" ("netrpěliví") → konec.

**p2 (B, TRAFIKA):**
- Generator "exp(5min)" → place → "p=1" transition that tests the place "přítomen" (token) → "Fronta". From the same place, an exit "není prodavač, odchází".
- Fronta → seize "prodavač" (labelled "Facility") → place → "exp(2min) Obsluha" → release → place → exit "obsloužen odchází".
- Idle: prodavač → timed "10min" ("Nikdo nepřichází") → place → "p=2" transition "Jde do skladu", which takes přítomen → place → "10min návrat" → returns přítomen and prodavač.
- Red note: "Velmi hypotetické možnost" (?).

**p3 (C, Pizzerie):**
- Generator "exp(5min)" → "FRONTA" → seize "zam." (3) → place → "exp(10min)" → release, and → "Hotová pizza". Also → place → exit ("transakce opouští systém, varianta A").
- "Rozvozník" (token):
  - "15min čekání" → place "uběhl timeout" → transition that needs ≥1 hotová. Note: "ale pak bude čekat na aspoň jednu hotovou (lib. dlouho)".
  - Immediate with weight "10" from Hotová ("10+ hotovo") + Rozvozník.
- Both lead to a place with a "P=1" loop "dobere zbylých hotových zakázek" → "vyráží" → "je na cestě" → "30-60min" (sic, task says 30-50) → back to Rozvozník. Also → place → exit ("Transakce opouští systém var B").
- Note: "Pozn.: Není důležité KOLIK máme zakázek, ale musí vzít všechny HOTOVÉ".

**p4 (C, Poznámky):** Common errors:
1. "nedobrat všechny hotové – malá chyba";
2. "model timeoutu – malá chyba".

It shows two mini-nets:
- Hotové --10--> transition with Rozvozník, and Rozvozník → "15min" → place → … ;
- Rozvozník → "15min" → place "jede".

Red text: "Tady chceme, že začíná čekání, až je aspoň 1 hotová; jinak řečeno, může čekat lib. dlouho." A "Srovnání v ose modelového času" timeline from t0 marks "15 min čekání", "hotová pizza", "odložení chování" and "odjezd".

**p5 (D, cestovka varianta A):**
- Generator "exp(10min)" → "Fronta" → seize "přepážky" (3) → place → "exp(8min)" → release → "hotovo" → exit.
- "nepřidáno" (token) → transition with weight-5 arcs on Fronta (test) and output "2 přidány" (weight 2 to přepážky) → place → "1 hod" → weight 2 → place "budu chtít dvě zpátky" → transition that takes a přepážka → place → weight 2 → transition "dostal jsem dvě zpátky a obnovuji stav" → nepřidáno.
- Notes: "nutno explicitně stavem odlišit přidáno/nepřidáno" and "4 'místo' 3+2 přepážek ⇒ přijatelné" (partly illegible).

**p6 (D, cestovka variace B):** "Má odlišné chování od varianty A!"
- 3 "základní přepážky" → obsluha → "konec".
- A separate pool of "2 přepážky extra" with its own seize → "obsluha" → konec.
- "nelze otevřít" (token) → transition (test 5 on the queue) → "otevřít jen" → enables the extra seize.
- A "Nezávislý proces odpočtu 1h": place → "1h" → place → transition → back.
- Red note about extra counters being taken back after the client (partly illegible).

## 13. `BASE/Hrubý - Řešení 2024-25.pdf` (4 pages, brown pen)

Solutions to §8.

**p1 (A, Zahradník):** "Model má 3 komponenty: 1) život zahradníka, 2) život bouřky, 3) interakce zahradník × bouřka."
- "začátek" (token) + "není bouřka" (token, test) → transition. It outputs weight "10" to "práce" and a token to the gardener place.
- → "p=1": práce + gardener → place → "exp(10m)" → back to the gardener place.
- When práce is empty → transition → "hotovo" → "30m v budce" → začátek.
- Storm: token → "exp(48h)" → "je bouřka" plus "proces bouřky" → "exp(1h)" → place → "konec" transition, which returns the storm start token and "není bouřka".
- "je bouřka" plus the in-progress okopávání token → transition → "čekám na konec" → transition after the storm ends (needs "není bouřka") → "Zpět ke místu" (back to the gardener place, restarting the current záhonek).

**p2 (B, Pizza-stánek):**
- Generator "exp(10min)" → "Fronta zák." → immediate taking Fronta + "obsluha" (pizzař, token) + "kapacita pece" (4) → place → "příprava" → returns obsluha → place → "pečení" → place → "p=1" (takes obsluha) → place → "vytažení". This returns obsluha and the pec capacity → place → exit "konec".
- Note: "Dává smysl alokovat si prostor v peci hned na začátku."
- "Alternativně": fronta → seize obsluha → příprava → release → "Fronta na pec" → "p=1" seize "kap. pece" (4) → place → pečení → place → "p=1 vytažení obsluhou" …
- Numeric times are not written on the transitions; they follow the task: 3-5', 4', 1'.

**p3 (C, Vyhlídkové lety):**
- Generator "příchod" → "fronta" → immediate (needs the "letadlo je doma" token) → place → "1-2m nástup" → returns letadlo and → "čítač nastoupených".
- "p=1" with weight "20" from čítač → "signál pro odlet" → "na cestě" → "50-60m" → "cesta…" → "zpět" to letadlo.
- Timer: letadlo → "5min" → place "nikdo nepřišel?" → if-else:
  - "p=1" → "nastoupil" (requires čítač ≥1) → "p=1" cycle "tedy už jenom nechají čítač nastoupených" → odlet;
  - else → "čekám dál" (loop back).
- Heavily overdrawn.

**p4 (D, Centrum M/M/1):**
- Generator "exp" → "příchod" queue → "p=1 seize" with "linka" (token) → place "mění ji" → split:
  - "p=0" "normální" path → "exp(7m)";
  - "p=1" path requiring "rychlo režim" → "exp(3m)".
  - Both → place → "release" → linka.
- "normální režim" (token) → transition with weight-5 test on the queue → "rychlo režim".
- "obnovení normálního" (?) transition when the queue is empty → back.
- Note: "Linka: provede 1) seize 2) obsazení"; circled "dle rychlo-režim".

## 14. `BASE/Hrubý - Řešení 2025-26.pdf` (4 high-res photos)

**The 2025/26 assignments are not in the folder.** The tasks below are inferred from the solutions only.

**p1 (A, "Psí salon"):**
- Generator token ↔ "exp(10min)" → "Fronta" → seize "Linka obsluhy" (token) → place → "exp(15min)" → release → place → exit "ven".
- Brown-circled "proces vyhlížení": token place → hatched "1h" timed transition, which also has an arc from Fronta. Note "Trvá!": the timer runs while someone is waiting → place → "p=1" loop that takes Fronta tokens. Note: "čekající zákazníci odchází ze salonu".
- Then → "deaktivace procesu příchodů": takes the generator token → place → "3h" → returns the generator token and the vyhlížení token.
- Notes: "abstrakce, pokud kdokoli ve frontě čeká ≥1h, pak…" and "Alternativně: pro každý proces transakce definovat jeho vlastní Timeout".
- Inferred task: waiting ≥1 h causes all waiting customers to leave, and arrivals stop for 3 h.

**p2 (B, "Obslužné centrum"):**
- Generator ↔ "exp(10min)" → "Fronta" → seize "Linka" (2 or 3 tokens; dots unclear) → place → "if-else" box:
  - normal immediate → place → "exp(5m)";
  - "p=1" requiring "je noc" (test) → place → "exp(10m)".
  - Both → place → release to Linka.
- "proces den/noc": token → "16h" (also marks "je noc") → place → "8h" → place → "p=2" (removes "je noc") → back.
- Note: "priorita zde není ESENCIÁLNÍ – V zásadě je jedno, jak by případná situace dopadla".

**p3 (C, "Výletní autobus"):**
- Generator "exp(3min)" → "Fronta turistů".
- Hatched source "1h" → "proces bus", weight "20" → "kapacita", and → "proces timeout".
- Bus: proces bus → "p=1" (if/else) → "čekám na turistu" → immediate with Fronta turistů and kapacita → place → "exp(30s)" → back to proces bus.
- Timeout: → "20min" → place → transition "*2" → "odjezd timeout" with a "p=1" flush loop.
- Full: transition "*1" (kapacita empty) → "odjezd kapacitní" → exit "autobus pryč".
- Notes: "Odjezd: *1 – plno, *2 – čekám ≥20min"; "Hypoteticky může nastat timeout ∧ kapacita=0 ⇒ 'bus' mrtvé (?)".

**p4 (D, "Úřad"):**
- Generator ↔ "exp(5min)" → "Fronta" → bold seize "Linka úředníci" (token) → place → "exp(10min)" → release → place → exit.
- "proces rozšíření kapacity" (token) → transition with weight-5 in and out arcs on Fronta → adds "2 'extra'" tokens to Linka, and → place → "1h" → weight 2 → place "chci 2 zpátky" → "beru si je zpět" (takes a Linka token) → place → weight 2 → "mám je" → back to the process token.

## 15. `BASE/FIT - Příprava 2021-22.pdf` (22 pages, student Google-doc export with Souhlasí/Nesouhlasí/Netuším votes)

- **p1:** title only, no PN.
- **p2: extra task "Příklad 3"** (photo of an old assignment, year unknown), read with OCR: "Na přehradě jezdí jedna vyhlídková loď s kapacitou 100 návštěvníků. Vyhlídková jízda trvá rovnoměrně 50 – 60 minut. Loď přijede do přístavu a nabírá návštěvníky až po svou kapacitu, maximálně však v přístavišti kotví 15 minut. Doba nástupu jednoho návštěvníka se řídí exponenciálním rozložením se středem 10 vteřin. Návštěvníci přichází do přístavu v intervalech daných exponenciálním rozložením se středem 1 minuta. Poznámka: Po uplynutí 15 minut přítomnosti lodi v přístavu (bez ohledu na počet návštěvníků) loď další návštěvníky nenaloží a odjíždí."
  - Student net: LOĎ (token) → transition → PŘÍSTAV + KAPACITA (weight 100). NÁVŠTĚVNÍCI generator exp(1min) → "prio 1" boarding → exp(10s). "15min" timer, cruise "50-60", and several "prio 2"/"prio 1" cleanup transitions with coloured arcs ("barvy jen pro přehlednost").
  - Votes 2/3/0. Comment: syntax error in the timer that empties capacity ("ideš z místa na miesto").
- **p3: Z1** (white on black). Generator exp(5m); provozní doba token → 10h → "ukončení p. doby"; "loď na molu"; "fronta" p=2; nástup exp(30s); "kapacita 50"; departure p=3; "nikdo nenastupuje 2m"; "vyplutí" → "plavba 1h"; "vyprázdnění" p=4; "depo" via p=1. Comments dispute the 2-min timer semantics.
- **p4: Z1, second solution** (blue pen photo): 50/50 arcs, 1h, 2min, p=1, exp(30s), 10h. Votes 0/2/0. Comment: the upper transition should not send 50, and 50 should return after an hour.
- **p4 also holds the Z2 text.**
- **p5: Z2.** Places BĚŽNÝ PROVOZ and MLÝN; exp(100d), prio1, 5h, 5h, 1min/5min mill loops. Votes 3/1/0. Comment: initial tokens should be in mlýn and běžný provoz.
- **p6: Z2, second solution.** "mlýn norm." ↔ 1m; "kotel jede"; exp(100d) → P=1 → "chladne" 5h → "start el." → "rozehřívá se" 5h; "mlýn po výpadku" 5m loop; P=1. Votes 2/0/1.
- **p7: Z3.** exp(100d) → "je havárie", 3h; A (500), B (500); 1m/4m transfer transitions; "A při havárii"; p=1; den/noc 16h/8h with "denní provoz"/"noční provoz". Comment: "opraveno, ale nepřehledné".
- **p8: Z4.** "odstraněno" with weight 1000 → P=2 end; "nákl. auto" (3 tokens); P=1 → "bagruje" exp(5m) → weight 3 → "naložení" → "odvoz" exp(1h); "bagrista" ↔ "bufet 10m". Votes 1/1/0.
- **p9: Z5.** Arrivals exp(10m); "volná rampa"; P=1; jeřáb exp(3m); "10min" idle → "5-10m"; "práce/volno" 8h/16h. Votes 1/0/0.
- **p10: Z6.** Arrivals exp(20m); registrace 1-2m; čekající; lékaři exp(10m); sanita exp(5h) "je sanita?"; P=2/P=1; zásah 3-4h (weight 2); přeregistrace 1-2m. Votes 0/3/0, with criticism.
- **p11: Z7.** Ads 1h; redaktor; 3-5m; posluchač exp(20m) P=1; 1-2m; 5m. Votes 5/0/0, the best rated.
- **p12: Z8.** Zahradník 2-5m; květiny (30) P=1; exp(1m); 20%/80%; arcs 3/4 from Konev (10); dopouštění 60s; zalito. Votes 0/2/0, with discussion.
- **p13: Z9.** kuchařky (5); exp(3m); exp(1m); 10-15m; žloutenka exp(100d); P=2/P=1 flush; P=3; 10d. Votes 0/2/0.
- **p14: Z10.** exp(10m); fronta; weights 10; 3 extra; 2h; P=1; pracovní doba 8h/16h; "volno". Votes 0, "100% špatně".
- **p15: Z12.** A-balíky exp(20m); weight 20; řidič; cesta exp(10m); 3-5m; 80%/20%; nezastižen; B-balíky 24h; P=1. "Opravená verze (asi)", votes 4/0/0.
- **p16: Z13.** požáry exp(8h) → nahlášen; vozy (5); exp(10m); hašení 30-60m; "nenahlášen 2-3h"; extrémní p. exp(1t); P=1; weight 5; 10h. Comment: "mezi přechody … má být stav".
- **p17: Z14.** zákazník exp(20m); fronta P=1; chleba (20); "když je chleba obsluhuje" P=1; 1-2m; odchod; "pekař u pultu"; "peče?"; 2h → "dopekl"; P=1; weight 20.
- **p18: Z15.** Auta 6m; 2m; sklad (50) with 100/100; místo; plný; odjezd; P=2; linka; 4m/2m; norm/rychle; P=1; porucha exp(3d) "je porucha"; 5h; 5h.
- **p19: Z16.** sběrači exp(30m); lisy (5); moštaři (2); 5-7m; 30-40m; weight 20 to nádoba; linka; lahvuje 1-2m; "dolahvoval"; P=1.
- **p20: Z17.** dráha; exp(10m); 10%/90%; 30m timeouts; P=2; přistává exp(3m) P=1; odbavení 20-30m; chce start; startuje exp(3m); 8h. Votes 0/1/0.
- **p21: Z19.** klient exp(5m); fronta; pošťák; řidič; P=1; exp(3m) ×2; zásilky with weight 100 → P=3 → 30m → 2h; weight-3 test; P=2.
- **p22: extra task "Příklad se zvukovou kartou"** (source unknown, not in the overview): "Mějme jednoprocesorový počítač se zvukovou kartou, na kterém běží 10 procesů. Jeden z nich je speciální a zapisuje do zvukové karty vzorky, které je schopen produkovat rychlostí 500 tisíc za sekundu. Karta má vyrovnávací paměť o velikosti 10 tisíc vzorků a je nastavena tak, že přehraje 100 tisíc vzorků za sekundu. Pokud se vyrovnávací paměť dostatečně vyprázdní (a je volný procesor), je procesor prioritně přidělen zvukovému procesu, který ji začne plnit po blocích 100 vzorků dokud nebude zcela plná a potom se vzdá procesoru. (Doporučení: tečka = volné místo pro jeden blok 100 vzorků) Všechny ostatní procesy mají stejnou prioritu a je jim spravedlivě (round-robin) přidělován procesor s časovým kvantem 10ms. Procesy se mohou vzdát procesoru s pravděpodobností 20 procent v libovolném okamžiku jim přiděleného časového kvanta. Dobu potřebnou pro přepnutí kontextu zanedbáváme."
  - Student net: "procesor" (token); "ZP" (token) p=1 → "a) 0,2 ms"; "100V" place with arcs 100; "b) 10ms"; "c)"; 9 process tokens → split "20%"/"80%" → "exp(10ms)" / "10 ms" → release.
  - Legend: a) plnenie vyrovnávacej pamäte (100 vzorkov), b) prehrávanie (100 vzorkov), c) vyrovnávacia pamäť je plná. "1V = 1 voľné miesto pre blok 100 vzorkov."

The PREP student nets are small white-on-black tablet drawings. The labels listed are legible, but the exact arc wiring needs the original.

---

## Pages with no Petri net content

- PREP p1 (title only). Every other page of every file contains PN material.
- The tasks that ask for a net but have no solution anywhere:
  - 2010-11 #1–4;
  - 2011-12 #1–4;
  - 2013-14 A–D and the theory question;
  - Z18, Z21, Z22, Z23 (Z11 has a student net on the student whiteboard, see `prep-materials.md` §F10);
  - 2023/24 A and D.

## Duplicates and variants

- **Exact duplicates:**
  - Z4/Z6/Z7/Z16/Z17 appear in the overview, DC and PREP.
  - Z20 is in the overview and DC.
  - Z24 is in the overview, DC p7 and FOTO p9.
  - The DC 1-page "řešení" file repeats the 7-page file with two P.S. notes.
  - 2022/23 A is in the zadání file and FOTO p1. 2022/23 B is in the zadání file and FOTO p5. 2023/24 C is in the zadání file and FOTO p3.
- **Two solutions to the same task:**
  - 2022/23 A, B and D: Hrubý vs FOTO.
  - Z24: DC vs FOTO.
  - Z1, Z2 and Z4: two student versions each (Z4 also has DC).
- **Near-variant themes:**
  - Copy centre: 2021/22 D (failure destroys work) vs 2022/23 A (70/30 split + impatience).
  - Boat or plane boarding with full-or-timeout departure: 2011-12 #3, PREP "Příklad 3", Z1, Z18, 2021/22 C, 2024/25 C, 2025/26 C (bus).
  - Pumped storage: Z3 vs Z11.
  - Incinerator: Z15 vs Z20.
  - Extra counters opened by queue length: Z10, Z19, 2022/23 D, 2025/26 D.
  - Queue-length mode switch: 2023/24 D (stop arrivals), 2024/25 D (fast mode), Z24 (stop assembly).
  - Strawberry pickers: 2021/22 B vs Z23.
  - Gardener: Z8 vs 2024/25 A.
  - Pizza: 2022/23 C (delivery) vs 2024/25 B (stand with oven).
  - Idle → leave/sleep: 2010-11 #4, 2022/23 B, 2023/24 "výpočetní služba", Z5.
  - Periodic failure: 2023/24 C, 2013-14 B, Z15.
  - CPU scheduling: 2013-14 C vs the sound-card task.

## Legibility issues

- 2023-24 p1–4 are tiny, blurry and skewed (OCR used).
- 2022-23 zadání p2 is partly covered.
- 2024-25 B and 2023-24 A are student paraphrases, not official text.
- The FOTO projector photos have overdrawn strokes.
- The Hrubý 2021-22, 2022-23 and 2024-25 scans render small, so captions such as the red "p=1 …" bar in 2021-22 A and the notes in 2022-23 D p5–6 are partly illegible.
- Hrubý 2025-26 photos are sharp, but the 2025/26 assignments are missing from the folder.