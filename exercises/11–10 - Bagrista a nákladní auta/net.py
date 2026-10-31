from pn import Net

net = Net("11–10", "Bagrista a nákladní auta (půlsemestrálky 2014–19, Z4)")

# přistavení auta: bagrista + prázdné auto -> auto u bagru se 3 volnými místy
net.place("auta", (2.7, 1.8), tokens=3, label="Auta", label_pos="above")
net.immediate("pristaveni", (4.5, 1.8), p=1, horizontal=True, label="přistavení",
              label_pos="below left", param_pos="below right")
net.arc("auta", "pristaveni")
net.place("u_bagru", (4.5, 0), label="auto u bagru", label_pos="left")
net.arc("pristaveni", "u_bagru")
net.place("kapacita", (6, 1.8), label="volné místo", label_pos="above")
net.arc("pristaveni", "kapacita", w=3, w_pos="above")

# bagrování po metrech (dokud je místo na autě a zbývá úsek)
net.place("usek", (7.8, 1.8), tokens=1000, label="Úsek [m]", label_pos="above")
net.immediate("bagrovani", (6, 0), p=1, param_pos="below left")
net.arc("u_bagru", "bagrovani")
net.arc("kapacita", "bagrovani")
net.arc("usek", "bagrovani")
net.place("bagruje", (7.5, 0))
net.timed("metr", (9, 0), "exp(5 min)", param_pos="above")
net.chain("bagrovani", "bagruje", "metr")
net.arc("metr", "u_bagru", via=[(9, -1.0), (5.2, -1.0)])
net.place("odstraneno", (10.5, 0), label="odstraněno [m]", label_pos="below")
net.arc("metr", "odstraneno")

# auto je plné (nebo úsek došel): odjíždí, vrací se za exp(1 h)
net.immediate("odjezd", (4.5, -1.8), horizontal=True, label="odjezd", label_pos="right")
net.arc("u_bagru", "odjezd")
net.place("jizda", (3, -1.8), label="jízda", label_pos="below")
net.timed("navrat", (1.5, 0), "exp(1 h)", param_pos="left")
net.chain("odjezd", "jizda", "navrat", "auta")

# bagrista: bez auta jde na 10 min do stánku; po 1000 m končí
net.place("bagrista", (12, 1.8), tokens=1, label="Bagrista", label_pos="right")
net.arc("odjezd", "bagrista", via=[(4.5, -3.0), (12, -3.0)])
net.arc("bagrista", "pristaveni", via=[(12, 3.2), (4.5, 3.2)])
net.immediate("prestavka", (14.4, 2.8), label="nemá auto", label_pos="above")
net.place("stanek", (15.9, 1.8), label="stánek", label_pos="right")
net.timed("svacina", (14.4, 0.8), "10 min", param_pos="below")
net.chain("bagrista", "prestavka", "stanek", "svacina", "bagrista")
net.immediate("konec", (10.5, 1.8), p=2, exit=True, horizontal=True, label="úsek hotov",
              label_pos="left", param_pos="above")
net.arc("odstraneno", "konec", w=1000, w_pos="right")
net.arc("bagrista", "konec")

net.bound("usek", 1000)
net.bound("odstraneno", 1000)  # po 1000 m je odebere přechod „úsek hotov“
net.invariant({"auta": 1, "u_bagru": 1, "bagruje": 1, "jizda": 1}, 3, name="3 auta")
net.bound("kapacita", 3)
net.bound("u_bagru", 1)
# Práce je konečná: po odstranění 1000 m bagrista odchází a síť se zastaví
# (zastavení je správný konec modelu, ne uváznutí).
net.deadlock_ok = True
