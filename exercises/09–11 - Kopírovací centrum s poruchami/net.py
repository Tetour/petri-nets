from pn import Net

net = Net("09–11", "Kopírovací centrum s poruchami (půlsemestrálka 2021/22, varianta D)")

# příchody a registrace u přepážky
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(2 min)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta")
net.place("prepazka", (4.5, 1.8), tokens=1, label="Přepážka")
net.immediate("reg_start", (4.5, 0))
net.place("registrace", (6, 0))
net.timed("reg", (7.5, 0), "2–3 min")
net.chain("prichod", "fronta", "reg_start", "registrace", "reg")
net.arc("prepazka", "reg_start")
net.arc("reg", "prepazka", bend=-25)

# obsluha s kapacitou 10, zahájení jen když je systém v pořádku (test hrany)
net.place("fronta2", (9, 0), label="Fronta na obsluhu")
net.place("obsluha", (10.5, 1.8), tokens=10, label="Obsluha", label_pos="left")
net.immediate("obsaz", (10.5, 0))
net.place("v_obsluze", (12, 0), label="v obsluze", label_pos="above")
net.timed("kopirovani", (13.5, 0), "exp(20 min)", param_pos="above right")
net.chain("reg", "fronta2", "obsaz", "v_obsluze", "kopirovani")
net.arc("obsluha", "obsaz")
net.arc("kopirovani", "obsluha", bend=-25)
net.place("ok", (10.5, -1.8), tokens=1, label="systém je OK", label_pos="left")
net.loop("ok", "obsaz", bend=25)

# odchod ze systému
net.place("konec", (15, 0), label="konec", label_pos="below right")
net.immediate("odchod", (16.5, 0), exit=True, label="odchod", label_pos="above")
net.chain("kopirovani", "konec", "odchod")

# poruchy: vyprázdnění systému, ničení rozpracovaných obsluh (p=1, dokud je co ničit)
net.place("gen_p", (3, -4.2), tokens=1, label="generátor poruch", label_pos="above")
net.timed("vznik", (4.5, -4.2), "exp(8 h)", param_pos="below")
net.loop("gen_p", "vznik")
net.place("porucha", (6, -4.2), label="vznik poruchy", label_pos="above")
net.arc("vznik", "porucha")
net.immediate("vyprazdni", (8.2, -4.2), p=1, label="vyprázdni systém", label_pos="below")
net.arc("porucha", "vyprazdni")
net.arc("ok", "vyprazdni")
net.place("niceni", (10.5, -4.2), label="ničení", label_pos="below")
net.arc("vyprazdni", "niceni")
net.immediate("zniceni", (12, -4.2), p=1, label="zničení obsluhy", label_pos="right",
              param_pos="below right")
net.loop("niceni", "zniceni")
net.arc("v_obsluze", "zniceni")
net.arc("zniceni", "konec")
net.arc("zniceni", "obsluha", via=[(12, -5.6), (17.8, -5.6), (17.8, 3.0), (10.5, 3.0)])
net.immediate("obnoveni", (10.5, -3.0), horizontal=True, label="obnovení", label_pos="right")
net.arc("niceni", "obnoveni")
net.arc("obnoveni", "ok")

net.invariant({"prepazka": 1, "registrace": 1}, 1)
net.invariant({"obsluha": 1, "v_obsluze": 1}, 10)
net.invariant({"ok": 1, "niceni": 1}, 1)
net.bound("porucha", 1)
# 2–3 min registrace (průměr 2,5 min) > 2 min mezi příchody: fronta před přepážkou roste
# bez omezení (přetížení je dané zadáním, ne chybou modelu)
net.unbounded_ok = {"fronta"}
