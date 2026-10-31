# Petri nets for IMS: project plan

Goal: one correct, exam-style Petri net diagram for every Petri net exercise in the IMS study material, plus enough explanation to learn from each one.

Status: **pilot built (§6.1): tooling, notation cheat sheet and 5 nets, waiting for your review.**

---

## 0. What the material contains

Five read-only sweeps went through every relevant file. Scanned PDFs were read page by page as images. The raw reports, with verbatim task texts and file/page references, are in [inventory/](inventory/).

| Source | Petri net exercises | Existing solutions |
|---|---|---|
| Final exams 2005–2026 (`Zkoušky z minulých let`) | ~66 entries → **44 unique M/M/x tasks + 9 D/D/x marking tasks** | almost none on the papers; student solutions for ~20 of them in the prep compilations |
| Midterms (`Půlsemestrálky`) | **~59 "word problem → net" tasks** (2010–2026 + the Z1–Z24 overview) | Hrubý's own solutions for 2021-22, 2022-23, 2024-25, 2025-26; student solutions for Z1–Z24 |
| Prep compilations (`Příprava na zkoušku`, cranycrane, fifinas, luppo, xenix, Bug) | mostly duplicates of the above; they add a few exam tasks | many student nets, several with real errors (lost facility tokens, failures piling up, a timer on the wrong place) |
| Lectures / MSI notes / scripta | ~6 worked examples + notation slides | the lecturer's own nets |

Key facts:

- **No exercise asks for analysis** (reachability, liveness, invariants). Every task is either *model the described system* or *draw the marking at time t* for a D/D/x simulation.
- **Notation must follow Hrubý's 2025 slides** (123–164, 186–198) and his handwritten solutions, not the MSI notes, which use a different convention. See §3.
- **2025-26 midterm**: only Hrubý's solutions exist; the task texts are missing. Those tasks will be reconstructed from the solutions and flagged as such.
- **Unusable entries**: 2025-26 exam D Q1 (the page was never scanned) and 2020-21 exam 3rd term Q2 ("Petriho sieť", no detail). These are listed but not drawn.
- The lecturer said in the 2024 lectures that the midterm is "one word problem → model it as a Petri net". The final exam's Q1/Q3 is the short M/M/1-variant type.

---

## 1. Decisions I need from you

1. **Which test is it: the midterm (půlsemestrálka, usually mid-November) or the final exam?** This sets the order of work (§6). My default assumption is the midterm, given today's date.
    - The midterm
2. **Language.** Default: diagram labels in **Czech**, as at the exam ("fronta", "linka", "porucha"); explanations in **English**; task statements always verbatim in the original Czech/Slovak. Alternative: everything in Czech.
    - Project structure in English, names of notes and the note text itself in Czech
3. **SIMLIB code.** About 15 exam tasks also ask for SIMLIB pseudocode isomorphic to the net. Default: **not included**, because you asked for diagrams. I can add a `simlib.cpp` for exactly those tasks if you want.
    - Not yet, but please note it as possible improvement
4. **Videos.** The 2023 demo-exercise videos (4×) and the 2024 lectures after 10-18 have no transcripts. The demo exercises very likely contain Hrubý solving midterm tasks, which would be useful as a reference. Default: **skip**. Optional: transcribe them with the video-transcriber tool and use them to cross-check.
    - *(no answer yet; keeping the default: skip)*
5. **Git.** Default: `git init` the project, local only, no remote and no commits unless you ask. Say no if you'd rather not.
    - Local and remote, you can commit and push in this project

**Resulting choices**

- Order: midterm word problems first (§6).
- Language: the project scaffolding is in English (directories `pn/`, `exercises/`, `notation/`, `book/`, file names `net.py`/`net.svg`/`net.pdf`, the top-level `README.md`, `Makefile`, code). Everything that is a note is in Czech:
  - each exercise's note file name, e.g. `M41 - Kopírovací centrum.md`;
  - its headings and text;
  - labels in the diagrams;
  - the notation cheat sheet (`notation/Notace a vzory.md`);
  - the printable collection.
