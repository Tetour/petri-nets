from pn import Net

net = Net("06–04", "M/D/1: do 10 od konce poslední obsluhy trvá obsluha 2, jinak 5")
net.params = {"A": 6}

net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(A)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta", label_pos="above")
net.arc("prichod", "fronta")

# volná linka ve dvou stavech: od konce obsluhy uplynulo < 10 (obsluha 2), nebo ≥ 10 (obsluha 5)
net.place("linka2", (6.75, 0), tokens=0, label="Linka (2)", label_pos="right")
net.timed("vychladnuti", (5.6, 0), "10", param_pos="below")
net.place("linka5", (4.5, 0), tokens=1, label="Linka (5)", label_pos="above")
net.chain("linka2", "vychladnuti", "linka5")

net.immediate("obsaz2", (4.5, 2))
net.place("obsluha2", (6, 2))
net.timed("obsl2", (7.5, 2), "2", param_pos="above")
net.chain("fronta", "obsaz2", "obsluha2", "obsl2")
net.arc("linka2", "obsaz2")
net.arc("obsl2", "linka2")

net.immediate("obsaz5", (4.5, -2))
net.place("obsluha5", (6, -2))
net.timed("obsl5", (7.5, -2), "5")
net.chain("fronta", "obsaz5", "obsluha5", "obsl5")
net.arc("linka5", "obsaz5")
net.arc("obsl5", "linka2")

net.place("konec", (9.6, 0), label="konec", label_pos="above")
net.immediate("odchod", (11.1, 0), exit=True, label="odchod")
net.arc("obsl2", "konec")
net.arc("obsl5", "konec")
net.arc("konec", "odchod")

net.invariant({"linka2": 1, "linka5": 1, "obsluha2": 1, "obsluha5": 1}, 1)
