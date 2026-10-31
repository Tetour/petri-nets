## IMS Petri nets: exercises, worked examples and notation

**Main findings:**
- **Notation:** the 2025 slides are the official reference. Timed transitions are gray-filled rectangles; immediate transitions are thin white (empty) rectangles. Hrubý's handwritten exam solutions use the same split: timed = scribble-filled rectangle, immediate = thin stroke.
- **Different convention in the MSI notes:** the two "poznámky MSI" PDFs (Vojnar) use another convention (details in A.2 and B.11). Don't copy it.
- **Item 4:** "IMP - Studijní opora.pdf" is IMS material, not IMP. It has no Petri exercises and no Petri figures.
- **Item 3:** the Rábová scripta's Petri chapter has every figure missing and no exercises.
- **Item 6:** there are 5 transcripts, not 4. The Petri lecture (2024-10-11) is one of them.

PDF page = slide number (the slides PDF has 339 pages for 339 slides), and in Rábová PDF page = printed page.

Base directory: `/home/adam/Documents/Knowledge/Vzdělání/FIT/6. semestr/IMS - Modelování a simulace/`

---

### A. Exercises and worked examples

#### A.1 Lecture slides `Přednášky - Prezentace 2025/IMS - Prezentace.pdf` (version 16. září 2025, Peringer + Hrubý; Hrubý authored the Petri slides)

The Petri section is slides 123–139. Petri fragments for queueing systems (SHO) are on slides 151–164 and repeated in the SIMLIB part on slides 174, 186, 189–198. Arcs are drawn red with arrowheads; some back-arcs are black. The colour has no meaning. There is no producer-consumer net, no drawn breakdown (porucha) net, and no M/M/1 net under that name. The closest equivalents are slides 61, 154/186 and 139.

- **Slide 61 "Příklad2 — pokračování" (customers in a shop; Petri net as an abstract declarative model).** Category: model.
  - A place with 1 token, a transition labelled `exponential(1e3/80)` (label above), and an arc from that transition back to the place (generator self-loop).
  - Then: place (queue) → Seize transition, which also takes from a facility place below it (1 token) → place → transition labelled `10` (service), which returns a token to the facility place → final place.
  - All transitions are small white rectangles with the time label above. This is an older style.
  - Paired with a block diagram G → queue → Z.
- **Slide 128 "Graf Petriho sítě".** Category: other (notation).
  - Text: "Místa – kružnice; Přechody – obdélníky; Incidenční relace – šipky; Váhová funkce – ohodnocení hran".
  - Example: place (1 token) → tall white transition → two output places, one empty and one with 1 token.
- **Slide 129 "Chování Petriho sítě".** Category: marking/enabling.
  - Text: "Přechod je proveditelný při značení M, jestliže: ve vstupních místech čeká dostatek procesů a současně výstupní místa mají dostatečně volnou kapacitu."
  - Example: place (1 token) → T; place (2 tokens) → T with arc weight `2` written in red next to the arc; T → empty place.
  - The 2024-10-11 transcript walks through it: state (1,2,0) → T1 → (0,0,1).
- **Slide 131 "Příklad: čtenáři a písaři" (readers/writers).** Category: model/evolution.
  - Readers loop: place N "čtenáři čekají" (initial marking written as the letter N) → T (also needs a token from shared place D "dokumenty") → "má dokument" → T "začíná číst" → "čte" → T "vrací", which returns tokens to D and to N.
  - Writers loop: symmetric, with place M "písaři čekají".
  - The transcript simulates it with 1 reader, 1 writer and 1 document.
- **Slide 132 "Prioritní přechody".**
  - Text: "pt ∈ {0,1,2,3,4,...}; vyšší číslo ⇒ vyšší priorita; implicitně je priorita pt = 0".
  - Example: one place → three horizontal white transitions with no outputs, labelled (none = 0), `p=1`, `p=2`, written below them.
- **Slide 133 "Poznámka: Inhibiční hrany".** Category: model-from-code.
  - Code: `while ( N > 0 ) { akce1(); N = N - 1; } akce2();`
  - Net: a place labelled N (counter) → transition akce1 with `p=1` above it → output place.
  - A process place (1 token) has an arc into akce1, and a black arc loops from akce1 back to the process place.
  - An inhibitor arc runs from N to akce2, ending in a small empty circle at the transition. The process place → akce2 → output place.
