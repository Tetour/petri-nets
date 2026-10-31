from pn import Net

net = Net("04–01", "M/M/1 – automat na kávu, po 5 č. j. nevytíženosti údržba na 20 č. j.")
net.params = {"A": 10, "B": 6}

# M/M/1
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(A)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta")
net.place("linka", (5.4, 1.7), tokens=1, label="Automat", label_pos="left")
net.immediate("obsaz", (4.5, 0))
net.place("obsluha", (6.3, 0))
net.timed("obsl", (7.8, 0), "exp(B)")
net.chain("prichod", "fronta", "obsaz", "obsluha", "obsl")
net.arc("linka", "obsaz")
net.arc("obsl", "linka", bend=-25)
net.place("konec", (9.3, 0))
net.immediate("odchod", (10.8, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# nevytíženost: odpočet 5 běží, jen dokud je značka v místě Automat (nikdo se neobsluhuje
# a fronta je prázdná); obsazení automatu značku vezme a odpočet zruší
net.timed("necinnost", (5.4, 3.4), "5", horizontal=True, label="nevytíženost",
          label_pos="left", param_pos="above")
net.arc("linka", "necinnost")
net.place("udrzba", (7.8, 3.4), label="údržba", label_pos="above")
net.arc("necinnost", "udrzba")
net.timed("konec_udrzby", (7.8, 1.7), "20", param_pos="right")
net.arc("udrzba", "konec_udrzby")
net.arc("konec_udrzby", "linka")

net.invariant({"linka": 1, "obsluha": 1, "udrzba": 1}, 1,
              name="automat je volný, obsluhuje, nebo je v údržbě")
