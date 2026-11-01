from pn import Net

net = Net("M/M/1 s frontou omezenou na 10 transakcí")
net.params = {"A": 5, "B": 6}   # přetížená linka, aby se fronta často zaplnila

# příchod a vstup do fronty, je-li v ní místo; jinak odmítnutí
net.place("gen", (0, 0), tokens=1, label="příchody transakcí", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(A)")
net.loop("gen", "prichod")
net.place("prisel", (3, 0), label="přišel", label_pos="above")
net.immediate("vstup", (4.5, 0), p=1, param_pos="above")
net.place("fronta", (6, 0), label="fronta", label_pos="above")
net.chain("prichod", "prisel", "vstup", "fronta")
net.immediate("odmitnuti", (3, -1.8), p=0, exit=True, label="odmítnutí", label_pos="below",
              param_pos="left")
net.arc("prisel", "odmitnuti")

# doplněk fronty: 10 volných míst, vstup bere, obsazení linky vrací
net.place("volno", (6, -1.8), tokens=10, label="volná místa ve frontě", label_pos="below")
net.arc("volno", "vstup", via=[(4.5, -1.8)])

# linka
net.place("linka", (7.5, 1.6), tokens=1, label="Linka")
net.immediate("obsaz", (7.5, 0))
net.place("obsluha", (9, 0))
net.timed("obsl", (10.5, 0), "exp(B)")
net.chain("fronta", "obsaz", "obsluha", "obsl")
net.arc("linka", "obsaz")
net.arc("obsl", "linka", out=90, into=0)
net.arc("obsaz", "volno", via=[(7.5, -1.8)])
net.place("konec", (12, 0), label="konec", label_pos="above")
net.immediate("odchod", (13.5, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

net.invariant({"linka": 1, "obsluha": 1}, 1)
net.invariant({"fronta": 1, "volno": 1}, 10)
net.bound("prisel", 1)
