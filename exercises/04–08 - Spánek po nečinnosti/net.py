from pn import Net

net = Net("04–08", "M/M/1 – linka po 10 min nečinnosti usne, probuzení požadavkem trvá 5 min")
net.params = {"A": 10, "B": 6}

# M/M/1 (časy v minutách); mezi frontou a obsazením je místo pro probouzení nad nimi
net.place("gen", (0, 0), tokens=1, label="příchody požadavků", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(A)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="fronta", label_pos="below")
net.immediate("obsaz", (7.5, 0))
net.place("obsluha", (9, 0))
net.timed("obsl", (10.5, 0), "exp(B)", param_pos="below")
net.chain("prichod", "fronta", "obsaz", "obsluha", "obsl")
net.place("konec", (12, 0), label="hotovo", label_pos="below")
net.immediate("odchod", (13.5, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# linka: volná (značka v místě Linka), obsluhuje, spí, nebo se probouzí
net.place("linka", (7.5, 1.6), tokens=1, label="Linka", label_pos="above right")
net.arc("linka", "obsaz")
net.arc("obsl", "linka", out=90, into=0)  # návrat linky

# usnutí po 10 min nečinnosti: odpočet běží, jen dokud je značka v místě Linka
net.timed("usnuti", (7.5, 3.2), "10 min", label="usnutí", label_pos="above",
          param_pos="right")
net.arc("linka", "usnuti")
net.place("spi", (3, 3.2), label="spí", label_pos="above")
net.arc("usnuti", "spi")

# probuzení příchozím požadavkem (testovací hrany: požadavek zůstává ve frontě)
net.immediate("probuzeni", (3, 1.6), label="probuzení", label_pos="left")
net.arc("spi", "probuzeni")
net.loop("fronta", "probuzeni", bend=25)
net.place("probouzeni", (4.5, 1.6), label="probouzí se", label_pos="above")
net.timed("t_probuzeni", (6, 1.6), "5 min", param_pos="above")
net.chain("probuzeni", "probouzeni", "t_probuzeni", "linka")

net.invariant({"linka": 1, "obsluha": 1, "spi": 1, "probouzeni": 1}, 1,
              name="linka je volná, obsluhuje, spí, nebo se probouzí")