- SIMLIB: not now; listed under §8 as a possible improvement.
- Git:
  - local repository plus a **private** GitHub repo `Tetour/petri-nets`;
  - private, because it contains verbatim faculty exam texts;
  - commits and pushes at sensible checkpoints, with no Claude attribution.

---

## 2. Project structure

```
petri-nets/
├── PLAN.md                  ← this file
├── README.md                ← project doc (English) + index table of all exercises (Czech titles, source, type, status)
├── Makefile                 ← make | make check | make book | make clean
├── pn/                      ← small Python library (no external deps; numpy available)
│   ├── net.py               ← DSL: places, transitions, arcs, positions
│   ├── tikz.py              ← emits TikZ that follows course notation
│   ├── lint.py              ← notation/structure rules (§4)
│   └── sim.py               ← timed token-game simulator (§4)
├── notation/
│   ├── Notace a vzory.md    ← cheat sheet (Czech): course notation + standard patterns, with slide refs
│   └── patterns/*.py        ← generator, seize/release, Store, timeout, preemption, counter, if/else by priority, test arc …
├── exercises/
│   ├── exam/E01-…/          ← final-exam M/M/x variants
│   ├── trace/T01-…/         ← D/D/x "marking at time t"
│   ├── midterm/M01-…/       ← midterm word problems
│   └── lecture/L01-…/       ← lecturer's worked examples
├── book/                    ← generated printable collection (task page, then solution page)
└── inventory/               ← raw source inventory (already present)
```

Each exercise folder:

```
exercises/midterm/M41/
├── M41 - Kopírovací centrum.md   ← the note (Czech), see below
├── net.py                        ← the net definition (single source of truth)
├── net.svg                       ← generated; embedded in the note (renders in the VS Code Markdown preview)
└── net.pdf                       ← generated; vector, for printing
```

Folders are named by id only, so paths stay short and stable; the note carries the Czech name.

Each note has these sections (headings in Czech):

1. **Zadání**: verbatim text, every source where it appears (file + page, term/group, points), and its variants or duplicates.
2. **Interpretace**: ambiguities and the assumption chosen (e.g. "přesáhne 5" means > 5, so the test arc has weight 6).
3. **Řešení**: the diagram plus a table mapping each requirement to the place or transition that implements it.
4. **Existující řešení**: how Hrubý's or students' nets differ, and which of their errors to avoid.
5. **Časté chyby**: the common mistakes for this pattern.

Nets that differ only in numbers stay separate exercises (you asked for every one), but their notes link to each other. The D/D/x trace tasks get one net per parameter set, with that task's marking.

---

## 3. Notation (Hrubý / course 2025)

From slides 128–139 and 151–198 and his handwritten midterm solutions:

| Element | Drawing |
|---|---|
| Place | circle; tokens as dots (≤ 4) or a number inside (e.g. `50`); label beside it |
| Immediate transition | thin white rectangle |
| Timed transition | filled (grey) rectangle, time under it: `exp(10)`, `5`, `uniform(10,15)`, `exp(4h)` |
| Priority | `p=1` beside an immediate transition (higher wins, default 0) |
| Probability | `30%` beside an immediate transition |
| One parameter per transition | never time + priority, never probability + priority (slide 135) |
| Arc weight | integer beside the arc; default 1 |
| Inhibitor arc | small empty circle at the transition end. **Avoided**: Hrubý prefers priority-based if/else, so it is used only where nothing else works |
| Generator | 1-token place in a self-loop with a timed `exp(x)` transition |
| Facility / Store | place with 1 / N tokens; seize = immediate transition, service = timed, release = arc back |
| Exit | immediate transition with no output ("transakce opouští systém"). Required on every net, since the 2022+ assignments demand it |
| Place capacity | not used; complement places instead (Hrubý advises against capacities) |

Rendering: TikZ (`petri` library, already installed) → tight PDF → SVG via `pdftocairo`. I tested this pipeline today and it works.

---

## 4. Correctness checks

Several student solutions in the material are subtly wrong: a facility token never returned, failures piling up while the line is idle, a timeout attached to service instead of to waiting. A wrong net learned for an exam is worse than no net, so every net gets mechanical checks besides my own review.

**`make check` → lint**

