from pn import Net

net = Net("11–09", "Překladiště s jeřábem (půlsemestrálky 2014–19, Z5)")

# auta s nákladem: přijíždí jen během pracovní doby, jeřáb vyloží 1 jednotku
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(10 min)")
net.loop("gen", "prichod")
net.place("rampa", (3, 0), label="Rampa", label_pos="above")
net.place("jerab", (4.5, 1.7), tokens=1, label="Jeřábník", label_pos="left")
net.immediate("obsaz", (4.5, 0))
net.place("vykladka", (6, 0))
net.timed("presun", (7.5, 0), "exp(3 min)")
net.chain("prichod", "rampa", "obsaz", "vykladka", "presun")
net.arc("jerab", "obsaz")
net.arc("presun", "jerab", bend=-25)
net.place("konec", (9, 0), label="vyloženo", label_pos="above")
net.immediate("odjezd", (10.5, 0), exit=True, label="odjezd", label_pos="above")
net.chain("presun", "konec", "odjezd")

# 10 min bez práce -> obchůzka 5–10 min
net.timed("necinnost", (3.6, 3.2), "10 min", param_pos="left")
net.place("obchuzka", (4.5, 4.4), label="obchůzka", label_pos="above")
net.timed("obch", (5.4, 3.2), "5–10 min", param_pos="right")
net.chain("jerab", "necinnost", "obchuzka", "obch", "jerab")

# pracovní doba 8 h / odpočinek 16 h; mimo pracovní dobu generátor stojí
net.immediate("stop", (0, -1.8), label="zastavení příchodů", label_pos="right")
net.arc("gen", "stop")
net.place("odpocinek", (-1.5, -1.8), label="odpočinek", label_pos="above")
net.arc("stop", "odpocinek")
net.timed("t16", (-3, -1.8), "16 h", param_pos="left")
net.arc("odpocinek", "t16")
net.arc("t16", "gen", via=[(-3, 0)])
net.place("prace", (-3, -3.4), tokens=1, label="pracovní doba", label_pos="below")
net.arc("t16", "prace")
net.timed("t8", (-1.5, -3.4), "8 h", param_pos="below")
net.place("konec_smeny", (0, -3.4), label="konec směny", label_pos="below")
net.chain("prace", "t8", "konec_smeny", "stop")

net.invariant({"jerab": 1, "vykladka": 1, "obchuzka": 1}, 1,
              name="jeřábník volný, vykládá, nebo na obchůzce")
net.invariant({"prace": 1, "konec_smeny": 1, "odpocinek": 1}, 1)
net.invariant({"gen": 1, "odpocinek": 1}, 1, name="generátor běží jen v pracovní době")
net.sim_events = 50000
