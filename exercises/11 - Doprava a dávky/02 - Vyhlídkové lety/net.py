from pn import Net

net = Net("Vyhlídkové lety (půlsemestrálka 2024/25, varianta C)")

# zákazníci: příchody, fronta, nástup po jednom (letadlo čekající na cestující = zařízení pro nástup)
net.place("gen", (0, 0), tokens=1, label="příchody zákazníků", label_pos="below")
net.timed("prichod", (1.75, 0), "exp(5 min)", param_pos="above")
net.loop("gen", "prichod")
net.place("fronta", (3.5, 0), label="fronta", label_pos="below")
net.immediate("nastup", (5.25, 0))
net.place("nastupuje", (7, 0), label="nastupuje", label_pos="below")
net.timed("t_nastup", (8.75, 0), "1–2 min", param_pos="below")
net.chain("prichod", "fronta", "nastup", "nastupuje", "t_nastup")
net.place("paluba", (11.25, 0), label="na palubě", label_pos="below left")
net.arc("t_nastup", "paluba")

# letadlo: jediné místo „letadlo čeká“ (zařízení pro nástup); vrací se do něj po nástupu i po letu
net.place("ceka", (5.25, 2), tokens=1, label="letadlo čeká", label_pos="above right")
net.arc("ceka", "nastup")
net.arc("t_nastup", "ceka", out=90, into=315)   # návrat po nástupu do pravého dolního rohu

# 1) plno: 20 na palubě (testovací hrany s váhou 20)
net.immediate("plno", (11.25, 2), p=1, label="plno", label_pos="above left", param_pos="above right")
net.arc("ceka", "plno")
net.loop("paluba", "plno", bend=20, w=20)

# 2) 5 min od posledního nástupu: if–else „sedí už někdo?“
net.timed("t5", (3.5, 3.6), "5 min", param_pos="above")
net.place("nikdo", (0, 2), label="nikdo nepřišel", label_pos="below")
net.arc("ceka", "t5", out=135, into=0)          # odpočet z levého horního rohu
net.arc("t5", "nikdo", via=[(0, 3.6)])
net.immediate("cekam", (1.75, 2), label="čekám dál", label_pos="above")
net.arc("nikdo", "cekam")
net.arc("cekam", "ceka")
net.immediate("nekdo", (11.25, -2), p=1, label="někdo sedí", label_pos="below left",
              param_pos="below right")
net.loop("paluba", "nekdo", bend=20)
net.arc("nikdo", "nekdo", via=[(-2, 2), (-2, -2)])

# odlet: všichni na palubě opouštějí systém výstupním přechodem s p=1 (testuje „odlet“), pak letadlo letí
net.place("odlet", (14.75, 0), label="odlet", label_pos="above right")
net.arc("plno", "odlet", via=[(14.75, 2)])
net.arc("nekdo", "odlet", via=[(14.75, -2)])
net.immediate("cyklus", (13, 0), p=1, exit=True, label="odchod", label_pos="above",
              param_pos="below")
net.arc("paluba", "cyklus")
net.loop("odlet", "cyklus", bend=20)

net.immediate("vzlet", (16.5, 0), label="vzlet", label_pos="below")
net.place("let", (18.25, 0), label="vyhlídkový let", label_pos="below")
net.timed("t_let", (20, 0), "50–60 min", param_pos="below")
net.chain("odlet", "vzlet", "let", "t_let")
net.arc("t_let", "ceka", via=[(20, 5.2), (5.25, 5.2)])

net.invariant({"ceka": 1, "nastupuje": 1, "nikdo": 1, "odlet": 1, "let": 1}, 1,
              name="letadlo je právě v jednom stavu")
net.bound("paluba", 20)
