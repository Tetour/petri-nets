# Note structure

How an exercise note looks. The diagram itself is covered by [STYLE.md](STYLE.md); the course notation by [Notace a vzory](Notace%20a%20vzory.md). The reference note is [Opravářská dílna](../exercises/01%20-%20Základní%20modely/01%20-%20Opravářská%20dílna/01%20-%20Opravářská%20dílna.md): when in doubt, copy it.

## File and language

- Folder and note: `exercises/<NN> - <kategorie>/<NN> - <název>/<NN> - <název>.md`, e.g. `exercises/01 - Základní modely/01 - Opravářská dílna/01 - Opravářská dílna.md`. Categories, names and their order come from [pn/catalog.py](../pn/catalog.py); the numbers are positions there. Exercise names are unique, so a note refers to another exercise by its **name**, never by its number.
- The note is in **Czech** (natural wording, diacritics, „uvozovky“, decimal comma, `33,3 %`).
- Next to it: `net.py` (the net), and the generated `net.svg`, `net.pdf` and the note's PDF (`make`).

## Skeleton

Only the heading and **Zadání** are visible when the note is opened; every other section sits behind its own toggle, so the reader can try the exercise first. After each `<summary>` comes `<br>`, which leaves an empty line between the toggle and its content in the Markdown preview (the PDF converter drops it).

````markdown
# Opravářská dílna

## Zadání

> task text …

Podobné úlohy: [Netrpělivé požadavky](<../../02 - Netrpělivost a omezená fronta/01 - Netrpělivé požadavky/01 - Netrpělivé požadavky.md>), …

## Interpretace

<details>
<summary>Zobrazit interpretaci (nápověda)</summary>
<br>

- …

</details>

## Petriho síť

<details>
<summary>Zobrazit Petriho síť</summary>
<br>

![Petriho síť – opravářská dílna](net.svg)

</details>

## Časté chyby

<details>
<summary>Zobrazit časté chyby</summary>
<br>

- …

</details>

## SIMLIB

<details>
<summary>Zobrazit SIMLIB kód</summary>
<br>

…

</details>

## Původ a zdroje

<details>
<summary>Zobrazit původ a zdroje</summary>
<br>

**Původ:** …

**Původní znění:**

> …

**Zdroje:**

- …

**Existující řešení:**

- …

</details>
````

## Sections

### Zadání

- The task text as a quote. Its **times are rewritten into one form** (plain text, no bold): the distribution as a Czech adverb before the value, units as whole words, no brackets.

  | distribution | in the text | in the diagram |
  |---|---|---|
  | exponential | exponenciálně se středem 20 minut | `exp(20 min)` |
  | uniform | rovnoměrně 10–15 minut | `10–15 min` |
  | constant | přesně 5 minut | `5 min` |
  | symbol | exponenciálně se středem X časových jednotek | `exp(X)` |

  A time **without a distribution** („v průměru 6 minut“) stays as written: choosing the distribution is part of the exercise, and the hints state the choice.

  A **speed** („rychlostí 15 kubíků za hodinu“) stays as written: converting it to a time per unit (`4 min`) is part of the exercise, and the hints state the conversion.

  The rest of the text stays as in the source. Diverging from the original is accepted (at the exam one can ask); the original is kept as **Původní znění** in Původ a zdroje.
- Zadání describes the system only. Lines that just say what to produce („Zadaný systém modelujte formou Petriho sítě s vyznačením všech potřebných parametrů.“, „V modelu jednoznačně ukažte (přechodem) moment, kdy transakce opouští systém.“, „+ SIMLIB“, „Napište program v SIMLIBu …“) are left out; they stay in Původní znění. Every net has an exit transition and every note a SIMLIB section anyway. An instruction that carries task data stays („se značením odpovídajícím času t2 = 10,5“).
- If the source is only a student's recollection or a reconstruction, a ⚠️ line before the quote says so.
- `Podobné úlohy:` links to related exercises (optional). Generate each link with `python3 -c "from pn.catalog import link; print(link('Netrpělivé požadavky'))"`. In running text, refer to an exercise the same way, with „úloha“ in the right case where the grammar needs it („jako v úloze [Výletní loď](…)“); in code comments, by its name in quotes.

### Interpretace → Nápověda

- Bullet points: how each requirement of the task becomes part of the net (arrivals, branching, resources, merged release, leaving …), in the order of the flow; and every ambiguity with the reading chosen (e.g. „přesáhne 5“ = more than 5, so the test arc has weight 6).
- The section is called **Interpretace** („Zobrazit interpretaci (nápověda)“) while it is an unconfirmed reading. Once the user reviews the note and confirms it, it is renamed to **Nápověda** („Zobrazit nápovědu“); the exercise index ([exercises/Readme.md](../exercises/Readme.md)) reads the status `reviewed` from that name.
- A hint states the modelling, not who said what: no mentions of the lecturer or transcripts here (those belong to Původ a zdroje).

### Petriho síť

- **Only the diagram**: `![Petriho síť – <název malými písmeny>](net.svg)`. No requirement table (that belongs to the hints) and no simulation notes (those belong to SIMLIB).

### Časté chyby

- Bullet points: the mistakes typical for this task and its pattern, each with why it is wrong.

### SIMLIB

- One sentence that the model is isomorphic to the net, then one `cpp` code block: complete, compilable SIMLIB/C++ with Czech comments linking each line to the net.
- A table **Petriho síť | SIMLIB** mapping places, transitions and tokens to the code.
- **Kontrola simulací.** What `make check` verified on the net (invariants, all transitions fire, bounded queues) and what one SIMLIB run gave, compared with the theory where it is easy to compute.
- `make simlib` compiles and runs the code block; it must pass.

### Původ a zdroje

- **Původ:** the exam or midterm, year, term, group, question, points — or the lecture/notes.
- **Původní znění:** the original task text, if Zadání was rewritten.
- **Zdroje:** the files with pages, as paths relative to the course study folder `IMS - Modelování a simulace/` (no remark about that in the note).
- **Existující řešení:** Hrubý's, the session's or students' solutions, how they differ from the net, and their errors.