- **Slide 134 "Pravděpodobnost provedení přechodu".**
  - Place (1 token) → akce1 labelled `30%` above → place; → akce2 labelled `70%` above → place.
  - Code: `r := Uniform(0,100); if (r <= 30) akce1(); else akce2();`
- **Slide 135 "Pravidla používání rozšířených přechodů".**
  - Text: "Přechod má pouze JEDEN parametr (priorita, pravděpodobnost, časování). Pozor: tento parametr NENÍ parametrem HRANY."
  - Crossed-out wrong example: 30% on one transition, and 70% plus `p=1` on the other. "Nejednoznačnost – přechod se provede s pravděpodobností 70%, ale prioritně = NESMYSL!"
- **Slide 136 "Časované Petriho sítě".**
  - Constant time: white rectangle labelled `3 s` underneath.
  - Random time: gray-filled rectangle labelled `Function(a1,a2,...)` underneath.
- **Slide 137 "Sémantika časovaného přechodu".** Category: marking at time t.
  - Three snapshots of place → T (`tWait`) → place: (1) `time = t0`, token in input; (2) `time < (t0 + tWait)`, token still in input; (3) `time = t0 + tWait`, token moved to output.
- **Slide 138.**
  - Text: "Běžný časovaný přechod neomezuje počet současně čekajících. Někdy ale zavádíme kapacitu časovaného přechodu … jeden (implicitně), vzniká fronta; více (nutno specifikovat poznámkou u přechodu)."
- **Slide 139 "Přechody ve Stochastické PN (SPN)".** This is the breakdown/interrupt pattern.
  - Text: "dva druhy přechodů: časované a okamžité; jediným povoleným parametrem časovaného přechodu je údaj o čase; parametry okamžitého přechodu: priorita, pravděpodobnost; okamžitý přechod má vždy vyšší prioritu než časovaný."
  - Net: place (1 token) → gray `exp(10)` → place.
  - The same token place also feeds a white immediate transition. A second, empty place (with an incoming arc from outside, the "porucha" signal) feeds that immediate transition too.
  - The transcript explains it: the timed transition starts waiting (e.g. 8.4). If a breakdown token arrives meanwhile, the immediate transition fires first, removes the token and cancels the planned end of the timed transition.
- **Slide 151 (= 174) "Příchod a odchod transakce".**
  - Generator form 1: gray `Exp(2)` with no input → place.
  - Generator form 2: place (1 token) ⇄ gray `Exp(2)` self-loop, plus output → place.
  - Leaving the system: place → white transition with no output.
- **Slide 152 "Obsazení zařízení".**
  - Facility: place "Facility" (1 token) and the transaction place → white `Seize` → place.
  - Store: place "Store" (3 tokens) → `Enter` → place.
- **Slide 153 (= 189) "Neblokující obsazení zařízení".**
  - Place "transaction" → `Seize` (`p=1`, also takes the "Facility" token) → place.
  - Same transaction place → second white transition (p=0, "else").
- **Slide 154 (= 186) "Přehled základních operací" (M/M/1 service cycle).** Category: marking evolution.
  - Four rows show the token moving through: place → white `Seize` (+ "Facility" place, 1 token) → place → gray `Exponential(10)` → place → white `Release` → final place.
  - Release has an arc back to the Facility place. The facility token is absent in rows 2–3.
- **Slide 155 (= 190) "Náhodný výběr zařízení".**
  - "transaction" place → 3 unlabelled white transitions (uniform choice) → 3 queue places.
  - Each queue → a Seize transition fed by place Fac1/Fac2/Fac3 (1 token each) → place.
- **Slide 156 "Výběr s prioritou zařízení".**
  - Transaction → 3 transitions, each also taking from Fac1/Fac2/Fac3. Labels `p=1` and `p=2` sit between transitions, so the placement is ambiguous.
- **Slide 193 "Výběr s prioritou — Petriho síť" (clearer version).**
  - Transaction place (token) → T with "Facility 1", `p=2` → place.
  - → T with "Facility 2", `p=1` → place.
  - → unlabelled T (p=0) → queue place → T with "Facility 3" → place. This implements slide 192: first free by priority, otherwise queue at the last facility.
