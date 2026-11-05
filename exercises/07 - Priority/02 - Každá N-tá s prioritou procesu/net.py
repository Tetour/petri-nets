from pn import Net

net = Net("Myčka aut M/M/1: každé N-té auto má vyšší prioritu procesu (předjede čekající)")
net.params = {"N": 5}

net.place("gen", (0, 0), tokens=1, label="příjezdy aut", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(10 min)", param_pos="below")
net.loop("gen", "prichod")
net.place("novy", (3, 0), label="auto", label_pos="right")
net.arc("prichod", "novy")

# čítač příjezdů: N-té auto (čítač dosáhl N) jde do prioritní fronty a čítač se vynuluje
net.place("citac", (1.5, 3.4), label="čítač", label_pos="left")
net.arc("prichod", "citac")
net.immediate("vyber_p", (4.5, 1.7), p=1, param_pos="below")
net.immediate("vyber_n", (4.5, -1.7))
net.arc("citac", "vyber_p", w="N", via=[(4.5, 3.4)], w_pos="above")

# horní řada N-tá auta, dolní ostatní; myčka je mezi řadami
for row, y, name in (("p", 1.7, "fronta P"), ("n", -1.7, "fronta N")):
    up = y > 0
    net.arc("novy", f"vyber_{row}", via=[(3, y)])
    net.place(f"fronta_{row}", (6, y), label=name, label_pos="below" if up else "above")
    net.place(f"myti_{row}", (9, y))
    net.timed(f"konec_{row}", (10.5, y), "exp(8 min)", param_pos="above" if up else "below")
    net.chain(f"vyber_{row}", f"fronta_{row}")
    net.chain(f"obsaz_{row}", f"myti_{row}", f"konec_{row}")

# myčka: auto z prioritní fronty má přednost (p=1), rozjeté mytí se nepřerušuje
net.place("mycka", (7.5, 0), tokens=1, label="myčka", label_pos="left")
net.immediate("obsaz_p", (7.5, 1.7), p=1, param_pos="above")
net.immediate("obsaz_n", (7.5, -1.7))
net.arc("fronta_p", "obsaz_p")
net.arc("fronta_n", "obsaz_n")
net.arc("mycka", "obsaz_p")
net.arc("mycka", "obsaz_n")
net.arc("konec_p", "mycka", out=270, into=25)
net.arc("konec_n", "mycka", out=90, into=-25)

net.place("konec", (12, 0), label="umyto", label_pos="left")
net.immediate("odchod", (13.5, 0), exit=True, label="odchod")
net.arc("konec_p", "konec", via=[(12, 1.7)])
net.arc("konec_n", "konec", via=[(12, -1.7)])
net.arc("konec", "odchod")

net.invariant({"mycka": 1, "myti_p": 1, "myti_n": 1}, 1)
net.bound("citac", net.params["N"])
