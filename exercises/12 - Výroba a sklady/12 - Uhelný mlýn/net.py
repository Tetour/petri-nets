from pn import Net

net = Net("Uhelný mlýn (půlsemestrálky 2014–19, Z2)")

# stav elektrárny: běžný provoz -> havárie -> chladnutí 5 h -> rozehřívání 5 h -> běžný provoz
net.place("do_havarie", (0, 0), tokens=1, label="do havárie", label_pos="below")
net.timed("havarie_t", (1.5, 0), "exp(100 d)", param_pos="above")
net.place("havarie", (3, 0), label="havárie", label_pos="below")
net.immediate("odstaveni", (4.5, 0), label="odstavení", label_pos="above")
net.place("chladne", (6, 0), label="kotel chladne", label_pos="below")
net.timed("chladnuti", (7.5, 0), "5 h", param_pos="above")
net.place("rozehrivani", (9, 0), label="rozehřívání", label_pos="above")
net.timed("rozehrati", (10.5, 0), "5 h", param_pos="above")
net.place("rozehrato", (12, 0))
net.immediate("nabehnuti", (13.5, 0), label="naběhnutí", label_pos="above right")
net.chain("do_havarie", "havarie_t", "havarie", "odstaveni", "chladne", "chladnuti",
          "rozehrivani", "rozehrati", "rozehrato", "nabehnuti")
# interval do další havárie se počítá od naběhnutí
net.arc("nabehnuti", "do_havarie", via=[(13.5, 1.6), (0, 1.6)])

# mlýn: v běžném provozu dávka po 1 min, při rozehřívání po 5 min
net.place("mlyn_b", (4.5, -2.6), tokens=1, label="mlýn – běžný provoz", label_pos="right")
net.arc("mlyn_b", "odstaveni")
net.arc("nabehnuti", "mlyn_b", via=[(14.4, 0), (14.4, -6.8), (2.4, -6.8), (2.4, -2.6)])
net.timed("davka_1", (4.5, -4.4), "1 min", param_pos="left")
net.loop("mlyn_b", "davka_1", bend=30)
net.place("mlyn_r", (12, -2.6), label="mlýn – rozehřívání", label_pos="left")
net.arc("chladnuti", "mlyn_r", via=[(7.5, -1.6), (12, -1.6)])
net.arc("mlyn_r", "nabehnuti", via=[(13.5, -2.6)])
net.timed("davka_5", (12, -4.4), "5 min", param_pos="right")
net.loop("mlyn_r", "davka_5", bend=30)

# dávky paliva v kotli shoří
net.place("kotel", (8.25, -4.4), label="Kotel", label_pos="above")
net.arc("davka_1", "kotel")
net.arc("davka_5", "kotel")
net.immediate("spaleni", (8.25, -5.9), exit=True, label="spálení", label_pos="right")
net.arc("kotel", "spaleni")

net.invariant({"mlyn_b": 1, "chladne": 1, "mlyn_r": 1}, 1,
              name="mlýn: běžný provoz / stojí / rozehřívání")
net.invariant({"do_havarie": 1, "havarie": 1, "chladne": 1, "rozehrivani": 1, "rozehrato": 1}, 1,
              name="jeden cyklus stavu elektrárny")
net.bound("kotel", 1)
# havárie exp(100 d) a mlýn po 1 min: ~1440 událostí za den, ~200 dní simulace
net.sim_events = 300000
