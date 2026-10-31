from pn import Net

net = Net("11–12", "Přehrada s přístavišti (půlsemestrálka 2011/12, příklad 3)")

# turisté na přístavišti A; na loď čekají nejvýš 20 min (každý vlastní odpočet)
net.place("gen", (0, 0), tokens=1, label="příchody turistů", label_pos="below")
net.timed("prichod", (1.5, 0), "exp(2 min)", param_pos="above")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="fronta", label_pos="below left")
net.arc("prichod", "fronta")
net.timed("netrp", (3, -1.6), "20 min", param_pos="left")
net.arc("fronta", "netrp")
net.place("odchazi", (3, -3.2), label="odcházejí", label_pos="left")
net.immediate("odchod", (3, -4.6), exit=True, label="odchod", label_pos="left")
net.chain("netrp", "odchazi", "odchod")

# u mola stojí loď a nikdo nenastupuje (test „nástup volný“): čekající přejdou k nástupu
net.immediate("na_molo", (4.5, 1.6), p=1, param_pos="above left")
net.arc("fronta", "na_molo", via=[(3, 1.6)])
net.place("nf", (4.5, 0), label="k nástupu", label_pos="above right")
net.arc("na_molo", "nf")

# nástup po jednom 20–30 s; „nástup volný“ vzniká přistáním lodi
net.place("nastup", (7, 1.6), label="nástup volný", label_pos="below left")
net.loop("nastup", "na_molo", bend=20)
net.immediate("obsaz", (7, 0))
net.place("nastupuje", (8.5, 0))
net.timed("t_nastup", (10, 0), "20–30 s", param_pos="below")
net.place("paluba", (11.5, 0), label="na palubě", label_pos="below right")
net.chain("nf", "obsaz", "nastupuje", "t_nastup", "paluba")
net.arc("nastup", "obsaz")
net.arc("t_nastup", "nastup", out=90, into=315)

# lodě: první příjezd po exp(3 h); přístaviště A má kapacitu 1
net.place("start", (-1.5, 5.0), tokens=2, label="lodě na začátku", label_pos="below")
net.timed("t_start", (0, 5.0), "exp(3 h)", param_pos="above")
net.place("ceka_a", (1.5, 5.0), label="loď čeká na A", label_pos="below")
net.chain("start", "t_start", "ceka_a")
net.place("molo_a", (3, 6.6), tokens=1, label="přístaviště A volné", label_pos="left")
net.immediate("pristani", (3, 5.0))
net.arc("ceka_a", "pristani")
net.arc("molo_a", "pristani")
net.arc("pristani", "nastup", via=[(3, 3.2), (7, 3.2)])
net.place("odpocet", (4.5, 5.0))
net.timed("t_15", (6.5, 5.0), "15 min", param_pos="above")
net.place("vyprselo", (8.5, 5.0))
net.chain("pristani", "odpocet", "t_15", "vyprselo")
# po odjezdu plné lodi ještě běží odpočet 15 min: zrušit ho, než přistane další loď
net.immediate("zrus", (4.5, 6.6), p=1, label="zruš odpočet", label_pos="above",
              param_pos="right")
net.arc("odpocet", "zrus")
net.loop("molo_a", "zrus", bend=20)

# odjezd po 15 min (p=1) nebo s plnou lodí (p=1, test 50 na palubě);
# obojí bere „nástup volný“, takže nastupující turista smí dokončit nástup
net.immediate("cas", (8.5, 3.4), p=1, label="po 15 min", label_pos="left",
              param_pos="below right")
net.arc("vyprselo", "cas")
net.arc("nastup", "cas", out=45, into=270)
net.immediate("plna", (11.5, 1.6), p=1, label="plná loď", label_pos="right",
              param_pos="above left")
