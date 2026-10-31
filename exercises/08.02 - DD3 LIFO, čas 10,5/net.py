from pn import Net

net = Net("08.02", "D/D/3 se společnou LIFO frontou, značení v čase t2 = 10,5 s", unit="s")

net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="below")
net.timed("prichod", (1.5, 0), "1 s")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), tokens=4, label="Fronta", label_pos="above left")
net.arc("prichod", "fronta")

net.place("konec", (9.3, 0))
net.immediate("odchod", (10.8, 0), exit=True, label="odchod")
net.arc("konec", "odchod")

for k, (y, p) in enumerate(((3.2, 2), (0, 1), (-3.2, None))):
    net.place(f"Z{k}", (4.5, y + 1.5), tokens=0, label=f"Z{k}", label_pos="above")
    net.immediate(f"obsaz{k}", (4.5, y), p=p, param_pos="below right")
    net.place(f"obsluha{k}", (6.2, y), tokens=1)
    net.timed(f"obsl{k}", (7.7, y), "5 s", param_pos="below" if y == 0 else "right")
    net.chain("fronta", f"obsaz{k}", f"obsluha{k}", f"obsl{k}", "konec")
    net.arc(f"Z{k}", f"obsaz{k}")
    net.arc(f"obsl{k}", f"Z{k}", bend=-25)
    net.invariant({f"Z{k}": 1, f"obsluha{k}": 1}, 1)

# zobrazené značení musí odpovídat simulaci od času 0 (P0 přichází v čase 0)
net.trace = {"start": {"gen": 1, "fronta": 1, "Z0": 1, "Z1": 1, "Z2": 1}, "at": 10.5}
net.unbounded_ok = {"fronta"}   # příchody 1/s, obsluha 3 za 5 s → systém není stabilní
net.sim_events = 3000
