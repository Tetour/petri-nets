# Diagram style

How to lay out a net in `net.py`. These are preferences, not hard rules: when following one would make a diagram worse, break it. The course notation itself (what each element looks like and means) is in [Notace a vzory](../basics/Notace%20a%20vzory.md); this file covers layout only.

## Flow

- Transactions flow **left to right**. Side processes (breakdowns, counters, signals) go in rows above or below the main flow.
- The **generator is on the left**: its place is the leftmost node of its row and the transactions it creates start from there. If something has to act on the generator's token (stopping arrivals, for example), put it below or above the generator, not to its left.
- Keep similar things aligned: one row per flow, one column per stage when rows run in parallel.
- **Split branches of the same kind symmetrically**: when a place branches into alternatives that are handled alike (e.g. 33 % / 67 % to two repairers), put one row above and one below the branching place, mirror-imaged, and merge them the same way. The symmetry shows that the branches are of a similar kind. See [Opravářská dílna](../exercises/01%20-%20Základní%20modely/01%20-%20Opravářská%20dílna/net.py).

## Transitions

- Draw transitions as **vertical bars** (the default): lay out the net so arcs come in from the left and leave to the right.
- **Exception:** a transition whose arcs all attach to its **top or bottom** (a vertical flow, none from the left or right) may be a horizontal bar, `horizontal=True`. The bar then lies across the flow, as a vertical bar does in a left-to-right flow.

## Arcs

- Route arcs **orthogonally**: horizontal and vertical segments with `via=[...]`. The `arc` style rounds the corners. Avoid diagonal lines and `bend=`.
- Where the main flow **splits into branches or merges back**, give the bend a larger radius: `corner=20` (20 pt instead of the default 5 pt). The arc keeps its up-then-right shape but reads as one smooth turn. Compared with curves (`out`/`into`), this was the preferred look; see [Opravářská dílna](../exercises/01%20-%20Základní%20modely/01%20-%20Opravářská%20dílna/net.py).
- **Round all bends in a net the same way.** Once a net uses `corner=20`, give its other orthogonal arcs (returns, detours, state switches) `corner=20` too, and route them orthogonally rather than as free curves (`out`/`into`). Mixed radii and stray curves make the net look patched together. The exceptions below still apply. See [MD1 – střídání 2 a 3](../exercises/06%20-%20Doba%20obsluhy%20podle%20stavu/02%20-%20MD1%20–%20střídání%202%20a%203/net.py).
- **Exception:** self-loops (a generator's `net.loop`, a test loop with weights) keep the usual curved lens.
- **Exception:** the return arc of a resource (a timed transition giving the token back to a facility or store above the seize transition) is a **curve**: it leaves the transition from the **top** and enters the resource place from the **side facing the transition**. Use `net.arc(t, resource, out=90, into=0)` when the resource is to the left of the transition (`into=180` when it is to the right; for a resource below the row, `out=270`). See [Zdravotní ordinace](../exercises/01%20-%20Základní%20modely/03%20-%20Zdravotní%20ordinace/net.py).
  - When a **second arc also returns the token** to the resource (e.g. a breakdown cancelling the service), place the resource **directly above the timed transition** and draw the return as a **straight vertical arc**; the other return arc enters the resource from the side. See [Porucha zruší obsluhu](../exercises/03%20-%20Poruchy/01%20-%20Porucha%20zruší%20obsluhu/net.py).
- The final segment always aims at the centre of the target node, so a place has only **four orthogonal entry points** (top, bottom, left, right). Plan positions so that each arc gets its own side.
  - **Exception:** don't split a place in two (with an extra transition between them) just to give every arc its own side. Fewer elements win: the place keeps all its arcs, and the extra ones enter at the **corners as curves** (`out`/`into`, e.g. `out=90, into=315` for the lower right corner). See *letadlo čeká* in [Vyhlídkové lety](../exercises/11%20-%20Doprava%20a%20dávky/02%20-%20Vyhlídkové%20lety/net.py).
- **No two arcs share a segment**, and **lines don't cross**. If the only orthogonal route is a detour around a few nodes, a detour is fine (see the return arc in [03-sklad](../basics/patterns/03-sklad/net.py)).

## Labels, parameters, weights

- **Name places after the example**, not after the pattern: the generator's place is not „generátor“ but what arrives in the task, e.g. „příchody zákazníků“ (Opravářská dílna). The generic word says nothing the shape doesn't already show; the specific name ties the net to the task.
- No text may touch a line or other text.
- Put a label on a side that no arc uses. If all four sides are taken, use a corner (`label_pos="below left"`).
- Move a parameter with `param_pos` when the default side has an arc (for example, a time above a bar whose output leaves downward).
- A weight sits at the middle of the arc's first segment. On a short arc it can touch the arrowhead: lengthen the arc or offset the weight (`w_pos="right=2pt"`).

## Checking

After `python3 -m pn.build <path>`, look at the render (`net.pdf`, or the PNG preview in `build/`) and check every label for contact with lines.
