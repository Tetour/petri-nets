from pn import Net

net = Net("08–06", "D/D/4 se společnou LIFO frontou, značení v čase t = 9,5 s", unit="s")

net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="below")
net.timed("prichod", (1.5, 0), "1 s")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), tokens=3, label="Fronta", label_pos="above left")
net.arc("prichod", "fronta")

net.place("konec", (9.7, 0))
net.immediate("odchod", (11.2, 0), exit=True, label="odchod")
net.arc("konec", "odchod")

# obsazení prioritně: Z0 (p=3) > Z1 (p=2) > Z2 (p=1) > Z3 (p=0); Z0, Z1 nad přechody, Z2, Z3 pod nimi
for k, (y, p, side) in enumerate(((5.2, 3, 1), (1.4, 2, 1), (-1.4, 1, -1), (-5.2, None, -1))):
    net.place(f"Z{k}", (4.5, y + side * 1.5), tokens=0, label=f"Z{k}",
              label_pos="above" if side > 0 else "below")
    net.immediate(f"obsaz{k}", (4.5, y), p=p, param_pos="below right" if side > 0 else "above right")
    net.place(f"obsluha{k}", (6.2, y), tokens=1)
    net.timed(f"obsl{k}", (7.7, y), "7 s", param_pos="above right" if side > 0 else "below right")
    net.chain("fronta", f"obsaz{k}", f"obsluha{k}", f"obsl{k}", "konec")
    net.arc(f"Z{k}", f"obsaz{k}")
    net.arc(f"obsl{k}", f"Z{k}", bend=-25 * side)
    net.invariant({f"Z{k}": 1, f"obsluha{k}": 1}, 1)

# zobrazené značení musí odpovídat simulaci od času 0 (P0 přichází v čase 0)
net.trace = {"start": {"gen": 1, "fronta": 1, "Z0": 1, "Z1": 1, "Z2": 1, "Z3": 1}, "at": 9.5}
net.unbounded_ok = {"fronta"}   # příchody 1/s, obsluha 4 za 7 s → systém není stabilní
net.sim_events = 3000
