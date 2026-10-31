from pn import Net

net = Net("11–10", "Bagrista a nákladní auta (půlsemestrálky 2014–19, Z4)")

# auta obíhají ve čtverci: Auta -> přistavení -> auto u bagru -> odjezd -> jízda -> exp(1 h)
net.place("auta", (1.5, 3.2), tokens=3, label="Auta", label_pos="left")
net.immediate("pristaveni", (1.5, 1.7), p=1, label="přistavení", label_pos="below right",
              param_pos="above right")
net.arc("auta", "pristaveni")
net.place("u_bagru", (3.5, 1.7), label="auto u bagru", label_pos="above right")
net.arc("pristaveni", "u_bagru")
net.immediate("odjezd", (3.5, 3.2), label="odjezd", label_pos="left")
net.arc("u_bagru", "odjezd")
net.place("jizda", (3.5, 4.6), label="jízda", label_pos="right")
net.timed("navrat", (1.5, 4.6), "exp(1 h)", param_pos="above")
net.chain("odjezd", "jizda", "navrat", "auta")

# bagrování po metrech (dokud je místo na autě a zbývá úsek); řada metrů y=0
net.place("kapacita", (1.5, 0), label="volné místo", label_pos="below")
net.arc("pristaveni", "kapacita", w=3, w_pos="left")
net.place("usek", (3.5, -1.7), tokens=1000, label="Úsek [m]", label_pos="below")
net.immediate("bagrovani", (3.5, 0), p=1, param_pos="below right")
net.arc("kapacita", "bagrovani")
net.arc("usek", "bagrovani")
net.arc("u_bagru", "bagrovani")
net.place("bagruje", (5, 0))
net.timed("metr", (6.5, 0), "exp(5 min)", param_pos="below")
net.chain("bagrovani", "bagruje", "metr")
net.arc("metr", "u_bagru", out=90, into=0)
net.place("odstraneno", (8, 0), label="odstraněno [m]", label_pos="above")
net.arc("metr", "odstraneno")

# bagrista: přistavení ho bere, odjezd vrací; bez auta jde na 10 min do stánku; po 1000 m končí
net.place("bagrista", (-0.6, 1.7), tokens=1, label="Bagrista", label_pos="above right")
net.arc("bagrista", "pristaveni")
net.arc("odjezd", "bagrista", via=[(4.7, 3.2), (4.7, 6.0), (-0.6, 6.0)])
net.immediate("prestavka", (-2.1, 2.5), label="nemá auto", label_pos="above")
net.place("stanek", (-3.6, 1.7), label="stánek", label_pos="left")
net.timed("svacina", (-2.1, 0.9), "10 min", param_pos="below")
net.arc("bagrista", "prestavka", out=150, into=0)
net.arc("prestavka", "stanek", out=180, into=90)
net.arc("stanek", "svacina", out=270, into=180)
net.arc("svacina", "bagrista", out=0, into=210)
net.immediate("konec", (10, 0), p=2, exit=True, label="úsek hotov", label_pos="right",
              param_pos="above")
net.arc("odstraneno", "konec", w=1000, w_pos="above")
net.arc("bagrista", "konec", via=[(-0.6, -3.0), (10, -3.0)])

net.bound("usek", 1000)
net.bound("odstraneno", 1000)  # po 1000 m je odebere přechod „úsek hotov“
net.invariant({"auta": 1, "u_bagru": 1, "bagruje": 1, "jizda": 1}, 3, name="3 auta")
net.bound("kapacita", 3)
net.bound("u_bagru", 1)
# Práce je konečná: po odstranění 1000 m bagrista odchází a síť se zastaví
# (zastavení je správný konec modelu, ne uváznutí).
net.deadlock_ok = True
