from pn import Net

net = Net("12–13", "Stavba z betonu (půlsemestrálka 2013/14, varianta D)")

# zdroje: 10 licích forem, 100 stavebních částí, dvě party
net.place("formy", (1.5, 0), tokens=10, label="Volné formy", label_pos="left")
net.place("zbyva", (3, 0), tokens=100, label="Zbývá částí", label_pos="right")
net.place("bednari", (21, 4.0), tokens=1, label="Bednáři", label_pos="above left")
net.place("betonari", (12, -4.2), tokens=1, label="Betonáři", label_pos="below left")

# 1) příprava formy: bednáři (p=1), jinak betonáři bez betonu (p=0)
net.immediate("prip_b", (3, 2.2), p=1, param_pos="left")
net.place("pripravuji_b", (4.5, 2.2))
net.timed("prip_b_t", (6, 2.2), "3–5 h", param_pos="below left")
net.chain("prip_b", "pripravuji_b", "prip_b_t")
net.immediate("prip_c", (3, -2.2), param_pos="left")
net.place("pripravuji_c", (4.5, -2.2))
net.timed("prip_c_t", (6, -2.2), "3–5 h", param_pos="below")
net.chain("prip_c", "pripravuji_c", "prip_c_t")
for t in ("prip_b", "prip_c"):
    net.arc("formy", t)
    net.arc("zbyva", t)

# 2) objednávka betonu, dodávka za 2 h
net.place("ceka", (7.5, 0), label="Čeká na beton", label_pos="below right")
net.arc("prip_b_t", "ceka")
net.arc("prip_c_t", "ceka")
net.timed("dodavka", (9, 0), "2 h", param_pos="above")
net.place("beton", (10.5, 0), label="Beton dorazil", label_pos="above")
net.chain("ceka", "dodavka", "beton")

# 3) lití (betonáři mají přednost lití) a zrání 10 dní
net.immediate("liti", (12, -2.2), p=2, param_pos="left")
net.place("leji", (13.5, -2.2))
net.timed("liti_t", (15, -2.2), "30–60 min", param_pos="below right")
net.chain("beton", "liti", "leji", "liti_t")
net.place("zraje", (16.5, 0), label="Zraje", label_pos="above")
net.arc("liti_t", "zraje")
net.timed("zrani", (18, 0), "10 d", param_pos="below")
net.place("vyzrale", (19.5, 0), label="Vyzrálé", label_pos="above left")
net.chain("zraje", "zrani", "vyzrale")

# 4) odstranění formy: bednáři přednostně (p=2 > příprava p=1), betonáři p=1
net.immediate("odstr_b", (21, 2.2), p=2, param_pos="left")
net.place("odstranuji_b", (22.5, 2.2))
net.timed("odstr_b_t", (24, 2.2), "2–3 h", param_pos="right")
net.chain("vyzrale", "odstr_b", "odstranuji_b", "odstr_b_t")
net.immediate("odstr_c", (21, -2.2), p=1, param_pos="left")
net.place("odstranuji_c", (22.5, -2.2))
net.timed("odstr_c_t", (24, -2.2), "2–3 h", param_pos="right")
net.chain("vyzrale", "odstr_c", "odstranuji_c", "odstr_c_t")

# hotové části, forma se vrací
net.place("hotove", (25.5, 0), label="Hotové části", label_pos="below right")
net.immediate("konec", (27.6, 0), exit=True, label="stavba dokončena", label_pos="right")
net.arc("odstr_b_t", "hotove")
net.arc("odstr_c_t", "hotove")
net.arc("hotove", "konec", w=100, w_pos="above")
net.arc("odstr_b_t", "formy", via=[(24.6, 2.9), (24.6, 5.0), (1.5, 5.0)])
net.arc("odstr_c_t", "formy", via=[(24.6, -2.9), (24.6, -5.8), (1.5, -5.8)])

# bednáři
net.arc("bednari", "prip_b", via=[(3, 4.0)])
net.arc("prip_b_t", "bednari", via=[(6, 3.3), (20.4, 3.3)])
net.arc("bednari", "odstr_b")
net.arc("odstr_b_t", "bednari", bend=-25)

# betonáři
net.arc("betonari", "liti")
net.arc("liti_t", "betonari")
net.arc("betonari", "prip_c", via=[(3, -4.2)])
net.arc("prip_c_t", "betonari")
net.arc("betonari", "odstr_c", via=[(21, -4.2)])
net.arc("odstr_c_t", "betonari", via=[(23.4, -5.0), (12, -5.0)])

net.invariant({"formy": 1, "pripravuji_b": 1, "pripravuji_c": 1, "ceka": 1, "beton": 1,
               "leji": 1, "zraje": 1, "vyzrale": 1, "odstranuji_b": 1, "odstranuji_c": 1}, 10)
net.invariant({"bednari": 1, "pripravuji_b": 1, "odstranuji_b": 1}, 1)
net.invariant({"betonari": 1, "pripravuji_c": 1, "leji": 1, "odstranuji_c": 1}, 1)
# konečný proces: po dokončení 100. části se síť zastaví (to je správný konec)
net.deadlock_ok = True
