from pn import Net

net = Net("M/M/1, správce v intervalech exp(100) přidá na 20 č. j. druhou jednotku kapacity")
net.params = {"A": 5, "B": 4}

# M/M/1
net.place("gen", (0, 0), tokens=1, label="příchody zákazníků", label_pos="left")
net.timed("prichod", (1.5, 0), "exp(A)", param_pos="below")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="fronta", label_pos="below")
net.place("linka", (4.5, 1.9), tokens=1, label="Linka", label_pos="above left")
net.immediate("obsaz", (4.5, 0))
net.place("obsluha", (6, 0))
net.timed("obsl", (7.5, 0), "exp(B)")
net.chain("prichod", "fronta", "obsaz", "obsluha", "obsl")
net.arc("linka", "obsaz")
net.arc("obsl", "linka", out=90, into=0)
net.place("konec", (9, 0))
net.immediate("odchod", (10.5, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# správce: přijde, přidá jednotku kapacity (zleva do Linky), po 20 č. j. ji odebere a odejde
net.place("jinde", (1.5, 1.9), tokens=1, label="správce jinde", label_pos="left")
net.timed("prichod_s", (3, 1.9), "exp(100)", param_pos="below")
net.arc("jinde", "prichod_s")
net.arc("prichod_s", "linka")
net.place("pomaha", (4.5, 3.5), label="pomáhá", label_pos="above")
net.arc("prichod_s", "pomaha", via=[(3, 3.5)])
net.timed("doba", (6, 3.5), "20", param_pos="above")
net.place("konci", (7.5, 3.5), label="končí", label_pos="above")
net.chain("pomaha", "doba", "konci")

# jednotku odebere, až je volná (p=1 předběhne obsazení); dokončí rozpracovanou obsluhu
net.immediate("odeber", (9, 3.5), p=1, label="odchod správce", label_pos="right",
              param_pos="below right")
net.arc("konci", "odeber")
net.arc("linka", "odeber", via=[(4.5, 2.7), (9, 2.7)])
net.arc("odeber", "jinde", via=[(9, 4.6), (1.5, 4.6)])

net.invariant({"linka": 1, "obsluha": 1, "jinde": 1}, 2)
net.invariant({"jinde": 1, "pomaha": 1, "konci": 1}, 1, name="správce je jinde, pomáhá, nebo končí")
