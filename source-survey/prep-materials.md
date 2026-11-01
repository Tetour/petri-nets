# Inventory of Petri net exercises in the IMS exam-prep materials

I found 63 Petri net exercise entries across 7 sources. Almost all are category (a), building a timed or stochastic Petri net for a queueing system (SHO, mostly M/M/1 variants). There are two category (b) items: the 2016 D/D/3 "draw the marking at t2 = 10.5" task, in two variants. No source asks for category (c) analysis (reachability, liveness, boundedness, invariants).

**Notation used below:**
- "Gen ⇄ T[exp(a)]" means a generator place with 1 token in a self-loop with a timed transition.
- **L** is the facility (line) place. **Q** is the queue place.
- "seize" is an immediate transition taking a Q token and an L token.
- "→ out → sink" is the exit.
- "test arc k/k" means an input arc of weight k plus an output arc of weight k back to the same place.
- Filled or black transitions are immediate.
- Base directory: `/home/adam/Documents/Knowledge/Vzdělání/FIT/6. semestr/IMS - Modelování a simulace/Fitcheats/Příprava na zkoušku/` (written as `…/` below).

---

## A. `…/FIT - Řešené výpočetní příklady 2017-21.pdf`

**A1. p.5–6, term "2019/2020 1. opravný" (a)**
- Task (photo): "2. (20 bodů) Vymyslete příklad systému hromadné obsluhy typu M/M/1, který bude demonstrovat netrpělivou transakci ve frontě u zařízení. Sestavte jeho model v Petriho síti a SIMLIBu."
- Solution is present. It models an "Automat na bagety"; a customer leaves the queue after 5 minutes.
  - Gen ⇄ T[exp(λ)] → Q.
  - L ("Automat na bagety", 1 token) → seize → busy → T[exp(µ)], which returns L and goes → out → sink.
  - Timed transition "5m" takes its input directly from Q and outputs into the same out place.
  - SIMLIB solution: a Timeout event that calls Cancel(); runs 5*60 s.
- Possible issue: the 5-minute timer hangs on the shared queue place, not on each customer. Whether each token gets its own 5-minute clock depends on the timed-PN semantics used.

**A2. p.10–11, term "2019:" (a)**
- Task: "3. (10 bodů) Pro následující systém nakreslete jeho model v Petriho síti. Systém typu M/M/3. Příchozí transakce je s pravděpodobností 20% prioritní a navíc vyžaduje zabrat dvě linky současně."
- Note on the page: "Proces má zabrat obě linky současně."
- Solution:
  - Gen ⇄ T[exp(x)] → Q.
  - Probabilistic transitions 20% / 80% lead to two branch places.
  - Priority branch: transition p=1 takes **2** tokens from L (L holds **3 tokens**) → place → T[exp(y)] → returns **2** tokens to L → shared out place.
  - Normal branch: transition takes 1 token from L → place → T[exp(y)] → returns 1 → shared out place.
  - Shared out place → sink.

**A3. p.15, group headed only "1" (between "2019:" and "2019 - 2. opravný"), item 4 (a)**
- Task: "(10b) Nakreslit petriho siet M/M/1 kde linka obsluhuje 5 jednotiek ak je vo fronte >= X procesov (presne takto to tam bolo formulované) a inak obsluha trva 10 jednotiek."
- Solution (clean draw.io drawing):
  - Gen place (1) ⇄ exp(N) → Q. L holds 1 token.
  - Normal branch: seize (Q + L) → busy → T[exp(10)] → L and out → sink.
  - Fast branch: transition P1 (priority 1) has input arc weight **x** from Q and output arc weight **x−1** back to Q. It also takes L → busy2 → T[exp(5)] → L and out.
- Comments on the page (they disagree): "nemá tam být obsluha jen 5 a ne exp(5)…" is answered with "je to M/M/1 … aby tam bylo jen trvání 5 jednotek, muselo by to být M/D/1".

**A4. p.17, same "1" group, item 8 (a)**
- Task: "(10 bodů) Nakreslete model v podobě Petriho sítě pro systém typu M/M/1 se zadaným specifikem: Pokud je po dokončení obsluhy transakce fronta před linkou prázdná, pak systém zahájí údržbu o délce 5 časových jednotek."
- Solution (whiteboard):
  - Gen ⇄ Exp(x) → Q.
  - Seize (Q + L, 1 token) → busy → T[Exp(µ)] → out → sink. Exp(µ) also puts a token into a "service finished" place D. It does **not** return L directly.
  - From D, the priority transition "P1" has a test arc on Q (input and output) and returns the token to L. In words: if the queue is not empty, the line is freed immediately.
  - Otherwise a lower-priority transition fires → place → timed "5" → L.
- Page discussion confirms the design: it is this complex "…aby linka nešla do údržby niekoľkokrát po sebe". Votes: Ano +2.

**A5. p.19, "2019 - 2. opravný" (a)**
- Task (paraphrase on the page): "M/M/1, pokud délka fronty přesáhne 5 – M/M/2 na 15j času". Bug's version has the full wording (see C2).
- Solution (paper photo by "@Laďa"):
  - Gen ⇄ exp(λ) → Q.
  - Seize (L at top, 1 token) → busy → exp(µ) → L and out → sink.
  - Switch transition "p=1": test arc **5/5** on Q, input from mode place "M/M/1" (1 token). Outputs: +1 token to L and a token to place "M/M/2".
  - "M/M/2" → timed "15" → place → transition "p=1" (in red) that takes 1 token from L and returns the token to "M/M/1".
- Issue: weight 5 tests "≥5", while the task says "přesáhne 5" (>5). Cranycrane (G1) uses 6.

**A6. p.27, "2020 - 1. opravný" (a)**
- Task (photo): "3. (10 bodů) Pro následující systém nakreslete jeho model v Petriho síti. Systém typu M/M/1. Pokud právě probíhající obsluha přesáhne délku X č.j., pak je přerušena a její transakce opouští systém."
- Solution:
  - Gen ⇄ exp(y) → Q. Seize (L) → busy.
  - Busy → T[exp(x)] → L and out → sink.
  - Busy → timed "X" → leaves the system, and returns L via a long arc.
