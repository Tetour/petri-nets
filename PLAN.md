# Petri nets for IMS: project plan

Goal: one correct, exam-style Petri net diagram for every Petri net exercise in the IMS study material, plus enough explanation to learn from each one.

Status: **all 118 exercises drafted and passing `make check` (§6.2 done). Remaining: polishing crowded diagrams, `make book`, final consistency pass (§6.4).**

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
  - each exercise's note file name, e.g. `09–10 - Kopírovací centrum.md` (folder of the same name);
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
│   ├── sim.py               ← timed token-game simulator (§4)
│   ├── dd.py                ← next-event trace for the D/D/x tasks
│   ├── catalog.py           ← all exercises: id, Czech name, origin (single source of truth)
│   └── index.py             ← regenerates the README index from the catalogue
├── notation/
│   ├── Notace a vzory.md    ← cheat sheet (Czech): course notation + standard patterns, with slide refs
│   └── patterns/*.py        ← generator, seize/release, Store, timeout, preemption, counter, if/else by priority, test arc …
├── exercises/               ← flat, one folder per exercise, ordered by topic (§5)
│   ├── 01–01 - Opravářská dílna/
│   ├── …
│   └── 12–18 - Logistická centrála/
├── book/                    ← generated printable collection (task page, then solution page)
└── inventory/               ← raw source inventory (already present)
```

Each exercise folder:

```
exercises/09–10 - Kopírovací centrum/
├── 09–10 - Kopírovací centrum.md   ← the note (Czech), see below
├── net.py                        ← the net definition (single source of truth)
├── net.svg                       ← generated; embedded in the note (renders in the VS Code Markdown preview)
└── net.pdf                       ← generated; vector, for printing
```

Folder and note are named `<TT–NN> - <název>`. The id carries no origin; the origin is in the note's last section **Původ a zdroje**.

Each note has these sections (headings in Czech):

1. **Zadání**: the verbatim task text and links to similar exercises.
2. **Interpretace** → **Nápověda**: ambiguities and the assumption chosen (e.g. "přesáhne 5" means > 5, so the test arc has weight 6). The section is called *Interpretace* while it is my unconfirmed reading; once you review the note and confirm the interpretation, it is renamed to *Nápověda* („Zobrazit nápovědu“). The README index derives the status `reviewed` from that name.
3. **Petriho síť**: the diagram only. (How each requirement maps to places and transitions belongs in the hints, not in a table here.)
4. **SIMLIB** (being added gradually, so far only 01–01): a SIMLIB/C++ model isomorphic to the net, a table mapping net elements to code, and the simulation check (what `make check` verified on the net and what the SIMLIB run gave).
5. **Časté chyby**: the common mistakes for this pattern.
6. **Původ a zdroje**: where the exercise comes from (exam/midterm, year, term, group, points), every source file with pages, and the comparison with existing solutions (Hrubý's or students' nets, with the errors to avoid).

When a note is opened, only the heading, **Zadání** and the visible part of **Původ a zdroje** are shown. Sections 2–5 and the existing-solutions part of section 6 are collapsed in `<details>` blocks (works in the VS Code preview and on GitHub), so you can try the exercise first and reveal the interpretation as a hint before the solution.

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

Exercises are ordered **by topic** and numbered `TT–NN` (topic – position within the topic). Topics go from basic models over single mechanisms (the short M/M/1-variant exam questions) to marking at time t and full word problems (the midterm format). Within a topic, newer tasks come first. The two-level id keeps numbers stable when an exercise is added later.

| Topic | Content | Count |
|---|---|---|
| 01 | Základní modely (lecture worked examples) | 6 |
| 02 | Netrpělivost, omezená fronta, opakování | 5 |
| 03 | Poruchy a přerušení obsluhy | 11 |
| 04 | Údržba, nečinnost, spánek | 8 |
| 05 | Řízení podle délky fronty a kapacita | 10 |
| 06 | Doba obsluhy podle stavu | 4 |
| 07 | Priority | 6 |
| 08 | Značení v čase t (D/D/x) | 9 |
| 09 | Slovní úlohy: obsluha zákazníků | 22 |
| 10 | Slovní úlohy: počítačové systémy | 5 |
| 11 | Slovní úlohy: doprava a dávky | 14 |
| 12 | Slovní úlohy: výroba, zdroje a sklady | 18 |

The full list (id, Czech name, origin) lives in [pn/catalog.py](pn/catalog.py); the README index is generated from it (`python3 -m pn.index`). Midterm word problems (09–12) are assigned to a topic by their dominant mechanism, judged from the task text. If a closer reading changes that, the exercise moves, but its id stays.

---

## 6. Order of work

0. **Git setup**: `git init`, private GitHub repo, first commit with the plan and the inventory.
1. **Tooling + pilot (5 nets).** Build `pn/` with lint and simulator and the notation cheat sheet. The pilot leans toward the midterm:
   - 09–10 kopírovací centrum (midterm 2022/23; Hrubý's solution exists, to compare);
   - 09–03 psí salon (midterm 2025/26; tests reconstructing a task from a solution);
   - 01–01 opravářská dílna (the lecturer's own net, to calibrate the style);
   - 03–02 failure → back to queue (exam type);
   - 08–02 D/D/3 marking at t = 10.5 (trace type).

   **You review these** for style, language and depth before I mass-produce. This is the cheapest point to change format.
2. **Main batch, midterm first:**
   - word problems (topics 09–12), by year across topics, newest first: 2025/26 → 2024/25 → … → 2010/11, then Z1–Z24 and the extras;
   - then the lecture examples (01);
   - then the mechanism topics 02–07 (newest first);
   - then marking at time t (08).
3. Drafting can run in parallel with subagents, one per batch of years. Each net still goes through `make check` and my visual review. I commit and push after each finished batch.
4. **Finish**: README index, `make book` → one PDF with each task on its own page and the solution on the next page (for practice), and a final consistency pass. Where my net disagrees with Hrubý's, his version wins unless it is demonstrably a different reading, and that gets noted.

Status per exercise in the README index: `todo / drafted / reviewed`.

---

## 7. Risks and limits

- **Legibility.** Some sources are blurry photos (2017-18 3.t Z, 2024-25 3.t H, 2023-24 midterm photos). The README of each such exercise states the uncertain words or numbers.
- **Paraphrased tasks.** Student recollections like "petriho siete M/M/1 s údržbou" are under-specified. I pick the reading closest to sibling tasks and say so.
- **Multiple valid models.** Modelling questions have more than one correct net. I aim for the one closest to Hrubý's style and mention real alternatives (e.g. constant vs. exp duration, ≥ vs. >).
- **Tooling gaps (not blocking).** Graphviz isn't installed, and TeX Live lacks `standalone`/`preview`. TikZ plus a manual page crop works fine. If you want the cleaner route, add `standalone` to your TeX Live package set in the NixOS config.

---

## 8. Possible improvements (later)

- **SIMLIB code** in each note's SIMLIB section (started with 01–01). The code is syntax-checked against a stub header; real compilation needs SIMLIB, which is not in nixpkgs (source: https://www.fit.vut.cz/person/peringer/public/SIMLIB/).
- **Video transcripts** of the 2023 demo exercises, used to cross-check midterm solutions against Hrubý's spoken reasoning.
