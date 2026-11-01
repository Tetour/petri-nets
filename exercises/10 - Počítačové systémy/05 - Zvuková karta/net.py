from pn import Net

net = Net("Zvuková karta (půlsemestrálka, rok neznámý)", unit="ms")

# vyrovnávací paměť: 100 míst po bloku 100 vzorků (10 000 vzorků)
net.place("volne", (0, 0), tokens=100, label="volné bloky", label_pos="left")
net.timed("plneni", (2.5, 0), "0,2 ms", param_pos="above")
net.place("plne", (5, 0), label="plné bloky", label_pos="above")
net.chain("volne", "plneni", "plne")

# karta přehraje blok 100 vzorků za 1 ms; přehraný blok opouští systém
net.timed("prehrani", (7.5, 0), "1 ms", label="přehrání", label_pos="above right",
          param_pos="above left")
net.place("karta", (7.5, -2), tokens=1, label="karta", label_pos="right")
net.arc("plne", "prehrani")
net.loop("karta", "prehrani", bend=20)
net.arc("prehrani", "volne", via=[(7.5, 1.6), (0, 1.6)])
net.place("prehrano", (9, 0), label="přehraný blok", label_pos="below")
net.arc("prehrani", "prehrano")
net.immediate("odchod", (10.5, 0), exit=True, label="odchod", label_pos="above")
net.arc("prehrano", "odchod")

# zvukový proces: při ≥ 50 volných blocích dostane procesor přednostně (p=1),
# plní po blocích, dokud není paměť plná, pak procesor vrátí
net.immediate("prideleni_z", (0, -2), p=1, param_pos="below right")
net.place("plni", (2.5, -2), label="plní", label_pos="below")
net.immediate("plna", (5, -2), label="paměť plná", label_pos="below right")
net.loop("volne", "prideleni_z", w=50, bend=20)
net.arc("prideleni_z", "plni")
net.loop("plni", "plneni", bend=20)
net.arc("plni", "plna")
net.loop("plne", "plna", w=100, bend=20)
net.place("zp", (5, -3.6), tokens=1, label="zvukový proces", label_pos="below")
net.arc("plna", "zp")
net.arc("zp", "prideleni_z", via=[(0, -3.6)])

# procesor
net.place("cpu", (2.5, -5.6), tokens=1, label="procesor", label_pos="below left")
net.arc("cpu", "prideleni_z", via=[(-1.2, -5.6), (-1.2, -2)])
net.arc("plna", "cpu", via=[(6.95, -2), (6.95, -4.8), (2.5, -4.8)])

# ostatní procesy: round-robin s kvantem 10 ms, 20 % se vzdá dřív
net.place("pripravene", (0, -8.4), tokens=9, label="připravené procesy", label_pos="above")
net.immediate("prideleni_o", (2.5, -8.4))
net.place("bezi", (4, -8.4), label="běží", label_pos="right")
net.chain("pripravene", "prideleni_o", "bezi")
net.arc("cpu", "prideleni_o")
for name, y, prob, label, time in (("vzda", -7, 20, "vzdá se", "0–10 ms"),
                                   ("cele", -9.8, 80, "celé kvantum", "10 ms")):
    up = y > -8.4
    net.immediate(name, (5.5, y), prob=prob, label=label, label_pos="above" if up else "below",
                  param_pos="below" if up else "above")
    net.arc("bezi", name, via=[(4, y)], corner=20)
    net.place(f"{name}_p", (7, y))
    net.timed(f"{name}_t", (8.5, y), time, param_pos="above" if up else "below")
    net.chain(name, f"{name}_p", f"{name}_t")
    net.arc(f"{name}_t", "konec_kv", via=[(10, y)], corner=20)
net.place("konec_kv", (10, -8.4))
net.immediate("uvolneni", (11.5, -8.4), label="uvolní procesor", label_pos="right")
net.arc("konec_kv", "uvolneni")
net.arc("uvolneni", "cpu", via=[(11.5, -5.6)])
net.arc("uvolneni", "pripravene", via=[(11.5, -11), (0, -11)])

net.invariant({"cpu": 1, "plni": 1, "bezi": 1, "vzda_p": 1, "cele_p": 1, "konec_kv": 1}, 1)
net.invariant({"zp": 1, "plni": 1}, 1)
net.invariant({"volne": 1, "plne": 1}, 100)
net.invariant({"pripravene": 1, "bezi": 1, "vzda_p": 1, "cele_p": 1, "konec_kv": 1}, 9)
net.invariant({"karta": 1}, 1)