- Minor label clash: service is exp(x) while the timeout is X. Discussion: Ano +2.

**A7. p.29, "2020 - 1OP. SK B" (a)**
- Task (photo): "3. (10 bodů) Pro následující systém nakreslete jeho model v Petriho síti. Systém typu M/M/1. V intervalech exp(X) dochází na lince k poruše, která přeruší případnou právě probíhající obsluhu a transakce se vrací do fronty."
- Solution:
  - Gen ⇄ exp(z) → Q → seize (L) → busy → exp(y) → L and out → sink.
  - Failure generator ⇄ exp(X); its self-loop was added in red. It feeds failure place F.
  - Transition "p=1" takes F + busy and outputs to Q and to L.
- Written criticism on the page: "Porucha by neměla nastat, když neprobíhá obsluha, resp. by se neměly moct poruchy řadit do fronty…" Failures pile up in F while the line is idle. Xenix (B11) and cranycrane (G3) fix this with a lower-priority discard transition.

**A8. p.31, "2020 - 2. opravný - skupina C" (a)**
- Task: same photo text as A1 ("netrpělivou transakci…").
- Only a SIMLIB link is given; there is **no Petri net drawing**.

**A9. p.31–32, "2021 - Řádný 10:00" (a)**
- Task: "Petriho síť (M/M/1 kde trvání dalsi obsluhy je 5 jednotek pokud jsou alespoň 3 transakce ve frontě, jinak 10 jednotek)"
- Solution (red digital drawing):
  - Gen ⇄ exp(λ) → Q. L holds 1 token.
  - Normal branch: seize → busy → exp(10) → L and out → sink.
  - Priority transition "p=1": input arc weight **3** from Q, output arc weight **2** back to Q, plus L → busy2 → exp(5) → L and out → sink.
- Same technique as A3. Open question: does "3 in the queue" count the transaction being taken?

**A10. p.33, "2021 - Řádný 14:00" (a)**
- Task: "Petriho siet M/M/1. Ked bude vo fronte 5 poziadaviek, zmeni sa to na M/M/3 natrvalo"
- Solution (whiteboard titled "M/M/1 ⇒ M/M/3"):
  - Source transition exp(x), with no generator place → Q → seize (L, 1 token) → busy → exp(y) → L and out → sink.
  - Transition "P=1": test arc **5/5** on Q, input from a once-only place (1 token), output arc weight **2** to L.

**A11. p.34, "2021 - Řádný 16:00" (a)**
- Task: "M/M/1 s údržbou". No solution. It is possibly the same task as A4.

**A12. p.35, "2021 - 1. opravný 9:00" (a)**
- Task: "Pokud od doby poslední obsluhy uplynulo méně než 10jč. (jednotek času), další transakce bude obsluhována 2jč., jinak 5jč. (M/D/1)"
- Follow-up question 3: "Popsat onu Petriho síť v 'pseudojazyku vycházejícího ze SIMLIBu'".
- No PN drawing; only an onlinegdb link.

**A13. p.37, "2021 - 1. opravný 11:00" (a)**
- Task: "2. (10b) Modelujte Petriho sítí systém M/M/1 s následujícími specifikacemi' v intervalech daných exponenciálním rozložením se středem x časových jednotek se v systému projeví porucha, která prodlouží právě probíhající obsluhu o 2 čas. jednotky."
- No PN drawing; only a pseudocode link.

**A14. p.38, "2021 - náhradný COVID termín" (a)**
- Task: "2. (10b) Petriho sieť pre M/M/1 kde vzniká porucha každých Exp(50), ktorá predĺži momentálny proces o 5 j.č. Ak pri vytvorení poruchy momentálne neprebieha žiadny proces tak sa nepredlžuje nič."
- No solution.

Pages 2–3 (2017 and "2018 H8*") and p.40–55 (theory) have no Petri exercises.

---

## B. `…/FIT - Příprava 2018-19.pdf`

**B1. p.2–5, "2016" Pr.1 — category (b), plus (d) next-event**
- Task (photo):
  > "1. (15 bodů) Napište pseudokód algoritmu řízení diskrétní simulace typu 'next-event' (nesmíte použít speciální ukončovací událost). POZOR: bude-li chybět, -5b. Mějme model systému typu D/D/3 se společnou LIFO frontou. Příchody požadavků začínají v čase 0 s intervalem 1s a doba obsluhy trvá 5s. Simulace bude provedena pro čas od 0 do 99s. Požadavky číslujte od 0 podle pořadí příchodu. Priorita všech událostí je 2 (Priority==2). Zařízení (číslovaná od 0) jsou obsazována prioritně (nižší číslo zařízení = vyšší priorita). Události vhodně pojmenujte (např. 'P0 obsazuje Z0', 'P2 jde do fronty'). Nakreslete časový diagram činnosti simulátoru a napište: • Seznam všech událostí provedených v čase t1 = 10. … • Obsah kalendáře v čase t2 = 10.5 … • Nakreslete Petriho síť systému se značením odpovídajícím času t2 = 10.5."
- Solution: a Gantt chart, events at T=10, and calendar entries T=11 (uvolnění Z1, generování P11), T=12 (uvolnění Z2), T=15 (uvolnění Z0).
- Petri net (photo p.5):
  - Source transition "1s", with no generator place → Q holding **4 tokens** (LIFO contents P3, P7, P8, P10).
  - Three seize transitions with priorities **p=3 (Z0), p=2 (Z1), p=1 (Z2)**, labelled "Z0/Z1/Z2".
  - Each line has its own L place, all **empty**.
  - Each busy place holds **1 token**.
  - Each busy place → timed "5s" → back to its L, and → out → filled sink transition.
- Comments: 20 agree, 0 disagree. "Proč jsou tam už na začátku 4? … LIFO P3,P7,P8,P10 v čase T=10.5".