- Every arc connects a place and a transition.
- Each transition has at most one parameter; timed transitions carry only a time.
- Probabilities leaving a conflict set add up to 100 %.
- An exit transition exists.
- Every place and transition is reachable from the initial marking.

**`make check` → simulation**

A timed token game:

- Immediate transitions fire before timed ones; priority wins.
- Enabling-memory semantics: a timed transition that loses its token is cancelled. This is exactly the slide 139 breakdown semantics.
- Symbolic parameters (X, C, …) get sample values.
- Each net declares invariants, e.g. `linka + obsluha == 1` or `vozíky + zákazníci_s_vozíkem == 50`.
- A long random run must keep every invariant, fire every transition at least once (a dead transition means a wiring mistake), and not grow places that should stay bounded.

**Trace tasks**

For D/D/x the simulator is deterministic. It computes the marking at the requested time *t*, and the drawn marking is checked against it. Each README also gets the event and calendar trace, so you can check your own work.

**Visual check**

I view every rendered PNG for overlaps and readability before marking an exercise done.

---

## 5. Exercise catalogue (118 diagrams)

Ids are provisional; the README index will link every one.

### E: final-exam M/M/x variants (44)

| Id | Task | Sources (term) |
|---|---|---|
| E01 | M/M/1, impatient requests, max wait W (10 / 20) | 2017-18 1.t A(8H), 7A; 2023-24 1.t A; student nets in Příprava 18-19 |
| E02 | only the **head** of the queue is impatient (5 / X / 4) | 2017-18 2.t A; 2019-20 2.t Y; 2024-25 2.t E (student net) |
| E03 | *invent* an M/M/1 showing an impatient transaction | 2019-20 1.opr; 2020-21 3.t C; Bug, cranycrane 4 |
| E04 | M/M/1 with queue limited to 10 | 2017-18 8C; xenix |
| E05 | failure exp(200) only cancels the service | 2017-18 1.t Z; xenix |
| E06 | failure exp(X) interrupts service → transaction back to queue | 2020 1.opr B; cranycrane 3 |
| E07 | failure Exp(E) occupies line for R, interrupted transaction back to queue | 2024-25 1.t A |
| E08 | failure Exp(X), repair C, interrupted transaction leaves | 2021-22 1.t A/? ; fifinas |
| E09 | critical failure exp(100) disables line for 10, work discarded | 2025-26 1.t C |
| E10 | failure destroys current service **or** waits for the next one | 2021-22 2.t |
| E11 | every 10th transaction triggers failure of length C | 2021-22 1.t B; fifinas |
| E12 | failure makes the **next** service 10 longer | 2017-18 3.t A; Příprava 18-19 |
| E13 | failure prolongs the **current** service by 2 | 2020-21 1.t; Řešené 17-21 |
| E14 | failure prolongs current service by 5, no effect if idle | 2021 COVID term |
| E15 | service longer than X is interrupted, transaction leaves | 2019-20 2.t Z; cranycrane 2 |
| E16 | coffee machine: 5 idle → maintenance 20 | 2017-18 2.t B; 2018-19 1.t |
| E17 | coffee machine: every 50 (40) services → maintenance 20 | 2017-18 2.t C; 2018-19 1.t |
| E18 | sleeps after 5 idle; wake-up adds 2 to the service | 2017-18 2.t D |
| E19 | queue empty after service → maintenance 5 | 2019-20 1.t D; 2020-21 1.t 16:00 |
| E20 | service lasted ≥ C → maintenance D | 2021-22 1.t D; fifinas |
| E21 | every 10th completed service → maintenance C | 2022-23 1.t D |
| E22 | maintenance worker every exp(4h); if ≥ 10 services → wait, 20 min maintenance | 2022-23 1.t C; cranycrane 8 (buggy) |
| E23 | 10 idle → sleep; arrival wakes, 5 min warm-up | 2022-23 2.t F |
| E24 | service 5 if queue ≥ X (3), else 10 | 2019-20 1.t; 2020-21 1.t 10:00 |
| E25 | queue > 5 → M/M/2 for 15 | 2018-19 3.t; Řešené; Bug; cranycrane 1 |
| E26 | queue reaches 5 → M/M/3 permanently | 2020-21 1.t 14:00; cranycrane 5 |
| E27 | arrival mean A if queue ≥ C, else B | 2021-22 1.t C; 2022-23 1.t A; fifinas |
| E28 | arrivals pause for 10 when queue reaches 5 | 2024-25 1.t B |
| E29 | M/M/3: arrivals stop when all busy, resume when ≥ 2 free | 2024-25 1.t C |
| E30 | every 100th transaction flushes the queue | 2022-23 2.t E |
| E31 | Store: periodically +3 capacity for 100 | 2017-18 3.t Z (blurry) |
| E32 | M/D/1: service 3, +3 after every 10 services | 2024-25 2.t F |
| E33 | M/D/1: service alternates 2, 3, 2, 3 … | 2025-26 1.t A |
| E34 | M/D/3: taking the last free server → 5, else 3 | 2024-25 3.t H |
| E35 | M/D/1: < 10 since last service → 2, else 5 | 2021 1.opr 9:00 |
| E36 | *invent* an M/M/1 showing process priority | 2019-20 3.t A |
| E37 | every N-th transaction gets process priority | 2022-23 3.t G |
| E38 | every 10th transaction gets service priority | 2022-23 3.t H; cranycrane 7 |
| E39 | two independent arrival streams, one with service priority | 2025-26 1.t B |
| E40 | process vs. service priority, small demo nets | 2025-26 1.t C Q3 |
| E41 | M/M/3: 20 % priority transactions need 2 lines at once | 2019 (Řešené); xenix |
| E42 | M/M/2: maintenance every exp(100) takes the whole capacity for 10, must not wait | 2025-26 2.t E |
| E43 | M/M/1: helper every exp(100) adds 1 capacity for 20 | 2025-26 2.t F |
| E44 | M/M/3 without queue, rejected transactions retry after X | 2023-24 1.t B; cranycrane 6 |