- **Slides 157–164 "Příklad I" (repair shop).** Category: model-from-description.
  - Verbatim task: "Do opravářské dílny přicházejí zákazníci v intervalech daných exponenciálním rozložením pravděpodobnosti se střední hodnotou 20 minut. V dílně jsou dva opraváři: jeden zpracovává normální zakázky a druhý náročné zakázky. Každá třetí zakázka je náročná. Vyřízení normální zakázky trvá 15 minut s exp. rozložením pravděpodobnosti, vyřízení náročné zakázky zabere 45 minut exp. Zákazník čeká na vyřízení své zakázky a pak systém opouští. Modelujte systém pomocí stochastické Petriho sítě."
  - Slides 158–163 build the net step by step; slide 164 is the final net.
  - Gray `exp(20)` with no input place → place → white `33%` / white `66%`.
  - 33% branch: → place (queue) → white Seize (+ place "Narocne", 1 token) → place → gray `exp(45)`, which returns a token to Narocne and goes to the common place.
  - 66% branch: same pattern with "Normalni" and gray `exp(15)`.
  - Common place → white exit transition with no output.
  - Transcript: release is merged into the timed transition ("zabral, pracoval, uvolnil … zdrcel do jednoho přechodu"). "Každá třetí" is read as probability 1/3.
- **Slides 195–198 "Příklad: Samoobsluha" (supermarket).** Category: model-from-description.
  - Verbatim task (195): "Do samoobsluhy přicházejí zákazníci v intervalech daných exponenciálním rozložením se středem 8 minut. Každý zákazník si nejprve opatří vozík. Vozíky se koncentrují na seřadišti a je jich celkem 50. Zákazník vstoupí do prodejny a 30% jde okamžitě k pultíku s lahůdkami, kde obsluhují dvě prodavačky. Obsloužení zákazníka zde trvá 2 minuty (exponenciálně) a pak zákazník pokračuje běžným nákupem. Běžný nákup trvá 10-15 minut rovnoměrně. Nakonec přistupuje k jedné z pěti pokladen. Vybírá si pokladnu podle nejkratší fronty. Doba obsluhy u pokladny se řídí exponenciálním rozložením se středem 3 minuty. Při odchodu ze systému zákazník vrací vozík. Zadání: analýza problému, model ve formě SPN, model ve formě SIMLIB"
  - Slide 196 is the conceptual analysis.
  - Net part 1 (197): `exp(8)` with no input → place → `Enter(Vozíky,1)` (+ place "sklad Vozíky" with `50` written inside) → place → `30%` → place → T (+ place with 2 tokens = prodavačky) → place → `exp(2)` (returns a token to the 2-token place) → place "nakup". The `70%` branch goes straight to "nakup".
  - Net part 2 (198): nakup → `uniform(10,15)` → place → immediate transitions "fronta k 1.", "fronta k 2." (blue dashed box: "přistupuje se k pokladně s nejkratší frontou") → queue place → `Seize(Pokladny[0])` (+ "pokladna 1", 1 token) → place → `exp(3)` (returns the pokladna token) → common place.
  - Then a horizontal transition `Leave(Vozíky, 1)` returns a token to "sklad Vozíky 50" → place → "exit...".
  - Dashed box "blok Pokladna"; caption "blok Pokladna se opakuje pro Pokladny 3-5".
  - Note: here timed transitions are white, not gray, which is inconsistent with slides 136/139/151/164.

#### A.2 `Web předmětu/Petriho sítě - Černobílé a barvené (poznámky MSI).pdf` (Vojnar; 4 PDF pages, each holding 2 printed pages)

- **Fig. 1 (P/T basics).** Two places (2 tokens; 1 token) → a thick black-bar transition, with weight `2` on one arc → 2 output places. Interpreted as machining: material ×2, tool ×1.
- **Fig. 2 (capacity).** `K=2` written on a place; equivalent construction with a complement place.
- **Fig. 3 (firing).**
- **Fig. 4 (inhibitor arcs, small circle at the transition end).** (a) "M(p1) ≥ 1 a M(p2) = 0"; (b) with weight 2: "M(p1) ≥ 2 a M(p2) < 2".
- **Fig. 5 (priority).** Label `pri = 2`.
- **Example 1 (Fig. 6).** Category: model-from-description.
  - Verbatim: "Výrobní systém – přicházející výrobky jsou zpracovány soustruhem, pak jednou ze dvou vrtaček a opouští systém po kontrole jako dobré nebo špatné."
  - Net: novy_mat → P1 → soustr_start (+P3 lathe token) → P2 → soustr_stop (returns P3) → P4.
  - P4 → vrt1_start (+P6) → P5 → vrt1_stop → P9, or P4 → vrt2_start (+P8) → P7 → vrt2_stop → P9.
  - P9 → kontr_start (+P11) → P10 → kontr_uspech → P12 → transition "zmetek", or kontr_neuspech → P13 → transition "vyrobek". Both kontr transitions return the P11 token.
  - (The labels as drawn look swapped.)