**B2. p.18–19, "Semestrálna skúška 2017/2018 - skupina 7A" (a)**
- Task: "Př. 1 (15 b) a) Nakreslete Petriho síť pro systém typu M/M/1 s netrpělivými požadavky (požadavek čeká nanejvýš 10 časových jednotek) b) Napište program v SIMLIBU pro systém z předchozího bodu (pozor na volbu typu příslušné obslužné linky)"
- Solution:
  - Gen ⇄ exp(λ) → Q → seize (L) → busy → exp(y) → L and out → sink.
  - Q → timed "10s" → place → sink.
- Comments: "Bacha na jednotky… tam aby asi sekundy být neměly… jinak je to správně (+3)". Showing the exit in the upper branch is optional.
- The SIMLIB uses a Timeout event; commenters point out it matches PePe's model2-timeout example.

**B3. p.28, "…skupina 8H" (a)**
- Task: identical to B2 but "nanejvýš 20 časových jednotek".
- Solution: the same net with exp(λ), exp(µ) and timeout "20".

**B4. p.32–33, "…skupina 8C" (a)**
- Task: "a) Nakreslete Petriho síť pro systém typu M/M/1 s frontou omezenou na 10 transakcí b) … SIMLIB…"
- Solution (low-resolution photo, "Prosim o kontrolu (MK)"):
  - Generator ⇄ Exp(x) → input place.
  - Immediate transition → queue place annotated **c=10** (capacity) → seize (place "Obsluha", 1 token) → busy → Exp(y) → back to Obsluha, and → "opuštění systému" → hatched sink.
  - A second transition from the input place leads down to a reject sink.
  - A "p=1" label sits between the two transitions. Most likely the enter-queue transition has priority over rejection.

**B5. p.37–38, "1. opravný termín 2017/2018 - skupina B" (a)**
- Task: "Př. 1 (10 b) Nakreslete Petriho síť pro systém typu M/M/1 s obslužnou linkou 'automat na kafe'. Automat sa po každých 5 časových jednotkách nevytíženosti přepne do režimu údržby (není k dispozici) na dobu 20 časových jednotek."
- Solution (photo rotated 90°, "Správně - 3x"):
  - Generator ⇄ Exp(x) → Q → seize (L) → busy → Exp(y) → L and "opuštění systému" → sink.
  - "Nevytíženost" branch: L → timed "5" → place → timed "20" → L.
  - The 5-unit timer is preempted when a seize takes the L token.
- SIMLIB attempts and pseudocode follow.

**B6. p.48, "2. opravný termín 2017/2018 - skupina A" (a)**
- Task: "Př. 3 (10 b) Nakreslete Petriho síť pro systém typu M/M/1. V intervalech daných exp(X) se na lince vyskytne porucha, která způsobí, že první následující transakce bude mít dobu obsluhy o 10 časových jednotek delší"
- Solution:
  - Gen ⇄ exp(x) → Q → immediate seize (L, 1 token) → place A.
  - A → immediate "p=1" (also takes failure place F) → place → timed "10" → place B.
  - A → immediate (p=0) → place B.
  - B → exp(y) → L and out → sink.
  - Failure subnet ("Porucha"): place (1) ⇄ exp(X) → F.
- Comments disagree:
  - Label exp(x) vs exp(X) is confusing ("dal bych tam … Z").
  - "Za mě je to špatně, protože těch poruch se tam může nakumulovat víc".

**B7. p.51, "řádný termín 2018/2019" (a)**
- Task (from memory): "Velmi jednoduchá Petriho síť typu X/Y/1. Já jsem měl konkrétně M/M/1 … automat na kávu, který při vydávání kávy zabere obslužnou linku a pokud u obslužné linky není fronta po dobu 5 časových jednotek … tak přejde do nečinného režimu na dobu 20 časových jednotek."
- No solution. It is the same as B5.

---

## C. `…/Bug - Řešené otázky.pdf` (section "SIMLIB a Petriho siete")

**C1. p.10 (a)**
- Task: "Vymyslite príklad systému hromadnej obsluhy typu M/M/1, ktorý bude demonštrovať netrpezlivú transakciu vo fronte u zariadenia. Zostavte jeho model v Petriho sieti aj v SIMLIBe."
- The net is the **same image as A1** ("Automat na bagety", 5m). The SIMLIB uses Timeout(300) and `delete t`.
- No term is stated.

**C2. p.11 (a)**
- Task: "Petriho sieť bola typu M/M/1, ak dĺžka fronty presiahne 5, tak sa SHO prepne na M/M/2 na 15 jednotiek času. Taktiež zapísať v SIMLIBe. Nápoveda: Treba využiť Store a meniť kapacitu v závislosti na dĺžke fronty. Možno riešiť aj bez Petriho siete."
- The net is the **same image as A5**.
- The SIMLIB uses `QueueLen() >= 5 && Capacity == 1` and a Wait(15) process. Again ≥5, not >5.

---

## D. `…/xenix - Příprava.pdf`

**D1. p.10–11, D/D/3 (b)**
- Task (photo), a variant of B1:
  > "Mějme model systému typu D/D/3 se společnou LIFO frontou. Příchody požadavků začínají v čase 0 s intervalem 1s a doba obsluhy trvá 5s. … Neuvažujte priority transakcí (všechny jsou stejné). Zařízení … obsazována prioritně (nižší číslo zařízení = vyšší priorita). … Seznam všech událostí provedených v čase t1 = 6. … Obsah kalendáře v čase t2 = 10.5 … Nakreslete Petriho síť systému se značením odpovídajícím času t2 = 10.5."
  - Differences from B1: t1 = 6 instead of 10, and no "Priority==2".
- Solution: a digital Gantt chart, events at T=6, and the same calendar as B1.
- Petri net (draw.io):
  - Source "1s" → Q = **4**.
  - Three seize transitions with priorities **p2, p1, (none = 0)**. L places are empty; busy places hold 1 token each.
  - Busy → "5s" → back to L. There are no exit places.
- Oddity: the T=6 event list says "FIFO poslední z fronty" even though the queue is LIFO.

