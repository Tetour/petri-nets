from pn import Net

net = Net("M/D/1: do 10 od konce poslední obsluhy trvá obsluha 2, jinak 5")
net.params = {"A": 6}

net.place("gen", (0, 0), tokens=1, label="příchody transakcí", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(A)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="fronta", label_pos="above left")
net.arc("prichod", "fronta")

# volná linka ve dvou stavech mezi řadami: od konce obsluhy uplynulo < 10 (obsluha 2),
# nebo ≥ 10 (obsluha 5); časovaný přechod 10 mezi nimi přesouvá značku z Linky (2) do Linky (5)
net.place("linka2", (5.6, 1.2), label="Linka (2)", label_pos="above left")
net.place("linka5", (5.6, -1.2), tokens=1, label="Linka (5)", label_pos="right")
net.timed("vychladnuti", (5.6, 0), "10", horizontal=True, param_pos="left")
net.chain("linka2", "vychladnuti", "linka5")

# horní řada obsluha 2, dolní obsluha 5
for row, y, time in (("2", 2.8, "2"), ("5", -2.8, "5")):
    up = y > 0
    net.immediate(f"obsaz{row}", (5.6, y))
    net.arc("fronta", f"obsaz{row}", via=[(3, y)], corner=20)
    net.place(f"obsluha{row}", (7.3, y))
    net.timed(f"obsl{row}", (9, y), time, param_pos="above" if up else "below")
    net.chain(f"obsaz{row}", f"obsluha{row}", f"obsl{row}")
    net.arc(f"linka{row}", f"obsaz{row}")
    # obě obsluhy vracejí linku do stavu „2“: oblouk ze spodní (u dolní řady z horní) strany
    net.arc(f"obsl{row}", "linka2", out=270 if up else 90, into=20 if up else -20)

net.place("konec", (10.6, 0), label="obslouženo", label_pos="left")
net.immediate("odchod", (12.1, 0), exit=True, label="odchod")
net.arc("obsl2", "konec", via=[(10.6, 2.8)], corner=20)
net.arc("obsl5", "konec", via=[(10.6, -2.8)], corner=20)
net.arc("konec", "odchod")

net.invariant({"linka2": 1, "linka5": 1, "obsluha2": 1, "obsluha5": 1}, 1)
