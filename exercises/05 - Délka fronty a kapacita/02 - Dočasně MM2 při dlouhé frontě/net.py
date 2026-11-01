from pn import Net

net = Net("M/M/1, při frontě delší než 5 dočasně M/M/2 na 15 č. j.")
net.params = {"A": 5, "B": 6}

# M/M/1
net.place("gen", (0, 0), tokens=1, label="příchody transakcí", label_pos="left")
net.timed("prichod", (1.5, 0), "exp(A)", param_pos="below")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta", label_pos="below")
net.place("linka", (4.5, 1.9), tokens=1, label="Linka", label_pos="above left")
net.immediate("obsaz", (4.5, 0))
net.place("obsluha", (6, 0))
net.timed("obsl", (7.5, 0), "exp(B)")
net.chain("prichod", "fronta", "obsaz", "obsluha", "obsl")
net.arc("linka", "obsaz")
net.arc("obsl", "linka", out=90, into=0)
net.place("konec", (9, 0))
net.immediate("odchod", (10.5, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# fronta přesáhne 5 (aspoň 6): přidej druhou jednotku Linky; test přímo nad Frontou
net.place("mm1", (1.5, 1.9), tokens=1, label="M/M/1", label_pos="left")
net.immediate("pridej", (3, 1.9), label="přidej", label_pos="above left")
net.loop("fronta", "pridej", w=6, bend=25)
net.arc("mm1", "pridej")
net.arc("pridej", "linka")

# M/M/2 na 15 č. j.
net.place("mm2", (4.5, 3.5), label="M/M/2", label_pos="above")
net.arc("pridej", "mm2", via=[(3, 3.5)])
net.timed("doba", (6, 3.5), "15", param_pos="above")
net.place("ubrat", (7.5, 3.5), label="ubrat", label_pos="above")
net.chain("mm2", "doba", "ubrat")

# po 15 č. j. odeber první volnou jednotku (p=1 předběhne obsazení), zpět na M/M/1
net.immediate("odeber", (9, 3.5), p=1, label="odeber", label_pos="right",
              param_pos="below right")
net.arc("ubrat", "odeber")
net.arc("linka", "odeber", via=[(4.5, 2.7), (9, 2.7)])
net.arc("odeber", "mm1", via=[(9, 4.6), (1.5, 4.6)])

net.invariant({"linka": 1, "obsluha": 1, "mm1": 1}, 2)
net.invariant({"mm1": 1, "mm2": 1, "ubrat": 1}, 1)