**D2. p.26, "M/M/1 s netrpělivými požadavky (čeká X)" (a)**
- Solution:
  - Source exp(t) → place → transition T1, which takes L (1 token) and outputs to busy **and** to a timer place.
  - Busy → exp(x) → L and a place → T_done, which also consumes the timer token → exit.
  - Timer → "X č.j." → place → T_timeout, which also consumes the busy token → exit.
- **Apparent errors:**
  - The timer starts at seize, so this models a limit on service time, not on time spent waiting in the queue.
  - The timeout branch never returns the L token, so the line is lost.

**D3. p.26, "M/M/1 s frontou omezenou na 10 transakcí" (a)**
- Solution:
  - Gen ⇄ exp(x) → input place.
  - Immediate "p=1" takes 1 token from a **complement place "10"** (10 tokens) → queue place.
  - Immediate seize (L) returns a token to "10" → busy → exp(y) → L and out → sink.
  - Input place → immediate reject sink (lower priority).
- This is cleaner than B4's capacity annotation.

**D4. p.26, "M/M/1 exp(200) porucha zruší obsluhu" (a)**
- Solution:
  - Gen ⇄ exp(X) → Q → hatched seize (L) → busy → exp(Y) → L and out place.
  - Failure: place ⇄ exp(200) → F.
  - F → "p=0" sink discards a failure when nothing is in service.
  - F + busy → "p=1" → L, plus a long arc to Q labelled "návrat zrušeného procesu".
- The "zruší" wording suggests the transaction should leave, but the drawing returns it to the queue. That matches A7's task.

**D5. p.27, "M/M/1 po 5 nevytíženosti údržba 20" (a)**
- The **same photo as B5**.

**D6. p.27, "M/M/3 20%priorita, 2 linky" (a)**
- Solution (header: "M/M/3 20% TRANSAKCÍ PRIORITNÍ, ZABÍRAJÍ 2 LINKY"):
  - Gen ⇄ EXP(x) → Q → 20% / 80% → branch places.
  - Priority branch: "P=1" takes **2** tokens from L → place → service → out → sink.
  - Normal branch: takes 1 token from L → place → EXP(y) → L and out → sink.
- **Differs from A2:**
  - The return arc from the priority service to L has no weight, so it returns 1 token and leaks a line.
  - L appears to hold only 1 token; it should hold 3.

Pages 18–19 are D/D/2 and D/D/3 calendar exercises with no Petri net requested.

---

## E. `…/fifinas - Tabule ze streamu.pdf` (Xournal export, stream of 17.1.2022)

The task statements are handwritten headings, so the texts below are reconstructions.

**E1. p.2, "A) M/M/1, porucha s Exp(x) na C jednotek" (a)**
- Reconstruction: failures arrive every Exp(x) and occupy the line for C time units, preempting service.
- Solution:
  - Gen ⇄ Exp(a) → Q → seize (L, 1 token) → busy → Exp(b) → L. L and busy are circled in green.
  - Failure: place ⇄ Exp(x) → F.
  - "p=1" takes F + L (idle case) → place → timed "C" → L.
  - A second transition (circled in red) takes F + busy and feeds the same pre-C place. The interrupted transaction is dropped.
- SIMLIB: `Seize(linka, 2); Wait(C); Release`.

**E2. p.3, "B) M/M/1 každá 10. vyvolá poruchu ⇒ C" (a)**
- Reconstruction: every 10th completed transaction triggers a failure lasting C.
- Solution:
  - Exp(b) outputs to a counter place "Cnt" and a release place.
  - Transition with Cnt arc weight 10 + release (probably the priority one; a "p=1"-like mark sits nearby) → place → C → L.
  - Otherwise, release → transition → L.
- Code: `done++; if (done >= 10) { Wait(C); done = 0; }`

**E3. p.4, "C) M/M/1, jestliže aspoň C, tak gen Exp(A), jinak Exp(B)" (a)**
- Reconstruction: the arrival rate depends on queue length ≥ C.
- Solution: two generator places, black with Exp(b) and green with Exp(a). A mode token switches between them through red/blue priority transitions "p=2" (test arcs of weight C on Q) and "p=1".
- The drawing is heavily overdrawn, so the exact arcs are uncertain.
- Code: `if (linka.queue.Length() >= C) Activate(Time + Exp(A)); else Activate(Time + Exp(B));`

**E4. p.5, "D) M/M/1, pokud obsluha ≥ C, pak údržba D" (a)**
- Solution:
  - Seize outputs to busy and to "Timer C".
  - Busy → Exp(b) → done place.
  - Timer → timed C → place. Done + C-elapsed → place → timed "D" → L.
  - Green: done + (unexpired) timer → L directly.
- A side sketch of two conflicting transitions is marked "1:1" in red.
- Code: `wait = Exponential(..); Wait(wait); if (wait >= C) Wait(D);`

---

## F. `…/luppo - Tabule.png` (16200×6163 whiteboard)

These are tasks Z3–Z13 plus the lecture slide "Příklad: kravín". No exam term is stated; they look like a course problem set. All are category (a). Each is a complex hand-drawn net; I give the main structure only.

Whiteboard annotations:
- A red outline around the left part (kravín, Z3, Z4, Z5) carries "No valid ↑", "This is not good", "ehh?" (near Z5) and a red "?" (near Z6).
- A green outline around Z7 carries "This cesi good".

**F1. Příklad: kravín**
- Task: "Kravín má 100 krav, 5 dojiček, 1 nakládací rampu, 2 auta. Krávy v intervalech exp(15h) potřebují podojit (dojička, 10% případů trvá exp(15min), jinak exp(8min)). Vznikne konvice s mlékem. Nakládají se na rampě do auta (kapacita 20). Auto náklad odváží (1hod). Identifikovat procesy."
- Solution:
  - Krav(100) → Exp(15h) → wait → seize Dojička(5) → 90% / 10% → Exp(8min) / Exp(15min) → transition "Mléko", which returns the cow and the milkmaid and produces Mléko.
  - Mléko + Rampa(1) + Auto(2) → "Nakládání" → transition "Je kap?" (takes Kapacita(20)) → "Naloženo".
  - Weight-20 transition → 1hod → back to Auto, and Kapacita returned with weight 20.

