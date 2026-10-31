from pn import Net

net = Net("04–02", "M/M/1 – automat na kávu, po každých 50 obsluhách údržba na 20 č. j.")
net.params = {"A": 10, "B": 6}

# M/M/1
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(A)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta")
net.place("linka", (5.4, 1.7), tokens=1, label="Automat", label_pos="left")
net.immediate("obsaz", (4.5, 0))
net.place("obsluha", (6.3, 0))
net.timed("obsl", (7.8, 0), "exp(B)")
net.chain("prichod", "fronta", "obsaz", "obsluha", "obsl")
net.arc("linka", "obsaz")
net.arc("obsl", "linka", bend=-25)
net.place("konec", (9.3, 0))
net.immediate("odchod", (10.8, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# čítač obsluh; po 50. obsluze vezme údržba volný automat dřív než další zákazník (p=1)
net.place("pocet", (9, 1.7), label="počet obsluh", label_pos="right")
net.arc("obsl", "pocet")
net.immediate("do_udrzby", (9, 3.4), p=1, horizontal=True, param_pos="right")
net.arc("pocet", "do_udrzby", w=50, w_pos="right")
net.arc("linka", "do_udrzby", bend=-10)
net.place("udrzba", (7.2, 3.4), label="údržba", label_pos="above")
net.arc("do_udrzby", "udrzba")
net.timed("konec_udrzby", (5.4, 3.4), "20", horizontal=True, param_pos="left")
net.arc("udrzba", "konec_udrzby")
net.arc("konec_udrzby", "linka")

net.invariant({"linka": 1, "obsluha": 1, "udrzba": 1}, 1,
              name="automat je volný, obsluhuje, nebo je v údržbě")
net.bound("pocet", 50)
