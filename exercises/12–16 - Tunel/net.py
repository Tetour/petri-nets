from pn import Net

net = Net("12–16", "Tunel (půlsemestrálka 2011/12, příklad 1)", unit="h")
net.params = {"N": 1000}

# metry tunelu: kdo začne metr vrtat, ten si ho zabere (soupravy se nesrazí)
net.place("zbyva", (1.5, -1.8), tokens="N", label="Zbývá metrů (N = 1000)", label_pos="left")

# souprava A: zabere metr, ve dne vrtá rychle, v noci pomalu (p=1)
net.place("a_volna", (0, 0), tokens=1, label="souprava A", label_pos="above left")
net.immediate("a_zabere", (1.5, 0))
net.arc("a_volna", "a_zabere")
net.arc("zbyva", "a_zabere")
net.place("a_metr", (3, 0), label="A má metr", label_pos="below")
net.arc("a_zabere", "a_metr")
net.immediate("a_rychle", (4.5, 2.2))
net.immediate("a_pomalu", (4.5, -2.0), p=1, param_pos="left")
net.arc("a_metr", "a_rychle")
net.arc("a_metr", "a_pomalu")
net.place("rychle", (6, 2.2), label="vrtá rychle", label_pos="above")
net.timed("t_rychle", (10.5, 2.2), "1–3 h", param_pos="above")
net.chain("a_rychle", "rychle", "t_rychle")
net.place("pomalu", (6, -2.0), label="vrtá pomalu", label_pos="below")
net.timed("t_pomalu", (10.5, -2.0), "3–5 h", param_pos="below")
net.chain("a_pomalu", "pomalu", "t_pomalu")

# přechod do noci přeruší rychlé vrtání: metr se začne znovu (v noci pomalu)
net.immediate("preruseni", (4.5, 0.9), label="přerušení", label_pos="above left")
net.arc("rychle", "preruseni")
net.arc("preruseni", "a_metr")

# den 16 h a noc 8 h; začínáme ráno
net.place("noc", (6, 0), label="Noc", label_pos="above")
net.place("den", (9, 0), tokens=1, label="Den", label_pos="right")
net.timed("t_noc", (7.5, 0.8), "8 h", param_pos="above")
net.timed("t_den", (7.5, -0.8), "16 h", param_pos="below")
net.chain("noc", "t_noc", "den", "t_den", "noc")
net.loop("noc", "preruseni", bend=15)
net.loop("noc", "a_pomalu", bend=15)

# dokončený metr soupravy A
net.place("a_hotovo", (12, 0))
net.arc("t_rychle", "a_hotovo")
net.arc("t_pomalu", "a_hotovo")
net.immediate("a_zapis", (13.5, 0))
net.place("a_metry", (15, 1.6), label="Vzdálenost od A (m)", label_pos="above")
net.place("vyvrtano", (15, -1.6), label="Vyvrtáno (m)", label_pos="below left")
net.chain("a_hotovo", "a_zapis", "a_metry")
net.arc("a_zapis", "vyvrtano")
net.arc("a_zapis", "a_volna", via=[(13.5, 3.6), (0, 3.6)])

# souprava B vrtá vždy 1–3 h na metr
net.place("b_volna", (1.5, -4.2), tokens=1, label="souprava B", label_pos="left")
net.immediate("b_zabere", (3, -4.2))
net.place("b_vrta", (4.5, -4.2), label="B vrtá", label_pos="below")
net.timed("t_b", (6, -4.2), "1–3 h", param_pos="above")
net.chain("b_volna", "b_zabere", "b_vrta", "t_b")
net.arc("zbyva", "b_zabere")
net.arc("t_b", "b_volna", via=[(6, -5.4), (1.5, -5.4)])
net.arc("t_b", "vyvrtano", via=[(15, -4.2)])

# setkání souprav: všech 1000 metrů je vyvrtáno
net.immediate("setkani", (16.8, -1.6), exit=True, label="setkání, konec prací", label_pos="above")
net.arc("vyvrtano", "setkani", w=1000, w_pos="below")

net.invariant({"den": 1, "noc": 1}, 1)
net.invariant({"a_volna": 1, "a_metr": 1, "rychle": 1, "pomalu": 1, "a_hotovo": 1}, 1)
net.invariant({"b_volna": 1, "b_vrta": 1}, 1)
net.bound("zbyva", 1000)
net.bound("vyvrtano", 1000)
net.bound("a_metry", 1000)
