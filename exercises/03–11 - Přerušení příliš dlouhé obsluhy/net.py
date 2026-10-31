from pn import Net

net = Net("03–11", "M/M/1, obsluha delší než X se přeruší a transakce odchází")
net.params = {"A": 10, "B": 6, "X": 10}

# M/M/1 (rozmístění jako v 03–02)
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(A)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta")
net.place("linka", (5.4, 1.7), tokens=1, label="Linka")
net.immediate("obsaz", (4.5, 0))
net.place("obsluha", (6.3, 0))
net.timed("obsl", (7.8, 0), "exp(B)")
net.chain("prichod", "fronta", "obsaz", "obsluha", "obsl")
net.arc("linka", "obsaz")
net.arc("obsl", "linka", bend=-25)
net.place("konec", (9.3, 0))
net.immediate("odchod", (10.8, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# časový limit obsluhy: soupeří s exp(B) o značku v místě obsluhy
net.timed("limit", (5.4, -1.8), "X", horizontal=True, param_pos="below")
net.arc("obsluha", "limit")
net.arc("limit", "linka")
net.place("prerusena", (3.6, -1.8), label="přerušená", label_pos="above")
net.arc("limit", "prerusena")
net.immediate("odchod_p", (2.1, -1.8), exit=True, label="odchod po přerušení", label_pos="below")
net.arc("prerusena", "odchod_p")

net.invariant({"linka": 1, "obsluha": 1}, 1)
