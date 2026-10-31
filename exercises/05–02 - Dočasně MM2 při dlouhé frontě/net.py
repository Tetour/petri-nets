from pn import Net

net = Net("05–02", "M/M/1, při frontě delší než 5 dočasně M/M/2 na 15 č. j.")
net.params = {"A": 5, "B": 6}

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

# fronta přesáhne 5 (aspoň 6): druhá linka na 15 č. j.
net.place("mm1", (1.5, 3.4), tokens=1, label="M/M/1", label_pos="left")
net.immediate("pridej", (3, 3.4), label="přidej", label_pos="above")
net.arc("mm1", "pridej")
net.arc("fronta", "pridej", w=6, bend=-15, w_pos="right")
net.arc("pridej", "fronta", w=6, bend=-15, w_pos="left")
net.arc("pridej", "linka")
net.place("mm2", (4.5, 3.4), label="M/M/2", label_pos="above")
net.timed("doba", (6, 3.4), "15")
net.place("ubrat", (7.5, 3.4), label="ubrat", label_pos="above")
net.chain("pridej", "mm2", "doba", "ubrat")

# po 15 č. j. odebrat linku, jakmile je volná (p=1 předběhne obsazení)
net.immediate("odeber", (7.5, 1.7), p=1, horizontal=True, label="odeber",
              label_pos="below right", param_pos="above left")
net.arc("ubrat", "odeber")
net.arc("linka", "odeber")
net.arc("odeber", "mm1", via=[(9, 1.7), (9, 4.9), (1.5, 4.9)])

net.invariant({"linka": 1, "obsluha": 1, "mm1": 1}, 2)
net.invariant({"mm1": 1, "mm2": 1, "ubrat": 1}, 1)
