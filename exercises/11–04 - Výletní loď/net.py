from pn import Net

net = Net("11–04", "Výletní loď (půlsemestrálka 2021/22, varianta C)")

# příchody turistů a nástup po jednom (loď u mola = zařízení pro nástup)
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="below")
net.timed("prichod", (1.5, 0), "exp(5 min)", param_pos="above")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta na molu", label_pos="below")
net.place("lod", (4.5, -1.6), tokens=1, label="Loď u mola", label_pos="left")
net.immediate("zacatek", (4.5, 0))
net.place("nastupuje", (6, 0))
net.timed("nastup", (7.5, 0), "exp(1 min)", label="nástup", label_pos="above",
          param_pos="below right")
net.chain("prichod", "fronta", "zacatek", "nastupuje", "nastup")
net.arc("lod", "zacatek")
net.arc("nastup", "lod", via=[(7.5, -1.6)])
net.place("paluba", (9, 0), label="Na palubě", label_pos="above")
net.arc("nastup", "paluba")

# 20. turista: loď končí nástup (p=1 před dalším nástupem)
net.immediate("vypluti", (10.5, 0), p=1, label="vyplutí", label_pos="above",
              param_pos="above right")
net.arc("paluba", "vypluti", w=20, w_pos="below")
net.arc("lod", "vypluti", via=[(5.4, -2.6), (10.5, -2.6)])
net.place("vyjizdi", (12, 0), label="Vyjíždí", label_pos="below right")
net.arc("vypluti", "vyjizdi")

# s vyplutím odcházejí všichni čekající (smyčka p=1 dokud je fronta neprázdná)
net.immediate("vycisti", (12, 1.8), p=1, horizontal=True, label="vyčisti frontu",
              label_pos="above left", param_pos="above right")
net.loop("vyjizdi", "vycisti", bend=25)
net.arc("fronta", "vycisti", via=[(3, 1.8)])

# okružní jízda 1 h
net.immediate("odplouva", (13.5, 0), label="odplutí", label_pos="above")
net.place("plavba", (15, 0), label="Plavba", label_pos="above")
net.timed("navrat", (16.5, 0), "1 h", label="návrat", label_pos="above", param_pos="below right")
net.chain("vyjizdi", "odplouva", "plavba", "navrat")
net.place("vyletnici", (13.5, -1.6), label="turisté na lodi", label_pos="below")
net.arc("vypluti", "vyletnici", w=20, w_pos="below left")
net.arc("vyletnici", "navrat", w=20, w_pos="below right")
net.arc("navrat", "lod", via=[(16.5, -3.4), (4.5, -3.4)])

# odchod ze systému
net.place("konec", (18, 0), label="konec", label_pos="below")
net.immediate("odchod", (19.5, 0), exit=True, label="odchod", label_pos="above")
net.arc("navrat", "konec", w=20, w_pos="above")
net.arc("vycisti", "konec", via=[(18, 1.8)])
net.arc("konec", "odchod")

net.invariant({"lod": 1, "nastupuje": 1, "vyjizdi": 1, "plavba": 1}, 1)
net.bound("paluba", 20)
net.bound("vyletnici", 20)
