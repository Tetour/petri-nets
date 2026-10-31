from pn import Net

net = Net("03–06", "M/M/1, porucha zničí probíhající obsluhu, jinak počká na další a zničí ji")
net.params = {"A": 10, "B": 6}

# M/M/1 (rozmístění jako v 03–02), časy v minutách
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(A)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta")
net.place("linka", (5.4, 1.7), tokens=1, label="Linka")
net.immediate("obsaz", (4.5, 0))
net.place("obsluha", (6.3, 0))
net.timed("obsl", (7.8, 0), "exp(B)")
net.chain("prichod", "fronta", "obsaz", "obsluha", "obsl")
net.arc("linka", "obsaz")
net.arc("obsl", "linka", bend=-25)
net.place("konec", (9.3, 0))
net.immediate("odchod", (10.8, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# poruchy: bez přechodu „porucha bez účinku“ – porucha čeká na další obsluhu
net.place("gen_p", (10.8, -1.8), tokens=1, label="generátor poruch", label_pos="above")
net.timed("vznik", (9.3, -1.8), "exp(8 h)", param_pos="below")
net.loop("gen_p", "vznik")
net.place("porucha", (7.8, -1.8), label="porucha", label_pos="below")
net.arc("vznik", "porucha")
net.immediate("zniceni", (5.4, -1.8), horizontal=True)
net.arc("obsluha", "zniceni")
net.arc("porucha", "zniceni")
net.arc("zniceni", "linka")
net.place("znicena", (3.6, -1.8), label="zničená", label_pos="above")
net.arc("zniceni", "znicena")
net.immediate("odchod_z", (2.1, -1.8), exit=True, label="odchod bez obsluhy", label_pos="below")
net.arc("znicena", "odchod_z")

net.invariant({"linka": 1, "obsluha": 1}, 1)