- **Example 2 (Fig. 7).** Category: model-from-description.
  - Verbatim: "Uvažujme dva procesy se sdílenou kritickou sekcí: Proces 1 provede akci A1, potom kritickou sekci KS1, akci A2 a pak se jeho činnost opakuje. Proces 2 provádí cyklicky B1, KS2 a B2."
  - Net: A1 (token) –t1→ A_pred_KS –t2 (+volna_KS)→ A_v_KS –t3 (returns volna_KS)→ A2 –t4→ A1, and the symmetric B loop t5–t8.
- **CPN/PNtalk notation (Figs. 8–10)** and the P-schema acknowledgement protocol (Fig. 11). Not exam style.
- The notes contain no exercises for students; these are worked examples only.

#### A.3 `Web předmětu/Petriho sítě - Stochastické (poznámky MSI).pdf` (3 PDF pages)

- **Fig. 1:** P/T start/stop pair versus a single SPN timed transition.
- **Fig. 2:** timed firing at "model time 5:30 / 10:30 / 15:30" with delay 10. Category: marking-at-time-t.
- **Fig. 3:** convention: "(a) exponenciální se střední hodnotou E" = white rectangle; "(b) deterministický se zpožděním D" = black; "(c) jiný typ … Uni(2,5)" = gray.
- **Memory policies:** enabling memory (default) versus age memory. Server capacity of a timed transition: 1 by default.
- **Fig. 4:** non-interruptible action.
- **Fig. 5:** weights 5/3/2 → p = 0.5/0.3/0.2.
- **Worked example (Fig. 6), category model-from-description.** Verbatim: "Budeme modelovat jednoduché zdravotní středisko: Příchod pacienta každých 12 minut s exp. rozložením. Všichni pacienti projdou kartotékou, což jim zabere rovnoměrně 40 až 150 sekund. Poté 25% pacientů jde přímo k lékaři. Zbývajících 75% pacientů jde nejdříve na odběr do laboratoře. To jim zabere v průměru 6 minut, načež polovina lidí odchází a druhá polovina pokračuje k lékaři. U lékaře pacienti stráví rovnoměrně 8 až 25 minut."
  - Net (times in seconds): Entrance (white, 720, no input place) → BeforeInd → Index (gray, Uni(40,150)) → AfterInd.
  - AfterInd → GoToLab (black bar, weight 75) → BeforeLab → Laboratory (white, 300) → AfterLab → LeaveWithoutExp (50) or GoToExp2 (50) → BeforeExp.
  - AfterInd → GoToExp1 (25) → BeforeExp.
  - BeforeExp → Expert (gray, Uni(480,1500)).
- **Section 4 (analysis):** utilisation, queue-length and throughput formulas. Fig. 7 rewrites the net as Queue → immediate → BeingServed → Expert → Free (token) to measure queue length.
- **Section 5:** conflict (Fig. 8), confusion (Fig. 9), liveness. Category: analysis.

#### A.4 Rábová et al. scripta (FEI 1992/2004, "neúplná")

- The Petri chapter is §6.2, pp. 126–138. §6.1 on p. 125 introduces GPSS, Q-GERT and higher-level Petri nets.
- **Every figure is missing** (it reads "obr. ??"). There are no end-of-chapter exercises.
- Worked examples in the text:
  - p. 128–129 (§6.2.5): processor handling requests. Events 1–4 with input/output conditions a–d in a table: 1: –/b; 2: a,b/c; 3: c/d,a; 4: d/–.
  - p. 132–133 (§6.2.10): stochastic net of the same processor. Verbatim: "Přechod t1 s místem p1 představující generátor požadavků … exponenciálním … se střední hodnotou T1. Přechod t2 modeluje zpracování požadavku procesorem … se střední hodnotou T2. Stochastickou simulací můžeme zjistit například průměrný počet značek v místě p3, což odpovídá průměrné délce fronty".
  - p. 134: interpreted net equal to the program `read(x); if x=0 then x:=x+1 else x:=0; write(x)`.
  - p. 135–137: CPN resource allocation (p/q processes, places A–E, resources R/S/T) and the blocks-world CPN (pick/put).
  - Appendix A, pp. 217–218: CPN plus SIMLIB model of a multiprocessor system (Fig. A.2 missing).
