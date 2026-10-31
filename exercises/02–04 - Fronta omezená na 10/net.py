from pn import Net

net = Net("02–04", "M/M/1 s frontou omezenou na 10 transakcí")
net.params = {"A": 5, "B": 6}   # přetížená linka, aby se fronta často zaplnila

# příchod a vstup do fronty, je-li v ní místo
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(A)")
net.loop("gen", "prichod")
net.place("prisel", (3, 0), label="přišel", label_pos="above")
net.immediate("vstup", (4.5, 0), p=1, param_pos="above")
net.place("fronta", (6, 0), label="Fronta", label_pos="above")
net.chain("prichod", "prisel", "vstup", "fronta")
net.place("volno", (6, -1.7), tokens=10, label="volná místa ve frontě", label_pos="below")
net.arc("volno", "vstup")
net.immediate("odmitnuti", (3, -1.7), horizontal=True, exit=True, label="odmítnutí",
              label_pos="below")
net.arc("prisel", "odmitnuti")

# linka
net.place("linka", (7.5, 1.6), tokens=1, label="Linka")
net.immediate("obsaz", (7.5, 0))
net.place("obsluha", (9, 0))
net.timed("obsl", (10.5, 0), "exp(B)")
net.chain("fronta", "obsaz", "obsluha", "obsl")
net.arc("linka", "obsaz")
net.arc("obsl", "linka", bend=-25)
net.arc("obsaz", "volno")
net.place("konec", (12, 0), label="konec", label_pos="above")
net.immediate("odchod", (13.5, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

net.invariant({"linka": 1, "obsluha": 1}, 1)
net.invariant({"fronta": 1, "volno": 1}, 10)
net.bound("prisel", 1)
