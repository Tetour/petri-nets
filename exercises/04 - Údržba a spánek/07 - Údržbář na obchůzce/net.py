from pn import Net

net = Net("M/M/1 s údržbářem: každých exp(4 h) přijde, po aspoň 10 obsluhách údržba 20 min")
net.params = {"A": 10, "B": 6}

# M/M/1 (časy v minutách)
net.place("gen", (0, 0), tokens=1, label="příchody transakcí", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(A)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="fronta", label_pos="below")
net.place("linka", (4.5, 1.6), tokens=1, label="Linka", label_pos="above right")
net.immediate("obsaz", (4.5, 0))
net.place("obsluha", (6, 0))
net.timed("obsl", (7.5, 0), "exp(B)", param_pos="below left")
net.chain("prichod", "fronta", "obsaz", "obsluha", "obsl")
net.arc("linka", "obsaz")
net.arc("obsl", "linka", out=90, into=0)  # návrat linky
net.place("konec", (9, 0), label="hotovo", label_pos="below")
net.immediate("odchod", (10.5, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# čítač dokončených obsluh (hrana oklikou kolem konce řady); víc než 10 není potřeba
net.place("pocet", (10.5, 3.2), label="obsluhy", label_pos="above right")
net.arc("obsl", "pocet", via=[(7.5, -1.2), (13.5, -1.2), (13.5, 3.2)])
net.immediate("nad10", (10.5, 1.6), label="nad 10", label_pos="right")
net.arc("pocet", "nad10", w=11, bend=25, w_pos="right")
net.arc("nad10", "pocet", w=10, bend=25, w_pos="left")

# údržbář: obchůzka exp(4 h), u linky rozhodne podle čítače a čítač vynuluje
net.place("obchuzka", (1.5, 4.8), tokens=1, label="údržbář na obchůzce", label_pos="left")
net.timed("navrat", (4.5, 6.4), "exp(4 h)", param_pos="above")
net.place("u_linky", (9, 4.8), label="u linky", label_pos="above left")
net.arc("obchuzka", "navrat", via=[(1.5, 6.4)])
net.arc("navrat", "u_linky", via=[(9, 6.4)])
net.immediate("aspon10", (9, 3.2), p=2, label="aspoň 10", label_pos="below",
              param_pos="above left")
net.arc("u_linky", "aspon10")
net.arc("pocet", "aspon10", w=10, w_pos="above")
net.immediate("vynulovani", (10.5, 4.8), p=1, label="vynulování", label_pos="right",
              param_pos="above")
net.loop("u_linky", "vynulovani", bend=20)
net.arc("pocet", "vynulovani")
net.immediate("pokracuje", (4.5, 4.8), label="pokračuje", label_pos="above")
net.chain("u_linky", "pokracuje", "obchuzka")

# údržba: počká na konec probíhající obsluhy, linku dostane přednostně (p=1)
net.place("ceka", (6, 3.2), label="čeká na linku", label_pos="below")
net.arc("aspon10", "ceka")
net.immediate("zahajeni", (4.5, 3.2), p=1, param_pos="above")
net.arc("ceka", "zahajeni")
net.arc("linka", "zahajeni")
net.place("udrzba", (3, 3.2), label="údržba", label_pos="above")
net.arc("zahajeni", "udrzba")
net.timed("t_udrzba", (3, 1.6), "20 min", param_pos="below")
net.arc("udrzba", "t_udrzba")
net.arc("t_udrzba", "linka")
net.arc("t_udrzba", "obchuzka", via=[(1.5, 1.6)])

net.invariant({"linka": 1, "obsluha": 1, "udrzba": 1}, 1,
              name="linka je volná, obsluhuje, nebo je v údržbě")
net.invariant({"obchuzka": 1, "u_linky": 1, "ceka": 1, "udrzba": 1}, 1,
              name="jeden údržbář")
net.bound("pocet", 10)
