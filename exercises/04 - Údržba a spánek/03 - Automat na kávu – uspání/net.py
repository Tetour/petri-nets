from pn import Net

net = Net("M/M/1 – automat na kávu, po 5 č. j. bez požadavku usne, probuzení prodlouží obsluhu o 2")
net.params = {"A": 10, "B": 6}

# M/M/1
net.place("gen", (0, 0), tokens=1, label="příchody zákazníků", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(A)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="fronta", label_pos="above")
net.place("linka", (4.5, 1.6), tokens=1, label="Automat", label_pos="above right")
net.immediate("obsaz", (4.5, 0))
net.place("obsluha", (6, 0))
net.timed("obsl", (7.5, 0), "exp(B)", param_pos="below")
net.chain("prichod", "fronta", "obsaz", "obsluha", "obsl")
net.arc("linka", "obsaz")
net.arc("obsl", "linka", out=90, into=0)  # návrat automatu
net.place("konec", (9, 0), label="hotovo", label_pos="below")
net.immediate("odchod", (10.5, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# usnutí: odpočet 5 běží, jen dokud automat stojí volný (značka v místě Automat)
net.timed("usnuti", (4.5, 3.2), "5", label="usnutí", label_pos="above", param_pos="right")
net.arc("linka", "usnuti")
net.place("spi", (3, 3.2), label="spí", label_pos="above")
net.arc("usnuti", "spi")

# probuzení: zákazník obsadí spící automat, jeho obsluha trvá o 2 déle
# (hrana ze „spí“ vede oklikou kolem začátku řady pod ni)
net.immediate("probuzeni", (3, -1.6), label="probuzení", label_pos="below left")
net.arc("fronta", "probuzeni")
net.arc("spi", "probuzeni", via=[(-2, 3.2), (-2, -1.6)])
net.place("probouzeni", (4.5, -1.6), label="probouzení", label_pos="below")
net.timed("prodlouzeni", (6, -1.6), "2", param_pos="right")
net.chain("probuzeni", "probouzeni", "prodlouzeni", "obsluha")

net.invariant({"linka": 1, "obsluha": 1, "spi": 1, "probouzeni": 1}, 1,
              name="automat je volný, obsluhuje, spí, nebo se probouzí")
