# Petri nets for IMS

Every Petri net exercise from the study material of the IMS course (Modelování a simulace, FIT VUT), solved in the course notation, checked by simulation and modelled in SIMLIB. It is meant for preparing for the midterm (one word problem → model it as a Petri net) and for the Petri net questions of the final exam.

The notes are in Czech; the tooling and these documents are in English.

## Where to start

1. **Notation:** [Notace a vzory](basics/Notace%20a%20vzory.md) is a cheat sheet of the course notation and the standard patterns (generator, facility, store, timeout, failure, counter, …), each with a small net in [basics/patterns/](basics/patterns/). [Jak síť funguje](<basics/Jak síť funguje.md>) explains how a net runs: firing, timed transitions, several tokens, cancelled countdowns.
2. **Exercises:** [Seznam úloh](<exercises/Seznam úloh.md>) lists all 118 exercises by category, with origin and review status. It opens with *Začni tady*: 15 exercises that cover every pattern once and then the newest midterms, a good first round before the midterm.
3. **Practise:** open a note. Only the task (*Zadání*) is visible; every other section is collapsed, so you can try the exercise first and then open the hint, the net, the common mistakes, the SIMLIB model and the sources one at a time. Each note also exists as a PDF next to it, with the task alone on the first page.

The categories go from basic models over single mechanisms (failures, maintenance, priorities, … as in the short exam questions) and marking at time t to full word problems as at the midterm:

```
exercises/
├── 01 - Základní modely/            lecture examples
├── 02 - Netrpělivost a omezená fronta/
├── …
├── 08 - Značení v čase t/           D/D/x marking at time t
├── 09 - Obsluha zákazníků/          midterm word problems, by dominant mechanism
├── …
└── 12 - Výroba a sklady/
    └── 18 - Logistická centrála/
        ├── 18 - Logistická centrála.md    the note
        ├── 18 - Logistická centrála.pdf   the same note as a PDF
        ├── net.py                          the net (source)
        └── net.svg, net.pdf                the rendered diagram
```

## Sources

The exercises come from the course material (outside this repository; paths in the notes are relative to the study folder `IMS - Modelování a simulace/`):

- **final exams 2005–2026:** M/M/x variants (failures, maintenance, impatience, priorities, …) and D/D/x marking at time t;
- **midterms 2010–2026** and the overview Z1–Z24: word problems, with Hrubý's own solutions for 2021/22, 2022/23, 2024/25 and 2025/26 (for 2025/26 only the solutions survive, so those tasks are reconstructed from them) and student solutions for many others;
- **student prep compilations:** mostly duplicates, with student nets, several of them wrong;
- **lectures and MSI notes:** worked examples and the notation.

[source-survey/](source-survey/) is the survey this project started from: every source file, what it contains and where every task was found (page, verbatim text). The notation follows Hrubý's 2025 slides and his handwritten solutions; the MSI notes use a different convention and are redrawn. Each note's last section, *Původ a zdroje*, gives the origin, the original wording and how existing solutions differ, including their errors.

Two exam entries are unusable and not drawn: 2025/26 exam D Q1 (the page was never scanned) and 2020/21 3rd term Q2 (no detail).

## How the notes are made

- [Note.md](notation/Note.md): the structure of a note and the rules for each section (times in the task text, hints, SIMLIB, sources).
- [Style.md](notation/Style.md): how a diagram is laid out.
- **Review:** a note's hint section is called *Interpretace* until you confirm the reading; then it is renamed to *Nápověda*, and the exercise list shows the note as *zkontrolováno*.
- **Limits:** a modelling task usually has more than one correct net. Each net aims at the one closest to Hrubý's style and the hints mention real alternatives (constant vs. exponential time, ≥ vs. >). Where only a student's recollection or a blurry photo of a task exists, a ⚠️ line in the task says so.

## Checks

A wrong net learned for an exam is worse than none, so every net is checked mechanically (`make check`):

- **Lint:** arcs connect a place and a transition; one parameter per transition; probabilities add up to 100 %; an exit transition exists.
- **Simulation:** a long random run of a timed token game with the course semantics (immediate before timed, priorities, a countdown cancelled when its transition loses its tokens, one clock per waiting token) must keep the declared invariants (e.g. *line + in service = 1*), fire every transition, and keep queues bounded where the system is stable.
- **Marking at time t:** the drawn marking must equal the simulated one.
- **SIMLIB:** the model in each note is compiled with SIMLIB 3.10 and run; its results are compared with the theory where it is easy to compute.

## Building

All tools come from the Nix flake (`flake.nix`, pinned by `flake.lock`): Python, a slim TeX Live with TikZ, poppler, pandoc + xelatex with the DejaVu fonts, and SIMLIB 3.10 built from the official FIT source. Pinned versions keep the committed PDFs and SVGs byte-identical between builds.

```sh
nix develop          # or: direnv allow  (the .envrc loads the shell when you cd into the project)
```

```sh
make            # everything below except check
make nets       # check every net and render net.pdf + net.svg next to each net.py
make notes      # render every note to its PDF (A4; task on page 1, hint and net on later pages)
make simlib     # compile and run the SIMLIB model of every note
make index      # regenerate "exercises/Seznam úloh.md" from pn/catalog.py
make check      # checks only (nets + SIMLIB models)

python3 -m pn.build "exercises/09 - Obsluha zákazníků/10 - Kopírovací centrum"   # one net, or a whole category
python3 -m pn.notes "exercises/03 - Poruchy"                                      # the PDFs of one category
python3 -m pn.dd 3 lifo 1 5 10 10.5     # D/D/3 LIFO trace: events at t1=10, state at t2=10.5
python3 -m pn.dd log 2 fifo 1 4 6.5     # every event from 0 to 6.5
python3 -m pn.dd table 1 fifo 2 4 10    # state table after each event time (D/D/1 tasks)
```

To add an exercise, add it to [pn/catalog.py](pn/catalog.py) (the single list of categories, names and origins), create its folder with `net.py` and the note, and run `make`.

## Layout

```
pn/            Python library: catalogue (catalog.py), exercise list (index.py),
               net model (net.py), TikZ output (tikz.py), lint rules (lint.py),
               timed token-game simulator (sim.py), D/D/x trace (dd.py),
               build driver (build.py), note PDFs (notes.py), SIMLIB runner (simlib.py)
basics/        notation cheat sheet, how a net runs, pattern nets
notation/      rules for writing a note (Note.md) and laying out a diagram (Style.md)
exercises/     the exercises, one folder per category (see above)
source-survey/ the initial survey of the course material, by source file
build/         generated intermediates (git-ignored)
```

## Open work

- Rework the crowded diagrams in *Výroba a sklady* (Zahradník na FIT, Přečerpávací elektrárna, Dílna se třemi stroji) and fix the few labels that touch lines.
- A printable collection (`make book`): each task on its own page, the solution on the next.
- A final consistency pass over all notes.
- Optionally, transcripts of the 2023 demo-exercise videos to cross-check the midterm solutions against Hrubý's reasoning.
