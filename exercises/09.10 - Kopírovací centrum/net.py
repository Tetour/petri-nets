from pn import Net

net = Net("09.10", "Kopírovací centrum (půlsemestrálka 2022/23, varianta A)")

# příchody a registrace u přepážky
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="below")
net.timed("prichod", (1.5, 0), "exp(3 min)", param_pos="below")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta")
net.place("prepazka", (4.5, 1.6), tokens=1, label="Přepážka")
net.immediate("reg_start", (4.5, 0))
net.place("registrace", (6, 0))
net.timed("reg", (7.5, 0), "1–2 min")
net.chain("prichod", "fronta", "reg_start", "registrace", "reg")
net.arc("prepazka", "reg_start")
net.arc("reg", "prepazka", bend=-25)

# rozdělení zakázek
net.place("rozdeleni", (9, 0), label="rozdělování")
net.arc("reg", "rozdeleni")
net.immediate("na_A", (10.5, 2), prob=70)
net.immediate("na_B", (10.5, -2), prob=30, param_pos="above")
net.arc("rozdeleni", "na_A")
net.arc("rozdeleni", "na_B")

# stroj A (normální zakázky)
net.place("fronta_A", (12, 2), label="Fronta A", label_pos="below")
net.place("stroj_A", (13.5, 3.6), tokens=1, label="Stroj A")
net.immediate("obsaz_A", (13.5, 2))
net.place("kopiruje_A", (15, 2))
net.timed("kop_A", (16.5, 2), "exp(3 min)", param_pos="right")
net.chain("na_A", "fronta_A", "obsaz_A", "kopiruje_A", "kop_A")
net.arc("stroj_A", "obsaz_A")
net.arc("kop_A", "stroj_A", bend=-25)

# stroj B (speciální zakázky) a netrpělivost
net.place("fronta_B", (12, -2), label="Fronta B", label_pos="below")
net.place("stroj_B", (13.5, -3.6), tokens=1, label="Stroj B", label_pos="below")
net.immediate("obsaz_B", (13.5, -2))
net.place("kopiruje_B", (15, -2))
net.timed("kop_B", (16.5, -2), "exp(3 min)", param_pos="right")
net.chain("na_B", "fronta_B", "obsaz_B", "kopiruje_B", "kop_B")
net.arc("stroj_B", "obsaz_B")
net.arc("kop_B", "stroj_B", bend=25)
net.timed("netrpelivost", (13.5, -0.4), "10 min", horizontal=True, param_pos="above")
net.arc("fronta_B", "netrpelivost", via=[(12, -0.4)])

# odchod ze systému
net.place("konec", (18, 0), label="konec", label_pos="below right")
net.immediate("odchod", (19.7, 0), exit=True, label="odchod")
net.arc("kop_A", "konec")
net.arc("kop_B", "konec")
net.arc("netrpelivost", "konec")
net.arc("konec", "odchod")

net.invariant({"prepazka": 1, "registrace": 1}, 1)
net.invariant({"stroj_A": 1, "kopiruje_A": 1}, 1)
net.invariant({"stroj_B": 1, "kopiruje_B": 1}, 1)
