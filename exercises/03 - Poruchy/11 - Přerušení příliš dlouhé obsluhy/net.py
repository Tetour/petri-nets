from pn import Net

net = Net("M/M/1, obsluha delší než X se přeruší a transakce odchází")
net.params = {"A": 10, "B": 6, "X": 10}

# M/M/1 (rozmístění jako v úloze „Porucha vrací transakci do fronty“)
net.place("gen", (0, 0), tokens=1, label="příchody transakcí", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(A)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta")
net.immediate("obsaz", (4.5, 0))
net.place("obsluha", (6, 0), label="obsluha")
net.timed("obsl", (7.5, 0), "exp(B)")
net.chain("prichod", "fronta", "obsaz", "obsluha", "obsl")
net.place("linka", (7.5, 1.6), tokens=1, label="Linka")
net.arc("linka", "obsaz", via=[(4.5, 1.6)])
net.arc("obsl", "linka")
net.place("konec", (9, 0), label="hotovo")
net.immediate("odchod", (10.5, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# časový limit obsluhy přímo pod místem obsluha: soupeří s exp(B) o značku transakce
net.timed("limit", (6, -1.6), "X", param_pos="left")
net.arc("obsluha", "limit")
net.place("prerusena", (7.5, -1.6), label="přerušená", label_pos="below")
net.immediate("odchod_p", (9, -1.6), exit=True, label="odchod po přerušení", label_pos="right")
net.chain("limit", "prerusena", "odchod_p")
# linka zpět (zespodu kolem odchodů)
net.arc("limit", "linka", via=[(6, -3.0), (12.6, -3.0), (12.6, 1.6)])

net.invariant({"linka": 1, "obsluha": 1}, 1)
