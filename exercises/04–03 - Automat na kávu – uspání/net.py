from pn import Net

net = Net("04–03", "M/M/1 – automat na kávu, po 5 č. j. bez požadavku usne, probuzení prodlouží obsluhu o 2")
net.params = {"A": 10, "B": 6}

# M/M/1
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(A)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta")
net.place("linka", (5.4, 1.7), tokens=1, label="Automat", label_pos="left")
net.immediate("obsaz", (4.5, 0))
net.place("obsluha", (6.3, 0))
net.timed("obsl", (7.8, 0), "exp(B)")
net.chain("prichod", "fronta", "obsaz", "obsluha", "obsl")
net.arc("linka", "obsaz")
net.arc("obsl", "linka", bend=-25)
net.place("konec", (9.3, 0))
net.immediate("odchod", (10.8, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# usnutí: odpočet 5 běží, jen dokud automat stojí volný (značka v místě Automat)
net.timed("usnuti", (5.4, 3.4), "5", horizontal=True, label="usnutí", label_pos="right",
          param_pos="above")
net.arc("linka", "usnuti")
net.place("spi", (1.5, -1.8), label="spí", label_pos="below")
net.arc("usnuti", "spi", via=[(-1.2, 3.4), (-1.2, -1.8)])

# probuzení: zákazník obsadí spící automat, jeho obsluha trvá o 2 déle
net.immediate("probuzeni", (3, -1.8), label="probuzení", label_pos="below")
net.arc("fronta", "probuzeni")
net.arc("spi", "probuzeni")
net.place("probouzeni", (4.65, -1.8), label="probouzení", label_pos="below")
net.timed("prodlouzeni", (6.3, -1.8), "2", param_pos="right")
net.chain("probuzeni", "probouzeni", "prodlouzeni", "obsluha")

net.invariant({"linka": 1, "obsluha": 1, "spi": 1, "probouzeni": 1}, 1,
              name="automat je volný, obsluhuje, spí, nebo se probouzí")
