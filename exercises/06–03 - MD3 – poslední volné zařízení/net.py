from pn import Net

net = Net("06–03", "M/D/3, kdo obsadí poslední volné zařízení, je obsluhován 5, jinak 3")
net.params = {"A": 2}

net.place("gen", (0, 0), tokens=1, label="příchody transakcí", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(A)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="fronta", label_pos="above left")
net.arc("prichod", "fronta")

# tři zařízení mezi řadami: nahoře obsazení p=1 (volná jsou aspoň 2), dole p=0 (poslední volné)
net.place("zarizeni", (5, 0), tokens=3, label="Zařízení", label_pos="below left")

for row, y, time in (("3", 2, "3"), ("5", -2, "5")):
    up = y > 0
    net.immediate(f"obsaz{row}", (5, y), p=1 if up else None, param_pos="above")
    net.arc("fronta", f"obsaz{row}", via=[(3, y)], corner=20)
    net.place(f"obsluha{row}", (6.7, y))
    net.timed(f"obsl{row}", (8.4, y), time, param_pos="above" if up else "below")
    net.chain(f"obsaz{row}", f"obsluha{row}", f"obsl{row}")
    # návrat zařízení: oblouk ze spodní (u dolní řady z horní) strany přechodu
    net.arc(f"obsl{row}", "zarizeni", out=270 if up else 90, into=20 if up else -20)

# p=1 vezme 2 zařízení a jedno hned vrátí (test „volná jsou aspoň 2“)
net.arc("zarizeni", "obsaz3", w=2, bend=25, w_pos="left")
net.arc("obsaz3", "zarizeni", bend=25)
net.arc("zarizeni", "obsaz5")

net.place("konec", (10, 0), label="obslouženo", label_pos="left")
net.immediate("odchod", (11.5, 0), exit=True, label="odchod")
net.arc("obsl3", "konec", via=[(10, 2)], corner=20)
net.arc("obsl5", "konec", via=[(10, -2)], corner=20)
net.arc("konec", "odchod")

net.invariant({"zarizeni": 1, "obsluha3": 1, "obsluha5": 1}, 3)
