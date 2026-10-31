from pn import Net

net = Net("02–03", "Zákaznická linka s jedním operátorem, volající zavěsí po 1–5 min čekání")

# volání a čekání na spojení
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="above")
net.timed("volani", (1.5, 0), "exp(4 min)")
net.loop("gen", "volani")
net.place("fronta", (3, 0), label="Fronta", label_pos="above")

# operátor (zařízení)
net.place("operator", (4.5, 1.6), tokens=1, label="Operátor")
net.immediate("spojeni", (4.5, 0))
net.place("hovor", (6, 0), label="hovor", label_pos="above")
net.timed("hovor_t", (7.5, 0), "exp(3 min)")
net.chain("volani", "fronta", "spojeni", "hovor", "hovor_t")
net.arc("operator", "spojeni")
net.arc("hovor_t", "operator", bend=-25)
net.place("vyrizen", (9, 0), label="vyřízen", label_pos="above")
net.immediate("odchod", (10.5, 0), exit=True, label="odchod")
net.chain("hovor_t", "vyrizen", "odchod")

# netrpělivost: každý volající má vlastní trpělivost 1–5 min
net.timed("zaveseni", (4.5, -1.6), "1–5 min", horizontal=True, label="zavěšení",
          label_pos="below", param_pos="above")
net.arc("fronta", "zaveseni", via=[(3, -1.6)])
net.place("zavesil", (7.5, -1.6), label="zavěsil", label_pos="below")
net.immediate("odchod2", (9, -1.6), exit=True, label="odchod bez obsluhy", label_pos="right")
net.chain("zaveseni", "zavesil", "odchod2")

net.invariant({"operator": 1, "hovor": 1}, 1)
