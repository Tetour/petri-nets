from pn import Net

net = Net("09–17", "Hudební rádio (půlsemestrálky 2014–19, Z7)")

# posluchači: volají, čekají na konec písničky (nebo reklamy), rozhovor
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="below")
net.timed("volani", (1.5, 0), "exp(20 min)", param_pos="below")
net.loop("gen", "volani")
net.place("cekaji", (3.2, 0), label="Posluchači na lince", label_pos="above")
net.immediate("vpusteni", (4.8, 0), p=1, label="vpuštění", label_pos="below",
              param_pos="above right")
net.place("rozhovor", (6.4, 0), label="Rozhovor", label_pos="above right")
net.timed("rozh", (8.4, 0), "1–2 min", param_pos="below")
net.chain("volani", "cekaji", "vpusteni", "rozhovor", "rozh")
net.place("konec", (10, 0), label="po rozhovoru", label_pos="above")
net.immediate("odchod", (11.6, 0), exit=True, label="odchod", label_pos="below")
net.chain("rozh", "konec", "odchod")

# redaktor pouští písničky ze seznamu; po písničce rozhoduje: posluchač (p=1), nebo další písnička
net.place("redaktor", (6.4, 3.4), tokens=1, label="Redaktor", label_pos="above right")
net.timed("pisen", (4.8, 3.4), "3–5 min", horizontal=True, label="písnička", label_pos="above",
          param_pos="left")
net.place("dohrano", (4.8, 1.7), label="dohráno", label_pos="above left")
net.immediate("dalsi", (6.4, 1.7), horizontal=True, label="další písnička", label_pos="right")
net.chain("redaktor", "pisen", "dohrano", "vpusteni")
net.chain("dohrano", "dalsi", "redaktor")
net.arc("rozh", "redaktor", via=[(8.4, 3.4)])

# reklama každou hodinu: přeruší písničku (písnička se neopakuje)
net.place("hodiny", (9.6, 8.1), tokens=1, label="hodiny", label_pos="left")
net.timed("hodina", (9.6, 6.6), "1 h", horizontal=True, param_pos="left")
net.loop("hodiny", "hodina")
net.place("na_rade", (9.6, 5.1), label="reklama na řadě", label_pos="below left")
net.arc("hodina", "na_rade")
net.immediate("spust", (6.4, 5.1))
net.arc("na_rade", "spust")
net.arc("redaktor", "spust")
net.place("reklama", (4.8, 5.1), label="Reklama", label_pos="above")
net.timed("rekl", (2.6, 5.1), "5 min", param_pos="above")
net.chain("spust", "reklama", "rekl")
net.arc("rekl", "dohrano", via=[(2.6, 1.7)])

# reklama přeruší rozhovor, rozhovor se pak opakuje od začátku
net.immediate("preruseni", (8.4, -2.2), horizontal=True, label="přerušení", label_pos="below")
net.arc("na_rade", "preruseni", via=[(13, 5.1), (13, -2.2)])
net.arc("rozhovor", "preruseni")
net.place("ceka", (6.4, -2.2), label="Reklama (posluchač čeká)", label_pos="below left")
net.timed("rekl2", (4.8, -2.2), "5 min", horizontal=True, param_pos="left")
net.chain("preruseni", "ceka", "rekl2", "rozhovor")

net.invariant({"redaktor": 1, "dohrano": 1, "rozhovor": 1, "reklama": 1, "ceka": 1}, 1,
              name="redaktor dělá právě jednu věc")
net.bound("na_rade", 1)
net.sim_events = 50000
