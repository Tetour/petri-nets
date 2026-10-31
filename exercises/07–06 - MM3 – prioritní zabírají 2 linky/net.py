from pn import Net

net = Net("07–06", "M/M/3, 20 % transakcí je prioritních a zabírá dvě linky současně")
net.params = {"X": 10, "Y": 15}

net.place("gen", (0, 2), tokens=1, label="generátor", label_pos="above")
net.timed("prichod", (1.5, 2), "exp(X)")
net.loop("gen", "prichod")
net.place("nova", (3, 2))
net.arc("prichod", "nova")

net.immediate("prior", (4.5, 4), prob=20, param_pos="above")
net.immediate("normal", (4.5, 0), prob=80, param_pos="below")
net.arc("nova", "prior")
net.arc("nova", "normal")
net.place("fronta_p", (6, 4), label="Fronta P", label_pos="below")
net.place("fronta_n", (6, 0), label="Fronta N", label_pos="above")
net.arc("prior", "fronta_p")
net.arc("normal", "fronta_n")

# tři linky jako sklad; prioritní zabírá a vrací dvě najednou
net.place("linky", (8.4, 2), tokens=3, label="Linky", label_pos="above right")
net.immediate("obsaz_p", (7.5, 4), p=1, param_pos="above")
net.immediate("obsaz_n", (7.5, 0))
net.place("obsluha_p", (9.3, 4))
net.place("obsluha_n", (9.3, 0))
net.timed("obsl_p", (10.8, 4), "exp(Y)", param_pos="above")
net.timed("obsl_n", (10.8, 0), "exp(Y)")
net.chain("fronta_p", "obsaz_p", "obsluha_p", "obsl_p")
net.chain("fronta_n", "obsaz_n", "obsluha_n", "obsl_n")
net.arc("linky", "obsaz_p", w=2, w_pos="left")
net.arc("linky", "obsaz_n")
net.arc("obsl_p", "linky", w=2, bend=40, w_pos="below")
net.arc("obsl_n", "linky", bend=-40)

net.place("konec", (12.3, 2))
net.immediate("odchod", (13.8, 2), exit=True, label="odchod")
net.arc("obsl_p", "konec")
net.arc("obsl_n", "konec")
net.arc("konec", "odchod")

net.invariant({"linky": 1, "obsluha_p": 2, "obsluha_n": 1}, 3)
