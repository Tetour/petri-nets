from pn import Net

net = Net("Přečerpávací elektrárna II (půlsemestrálky 2014–19, Z11)")

# nádrže a přesun vody po jednotkách (kruh B → A → B); režim testují hrany tam a zpět
net.place("B", (0, 0), tokens=600, label="nádrž B", label_pos="above")
net.place("A", (4, 0), tokens=0, label="nádrž A", label_pos="above")
net.timed("spousteni", (2, 0), "2 min", param_pos="below")
net.chain("B", "spousteni", "A")
net.timed("cerp", (2, -2), "1 min", param_pos="above")
net.arc("A", "cerp", via=[(4, -2)])
net.arc("cerp", "B", via=[(0, -2)])
net.place("vyroba", (2, 1.6), tokens=1, label="Výroba", label_pos="above")
net.loop("vyroba", "spousteni")
net.place("cerpani", (2, -3.6), label="Čerpání", label_pos="below right")
net.loop("cerpani", "cerp")

# přepnutí režimu na signál: kolem nádrží po směru hodin (výroba → čerpání vpravo, zpět vlevo)
net.place("na_cerpani", (7.2, -0.8), label="na čerpání", label_pos="right")
net.immediate("prepni_c", (5.6, -0.8), label="přepni", label_pos="left")
net.arc("na_cerpani", "prepni_c")
net.arc("vyroba", "prepni_c", via=[(5.6, 1.6)])
net.arc("prepni_c", "cerpani", via=[(5.6, -3.6)])
net.place("na_vyrobu", (-3.2, -0.8), label="na výrobu", label_pos="left")
net.immediate("prepni_v", (-1.6, -0.8), label="přepni", label_pos="right")
net.arc("na_vyrobu", "prepni_v")
net.arc("cerpani", "prepni_v", via=[(-1.6, -3.6)])
net.arc("prepni_v", "vyroba", via=[(-1.6, 1.6)])

# denní doba nahoře: den 16 h, noc 8 h (časovače v jiných místech než testovaný režim)
net.place("den", (1.2, 3.4), tokens=1, label="den", label_pos="left")
net.timed("t16", (2.8, 3.4), "16 h", param_pos="above")
net.place("noc", (4.4, 3.4), label="noc", label_pos="right")
net.timed("t8", (2.8, 5.4), "8 h", param_pos="below")
net.chain("den", "t16", "noc")
net.arc("noc", "t8", via=[(4.4, 5.4)])
net.arc("t8", "den", via=[(1.2, 5.4)])
net.arc("t16", "na_cerpani", via=[(2.8, 2.4), (7.2, 2.4)])
net.arc("t8", "na_vyrobu", via=[(2.8, 6.2), (-3.2, 6.2)])

# havárie exp(10 d) dole: v noci (p=1, je režim čerpání) přepne na výrobu na 1 h, ve dne (p=0) nic
net.place("gen_h", (-1, -6.8), tokens=1, label="příchody havárií", label_pos="below")
net.timed("vznik", (0.5, -6.8), "exp(10 d)", param_pos="above")
net.loop("gen_h", "vznik")
net.place("havarie", (2, -6.8), label="havárie", label_pos="below")
net.arc("vznik", "havarie")
net.immediate("v_noci", (2, -5.2), p=1, param_pos="below left")
net.arc("havarie", "v_noci")
net.loop("cerpani", "v_noci")
net.immediate("ve_dne", (3.5, -6.8), label="ve dne: bez účinku", label_pos="right")
net.arc("havarie", "ve_dne")
net.arc("v_noci", "na_vyrobu", via=[(-3.2, -5.2)])
net.place("trva", (3.5, -5.2), label="havárie trvá", label_pos="below")
net.timed("hodina", (5.2, -5.2), "1 h", param_pos="below")
net.chain("v_noci", "trva", "hodina")
net.arc("hodina", "na_cerpani", via=[(7.2, -5.2)])

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
