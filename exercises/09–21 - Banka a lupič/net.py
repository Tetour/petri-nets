from pn import Net

net = Net("09–21", "Banka a lupič (půlsemestrálka 2010/11)")

# klienti: M/M/1 u přepážky
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="above left")
net.timed("prichod", (1.5, 0), "exp(10 min)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta", label_pos="above")
net.place("prepazka", (4.5, -1.6), tokens=1, label="Přepážka", label_pos="left")
net.immediate("obsaz", (4.5, 0))
net.place("obsluha", (6, 0))
net.timed("obsl", (7.5, 0), "exp(5 min)", param_pos="above")
net.chain("prichod", "fronta", "obsaz", "obsluha", "obsl")
net.arc("prepazka", "obsaz")
net.arc("obsl", "prepazka", via=[(7.5, -1.6)])
net.place("konec", (9, 0), label="konec", label_pos="above")
net.immediate("odchod", (10.5, 0), exit=True, label="odchod", label_pos="above")
net.chain("obsl", "konec", "odchod")

# v okamžiku přepadení odchází klient u přepážky i všichni ve frontě (p=1)
net.immediate("vyhnani_f", (3, -3.0), p=1, horizontal=True, param_pos="below left")
net.immediate("vyhnani_k", (6, -3.0), p=1, horizontal=True, param_pos="below right")
net.arc("fronta", "vyhnani_f")
net.arc("obsluha", "vyhnani_k")
net.arc("vyhnani_k", "prepazka")
net.arc("vyhnani_k", "konec", via=[(9, -3.0)])
net.place("vyhnani", (1.5, -3.0), label="vyhnaní", label_pos="above")
net.arc("vyhnani_f", "vyhnani")
net.immediate("odchod_v", (0, -3.0), exit=True, label="odchod", label_pos="above")
net.arc("vyhnani", "odchod_v")

# lupič: přijde-li a vidí policistu (p=1), odchází; jinak přepadne banku
net.place("gen_l", (-1.5, -5), tokens=1, label="lupiči", label_pos="below")
net.timed("prichod_l", (0, -5), "exp(1 měsíc)", sim="exp(30 d)", param_pos="below")
net.loop("gen_l", "prichod_l")
net.place("lupic", (1.5, -5), label="Lupič u banky", label_pos="above")
net.arc("prichod_l", "lupic")
net.immediate("prepadeni_t", (3, -5))
net.arc("lupic", "prepadeni_t")
net.arc("gen", "prepadeni_t", via=[(-0.9, 0), (-0.9, -3.8), (3, -3.8)])
net.place("prepadeni", (4.5, -5), label="Přepadení", label_pos="below right")
net.arc("prepadeni_t", "prepadeni")
net.loop("prepadeni", "vyhnani_f", bend=15)
net.loop("prepadeni", "vyhnani_k", bend=15)

# konec přepadení po 5–10 min, nebo hned, když přijde policista
net.timed("konec_prep", (6.3, -5), "5–10 min", param_pos="above")
net.immediate("likvidace", (4.5, -6.2), horizontal=True, label="zlikvidování",
              label_pos="below right", param_pos="right")
net.arc("prepadeni", "konec_prep")
net.arc("prepadeni", "likvidace")
net.place("po_prep", (8.1, -5), label="konec přepadení", label_pos="above")
net.arc("konec_prep", "po_prep")
net.arc("likvidace", "po_prep", via=[(8.1, -6.2)])
net.immediate("lupic_pryc", (9.9, -5))
net.arc("po_prep", "lupic_pryc")

# po 10 minutách obnova provozu: generátor klientů dostane značku zpět
net.place("obnova", (11.7, -5), label="obnova provozu", label_pos="above")
net.timed("obnova_t", (13.5, -5), "10 min", param_pos="above")
net.chain("lupic_pryc", "obnova", "obnova_t")
net.arc("obnova_t", "gen", via=[(13.5, -10.6), (-2.4, -10.6), (-2.4, 1), (0, 1)])

# lupiči opouštějí systém
net.place("lupic_ven", (9.9, -6.2), label="lupič odchází", label_pos="below left")
net.arc("lupic_pryc", "lupic_ven")
net.immediate("odchod_l", (11.7, -6.2), exit=True, label="odchod", label_pos="right")
net.arc("lupic_ven", "odchod_l")
net.immediate("vidi", (1.5, -6.2), p=1, horizontal=True, label="vidí policistu",
              label_pos="below left", param_pos="right")
net.arc("lupic", "vidi")
net.arc("vidi", "lupic_ven", via=[(0.6, -6.2), (0.6, -10), (9.9, -10)])

# policista: obchůzka exp(2 h), u banky 3–5 min
net.place("u_banky", (3, -7.6), label="Policista u banky", label_pos="right")
net.loop("u_banky", "vidi", bend=15)
net.loop("u_banky", "likvidace", bend=15)
net.place("obchuzka", (3, -9.2), tokens=1, label="obchůzka", label_pos="below")
net.timed("prichod_p", (1.8, -8.4), "exp(2 h)", param_pos="left")
net.timed("odchod_p", (4.2, -8.4), "3–5 min", param_pos="right")
net.chain("obchuzka", "prichod_p", "u_banky", "odchod_p", "obchuzka")

net.invariant({"prepazka": 1, "obsluha": 1}, 1)
net.invariant({"gen": 1, "prepadeni": 1, "po_prep": 1, "obnova": 1}, 1)
net.invariant({"obchuzka": 1, "u_banky": 1}, 1)
net.bound("lupic", 1)
net.sim_events = 300000
