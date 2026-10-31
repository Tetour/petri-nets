from pn import Net


net = Net("05–04", "M/M/1, po každém příchodu interval exp(A) při frontě aspoň C, jinak exp(B)")
net.params = {"A": 20, "B": 5, "C": 5, "S": 8}

# po příchodu se rozhodne o dalším intervalu
net.place("volba", (0, 0), label="po příchodu", label_pos="left")
net.immediate("vol_a", (1.5, 1.9), p=1, label="fronta ≥ C", label_pos="above",
              param_pos="above left")
net.immediate("vol_b", (1.5, -1.9), label="jinak", label_pos="below")
net.arc("volba", "vol_a")
net.arc("volba", "vol_b")
net.place("gen_a", (3, 1.9), label="interval A", label_pos="above")
net.place("gen_b", (3, -1.9), tokens=1, label="interval B", label_pos="below")
net.timed("prichod_a", (4.5, 1.9), "exp(A)", param_pos="right")
net.timed("prichod_b", (4.5, -1.9), "exp(B)", param_pos="right")
net.chain("vol_a", "gen_a", "prichod_a")
net.chain("vol_b", "gen_b", "prichod_b")
net.arc("prichod_a", "volba", via=[(4.5, 3.3), (0, 3.3)])
net.arc("prichod_b", "volba", via=[(4.5, -3.3), (0, -3.3)])

# M/M/1
net.place("fronta", (4.5, 0), label="Fronta", label_pos="below left")
net.arc("prichod_a", "fronta")
net.arc("prichod_b", "fronta")
net.arc("fronta", "vol_a", w="C", bend=9, w_pos="below left")
net.arc("vol_a", "fronta", w="C", bend=9, w_pos="above right")
net.place("linka", (6.3, 1.7), tokens=1, label="Linka", label_pos="above")
net.immediate("obsaz", (6.3, 0))
net.place("obsluha", (7.8, 0))
net.timed("obsl", (9.3, 0), "exp(S)")
net.chain("fronta", "obsaz", "obsluha", "obsl")
net.arc("linka", "obsaz")
net.arc("obsl", "linka", bend=-25)
net.place("konec", (10.8, 0))
net.immediate("odchod", (12.3, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

net.invariant({"linka": 1, "obsluha": 1}, 1)
net.invariant({"volba": 1, "gen_a": 1, "gen_b": 1}, 1, name="jeden generátor")
