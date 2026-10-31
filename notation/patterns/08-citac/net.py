from pn import Net

net = Net("P08", "Čítač: každá N-tá transakce (N = 10)")
net.closed = True
net.simulate = False
net.place("p", (0, 0), tokens=1, label="po obsluze", label_pos="above")
net.immediate("zapocti", (1.5, 0))
net.place("dal", (3, 0), label="pokračuje", label_pos="above")
net.place("cit", (1.5, -1.6), tokens=9, label="čítač", label_pos="left")
net.chain("p", "zapocti", "dal")
net.arc("zapocti", "cit")
net.immediate("desata", (3.6, -1.6), label="10. transakce", label_pos="right",
              param_pos="below")
net.arc("cit", "desata", w=10, w_pos="above")
net.place("akce", (3.6, -3.3), label="akce (údržba, porucha …)", label_pos="right")
net.arc("desata", "akce")