### T: D/D/x, marking at time t (9)

| Id | System | t | Sources |
|---|---|---|---|
| T01 | D/D/2 FIFO, arrivals 1 s, service 4 s | 6.5 | 2012-13 2.t C |
| T02 | D/D/3 LIFO, 1 / 5 | 10.5 | 2015-16 3.t A; 2014-15 1.t C; Příprava, xenix (student nets) |
| T03 | D/D/2 LIFO, 1 / 6 | 13.5 | 2015-16 3.t D (+ "2005-06" transcript) |
| T04 | D/D/2 LIFO, 1 / 5 | 9.5 | 2014-15 1.t B; 2015-16 2.t |
| T05 | D/D/2 LIFO, 1 / 4 | 9.5 | 2015-16 2.t A |
| T06 | D/D/4 LIFO, 1 / 7 | 9.5 | 2014-15 3.t D |
| T07 | D/D/3 FIFO, 1 / 5 | 9.5 | 2015-16 1.t 5H |
| T08 | D/D/1, 2 / 4: net + state table to 10, stability | — | 2022-23 3.t G |
| T09 | D/D/1, 3 / 2: same | — | 2022-23 3.t H |

### M: midterm word problems (59)

| Year | Ids and tasks | Reference solutions |
|---|---|---|
| 2010-11 | M01 banka + lupič · M02 logistická centrála · M03 chmel · M04 pražírna kávy | student nets for M02–M04 in Studentská skripta |
| 2011-12 | M05 tunel · M06 pošta (100 zásilek) · M07 přehrada, přístaviště A/B · M08 dílna, 3 stroje | — |
| 2013-14 | M09 banka · M10 hrášek · M11 server · M12 stavba (betonáři) | student nets in skripta |
| 2014-19 overview | M13–M36 = Z1–Z24 (loď, uhelný mlýn, přečerpávací el. ×2, bagrista, překladiště, ambulance, rádio, zahradník, menza, úřad, přepravní firma, hasiči, pekárna, spalovna ×2, moštárna, letiště, vyhlídková loď, pošta, festivalový autobus, DB server, jahodová farma, výrobní hala) | demo-exercise solutions (Z4, Z6, Z7, Z16, Z17, Z20, Z24); student nets for most in Příprava 21-22 and luppo |
| 2021-22 | M37 překladiště · M38 jahody · M39 výletní loď · M40 kopírovací centrum | Hrubý |
| 2022-23 | M41 kopírovací centrum · M42 trafika · M43 pizzerie · M44 cestovní kancelář | Hrubý (+ projector photos) |
| 2023-24 | M45 server, maintenance after 1000 (paraphrase) · M46 výpočetní služba (sleep) · M47 automat na kávu · M48 klientské centrum | student sketch for M46 |
| 2024-25 | M49 zahradnictví + bouřka · M50 pizza stánek (paraphrase) · M51 vyhlídkové lety · M52 centrum M/M/1 | Hrubý |
| 2025-26 | M53 psí salon · M54 obslužné centrum · M55 výletní autobus · M56 úřad — **task text reconstructed from Hrubý's solutions** | Hrubý |
| extra | M57 přehrada, vyhlídková loď ("Příklad 3") · M58 zvuková karta · M59 ústředna | student nets |

