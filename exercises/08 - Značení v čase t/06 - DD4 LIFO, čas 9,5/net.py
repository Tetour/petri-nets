from pn import Net

net = Net("D/D/4 se společnou LIFO frontou, značení v čase t = 9,5 s", unit="s")

net.place("gen", (0, 0), tokens=1, label="příchody požadavků", label_pos="above")
net.timed("prichod", (1.5, 0), "1 s")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), tokens=3, label="fronta", label_pos="above left")
net.arc("prichod", "fronta")

net.place("konec", (9, 0), label="hotovo", label_pos="above right")
net.immediate("odchod", (10.5, 0), exit=True, label="odchod", label_pos="below")
net.arc("konec", "odchod")

# obsazení prioritně: Z0 (p=3) > Z1 (p=2) > Z2 (p=1) > Z3 (implicitní p=0);
# řady Z0, Z1 nahoře (zařízení nad řadou), Z2, Z3 dole (zařízení pod řadou)
for k, (y, p) in enumerate(((5.4, 3), (1.8, 2), (-1.8, 1), (-5.4, None))):
    up = y > 0
    outer = abs(y) > 3
    net.immediate(f"obsaz{k}", (4.5, y), p=p, param_pos="below" if up else "above")
    net.place(f"Z{k}", (4.5, y + (1.6 if up else -1.6)), tokens=0, label=f"Z{k}",
              label_pos=("above" if up else "below") if outer else "left")
    net.place(f"obsluha{k}", (6, y), tokens=1)
    net.timed(f"obsl{k}", (7.5, y), "7 s", param_pos="below" if up else "above")
    net.chain(f"obsaz{k}", f"obsluha{k}", f"obsl{k}")
    net.arc(f"Z{k}", f"obsaz{k}")
    # návrat zařízení: oblouk z horní (u dolních řad ze spodní) strany přechodu
    net.arc(f"obsl{k}", f"Z{k}", out=90 if up else 270, into=0)
    # rozvětvení z fronty a sloučení do místa hotovo: krajní řady pravoúhle,
    # vnitřní obloukem šikmo (místo má jen čtyři strany)
    if outer:
        net.arc("fronta", f"obsaz{k}", via=[(3, y)])
        net.arc(f"obsl{k}", "konec", via=[(9, y)])
    else:
        net.arc("fronta", f"obsaz{k}", out=45 if up else -45, into=180)
        net.arc(f"obsl{k}", "konec", out=0, into=135 if up else 225)
    net.invariant({f"Z{k}": 1, f"obsluha{k}": 1}, 1)

# zobrazené značení musí odpovídat simulaci od času 0 (P0 přichází v čase 0)
net.trace = {"start": {"gen": 1, "fronta": 1, "Z0": 1, "Z1": 1, "Z2": 1, "Z3": 1}, "at": 9.5}
net.unbounded_ok = {"fronta"}   # příchody 1/s, obsluha 4 za 7 s → systém není stabilní
net.sim_events = 3000