net.arc("nastup", "plna")
net.loop("paluba", "plna", w=50, bend=20)
net.place("odplouva", (11.5, 3.4), label="odplouvá", label_pos="above")
net.arc("cas", "odplouva")
net.arc("plna", "odplouva")
net.immediate("odpluti", (13.5, 3.4))
net.arc("odplouva", "odpluti")
net.arc("odpluti", "molo_a", via=[(13.5, 7.8), (3, 7.8)])

# s odplutím: turisté na palubě jedou (dál je nesledujeme), neobsloužení odcházejí;
# úklid (p=2) proběhne celý dřív, než „hotovo“ (p=1) zruší značku a přistane další loď
net.place("odplula", (13.5, -1.6), label="loď odplula", label_pos="below right")
net.arc("odpluti", "odplula")
net.immediate("jedou_t", (11.5, -1.6), p=2, param_pos="below")
net.arc("paluba", "jedou_t")
net.loop("odplula", "jedou_t", bend=20)
net.place("jedou", (10, -1.6), label="na vyhlídce", label_pos="below")
net.immediate("vyhlidka", (8.5, -1.6), exit=True, label="odchod", label_pos="below")
net.chain("jedou_t", "jedou", "vyhlidka")
net.immediate("vycisti", (13.5, -3.2), p=2, label="vyčisti", label_pos="left",
              param_pos="above left")
net.arc("nf", "vycisti", via=[(4.5, -4.6), (13.5, -4.6)])
net.loop("odplula", "vycisti", bend=20)
net.place("neobslouzeni", (15, -3.2), label="neobsloužení", label_pos="below")
net.immediate("odchod_n", (16.5, -3.2), exit=True, label="odchod", label_pos="right")
net.chain("vycisti", "neobslouzeni", "odchod_n")
net.immediate("konec_o", (16, -1.6), p=1, label="hotovo", label_pos="right")
net.arc("odplula", "konec_o")

# plavba do B 30–40 min, výstup 5 min (přístaviště B s kapacitou 1), zpět 20 min
net.place("plavba", (15, 3.4), label="plavba", label_pos="below")
net.arc("odpluti", "plavba")
net.timed("t_plavba", (16.5, 3.4), "30–40 min", param_pos="below")
net.place("ceka_b", (18, 3.4), label="loď čeká na B", label_pos="above")
net.chain("plavba", "t_plavba", "ceka_b")
net.place("molo_b", (19.5, 5.0), tokens=1, label="přístaviště B volné", label_pos="above")
net.immediate("pristani_b", (19.5, 3.4))
net.place("vystup", (21, 3.4), label="výstup", label_pos="below")
net.timed("t_vystup", (22.5, 3.4), "5 min", param_pos="below")
net.chain("ceka_b", "pristani_b", "vystup", "t_vystup")
net.arc("molo_b", "pristani_b")
net.arc("t_vystup", "molo_b", out=90, into=0)
net.place("zpet", (24, 3.4), label="cesta do A", label_pos="below")
net.timed("t_zpet", (25.5, 3.4), "20 min", param_pos="below")
net.chain("t_vystup", "zpet", "t_zpet")
net.arc("t_zpet", "ceka_a", via=[(25.5, 8.6), (1.5, 8.6)])

net.invariant({"molo_a": 1, "nastup": 1, "nastupuje": 1, "odplouva": 1}, 1)
net.invariant({"start": 1, "ceka_a": 1, "nastup": 1, "nastupuje": 1, "odplouva": 1,
               "plavba": 1, "ceka_b": 1, "vystup": 1, "zpet": 1}, 2)
net.invariant({"molo_b": 1, "vystup": 1}, 1)
net.bound("paluba", 50)
net.bound("odpocet", 1)
net.bound("odplula", 1)
# nástup 50 turistů trvá aspoň 50 × 20 s ≈ 17 min > 15 min, takže loď s danými čísly
# vždy odplouvá po 15 minutách (plná loď ani rušení odpočtu nenastanou);
# ověřeno zvlášť s rychlejším nástupem
net.may_not_fire |= {"plna", "zrus"}