### L: lecture worked examples (6)

L01 opravářská dílna (slides 157–164) · L02 samoobsluha (195–198) · L03 kravín (lecture example, luppo board) · L04 výrobní systém (MSI) · L05 kritická sekce (MSI) · L06 zdravotní středisko (MSI, redrawn in course notation).

The small notation demos (readers/writers, while loop, 30 %/70 %, breakdown on `exp(10)`) go into `notation/` as patterns rather than exercises.

---

## 6. Order of work

0. **Git setup**: `git init`, private GitHub repo, first commit with the plan and the inventory.
1. **Tooling + pilot (5 nets).** Build `pn/` with lint and simulator and the notation cheat sheet. The pilot leans toward the midterm:
   - M41 kopírovací centrum (2022-23; Hrubý's solution exists, to compare);
   - M53 psí salon (2025-26; tests reconstructing a task from a solution);
   - L01 opravářská dílna (the lecturer's own net, to calibrate the style);
   - E06 failure → back to queue (exam type);
   - T02 D/D/3 marking at t = 10.5 (trace type).

   **You review these** for style, language and depth before I mass-produce. This is the cheapest point to change format.
2. **Main batch, midterm first:**
   - M, newest years first: 2025-26 → 2024-25 → … → 2010-11, then the Z1–Z24 overview and the extras;
   - then L;
   - then E (newest first);
   - then T.
3. Drafting can run in parallel with subagents, one per batch of years. Each net still goes through `make check` and my visual review. I commit and push after each finished batch.
4. **Finish**: README index, `make book` → one PDF with each task on its own page and the solution on the next page (for practice), and a final consistency pass. Where my net disagrees with Hrubý's, his version wins unless it is demonstrably a different reading, and that gets noted.

Status per exercise in the index: `todo / drafted / checked / reviewed-by-you`.

---

## 7. Risks and limits

- **Legibility.** Some sources are blurry photos (2017-18 3.t Z, 2024-25 3.t H, 2023-24 midterm photos). The README of each such exercise states the uncertain words or numbers.
- **Paraphrased tasks.** Student recollections like "petriho siete M/M/1 s údržbou" are under-specified. I pick the reading closest to sibling tasks and say so.
- **Multiple valid models.** Modelling questions have more than one correct net. I aim for the one closest to Hrubý's style and mention real alternatives (e.g. constant vs. exp duration, ≥ vs. >).
- **Tooling gaps (not blocking).** Graphviz isn't installed, and TeX Live lacks `standalone`/`preview`. TikZ plus a manual page crop works fine. If you want the cleaner route, add `standalone` to your TeX Live package set in the NixOS config.

---

## 8. Possible improvements (later)

- **SIMLIB code** (`simlib.cpp`) for the ~15 exam tasks that ask for a SIMLIB model isomorphic to the net (E01, E03, E05, E08, E10, E11, E20, E22, E25, E27, E36–E38, …). The simulator in `pn/` makes it possible to cross-check net and code behaviour.
- **Video transcripts** of the 2023 demo exercises, used to cross-check midterm solutions against Hrubý's spoken reasoning.
