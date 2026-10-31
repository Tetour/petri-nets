from pn import Net

net = Net("05–09", "M/M/2, údržba exp(100) zabere obě jednotky linky na 10 č. j.")
net.params = {"A": 6, "B": 9}

# M/M/2
net.place("gen", (0, 0), tokens=1, label="příchody zákazníků", label_pos="below")
net.timed("prichod", (1.5, 0), "exp(A)", param_pos="above")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta", label_pos="below")
net.place("linka", (4.5, 1.6), tokens=2, label="Linka", label_pos="below left")
net.immediate("obsaz", (4.5, 0))
net.place("obsluha", (6, 0))
net.timed("obsl", (7.5, 0), "exp(B)")
net.chain("prichod", "fronta", "obsaz", "obsluha", "obsl")
net.arc("linka", "obsaz")
net.arc("obsl", "linka", out=90, into=0)
net.place("konec", (9, 0))
net.immediate("odchod", (10.5, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# údržbový proces v horní řadě
net.place("gen_u", (-1.2, 3.4), tokens=1, label="příchody údržby", label_pos="left")
net.timed("prichod_u", (0.3, 3.4), "exp(100)", param_pos="below")
net.loop("gen_u", "prichod_u")
net.place("ceka", (2, 3.4), label="údržba čeká", label_pos="below")
net.arc("prichod_u", "ceka")

# dokud údržba čeká (test vedle), bere každou uvolněnou jednotku (p=1 předběhne zákazníky)
net.immediate("zabira", (3.8, 3.4), p=1, label="zabírá", label_pos="above",
              param_pos="below right")
net.loop("ceka", "zabira", bend=25)
net.arc("linka", "zabira", via=[(3.8, 1.6)])
net.place("zabrano", (5.3, 3.4), label="zabráno", label_pos="above")
net.arc("zabira", "zabrano")

# obě jednotky zabrané: údržba 10 č. j., pak obě shora zpět do Linky
net.immediate("zacni", (6.8, 3.4), label="začni", label_pos="below")
net.arc("ceka", "zacni", via=[(2, 4.6), (6.8, 4.6)])
net.arc("zabrano", "zacni", w=2, w_pos="below")
net.place("udrzba", (8.3, 3.4), label="údržba", label_pos="above")
net.timed("t10", (9.8, 3.4), "10", param_pos="right")
net.chain("zacni", "udrzba", "t10")
net.arc("t10", "linka", w=2, via=[(9.8, 2.4), (4.5, 2.4)], w_pos="right")

net.invariant({"linka": 1, "obsluha": 1, "zabrano": 1, "udrzba": 2}, 2)
net.sim_events = 60000
