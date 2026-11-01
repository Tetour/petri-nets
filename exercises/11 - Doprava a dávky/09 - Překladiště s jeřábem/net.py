from pn import Net

net = Net("Překladiště s jeřábem (půlsemestrálky 2014–19, Z5)")

# auta s nákladem: přijíždí jen během pracovní doby, jeřáb vyloží 1 jednotku
net.place("gen", (0, 0), tokens=1, label="příchody aut", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(10 min)", param_pos="below")
net.loop("gen", "prichod")
net.place("rampa", (3, 0), label="Rampa", label_pos="below")
net.place("jerab", (4.5, 1.7), tokens=1, label="Jeřábník", label_pos="above right")
net.immediate("obsaz", (4.5, 0))
net.place("vykladka", (6, 0))
net.timed("presun", (7.5, 0), "exp(3 min)", param_pos="below")
net.chain("prichod", "rampa", "obsaz", "vykladka", "presun")
net.arc("jerab", "obsaz")
net.arc("presun", "jerab", out=90, into=0)
net.place("konec", (9, 0), label="vyloženo", label_pos="below")
net.immediate("odjezd", (10.5, 0), exit=True, label="odjezd", label_pos="below")
net.chain("presun", "konec", "odjezd")

# 10 min bez práce -> obchůzka 5–10 min (smyčka nad jeřábníkem)
net.timed("necinnost", (3, 1.7), "10 min", param_pos="left")
net.place("obchuzka", (3, 3.2), label="obchůzka", label_pos="above")
net.timed("obch", (4.5, 3.2), "5–10 min", param_pos="right")
net.chain("jerab", "necinnost", "obchuzka", "obch", "jerab")

# pracovní doba 8 h / odpočinek 16 h; mimo pracovní dobu nemá generátor značku
net.immediate("stop", (0, -1.8))
net.arc("gen", "stop")
net.place("odpocinek", (0, -3.4), label="odpočinek", label_pos="below")
net.timed("t16", (1.5, -3.4), "16 h", param_pos="above")
net.place("prace", (3, -3.4), tokens=1, label="pracovní doba", label_pos="below")
net.timed("t8", (3, -1.8), "8 h", param_pos="right")
net.place("konec_smeny", (1.5, -1.8), label="konec směny", label_pos="above")
net.chain("stop", "odpocinek", "t16", "prace", "t8", "konec_smeny", "stop")
net.arc("t16", "gen", via=[(1.5, -4.6), (-1.2, -4.6), (-1.2, 0)])

net.invariant({"jerab": 1, "vykladka": 1, "obchuzka": 1}, 1,
              name="jeřábník volný, vykládá, nebo na obchůzce")
net.invariant({"prace": 1, "konec_smeny": 1, "odpocinek": 1}, 1)
net.invariant({"gen": 1, "odpocinek": 1}, 1, name="generátor běží jen v pracovní době")
net.sim_events = 50000
