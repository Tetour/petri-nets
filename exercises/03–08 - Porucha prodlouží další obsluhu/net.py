from pn import Net

net = Net("03–08", "M/M/1, porucha prodlouží obsluhu první následující transakce o 10")
net.params = {"A": 10, "B": 6, "X": 50}

# M/M/1 s rozhodnutím na začátku obsluhy (rozmístění jako v 03–02)
net.place("gen", (0, 0), tokens=1, label="příchody transakcí", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(A)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta")
net.immediate("obsaz", (4.5, 0))
net.place("zahajeni", (6, 0), label="zahájení")
net.immediate("bez", (7.5, 0), label="bez poruchy", label_pos="below")
net.place("obsluha", (9, 0), label="obsluha", label_pos="above")
net.timed("obsl", (10.5, 0), "exp(B)")
net.chain("prichod", "fronta", "obsaz", "zahajeni", "bez", "obsluha", "obsl")
net.place("linka", (10.5, 1.6), tokens=1, label="Linka")
net.arc("linka", "obsaz", via=[(4.5, 1.6)])
net.arc("obsl", "linka")
net.place("konec", (12, 0), label="hotovo")
net.immediate("odchod", (13.5, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# prodloužená obsluha pod hlavní řadou: 10 j. navíc před běžnou obsluhou
net.immediate("s_poruchou", (6, -1.6), p=1, param_pos="left")
net.arc("zahajeni", "s_poruchou")
net.place("prodl", (7.5, -1.6), label="prodloužení", label_pos="below")
net.timed("deset", (9, -1.6), "10", param_pos="right")
net.chain("s_poruchou", "prodl", "deset", "obsluha")

# poruchy: řada pod prodloužením; druhá čekající porucha nemá účinek (sloučí se s první)
net.place("gen_p", (3, -3.2), tokens=1, label="vznik poruch", label_pos="left")
net.timed("vznik", (4.5, -3.2), "exp(X)")
net.loop("gen_p", "vznik")
net.place("porucha", (6, -3.2), label="porucha", label_pos="below")
net.arc("vznik", "porucha")
net.arc("porucha", "s_poruchou")
net.immediate("zanik", (7.8, -3.2), label="další porucha bez účinku", label_pos="right")
net.arc("porucha", "zanik", w=2, bend=20, w_pos="above")
net.arc("zanik", "porucha", bend=20)

net.invariant({"linka": 1, "zahajeni": 1, "prodl": 1, "obsluha": 1}, 1)
net.bound("porucha", 1)
