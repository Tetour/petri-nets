from pn import Net

net = Net("M/M/1, obsluha 5 při frontě aspoň 3, jinak 10")
net.params = {"A": 7}

# příchody
net.place("gen", (0, 0), tokens=1, label="příchody transakcí", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(A)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="fronta", label_pos="above")
net.arc("prichod", "fronta")

# fronta ≥ 3 (včetně té, která obsazuje): z fronty 3, zpět 2, rychlá obsluha rovně
net.immediate("rychle", (4.8, 0), p=1, label="fronta ≥ 3", label_pos="above",
              param_pos="below right")
net.arc("fronta", "rychle", w=3, bend=25, w_pos="above")
net.arc("rychle", "fronta", w=2, bend=25, w_pos="below")
net.place("obsl_r", (6.3, 0))
net.timed("exp5", (7.8, 0), "exp(5)", param_pos="above")
net.chain("rychle", "obsl_r", "exp5")

# jinak běžná obsluha v dolní řadě
net.immediate("bezne", (4.8, -3.2), label="jinak", label_pos="below")
net.arc("fronta", "bezne", via=[(3, -3.2)], corner=20)
net.place("obsl_b", (6.3, -3.2))
net.timed("exp10", (7.8, -3.2), "exp(10)", param_pos="below")
net.chain("bezne", "obsl_b", "exp10")

# Linka mezi oběma řadami: zespodu do rychlé větve, shora do běžné
net.place("linka", (6.3, -1.6), tokens=1, label="Linka", label_pos="below left")
net.arc("linka", "rychle", via=[(6.3, -0.8), (4.8, -0.8)])
net.arc("linka", "bezne", via=[(4.8, -1.6)])
net.arc("exp5", "linka", out=270, into=0)
net.arc("exp10", "linka", via=[(7.8, -2.4), (6.3, -2.4)])

# odchod
net.place("konec", (9.3, -1.6), label="konec", label_pos="left")
net.immediate("odchod", (10.8, -1.6), exit=True, label="odchod")
net.arc("exp5", "konec", via=[(9.3, 0)], corner=20)
net.arc("exp10", "konec", via=[(9.3, -3.2)], corner=20)
net.arc("konec", "odchod")

net.invariant({"linka": 1, "obsl_r": 1, "obsl_b": 1}, 1)
