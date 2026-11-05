"""Petri net model: places, transitions, arcs, layout, and what to check.

A net is described in an exercise's `net.py`, which must define a module-level
variable `net`. Coordinates are in centimetres; y grows upwards.
"""

from dataclasses import dataclass, field


@dataclass
class Place:
    id: str
    at: tuple
    tokens: int | str = 0       # int, or a symbol such as "N" shown inside the place
    label: str | None = None    # name shown next to the place
    label_pos: str = "above"


@dataclass
class Transition:
    id: str
    at: tuple
    kind: str                   # "timed" | "immediate"
    time: str | None = None     # timed: displayed and simulated time, e.g. "exp(3 min)"
    p: int | None = None        # immediate: priority
    prob: float | None = None   # immediate: probability in percent
    label: str | None = None    # optional name, e.g. "Seize"
    label_pos: str = "above"
    param_pos: str | None = None
    horizontal: bool = False
    exit: bool = False          # the transaction leaves the system here
    capacity: int | None = None # timed: server capacity (None = unlimited, slide 138)
    sim: str | None = None      # override of `time` for the simulator

    @property
    def param(self):
        if self.kind == "timed":
            return self.time
        if self.p is not None:
            return f"p={self.p}"
        if self.prob is not None:
            return f"{self.prob:g} %".replace(".", ",")
        return None


@dataclass
class Arc:
    src: str
    dst: str
    w: int | str = 1            # a symbol (e.g. "C") needs a value in net.params
    inhibitor: bool = False
    bend: float = 0             # degrees; positive bends left
    via: list = field(default_factory=list)
    w_pos: str = "auto"         # TikZ placement of the weight label
    out: float | None = None    # curved arc: direction it leaves the source (degrees, 90 = up)
    into: float | None = None   # ... and direction from which it enters the target (0 = from the right)
    looseness: float | None = None  # curved arc: how far the curve swings out (TikZ default 1)
    corner: float | None = None # orthogonal arc (via): corner radius in pt (default 20, less where a segment is short)


class Net:
    def __init__(self, title, unit="min"):
        self.title = title
        self.unit = unit                # default unit for times without one
        self.places = {}
        self.transitions = {}
        self.arcs = []
        self.params = {}                # values for symbols in times, e.g. {"X": 50}
        self.invariants = []            # (name, {place: coef}, value)
        self.bounds = {}                # place -> max tokens expected
        self.unbounded_ok = set()       # places allowed to grow (unstable queues)
        self.may_not_fire = set()       # transitions allowed to stay dead in a run
        self.closed = False             # no exit transition expected
        self.deadlock_ok = False        # the simulation may stop (finite task, e.g. one working day)
        self.simulate = True
        self.sim_events = 20000
        self.trace = None               # {"start": {...}, "at": t}: displayed marking must equal sim at t
        self.notes = []                 # free-form text boxes: (at, text)

    # --- nodes -----------------------------------------------------------
    def place(self, id, at, tokens=0, label=None, label_pos="above"):
        assert id not in self.places and id not in self.transitions, id
        self.places[id] = Place(id, at, tokens, label, label_pos)
        return id

    def timed(self, id, at, time, **kw):
        assert id not in self.places and id not in self.transitions, id
        self.transitions[id] = Transition(id, at, "timed", time=time, **kw)
        return id

    def immediate(self, id, at, p=None, prob=None, **kw):
        assert id not in self.places and id not in self.transitions, id
        assert p is None or prob is None, f"{id}: a transition has one parameter only (slide 135)"
        self.transitions[id] = Transition(id, at, "immediate", p=p, prob=prob, **kw)
        return id

    # --- arcs ------------------------------------------------------------
    def arc(self, src, dst, w=1, **kw):
        self.arcs.append(Arc(src, dst, w, **kw))

    def inhibitor(self, place, trans, w=1, **kw):
        self.arcs.append(Arc(place, trans, w, inhibitor=True, **kw))

    def chain(self, *nodes, **kw):
        """Arcs a -> b -> c -> ... with default styling."""
        for a, b in zip(nodes, nodes[1:]):
            self.arc(a, b, **kw)

    def loop(self, place, trans, bend=30, w=1):
        """Place <-> transition self-loop (generator, test arc)."""
        self.arc(place, trans, w=w, bend=bend)
        self.arc(trans, place, w=w, bend=bend)

    # --- checks ----------------------------------------------------------
    def invariant(self, coefs, value, name=None):
        name = name or " + ".join(coefs) + f" = {value}"
        self.invariants.append((name, dict(coefs), value))

    def bound(self, place, max_tokens):
        self.bounds[place] = max_tokens

    # --- helpers ---------------------------------------------------------
    def inputs(self, t):
        return [(a.src, a.w) for a in self.arcs if a.dst == t and not a.inhibitor]

    def inhibitors(self, t):
        return [(a.src, a.w) for a in self.arcs if a.dst == t and a.inhibitor]

    def outputs(self, t):
        return [(a.dst, a.w) for a in self.arcs if a.src == t]

    def marking(self):
        return {p.id: p.tokens if isinstance(p.tokens, int) else 0 for p in self.places.values()}