**F2. Z3**
- Task: "Přečerpávací vodní elektrárna je složena ze dvou nádrží A a B. Každá nádrž má kapacitu 1000 jednotek vody. V počátečním stavu jsou obě naplněny 500 jednotkami vody. Elektrizační soustava pracuje v běžném denním provozu 16 hodin a v nočním provozu 8 hodin. V běžném denním provozu se spouští voda z nádrže A do nádrže B rychlostí jednotka vody za 4 minuty. V běžném nočním provozu se čerpá z B zpátky do A rychlostí jednotka vody za 1 minutu až do vyprázdnění nádrže B. V intervalech daných exponenciálním rozložením se středem 100 dní dochází k havárii v soustavě. Pokud tato havárie nastane v běžném denním provozu, pak elektrárna zvýší produkci tím, že spouští vodu z A do B rychlostí jednotka vody za 1 minutu do vyčerpání zásob, nejvýše však 3 hodiny. Potom se vrací do režimu dle denní doby."
- Solution:
  - A(500) and B(500) places.
  - Day/night clock: den → 16h → noc → 8h, with test places "Den"/"Noc".
  - Transitions "4min" (A→B) and "1min".
  - Exp(100) → "Můžu přečerpat" → 3hod timer.
- Inside the red "not valid" zone.

**F3. Z4**
- Task: "Bagrista má odstranit zeminu z 1000 metrů dlouhého úseku pro stavbu silnice. Zeminu ukládá na jedno aktuálně přistavené nákladní auto. V systému jsou 3 nákladní auta, která jsou v počátečním stavu přítomna na stavbě. Jedno auto pojme zeminu z úseku 3 metrů stavby. Bagrování jednoho metru úseku trvá dobu danou exponenciálním rozložením se středem 5 minut. Naložené auto odjíždí a vrací se prázdné za dobu danou expenciálním rozložením se středem 1 hodina." The rest is struck through: "Pokud bagrista nemá přistaveno nákladní auto, přeruší práci a odchází na dobu 10 minut do nedalekého stánku s občerstvením."
- Solution:
  - Bagrista(1) → "Bagr" (P=2) → Bagrujeme → Exp(5min), consuming from the 1000 place.
  - Loaded-metre place → P=2 transition with weight 3 that also takes from Nákladní auto(3) → Exp(1hod) → … → back to auta, then Out.
  - 10min "Bufet" loop.
- Margin note: "3 metry kapacita".

**F4. Z5**
- Task: "Životní cyklus překladiště se skládá z osmihodinové pracovní doby a 16 hodin odpočinku. Auta s nákladem přijíždí na rampu překladiště pouze během pracovní doby v intervalech daných exp. rozložením se středem 10 minut. Auto je přistaveno na rampu a čeká dokud z něj jeřáb nevyloží 1 jednotku nákladu. Jeřábník přesouvá jednotku nákladu z auta do místa určení dobu danou exponenciálním rozložením se středem 3 minuty. Pokud nemá 10 minut co přesouvat (na rampě není auto), pak jeřábník vyráží na obchůzku po překladišti, která trvá 5-10 minut rovnoměrně."
- Partial or unfinished solution:
  - Rest/Work cycle (8h / 16h) with "Rest check"/"Work check".
  - Auto ⇄ Exp(10) → Rampa → "Je auto" → Exp(3).
  - Jeřáb, Čekání → 10min, Obchůzka Rov(5–10).
- Marked "ehh?".

**F5. Z6**
- Task: "Do nemocniční ambulace přicházejí stále pacienti v intervalech daných exp. rozložením se středem 20 minut. Po příchodu jsou registrováni u přepážky objednávání a registrace pacientů (1-2 minuty). Ambulance obsahuje dva lékaře, kteří vyšetřují čekající pacienty. Doba vyšetření se řídí exp. rozložením se středem 10 minut. V intervalech daných exp. rozložením se středem 5 hodin sanita přiveze do nemocnice dodávku urgentních pacientů. Oba lékaři přeruší svou případnou práci v ambulanci a opouští ordinace na dobu 3-4 hodiny k urgentnímu zásahu. Aktuálně rozpracovaní pacienti u registrační přepážky prioritně provedou přeobjednání (1-2 minuty) a opustí systém. Ostatní pacienti v čekárně čekají dále."
- Solution:
  - Exp(20min) → Přepážka → 1–2min → Čekárna → Exp(10min), with Lékaři (2 tokens).
  - Sanita ⇄ Exp(5hodin) → "p=2" takes both doctors (weight 2) → 3–4h → returns 2.
  - Branch to 1–2h re-booking.

**F6. Z7**
- Task: "Hudební rádio pouští písničky, reklamy a rozhovory s posluchači, kteří si přejí přehrát oblíbenou písničku. Písnička hraje po dobu 3-5 minut. Redaktor rádia přehrává písničky ze svého seznamu a kromě toho musí každou hodinu začít přehrávat reklamní stopu o délce 5 minut. Posluchači volají do rádia v intervalech daných exp. rozložením se středem 20 minut. Posluchač je vpuštěn do vysílání až potom, kdy dohraje písnička, případně reklama (reklama má přednost před posluchačem). Rozhovor s posluchačem trvá 1-2 minuty. Reklama přeruší přehrávání písničky i rozhovor s posluchačem. Přerušená písnička se neopakuje. Přerušený rozhovor se opakuje od začátku."
- Solution:
  - Posluchač ⇄ Exp(20min) → "Zavola" (takes Redaktor) → 1–2min → Písnička 3–5.
  - Reklama ⇄ 1hod → preemption transitions "Roz"/"Music" → 5min.
- In the green "This cesi good" region.

