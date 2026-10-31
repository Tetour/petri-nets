# Petri nets for IMS

Petri net diagrams for the Petri net exercises of the IMS course (Modelování a simulace, FIT VUT), drawn in the course notation and checked by simulation. The notes are in Czech; the scaffolding is in English. The full plan and the catalogue of all 118 exercises are in [PLAN.md](PLAN.md); the raw source inventory is in [inventory/](inventory/).

Start with the notation cheat sheet: [Notace a vzory](notation/Notace%20a%20vzory.md).

## Exercises

Status: `drafted` = built and passing `make check`, waiting for review; `reviewed` = accepted.

| Id | Note | Type | Status |
|---|---|---|---|
| M41 | [Kopírovací centrum](exercises/midterm/M41/M41%20-%20Kopírovací%20centrum.md) | midterm 2022/23 A | drafted |
| M53 | [Psí salon](exercises/midterm/M53/M53%20-%20Psí%20salon.md) | midterm 2025/26 A (reconstructed task) | drafted |
| L01 | [Opravářská dílna](exercises/lecture/L01/L01%20-%20Opravářská%20dílna.md) | lecture example | drafted |
| E06 | [Porucha vrací transakci do fronty](exercises/exam/E06/E06%20-%20Porucha%20vrací%20transakci%20do%20fronty.md) | exam 2019/20 | drafted |
| T02 | [D/D/3 LIFO, značení v čase 10,5](exercises/trace/T02/T02%20-%20DD3%20LIFO,%20značení%20v%20čase%2010,5.md) | exam 2015/16 (marking at time t) | drafted |

## Layout

```
pn/            Python library: net model (net.py), TikZ output (tikz.py),
               lint rules (lint.py), timed token-game simulator (sim.py),
               D/D/x next-event trace (dd.py), build driver (build.py)
notation/      cheat sheet + small pattern nets
exercises/     one folder per exercise: <Id> - <název>.md, net.py, net.svg, net.pdf
inventory/     where every exercise comes from (file, page, verbatim text)
build/         generated intermediates (git-ignored)
```

## Building

Requires Python 3.11+, pdflatex with TikZ, and poppler (`pdftocairo`, `pdftoppm`).

```sh
make            # check every net and render net.pdf + net.svg next to each net.py
make check      # checks only
python3 -m pn.build exercises/midterm/M41      # one net
python3 -m pn.dd 3 lifo 1 5 10 10.5            # D/D/3 LIFO trace: events at t1=10, state at t2=10.5
```

What `make check` verifies for each net:

- **Lint:** arcs connect a place and a transition; one parameter per transition; probabilities add up to 100 %; an exit transition exists.
- **Simulation:** a long random run (immediate before timed, priorities, cancelled countdowns, one clock per waiting token) must keep the declared invariants (e.g. *line + in service = 1*), fire every transition, and keep queues bounded where the system is stable.
- **Marking-at-time-t tasks:** the drawn marking must equal the simulated marking at that time.
