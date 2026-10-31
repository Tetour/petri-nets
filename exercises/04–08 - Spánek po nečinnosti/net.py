from pn import Net

net = Net("04–08", "M/M/1 – linka po 10 min nečinnosti usne, probuzení požadavkem trvá 5 min")
net.params = {"A": 10, "B": 6}

# M/M/1 (časy v minutách)
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(A)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta", label_pos="below")
net.immediate("obsaz", (4.5, 0))
net.place("obsluha", (6.3, 0))
net.timed("obsl", (7.8, 0), "exp(B)")
net.chain("prichod", "fronta", "obsaz", "obsluha", "obsl")
net.place("konec", (9.3, 0))
net.immediate("odchod", (10.8, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# linka: volná (značka v místě Linka), obsluhuje, spí, nebo se probouzí
net.place("linka", (7.8, 1.7), tokens=1, label="Linka", label_pos="right")
net.arc("linka", "obsaz")
net.arc("obsl", "linka")

# usnutí po 10 min nečinnosti: odpočet běží, jen dokud je značka v místě Linka
net.timed("usnuti", (7.8, 3.4), "10 min", param_pos="right", label="usnutí", label_pos="above")
net.place("spi", (3, 3.4), label="spí", label_pos="above")
net.arc("linka", "usnuti")
net.arc("usnuti", "spi")

# probuzení příchozím požadavkem (testovací hrany: požadavek zůstává ve Frontě)
net.immediate("probuzeni", (3, 1.7), label="probuzení", label_pos="left")
net.arc("spi", "probuzeni")
net.loop("fronta", "probuzeni", bend=25)
net.place("probouzeni", (4.65, 1.7), label="probouzí se", label_pos="above")
net.timed("t_probuzeni", (6.3, 1.7), "5 min", param_pos="above")
net.chain("probuzeni", "probouzeni", "t_probuzeni", "linka")

net.invariant({"linka": 1, "obsluha": 1, "spi": 1, "probouzeni": 1}, 1,
              name="linka je volná, obsluhuje, spí, nebo se probouzí")
