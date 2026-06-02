def citeste_gramatica_fnc(fisier):
    with open(fisier) as f:
        linii = [l.strip() for l in f.readlines() if l.strip()]

    idx = 0
    neterminale = set(linii[idx].split()); idx += 1
    terminale   = set(linii[idx].split()); idx += 1
    nr_prod     = int(linii[idx]);         idx += 1

    productii = {}
    for _ in range(nr_prod):
        parti  = linii[idx].split()
        stanga = parti[0]
        tokeni = parti[1:]
        if tokeni == ['λ']:
            dreapta = []
        elif len(tokeni) == 1 and len(tokeni[0]) > 1:
            dreapta = list(tokeni[0])
        else:
            dreapta = tokeni
        if stanga not in productii:
            productii[stanga] = []
        productii[stanga].append(dreapta)
        idx += 1

    start  = linii[idx]; idx += 1
    cuvant = linii[idx] if idx < len(linii) else ""

    return neterminale, terminale, productii, start, cuvant


def cyk(fisier_input, fisier_output):
    neterminale, terminale, productii, start, cuvant = citeste_gramatica_fnc(fisier_input)

    n = len(cuvant)

    if n == 0:
        acceptat = [] in productii.get(start, [])
        rezultat = "DA" if acceptat else "NU"
        with open(fisier_output, 'w') as f:
            f.write(rezultat + "\n")
        print(rezultat)
        return

    dp = [[set() for _ in range(n)] for _ in range(n)]

    for i in range(n):
        caracter = cuvant[i]
        for nt, prods in productii.items():
            for prod in prods:
                if prod == [caracter]:
                    dp[i][i].add(nt)

    for lungime in range(2, n + 1):
        for i in range(n - lungime + 1):
            j = i + lungime - 1
            for k in range(i, j):
                for nt, prods in productii.items():
                    for prod in prods:
                        if len(prod) == 2:
                            b, c = prod[0], prod[1]
                            if b in dp[i][k] and c in dp[k+1][j]:
                                dp[i][j].add(nt)

    acceptat = start in dp[0][n-1]
    rezultat = "DA" if acceptat else "NU"

    with open(fisier_output, 'w') as f:
        f.write(rezultat + "\n\n")
        f.write(afiseaza_tabela(dp, cuvant))

    print(rezultat)
    print(afiseaza_tabela(dp, cuvant))


def afiseaza_tabela(dp, cuvant):
    n     = len(cuvant)
    linii = []

    header = "     " + "  ".join(f"{cuvant[j]:>8}" for j in range(n))
    linii.append(header)

    for i in range(n):
        rand = f"{cuvant[i]} {i}  "
        for j in range(n):
            if j < i:
                rand += " " * 10
            else:
                continut = "{" + ",".join(sorted(dp[i][j])) + "}"
                rand += f"{continut:>10}"
        linii.append(rand)

    return "\n".join(linii)


if __name__ == "__main__":
    import sys
    fin  = sys.argv[1] if len(sys.argv) > 1 else "input_cyk.txt"
    fout = sys.argv[2] if len(sys.argv) > 2 else "output_cyk.txt"
    cyk(fin, fout)
