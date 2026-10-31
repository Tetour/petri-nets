from pn import Net

net = Net("02–02", "M/M/1, netrpělivý je jen první ve frontě (odchází po 4)")
net.params = {"A": 5, "B": 4}

# příchody; fronta rozdělená na dvě místa: ostatní čekající a první ve frontě
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(A)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta", label_pos="above")
net.immediate("postup", (4.5, 0))
net.place("prvni", (6, 0), label="První", label_pos="above")
net.chain("prichod", "fronta", "postup", "prvni")
# doplněk místa První: v čele fronty je nejvýš jedna transakce
net.place("volno", (4.5, -2.4), tokens=1, label="1. místo volné", label_pos="below left")
net.arc("volno", "postup")

# linka
net.place("linka", (7.5, 1.6), tokens=1, label="Linka")
net.immediate("obsaz", (7.5, 0))
net.place("obsluha", (9, 0))
net.timed("obsl", (10.5, 0), "exp(B)")
net.chain("prvni", "obsaz", "obsluha", "obsl")
net.arc("linka", "obsaz")
net.arc("obsl", "linka", bend=-25)
net.arc("obsaz", "volno")
net.place("konec", (12, 0), label="konec", label_pos="above")
net.immediate("odchod", (13.5, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# netrpělivost prvního ve frontě
net.timed("netrp", (6, -2.4), "4", horizontal=True, label="netrpělivost",
          label_pos="below", param_pos="above right")
net.arc("prvni", "netrp")
net.arc("netrp", "volno")
net.arc("netrp", "konec", via=[(12, -2.4)])

net.invariant({"linka": 1, "obsluha": 1}, 1)
net.invariant({"volno": 1, "prvni": 1}, 1)
