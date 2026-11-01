from pn import Net

net = Net("Přečerpávací elektrárna (půlsemestrálky 2014–19, Z3)")

# nádrže a přesuny vody; režim (denní / noční / havarijní) je značka, přesun ji testuje.
# Denní přesun vede horem, havarijní dolem; noční přesun stojí vpravo od B, aby místo
# „noční provoz“ nebylo uzavřené mezi přesuny. Jeho hrana zpět do A jediná kříží jinou hranu.
net.place("A", (0, -1.4), tokens=500, label="A", label_pos="left")
net.place("B", (9, 0), tokens=500, label="B", label_pos="left")
net.place("den_p", (4.5, 4.4), tokens=1, label="denní provoz", label_pos="above left")
net.timed("t_den", (4.5, 2.8), "4 min", param_pos="below")
net.loop("den_p", "t_den", bend=30)
net.arc("A", "t_den", via=[(0, 2.8)])
net.arc("t_den", "B", via=[(9, 2.8)])
net.place("noc_p", (12, 0), label="noční provoz", label_pos="below")
net.timed("t_noc", (10.5, 0), "1 min", param_pos="above")
net.loop("noc_p", "t_noc", bend=30)
net.arc("B", "t_noc")
net.arc("t_noc", "A", via=[(10.5, -1.4)])
net.place("hav_p", (4.5, -4.4), label="havarijní provoz", label_pos="right")
net.timed("t_hav", (4.5, -2.8), "1 min", param_pos="above")
net.loop("hav_p", "t_hav", bend=30)
net.arc("A", "t_hav", via=[(0, -2.8)])
net.arc("t_hav", "B", via=[(9, -2.8)])

# hodiny: den 16 h, noc 8 h; konec dne / noci je signál pro přepnutí režimu
net.place("den", (6, 7.2), tokens=1, label="den", label_pos="left")
net.timed("t16", (7.5, 7.2), "16 h", param_pos="above")
net.place("noc", (9, 7.2), label="noc", label_pos="below")
net.timed("t8", (10.5, 7.2), "8 h", param_pos="below")
net.arc("den", "t16")
net.arc("t16", "noc")
net.arc("noc", "t8")
net.arc("t8", "den", via=[(10.5, 8.6), (6, 8.6)])
net.place("sig_noc", (7.5, 5.8), label="konec dne", label_pos="left")
net.arc("t16", "sig_noc")
net.place("sig_den", (12, 7.2), label="konec noci", label_pos="above")
net.arc("t8", "sig_den")

# přepnutí na noc a na den
net.immediate("na_noc", (10.5, 4.4), label="na noc", label_pos="below")
net.arc("den_p", "na_noc")
net.arc("sig_noc", "na_noc", via=[(10.5, 5.8)])
net.arc("na_noc", "noc_p", via=[(12, 4.4)])
net.immediate("na_den", (14, 0), label="na den", label_pos="below")
net.arc("noc_p", "na_den")
net.arc("sig_den", "na_den", via=[(14, 7.2)])

# do denního provozu se vrací přes místo „návrat ke dni“ (z noci i po havárii)
net.place("ke_dni", (15.5, 0), label="návrat ke dni", label_pos="right")
net.immediate("do_dne", (9, 10))
net.arc("ke_dni", "do_dne", via=[(15.5, 10)])
net.arc("do_dne", "den_p", via=[(4.5, 10)])
net.arc("na_den", "ke_dni")

# havárie: jen v běžném denním provozu zvýší výrobu na 3 h, jinak bez účinku
net.place("gen_h", (-6, -4.4), tokens=1, label="příchody havárií", label_pos="above")
net.timed("vznik", (-4.5, -4.4), "exp(100 d)", param_pos="below")
net.loop("gen_h", "vznik")
net.place("havarie", (-3, -4.4), label="havárie", label_pos="below")
net.arc("vznik", "havarie")
net.immediate("bez_ucinku", (-3, -2.8), label="bez účinku", label_pos="left")
net.arc("havarie", "bez_ucinku")
net.immediate("zvyseni", (-1.5, -4.4), p=1, label="zvýšení výroby", label_pos="above right",
              param_pos="below right")
net.arc("havarie", "zvyseni")
net.arc("den_p", "zvyseni", via=[(-1.5, 4.4)])
net.arc("zvyseni", "hav_p")
net.place("trvani", (0, -6))
net.timed("t3", (1.5, -6), "3 h", param_pos="below")
net.place("konec_h", (3, -6))
net.arc("zvyseni", "trvani", via=[(-1.5, -6)])
net.chain("trvani", "t3", "konec_h")
net.immediate("navrat", (4.5, -6), label="návrat", label_pos="below")
net.arc("konec_h", "navrat")
net.arc("hav_p", "navrat")
net.arc("navrat", "ke_dni", via=[(15.5, -6)])

net.closed = True  # voda jen obíhá mezi nádržemi, žádná transakce systém neopouští
net.invariant({"A": 1, "B": 1}, 1000)
net.bound("A", 1000)  # kapacita nádrží se nikdy nepřekročí
net.bound("B", 1000)
net.invariant({"den": 1, "noc": 1}, 1)
net.invariant({"den_p": 1, "noc_p": 1, "hav_p": 1, "ke_dni": 1}, 1, name="právě jeden režim")
net.invariant({"hav_p": 1, "trvani": -1}, 0, name="havarijní provoz = běží 3 h")
net.bound("ke_dni", 0)
net.bound("sig_noc", 1)
net.bound("sig_den", 1)
net.bound("havarie", 0)
# havárie exp(100 d), přesuny po 1–4 min: ~500 událostí za den, ~600 dní simulace
net.sim_events = 300000
