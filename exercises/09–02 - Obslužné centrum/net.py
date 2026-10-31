from pn import Net

net = Net("09–02", "Obslužné centrum (půlsemestrálka 2025/26, varianta B – zadání rekonstruované)")

# příchody a obsazení jedné ze tří linek
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(10 min)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta")
net.place("linka", (4.5, 1.8), tokens=3, label="Linka", label_pos="left")
net.immediate("obsaz", (4.5, 0))
net.place("volba", (6, 0))
net.chain("prichod", "fronta", "obsaz", "volba")
net.arc("linka", "obsaz")

# if–else: v noci pomalejší obsluha
net.immediate("ve_dne", (7.5, 1.2))
net.place("obsl_den", (9, 1.2))
net.timed("den_obsl", (10.5, 1.2), "exp(5 min)")
net.chain("volba", "ve_dne", "obsl_den", "den_obsl")
net.immediate("v_noci", (7.5, -1.2), p=1, param_pos="above right")
net.place("obsl_noc", (9, -1.2))
net.timed("noc_obsl", (10.5, -1.2), "exp(10 min)")
net.chain("volba", "v_noci", "obsl_noc", "noc_obsl")
net.arc("den_obsl", "linka", bend=-20)
net.arc("noc_obsl", "linka", via=[(11.4, -1.2), (11.4, 2.8), (4.5, 2.8)])

# odchod
net.place("konec", (12.6, 0), label="konec", label_pos="below")
net.immediate("odchod", (14.1, 0), exit=True, label="odchod")
net.arc("den_obsl", "konec")
net.arc("noc_obsl", "konec")
net.arc("konec", "odchod")

# proces den/noc
net.place("je_noc", (7.5, -2.8), label="je noc", label_pos="left")
net.loop("je_noc", "v_noci", bend=25)
net.place("den", (5, -4.4), tokens=1, label="den", label_pos="above")
net.timed("den_16h", (6.5, -4.4), "16 h")
net.place("noc", (8, -4.4), label="noc", label_pos="below")
net.timed("noc_8h", (9.5, -4.4), "8 h")
net.place("rano", (11, -4.4), label="ráno", label_pos="below")
net.immediate("konec_noci", (12.5, -4.4), p=2, label="konec noci", label_pos="below right", param_pos="above right")
net.chain("den", "den_16h", "noc", "noc_8h", "rano", "konec_noci")
net.arc("den_16h", "je_noc")
net.arc("je_noc", "konec_noci", via=[(12.5, -2.8)])
net.arc("konec_noci", "den", via=[(12.5, -5.6), (5, -5.6)])

net.invariant({"linka": 1, "volba": 1, "obsl_den": 1, "obsl_noc": 1}, 3)
net.invariant({"den": 1, "noc": 1, "rano": 1}, 1)
net.invariant({"den": 1, "je_noc": 1}, 1)
net.bound("je_noc", 1)
