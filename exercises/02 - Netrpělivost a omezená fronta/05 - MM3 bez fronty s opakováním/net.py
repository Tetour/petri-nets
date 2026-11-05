from pn import Net

net = Net("M/M/3 bez fronty, odmítnutá transakce to zkusí znovu po X")
net.params = {"A": 3, "B": 5, "X": 4}

net.place("gen", (0, 0), tokens=1, label="příchody transakcí", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(A)")
net.loop("gen", "prichod")
net.place("zada", (3, 0), label="žádá o linku", label_pos="above right")
net.arc("prichod", "zada")

# nahoru: obsazení volné linky (p=1); M/M/3 = tři linky jako jedno místo se 3 značkami
net.immediate("obsaz", (4.5, 1.8), p=1, param_pos="below")
net.arc("zada", "obsaz", via=[(3, 1.8)])
net.place("linky", (4.5, 3.4), tokens=3, label="Linky")
net.place("obsluha", (6, 1.8))
net.timed("obsl", (7.5, 1.8), "exp(B)")
net.chain("obsaz", "obsluha", "obsl")
net.arc("linky", "obsaz")
net.arc("obsl", "linky", out=90, into=0)
net.place("konec", (9, 1.8), label="konec", label_pos="above")
net.immediate("odchod", (10.5, 1.8), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# dolů: všechny linky obsazené (p=0), transakce odejde a po X se vrátí zprava do „žádá o linku“
net.immediate("odmitnuti", (4.5, -1.8), p=0, label="odmítnutí", label_pos="below",
              param_pos="above")
net.arc("zada", "odmitnuti", via=[(3, -1.8)])
net.place("ceka", (6, -1.8), label="čeká na opakování", label_pos="right")
net.timed("opakovani", (6, 0), "X", label="návrat", label_pos="right", param_pos="above")
net.chain("odmitnuti", "ceka", "opakovani")
net.arc("opakovani", "zada")

net.invariant({"linky": 1, "obsluha": 1}, 3)
net.bound("zada", 1)
