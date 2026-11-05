from pn import Net

net = Net("Kopírovací centrum s poruchami (půlsemestrálka 2021/22, varianta D)")

# příchody a registrace u přepážky
net.place("gen", (0, 0), tokens=1, label="příchody požadavků", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(2 min)", param_pos="below")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="fronta", label_pos="below")
net.place("prepazka", (4.5, 1.6), tokens=1, label="Přepážka", label_pos="above")
net.immediate("reg_start", (4.5, 0))
net.place("registrace", (6, 0))
net.timed("reg", (7.5, 0), "2–3 min", param_pos="below")
net.chain("prichod", "fronta", "reg_start", "registrace", "reg")
net.arc("prepazka", "reg_start")
net.arc("reg", "prepazka", out=90, into=0)

# obsluha s kapacitou 10
net.place("fronta2", (9, 0), label="fronta", label_pos="above")
net.place("obsluha", (10.5, 1.6), tokens=10, label="Obsluha", label_pos="left")
net.immediate("obsaz", (10.5, 0))
net.place("v_obsluze", (13.5, 0), label="v obsluze", label_pos="above")
net.timed("kopirovani", (15, 0), "exp(20 min)", param_pos="below")
net.chain("reg", "fronta2", "obsaz", "v_obsluze", "kopirovani")
net.arc("obsluha", "obsaz")
net.arc("kopirovani", "obsluha", out=90, into=0)

# odchod ze systému
net.place("konec", (16.5, 0), label="konec", label_pos="above")
net.immediate("odchod", (18, 0), exit=True, label="odchod", label_pos="above")
net.chain("kopirovani", "konec", "odchod")

# poruchy: dokud je co ničit, ničí rozpracované obsluhy (p=2), pak porucha skončí (p=1);
# teprve potom (p=0) může začít nová obsluha
net.place("gen_p", (9, -3.2), tokens=1, label="poruchy", label_pos="above")
net.timed("vznik", (10.5, -3.2), "exp(8 h)", param_pos="below")
net.loop("gen_p", "vznik")
net.place("niceni", (12, -3.2), label="porucha", label_pos="below")
net.arc("vznik", "niceni")
net.immediate("zniceni", (13.5, -3.2), p=2, label="zničení obsluhy", label_pos="below right",
              param_pos="above right")
net.loop("niceni", "zniceni")
net.arc("v_obsluze", "zniceni")
# zničená zakázka odchází zvlášť, bez obsluhy
net.place("znicena", (16.5, -3.2), label="zničená", label_pos="below")
net.immediate("odchod_z", (18, -3.2), exit=True, label="odchod bez obsluhy",
              label_pos="above")
net.chain("zniceni", "znicena", "odchod_z")
# uvolnění kapacity (Hrubý: „release“) objíždí síť zprava
net.arc("zniceni", "obsluha", via=[(13.5, -4.6), (19.8, -4.6), (19.8, 2.8), (10.5, 2.8)])
net.immediate("obnoveni", (12, -1.6), p=1, horizontal=True, label="obnovení",
              label_pos="left", param_pos="right")
net.arc("niceni", "obnoveni")

net.invariant({"prepazka": 1, "registrace": 1}, 1)
net.invariant({"obsluha": 1, "v_obsluze": 1}, 10)
net.bound("niceni", 1)
# 2–3 min registrace (průměr 2,5 min) > 2 min mezi příchody: fronta před přepážkou roste
# bez omezení (přetížení je dané zadáním, ne chybou modelu)
net.unbounded_ok = {"fronta"}
