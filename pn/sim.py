"""Timed token game used to check nets.

Semantics follow the IMS slides:
- immediate transitions always fire before timed ones; among immediate ones
  the highest priority wins, ties are broken by probability or uniformly;
- a timed transition starts counting when it becomes enabled and the tokens
  stay in its input places while it counts (slide 137), so another transition
  may take them away and the countdown is cancelled (slide 139);
- an ordinary timed transition does not limit how many tokens wait in it at
  once (slide 138): every enabling instance has its own clock. A `capacity`
  limits the number of clocks. When an instance is cancelled, the oldest one
  goes (the token taken first is the one that has waited longest).
"""

import math
import random
import re
from collections import Counter

UNITS = {"ms": 1 / 60000, "s": 1 / 60, "sec": 1 / 60, "min": 1, "m": 1, "h": 60, "hod": 60,
         "d": 1440, "den": 1440, "dní": 1440, "dny": 1440, "t": 10080, "týden": 10080}


class SimError(Exception):
    pass


def _num(token, net):
    """'3', '2,5', 'X', '3 min', 'X h' -> value in minutes (or in the net's unit)."""
    token = token.strip()
    m = re.fullmatch(r"([0-9]+(?:[.,][0-9]+)?|[A-Za-z_]\w*)\s*([A-Za-zíý]*)", token)
    if not m:
        raise SimError(f"cannot parse time value {token!r}")
    val, unit = m.groups()
    if re.fullmatch(r"[0-9]+(?:[.,][0-9]+)?", val):
        x = float(val.replace(",", "."))
    elif val in net.params:
        x = float(net.params[val])
    else:
        raise SimError(f"symbol {val!r} has no value in net.params")
    return x * UNITS[unit or net.unit] / UNITS[net.unit]


def sampler(spec, net):
    """Return a function rng -> duration (in the net's unit)."""
    s = spec.strip()
    m = re.fullmatch(r"(?:exp|Exp|exponential|Exponential)\((.+)\)\s*", s)
    if m:
        mean = _num(m.group(1), net)
        return lambda rng: rng.expovariate(1 / mean)
    m = re.fullmatch(r"(?:uniform|Uniform|Uni|U)\((.+),(.+)\)\s*", s)
    if m:
        a, b = _num(m.group(1), net), _num(m.group(2), net)
        return lambda rng: rng.uniform(a, b)
    m = re.fullmatch(r"(\S+)\s*[–-]\s*(\S+)\s*([A-Za-zíý]*)", s)
    if m and not s.startswith("-"):
        unit = m.group(3)
        a, b = _num(f"{m.group(1)} {unit}", net), _num(f"{m.group(2)} {unit}", net)
        return lambda rng: rng.uniform(a, b)
    c = _num(s, net)
    return lambda rng: c


def initial(net, start=None):
    if start is not None:
        m = {p: 0 for p in net.places}
        m.update(start)
        return m
    return {p.id: (p.tokens if isinstance(p.tokens, int) else int(net.params[p.tokens]))
            for p in net.places.values()}


def run(net, until=None, events=None, seed=1, start=None):
    """Simulate; returns a report dict. Raises SimError on a broken invariant."""
    rng = random.Random(seed)
    M = initial(net, start)
    imm = [t for t in net.transitions.values() if t.kind == "immediate"]
    tim = [t for t in net.transitions.values() if t.kind == "timed"]
    ins = {t: net.inputs(t) for t in net.transitions}
    inh = {t: net.inhibitors(t) for t in net.transitions}
    outs = {t: net.outputs(t) for t in net.transitions}
    samp = {t.id: sampler(t.sim or t.time, net) for t in tim}
    clocks = {t.id: [] for t in tim}          # list of (start, fire_at)
    fired = Counter()
    peak = dict(M)
    now = 0.0
    events = events if events is not None else net.sim_events

    def degree(t):
        if any(M[p] >= w for p, w in inh[t]):
            return 0
        if not ins[t]:
            return 1
        return min(M[p] // w for p, w in ins[t])

    def fire(t):
        for p, w in ins[t]:
            M[p] -= w
            assert M[p] >= 0
        for p, w in outs[t]:
            M[p] += w
            peak[p] = max(peak[p], M[p])
        fired[t] += 1

    def check():
        for name, coefs, value in net.invariants:
            got = sum(c * M[p] for p, c in coefs.items())
            if got != value:
                raise SimError(f"t={now:.3f}: invariant {name} broken (= {got}); marking {nonzero()}")
        for p, b in net.bounds.items():
            if M[p] > b:
                raise SimError(f"t={now:.3f}: place {p} has {M[p]} tokens, bound {b}")

    def nonzero():
        return {p: v for p, v in M.items() if v}

    n_events = 0
    deadlock = False
    while True:
        # immediate phase
        k = 0
        while True:
            cand = [t for t in imm if degree(t.id) > 0]
            if not cand:
                break
            top = max(t.p or 0 for t in cand)
            cand = [t for t in cand if (t.p or 0) == top]
            weights = [t.prob if t.prob is not None else 1 for t in cand]
            t = rng.choices(cand, weights)[0]
            fire(t.id)
            k += 1
            if k > 100000:
                raise SimError(f"t={now:.3f}: immediate transitions fire forever (livelock), last {t.id}")
        check()
        # keep one clock per enabling instance of every timed transition
        for t in tim:
            d = degree(t.id)
            if t.capacity:
                d = min(d, t.capacity)
            cl = clocks[t.id]
            cl.sort()
            while len(cl) > d:
                cl.pop(0)
            while len(cl) < d:
                cl.append((now, now + samp[t.id](rng)))
        pending = [(fire_at, start, tid) for tid, cl in clocks.items() for start, fire_at in cl]
        if not pending:
            deadlock = True
            break
        fire_at, start, tid = min(pending)
        if until is not None and fire_at > until:
            now = until
            break
        if until is None and n_events >= events:
            break
        now = fire_at
        clocks[tid].remove((start, fire_at))
        fire(tid)
        n_events += 1

    return {"time": now, "events": n_events, "marking": M, "fired": fired,
            "peak": peak, "deadlock": deadlock}


def check(net, seeds=(1, 2, 3)):
    """Run the standard checks; return a list of problems (empty = fine)."""
    problems = []
    if net.simulate:
        dead = set(net.transitions) - net.may_not_fire
        for seed in seeds:
            try:
                r = run(net, seed=seed)
            except SimError as e:
                problems.append(f"seed {seed}: {e}")
                continue
            dead -= {t for t, n in r["fired"].items() if n}
            if r["deadlock"] and not net.closed:
                problems.append(f"seed {seed}: deadlock at t={r['time']:.2f}, marking "
                                f"{ {p: v for p, v in r['marking'].items() if v} }")
            for p, v in r["peak"].items():
                if v > 500 and p not in net.unbounded_ok and p not in net.bounds:
                    problems.append(f"seed {seed}: place {p} grew to {v} tokens (unbounded?)")
        if dead:
            problems.append(f"transitions that never fired: {sorted(dead)}")
    if net.trace:
        r = run(net, until=net.trace["at"], start=net.trace["start"], seed=1)
        want = initial(net)
        if r["marking"] != want:
            diff = {p: (want[p], r["marking"][p]) for p in want if want[p] != r["marking"][p]}
            problems.append(f"trace: drawn marking differs from simulation at t={net.trace['at']}: "
                            f"(drawn, simulated) {diff}")
    return problems
