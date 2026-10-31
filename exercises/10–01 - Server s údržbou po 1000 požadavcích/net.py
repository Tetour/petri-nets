from pn import Net

net = Net("10–01", "Server s údržbou po 1000 požadavcích (půlsemestrálka 2023/24, varianta A – převyprávěné zadání)",
          unit="s")

# příchody a obsluha
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="below")
net.timed("prichod", (1.5, 0), "exp(100 ms)", param_pos="below")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta", label_pos="below")
net.place("server", (4.5, 1.8), tokens=1, label="Server", label_pos="above right")
net.immediate("obsaz", (4.5, 0))
net.place("obsluha", (6, 0))
net.timed("obsl", (7.5, 0), "exp(70 ms)")
net.chain("prichod", "fronta", "obsaz", "obsluha", "obsl")
net.arc("server", "obsaz")
net.arc("obsl", "server", bend=-25)
net.place("konec", (9, 0))
net.immediate("odchod", (10.5, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# čítač obsloužených požadavků; po 1000. obsluze jde server do údržby
net.place("pocet", (7.5, 3.6), label="obsloužené", label_pos="right")
net.arc("obsl", "pocet")
net.immediate("do_udrzby", (4.5, 3.6), p=1, param_pos="above")
net.arc("pocet", "do_udrzby", w=1000, w_pos="above")
net.arc("server", "do_udrzby")
net.place("udrzba", (3, 3.6), label="Údržba", label_pos="above")
net.arc("do_udrzby", "udrzba")
net.timed("konec_udrzby", (3, 1.8), "100 s", param_pos="below")
net.arc("udrzba", "konec_udrzby")
net.arc("konec_udrzby", "server")

# během údržby jsou čekající i nově příchozí vyhozeni (testovací hrany na Údržbu)
net.immediate("vyhozeni", (1.5, 1.8), label="vyhození", label_pos="left")
net.arc("fronta", "vyhozeni")
net.loop("udrzba", "vyhozeni", bend=20)
net.place("vyhozeny", (1.5, 3.6), label="bez obsluhy", label_pos="above")
net.arc("vyhozeni", "vyhozeny")
net.immediate("odchod_bez", (0, 3.6), exit=True, label="odchod", label_pos="above")
net.arc("vyhozeny", "odchod_bez")

net.invariant({"server": 1, "obsluha": 1, "udrzba": 1}, 1,
              name="server je volný, obsluhuje, nebo je v údržbě")
net.bound("pocet", 1000)
