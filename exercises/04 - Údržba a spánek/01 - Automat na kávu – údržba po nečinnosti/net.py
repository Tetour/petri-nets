from pn import Net

net = Net("M/M/1 – automat na kávu, po 5 č. j. nevytíženosti údržba na 20 č. j.")
net.params = {"A": 10, "B": 6}

# M/M/1
net.place("gen", (0, 0), tokens=1, label="příchody zákazníků", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(A)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="fronta", label_pos="below")
net.place("linka", (4.5, 1.6), tokens=1, label="Automat", label_pos="above right")
net.immediate("obsaz", (4.5, 0))
net.place("obsluha", (6, 0))
net.timed("obsl", (7.5, 0), "exp(B)", param_pos="below")
net.chain("prichod", "fronta", "obsaz", "obsluha", "obsl")
net.arc("linka", "obsaz")
net.arc("obsl", "linka", out=90, into=0)  # návrat automatu
net.place("konec", (9, 0), label="hotovo", label_pos="below")
net.immediate("odchod", (10.5, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# nevytíženost: odpočet 5 běží, jen dokud je značka v místě Automat (nikdo se neobsluhuje
# a fronta je prázdná); obsazení automatu značku vezme a odpočet zruší
net.timed("necinnost", (4.5, 3.2), "5", label="nevytíženost", label_pos="above",
          param_pos="right")
net.arc("linka", "necinnost")
net.place("udrzba", (3, 3.2), label="údržba", label_pos="above")
net.arc("necinnost", "udrzba")
net.timed("konec_udrzby", (3, 1.6), "20", param_pos="left")
net.arc("udrzba", "konec_udrzby")
net.arc("konec_udrzby", "linka")

net.invariant({"linka": 1, "obsluha": 1, "udrzba": 1}, 1,
              name="automat je volný, obsluhuje, nebo je v údržbě")
