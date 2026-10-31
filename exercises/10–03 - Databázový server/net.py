from pn import Net

net = Net("10–03", "Databázový server (půlsemestrálky 2014–19, Z22)", unit="s")

# příchody požadavků; z fronty je obsluhuje proces A (nahoře) nebo aktivní proces B (dole)
net.place("gen", (0, 0), tokens=1, label="příchody požadavků", label_pos="below")
net.timed("prichod", (1.5, 0), "exp(1 s)", param_pos="above")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="fronta", label_pos="below left")
net.arc("prichod", "fronta")

for row, y in (("a", 1.8), ("b", -1.8)):
    up = y > 0
    net.immediate(f"obsaz_{row}", (4.5, y))
    net.place(f"obsluha_{row}", (6, y))
    net.timed(f"vyrizeni_{row}", (7.5, y), "exp(0,5 s)", param_pos="below" if up else "above")
    net.arc("fronta", f"obsaz_{row}", via=[(3, y)], corner=20)
    net.chain(f"obsaz_{row}", f"obsluha_{row}", f"vyrizeni_{row}")

# proces A je mezi řadami (horní stranou jeho obsluha přidává do čítače), proces B pod nimi
net.place("a", (4.5, 0), tokens=1, label="proces A", label_pos="below right")
net.arc("a", "obsaz_a")
net.arc("vyrizeni_a", "a", out=270, into=0)
net.place("b", (4.5, -3.6), label="proces B aktivní", label_pos="below right")
net.arc("b", "obsaz_b")
net.arc("vyrizeni_b", "b", out=270, into=0)

net.place("konec", (9, 0), label="vyřízeno", label_pos="left")
net.immediate("odchod", (10.5, 0), exit=True, label="odchod", label_pos="above")
net.arc("vyrizeni_a", "konec", via=[(9, 1.8)], corner=20)
net.arc("vyrizeni_b", "konec", via=[(9, -1.8)], corner=20)
net.arc("konec", "odchod")

# proces S: minutu počítá dokončené obsluhy procesu A, pak vyhodnotí a čítač vynuluje
net.place("citac", (7.5, 3.6), label="obslouženo A", label_pos="left")
net.arc("vyrizeni_a", "citac")
net.place("s_pocita", (4.5, 7.2), tokens=1, label="S počítá", label_pos="below")
net.timed("minuta", (13, 3.6), "1 min", param_pos="right")
net.arc("s_pocita", "minuta", via=[(4.5, 9.6), (13, 9.6)])
net.place("s_vyhodnoti", (11.5, 3.6), label="S vyhodnocuje", label_pos="below")
net.arc("minuta", "s_vyhodnoti")
net.immediate("naplanuj", (9.5, 3.6), p=1, label="naplánuj B", label_pos="above right",
              param_pos="below right")
net.immediate("nenaplanuj", (11.5, 5.4), label="jinak", label_pos="right")
net.arc("s_vyhodnoti", "naplanuj")
net.arc("s_vyhodnoti", "nenaplanuj")
net.arc("citac", "naplanuj", w=70, w_pos="above")
net.place("s_nuluje", (7.5, 7.2), label="S nuluje", label_pos="above right")
net.arc("naplanuj", "s_nuluje", via=[(9.5, 7.2)])
net.arc("nenaplanuj", "s_nuluje", via=[(11.5, 8.4), (7.5, 8.4)])
net.immediate("nulovani", (7.5, 5.4), p=1, label="vynulování", label_pos="left",
              param_pos="right")
net.arc("citac", "nulovani")
net.loop("s_nuluje", "nulovani", bend=20)
net.immediate("novy_cyklus", (6, 7.2), label="nový cyklus", label_pos="above")
net.arc("s_nuluje", "novy_cyklus")
net.arc("novy_cyklus", "s_pocita")

# aktivace procesu B na 1 min (plán počká, když B právě běží)
net.place("plan", (6.5, -5.4), label="B naplánován", label_pos="above")
net.arc("naplanuj", "plan", via=[(9.5, 2.6), (14.5, 2.6), (14.5, -5.4)])
net.place("b_spi", (3, -5.4), tokens=1, label="B čeká", label_pos="left")
net.immediate("aktivace", (4.5, -5.4), label="aktivace B", label_pos="below right")
net.arc("plan", "aktivace")
net.arc("b_spi", "aktivace")
net.arc("aktivace", "b")
net.place("b_bezi", (4.5, -7.2), label="B běží", label_pos="below")
net.arc("aktivace", "b_bezi")
net.timed("b_minuta", (6, -7.2), "1 min", param_pos="below")
net.place("b_konci", (7.5, -7.2), label="minuta uplynula", label_pos="right")
net.chain("b_bezi", "b_minuta", "b_konci")
net.immediate("deaktivace", (3, -3.6), p=1, label="deaktivace B", label_pos="above left",
              param_pos="below left")
net.arc("b_konci", "deaktivace", via=[(7.5, -8.6), (1.5, -8.6), (1.5, -3.6)])
net.arc("b", "deaktivace")
net.arc("deaktivace", "b_spi")

net.invariant({"a": 1, "obsluha_a": 1}, 1)
net.invariant({"b_spi": 1, "b": 1, "obsluha_b": 1}, 1)
net.invariant({"s_pocita": 1, "s_vyhodnoti": 1, "s_nuluje": 1}, 1)
net.sim_events = 200000
