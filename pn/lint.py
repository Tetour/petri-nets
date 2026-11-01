"""Structural and notation rules (course notation, slides 128–139)."""

from collections import defaultdict


def lint(net):
    problems = []
    P, T = net.places, net.transitions
    for a in net.arcs:
        kinds = (a.src in P, a.dst in P, a.src in T, a.dst in T)
        if not ((kinds[0] and kinds[3]) or (kinds[2] and kinds[1])):
            problems.append(f"arc {a.src} -> {a.dst} must connect a place and a transition")
        if a.inhibitor and a.src not in P:
            problems.append(f"inhibitor arc {a.src} -> {a.dst} must start in a place")
        if isinstance(a.w, str):
            if a.w not in net.params:
                problems.append(f"arc {a.src} -> {a.dst}: weight symbol {a.w!r} has no value in net.params")
        elif a.w < 1:
            problems.append(f"arc {a.src} -> {a.dst} has weight {a.w}")
    used = {a.src for a in net.arcs} | {a.dst for a in net.arcs}
    for n in list(P) + list(T):
        if n not in used:
            problems.append(f"{n} is not connected to anything")

    for t in T.values():
        if t.kind == "timed" and (t.p is not None or t.prob is not None):
            problems.append(f"{t.id}: a timed transition has only a time (slide 139)")
        if t.kind == "immediate" and t.p is not None and t.prob is not None:
            problems.append(f"{t.id}: a transition has one parameter only (slide 135)")
        # an exit transition may only give back what it tests (a test loop, e.g. on a state place)
        if t.exit and any(o not in net.inputs(t.id) for o in net.outputs(t.id)):
            problems.append(f"{t.id}: an exit transition may only return tokens it tests")
        if not net.inputs(t.id) and t.kind == "immediate":
            problems.append(f"{t.id}: immediate transition without input fires forever")

    # probabilities of transitions sharing an input place must add up to 100 %
    groups = defaultdict(set)
    for t in T.values():
        if t.prob is not None:
            for p, _ in net.inputs(t.id):
                groups[p].add(t.id)
    # a place feeding only part of a branch (e.g. an extra resource taken by the 90 % branch)
    # is not the branching place: check only the maximal sets
    maximal = {p: ts for p, ts in groups.items() if not any(ts < other for other in groups.values())}
    for p, ts in maximal.items():
        total = sum(T[t].prob for t in ts)
        if abs(total - 100) > 0.5:
            problems.append(f"probabilities of {sorted(ts)} (from {p}) add up to {total:g} %, not 100 %")

    if not net.closed and not any(t.exit for t in T.values()):
        problems.append("no exit transition (mark the one where the transaction leaves with exit=True)")

    for name, coefs, _ in net.invariants:
        for p in coefs:
            if p not in P:
                problems.append(f"invariant {name}: unknown place {p}")
    return problems
