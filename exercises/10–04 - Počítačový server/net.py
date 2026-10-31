from pn import Net

net = Net("10–04", "Počítačový server (půlsemestrálka 2013/14, varianta C)", unit="ms")
# doby příjmu a odeslání zprávy zadání neuvádí
net.params = {"Tp": 0.1, "To": 0.1}

# požadavky z okolí, příjem síťovou linkou do vstupního bufferu
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="below")
net.timed("prichod", (1.5, 0), "exp(1 s)", param_pos="below")
net.loop("gen", "prichod")
net.place("okoli", (3, 0), label="Zprávy z okolí", label_pos="above")
net.immediate("obsaz_rx", (4.5, 0))
net.place("prijem", (6, 0), label="příjem", label_pos="below")
net.timed("rx", (7.5, 0), "Tp", param_pos="below")
net.place("buf_in", (9, 0), label="Vstupní buffer", label_pos="above")
net.chain("prichod", "okoli", "obsaz_rx", "prijem", "rx", "buf_in")

# databázová úloha zpracovává požadavky, dokud je buffer neprázdný
net.immediate("vezmi", (10.5, 0), p=1, param_pos="above")
net.place("zprac", (12, 0))
net.timed("proc", (13.5, 0), "exp(1 ms)", param_pos="below left")
net.place("buf_out", (15, 0), label="Výstupní buffer", label_pos="above")
net.chain("buf_in", "vezmi", "zprac", "proc", "buf_out")

# odeslání výsledku síťovou linkou
net.immediate("obsaz_tx", (16.5, 0))
net.place("odesila", (18, 0), label="odesílání", label_pos="below")
net.timed("tx", (19.5, 0), "To", param_pos="below")
net.place("odeslano", (21, 0), label="odesláno", label_pos="above")
net.immediate("odchod", (22.5, 0), exit=True, label="odchod", label_pos="above")
net.chain("buf_out", "obsaz_tx", "odesila", "tx", "odeslano", "odchod")

# síťová linka: buď přijímá, nebo odesílá
net.place("linka", (12, 2.8), tokens=1, label="Síťová linka", label_pos="above")
net.arc("linka", "obsaz_rx", via=[(4.5, 2.8)])
net.arc("rx", "linka", via=[(7.5, 2.0), (11.5, 2.0)])
net.arc("linka", "obsaz_tx", via=[(16.5, 2.8)])
net.arc("tx", "linka", via=[(19.5, 2.0), (12.5, 2.0)])

# procesor a plánovač
net.place("cpu", (9, -6), tokens=1, label="Procesor volný", label_pos="below")
net.immediate("plan_u", (6, -4.6), prob=90, param_pos="left")
net.place("uziv", (7.5, -3.2), label="běží uživatelská úloha", label_pos="above left")
net.timed("kvantum", (7.5, -4.6), "10 ms", param_pos="right")
net.chain("cpu", "plan_u", "uziv", "kvantum", "cpu")
net.immediate("plan_db", (12, -4.6), prob=10, param_pos="right")
net.place("db", (10.5, -3.2), label="běží DB úloha", label_pos="above right")
net.immediate("uvolni", (10.5, -4.6))
net.chain("cpu", "plan_db", "db", "uvolni", "cpu")
net.arc("db", "vezmi")
net.arc("proc", "db", via=[(13.5, -3.2)])

# více než 100 požadavků v bufferu: DB úloha odebere procesor uživatelské úloze
net.immediate("preempce", (9, -3.2), horizontal=False, label="přerušení", label_pos="below",
              param_pos="below")
net.arc("buf_in", "preempce", w=101, bend=20, w_pos="right")
net.arc("preempce", "buf_in", w=101, bend=20, w_pos="left")
net.arc("uziv", "preempce")
net.arc("preempce", "db")

net.invariant({"linka": 1, "prijem": 1, "odesila": 1}, 1)
net.invariant({"cpu": 1, "uziv": 1, "db": 1, "zprac": 1}, 1)
net.sim_events = 100000
# s danými parametry DB úloha dostane procesor zhruba každých 100 ms, požadavky chodí
# po 1 s, takže se ve vstupním bufferu nikdy nesejde 101 požadavků (ověřeno zvlášť
# se zrychlenými příchody)
net.may_not_fire.add("preempce")
