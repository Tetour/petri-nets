from pn import Net

net = Net("04–07", "M/M/1 s údržbářem: každých exp(4 h) přijde, po aspoň 10 obsluhách údržba 20 min")
net.params = {"A": 10, "B": 6}

# M/M/1 (časy v minutách)
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(A)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta", label_pos="below")
net.place("linka", (5.4, 1.7), tokens=1, label="Linka", label_pos="below right")
net.immediate("obsaz", (4.5, 0))
net.place("obsluha", (6.3, 0))
net.timed("obsl", (7.8, 0), "exp(B)")
net.chain("prichod", "fronta", "obsaz", "obsluha", "obsl")
net.arc("linka", "obsaz")
net.arc("obsl", "linka", bend=-25)
net.place("konec", (9.3, 0))
net.immediate("odchod", (10.8, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# čítač dokončených obsluh; víc než 10 není potřeba si pamatovat
net.place("pocet", (9.3, 2.0), label="obsluhy", label_pos="left")
net.arc("obsl", "pocet")
net.immediate("nad10", (11.0, 2.0), label="nad 10", label_pos="right")
net.arc("pocet", "nad10", w=11, bend=20, w_pos="above")
net.arc("nad10", "pocet", w=10, bend=20, w_pos="below")

# údržbář: obchůzka exp(4 h), u linky rozhodne podle čítače a čítač vynuluje
net.place("obchuzka", (5.4, 5.3), tokens=1, label="údržbář na obchůzce", label_pos="above left")
net.timed("navrat", (7.35, 6.6), "exp(4 h)", horizontal=True, param_pos="above")
net.place("u_linky", (9.3, 5.3), label="u linky", label_pos="above right")
net.chain("obchuzka", "navrat", "u_linky")
net.immediate("aspon10", (9.3, 3.6), p=2, label="aspoň 10", label_pos="right",
              param_pos="below right")
net.arc("u_linky", "aspon10")
net.arc("pocet", "aspon10", w=10, w_pos="left")
net.immediate("vynulovani", (11.4, 3.6), p=1, label="vynulování", label_pos="right",
              param_pos="below right")
net.loop("u_linky", "vynulovani", bend=20)
net.arc("pocet", "vynulovani")
net.immediate("pokracuje", (7.35, 5.3), horizontal=True, label="pokračuje", label_pos="below")
net.chain("u_linky", "pokracuje", "obchuzka")

# údržba: počká na konec probíhající obsluhy, linku dostane přednostně (p=1)
net.place("ceka", (7.5, 3.6), label="čeká na linku", label_pos="below")
net.arc("aspon10", "ceka")
net.immediate("zahajeni", (5.4, 3.6), p=1, param_pos="above")
net.arc("ceka", "zahajeni")
net.arc("linka", "zahajeni")
net.place("udrzba", (3.6, 3.6), label="údržba", label_pos="above")
net.arc("zahajeni", "udrzba")
net.timed("t_udrzba", (3.6, 1.7), "20 min", horizontal=True, param_pos="below")
net.arc("udrzba", "t_udrzba")
net.arc("t_udrzba", "linka")
net.arc("t_udrzba", "obchuzka", via=[(2.2, 1.7), (2.2, 5.3)])

net.invariant({"linka": 1, "obsluha": 1, "udrzba": 1}, 1,
              name="linka je volná, obsluhuje, nebo je v údržbě")
net.invariant({"obchuzka": 1, "u_linky": 1, "ceka": 1, "udrzba": 1}, 1,
              name="jeden údržbář")
net.bound("pocet", 10)