**F7. Z8**
- Task: "Zahradník na FIT má každý den zalít 30 květin v květináčích. Květiny obchází s konvicí o kapacitě 10 jednotek vody. Květina s pravděpodobností 20% vyžaduje 3 jednotky vody, jinak 4 jednotky vody. Zahradník napustí konvici do plné kapacity za 60 sekund. Cesta mezi zdrojem vody a libovolným květináčem nechť je 2-5 minut. Cesta mezi květináči nechť je dána exp. rozložením se středem 1 minuta. Pokud u květináče zahradník zjistí, že daná květina vyžaduje více vody než má aktuálně v konvici, pak se vrací vodu (cesta ke zdroji a zpět) v konvici doplnit. Zalití květiny trvá vždy 20 sekund. Zahradník je na počátku u zdroje vody a má naplněnou konvici. Modelujte jeden den [rest struck through]."
- Solution:
  - Zahradník(1) → 2–5min → Start, which takes from Květiny(30).
  - "T get spotted" → 20% / 80% → water consumed from konvice(10) with weights 3 / 4 → "Zalito" 20s.
  - "Musím naplnit" with priorities P1/P0 → 2–5 → refill with weight 10.

**F8. Z9**
- Task: "Do školní menzy přichází studenti v intervalech exp(3 min). Jídlo vydává 5 kuchařek. Doba obsluhy jednoho studenta kuchařkou se řídí exp(1min). Po obdržení jídla student konzumuje po dobu 10-15 minut rovnoměrně. V intervalech exp(100 dní) dostává menza hlášení o žloutenkové karanténě. Po příchodu hlášení se ukončí okamžitě všechny činnosti (výdej, konzumace) a úplně všichni studenti opustí menzu. Po odchodu všech studentů z menzy se zahájí karanténa trvající 10 dní. Příchodem hlášení se zastaví proces příchodu studentů do menzy."
- Solution:
  - Studenti ⇄ Exp(3min) → Příchod → seize Kuchařky(5) → Obsluha Exp(1min) → Žere Rov(10–15) → Odchod.
  - "Přerušení Žloutenka" ⇄ exp(100) → Hlášení, which feeds "p=2" flush transitions and a 10-day transition.

**F9. Z10**
- Task: "Pracovní doba úřadu je 8 hodin, po kterých následuje 16 hodin volna. Do úřadovny přichází klienti v období pracovní doby v intervalech exp(10min). Agendu klientů vyřizují úředníci na třech přepážkách. Zpracování jednoho klienta trvá dobu exp(15min). Pokud počet klientů ve frontě k přepážkám dosáhne počtu 10 klientů, úřad na dobu 2 hodin otevře tři další dodatečné přepážky. Po ukončení pracovní doby opouští všichni klienti ve frontě úřad (rozpracovaní klienti jsou dokončeni) a po uvolnění klientem se taky okamžitě uzavřou případné dodatečné přepážky."
- Solution:
  - Work/Rest cycle 8h / 16h.
  - Client ⇄ exp(10) → Q → Úředníci(3) → exp(15).
  - Test arcs 10/10 on Q → "Noví úředníci" → +3 → 2h → "P=3" removal.
  - "P=1000" flush at end of day.

**F10. Z11 (mostly struck through)**
- Task: "Systém vodní přečerpávací elektrárny je tvořen dvěma nádržemi A a B, obě s kapacitou 600 jednotek vody. Režim systému se dělí na: 1) denní etapu výroby (16 hodin), kdy se voda spouští z elektrárny B do A rychlostí 1 jednotka vody za 2 minuty do vyčerpání zásob a na 2) noční etapu spotřeby, kdy se voda z A čerpá do B rychlostí 1 jednotka za 1 minutu. V intervalech daných exp(10 dní) dochází v elektrizační soustavě k havárii vyžadující zvýšenou spotřebu elektřiny. Havárie trvá 1 hodinu. Pokud k havárii dojde v noční etapě, pak se na dobu havárie práce elektrárny přepne do denního (výrobního) režimu. Po dokončení havárie pokračuje systém v práci dle aktuální denní doby. V počátečním stavu začíná denní etapa a stav v nádržích je A: 0, B: 600."
- Solution:
  - B(600) and A(0); 2min and 1min transfer transitions.
  - den/noc clock (16h / 8h) with "Den token"/"Noc token".
  - Porucha ⇄ exp(10) → "P=2" → 1hod; "p=2" green override.

**F11. Z12**
- Task: "Do centrály přepravní firmy přichází balíky k rozvozu v intervalech exp(20min). Firma zaměstnává jednoho řidiče, který balíky z centrály rozváží autem o kapacitě 20 balíků. V systému rozlišujeme nově podané A-balíky a B-balíky, u kterých se zatím nepodařilo zastihnout adresáta. Řidič vyráží z centrály po plném naložení auta A-balíky. Dobu nakládání balíku zanedbáváme. Doba každé cesty (z centrály k adresátovi, mezi adresáty, zpět do centrály) se řídí exp(10min). Zastávka u každého adresáta trvá rovnoměrně 3-5 minut. Adresát je s pravděpodobností 20% nezastižen a balík se tudíž vrací do centrály. Balíky s nezastiženým adresátem (tzv. B-balíky) se odkládají na další pokusy o doručení. Dobu vykládání B-balíků zanedbáváme. B-balík se stává A-balíkem po 24 hodinách. V počátečním stavu nejsou v systému žádné B-balíky."
- Solution:
  - A-Balík ⇄ exp(20) → place → transition taking 20 (weight 20) plus Řidič → "Vzum".
  - exp(20) [should be exp(10)] → 3–5min → 80% "odevzdán" / 20% → 24h → back.
  - Counter weight 20.
- Label slip: the drawing has exp(20) where the task says exp(10min).

**F12. Z13**
- Task (first sentence struck through): "V regionu dochází ke vzniku požárů v intervalech daných exponenciálním rozložením se středem 8 hodin. Centrála hasičů dostává hlášení o novém požáru okamžitě po jeho vzniku. Nehašený požár trvá 2-3 hodiny, tj. po uplynutí této doby žádost o pomoc hasičů zaniká. Hasičská centrála má 5 hasičských vozů. K běžnému požáru je třeba výjezd jednoho vozu. Doba cesty vozu ke každému požáru se řídí exp 10 minut (symetricky cesta zpátky). Hašení požáru trvá 30-60 minut. V intervalech daných exp rozložením se středem 1 týden dochází k požáru extrémního rozsahu, která vyžaduje výjezd všech dostupných požárních vozů (všechny vozy dostupné v centrále, všechny vozy po návratu z běžného požáru). Extrémní požár po 10 hodinách skončí, tj. pak se vozy vrací."
- Solution:
  - Požár ⇄ exp(8hodin) → "Dostali jsme hlášení" → 2–3h "Vyhořelo" (expires) vs dispatch with Vůz(5) → exp(10) → 30–60min.
  - Extrémní: exp(1t) → "Hoří Token" → "P=2" takes all 5 → exp(10) → 10h.
