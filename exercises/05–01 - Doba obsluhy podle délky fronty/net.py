from pn import Net

net = Net("05–01", "M/M/1, obsluha 5 při frontě aspoň 3, jinak 10")
net.params = {"A": 7}

# příchody
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(A)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta", label_pos="above left")
net.arc("prichod", "fronta")

# linka mezi oběma způsoby obsazení
net.place("linka", (4.5, 0), tokens=1, label="Linka", label_pos="right")

# fronta >= 3 (včetně té, která obsazuje): rychlá obsluha
net.immediate("rychle", (4.5, 1.6), p=1, label="fronta ≥ 3", label_pos="above",
              param_pos="above right")
net.arc("fronta", "rychle", w=3, bend=12, w_pos="above left")
net.arc("rychle", "fronta", w=2, bend=12, w_pos="below right")
net.place("obsl_r", (6, 1.6))
net.timed("exp5", (7.5, 1.6), "exp(5)", param_pos="above")
net.chain("rychle", "obsl_r", "exp5")

# jinak běžná obsluha
net.immediate("bezne", (4.5, -1.6), label="jinak", label_pos="below")
net.arc("fronta", "bezne")
net.place("obsl_b", (6, -1.6))
net.timed("exp10", (7.5, -1.6), "exp(10)")
net.chain("bezne", "obsl_b", "exp10")

net.arc("linka", "rychle")
net.arc("linka", "bezne")
net.arc("exp5", "linka")
net.arc("exp10", "linka")

# odchod
net.place("konec", (9, 0))
net.immediate("odchod", (10.5, 0), exit=True, label="odchod")
net.arc("exp5", "konec")
net.arc("exp10", "konec")
net.arc("konec", "odchod")

net.invariant({"linka": 1, "obsl_r": 1, "obsl_b": 1}, 1)
