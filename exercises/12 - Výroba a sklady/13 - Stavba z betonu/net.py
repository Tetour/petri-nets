from pn import Net

net = Net("Stavba z betonu (půlsemestrálka 2013/14, varianta D)")

# zdroje: 10 licích forem, 100 stavebních částí, dvě party
net.place("formy", (1.5, 0), tokens=10, label="Volné formy", label_pos="below left")
net.place("zbyva", (3, 0), tokens=100, label="Zbývá částí", label_pos="right")
net.place("bednari", (13.5, 4.6), tokens=1, label="Bednáři", label_pos="below right")
net.place("betonari", (12, -4.4), tokens=1, label="Betonáři", label_pos="below left")

# 1) příprava formy: bednáři (p=1, horní řada), jinak betonáři bez betonu (p=0, dolní řada)
for m, y, p in (("b", 2.4, 1), ("c", -2.4, None)):
    up = y > 0
    net.immediate(f"prip_{m}", (3, y), p=p, param_pos="above left")
    net.place(f"pripravuji_{m}", (4.5, y))
    net.timed(f"prip_{m}_t", (6, y), "3–5 h", param_pos="below" if up else "above")
    net.chain(f"prip_{m}", f"pripravuji_{m}", f"prip_{m}_t")
    net.arc("formy", f"prip_{m}", via=[(1.5, y)], corner=20)
    net.arc("zbyva", f"prip_{m}")

# 2) objednávka betonu, dodávka za 2 h
net.place("ceka", (7.5, 0), label="Čeká na beton", label_pos="below right")
net.arc("prip_b_t", "ceka", via=[(7.5, 2.4)], corner=20)
net.arc("prip_c_t", "ceka", via=[(7.5, -2.4)], corner=20)
net.timed("dodavka", (9, 0), "2 h", param_pos="above")
net.place("beton", (10.5, 0), label="Beton dorazil", label_pos="above")
net.chain("ceka", "dodavka", "beton")

# 3) lití (betonáři, p=2) a zrání 10 dní
net.immediate("liti", (12, 0), p=2, param_pos="above")
net.place("leji", (13.5, 0))
net.timed("liti_t", (15, 0), "30–60 min", param_pos="above")
net.place("zraje", (16.5, 0), label="Zraje", label_pos="above")
net.timed("zrani", (18, 0), "10 d", param_pos="above")
net.place("vyzrale", (19.5, 0), label="Vyzrálé", label_pos="right")
net.chain("beton", "liti", "leji", "liti_t", "zraje", "zrani", "vyzrale")

# 4) odstranění formy: bednáři přednostně (p=2 > příprava p=1), betonáři p=1
for m, y, p in (("b", 2.4, 2), ("c", -2.4, 1)):
    up = y > 0
    net.immediate(f"odstr_{m}", (21, y), p=p, param_pos="below" if up else "above")
    net.place(f"odstranuji_{m}", (22.5, y))
    net.timed(f"odstr_{m}_t", (24, y), "2–3 h", param_pos="below" if up else "above")
    net.arc("vyzrale", f"odstr_{m}", via=[(19.5, y)], corner=20)
    net.chain(f"odstr_{m}", f"odstranuji_{m}", f"odstr_{m}_t")

# odstraněná forma se vrací, část je hotová
net.place("odstraneno", (25.5, 0))
net.arc("odstr_b_t", "odstraneno", via=[(25.5, 2.4)], corner=20)
net.arc("odstr_c_t", "odstraneno", via=[(25.5, -2.4)], corner=20)
net.immediate("uvolneni", (27.3, 0))
net.arc("odstraneno", "uvolneni")
net.arc("uvolneni", "formy", via=[(27.3, 6.8), (0, 6.8), (0, 0)])
net.place("hotove", (28.8, 0), label="Hotové části", label_pos="below")
net.arc("uvolneni", "hotove")
net.immediate("konec", (30.6, 0), exit=True, label="stavba dokončena", label_pos="right")
net.arc("hotove", "konec", w=100, w_pos="above")

# bednáři (nad horní řadou)
net.arc("bednari", "prip_b", via=[(3, 4.6)])
net.arc("bednari", "odstr_b", via=[(21, 4.6)])
net.arc("prip_b_t", "bednari", via=[(6, 3.6), (13.5, 3.6)])
net.arc("odstr_b_t", "bednari", via=[(24, 5.8), (13.5, 5.8)])

# betonáři (pod dolní řadou); po každém úkonu se vracejí přes místo „betonáři hotovi“
net.arc("betonari", "liti")
net.arc("betonari", "prip_c", via=[(3, -4.4)])
net.arc("betonari", "odstr_c", via=[(21, -4.4)])
net.place("bet_hotovi", (12, -7.2), label="betonáři hotovi", label_pos="below left")
net.immediate("bet_zpet", (12, -5.8), p=3, param_pos="right")
net.chain("bet_hotovi", "bet_zpet", "betonari")
net.arc("prip_c_t", "bet_hotovi", via=[(6, -7.2)])
net.arc("liti_t", "bet_hotovi", via=[(15, -7.2)])
net.arc("odstr_c_t", "bet_hotovi", via=[(24, -8.4), (12, -8.4)])

net.invariant({"formy": 1, "pripravuji_b": 1, "pripravuji_c": 1, "ceka": 1, "beton": 1,
               "leji": 1, "zraje": 1, "vyzrale": 1, "odstranuji_b": 1, "odstranuji_c": 1,
               "odstraneno": 1}, 10)
net.invariant({"bednari": 1, "pripravuji_b": 1, "odstranuji_b": 1}, 1)
net.invariant({"betonari": 1, "pripravuji_c": 1, "leji": 1, "odstranuji_c": 1, "bet_hotovi": 1}, 1)
net.bound("odstraneno", 0)  # uvolnění formy proběhne hned
net.bound("bet_hotovi", 0)  # návrat betonářů proběhne hned
# konečný proces: po dokončení 100. části se síť zastaví (to je správný konec)
net.deadlock_ok = True
