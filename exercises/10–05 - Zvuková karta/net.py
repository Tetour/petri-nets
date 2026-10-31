from pn import Net

net = Net("10–05", "Zvuková karta (půlsemestrálka, rok neznámý)", unit="ms")

# vyrovnávací paměť: 100 míst po bloku 100 vzorků (10 000 vzorků)
net.place("volne", (2, 2.2), tokens=100, label="Volné bloky", label_pos="above left")
net.timed("plneni", (4.5, 2.2), "0,2 ms", label="zápis", label_pos="above",
          param_pos="below right")
net.place("plne", (7, 2.2), label="Plné bloky", label_pos="above")
net.chain("volne", "plneni", "plne")

# karta přehraje blok 100 vzorků za 1 ms; přehraný blok opouští systém
net.place("karta", (8.5, 0.6), tokens=1, label="Karta", label_pos="right")
net.timed("prehrani", (8.5, 2.2), "1 ms", label="přehrání", label_pos="above right",
          param_pos="below right")
net.arc("plne", "prehrani")
net.loop("karta", "prehrani", bend=20)
net.arc("prehrani", "volne", via=[(8.5, 3.6), (2, 3.6)])
net.place("prehrano", (10, 2.2), label="přehraný blok", label_pos="below")
net.arc("prehrani", "prehrano")
net.immediate("odchod", (11.5, 2.2), exit=True, label="odchod", label_pos="above")
net.arc("prehrano", "odchod")

# zvukový proces: při ≥ 50 volných blocích dostane procesor přednostně (p=1),
# plní po blocích, dokud není paměť plná, pak procesor vrátí
net.place("zp", (4.5, -1.2), tokens=1, label="Zvuk. proces", label_pos="below")
net.immediate("prideleni_z", (2, 0), p=1, param_pos="left")
net.place("plni", (4.5, 0), label="plní", label_pos="below right")
net.immediate("plna", (7, 0), label="paměť plná", label_pos="below right")
net.arc("zp", "prideleni_z")
net.loop("volne", "prideleni_z", w=50, bend=20)
net.arc("prideleni_z", "plni")
net.loop("plni", "plneni", bend=25)
net.arc("plni", "plna")
net.loop("plne", "plna", w=100, bend=20)
net.arc("plna", "zp")

# procesor
net.place("cpu", (4.5, -3.0), tokens=1, label="Procesor", label_pos="left")
net.arc("cpu", "prideleni_z")
net.arc("plna", "cpu")

# ostatní procesy: round-robin s kvantem 10 ms, 20 % se vzdá dřív
net.place("pripravene", (1.5, -5.0), tokens=9, label="Připravené procesy", label_pos="below")
net.immediate("prideleni_o", (3, -5.0))
net.place("bezi", (4.5, -5.0), label="běží", label_pos="below")
net.chain("pripravene", "prideleni_o", "bezi")
net.arc("cpu", "prideleni_o")
net.immediate("vzda", (6, -4.1), prob=20, label="vzdá se", label_pos="above",
              param_pos="below")
net.immediate("cele", (6, -5.9), prob=80, label="celé kvantum", label_pos="below",
              param_pos="above")
net.arc("bezi", "vzda")
net.arc("bezi", "cele")
net.place("vzdava", (7.5, -4.1))
net.timed("vzdani", (9, -4.1), "0–10 ms", param_pos="below")
net.place("kvantum", (7.5, -5.9))
net.timed("kvantum_t", (9, -5.9), "10 ms", param_pos="above")
net.chain("vzda", "vzdava", "vzdani")
net.chain("cele", "kvantum", "kvantum_t")
net.place("konec_kv", (10.5, -5.0))
net.arc("vzdani", "konec_kv")
net.arc("kvantum_t", "konec_kv")
net.immediate("uvolneni", (12, -5.0), label="uvolní procesor", label_pos="right")
net.arc("konec_kv", "uvolneni")
net.arc("uvolneni", "cpu", via=[(12, -3.0)])
net.arc("uvolneni", "pripravene", via=[(12, -7.1), (1.5, -7.1)])

net.invariant({"cpu": 1, "plni": 1, "bezi": 1, "vzdava": 1, "kvantum": 1, "konec_kv": 1}, 1)
net.invariant({"zp": 1, "plni": 1}, 1)
net.invariant({"volne": 1, "plne": 1}, 100)
net.invariant({"pripravene": 1, "bezi": 1, "vzdava": 1, "kvantum": 1, "konec_kv": 1}, 9)
net.invariant({"karta": 1}, 1)
