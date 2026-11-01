from pn import Net

net = Net("D/D/2 se společnou LIFO frontou, značení v čase t2 = 13,5 s", unit="s")

net.place("gen", (0, 0), tokens=1, label="příchody požadavků", label_pos="above")
net.timed("prichod", (1.5, 0), "1 s")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), tokens=8, label="fronta", label_pos="right")
net.arc("prichod", "fronta")

# horní řada zařízení Z0 (Z0 nad ní, přednost p=1), dolní řada Z1 (Z1 pod ní, implicitní p=0)
for k, (y, p) in enumerate(((1.7, 1), (-1.7, None))):
    up = y > 0
    net.immediate(f"obsaz{k}", (4.5, y), p=p, param_pos="below" if up else "above")
    net.arc("fronta", f"obsaz{k}", via=[(3, y)], corner=20)
    net.place(f"Z{k}", (4.5, y + (1.6 if up else -1.6)), tokens=0, label=f"Z{k}",
              label_pos="above" if up else "below")
    net.place(f"obsluha{k}", (6, y), tokens=1)
    net.timed(f"obsl{k}", (7.5, y), "6 s", param_pos="below" if up else "above")
    net.chain(f"obsaz{k}", f"obsluha{k}", f"obsl{k}")
    net.arc(f"Z{k}", f"obsaz{k}")
    # návrat zařízení: oblouk z horní (u dolní řady ze spodní) strany přechodu
    net.arc(f"obsl{k}", f"Z{k}", out=90 if up else 270, into=0)
    net.invariant({f"Z{k}": 1, f"obsluha{k}": 1}, 1)

net.place("konec", (9, 0), label="hotovo", label_pos="left")
net.immediate("odchod", (10.5, 0), exit=True, label="odchod")
net.arc("obsl0", "konec", via=[(9, 1.7)], corner=20)
net.arc("obsl1", "konec", via=[(9, -1.7)], corner=20)
net.arc("konec", "odchod")

# zobrazené značení musí odpovídat simulaci od času 0 (P0 přichází v čase 0)
net.trace = {"start": {"gen": 1, "fronta": 1, "Z0": 1, "Z1": 1}, "at": 13.5}
net.unbounded_ok = {"fronta"}   # příchody 1/s, obsluha 2 za 6 s → systém není stabilní
net.sim_events = 3000
