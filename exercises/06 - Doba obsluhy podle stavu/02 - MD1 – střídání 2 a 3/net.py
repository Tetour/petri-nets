from pn import Net

net = Net("M/D/1, doba obsluhy se střídá 2, 3, 2, 3, …")
net.params = {"A": 3}

net.place("gen", (0, 0), tokens=1, label="příchody transakcí", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(A)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="fronta", label_pos="above left")
net.arc("prichod", "fronta")

# linka má dva stavy volné linky: příští obsluha trvá 2 (nahoře), nebo 3 (mezi řadami)
net.place("linka2", (4.5, 3.4), tokens=1, label="Linka (2)", label_pos="left")
net.place("linka3", (4.5, 0), label="Linka (3)", label_pos="above")

# horní řada obsluha 2, dolní obsluha 3
for row, y, time in (("2", 1.7, "2"), ("3", -1.7, "3")):
    net.immediate(f"obsaz{row}", (4.5, y))
    net.arc("fronta", f"obsaz{row}", via=[(3, y)])
    net.place(f"obsluha{row}", (6, y))
    net.timed(f"obsl{row}", (7.5, y), time, param_pos="above")
    net.chain(f"obsaz{row}", f"obsluha{row}", f"obsl{row}")
    net.arc(f"linka{row}", f"obsaz{row}")

# obsluha 2 předá linku do stavu „3“: dolů ze spodní strany přechodu a doleva
net.arc("obsl2", "linka3", via=[(7.5, 0)])
# obsluha 3 předá linku do stavu „2“: objížďka kolem konce sítě
net.arc("obsl3", "linka2", via=[(7.5, -3.1), (12.5, -3.1), (12.5, 3.4)])

net.place("konec", (9.5, 0), label="obslouženo", label_pos="left")
net.immediate("odchod", (11, 0), exit=True, label="odchod")
net.arc("obsl2", "konec", via=[(9.5, 1.7)])
net.arc("obsl3", "konec", via=[(9.5, -1.7)])
net.arc("konec", "odchod")

net.invariant({"linka2": 1, "linka3": 1, "obsluha2": 1, "obsluha3": 1}, 1)
