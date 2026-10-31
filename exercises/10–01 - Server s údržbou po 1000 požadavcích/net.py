from pn import Net

net = Net("10–01", "Server s údržbou po 1000 požadavcích (půlsemestrálka 2023/24, varianta A – převyprávěné zadání)",
          unit="s")

# příchody a obsluha
net.place("gen", (0, 0), tokens=1, label="příchody požadavků", label_pos="below")
net.timed("prichod", (1.5, 0), "exp(100 ms)", param_pos="above")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="fronta", label_pos="below")
net.immediate("obsaz", (8, 0))
net.place("obsluha", (9.5, 0))
net.timed("obsl", (11, 0), "exp(70 ms)", param_pos="below right")
net.place("konec", (13, 0), label="obsloužen", label_pos="above")
net.immediate("odchod", (14.5, 0), exit=True, label="odchod")
net.chain("prichod", "fronta", "obsaz", "obsluha", "obsl", "konec", "odchod")

net.place("server", (8, 1.8), tokens=1, label="server", label_pos="below right")
net.arc("server", "obsaz")
net.arc("obsl", "server", out=90, into=0)

# čítač obsloužených požadavků; po 1000. obsluze jde server do údržby (p=1 před obsazením)
net.place("pocet", (11, -1.8), label="počet obsloužených", label_pos="left")
net.arc("obsl", "pocet")
net.immediate("do_udrzby", (8, 3.6), p=1, label="do údržby", label_pos="above right",
              param_pos="below left")
# čítač je pod hlavní řadou (obsluha vrací server horní stranou), hrana obchází odchod zprava
net.arc("pocet", "do_udrzby", w=1000, w_pos="below", via=[(15.7, -1.8), (15.7, 3.6)])
net.arc("server", "do_udrzby")
net.place("udrzba", (6.5, 3.6), label="údržba", label_pos="above")
net.arc("do_udrzby", "udrzba")
net.timed("konec_udrzby", (6.5, 1.8), "100 s", param_pos="below")
net.arc("udrzba", "konec_udrzby")
net.arc("konec_udrzby", "server")

# stav „probíhá údržba“ je samostatné místo, které časovaný přechod nebere: testovací hrany
# vyhazování ho berou a vracejí, a kdyby byl vstupem odpočtu 100 s, každé vyhození by ho
# spustilo znovu (slajdy 137–139). Stav zruší okamžitý přechod po skončení údržby.
net.place("rezim", (3, 3.6), label="probíhá údržba", label_pos="left")
net.arc("do_udrzby", "rezim", via=[(8, 5.2), (3, 5.2)])
net.place("skoncila", (5, 1.8), label="údržba skončila", label_pos="below")
net.arc("konec_udrzby", "skoncila")
net.immediate("zrus_rezim", (5, 3.6), p=1, label="konec režimu", label_pos="above",
              param_pos="right")
net.arc("skoncila", "zrus_rezim")
net.arc("rezim", "zrus_rezim")

# během údržby jsou čekající i nově příchozí vyhozeni (testovací hrany na „probíhá údržba“)
net.immediate("vyhozeni", (3, 1.8), label="vyhození", label_pos="right")
net.arc("fronta", "vyhozeni")
net.loop("rezim", "vyhozeni", bend=20)
net.place("vyhozeny", (1.5, 1.8), label="bez obsluhy", label_pos="above")
net.arc("vyhozeni", "vyhozeny")
net.immediate("odchod_bez", (0, 1.8), exit=True, label="odchod", label_pos="above")
net.arc("vyhozeny", "odchod_bez")

net.invariant({"rezim": 1, "udrzba": -1, "skoncila": -1}, 0, name="probíhá údržba = údržba + skončila")
net.invariant({"server": 1, "obsluha": 1, "udrzba": 1}, 1,
              name="server je volný, obsluhuje, nebo je v údržbě")
net.bound("pocet", 1000)
