from pn import Net

net = Net("Logistická centrála (půlsemestrálka 2010/11)")

# příjezdy dodávek a vyložení na rampě (doba vyložení zanedbaná)
net.place("gen", (0, 0), tokens=1, label="příjezdy dodávek", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(2 h)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="fronta", label_pos="below")
net.place("rampa", (4.5, 1.6), tokens=1, label="Rampa", label_pos="left")
net.immediate("vylozeni", (4.5, 0))
net.place("vylozena", (6, 0), label="Vyložená", label_pos="below")
net.chain("prichod", "fronta", "vylozeni", "vylozena")
net.arc("rampa", "vylozeni")

# polovina odjíždí hned (horní řada), polovina nakládá 100 zpracovaných balíků
net.immediate("prazdna", (8, 2.2), prob=50, label="odjíždí prázdná", label_pos="above",
              param_pos="below")
net.immediate("nakladat", (8, 0), prob=50, label="bude nakládat", label_pos="below",
              param_pos="above")
net.arc("vylozena", "prazdna", via=[(6, 2.2)])
net.arc("vylozena", "nakladat")
net.place("naklada", (12, 0), label="Nakládá", label_pos="above")
net.arc("nakladat", "naklada")
net.timed("nalozeni", (12, -2.2), "exp(1 min)", param_pos="below")
net.loop("naklada", "nalozeni", bend=25)
net.place("nalozeno", (13.5, -2.2), label="Naloženo", label_pos="below")
net.arc("nalozeni", "nalozeno")
net.immediate("odjezd", (13.5, 0), label="plná", label_pos="above")
net.arc("naklada", "odjezd")
net.arc("nalozeno", "odjezd", w=100, w_pos="right")

# obě větve se sejdou, dodávka uvolní rampu a opouští systém
net.place("odjizdi", (15, 0), label="Odjíždí", label_pos="below")
net.arc("odjezd", "odjizdi")
net.arc("prazdna", "odjizdi", via=[(15, 2.2)])
net.immediate("uvolneni", (16.8, 0), label="uvolní rampu", label_pos="below")
net.arc("odjizdi", "uvolneni")
net.arc("uvolneni", "rampa", via=[(16.8, 3.6), (4.5, 3.6)])
net.place("konec", (18.3, 0), label="konec", label_pos="below")
net.immediate("odchod", (19.8, 0), exit=True, label="odchod", label_pos="above")
net.chain("uvolneni", "konec", "odchod")

# pracovník zpracovává přivezené balíky (nezávislý proces, dolní řada)
net.place("nezprac", (4.5, -2.2), label="Nezpracované", label_pos="left")
net.arc("vylozeni", "nezprac", w=100, w_pos="left")
net.place("pracovnik", (6, -3.8), tokens=1, label="Pracovník", label_pos="below")
net.immediate("obsaz_p", (6, -2.2))
net.place("zpracovava", (7.5, -2.2))
net.timed("zpracovani", (9, -2.2), "exp(1 min)", param_pos="above")
net.chain("nezprac", "obsaz_p", "zpracovava", "zpracovani")
net.arc("pracovnik", "obsaz_p")
net.arc("zpracovani", "pracovnik", out=270, into=0)
net.place("zprac", (10.7, -2.2), label="Zpracované", label_pos="above")
net.arc("zpracovani", "zprac")
net.arc("zprac", "nalozeni")

net.invariant({"rampa": 1, "vylozena": 1, "naklada": 1, "odjizdi": 1}, 1)
net.invariant({"pracovnik": 1, "zpracovava": 1}, 1)
net.bound("nalozeno", 100)
# kapacitu centrály zadání nezkoumá: přiváží každá dodávka, odváží jen polovina,
# takže zásoba zpracovaných balíků roste v průměru o 50 na dodávku
net.unbounded_ok = {"zprac"}
# fronta nezpracovaných je stabilní (vytížení pracovníka 100 min za 2 h ≈ 83 %),
# ale balíky přicházejí po stovkách, takže občas naroste na stovky kusů
net.unbounded_ok.add("nezprac")
