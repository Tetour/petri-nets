from pn import Net

net = Net("12–10", "Zahradník na FIT (půlsemestrálky 2014–19, Z8)")

# začátek dne: zahradník u zdroje s plnou konví jde k první květině
net.place("start", (0, 0), tokens=1, label="u zdroje (ráno)", label_pos="above")
net.place("kvetiny", (1.5, 1.8), tokens=30, label="Květiny", label_pos="left")
net.timed("k_prvni", (1.5, 0), "2–5 min", param_pos="below")
net.place("u_kv", (3, 0), label="u květiny", label_pos="above")
net.chain("start", "k_prvni", "u_kv")
net.arc("kvetiny", "k_prvni")

# květina potřebuje 3 (20 %) nebo 4 (80 %) jednotky; potřeba zůstává u květiny
net.immediate("s3", (4.5, 1.8), prob=20, param_pos="above left")
net.immediate("s4", (4.5, -1.8), prob=80, param_pos="below left")
net.arc("u_kv", "s3")
net.arc("u_kv", "s4")
net.place("z", (6, 0), label="zahradník", label_pos="left")
net.place("n3", (7, 3.8), label="potřebuje 3", label_pos="above")
net.place("n4", (7, -3.8), label="potřebuje 4", label_pos="below")
net.arc("s3", "z")
net.arc("s4", "z")
net.arc("s3", "n3")
net.arc("s4", "n4")

# zalití, je-li v konvi dost vody (p=1)
net.place("konev", (14.6, 0), tokens=10, label="Konev", label_pos="below")
net.immediate("zal3", (10, 3.8), p=1, param_pos="above")
net.immediate("zal4", (10, -3.8), p=1, param_pos="below")
net.arc("n3", "zal3")
net.arc("n4", "zal4")
net.arc("z", "zal3")
net.arc("z", "zal4")
net.arc("konev", "zal3", w=3, w_pos="above right")
net.arc("konev", "zal4", w=4, w_pos="below right")
net.place("zaleva", (16.4, 0), label="zalévá", label_pos="above left")
net.arc("zal3", "zaleva", via=[(16.4, 3.8)])
net.arc("zal4", "zaleva", via=[(16.4, -3.8)])

# jinak (p=0) cesta ke zdroji, vylití zbytku, napuštění 10 jednotek za 60 s a návrat
net.immediate("dojdi", (7.8, 0.8), label="málo vody", label_pos="above")
net.place("ke_zdroji", (9, 0.8))
net.timed("tam", (10.2, 0.8), "2–5 min", param_pos="above")
net.place("u_zdroje", (11.6, 0), label="u zdroje", label_pos="above")
net.chain("z", "dojdi", "ke_zdroji", "tam", "u_zdroje")
net.immediate("vylij", (13, 0), p=1, horizontal=True, param_pos="above")
net.loop("u_zdroje", "vylij", bend=25)
net.arc("konev", "vylij")
net.timed("napust", (10.2, -0.8), "60 s", param_pos="below")
net.arc("u_zdroje", "napust")
net.arc("napust", "konev", w=10, via=[(13, -0.8)], w_pos="below")
net.place("zpet", (9, -0.8))
net.timed("zpet_t", (7.8, -0.8), "2–5 min", param_pos="above")
net.chain("napust", "zpet", "zpet_t", "z")

# po zalití (20 s): květina hotová, zahradník jde k další (p=1), nebo den končí
net.timed("zaliti", (17.7, 0), "20 s", param_pos="below")
net.arc("zaleva", "zaliti")
net.place("zalita", (17.7, 1.8), label="zalitá květina", label_pos="left")
net.immediate("odchod", (17.7, 3.4), exit=True, horizontal=True, label="odchod", label_pos="right")
net.chain("zaliti", "zalita", "odchod")
net.place("po", (19.2, 0), label="po zalití", label_pos="above")
net.arc("zaliti", "po")
net.immediate("k_dalsi", (20.7, 0), p=1, param_pos="above left")
net.arc("po", "k_dalsi")
net.arc("kvetiny", "k_dalsi", via=[(1.5, 5.4), (20.7, 5.4)])
net.place("cesta", (22.2, 0))
net.timed("prejezd", (23.7, 0), "exp(1 min)", param_pos="below")
net.chain("k_dalsi", "cesta", "prejezd")
net.arc("prejezd", "u_kv", via=[(23.7, -5.4), (3, -5.4)])
net.immediate("konec", (19.2, -1.8), horizontal=True, label="květiny došly", label_pos="right")
net.place("den", (19.2, -3.4), label="konec dne", label_pos="right")
net.chain("po", "konec", "den")

net.invariant({"start": 1, "u_kv": 1, "z": 1, "ke_zdroji": 1, "u_zdroje": 1, "zpet": 1,
               "zaleva": 1, "po": 1, "cesta": 1, "den": 1}, 1, name="zahradník je právě v jednom stavu")
net.bound("konev", 10)
# model jednoho dne: po zalití 30 květin síť skončí (značka v „konec dne“), proto se nehlásí deadlock
net.deadlock_ok = True
