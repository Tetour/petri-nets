from pn import Net

net = Net("05–09", "M/M/2, údržba exp(100) zabere obě jednotky linky na 10 č. j.")
net.params = {"A": 6, "B": 9}

# M/M/2
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="below")
net.timed("prichod", (1.5, 0), "exp(A)", param_pos="below")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta", label_pos="below")
net.place("linka", (4.5, 1.7), tokens=2, label="Linka", label_pos="below left")
net.immediate("obsaz", (4.5, 0))
net.place("obsluha", (6, 0))
net.timed("obsl", (7.5, 0), "exp(B)")
net.chain("prichod", "fronta", "obsaz", "obsluha", "obsl")
net.arc("linka", "obsaz")
net.arc("obsl", "linka", bend=-25)
net.place("konec", (9, 0))
net.immediate("odchod", (10.5, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# údržbový proces
net.place("gen_u", (-0.3, 3.9), tokens=1, label="generátor údržby", label_pos="left")
net.timed("prichod_u", (1.2, 3.9), "exp(100)", param_pos="above")
net.loop("gen_u", "prichod_u")
net.place("ceka", (2.7, 3.9), label="údržba čeká", label_pos="above")
net.arc("prichod_u", "ceka")

# dokud údržba čeká, bere každou uvolněnou jednotku (p=1 předběhne zákazníky)
net.immediate("zabira", (2.7, 1.7), p=1, horizontal=True, label="zabírá", label_pos="below",
              param_pos="left")
net.loop("ceka", "zabira", bend=15)
net.arc("linka", "zabira")
net.place("zabrano", (3.6, 2.8), label="zabráno", label_pos="right")
net.arc("zabira", "zabrano")

# obě jednotky zabrané: údržba 10 č. j., pak obě vrátí
net.immediate("zacni", (4.5, 3.9), label="začni", label_pos="above")
net.arc("ceka", "zacni")
net.arc("zabrano", "zacni", w=2, w_pos="above left")
net.place("udrzba", (6, 3.9), label="údržba", label_pos="above")
net.timed("t10", (7.5, 3.9), "10", param_pos="above")
net.chain("zacni", "udrzba", "t10")
net.arc("t10", "linka", w=2, w_pos="above right")

net.invariant({"linka": 1, "obsluha": 1, "zabrano": 1, "udrzba": 2}, 2)
net.sim_events = 60000
