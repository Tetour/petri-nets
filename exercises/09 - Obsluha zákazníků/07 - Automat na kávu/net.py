from pn import Net

net = Net("Automat na kávu (půlsemestrálka 2023/24, varianta C)")

# hlavní řada: příchody a obsluha, automat nad ní
net.place("gen", (0, 0), tokens=1, label="příchody zákazníků", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(10 min)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="fronta", label_pos="above")
net.place("automat", (4.5, 1.8), tokens=1, label="Automat", label_pos="above")
net.immediate("obsaz", (4.5, 0))
net.place("obsluha", (6, 0))
net.timed("obsl", (7.5, 0), "exp(2 min)", param_pos="below")
net.chain("prichod", "fronta", "obsaz", "obsluha", "obsl")
net.arc("automat", "obsaz")
net.arc("obsl", "automat", out=90, into=0)
net.place("konec", (9, 0), label="ven", label_pos="above")
net.immediate("odchod", (10.5, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# porucha zasáhne probíhající, nebo první další obsluhu; zákazník odchází bez obsluhy
net.immediate("zasah", (6, -1.8), label="zásah", label_pos="above right")
net.arc("obsluha", "zasah")
net.arc("zasah", "konec", via=[(9, -1.8)])
net.place("oprava", (4.5, -1.8), label="oprava", label_pos="below")
net.timed("opr", (3, -1.8), "1 h", param_pos="above")
net.chain("zasah", "oprava", "opr")
# automat se po opravě vrací obloukem kolem generátoru (hlavní řadu nekříží)
net.arc("opr", "automat", via=[(-1.6, -1.8), (-1.6, 1.8)])

# cyklus poruchy: 5–6 h od konce poslední opravy, pak porucha čeká na obsluhu
net.place("provoz", (9, -3.4), tokens=1, label="bez poruchy", label_pos="right")
net.timed("vznik", (7.5, -3.4), "5–6 h", param_pos="below")
net.place("porucha", (6, -3.4), label="porucha", label_pos="below")
net.chain("provoz", "vznik", "porucha")
net.arc("porucha", "zasah")
net.arc("opr", "provoz", via=[(3, -4.8), (9, -4.8)])

net.invariant({"automat": 1, "obsluha": 1, "oprava": 1}, 1,
              name="automat je volný, obsluhuje, nebo se opravuje")
net.invariant({"provoz": 1, "porucha": 1, "oprava": 1}, 1,
              name="jediný cyklus poruchy")
net.sim_events = 100000
