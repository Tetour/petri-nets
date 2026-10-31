# Diagram style

How to lay out a net in `net.py`. These are preferences, not hard rules: when following one would make a diagram worse, break it. The course notation itself (what each element looks like and means) is in [Notace a vzory](Notace%20a%20vzory.md) and in [PLAN.md](../PLAN.md) §3; this file covers layout only.

## Flow

- Transactions flow **left to right**. Side processes (breakdowns, counters, signals) go in rows above or below the main flow.
- The **generator is on the left**: its place is the leftmost node of its row and the transactions it creates start from there. If something has to act on the generator's token (stopping arrivals, for example), put it below or above the generator, not to its left.
- Keep similar things aligned: one row per flow, one column per stage when rows run in parallel.
- **Split branches of the same kind symmetrically**: when a place branches into alternatives that are handled alike (e.g. 33 % / 67 % to two repairers), put one row above and one below the branching place, mirror-imaged, and merge them the same way. The symmetry shows that the branches are of a similar kind. See [01–01](../exercises/01–01%20-%20Opravářská%20dílna/net.py).

## Transitions

- Draw transitions as **vertical bars** (the default). Avoid `horizontal=True`: lay out the net so arcs come in from the left and leave to the right, and let a vertical flow enter the bar from the top or bottom.

## Arcs

- Route arcs **orthogonally**: horizontal and vertical segments with `via=[...]`. The `arc` style rounds the corners. Avoid diagonal lines and `bend=`.
- Where the main flow **splits into branches or merges back**, give the bend a larger radius: `corner=20` (20 pt instead of the default 5 pt). The arc keeps its up-then-right shape but reads as one smooth turn. Compared with curves (`out`/`into`), this was the preferred look; see [01–01](../exercises/01–01%20-%20Opravářská%20dílna/net.py).
- **Exception:** self-loops (a generator's `net.loop`, a test loop with weights) keep the usual curved lens.
- **Exception:** the return arc of a resource (a timed transition giving the token back to a facility or store above the seize transition) is a **curve**: it leaves the transition from the **top** and enters the resource place from the **side facing the transition**. Use `net.arc(t, resource, out=90, into=0)` when the resource is to the left of the transition (`into=180` when it is to the right; for a resource below the row, `out=270`). See [01–03](../exercises/01–03%20-%20Zdravotní%20ordinace/net.py).
- The final segment always aims at the centre of the target node, so a place has only **four orthogonal entry points** (top, bottom, left, right). Plan positions so that each arc gets its own side.
- **No two arcs share a segment**, and **lines don't cross**. If the only orthogonal route is a detour around a few nodes, a detour is fine (see the return arc in [03-sklad](patterns/03-sklad/net.py)).

## Labels, parameters, weights

- No text may touch a line or other text.
- Put a label on a side that no arc uses. If all four sides are taken, use a corner (`label_pos="below left"`).
- Move a parameter with `param_pos` when the default side has an arc (for example, a time above a bar whose output leaves downward).
- A weight sits at the middle of the arc's first segment. On a short arc it can touch the arrowhead: lengthen the arc or offset the weight (`w_pos="right=2pt"`).

## Checking

After `python3 -m pn.build <path>`, look at the render (`net.pdf`, or the PNG preview in `build/`) and check every label for contact with lines.
