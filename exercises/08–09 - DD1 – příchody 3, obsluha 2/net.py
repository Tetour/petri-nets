from pn import Net

net = Net("08–09", "D/D/1, příchody á 3 min, obsluha 2 min, značení v čase TMAX = 10", unit="min")

net.place("gen", (0, 0), tokens=1, label="příchody požadavků", label_pos="above")
net.timed("prichod", (1.5, 0), "3 min")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), tokens=0, label="fronta", label_pos="below")
net.place("linka", (4.5, 1.6), tokens=0, label="linka", label_pos="above")
net.immediate("obsaz", (4.5, 0))
net.place("obsluha", (6, 0), tokens=1)
net.timed("obsl", (7.5, 0), "2 min", param_pos="below")
net.place("konec", (9, 0), label="hotovo", label_pos="below")
net.immediate("odchod", (10.5, 0), exit=True, label="odchod")
net.chain("prichod", "fronta", "obsaz", "obsluha", "obsl", "konec", "odchod")
net.arc("linka", "obsaz")
# návrat linky: oblouk z horní strany přechodu
net.arc("obsl", "linka", out=90, into=0)
net.invariant({"linka": 1, "obsluha": 1}, 1)

# zobrazené značení = stav po provedení všech událostí v čase 10 (P0 přichází v čase 0)
net.trace = {"start": {"gen": 1, "fronta": 1, "linka": 1}, "at": 10}
net.bound("fronta", 0)   # příchod á 3 min, obsluha 2 min → stabilní, nikdo nikdy nečeká
net.sim_events = 3000
