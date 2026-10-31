from pn import Net

net = Net("06–02", "M/D/1, doba obsluhy se střídá 2, 3, 2, 3, …")
net.params = {"A": 3}

net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(A)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta", label_pos="above")
net.arc("prichod", "fronta")

# linka má dva stavy volné linky: příští obsluha trvá 2, nebo 3
net.place("linka2", (5.25, 0), tokens=1, label="Linka (2)", label_pos="left")
net.place("linka3", (6.75, 0), tokens=0, label="Linka (3)", label_pos="below right")

net.immediate("obsaz2", (4.5, 1.5))
net.place("obsluha2", (6, 1.5))
net.timed("obsl2", (7.5, 1.5), "2")
net.chain("fronta", "obsaz2", "obsluha2", "obsl2")
net.arc("linka2", "obsaz2")
net.arc("obsl2", "linka3")

net.immediate("obsaz3", (4.5, -1.5))
net.place("obsluha3", (6, -1.5))
net.timed("obsl3", (7.5, -1.5), "3")
net.chain("fronta", "obsaz3", "obsluha3", "obsl3")
net.arc("linka3", "obsaz3")
net.arc("obsl3", "linka2")

net.place("konec", (9.5, 0), label="konec", label_pos="above")
net.immediate("odchod", (11, 0), exit=True, label="odchod")
net.arc("obsl2", "konec")
net.arc("obsl3", "konec")
net.arc("konec", "odchod")

net.invariant({"linka2": 1, "linka3": 1, "obsluha2": 1, "obsluha3": 1}, 1)
