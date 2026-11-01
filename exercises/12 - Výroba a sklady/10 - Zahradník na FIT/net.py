from pn import Net

net = Net("Zahradník na FIT (půlsemestrálky 2014–19, Z8)")

# Rozvržení: hlavní řada vede zleva doprava. Obě zalití (nahoře a dole) se sbíhají do „zalévá“,
# cesta pro vodu vede mezi nimi a její návrat k místu před „zahradníkem“ jednou kříží
# hranu k dolnímu zalití. Bez křížení to nejde (graf sítě není rovinný).

# začátek dne: zahradník u zdroje s plnou konví jde k první květině
net.place("start", (0, 0), tokens=1, label="u zdroje (ráno)", label_pos="above")
net.place("kvetiny", (1.5, 1.6), tokens=30, label="Květiny", label_pos="left")
net.timed("k_prvni", (1.5, 0), "2–5 min", param_pos="below")
net.place("u_kv", (3.6, 0), label="u květiny", label_pos="above left")
net.chain("start", "k_prvni", "u_kv")
net.arc("kvetiny", "k_prvni")

# květina potřebuje 3 (20 %, nahoru) nebo 4 (80 %, rovně); potřeba zůstává u květiny
net.immediate("s3", (5.1, 1.8), prob=20, param_pos="above left")
net.immediate("s4", (5.1, 0), prob=80, param_pos="above")
net.arc("u_kv", "s3", via=[(3.6, 1.8)], corner=20)
net.arc("u_kv", "s4")
net.place("n3", (5.1, 3.4), label="potřebuje 3", label_pos="right")
net.place("n4", (5.1, -2.4), label="potřebuje 4", label_pos="right")
net.arc("s3", "n3")
net.arc("s4", "n4")

# zahradník u květiny (z obou větví i po návratu od zdroje)
net.place("w", (6.6, 0))
net.arc("s3", "w", via=[(6.6, 1.8)], corner=20)
net.arc("s4", "w")
net.immediate("t_w", (8.1, 0))
net.place("z", (9.6, 0), label="zahradník", label_pos="above right")
net.chain("w", "t_w", "z")

# zalití, je-li v konvi dost vody (p=1)
net.immediate("zal3", (11.7, 3.4), p=1, param_pos="above left")
net.immediate("zal4", (11.7, -3.6), p=1, param_pos="below left")
net.arc("n3", "zal3", via=[(5.1, 4.6), (11.7, 4.6)])
net.arc("n4", "zal4", via=[(5.1, -4.8), (11.7, -4.8)])
net.arc("z", "zal3", via=[(9.6, 3.4)], corner=20)
net.arc("z", "zal4", via=[(9.6, -3.6)], corner=20)
net.place("zaleva", (22.1, 0), label="zalévá", label_pos="left")
net.arc("zal3", "zaleva", via=[(22.1, 3.4)], corner=20)
net.arc("zal4", "zaleva", via=[(22.1, -3.6)], corner=20)

# jinak (p=0) cesta ke zdroji, vylití zbytku, napuštění 10 jednotek za 60 s a návrat
net.immediate("dojdi", (11.7, 0), label="málo vody", label_pos="below")
net.place("ke_zdroji", (13.2, 0))
net.timed("tam", (14.7, 0), "2–5 min", param_pos="above")
net.place("u_zdroje", (16.2, 0), label="u zdroje", label_pos="below")
net.chain("z", "dojdi", "ke_zdroji", "tam", "u_zdroje")
net.immediate("vylij", (16.2, 1.4), p=1, param_pos="left")
net.loop("u_zdroje", "vylij", bend=30)
net.place("konev", (19.4, 0), tokens=10, label="Konev", label_pos="below left")
net.arc("konev", "vylij", via=[(19.4, 1.4)])
net.timed("napust", (17.7, 0), "60 s", param_pos="above")
net.arc("u_zdroje", "napust")
net.arc("napust", "konev", w=10, w_pos="above")
net.arc("konev", "zal3", w=3, w_pos="above", via=[(20.5, 0), (20.5, 2.5), (11.7, 2.5)])
net.arc("konev", "zal4", w=4, w_pos="right", via=[(19.4, -2.7), (11.7, -2.7)])
net.place("zpet", (17.7, -1.4))
net.arc("napust", "zpet")
net.timed("zpet_t", (14.7, -1.4), "2–5 min", param_pos="below")
net.chain("zpet", "zpet_t")
net.arc("zpet_t", "w", via=[(6.6, -1.4)])

# po zalití (20 s): květina hotová, zahradník jde k další (p=1), nebo den končí
net.timed("zaliti", (23.6, 0), "20 s", param_pos="below")
net.arc("zaleva", "zaliti")
net.place("zalita", (23.6, 1.6), label="zalitá květina", label_pos="above")
net.immediate("odchod", (25.1, 1.6), exit=True, label="odchod", label_pos="right")
net.arc("zaliti", "zalita")
net.arc("zalita", "odchod")
net.place("po", (25.1, 0), label="po zalití", label_pos="above")
net.arc("zaliti", "po")
net.immediate("k_dalsi", (26.9, 0), p=1, param_pos="below")
net.arc("po", "k_dalsi")
net.arc("kvetiny", "k_dalsi", via=[(1.5, 5.6), (26.9, 5.6)])
net.place("cesta", (28.4, 0))
net.timed("prejezd", (29.9, 0), "exp(1 min)", param_pos="above")
net.chain("k_dalsi", "cesta", "prejezd")
net.arc("prejezd", "u_kv", via=[(29.9, -6.0), (3.6, -6.0)])
net.immediate("konec", (25.1, -1.6), label="květiny došly", label_pos="below")
net.place("den", (26.9, -1.6), label="konec dne", label_pos="right")
net.arc("po", "konec")
net.arc("konec", "den")

net.invariant({"start": 1, "u_kv": 1, "w": 1, "z": 1, "ke_zdroji": 1, "u_zdroje": 1, "zpet": 1,
               "zaleva": 1, "po": 1, "cesta": 1, "den": 1}, 1, name="zahradník je právě v jednom stavu")
net.bound("konev", 10)
net.bound("w", 1)
# model jednoho dne: po zalití 30 květin síť skončí (značka v „konec dne“), proto se nehlásí deadlock
net.deadlock_ok = True
