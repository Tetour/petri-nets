from pn import Net

net = Net("Telefonní ústředna (půlsemestrálka, rok neznámý)")

# příchody volajících (30 za hodinu = střed 2 min) a rozdělení 60 % nahoru / 40 % dolů
net.place("gen", (0, 0), tokens=1, label="volání zákazníků", label_pos="below")
net.timed("prichod", (1.5, 0), "exp(2 min)", param_pos="above")
net.loop("gen", "prichod")
net.place("volajici", (3, 0), label="volající", label_pos="right")
net.arc("prichod", "volajici")
net.immediate("zna", (4.5, 2.4), prob=60, label="zná klapku", label_pos="below",
              param_pos="above")
net.immediate("nezna", (4.5, -2.4), prob=40, label="nezná klapku", label_pos="above",
              param_pos="below")
net.arc("volajici", "zna", via=[(3, 2.4)], corner=20)
net.arc("volajici", "nezna", via=[(3, -2.4)], corner=20)

# volající, kteří znají klapku, čekají přímo na linku
net.place("ceka_A", (12.3, 2.4), label="čeká na linku", label_pos="above")
net.arc("zna", "ceka_A")

# ostatní přes operátorku
net.place("fronta_op", (6, -2.4), label="fronta", label_pos="above")
net.place("operatorka", (7.5, -4), tokens=1, label="Operátorka", label_pos="below")
net.immediate("obsaz_op", (7.5, -2.4))
net.place("u_op", (9, -2.4))
net.timed("zjisteni", (10.5, -2.4), "5–15 s", label="zjištění klapky", label_pos="above",
          param_pos="below right")
net.chain("nezna", "fronta_op", "obsaz_op", "u_op", "zjisteni")
net.arc("operatorka", "obsaz_op")
net.arc("zjisteni", "operatorka", out=270, into=0)
net.place("spojeny", (12.3, -2.4), label="spojovaný", label_pos="below")
net.arc("zjisteni", "spojeny")

# 20 linek mezi oběma řadami; spojovaný přes operátorku má přednost (p=1)
net.place("linky", (13.5, 0), tokens=20, label="Linky", label_pos="left")
net.immediate("obsaz_A", (13.5, 2.4))
net.immediate("obsaz_B", (13.5, -2.4), p=1, param_pos="below right")
net.arc("ceka_A", "obsaz_A")
net.arc("spojeny", "obsaz_B")
net.arc("linky", "obsaz_A")
net.arc("linky", "obsaz_B")
net.place("hovor", (15, 0), label="hovor", label_pos="below right")
net.arc("obsaz_A", "hovor", via=[(15, 2.4)], corner=20)
net.arc("obsaz_B", "hovor", via=[(15, -2.4)], corner=20)
net.timed("hovor_t", (16.5, 0), "exp(2 min)", param_pos="above")
net.arc("hovor", "hovor_t")
# návrat linky do skladu zprava (jediné křížení: se spojením zdola do „hovor“)
net.arc("hovor_t", "linky", via=[(16.5, -1.4), (14.25, -1.4), (14.25, 0)])

# odchod ze systému
net.place("konec", (18, 0), label="konec", label_pos="below")
net.immediate("odchod", (19.5, 0), exit=True, label="odchod", label_pos="above")
net.chain("hovor_t", "konec", "odchod")

net.invariant({"linky": 1, "hovor": 1}, 20)
net.invariant({"operatorka": 1, "u_op": 1}, 1)
