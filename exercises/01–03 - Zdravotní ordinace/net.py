from pn import Net

net = Net("01–03", "Zdravotní ordinace (poznámky MSI, stochastické PN, obr. 6)")

# příchody a kartotéka
net.place("gen", (0, 0), tokens=1, label="příchody pacientů", label_pos="below")
net.timed("prichod", (1.5, 0), "exp(12 min)", param_pos="above")
net.loop("gen", "prichod")
net.place("fronta_K", (3, 0), label="fronta", label_pos="below")
net.place("kartoteka", (4.5, 1.6), tokens=1, label="Kartotéka", label_pos="above")
net.immediate("obsaz_K", (4.5, 0))
net.place("v_kartotece", (6, 0))
net.timed("kart", (7.5, 0), "40–150 s", param_pos="below")
net.chain("prichod", "fronta_K", "obsaz_K", "v_kartotece", "kart")
net.arc("kartoteka", "obsaz_K")
net.arc("kart", "kartoteka", out=90, into=0)  # zakřivená, z přechodu odchází nahoru
net.place("po_kartotece", (9, 0))
net.arc("kart", "po_kartotece")

# 25 % rovně k lékaři, 75 % nahoru do laboratoře
net.immediate("k_lekari_1", (10.5, 0), prob=25, param_pos="below")
net.immediate("do_lab", (10.5, 2.6), prob=75)
net.arc("po_kartotece", "k_lekari_1")
net.arc("po_kartotece", "do_lab", via=[(9, 2.6)], corner=20)
net.place("fronta_L", (12, 2.6), label="fronta", label_pos="below")
net.place("laborator", (13.5, 4.2), tokens=1, label="Laboratoř", label_pos="above")
net.immediate("obsaz_L", (13.5, 2.6))
net.place("v_lab", (15, 2.6))
net.timed("odber", (16.5, 2.6), "exp(6 min)", param_pos="below")
net.chain("do_lab", "fronta_L", "obsaz_L", "v_lab", "odber")
net.arc("laborator", "obsaz_L")
net.arc("odber", "laborator", out=90, into=0)
net.place("po_odberu", (18, 2.6))
net.arc("odber", "po_odberu")

# po odběru 50 % pokračuje rovně k lékaři, 50 % nahoru odchází
net.immediate("k_lekari_2", (19.5, 2.6), prob=50, param_pos="below")
net.immediate("odchod_lab", (19.5, 4.2), prob=50, exit=True, label="odchází", label_pos="right")
net.arc("po_odberu", "k_lekari_2")
net.arc("po_odberu", "odchod_lab", via=[(18, 4.2)], corner=20)

# lékař: fronta bere pacienty zleva (z kartotéky) a shora (z laboratoře)
net.place("fronta_D", (21, 0), label="fronta", label_pos="below")
net.arc("k_lekari_1", "fronta_D")
net.arc("k_lekari_2", "fronta_D", via=[(21, 2.6)], corner=20)
net.place("lekar", (22.5, 1.6), tokens=1, label="Lékař", label_pos="above")
net.immediate("obsaz_D", (22.5, 0))
net.place("u_lekare", (24, 0))
net.timed("vysetreni", (25.5, 0), "8–25 min", param_pos="below")
net.chain("fronta_D", "obsaz_D", "u_lekare", "vysetreni")
net.arc("lekar", "obsaz_D")
net.arc("vysetreni", "lekar", out=90, into=0)
net.place("konec", (27, 0))
net.immediate("odchod", (28.5, 0), exit=True, label="odchod")
net.chain("vysetreni", "konec", "odchod")

net.invariant({"kartoteka": 1, "v_kartotece": 1}, 1)
net.invariant({"laborator": 1, "v_lab": 1}, 1)
net.invariant({"lekar": 1, "u_lekare": 1}, 1)
