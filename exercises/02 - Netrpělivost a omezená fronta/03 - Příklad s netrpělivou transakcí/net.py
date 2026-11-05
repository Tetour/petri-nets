from pn import Net

net = Net("Zákaznická linka s jedním operátorem, volající zavěsí po 1–5 min čekání")

# volání a čekání na spojení
net.place("gen", (0, 0), tokens=1, label="příchody hovorů", label_pos="above")
net.timed("volani", (1.5, 0), "exp(4 min)")
net.loop("gen", "volani")
net.place("fronta", (3, 0), label="fronta", label_pos="above")

# operátor (zařízení)
net.place("operator", (4.5, 1.6), tokens=1, label="Operátor")
net.immediate("spojeni", (4.5, 0))
net.place("hovor", (6, 0), label="hovor", label_pos="above")
net.timed("hovor_t", (7.5, 0), "exp(3 min)")
net.chain("volani", "fronta", "spojeni", "hovor", "hovor_t")
net.arc("operator", "spojeni")
net.arc("hovor_t", "operator", out=90, into=0)
net.place("vyrizen", (9, 0), label="vyřízen", label_pos="above")
net.immediate("odchod", (10.5, 0), exit=True, label="odchod")
net.chain("hovor_t", "vyrizen", "odchod")

# netrpělivost: každý volající má vlastní trpělivost 1–5 min
net.timed("zaveseni", (4.5, -1.8), "1–5 min", label="zavěšení", label_pos="below",
          param_pos="above")
net.arc("fronta", "zaveseni", via=[(3, -1.8)])
net.place("zavesil", (6, -1.8), label="zavěsil", label_pos="below")
net.immediate("odchod2", (7.5, -1.8), exit=True, label="odchod bez obsluhy", label_pos="right")
net.chain("zaveseni", "zavesil", "odchod2")

net.invariant({"operator": 1, "hovor": 1}, 1)
