from pn import Net

net = Net("05–07", "M/M/1, každá 100. příchozí transakce vyprázdní frontu")
net.params = {"A": 5, "B": 4.5}

# příchod: transakce do místa „příchozí“, započte se do čítače
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(A)", param_pos="above")
net.loop("gen", "prichod")
net.place("nova", (3, 0), label="příchozí", label_pos="above")
net.immediate("do_fronty", (4.5, 0))
net.place("fronta", (6, 0), label="Fronta", label_pos="above left")
net.chain("prichod", "nova", "do_fronty", "fronta")
net.place("citac", (4.5, -1.8), label="čítač", label_pos="left")
net.arc("prichod", "citac")

# M/M/1
net.place("linka", (7.5, 1.7), tokens=1, label="Linka")
net.immediate("obsaz", (7.5, 0))
net.place("obsluha", (9, 0))
net.timed("obsl", (10.5, 0), "exp(B)")
net.chain("fronta", "obsaz", "obsluha", "obsl")
net.arc("linka", "obsaz")
net.arc("obsl", "linka", bend=-25)
net.place("konec", (12, 0))
net.immediate("odchod", (13.5, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# 100. příchod: dokud je čítač plný, vyhazuj čekající (p=2), pak vynuluj (p=1);
# teprve potom (p=0) jde 100. transakce sama do fronty
net.immediate("vyhod", (6, -1.8), p=2, horizontal=True, label="vyhoď", label_pos="below right",
              param_pos="above right")
net.arc("fronta", "vyhod")
net.arc("citac", "vyhod", w=100, bend=28, w_pos="above")
net.arc("vyhod", "citac", w=100, bend=28, w_pos="below")
net.place("vyhozena", (7.5, -1.8))
net.immediate("vyhozeni", (9, -1.8), exit=True, label="odchod bez obsluhy", label_pos="below")
net.chain("vyhod", "vyhozena", "vyhozeni")
net.immediate("vynuluj", (4.5, -3.4), p=1, horizontal=True, label="vynuluj", label_pos="right",
              param_pos="left")
net.arc("citac", "vynuluj", w=100, w_pos="right")

net.invariant({"linka": 1, "obsluha": 1}, 1)
net.bound("citac", 99)
