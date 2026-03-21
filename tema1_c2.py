def read():
    with open("date_c2.in", "r") as f:
        N = int(f.readline().strip())
        stari = f.readline().strip().split()
        M = int(f.readline().strip())

        tranz = {}
        for _ in range(M):
            start, stop, litera = f.readline().strip().split()

            key = (start, litera)
            if key not in tranz:
                tranz[key] = []

            tranz[key].append(stop)

        init = f.readline().strip()
        nr_fin = int(f.readline().strip())
        fin = set(f.readline().strip().split())
        nr_cuvinte = int(f.readline().strip())

        cuvinte = []
        for _ in range(nr_cuvinte):
            cuvinte.append(f.readline().strip())
    return stari, tranz, init, fin, cuvinte


def valid(cuvant, tranz, init, fin):
    stari_curente = [(init, [])]

    for litera in cuvant:
        stari_noi = []

        for (stare, drum) in stari_curente:
            if (stare, litera) in tranz:
                for stare_urmatoare in tranz[(stare, litera)]:
                    drum_nou = drum + [(stare, litera, stare_urmatoare)]
                    stari_noi.append((stare_urmatoare, drum_nou))
        stari_curente = stari_noi

    for (stare, drum) in stari_curente:
        if stare in fin:
            return True, drum
    return False, []


def alfabet(tranz):
    litere = set()
    for (_, litera) in tranz:
        litere.add(litera)
    return litere


def main():
    stari, tranz, init, fin, cuvinte = read()

    with open("date_c2.out", "w") as g:
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