- Notation in the text:
  - Transition = "obdélníček (nebo silnou čárkou)"; place = circle or ellipse.
  - Inhibitor = "změnou šipky na konci hrany na kolečko".
  - Capacity K: P → N ∪ {∞}; guards in [ ].

#### A.5 `IMP - Studijní opora.pdf`

- It is actually "Modelování a simulace – IMS – Studijní opora", Petr Peringer, 2. února 2022, 94 pp.; the file name is wrong.
- Petri nets are only mentioned in text (pp. 14, 31–32, 40, 57). There are no Petri figures.
- The only discrete exercise is §5.5.15 Samoobsluha (pp. 53–55), with the same task text as slide 195 but a SIMLIB solution only.
- "Otázky a úkoly" §5.7 (p. 55) asks nothing about Petri nets.

#### A.6 `Fitcheats/Skripta/FIT - Studentská skripta 2015-16.pdf` (student-made, unofficial; pp. 34–51)

- Drawn nets:
  - M/M/1 PN (p. 34): blue exp(x) generator, Seize/Release, green timed exp(x) transition.
  - Priority selection (p. 37), copied from slide 156.
  - Four priority-service variants (pp. 39–41), including preemption.
  - Timed transition semantics (p. 42), copied from slides 136–137.
- Midterm Petri tasks with student solutions, each verbatim in the PDF:
  - Ústředna (p. 42; hand-drawn solution with 60%/40%, p=1/p=2, linka `20`, operátorka) and Zvuková karta (p. 43).
  - Logistická centrála (p. 44) and Chmel (p. 45; solution draws immediate transitions as black bars, plus a hand sketch on p. 46).
  - Pražírna kávy (pp. 46–47).
  - 2013/14 variants: A banka (pp. 48–49, hand sketch); B M/M/1 plus hrášek with porucha (p. 50); C server/DB task (pp. 50–51); D stavba bednáři/betonáři (p. 51).
- Useful remarks in it:
  - "použitie kapacity v stave 'sklad' … Hrubý tuším povedal, že tomu sa máme vyhýbať".
  - "nesmi byt: prechod -> prechod, stav -> stav".

#### A.7 Notes and link files

- `IMS - Poznámky z přednášek.md` contains only 2 links (Feynman probability, Stanford calculus). Nothing on Petri nets.
- `IMS - Odkazy.md` and `Fitcheats/Odkazy.txt` contain no Petri tools or simulators. The only Petri link is the "Petriho sítě (mazanec)" YouTube playlist: https://www.youtube.com/playlist?list=PLsqIxiRzWlw2gcNept2PKCyTwuty_o7Dv
- There is also the PNtalk URL in the MSI notes: http://www.fee.vutbr.cz/~janousek/pntalk/pntalk.html
- Not reviewed: the 8 net PNGs and C++ files in the working directory `cranycrane …/petri/1–8.png`.

#### A.8 Transcripts (`Přednášky - Video 2024/Přepisy/`)

Five transcripts exist, each as .txt and .srt: 2024-09-20, 09-27, 10-04, 10-11, 10-18.

- **10-11 (Hrubý) is the Petri lecture** and covers slides 123–164. It contains no formal exercise. Worked walkthroughs:
  - Marking vector (1,2,0) → (0,0,1).
  - Readers/writers evolution.
  - Weights example: inputs 3 and 1, outputs 2 and 4.
  - While-loop by priority.
  - Breakdown interrupting `exp(10)`.
  - Repair shop (Příklad I), called "typizovaná úloha pro … půlsemestrální písemku".
- **10-18:** the generator with a self-loop place is "mírně korektnější" than the source-transition form. The midterm is announced as "jedna úloha … slovní zadání a vy na to sestavíte model v Petryho síti".
- **09-20 (Peringer):** the midterm is "namalovat model Petriho sítě pro nějaký problém".
- **09-27 (Hrubý):** demo-cvičení plan. 1st: modelling discrete systems with Petri nets. 2nd: discrete simulation. 3rd: practical PN modelling of past midterm tasks. Then the midterm.

