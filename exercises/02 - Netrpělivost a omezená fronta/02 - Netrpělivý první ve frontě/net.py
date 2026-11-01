from pn import Net

net = Net("M/M/1, netrpělivý je jen první ve frontě (odchází po 4)")
net.params = {"A": 5, "B": 4}

# příchody; fronta rozdělená na dvě místa: ostatní čekající a první ve frontě
net.place("gen", (0, 0), tokens=1, label="příchody transakcí", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(A)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta", label_pos="above")
net.immediate("postup", (4.5, 0))
net.place("prvni", (6, 0), label="První", label_pos="above")
net.chain("prichod", "fronta", "postup", "prvni")
# doplněk místa První: v čele fronty je nejvýš jedna transakce
net.place("volno", (4.5, -1.8), tokens=1, label="1. místo volné", label_pos="left")
net.arc("volno", "postup")

# netrpělivost prvního ve frontě: vrací doplněk a transakce odchází bez obsluhy
net.timed("netrp", (6, -1.8), "4", label="netrpělivost", label_pos="below",
          param_pos="above right")
net.arc("prvni", "netrp")
net.arc("netrp", "volno")
net.place("odesel", (7.5, -1.8))
net.immediate("odchod2", (9, -1.8), exit=True, label="odchod bez obsluhy", label_pos="below")
net.chain("netrp", "odesel", "odchod2")

# linka; obsazení uvolní čelo fronty (vrací doplněk oklikou pod netrpělivou větví)
net.place("linka", (10.5, 1.6), tokens=1, label="Linka")
net.immediate("obsaz", (10.5, 0))
net.place("obsluha", (12, 0))
net.timed("obsl", (13.5, 0), "exp(B)")
net.chain("prvni", "obsaz", "obsluha", "obsl")
net.arc("linka", "obsaz")
net.arc("obsl", "linka", out=90, into=0)
net.arc("obsaz", "volno", via=[(10.5, -3.6), (4.5, -3.6)])
net.place("konec", (15, 0), label="konec", label_pos="above")
net.immediate("odchod", (16.5, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

net.invariant({"linka": 1, "obsluha": 1}, 1)
net.invariant({"volno": 1, "prvni": 1}, 1)
