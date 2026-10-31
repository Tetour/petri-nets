from pn import Net

net = Net("05–10", "M/M/1, správce v intervalech exp(100) přidá na 20 č. j. druhou jednotku kapacity")
net.params = {"A": 5, "B": 4}

# M/M/1
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="below")
net.timed("prichod", (1.5, 0), "exp(A)", param_pos="below")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta", label_pos="below")
net.place("linka", (4.5, 1.7), tokens=1, label="Linka", label_pos="above right")
net.immediate("obsaz", (4.5, 0))
net.place("obsluha", (6, 0))
net.timed("obsl", (7.5, 0), "exp(B)")
net.chain("prichod", "fronta", "obsaz", "obsluha", "obsl")
net.arc("linka", "obsaz")
net.arc("obsl", "linka", bend=-15)
net.place("konec", (9, 0))
net.immediate("odchod", (10.5, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# správce: přijde, přidá jednotku kapacity, po 20 č. j. ji odebere a odejde
net.place("jinde", (1.5, 3.4), tokens=1, label="správce jinde", label_pos="left")
net.timed("prichod_s", (3, 3.4), "exp(100)", param_pos="above")
net.arc("jinde", "prichod_s")
net.arc("prichod_s", "linka")
net.place("pomaha", (4.5, 3.4), label="pomáhá", label_pos="above")
net.timed("doba", (6, 3.4), "20")
net.place("konci", (7.5, 3.4), label="končí", label_pos="above")
net.chain("prichod_s", "pomaha", "doba", "konci")

# jednotku odebere, až je volná (p=1 předběhne obsazení); dokončí rozpracovanou obsluhu
net.immediate("odeber", (7.5, 1.7), p=1, horizontal=True, label="odchod správce",
              label_pos="below right", param_pos="above left")
net.arc("konci", "odeber")
net.arc("linka", "odeber")
net.arc("odeber", "jinde", via=[(9, 1.7), (9, 4.9), (1.5, 4.9)])

net.invariant({"linka": 1, "obsluha": 1, "jinde": 1}, 2)
net.invariant({"jinde": 1, "pomaha": 1, "konci": 1}, 1, name="správce je jinde, pomáhá, nebo končí")