Lecture videos without transcripts: 2024-10-25, 11-01, 11-08, 11-15, 11-22, 11-29, 12-06.

Demo-cvičení 2023 videos (no transcripts): `IMS_2023-10-11_1080p.mp4`, `IMS_2023-10-18_1080p.mp4`, `IMS_2023-10-25_1080p.mp4`, `IMS_2023-11-08_1080p.mp4`. Going by the plan above, 10-11 is probably PN basics and 10-25 probably PN practice, but I haven't watched them.

---

### B. Notation conventions (Hrubý/Peringer, IMS)

1. **Places:** circles. Tokens are black dots. The marking can also be written as a number or symbol inside the place: N, M, D on slide 131; "50" on slides 197–198. Transcript: "buď tam ty značky vytečkujeme … nebo … napsat číslo". Labels go next to the place ("Facility", "Narocne", "transaction").
2. **Transitions:** rectangles (slide 128). The lecturer says the shape is not dogma ("čárkami, silnějšími čárkami, obdélníčky").
   - **Immediate:** thin white (empty) rectangle (slides 132–164). In Hrubý's handwritten official solutions it is a single thin stroke.
   - **Timed:** gray-filled rectangle with the time expression written under or next to it (slides 136, 139, 151, 154, 158–164, 174). Slide 136 shows a constant time as white with `3 s`; slides 61 and 197–198 use white for timed transitions too, so there is some inconsistency.
   - Hrubý's own drawings (`Fitcheats/Půlsemestrálky/Hrubý - Řešení 2024-25.pdf` and `2025-26.pdf`) consistently draw timed transitions as wider rectangles filled with zigzag/hatching, labelled `exp(10min)`, `exp(15min)`, `1h`, `30m`, `1-2m`, `16h`.
3. **Time labels as written:** `exp(10)`, `exp(20)`, `Exp(2)`, `Exponential(10)`, `exponential(1e3/80)`, `uniform(10,15)`, `3 s`, `Function(a1,a2,...)`. The parameter of exp is the mean.
4. **Priority:** `p=1`, `p=2` written next to an immediate transition (below on slides 132/153, above on 133/193). Default is 0; a higher number means higher priority. Hrubý uses `p=1`.
5. **Probability:** a percentage written above the transition (`30%`/`70%`; `33%`/`66%`). With no labels, the choice is uniform (slide 155; transcript).
6. **One parameter per transition** (priority, probability or time). The parameter belongs to the transition, not to the arc (slide 135). Timed transitions take only a time; immediate ones take a priority or probability. An immediate transition always beats a timed one (slide 139).
7. **Arc weights:** an integer written next to the arc (slide 129's "2"; Hrubý's `5`, `2`, `20`). Default is 1.
8. **Inhibitor arc:** a line ending in a small empty circle at the transition (slide 133). Hrubý: "Já poslední roky bojuju proti těmto inhibičním hranám" — he prefers priority-based if/else.
9. **Place capacity:** C: P → N (slide 127), default unlimited. Student notes say Hrubý advises avoiding it; model resources as token places instead. Timed-transition capacity defaults to 1 and anything else must be written as a note at the transition (slide 138).
10. **Patterns:**
    - **Facility:** a place with 1 token, labelled.
    - **Store:** a place with N tokens.
    - **Queue:** the place in front of the Seize transition; there is no special symbol.
    - **Seize/Enter:** immediate transition taking the transaction token and the facility token.
    - **Service:** timed transition.
    - **Release:** immediate transition (or the timed transition itself) with an arc back to the facility place (slides 152, 154, 164).
    - **Generator:** gray timed transition `Exp(x)` in a self-loop with a 1-token place, plus an output arc to the first place. This is the "more correct" form; the short form is a source transition with no input (slides 151, 164).
    - **Exit:** immediate transition with no output arcs.
    - **Non-blocking seize / if-else:** Seize with `p=1` plus a p=0 alternative.
    - **Breakdown:** an immediate transition stealing the token waiting at a timed transition (slide 139).
11. **The MSI notes use a different convention. Do not copy it:**
    - Immediate = thick black bar.
    - Exponential = white rectangle.
    - Deterministic = black rectangle.
    - Other distributions = gray.
    - Weights instead of percentages; `pri = 2`; times in seconds.
