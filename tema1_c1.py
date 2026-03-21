def read():
    with open("date_c1.in", "r") as f:
        N = int(f.readline().strip())
        stari = f.readline().strip().split()
        M = int(f.readline().strip())

        tranz = {}
        for _ in range(M):
            start, stop, litera = f.readline().strip().split()
            tranz[(start, litera)] = stop

        init = f.readline().strip()
        nr_fin = int(f.readline().strip())
        fin = set(f.readline().strip().split())
        nr_cuvinte = int(f.readline().strip())

        cuvinte = []
        for _ in range(nr_cuvinte):
            cuvinte.append(f.readline().strip())
    return stari, tranz, init, fin, cuvinte


def valid(cuvant, tranz, init, fin):
    stare_curenta = init
    drum = []

    for litera in cuvant:
        if (stare_curenta, litera) not in tranz:
            return False, []
        stare_urmatoare = tranz[(stare_curenta, litera)]
        drum.append((stare_curenta, litera, stare_urmatoare))
        stare_curenta = stare_urmatoare

    if stare_curenta in fin:
        return True, drum
    else:
        return False, []



def alfabet(tranz):
    litere = set()
    for (_, litera) in tranz:
        litere.add(litera)
    return litere

def main():
    stari, tranz, init, fin, cuvinte = read()

    with open("date_c1.out", "w") as g:
        alf = alfabet(tranz)
        g.write("Alfabet: " + " ".join(sorted(alf)) + "\n")
        for cuvant in cuvinte:
            ok, drum = valid(cuvant, tranz, init, fin)
            if ok:
                g.write("Da\n")
                g.write("Tranzitii:\n")
                for t in drum:
                    g.write(f"{t[0]} prin {t[1]} la {t[2]}\n")
            else:
                g.write("Nu\n")

main()