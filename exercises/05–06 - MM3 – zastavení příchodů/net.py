from pn import Net

net = Net("05–06", "M/M/3, příchody stojí od obsazení všech linek, dokud nejsou volné aspoň dvě")
net.params = {"A": 3, "B": 8}

# M/M/3
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="below left")
net.timed("prichod", (1.5, 0), "exp(A)", param_pos="below")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta", label_pos="above")
net.place("linky", (4.5, 1.7), tokens=3, label="Linky", label_pos="above right")
net.immediate("obsaz", (4.5, 0))
net.place("obsluha", (6, 0))
net.timed("obsl", (7.5, 0), "exp(B)")
net.chain("prichod", "fronta", "obsaz", "obsluha", "obsl")
net.arc("linky", "obsaz")
net.arc("obsl", "linky", bend=-25)
net.place("konec", (9, 0))
net.immediate("odchod", (10.5, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# všechny 3 linky obsazené: generátor přijde o značku
net.immediate("zastav", (6, -1.8), horizontal=True, label="zastav", label_pos="right",
              param_pos="right")
net.loop("obsluha", "zastav", w=3, bend=20)
net.arc("gen", "zastav", via=[(0, -1.8)])
net.place("zastaveno", (0, 1.7), label="zastaveno", label_pos="above")
net.arc("zastav", "zastaveno", via=[(6, -3.2), (-1.8, -3.2), (-1.8, 1.7)])

# aspoň 2 volné linky: generátor se rozběhne
net.immediate("rozbeh", (1.5, 1.7), horizontal=True, label="rozběh", label_pos="above")
net.arc("zastaveno", "rozbeh")
net.loop("linky", "rozbeh", w=2, bend=10)
net.arc("rozbeh", "gen")

net.invariant({"linky": 1, "obsluha": 1}, 3)
net.invariant({"gen": 1, "zastaveno": 1}, 1, name="příchody běží, nebo stojí")
net.bound("fronta", 1)
