from pn import Net

net = Net("07–01", "Ambulance M/M/1: akutní pacienti mají vyšší prioritu procesu (předbíhají ve frontě)")

net.place("gen", (0, 2), tokens=1, label="generátor", label_pos="above")
net.timed("prichod", (1.5, 2), "exp(15 min)")
net.loop("gen", "prichod")
net.place("novy", (3, 2), label="pacient", label_pos="above")
net.arc("prichod", "novy")

# 20 % akutních (nahoře), 80 % ostatních (dole)
net.immediate("akutni", (4.5, 4), prob=20, param_pos="above")
net.immediate("ostatni", (4.5, 0), prob=80, param_pos="below")
net.arc("novy", "akutni")
net.arc("novy", "ostatni")
net.place("fronta_a", (6, 4), label="Fronta akutních", label_pos="below")
net.place("fronta_o", (6, 0), label="Fronta ostatních", label_pos="above")
net.arc("akutni", "fronta_a")
net.arc("ostatni", "fronta_o")

# lékař: akutní pacient má přednost (p=1), probíhající vyšetření se nepřerušuje
net.place("lekar", (8.4, 2), tokens=1, label="Lékař", label_pos="above right")
net.immediate("obsaz_a", (7.5, 4), p=1, param_pos="above")
net.immediate("obsaz_o", (7.5, 0))
net.place("vys_a", (9.3, 4))
net.place("vys_o", (9.3, 0))
net.timed("konec_a", (10.8, 4), "exp(10 min)", param_pos="above")
net.timed("konec_o", (10.8, 0), "exp(10 min)")
net.chain("fronta_a", "obsaz_a", "vys_a", "konec_a")
net.chain("fronta_o", "obsaz_o", "vys_o", "konec_o")
net.arc("lekar", "obsaz_a")
net.arc("lekar", "obsaz_o")
net.arc("konec_a", "lekar", bend=40)
net.arc("konec_o", "lekar", bend=-40)

net.place("konec", (12.3, 2))
net.immediate("odchod", (13.8, 2), exit=True, label="odchod")
net.arc("konec_a", "konec")
net.arc("konec_o", "konec")
net.arc("konec", "odchod")

net.invariant({"lekar": 1, "vys_a": 1, "vys_o": 1}, 1)
