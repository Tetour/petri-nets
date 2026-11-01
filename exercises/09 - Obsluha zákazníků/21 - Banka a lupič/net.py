from pn import Net

net = Net("Banka a lupič (půlsemestrálka 2010/11)")

# klienti: M/M/1 u přepážky
net.place("gen", (0, 0), tokens=1, label="příchody klientů", label_pos="left")
net.timed("prichod", (1.5, 0), "exp(10 min)", param_pos="above")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="fronta", label_pos="above")
net.place("prepazka", (4.5, 1.6), tokens=1, label="Přepážka", label_pos="above")
net.immediate("obsaz", (4.5, 0))
net.place("obsluha", (6, 0))
net.timed("obsl", (7.5, 0), "exp(5 min)", param_pos="below")
net.chain("prichod", "fronta", "obsaz", "obsluha", "obsl")
net.arc("prepazka", "obsaz")
net.arc("obsl", "prepazka", out=90, into=0)
net.place("konec", (9, 0), label="konec", label_pos="above")
net.immediate("odchod", (10.5, 0), exit=True, label="odchod", label_pos="above")
net.chain("obsl", "konec", "odchod")

# v okamžiku přepadení odchází klient u přepážky i všichni ve frontě (p=1, test na přepadení)
net.immediate("vyhnani_f", (3, -1.6), p=1, param_pos="above left")
net.immediate("vyhnani_k", (6, -1.6), p=1, param_pos="above right")
net.arc("fronta", "vyhnani_f")
net.arc("obsluha", "vyhnani_k")
# přepážka se vrací zleva (jediné křížení s řadou klientů)
net.arc("vyhnani_k", "prepazka", via=[(3.75, -1.6), (3.75, 1.6)])
net.arc("vyhnani_k", "konec", via=[(9, -1.6)])
net.place("vyhnani", (1.5, -1.6), label="vyhnaní", label_pos="above")
net.immediate("odchod_v", (1.5, -2.85), exit=True, label="odchod", label_pos="left")
net.chain("vyhnani_f", "vyhnani", "odchod_v")

# přepadení: lupič vezme i značku příchodů klientů (zastaví příchody).
# Stav „přepadení“ je samostatné místo, které časovaný přechod nebere: testují ho přechody
# vyhnání, a kdyby byl vstupem odpočtu 5–10 min, každý test by ho spustil znovu (slajdy 137–139).
# Odpočet běží na místě „přepadení trvá“.
net.immediate("prepadeni_t", (3, -4.6))
net.arc("gen", "prepadeni_t", via=[(0, -4.6)])
net.place("prepadeni", (4.5, -3.0), label="přepadení", label_pos="below right")
net.arc("prepadeni_t", "prepadeni", via=[(3, -3.0)])
net.loop("prepadeni", "vyhnani_f", bend=15)
net.loop("prepadeni", "vyhnani_k", bend=15)
net.place("prep_trva", (4.5, -4.6), label="přepadení trvá", label_pos="below right")
net.arc("prepadeni_t", "prep_trva")

# konec přepadení po 5–10 min, nebo hned, když přijde policista (zlikvidování)
net.timed("konec_prep", (7.2, -4.6), "5–10 min", param_pos="above")
net.immediate("likvidace", (4.5, -6.2), label="zlikvidování", label_pos="above right")
net.place("po_prep", (9.1, -4.6), label="konec přepadení", label_pos="above")
net.chain("prep_trva", "konec_prep", "po_prep")
net.arc("prep_trva", "likvidace")
net.arc("likvidace", "po_prep", via=[(9.1, -6.2)])
net.immediate("lupic_pryc", (10.6, -4.6))
net.arc("po_prep", "lupic_pryc")
net.arc("prepadeni", "lupic_pryc", via=[(10.6, -3.0)])

# po 10 minutách obnova provozu: příchody klientů dostanou značku zpět
net.place("obnova", (12.1, -4.6), label="obnova provozu", label_pos="below")
net.timed("obnova_t", (13.6, -4.6), "10 min", param_pos="right")
net.chain("lupic_pryc", "obnova", "obnova_t")
net.arc("obnova_t", "gen", via=[(13.6, 3.2), (0, 3.2)])

# lupiči: přijde-li a vidí policistu (p=1), odchází; jinak přepadne banku
net.place("gen_l", (-1.5, -6.2), tokens=1, label="příchody lupičů", label_pos="left")
net.timed("prichod_l", (0, -6.2), "exp(1 měsíc)", sim="exp(30 d)", param_pos="below")
net.loop("gen_l", "prichod_l")
net.place("lupic", (3, -6.2), label="lupič u banky", label_pos="above left")
net.arc("prichod_l", "lupic")
net.arc("lupic", "prepadeni_t")
net.immediate("vidi", (3, -7.8), p=1, label="vidí policistu", label_pos="below",
              param_pos="above left")
net.arc("lupic", "vidi")
net.place("odrazen", (1.5, -7.8), label="odražený lupič", label_pos="left")
net.arc("vidi", "odrazen")
net.immediate("odchod_o", (1.5, -9.2), exit=True, label="odchod", label_pos="left")
net.arc("odrazen", "odchod_o")
net.place("lupic_ven", (10.6, -6.2), label="lupič odchází", label_pos="below")
net.arc("lupic_pryc", "lupic_ven")
net.immediate("odchod_l", (12.1, -6.2), exit=True, label="odchod", label_pos="right")
net.arc("lupic_ven", "odchod_l")

# policista: obchůzka exp(2 h), u banky 3–5 min.
# Přítomnost policisty je samostatné místo, které testují „vidí policistu“ a „zlikvidování“;
# odpočet 3–5 min běží na místě „policista u banky“, které nikdo netestuje. Po odpočtu
# okamžitý „odchod policisty“ přítomnost zruší.
net.place("pritomen", (4.5, -7.8), label="policista přítomen", label_pos="below right")
net.loop("pritomen", "vidi", bend=20)
net.loop("pritomen", "likvidace", bend=20)
net.place("obchuzka", (4.5, -11), tokens=1, label="obchůzka", label_pos="left")
net.timed("prichod_p", (4.5, -9.4), "exp(2 h)", param_pos="left")
net.arc("obchuzka", "prichod_p")
net.arc("prichod_p", "pritomen")
net.place("u_banky", (6, -9.4), label="policista u banky", label_pos="below")
net.timed("odchod_p", (7.5, -9.4), "3–5 min", param_pos="above")
net.place("po_pobytu", (9, -9.4), label="pobyt skončil", label_pos="below")
net.immediate("odchod_pol", (10.5, -9.4), label="odchod policisty", label_pos="right")
net.chain("prichod_p", "u_banky", "odchod_p", "po_pobytu", "odchod_pol")
net.arc("pritomen", "odchod_pol", via=[(10.5, -7.8)])
net.arc("odchod_pol", "obchuzka", via=[(10.5, -11)])

net.invariant({"prepazka": 1, "obsluha": 1}, 1)
net.invariant({"gen": 1, "prepadeni": 1, "obnova": 1}, 1)
net.invariant({"prepadeni": 1, "prep_trva": -1, "po_prep": -1}, 0,
              name="přepadení = přepadení trvá + konec přepadení")
net.invariant({"obchuzka": 1, "pritomen": 1}, 1)
net.invariant({"pritomen": 1, "u_banky": -1, "po_pobytu": -1}, 0,
              name="policista přítomen = u banky + pobyt skončil")
net.bound("lupic", 1)
net.sim_events = 300000
