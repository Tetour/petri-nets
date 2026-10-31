from pn import Net

net = Net("08–07", "D/D/3 se společnou FIFO frontou, značení v čase t = 9,5 s", unit="s")

net.place("gen", (0, 0), tokens=1, label="příchody požadavků", label_pos="above")
net.timed("prichod", (1.5, 0), "1 s")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), tokens=4, label="fronta", label_pos="above left")
net.arc("prichod", "fronta")

net.place("konec", (9, 0), label="hotovo", label_pos="below right")
net.immediate("odchod", (10.5, 0), exit=True, label="odchod")
net.arc("konec", "odchod")

# řady zařízení Z0 (nahoře, p=2), Z1 (uprostřed, p=1), Z2 (dole, implicitní p=0);
# Z0 a Z1 nad svou řadou, Z2 pod ní
for k, (y, p) in enumerate(((3.2, 2), (0, 1), (-3.2, None))):
    up = y >= 0
    net.immediate(f"obsaz{k}", (4.5, y), p=p, param_pos="below" if up else "above")
    net.place(f"Z{k}", (4.5, y + (1.6 if up else -1.6)), tokens=0, label=f"Z{k}",
              label_pos=("left" if y == 0 else "above") if up else "below")
    net.place(f"obsluha{k}", (6, y), tokens=1)
    net.timed(f"obsl{k}", (7.5, y), "5 s", param_pos="below" if up else "above")
    net.chain(f"obsaz{k}", f"obsluha{k}", f"obsl{k}")
    net.arc(f"Z{k}", f"obsaz{k}")
    # návrat zařízení: oblouk z horní (u dolní řady ze spodní) strany přechodu
    net.arc(f"obsl{k}", f"Z{k}", out=90 if up else 270, into=0)
    # rozvětvení z fronty a sloučení do místa hotovo
    if y == 0:
        net.arc("fronta", f"obsaz{k}")
        net.arc(f"obsl{k}", "konec")
    else:
        net.arc("fronta", f"obsaz{k}", via=[(3, y)], corner=20)
        net.arc(f"obsl{k}", "konec", via=[(9, y)], corner=20)
    net.invariant({f"Z{k}": 1, f"obsluha{k}": 1}, 1)

# zobrazené značení musí odpovídat simulaci od času 0 (P0 přichází v čase 0)
net.trace = {"start": {"gen": 1, "fronta": 1, "Z0": 1, "Z1": 1, "Z2": 1}, "at": 9.5}
net.unbounded_ok = {"fronta"}   # příchody 1/s, obsluha 3 za 5 s → systém není stabilní
net.sim_events = 3000
