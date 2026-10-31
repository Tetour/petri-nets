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
net.immediate("do_udrzby", (4.5, 3.6), p=1, param_pos="below left")
net.arc("pocet", "do_udrzby", w=1000, w_pos="above")
net.arc("server", "do_udrzby")
net.place("udrzba", (4.5, 5.2), label="Údržba", label_pos="above")
net.arc("do_udrzby", "udrzba")
net.timed("konec_udrzby", (3, 5.2), "100 s", param_pos="above")
net.arc("udrzba", "konec_udrzby")
net.arc("konec_udrzby", "server", via=[(3, 1.8)])

# stav „probíhá údržba“ je samostatné místo, které časovaný přechod nebere: testovací hrany
# vyhazování ho berou a vracejí, a kdyby byl vstupem odpočtu 100 s, každé vyhození by ho
# spustilo znovu (slajdy 137–139). Stav zruší okamžitý přechod po skončení údržby.
net.place("rezim", (1.5, 3.6), label="probíhá údržba", label_pos="above right")
net.arc("do_udrzby", "rezim")
net.place("skoncila", (1.5, 5.2), label="údržba skončila", label_pos="below")
net.arc("konec_udrzby", "skoncila")
net.immediate("zrus_rezim", (0, 5.2), p=1, label="konec režimu", label_pos="left", param_pos="below")
net.arc("skoncila", "zrus_rezim")
net.arc("rezim", "zrus_rezim")

# během údržby jsou čekající i nově příchozí vyhozeni (testovací hrany na „probíhá údržba“)
net.immediate("vyhozeni", (1.5, 1.8), label="vyhození", label_pos="below left")
net.arc("fronta", "vyhozeni")
net.loop("rezim", "vyhozeni", bend=20)
net.place("vyhozeny", (-0.6, 1.8), label="bez obsluhy", label_pos="left")
net.arc("vyhozeni", "vyhozeny")
net.immediate("odchod_bez", (-0.6, 3.4), exit=True, label="odchod", label_pos="left")
net.arc("vyhozeny", "odchod_bez")

net.invariant({"rezim": 1, "udrzba": -1, "skoncila": -1}, 0, name="probíhá údržba = Údržba + skončila")
net.invariant({"server": 1, "obsluha": 1, "udrzba": 1}, 1,
              name="server je volný, obsluhuje, nebo je v údržbě")
net.bound("pocet", 1000)
