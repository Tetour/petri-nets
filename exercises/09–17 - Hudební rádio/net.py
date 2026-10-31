from pn import Net

net = Net("09–17", "Hudební rádio (půlsemestrálky 2014–19, Z7)")

# posluchači: volají, čekají na konec písničky (nebo reklamy), rozhovor, odchod
net.place("gen", (0, 0), tokens=1, label="volání posluchačů", label_pos="below")
net.timed("volani", (1.5, 0), "exp(20 min)", param_pos="above")
net.loop("gen", "volani")
net.place("cekaji", (3, 0), label="na lince", label_pos="below")
net.immediate("vpusteni", (4.5, 0), p=1, label="vpuštění", label_pos="below",
              param_pos="above left")
net.place("rozhovor", (6, -1.6), label="rozhovor", label_pos="below right")
net.timed("rozh", (7.5, -1.6), "1–2 min", param_pos="above right")
net.chain("volani", "cekaji", "vpusteni")
# rozhovor shora, aby měl volné strany pro přerušení (zdola) a opakování (zleva)
net.arc("vpusteni", "rozhovor", via=[(6, 0)])
net.arc("rozhovor", "rozh")
net.place("konec", (9, -1.6), label="po rozhovoru", label_pos="below")
net.immediate("odchod", (10.5, -1.6), exit=True, label="odchod", label_pos="below")
net.chain("rozh", "konec", "odchod")

# redaktor pouští písničky ze seznamu; po písničce (nebo reklamě) rozhoduje:
# posluchač (vpuštění, p=1), nebo další písnička
net.place("redaktor", (7.5, 1.6), tokens=1, label="Redaktor", label_pos="below right")
net.timed("pisen", (6, 1.6), "3–5 min", label="písnička", label_pos="above", param_pos="below")
net.place("dohrano", (4.5, 1.6), label="dohráno", label_pos="below left")
net.chain("redaktor", "pisen", "dohrano", "vpusteni")
net.immediate("dalsi", (4.5, 3.2), label="další písnička", label_pos="above")
net.arc("dohrano", "dalsi")
net.arc("dalsi", "redaktor", via=[(7.5, 3.2)])
net.arc("rozh", "redaktor")

# reklama každou hodinu: vezme redaktora, přeruší písničku (ta se neopakuje)
net.place("hodiny", (11, 4.8), tokens=1, label="hodiny", label_pos="right")
net.timed("hodina", (11, 3.2), "1 h", param_pos="right")
net.loop("hodiny", "hodina", bend=25)
net.place("na_rade", (11, 1.6), label="reklama na řadě", label_pos="below")
net.arc("hodina", "na_rade")
net.immediate("spust", (9.5, 1.6))
net.arc("na_rade", "spust")
net.arc("redaktor", "spust")
net.place("reklama", (7.5, 4.8), label="reklama", label_pos="above")
net.timed("rekl", (6, 4.8), "5 min", param_pos="above")
net.arc("spust", "reklama", via=[(9.5, 4.8)])
net.arc("reklama", "rekl")
net.arc("rekl", "dohrano", via=[(3, 4.8), (3, 1.6)])

# reklama přeruší rozhovor, rozhovor se pak opakuje od začátku
net.immediate("preruseni", (6, -3.2), label="přerušení", label_pos="below")
net.arc("rozhovor", "preruseni")
net.arc("na_rade", "preruseni", via=[(12.5, 1.6), (12.5, -3.2)])
net.place("ceka", (4.5, -3.2), label="reklama (posluchač čeká)", label_pos="left")
net.timed("rekl2", (4.5, -1.6), "5 min", param_pos="left")
net.chain("preruseni", "ceka", "rekl2", "rozhovor")

net.invariant({"redaktor": 1, "dohrano": 1, "rozhovor": 1, "reklama": 1, "ceka": 1}, 1,
              name="redaktor dělá právě jednu věc")
net.bound("na_rade", 1)
net.sim_events = 50000
