from pn import Net

net = Net("03–06", "M/M/1, porucha zničí probíhající obsluhu, jinak počká na další a zničí ji")
net.params = {"A": 10, "B": 6}

# M/M/1 (rozmístění jako v 03–02), časy v minutách
net.place("gen", (0, 0), tokens=1, label="příchody transakcí", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(A)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta")
net.immediate("obsaz", (4.5, 0))
net.place("obsluha", (6, 0), label="obsluha")
net.timed("obsl", (7.5, 0), "exp(B)")
net.chain("prichod", "fronta", "obsaz", "obsluha", "obsl")
net.place("linka", (7.5, 1.6), tokens=1, label="Linka")
net.arc("linka", "obsaz", via=[(4.5, 1.6)])
net.arc("obsl", "linka")
net.place("konec", (9, 0), label="hotovo")
net.immediate("odchod", (10.5, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# poruchy: bez přechodu „porucha bez účinku“ – porucha čeká na další obsluhu
net.place("gen_p", (3, -3.2), tokens=1, label="vznik poruch", label_pos="left")
net.timed("vznik", (4.5, -3.2), "exp(8 h)")
net.loop("gen_p", "vznik")
net.place("porucha", (6, -3.2), label="porucha", label_pos="below")
net.arc("vznik", "porucha")
net.immediate("zniceni", (6, -1.6))
net.arc("obsluha", "zniceni")
net.arc("porucha", "zniceni")
# zničená transakce odchází (vlevo), linka zpět (vpravo kolem odchodu)
net.place("znicena", (4.5, -1.6), label="zničená", label_pos="below")
net.immediate("odchod_z", (3, -1.6), exit=True, label="odchod bez obsluhy", label_pos="left")
net.chain("zniceni", "znicena", "odchod_z")
net.arc("zniceni", "linka", via=[(11.5, -1.6), (11.5, 1.6)])

net.invariant({"linka": 1, "obsluha": 1}, 1)
