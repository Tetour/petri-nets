from pn import Net

net = Net("05–08", "M/M/1 se skladem, každých 500 č. j. kapacita +3 na 100 č. j.")
net.params = {"A": 10, "B": 8}

# M/M/1, linka typu Sklad s kapacitou 1
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="below")
net.timed("prichod", (1.5, 0), "exp(A)", param_pos="below")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta", label_pos="below")
net.place("sklad", (4.5, 1.7), tokens=1, label="Sklad", label_pos="above right")
net.immediate("enter", (4.5, 0))
net.place("obsluha", (6, 0))
net.timed("obsl", (7.5, 0), "exp(B)")
net.chain("prichod", "fronta", "enter", "obsluha", "obsl")
net.arc("sklad", "enter")
net.arc("obsl", "sklad", bend=-15)
net.place("konec", (9, 0))
net.immediate("odchod", (10.5, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# každých 500 č. j.: kapacita +3 na 100 č. j.
net.place("gen_r", (1.5, 3.4), tokens=1, label="generátor rozšíření", label_pos="left")
net.timed("rozsir", (3, 3.4), "500", param_pos="above")
net.loop("gen_r", "rozsir")
net.arc("rozsir", "sklad", w=3, w_pos="above right")
net.place("rozsireno", (4.5, 3.4), label="M/M/4", label_pos="above")
net.timed("doba", (6, 3.4), "100")
net.place("vratit", (7.5, 3.4), label="vrátit", label_pos="above")
net.arc("rozsir", "rozsireno")
net.chain("rozsireno", "doba")
net.arc("doba", "vratit", w=3, w_pos="above")

# po 100 č. j. odebírat jednotky, jak se uvolňují (p=1 předběhne obsazení)
net.immediate("odeber", (7.5, 1.7), p=1, horizontal=True, label="odeber",
              label_pos="below right", param_pos="above left")
net.arc("vratit", "odeber")
net.arc("sklad", "odeber")

# kapacita = 1 + 3 za probíhající rozšíření + jednotky, které se ještě mají vrátit
net.invariant({"sklad": 1, "obsluha": 1, "rozsireno": -3, "vratit": -1}, 1,
              name="sklad + obsluha = 1 + 3·M/M/4 + vrátit")
net.sim_events = 60000
