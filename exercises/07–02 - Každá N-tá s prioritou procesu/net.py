from pn import Net

net = Net("07–02", "Myčka aut M/M/1: každé N-té auto má vyšší prioritu procesu (předjede čekající)")
net.params = {"N": 5}

net.place("gen", (0, 2), tokens=1, label="generátor", label_pos="above")
net.timed("prichod", (1.5, 2), "exp(10 min)")
net.loop("gen", "prichod")
net.place("novy", (3, 2), label="auto", label_pos="above")
net.arc("prichod", "novy")

# čítač příchodů: N-té auto (čítač dosáhl N) jde do prioritní fronty a čítač se vynuluje
net.place("citac", (3, 4), label="čítač", label_pos="above")
net.arc("prichod", "citac")
net.immediate("nta", (4.5, 4), p=1, param_pos="above")
net.immediate("ostatni", (4.5, 0))
net.arc("citac", "nta", w="N", w_pos="above")
net.arc("novy", "nta")
net.arc("novy", "ostatni")
net.place("fronta_p", (6, 4), label="Fronta P", label_pos="below")
net.place("fronta_n", (6, 0), label="Fronta N", label_pos="above")
net.arc("nta", "fronta_p")
net.arc("ostatni", "fronta_n")

# myčka: auto z prioritní fronty má přednost (p=1), rozjeté mytí se nepřerušuje
net.place("mycka", (8.4, 2), tokens=1, label="Myčka", label_pos="above right")
net.immediate("obsaz_p", (7.5, 4), p=1, param_pos="above")
net.immediate("obsaz_n", (7.5, 0))
net.place("myti_p", (9.3, 4))
net.place("myti_n", (9.3, 0))
net.timed("konec_p", (10.8, 4), "exp(8 min)", param_pos="above")
net.timed("konec_n", (10.8, 0), "exp(8 min)")
net.chain("fronta_p", "obsaz_p", "myti_p", "konec_p")
net.chain("fronta_n", "obsaz_n", "myti_n", "konec_n")
net.arc("mycka", "obsaz_p")
net.arc("mycka", "obsaz_n")
net.arc("konec_p", "mycka", bend=40)
net.arc("konec_n", "mycka", bend=-40)

net.place("konec", (12.3, 2))
net.immediate("odchod", (13.8, 2), exit=True, label="odchod")
net.arc("konec_p", "konec")
net.arc("konec_n", "konec")
net.arc("konec", "odchod")

net.invariant({"mycka": 1, "myti_p": 1, "myti_n": 1}, 1)
net.bound("citac", net.params["N"])
