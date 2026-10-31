from pn import Net

net = Net("04–04", "M/M/1 – je-li po dokončení obsluhy fronta prázdná, následuje údržba 5 č. j.")
net.params = {"A": 10, "B": 6}

# M/M/1; obsluha linku nevrací přímo, rozhoduje se až po ní
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(A)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta", label_pos="below")
net.place("linka", (4.5, 1.7), tokens=1, label="Linka", label_pos="above right")
net.immediate("obsaz", (4.5, 0))
net.place("obsluha", (6.3, 0))
net.timed("obsl", (7.8, 0), "exp(B)")
net.chain("prichod", "fronta", "obsaz", "obsluha", "obsl")
net.arc("linka", "obsaz")
net.place("konec", (9.3, 0))
net.immediate("odchod", (10.8, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# po obsluze: linka čeká na rozhodnutí v místě „dokončeno“
net.place("dokonceno", (3, 3.4), label="dokončeno", label_pos="left")
net.arc("obsl", "dokonceno", via=[(7.8, 5.1), (3, 5.1)])

# fronta neprázdná (testovací hrany na Frontě): linka je hned volná
net.immediate("neprazdna", (3, 1.7), p=1, label="fronta neprázdná", label_pos="left",
              param_pos="above left")
net.arc("dokonceno", "neprazdna")
net.loop("fronta", "neprazdna", bend=25)
net.arc("neprazdna", "linka")

# fronta prázdná: údržba 5
net.immediate("prazdna", (4.5, 3.4), horizontal=True, label="fronta prázdná",
              label_pos="above")
net.arc("dokonceno", "prazdna")
net.place("udrzba", (6.3, 3.4), label="údržba", label_pos="above")
net.arc("prazdna", "udrzba")
net.timed("konec_udrzby", (6.3, 1.7), "5", param_pos="right")
net.arc("udrzba", "konec_udrzby")
net.arc("konec_udrzby", "linka")

net.invariant({"linka": 1, "obsluha": 1, "dokonceno": 1, "udrzba": 1}, 1,
              name="linka je volná, obsluhuje, rozhoduje se, nebo je v údržbě")
