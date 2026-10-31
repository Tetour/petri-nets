from pn import Net

net = Net("12–09", "Přečerpávací elektrárna II (půlsemestrálky 2014–19, Z11)")

# nádrže a přesun vody po jednotkách; režim (výroba / čerpání) testují hrany tam a zpět
net.place("B", (3, 0), tokens=600, label="nádrž B", label_pos="below left")
net.place("A", (9, 0), tokens=0, label="nádrž A", label_pos="below right")
net.place("vyroba", (6, 0), tokens=1, label="Výroba", label_pos="left")
net.timed("spousteni", (6, 1.4), "2 min", horizontal=True, param_pos="above")
net.arc("B", "spousteni")
net.arc("spousteni", "A")
net.loop("vyroba", "spousteni", bend=25)
net.place("cerpani", (6, 4.2), label="Čerpání", label_pos="below left")
net.timed("cerp", (6, 2.8), "1 min", horizontal=True, param_pos="left")
net.arc("A", "cerp")
net.arc("cerp", "B")
net.loop("cerpani", "cerp", bend=25)

# přepnutí režimu na signál
net.place("na_cerpani", (-0.6, 2.1), label="na čerpání", label_pos="left")
net.immediate("prepni_c", (0.8, 2.1), label="přepni", label_pos="right")
net.arc("na_cerpani", "prepni_c")
net.arc("vyroba", "prepni_c", via=[(5.6, -1.3), (0.8, -1.3)])
net.arc("prepni_c", "cerpani", via=[(0.8, 4.2)])
net.place("na_vyrobu", (12.6, 2.1), label="na výrobu", label_pos="right")
net.immediate("prepni_v", (11.2, 2.1), label="přepni", label_pos="left")
net.arc("na_vyrobu", "prepni_v")
net.arc("cerpani", "prepni_v", via=[(11.2, 4.2)])
net.arc("prepni_v", "vyroba", via=[(11.2, -1.3), (6.4, -1.3)])

# denní doba: den 16 h, noc 8 h (časovače v jiných místech než testovaný režim)
net.place("den", (6, -2.6), tokens=1, label="den", label_pos="above right")
net.timed("t16", (3, -3.5), "16 h", param_pos="above")
net.place("noc", (6, -4.4), label="noc", label_pos="below right")
net.timed("t8", (9, -3.5), "8 h", param_pos="above")
net.chain("den", "t16", "noc", "t8", "den")
net.arc("t16", "na_cerpani", via=[(-0.6, -3.5)])
net.arc("t8", "na_vyrobu", via=[(12.6, -3.5)])

# havárie exp(10 d): v noci (p=1, je režim čerpání) přepne na výrobu na 1 h, ve dne (p=0) nic
net.place("gen_h", (9, 7), tokens=1, label="generátor havárií", label_pos="right")
net.timed("vznik", (7.5, 7), "exp(10 d)", param_pos="above")
net.loop("gen_h", "vznik")
net.place("havarie", (6, 7), label="havárie", label_pos="above")
net.arc("vznik", "havarie")
net.immediate("v_noci", (6, 5.6), p=1, horizontal=True, param_pos="above right")
net.arc("havarie", "v_noci")
net.loop("cerpani", "v_noci", bend=25)
net.immediate("ve_dne", (4.5, 7), label="ve dne: bez účinku", label_pos="left")
net.arc("havarie", "ve_dne")
net.arc("v_noci", "na_vyrobu", via=[(12.6, 5.6)])
net.place("trva", (4.5, 5.6), label="havárie trvá", label_pos="below")
net.timed("hodina", (3, 5.6), "1 h", param_pos="above")
net.chain("v_noci", "trva", "hodina")
net.arc("hodina", "na_cerpani", via=[(-0.6, 5.6)])

net.invariant({"A": 1, "B": 1}, 600, name="A + B = 600 (voda se jen přelévá)")
net.invariant({"vyroba": 1, "cerpani": 1}, 1)
net.invariant({"den": 1, "noc": 1}, 1)
net.bound("A", 600)  # kapacita nádrží: díky A + B = 600 se nikdy nepřekročí
net.bound("B", 600)
net.bound("na_vyrobu", 1)
net.bound("na_cerpani", 1)
net.bound("trva", 1)
# voda systém neopouští, transakce tu nejsou: síť nemá výstupní přechod
net.closed = True
net.sim_events = 300000