- Red notes: "Fakt cokolí na Tranta?", "Požár LMAO".

---

## G. `…/cranycrane - Kódy (generátory, Monte Carlo, Euler, RK, Petri + SIMLIB)/petri/`

Each item is a PNG (stream screenshots or paper) plus a SIMLIB `.cpp`. The README says only "Nakreslené Petriho sítě a jejich implementace". In the drawings, black is the base M/M/1 and green/purple/orange are added parts.

**G1. 1.png / 1.cpp (a)**
- Task (header): "M/M/1, pokud délka fronty přesáhne 5 – M/M/2 na 15j času". Same as A5 / C2.
- Net:
  - Gen ⇄ exp(A) → Q → seize (L) → busy → exp(B) → L and out → sink.
  - Green switch: test arc **6/6** on Q, plus orange mode place (1 token) → place → transition → +1 to L, and to purple place.
  - Purple: → **exp(15)** → place → "p=1" takes 1 from L → place → sink. Orange arc returns the mode token.
- Disagreements:
  - The net uses exp(15) where A5 uses a constant 15.
  - Weight 6 (>5) here vs 5 in A5.
- .cpp: Store capacity 1. `if (QueueLen() > 5) new Nova_linka` → SetCapacity(2), Wait(Exponential(15)), SetCapacity(1). There is no guard against repeated activation, unlike the PN's mode token. No main().

**G2. 2.png / 2.cpp (a)**
- Task (photo crop): "3. (10 bodů) Pro následující systém nakreslete jeho model v Petriho síti. Systém typu M/M/1. Pokud právě probíhající obsluha přesáhne délku X č.j., pak je přerušena a její transakce opouští systém." Same as A6.
- Net: base M/M/1. Green: busy → timed "X" → L, and → place → sink.
- .cpp: `Wait(min(Exponential(B), X))`.
- **Bug:** Generator::Behavior never creates a transaction (`(new Rob_neco)->Activate()` is missing). No main().

**G3. 3.png / 3.cpp (a)**
- Task (photo): same as A7 ("…porucha, která přeruší případnou právě probíhající obsluhu a transakce se vrací do fronty").
- Net:
  - Green failure generator ⇄ exp(X) → F.
  - "p=1" takes F + busy → Q and → L, plus a further output place → transition (off-screen, purpose unclear).
  - A lower-priority transition from F discards the failure, which fixes A7's accumulation problem.
- .cpp: `if (linka.Busy()) { Release(linka); (new Rob_neco)->Activate(); }`. The author's comment admits it creates a new transaction instead of returning the original. Also, in SIMLIB, Release by a non-owner process is invalid.

**G4. 4.png / 4.cpp (a)**
- Task (photo): same as A1 ("…netrpělivou transakci ve frontě…").
- Net: base M/M/1 with seize at "P=1". A green, lower-priority immediate transition from Q → place → orange sink.
- This models **balking** (leave if the line is busy) rather than a timeout.
- .cpp: `if (linka.Busy()) return;`, which matches the net. It is a different interpretation from A1, B2 and B3.

**G5. 5.png / 5.cpp (a)**
- Task (header): "Petriho siet M/M/1. Ked bude vo fronte 5 poziadaviek, zmeni sa to na M/M/3 natrvalo". Same as A10.
- Net: green switch transition with test arcs **5/5** on Q, input from a once-only place (1 token), output arc weight **2** to L. Identical to A10.
- .cpp: Store(1); an Increase_cap process per arrival does `if (QueueLen() >= 5) SetCapacity(3)`.

**G6. 6.png / 6.cpp (a, task inferred)**
- Task (from the .cpp comment): "M/M/3 bez fronty, neobsloužené transakce se vrací po X časových jednotkách."
- Net (paper; the top shows unrelated "return p*10"):
  - Gen ⇄ Exp(a) → arrival place → "p=1" seize from L (**3 tokens**) → busy → Exp(b) → L and out place (no sink).
  - Lower-priority immediate transition from the arrival place → wait place → **Exp(x)** → back to the arrival place.
- Mismatch: the code uses a constant `Wait(X)` and Store(3) with `Full()`.

**G7. 7.png / 7.cpp (a, task inferred)**
- Task (from the .cpp comment): "M/M/1 který demonstruje použití priority obsluhy každé 10. transakce – petriho síť + kód bez mainu a generátoru".
- Net:
  - exp(A) also feeds a "Counter" place.
  - Normal seize (Q + L) → busy → exp(B) → L and out → sink.
  - "p=1" takes Q, Counter with weight **10**, and the busy token. It outputs back to Q (the preempted transaction) and to busy (the new one).
- Weaknesses:
  - It only fires when the line is busy. Otherwise the counter keeps growing past 10.
  - It cannot tell which queued token is the 10th.
- .cpp: `counter++; if (counter == 10) Seize(linka, 1)`. **Bug:** counter is never reset, so only the 10th transaction ever gets priority.

**G8. 8.png / 8.cpp (a, task inferred)**
- Task (from the .cpp comment): "M/M/1, každých exp(4h) údržbář, pokud 10 obsluh od jeho poslední návštěvy, tak počká na dokončení právě probíhající obsluhy a zahájí údržbu na 20MIN, jinak pokračuje v obchůzce".
- Net:
  - Exp(B) outputs to a "line freed" place and a counter.
  - Freed → immediate → L.
  - Worker place (1) → exp(4h) → arrived place.
  - "P=2" takes arrived + freed + counter with weight **10** → place → "20" → L.
  - "P=1" takes counter tokens one at a time while the worker is present (reset).
  - The lowest-priority transition returns the worker.
