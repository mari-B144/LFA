def read():
    with open("date.in", "r") as f:
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


def valid(cuvant,tranz, init,fin):
    stare_curenta=init

    for litera in cuvant:
        if(stare_curenta,litera) not in tranz:
            return False
        stare_curenta = tranz[(stare_curenta,litera)]
    
    return stare_curenta in fin

def alfabet(tranz):
    litere = set()

    for (_, litera) in tranz:
        litere.add(litera)

    return litere



def main():
    stari, tranz, init, fin, cuvinte = read()

    for cuvant in cuvinte:
        if valid(cuvant,tranz, init,fin):
            print("Da")
        else:
            print("Nu")


main()