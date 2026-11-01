from pn import Net

net = Net("Výletní loď (půlsemestrálka 2021/22, varianta C)")

# příchody turistů a nástup po jednom (loď u mola = zařízení pro nástup)
net.place("gen", (0, 0), tokens=1, label="příchody turistů", label_pos="below")
net.timed("prichod", (1.5, 0), "exp(5 min)", param_pos="above")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="fronta na molu", label_pos="below")
net.place("lod", (4.5, 1.8), tokens=1, label="loď u mola", label_pos="below right")
net.immediate("zacatek", (4.5, 0))
net.place("nastupuje", (6, 0))
net.timed("nastup", (7.5, 0), "exp(1 min)", param_pos="below")
net.chain("prichod", "fronta", "zacatek", "nastupuje", "nastup")
net.arc("lod", "zacatek")
net.arc("nastup", "lod", out=90, into=0)
net.place("paluba", (9.75, 0), label="na palubě", label_pos="above")
net.arc("nastup", "paluba")

# 20. turista: loď končí nástup (p=1 před dalším nástupem)
net.immediate("vypluti", (11.25, 0), p=1, label="vyplutí", label_pos="below left",
              param_pos="above right")
net.arc("paluba", "vypluti", w=20, w_pos="above")
net.arc("lod", "vypluti", via=[(4.5, 3.6), (11.25, 3.6)])
net.place("vyjizdi", (12.75, 0), label="vyjíždí", label_pos="below right")
net.arc("vypluti", "vyjizdi")

# s vyplutím odcházejí všichni čekající (smyčka p=1, dokud je fronta neprázdná)
net.immediate("vycisti", (12.75, 1.8), p=1, label="vyčisti frontu", label_pos="above right",
              param_pos="left")
net.loop("vyjizdi", "vycisti", bend=20)
net.arc("fronta", "vycisti", via=[(3, 6.6), (12.75, 6.6)])

# okružní jízda 1 h; turisté na lodi jedou s ní
net.immediate("odplouva", (14.25, 0), label="odplutí", label_pos="above")
net.place("plavba", (15.75, 0), label="plavba", label_pos="above")
net.timed("navrat", (17.25, 0), "1 h", param_pos="below left")
net.chain("vyjizdi", "odplouva", "plavba", "navrat")
net.place("vyletnici", (14.25, -1.8), label="turisté na lodi", label_pos="below")
net.arc("vypluti", "vyletnici", w=20, via=[(11.25, -1.8)], w_pos="right")
net.arc("vyletnici", "navrat", w=20, via=[(17.25, -1.8)], w_pos="above")
net.arc("navrat", "lod", via=[(18.75, 0), (18.75, 5.4), (3.75, 5.4), (3.75, 1.8)])

# odchod ze systému: vyhnaní z mola i turisté po jízdě
net.place("konec", (17.25, 1.8), label="konec", label_pos="right")
net.arc("navrat", "konec", w=20, w_pos="right")
net.arc("vycisti", "konec")
net.immediate("odchod", (17.25, 3.6), exit=True, label="odchod", label_pos="right")
net.arc("konec", "odchod")

net.invariant({"lod": 1, "nastupuje": 1, "vyjizdi": 1, "plavba": 1}, 1)
net.bound("paluba", 20)
net.bound("vyletnici", 20)
