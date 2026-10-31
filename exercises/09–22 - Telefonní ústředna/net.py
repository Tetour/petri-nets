from pn import Net

net = Net("09–22", "Telefonní ústředna (půlsemestrálka, rok neznámý)")

# příchody volajících (30 za hodinu = střed 2 min) a rozdělení 60 % / 40 %
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="below")
net.timed("prichod", (1.5, 0), "exp(2 min)")
net.loop("gen", "prichod")
net.place("volajici", (3, 0), label="Volající", label_pos="above")
net.arc("prichod", "volajici")
net.immediate("zna", (4.5, 1.6), prob=60, label="zná klapku", label_pos="above",
              param_pos="left")
net.immediate("nezna", (4.5, -1.6), prob=40, label="nezná klapku", label_pos="below",
              param_pos="left")
net.arc("volajici", "zna")
net.arc("volajici", "nezna")

# volající, kteří znají klapku, čekají přímo na linku
net.place("ceka_A", (12, 1.6), label="Čeká na linku", label_pos="above")
net.arc("zna", "ceka_A")

# ostatní přes operátorku
net.place("fronta_op", (6, -1.6), label="Fronta", label_pos="above")
net.place("operatorka", (7.5, -3.2), tokens=1, label="Operátorka", label_pos="below")
net.immediate("obsaz_op", (7.5, -1.6))
net.place("u_op", (9, -1.6))
net.timed("zjisteni", (10.5, -1.6), "5–15 s", label="zjištění klapky", label_pos="above",
          param_pos="below left")
net.chain("nezna", "fronta_op", "obsaz_op", "u_op", "zjisteni")
net.arc("operatorka", "obsaz_op")
net.arc("zjisteni", "operatorka", via=[(10.5, -3.2)])
net.place("spojeny", (12, -1.6), label="Spojovaný", label_pos="below")
net.arc("zjisteni", "spojeny")

# 20 linek; spojovaný přes operátorku má přednost (p=1)
net.place("linky", (13.5, 0), tokens=20, label="Linky", label_pos="below left")
net.immediate("obsaz_A", (13.5, 1.6))
net.immediate("obsaz_B", (13.5, -1.6), p=1, param_pos="below")
net.arc("ceka_A", "obsaz_A")
net.arc("spojeny", "obsaz_B")
net.arc("linky", "obsaz_A")
net.arc("linky", "obsaz_B")
net.place("hovor", (15, 0), label="Hovor", label_pos="above")
net.arc("obsaz_A", "hovor")
net.arc("obsaz_B", "hovor")
net.timed("hovor_t", (16.5, 0), "exp(2 min)", param_pos="below")
net.arc("hovor", "hovor_t")
net.arc("hovor_t", "linky", via=[(16.5, 2.8), (12.75, 2.8), (12.75, 0)])

# odchod ze systému
net.place("konec", (18, 0), label="konec", label_pos="below")
net.immediate("odchod", (19.5, 0), exit=True, label="odchod", label_pos="above")
net.chain("hovor_t", "konec", "odchod")

net.invariant({"linky": 1, "hovor": 1}, 20)
net.invariant({"operatorka": 1, "u_op": 1}, 1)
