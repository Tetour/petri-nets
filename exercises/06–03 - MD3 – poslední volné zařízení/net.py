from pn import Net

net = Net("06–03", "M/D/3, kdo obsadí poslední volné zařízení, je obsluhován 5, jinak 3")
net.params = {"A": 2}

net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(A)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta", label_pos="above")
net.arc("prichod", "fronta")

net.place("zarizeni", (6, 0), tokens=3, label="Zařízení", label_pos="right")

# volná jsou aspoň 2 zařízení: vezme 2, jedno hned vrátí → obsluha 3
net.immediate("obsaz3", (4.5, 1.8), p=1, param_pos="above")
net.place("obsluha3", (6, 1.8))
net.timed("obsl3", (7.5, 1.8), "3", param_pos="above")
net.chain("fronta", "obsaz3", "obsluha3", "obsl3")
net.arc("zarizeni", "obsaz3", w=2, bend=18, w_pos="below left")
net.arc("obsaz3", "zarizeni", bend=18)
net.arc("obsl3", "zarizeni")

# volné je jen poslední zařízení (p=0) → obsluha 5
net.immediate("obsaz5", (4.5, -1.8), param_pos="below")
net.place("obsluha5", (6, -1.8))
net.timed("obsl5", (7.5, -1.8), "5")
net.chain("fronta", "obsaz5", "obsluha5", "obsl5")
net.arc("zarizeni", "obsaz5")
net.arc("obsl5", "zarizeni")

net.place("konec", (9, 0), label="konec", label_pos="above")
net.immediate("odchod", (10.5, 0), exit=True, label="odchod")
net.arc("obsl3", "konec")
net.arc("obsl5", "konec")
net.arc("konec", "odchod")

net.invariant({"zarizeni": 1, "obsluha3": 1, "obsluha5": 1}, 3)
