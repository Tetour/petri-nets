from pn import Net

net = Net("05–06", "M/M/3, příchody stojí od obsazení všech linek, dokud nejsou volné aspoň dvě")
net.params = {"A": 3, "B": 8}

# M/M/3, Linky pod obsazením (návrat zespodu)
net.place("gen", (0, 0), tokens=1, label="příchody transakcí", label_pos="left")
net.timed("prichod", (1.5, 0), "exp(A)", param_pos="below")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta", label_pos="above")
net.place("linky", (4.5, -1.6), tokens=3, label="Linky", label_pos="below")
net.immediate("obsaz", (4.5, 0))
net.place("obsluha", (6, 0))
net.timed("obsl", (7.5, 0), "exp(B)", param_pos="above")
net.chain("prichod", "fronta", "obsaz", "obsluha", "obsl")
net.arc("linky", "obsaz")
net.arc("obsl", "linky", out=270, into=0)
net.place("konec", (9, 0))
net.immediate("odchod", (10.5, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# všechny 3 linky obsazené (test 3 nad obsluhou): příchody přijdou o značku (shora)
net.immediate("zastav", (6, 1.6), label="zastav", label_pos="above")
net.loop("obsluha", "zastav", w=3, bend=25)
net.arc("gen", "zastav", via=[(0, 1.6)])
net.place("zastaveno", (9, 1.6), label="zastaveno", label_pos="above")
net.arc("zastav", "zastaveno")

# aspoň 2 volné linky (test 2 vedle Linek): značka se vrací příchodům (zespodu)
net.immediate("rozbeh", (3, -1.6), label="rozběh", label_pos="above")
net.loop("linky", "rozbeh", w=2, bend=25)
net.arc("zastaveno", "rozbeh", via=[(12, 1.6), (12, -3.2), (3, -3.2)])
net.arc("rozbeh", "gen", via=[(0, -1.6)])

net.invariant({"linky": 1, "obsluha": 1}, 3)
net.invariant({"gen": 1, "zastaveno": 1}, 1, name="příchody běží, nebo stojí")
net.bound("fronta", 1)
