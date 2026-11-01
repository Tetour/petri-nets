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

# letadlo: po nástupu i po letu se vrací „domů“; plné odlétá (p=1), jinak čeká na cestující
net.place("doma", (8.75, 2), tokens=1, label="letadlo doma", label_pos="above right")
net.arc("t_nastup", "doma")
net.immediate("pripraveno", (7, 2))
net.place("ceka", (5.25, 2), label="čeká na cestující", label_pos="below left")
net.chain("doma", "pripraveno", "ceka")
net.arc("ceka", "nastup")

# 1) plno: 20 na palubě (testovací hrany s váhou 20)
net.immediate("plno", (11.25, 2), p=1, label="plno", label_pos="right", param_pos="above right")
net.arc("doma", "plno")
net.loop("paluba", "plno", bend=20, w=20)

# 2) 5 min od posledního nástupu: if–else „sedí už někdo?“
net.timed("t5", (5.25, 3.8), "5 min", param_pos="right")
net.place("nikdo", (5.25, 5.6), label="nikdo nepřišel", label_pos="right")
net.chain("ceka", "t5", "nikdo")
net.immediate("cekam", (3.5, 3.8), label="čekám dál", label_pos="left")
net.arc("nikdo", "cekam", via=[(3.5, 5.6)])
net.arc("cekam", "ceka", via=[(3.5, 2)])
net.immediate("nekdo", (11.25, -2), p=1, label="někdo sedí", label_pos="below", param_pos="right")
net.loop("paluba", "nekdo", bend=20)
net.arc("nikdo", "nekdo", via=[(5.25, 7), (-2, 7), (-2, -2)])

# odlet: všichni na palubě opouštějí systém (smyčka p=1), pak letadlo letí
net.place("odlet", (14.75, 0), label="odlet", label_pos="above right")
net.arc("plno", "odlet", via=[(11.25, 4), (14.75, 4)])
net.arc("nekdo", "odlet", via=[(14.75, -2)])
net.immediate("cyklus", (13, 0), p=1, param_pos="below")
net.arc("paluba", "cyklus")
net.loop("odlet", "cyklus", bend=20)
net.place("odletajici", (13, 1.6), label="odlétá", label_pos="right")
net.immediate("odchod", (13, 3), exit=True, label="odchod", label_pos="right")
net.chain("cyklus", "odletajici", "odchod")

net.immediate("vzlet", (16.5, 0), label="vzlet", label_pos="below")
net.place("let", (18.25, 0), label="vyhlídkový let", label_pos="below")
net.timed("t_let", (20, 0), "50–60 min", param_pos="below")
net.chain("odlet", "vzlet", "let", "t_let")
net.arc("t_let", "doma", via=[(20, 5.6), (8.75, 5.6)])

net.invariant({"doma": 1, "ceka": 1, "nastupuje": 1, "nikdo": 1, "odlet": 1, "let": 1}, 1,
              name="letadlo je právě v jednom stavu")
net.bound("paluba", 20)
