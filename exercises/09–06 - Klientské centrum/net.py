from pn import Net

net = Net("09–06", "Klientské centrum (půlsemestrálka 2023/24, varianta D)")

# příchody a obsluha
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="left")
net.timed("prichod", (1.5, 0), "exp(20 min)", param_pos="above")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta", label_pos="above")
net.place("pracovnice", (4.5, 1.7), tokens=1, label="Pracovnice")
net.immediate("obsaz", (4.5, 0))
net.place("obsluha", (6, 0))
net.timed("obsl", (7.5, 0), "exp(10 min)")
net.chain("prichod", "fronta", "obsaz", "obsluha", "obsl")
net.arc("pracovnice", "obsaz")
net.arc("obsl", "pracovnice", bend=-25)
net.place("konec", (9, 0))
net.immediate("odchod", (10.5, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# fronta dosáhne 10 čekajících: stop stav = generátor přijde o značku na 4 h
net.immediate("stop", (1.5, -2), p=1, param_pos="left")
net.arc("gen", "stop")
net.arc("fronta", "stop", w=10, bend=-20, w_pos="left")
net.arc("stop", "fronta", w=10, bend=-20, w_pos="below right")
net.place("stop_stav", (1.5, -3.6), label="stop stav", label_pos="right")
net.arc("stop", "stop_stav")
net.timed("trvani", (0, -3.6), "4 h", param_pos="left")
net.arc("stop_stav", "trvani")
net.arc("trvani", "gen")

net.invariant({"pracovnice": 1, "obsluha": 1}, 1)
net.invariant({"gen": 1, "stop_stav": 1}, 1, name="příchody běží, nebo je stop stav")
net.bound("fronta", 10)
net.sim_events = 300000
