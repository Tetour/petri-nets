"""Next-event simulation of D/D/c with a common FIFO or LIFO queue.

Used for the "marking at time t" exam tasks. Conventions from the exam
assignments: arrivals start at time 0 with a constant interval, requests are
numbered P0, P1, ... in order of arrival, devices Z0, Z1, ... are taken
lowest number first, all events have the same priority, so events planned for
the same time run in the order they were planned (calendar is FIFO for ties).

    python3 -m pn.dd C {fifo|lifo} INTERVAL SERVICE T1 T2
"""

import heapq
import itertools
import sys


def fmt(x):
    return f"{x:g}".replace(".", ",")


class DD:
    def __init__(self, c, discipline, interval, service):
        self.c, self.lifo = c, discipline.lower() == "lifo"
        self.interval, self.service = interval, service

    def run(self, until):
        cal, seq = [], itertools.count()
        dev = [None] * self.c                    # request in service per device
        queue = []
        log = []                                 # (time, [lines])
        gantt = []                               # (device, request, start, end)
        snapshots = []                           # (time, calendar, queue, dev) after each event

        def plan(t, kind, data, lines):
            heapq.heappush(cal, (t, next(seq), kind, data))
            what = f"příchod P{data}" if kind == "arr" else f"konec obsluhy P{data[0]} na Z{data[1]}"
            lines.append(f"  plánuje: {what} v čase {fmt(t)}")

        def seize(t, p, k, lines):
            dev[k] = p
            lines.append(f"P{p} obsazuje Z{k}")
            gantt.append((k, p, t, t + self.service))
            plan(t + self.service, "end", (p, k), lines)

        heapq.heappush(cal, (0, next(seq), "arr", 0))
        while cal and cal[0][0] <= until:
            t, _, kind, data = heapq.heappop(cal)
            lines = []
            if kind == "arr":
                p = data
                lines.append(f"příchod P{p}")
                plan(t + self.interval, "arr", p + 1, lines)
                free = [k for k in range(self.c) if dev[k] is None]
                if free:
                    seize(t, p, free[0], lines)
                else:
                    queue.append(p)
                    lines.append(f"P{p} jde do fronty")
            else:
                p, k = data
                dev[k] = None
                lines.append(f"P{p} uvolňuje Z{k} a odchází")
                if queue:
                    q = queue.pop() if self.lifo else queue.pop(0)
                    lines.append(f"P{q} vystupuje z fronty ({'LIFO – poslední' if self.lifo else 'FIFO – první'})")
                    seize(t, q, k, lines)
            log.append((t, lines))
            snapshots.append((t, sorted(cal), list(queue), list(dev)))
        return log, gantt, snapshots

    def state_at(self, t):
        _, _, snaps = self.run(t)
        return snaps[-1]


def describe_calendar(cal):
    rows = []
    for t, s, kind, data in cal:
        what = f"příchod P{data}" if kind == "arr" else f"konec obsluhy P{data[0]} na Z{data[1]}"
        rows.append(f"| {fmt(t)} | {what} |")
    return "\n".join(["| čas | událost |", "|---|---|"] + rows)


def main(argv):
    c, disc, interval, service, t1, t2 = argv
    m = DD(int(c), disc, float(interval), float(service))
    log, gantt, _ = m.run(float(t2) + float(service))
    print(f"# D/D/{c} {disc.upper()}, příchody á {interval}, obsluha {service}\n")
    print("## Časový diagram (obsazení zařízení)\n")
    for k in range(int(c)):
        cells = [f"P{p} {fmt(a)}–{fmt(b)}" for kk, p, a, b in gantt if kk == k and a <= float(t2)]
        print(f"- Z{k}: " + ", ".join(cells))
    print(f"\n## Události provedené v čase t1 = {t1}\n")
    for t, lines in log:
        if t == float(t1):
            print("\n".join(lines))
    tt, cal, queue, dev = m.state_at(float(t2))
    print(f"\n## Stav v čase t2 = {t2}\n")
    print(describe_calendar(cal))
    print(f"\nfronta (od začátku): {', '.join(f'P{p}' for p in queue) or 'prázdná'}")
    print("zařízení: " + ", ".join(f"Z{k}: {'P' + str(p) if p is not None else 'volné'}" for k, p in enumerate(dev)))


if __name__ == "__main__":
    main(sys.argv[1:])
