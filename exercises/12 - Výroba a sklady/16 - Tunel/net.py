from pn import Net

net = Net("Tunel (půlsemestrálka 2011/12, příklad 1)", unit="h")
net.params = {"N": 1000}

# metry tunelu: kdo začne metr vrtat, ten si ho zabere (soupravy se nesrazí)
net.place("zbyva", (1.5, -2.5), tokens="N", label="Zbývá metrů (N = 1000)", label_pos="left")

# souprava A: zabere metr, v noci vrtá pomalu (p=1, dolní řada), jinak rychle (horní řada)
net.place("a_volna", (0, 0), tokens=1, label="souprava A", label_pos="above left")
net.immediate("a_zabere", (1.5, 0))
net.place("a_metr", (3, 0), label="A má metr", label_pos="right")
net.chain("a_volna", "a_zabere", "a_metr")
net.arc("zbyva", "a_zabere")
net.immediate("a_rychle", (12, 3))
net.immediate("a_pomalu", (12, -3), p=1, param_pos="below")
net.arc("a_metr", "a_rychle", via=[(3, 3)], corner=20)
net.arc("a_metr", "a_pomalu", via=[(3, -3)], corner=20)
net.place("rychle", (13.5, 3), label="vrtá rychle", label_pos="above")
net.timed("t_rychle", (15, 3), "1–3 h", param_pos="above")
net.chain("a_rychle", "rychle", "t_rychle")
net.place("pomalu", (13.5, -3), label="vrtá pomalu", label_pos="below")
net.timed("t_pomalu", (15, -3), "3–5 h", param_pos="below")
net.chain("a_pomalu", "pomalu", "t_pomalu")

# soumrak přeruší rychlé vrtání: týž metr se začne znovu pomalu
# (rovnou do „vrtá pomalu“; z „A má metr“ by v noci stejně vyhrálo pomalé vrtání)
net.immediate("preruseni", (13.5, -0.9), label="přerušení", label_pos="right")
net.chain("rychle", "preruseni", "pomalu")

# den 16 h a noc 8 h; začínáme ráno.
# Odpočet noci běží na vlastním místě „noc trvá“. Vrtání testuje jen stavové místo „Noc“:
# testovací hrana značku na okamžik vezme a vrátí, a kdyby testovala místo, ze kterého bere
# časovaný přechod 8 h, každý nový metr by noc prodloužil (slajdy 137–139).
net.place("den", (7.5, 0.5), tokens=1, label="Den", label_pos="right")
net.timed("t_den", (6, 0.5), "16 h", param_pos="left")
net.place("noc_trva", (6, -0.9), label="noc trvá", label_pos="below")
net.timed("t_noc", (7.5, -0.9), "8 h", param_pos="below")
net.place("rano", (9, -0.9), label="ráno", label_pos="below")
net.immediate("konec_noci", (10.5, -0.9), p=2, param_pos="below")
net.place("noc", (12, -0.9), label="Noc", label_pos="above left")
net.arc("den", "t_den")
net.arc("t_den", "noc_trva")
net.arc("t_den", "noc", via=[(6, 1.3), (12, 1.3)])
net.chain("noc_trva", "t_noc", "rano", "konec_noci")
net.arc("t_noc", "den")
net.arc("noc", "konec_noci")
net.loop("noc", "preruseni", bend=30)
net.loop("noc", "a_pomalu", bend=30)

# dokončený metr soupravy A
net.place("a_hotovo", (16.5, 0))
net.arc("t_rychle", "a_hotovo", via=[(16.5, 3)], corner=20)
net.arc("t_pomalu", "a_hotovo", via=[(16.5, -3)], corner=20)
net.immediate("a_zapis", (18, 0))
net.place("a_metry", (19.5, 0), label="Vzdálenost od A (m)", label_pos="right")
net.place("vyvrtano", (19.5, -2.5), label="Vyvrtáno (m)", label_pos="above")
net.chain("a_hotovo", "a_zapis", "a_metry")
net.arc("a_zapis", "vyvrtano", via=[(18, -2.5)])
net.arc("a_zapis", "a_volna", via=[(18, 4.4), (0, 4.4)])

# souprava B vrtá vždy 1–3 h na metr
net.place("b_volna", (0, -5), tokens=1, label="souprava B", label_pos="above left")
net.immediate("b_zabere", (1.5, -5))
net.place("b_vrta", (3, -5), label="B vrtá", label_pos="below")
net.timed("t_b", (4.5, -5), "1–3 h", param_pos="above")
net.chain("b_volna", "b_zabere", "b_vrta", "t_b")
net.arc("zbyva", "b_zabere")
net.arc("t_b", "b_volna", via=[(4.5, -6.2), (0, -6.2)])
net.arc("t_b", "vyvrtano", via=[(19.5, -5)])

# setkání souprav: všech 1000 metrů je vyvrtáno
net.immediate("setkani", (21.6, -2.5), exit=True, label="setkání, konec prací", label_pos="right")
net.arc("vyvrtano", "setkani", w=1000, w_pos="below")

net.invariant({"den": 1, "noc_trva": 1}, 1)
net.invariant({"noc": 1, "rano": 1, "den": 1}, 1, name="Noc + ráno + Den = 1")
net.invariant({"a_volna": 1, "a_metr": 1, "rychle": 1, "pomalu": 1, "a_hotovo": 1}, 1)
net.invariant({"b_volna": 1, "b_vrta": 1}, 1)
net.bound("zbyva", 1000)
net.bound("vyvrtano", 1000)
net.bound("a_metry", 1000)
