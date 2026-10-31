from pn import Net

net = Net("09–12", "Pošta (půlsemestrálky 2014–19, Z19)")

# příchody klientů
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(5 min)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta", label_pos="above left")
net.arc("prichod", "fronta")

# přepážka A: pošťák
net.place("postak", (4.5, 3.6), tokens=1, label="Pošťák", label_pos="left")
net.immediate("obsaz_a", (4.5, 2), p=1, param_pos="left")
net.place("obsluha_a", (6, 2))
net.timed("podani_a", (7.5, 2), "exp(3 min)")
net.arc("fronta", "obsaz_a")
net.chain("obsaz_a", "obsluha_a", "podani_a")
net.arc("postak", "obsaz_a")
net.arc("podani_a", "postak", bend=-25)

# přepážka B: řidič, když ji otevře
net.place("u_b", (4.5, -3.6), label="Řidič u B", label_pos="below left")
net.immediate("obsaz_b", (4.5, -2), p=1, param_pos="left")
net.place("obsluha_b", (6, -2))
net.timed("podani_b", (7.5, -2), "exp(3 min)", param_pos="above")
net.arc("fronta", "obsaz_b")
net.chain("obsaz_b", "obsluha_b", "podani_b")
net.arc("u_b", "obsaz_b")
net.arc("podani_b", "u_b", bend=25)

# klient odchází, jeho zásilka zůstává na poště
net.place("obslouzen", (9, 0))
net.arc("podani_a", "obslouzen")
net.arc("podani_b", "obslouzen")
net.immediate("predani", (10.5, 0), label="podání zásilky", label_pos="above right")
net.place("klient_odchazi", (12, 0))
net.immediate("odchod", (13.5, 0), exit=True, label="odchod", label_pos="above")
net.chain("obslouzen", "predani", "klient_odchazi", "odchod")
net.place("zasilky", (10.5, -2.2), label="Podané zásilky", label_pos="right")
net.arc("predani", "zasilky")

# řidič otevře B, když fronta dosáhne 3; odejde, když je fronta prázdná (p=0 < obsazení p=1)
net.place("ridic", (2.4, -5.2), tokens=1, label="Řidič volný", label_pos="left")
net.immediate("otevreni", (2.4, -3.6), label="otevření B", label_pos="left")
net.arc("ridic", "otevreni")
net.arc("fronta", "otevreni", w=3, bend=10, w_pos="left")
net.arc("otevreni", "fronta", w=3, bend=10, w_pos="left")
net.arc("otevreni", "u_b")
net.immediate("zavreni", (3.6, -5.2), horizontal=True, label="zavření B", label_pos="below")
net.arc("u_b", "zavreni")
net.arc("zavreni", "ridic")

# odvoz 100 zásilek: řidič je primárně určen pro náklad (p=2 / p=1)
net.immediate("nalozeni_b", (6.3, -4.2), p=2, horizontal=True, param_pos="below left")
net.arc("u_b", "nalozeni_b")
net.arc("zasilky", "nalozeni_b", w=100, w_pos="left")
net.immediate("nalozeni", (9, -6.8), p=1, horizontal=True, label="naložení", label_pos="right",
              param_pos="above right")
net.arc("ridic", "nalozeni", via=[(2.4, -8.2), (9, -8.2)])
net.arc("zasilky", "nalozeni", w=100, w_pos="right")
net.place("naklada", (7.5, -5.2), label="nakládá", label_pos="right")
net.arc("nalozeni_b", "naklada")
net.arc("nalozeni", "naklada")
net.timed("nakladani", (6, -5.2), "30 min", param_pos="left")
net.place("veze", (6, -6.8), label="veze do Centrály", label_pos="below")
net.timed("cesta", (4.5, -6.8), "2 h", param_pos="below")
net.chain("naklada", "nakladani", "veze", "cesta", "ridic")

net.invariant({"postak": 1, "obsluha_a": 1}, 1)
net.invariant({"ridic": 1, "u_b": 1, "obsluha_b": 1, "naklada": 1, "veze": 1}, 1)
