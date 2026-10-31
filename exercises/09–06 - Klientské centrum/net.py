from pn import Net

net = Net("09–06", "Klientské centrum (půlsemestrálka 2023/24, varianta D)")

# hlavní řada: příchody a obsluha
net.place("gen", (0, 0), tokens=1, label="příchody klientů", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(20 min)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta", label_pos="above")
net.place("pracovnice", (4.5, 1.7), tokens=1, label="Pracovnice", label_pos="left")
net.immediate("obsaz", (4.5, 0))
net.place("obsluha", (6, 0))
net.timed("obsl", (7.5, 0), "exp(10 min)", param_pos="below")
net.chain("prichod", "fronta", "obsaz", "obsluha", "obsl")
net.arc("pracovnice", "obsaz")
net.arc("obsl", "pracovnice", out=90, into=0)
net.place("konec", (9, 0), label="konec", label_pos="above")
net.immediate("odchod", (10.5, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# fronta dosáhne 10 čekajících: stop stav = příchody přijdou o značku na 4 h
net.immediate("stop", (3, -2), p=1, param_pos="below")
net.arc("gen", "stop", via=[(0, -2)])
net.arc("fronta", "stop", w=10, bend=-25, w_pos="left")
net.arc("stop", "fronta", w=10, bend=-25, w_pos="right")
net.place("stop_stav", (4.5, -2), label="stop stav", label_pos="below")
net.arc("stop", "stop_stav")
net.timed("trvani", (6, -2), "4 h", param_pos="right")
net.arc("stop_stav", "trvani")
net.arc("trvani", "gen", via=[(6, -3.3), (-0.9, -3.3), (-0.9, 0)])

net.invariant({"pracovnice": 1, "obsluha": 1}, 1)
net.invariant({"gen": 1, "stop_stav": 1}, 1, name="příchody běží, nebo je stop stav")
net.bound("fronta", 10)
net.sim_events = 300000
