from pn import Net


net = Net("M/M/1, po každém příchodu interval exp(A) při frontě aspoň C, jinak exp(B)")
net.params = {"A": 20, "B": 5, "C": 5, "S": 8}

# po příchodu se rozhodne o dalším intervalu: fronta ≥ C rovně (test vedle fronty), jinak dolů
net.place("volba", (1.5, 0), label="po příchodu", label_pos="above left")
net.immediate("vol_a", (3, 0), p=1, label="fronta ≥ C", label_pos="below",
              param_pos="above left")
net.immediate("vol_b", (3, -1.6), label="jinak", label_pos="right")
net.arc("volba", "vol_a")
net.arc("volba", "vol_b", via=[(1.5, -1.6)], corner=20)

# interval A nad testem, interval B pod větví „jinak“
net.place("gen_a", (3, 1.6), label="interval A", label_pos="above")
net.timed("prichod_a", (5, 1.6), "exp(A)", param_pos="right")
net.chain("vol_a", "gen_a", "prichod_a")
net.place("gen_b", (3, -3.2), tokens=1, label="interval B", label_pos="left")
net.timed("prichod_b", (5, -3.2), "exp(B)", param_pos="right")
net.chain("vol_b", "gen_b", "prichod_b")

# každý příchod vrací značku generátoru do „po příchodu“ a transakci dává do fronty
net.arc("prichod_a", "volba", via=[(5, 2.9), (1.5, 2.9)])
net.arc("prichod_b", "volba", via=[(5, -4.3), (0, -4.3), (0, 0)])
net.place("fronta", (5, 0), label="fronta", label_pos="below right")
net.arc("prichod_a", "fronta")
net.arc("prichod_b", "fronta")
net.arc("fronta", "vol_a", w="C", bend=25, w_pos="below")
net.arc("vol_a", "fronta", w="C", bend=25, w_pos="above")

# M/M/1
net.place("linka", (6.8, 1.6), tokens=1, label="Linka", label_pos="above")
net.immediate("obsaz", (6.8, 0))
net.place("obsluha", (8.3, 0))
net.timed("obsl", (9.8, 0), "exp(S)")
net.chain("fronta", "obsaz", "obsluha", "obsl")
net.arc("linka", "obsaz")
net.arc("obsl", "linka", out=90, into=0)
net.place("konec", (11.3, 0))
net.immediate("odchod", (12.8, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

net.invariant({"linka": 1, "obsluha": 1}, 1)
net.invariant({"volba": 1, "gen_a": 1, "gen_b": 1}, 1, name="jeden generátor")
