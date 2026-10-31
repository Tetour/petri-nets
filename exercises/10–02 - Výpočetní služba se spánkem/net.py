from pn import Net

net = Net("10–02", "Výpočetní služba se spánkem (půlsemestrálka 2023/24, pravděpodobně varianta B)", unit="s")

# příchody a obsluha
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="below")
net.timed("prichod", (1.5, 0), "exp(100 s)", param_pos="below")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta", label_pos="below")
net.immediate("obsaz", (4.5, 0))
net.place("obsluha", (6, 0))
net.timed("obsl", (7.5, 0), "exp(5 s)")
net.chain("prichod", "fronta", "obsaz", "obsluha", "obsl")
net.place("konec", (9, 0))
net.immediate("odchod", (10.5, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# služba: volná (značka v místě Služba), spí, nebo se probouzí
net.place("sluzba", (7.5, 1.8), tokens=1, label="Služba", label_pos="right")
net.arc("sluzba", "obsaz")
net.arc("obsl", "sluzba")

# usnutí po 200 s nečinnosti: odpočet běží, jen dokud je značka v místě Služba
net.timed("usnuti", (7.5, 3.6), "200 s", param_pos="right", label="usnutí", label_pos="above")
net.place("spi", (3, 3.6), label="spící služba", label_pos="above")
net.arc("sluzba", "usnuti")
net.arc("usnuti", "spi")

# probuzení nově příchozím požadavkem (testovací hrany: požadavek zůstává ve Frontě)
net.immediate("probuzeni", (3, 1.8), label="probuzení", label_pos="left")
net.arc("spi", "probuzeni")
net.loop("fronta", "probuzeni", bend=25)
net.place("inicializace", (4.5, 1.8), label="iniciace", label_pos="above")
net.timed("init", (6, 1.8), "5 s", param_pos="above")
net.chain("probuzeni", "inicializace", "init", "sluzba")

net.invariant({"sluzba": 1, "obsluha": 1, "spi": 1, "inicializace": 1}, 1,
              name="služba je volná, obsluhuje, spí, nebo se probouzí")
