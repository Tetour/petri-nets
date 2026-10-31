from pn import Net

net = Net("11–02", "Vyhlídkové lety (půlsemestrálka 2024/25, varianta C)")

# příchody a nástup do letadla (letadlo funguje jako zařízení)
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(5 min)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta", label_pos="below")
net.place("letadlo", (6, 2.2), tokens=1, label="letadlo doma", label_pos="below left")
net.immediate("nastup", (4.5, 0))
net.place("nastupuje", (6, 0), label="nastupuje", label_pos="below")
net.timed("t_nastup", (7.5, 0), "1–2 min")
net.chain("prichod", "fronta", "nastup", "nastupuje", "t_nastup")
net.arc("letadlo", "nastup")
net.arc("t_nastup", "letadlo")
net.place("paluba", (9.5, 0), label="na palubě", label_pos="below")
net.arc("t_nastup", "paluba")

# 1) letadlo je plné: 20 na palubě a letadlo doma
net.immediate("plno", (7.75, 2.2), p=1, label="plno", label_pos="above left", param_pos="above right")
net.arc("letadlo", "plno")
net.loop("paluba", "plno", bend=15, w=20)

# 2) 5 min od posledního nástupu (odpočet běží, jen když je letadlo doma volné)
net.timed("t5", (6, 3.8), "5 min", horizontal=True, param_pos="right")
net.place("kontrola", (6, 5.4), label="nikdo nepřišel", label_pos="above")
net.immediate("cekam", (4.5, 3.8), horizontal=True, label="čekám dál", label_pos="left")
net.chain("letadlo", "t5", "kontrola", "cekam", "letadlo")
net.immediate("nekdo", (9.5, 2.2), p=1, label="někdo sedí", label_pos="above",
              param_pos="below right")
net.arc("kontrola", "nekdo")
net.loop("paluba", "nekdo", bend=15)

# odlet: všichni na palubě opouštějí systém, letadlo letí
net.place("odlet", (11.5, 2.2), label="odlet", label_pos="above left")
net.arc("plno", "odlet", via=[(7.75, 4.2), (11.5, 4.2)])
net.arc("nekdo", "odlet")
net.immediate("cyklus", (11.5, 0), p=1, param_pos="below")
net.loop("odlet", "cyklus", bend=15)
net.arc("paluba", "cyklus")
net.place("odletajici", (13, 0), label="odlétá", label_pos="below")
net.immediate("odchod", (14.5, 0), exit=True, label="odchod", label_pos="below")
net.chain("cyklus", "odletajici", "odchod")

net.immediate("vzlet", (13, 2.2), label="vzlet", label_pos="above")
net.place("let", (14.5, 2.2), label="vyhlídkový let", label_pos="above")
net.timed("t_let", (16, 2.2), "50–60 min", param_pos="below")
net.chain("odlet", "vzlet", "let", "t_let")
net.arc("t_let", "letadlo", via=[(16, 6.8), (3.3, 6.8), (3.3, 2.2)])

net.invariant({"letadlo": 1, "nastupuje": 1, "kontrola": 1, "odlet": 1, "let": 1}, 1,
              name="letadlo je právě v jednom stavu")
net.bound("paluba", 20)
