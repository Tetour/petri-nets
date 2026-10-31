from pn import Net

net = Net("05–03", "M/M/1, při 5 transakcích ve frontě natrvalo M/M/3")
net.params = {"A": 4, "B": 6}

# M/M/1
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="below")
net.timed("prichod", (1.5, 0), "exp(A)", param_pos="below")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta", label_pos="below")
net.place("linka", (4.5, 1.7), tokens=1, label="Linka", label_pos="above right")
net.immediate("obsaz", (4.5, 0))
net.place("obsluha", (6, 0))
net.timed("obsl", (7.5, 0), "exp(B)")
net.chain("prichod", "fronta", "obsaz", "obsluha", "obsl")
net.arc("linka", "obsaz")
net.arc("obsl", "linka", bend=-15)
net.place("konec", (9, 0))
net.immediate("odchod", (10.5, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# fronta dosáhne 5: jednou provždy +2 linky
net.place("mm1", (1.5, 3.4), tokens=1, label="M/M/1", label_pos="left")
net.immediate("zmena", (3, 3.4), label="změna", label_pos="above")
net.arc("mm1", "zmena")
net.arc("fronta", "zmena", w=5, bend=-15, w_pos="right")
net.arc("zmena", "fronta", w=5, bend=-15, w_pos="left")
net.arc("zmena", "linka", w=2, w_pos="above right")
net.place("mm3", (4.5, 3.4), label="M/M/3", label_pos="right")
net.arc("zmena", "mm3")

net.invariant({"linka": 1, "obsluha": 1, "mm1": 2}, 3)
net.invariant({"mm1": 1, "mm3": 1}, 1)
