from pn import Net

net = Net("Obslužné centrum (půlsemestrálka 2025/26, varianta B – zadání rekonstruované)")

# hlavní řada: příchody a obsazení jedné ze tří linek
net.place("gen", (0, 0), tokens=1, label="příchody zákazníků", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(10 min)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta", label_pos="above")
net.place("linka", (4.5, 2.4), tokens=3, label="Linka", label_pos="left")
net.immediate("obsaz", (4.5, 0))
net.place("volba", (6, 0))
net.chain("prichod", "fronta", "obsaz", "volba")
net.arc("linka", "obsaz")

# if–else: ve dne nahoru, v noci (p=1) dolů
net.immediate("ve_dne", (7.5, 1.5))
net.place("obsl_den", (9, 1.5))
net.timed("den_obsl", (10.5, 1.5), "exp(5 min)", param_pos="below")
net.arc("volba", "ve_dne", via=[(6, 1.5)], corner=20)
net.chain("ve_dne", "obsl_den", "den_obsl")
net.immediate("v_noci", (7.5, -1.5), p=1, param_pos="above")
net.place("obsl_noc", (9, -1.5))
net.timed("noc_obsl", (10.5, -1.5), "exp(10 min)", param_pos="above")
net.arc("volba", "v_noci", via=[(6, -1.5)], corner=20)
net.chain("v_noci", "obsl_noc", "noc_obsl")
# návrat linky: z denní obsluhy oblouk, z noční obchází síť zprava a shora
net.arc("den_obsl", "linka", out=90, into=0)
net.arc("noc_obsl", "linka", via=[(10.5, -2.4), (14.6, -2.4), (14.6, 3.6), (4.5, 3.6)])

# odchod
net.place("konec", (12, 0), label="konec", label_pos="left")
net.immediate("odchod", (13.5, 0), exit=True, label="odchod")
net.arc("den_obsl", "konec", via=[(12, 1.5)], corner=20)
net.arc("noc_obsl", "konec", via=[(12, -1.5)], corner=20)
net.arc("konec", "odchod")

# proces den/noc
net.place("je_noc", (7.5, -3.2), label="je noc", label_pos="below right")
net.loop("je_noc", "v_noci", bend=25)
net.place("den", (4.5, -4.8), tokens=1, label="den", label_pos="above")
net.timed("den_16h", (6, -4.8), "16 h", param_pos="below")
net.place("noc", (7.5, -4.8), label="noc", label_pos="below")
net.timed("noc_8h", (9, -4.8), "8 h", param_pos="below")
net.place("rano", (10.5, -4.8), label="ráno", label_pos="below")
net.immediate("konec_noci", (12, -4.8), p=2, label="konec noci", label_pos="right",
              param_pos="above right")
net.chain("den", "den_16h", "noc", "noc_8h", "rano", "konec_noci")
net.arc("den_16h", "je_noc", via=[(6, -3.2)])
net.arc("je_noc", "konec_noci", via=[(12, -3.2)])
net.arc("konec_noci", "den", via=[(12, -6.1), (4.5, -6.1)])

net.invariant({"linka": 1, "volba": 1, "obsl_den": 1, "obsl_noc": 1}, 3)
net.invariant({"den": 1, "noc": 1, "rano": 1}, 1)
net.invariant({"den": 1, "je_noc": 1}, 1)
net.bound("je_noc", 1)
