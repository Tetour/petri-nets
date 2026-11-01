# Petri nets for IMS

All 118 Petri net exercises from the IMS course materials (Modelování a simulace, FIT VUT), each solved in the course notation, checked by simulation and modelled in SIMLIB. Use it to prepare for the midterm (model a word problem as a Petri net) and for the Petri net questions of the final exam. The notes are in Czech.

## How to study

1. **Learn the notation.** [Notace a vzory](basics/Notace%20a%20vzory.md) shows the course notation and the standard patterns, each with exercises to practise it. [Jak síť funguje](<basics/Jak síť funguje.md>) explains how a net runs: timed transitions, several tokens, cancelled countdowns.
2. **Pick exercises** from [Seznam úloh](<exercises/Seznam úloh.md>). Start with *Začni tady*: 15 exercises that cover every pattern and the newest midterms.
3. **Solve, then check.** A note opens with only the task. Draw your net on paper, then open the hint, the net, the common mistakes, the SIMLIB model and the sources one at a time. Every note also has a PDF next to it.
4. **Repeat in Anki.** The 20 midterm word problems of 2021/22–2025/26 are flashcards in the deck *FIT::IMS* (tag `ims::petriho-site::pulsemestralka`).

Found a mistake? Fix it in the note, or ask for the fix.

## Keep in mind

- A task often has more than one correct net. The notes follow Hrubý's style and mention the real alternatives.
- ⚠️ marks a task known only from a student's recollection or a blurry photo, or reconstructed from Hrubý's solution (the 2025/26 midterms).
- The notation follows Hrubý's 2025 slides and his midterm solutions; the MSI notes use a different convention.

## Where the exercises come from

Final exams 2005–2026, midterms 2010–2026 (including the Z1–Z24 overview and Hrubý's own solutions for 2021/22–2025/26), student prep compilations and the lectures. Each note's last section, *Původ a zdroje*, names the files and pages and compares existing solutions. [source-survey/](source-survey/) records what every source file contains.

## Maintenance

All tools come from the Nix flake: `nix develop`, or `direnv allow` once.

```sh
make                                     # nets, note PDFs, SIMLIB models, exercise list
make check                               # notes, nets (lint + simulation) and SIMLIB models
python3 -m pn.notes "<exercise folder>"  # rebuild one note's PDF after editing it
python3 -m pn.dd 3 lifo 1 5 10 10.5      # D/D/x trace for the marking-at-time-t tasks
```

- How notes and diagrams are written: [Note.md](notation/Note.md) and [Style.md](notation/Style.md).
- A new exercise goes into [pn/catalog.py](pn/catalog.py); then create its folder with `net.py` and the note, and run `make`.
- The note PDFs are committed, so rebuild only those you changed.
