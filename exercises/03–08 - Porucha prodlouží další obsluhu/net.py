from pn import Net

net = Net("03–08", "M/M/1, porucha prodlouží obsluhu první následující transakce o 10")
net.params = {"A": 10, "B": 6, "X": 50}

# M/M/1 s rozhodnutím na začátku obsluhy
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(A)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta")
net.place("linka", (5.25, 1.7), tokens=1, label="Linka")
net.immediate("obsaz", (4.5, 0))
net.place("zahajeni", (6, 0), label="zahájení", label_pos="above")
net.immediate("bez", (7.5, 0), label="bez poruchy", label_pos="below")
net.place("obsluha", (9, 0))
net.timed("obsl", (10.5, 0), "exp(B)", param_pos="below right")
net.chain("prichod", "fronta", "obsaz", "zahajeni", "bez", "obsluha", "obsl")
net.arc("linka", "obsaz")
net.arc("obsl", "linka", via=[(10.5, 1.7)])
net.place("konec", (12, 0))
net.immediate("odchod", (13.5, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# prodloužená obsluha: 10 j. navíc před běžnou obsluhou
net.immediate("s_poruchou", (6, -1.8), p=1, horizontal=True, param_pos="left")
net.arc("zahajeni", "s_poruchou")
net.place("prodl", (7.5, -1.8), label="prodloužení", label_pos="below")
net.arc("s_poruchou", "prodl")
net.timed("deset", (9, -1.8), "10", horizontal=True, param_pos="below")
net.arc("prodl", "deset")
net.arc("deset", "obsluha")

# poruchy; druhá čekající porucha nemá účinek (sloučí se s první)
net.place("gen_p", (9, -3.6), tokens=1, label="generátor poruch", label_pos="right")
net.timed("vznik", (7.5, -3.6), "exp(X)", param_pos="below")
net.loop("gen_p", "vznik")
net.place("porucha", (6, -3.6), label="porucha", label_pos="below")
net.arc("vznik", "porucha")
net.arc("porucha", "s_poruchou")
net.immediate("zanik", (4.2, -3.6), label="další porucha bez účinku", label_pos="left",
              param_pos="above")
net.arc("porucha", "zanik", w=2, bend=-20, w_pos="below")
net.arc("zanik", "porucha", bend=-20)

net.invariant({"linka": 1, "zahajeni": 1, "prodl": 1, "obsluha": 1}, 1)
net.bound("porucha", 1)
