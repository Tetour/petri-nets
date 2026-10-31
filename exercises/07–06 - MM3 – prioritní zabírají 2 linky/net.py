from pn import Net

net = Net("07–06", "M/M/3, 20 % transakcí je prioritních a zabírá dvě linky současně")
net.params = {"X": 10, "Y": 15}

net.place("gen", (0, 0), tokens=1, label="příchody transakcí", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(X)", param_pos="below")
net.loop("gen", "prichod")
net.place("nova", (3, 0), label="transakce", label_pos="right")
net.arc("prichod", "nova")

# horní řada prioritní (20 %), dolní normální (80 %); sklad linek je mezi řadami
for row, y, prob, name in (("p", 1.7, 20, "fronta P"), ("n", -1.7, 80, "fronta N")):
    up = y > 0
    net.immediate(f"vyber_{row}", (4.5, y), prob=prob, param_pos="above" if up else "below")
    net.arc("nova", f"vyber_{row}", via=[(3, y)], corner=20)
    net.place(f"fronta_{row}", (6, y), label=name, label_pos="below" if up else "above")
    net.place(f"obsluha_{row}", (9, y))
    net.timed(f"obsl_{row}", (10.5, y), "exp(Y)", param_pos="above" if up else "below")
    net.chain(f"vyber_{row}", f"fronta_{row}")
    net.chain(f"obsaz_{row}", f"obsluha_{row}", f"obsl_{row}")

# tři linky jako sklad; prioritní zabírá a vrací dvě najednou a má přednost (p=1)
net.place("linky", (7.5, 0), tokens=3, label="linky", label_pos="left")
net.immediate("obsaz_p", (7.5, 1.7), p=1, param_pos="above")
net.immediate("obsaz_n", (7.5, -1.7))
net.arc("fronta_p", "obsaz_p")
net.arc("fronta_n", "obsaz_n")
net.arc("linky", "obsaz_p", w=2, w_pos="right")
net.arc("linky", "obsaz_n")
net.arc("obsl_p", "linky", w=2, out=270, into=25, w_pos="above")
net.arc("obsl_n", "linky", out=90, into=-25)

net.place("konec", (12, 0), label="obslouženo", label_pos="left")
net.immediate("odchod", (13.5, 0), exit=True, label="odchod")
net.arc("obsl_p", "konec", via=[(12, 1.7)], corner=20)
net.arc("obsl_n", "konec", via=[(12, -1.7)], corner=20)
net.arc("konec", "odchod")

net.invariant({"linky": 1, "obsluha_p": 2, "obsluha_n": 1}, 3)