- **Apparent errors:**
  - After maintenance, the "20" transition returns only L, not the worker. The worker never comes back.
  - If the line is busy when the worker arrives, P=1 drains the counter, so maintenance is skipped. That contradicts "počká na dokončení".
- .cpp: uses `counter == 10` instead of ≥10; sets Priority = 100 before Seize.

---

## Files with no Petri exercise

- `…/adosi - Úlohy na rozložení 2019-21.pdf`: probability distribution tasks only.
- `…/empire - Řešené statistické příklady.pdf`: statistics, generators and Markov theory only.
- `…/Fituška - Souhrn témat 2010-11.pdf`: Markov, Euler, SIMLIB NAND, cellular automata, fuzzy, D/D/x calendar; no nets.
- `…/Fituška - Řešené příklady 2016.pdf`: one definition only (see the theory list).
- `…/brug - Shrnutí teorie.pdf`: theory mentions only.
- `…/professor - Teorie.pdf`: theory mention only.
- `/home/adam/Documents/Knowledge/Vzdělání/FIT/6. semestr/IMS - Modelování a simulace/Fitcheats/Zkouškové otázky a nejčastější chyby/Nejčastější otázky 2016-20.png`: no exercise. It is a bar chart "Poslední 4 roky v IMS" showing "Petriho síť" with about 7 occurrences, tied with "Generátor čísel" and behind "Dif. rce" and "Teorie" (about 9 each).
- Not on your list but in the folder: `FIT - Teoretické otázky.pdf`, `M-M-3 bez fronty - Rovnice ustáleného stavu.pdf` and `Runge-Kutta 3. řádu - Vysvětlený příklad.pdf` contain no Petri content.
- The cranycrane `algo/` folder has no Petri content.

## Theory-only Petri content (no exercises)

- **Anki deck "Anki balíček IMS (2024).apkg"** (124 notes): three passing mentions, under "Příklady abstraktních modelů", "Deklarativní modely" and "Markovský řetězec".
- **Anki deck "Quaky - Anki balíček IMS (2024).apkg"** (66 notes):
  - "Matematická definice Petriho sítě" Σ=(P,T,F,W,C,M0).
  - "Petriho síť" (uses).
  - "proveditelnost přechodu", with a slide image of a weight-2 arc.
  - "prioritní přechody" (higher number wins; default 0).
  - "inhibiční hrany" ("Pro vytvoření cyklů"), with a while(N>0) slide net using p=1 and an inhibitor arc.
  - "pravděpodobnost provedení přechodu", with a 30%/70% slide net.
  - "Deklarativní modely".
- Fituška Řešené 2016 p.9: a one-line definition.
- Mentions in brug p.2–3, professor p.2, xenix p.3 and p.25, Bug p.18, and FIT Řešené p.13, p.46 and p.47.
- fifinas p.12: a small seize/release Facility net drawn only as an illustration for "Simlib Facility implementace".

## Duplicates and variants

1. **Impatient transaction, M/M/1 (PN + SIMLIB, 20 b):**
   - A1 (2019/20 1. opravný) is the same image as C1 (Bug p.10).
   - A8 (2020 2. opravný C) has the same task text with no net.
   - G4 interprets it as balking.
   - Related tasks with a fixed wait limit: B2 (10 units, 2017/18 7A), B3 (20 units, 8H) and D2 (X, with the timer-placement and lost-line errors).
2. **Queue >5 → M/M/2 for 15:**
   - A5 (2019 2. opravný) is the same image as C2.
   - G1 differs: arc weight 6 vs 5, and exp(15) vs constant 15.
   - The SIMLIB tests also differ: C2 uses ≥5, G1 uses >5.
3. **M/M/3, 20% priority needing 2 lines:** A2 (2019) vs D6. They disagree on return weight 2 and on L's initial marking (3 vs 1).
4. **Service exceeds X → interrupted, transaction leaves:** A6 (2020 1. opravný) ≈ G2. E4 is related (service ≥ C → maintenance).
5. **Failure exp(X) interrupts service, transaction returns to queue:** A7 (2020 1OP B) vs G3 vs D4 (exp(200)). A7 lacks the discard transition for failures arriving while the line is idle.
6. **Queue = 5 → permanently M/M/3:** A10 (2021 Řádný 14:00) ≈ G5. Same structure: 5/5 test arcs, weight 2 to L.
7. **Coffee machine, 5 idle → maintenance 20:** B5 (1. opravný 2017/18 B) is the same photo as D5. B7 (řádný 2018/19) is the same task from memory with no net.
8. **Queue limited to 10:** B4 (8C, capacity annotation c=10) vs D3 (complement place "10").
9. **D/D/3 LIFO, marking at t2 = 10.5:** B1 (2016: t1=10, Priority==2, seize priorities 3/2/1, exit sinks) vs D1 (t1=6, no priorities, priorities 2/1/0, no exits). Both have Q=4 and 1 token in each busy place.
10. **Service time depends on queue length:** A3 (≥X → 5, else 10; weights x / x−1) and A9 (2021 Řádný 10:00; ≥3 → 5, else 10; weights 3/2). Both use exp() for the stated durations, which is disputed in A3's comments.
11. **Maintenance after service when the queue is empty:** A4, and probably the same as A11 (2021 Řádný 16:00, "M/M/1 s údržbou", no solution).
12. **Failure prolongs service:** B6 (+10 for the next transaction, 2. opravný 2017/18 A), A13 (+2 current, 2021 1. opravný 11:00), A14 (+5 current, only if running, 2021 COVID). Related: E1 (failure lasting C), E2 (every 10th causes failure).
13. **Pumped-storage power plant:** luppo Z3 vs Z11.
14. **Every 10th transaction:** E2 (triggers failure) vs G7 (service priority) both use a weight-10 counter place.

All crops and extracts I made are in the scratchpad (`/tmp/claude-1000/-home-adam-Projects-Education-petri-nets/a6f232b0-aee0-42a0-9423-8c1043651165/scratchpad/`); no source files were modified.