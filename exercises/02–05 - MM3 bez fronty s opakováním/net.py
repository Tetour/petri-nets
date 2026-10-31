from pn import Net

net = Net("02–05", "M/M/3 bez fronty, odmítnutá transakce to zkusí znovu po X")
net.params = {"A": 3, "B": 5, "X": 4}

net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(A)")
net.loop("gen", "prichod")
net.place("zada", (3, 0), label="žádá o linku", label_pos="above")
net.arc("prichod", "zada")

# M/M/3: tři linky jako jedno místo se 3 značkami
net.place("linky", (4.5, 1.7), tokens=3, label="Linky")
net.immediate("obsaz", (4.5, 0), p=1, param_pos="below right")
net.place("obsluha", (6, 0))
net.timed("obsl", (7.5, 0), "exp(B)")
net.chain("zada", "obsaz", "obsluha", "obsl")
net.arc("linky", "obsaz")
net.arc("obsl", "linky", bend=-25)
net.place("konec", (9, 0), label="konec", label_pos="above")
net.immediate("odchod", (10.5, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# všechny linky obsazené: transakce odejde a po X se vrátí
net.immediate("odmitnuti", (4.5, -1.6), label="odmítnutí", label_pos="right")
net.place("ceka", (3, -3.2), label="čeká na opakování", label_pos="below")
net.timed("opakovani", (1.5, -1.6), "X", label="návrat", label_pos="left",
          param_pos="below left")
net.chain("zada", "odmitnuti", "ceka", "opakovani", "zada")

net.invariant({"linky": 1, "obsluha": 1}, 3)
net.bound("zada", 1)
