def citeste_gramatica(fisier):
    with open(fisier) as f:
        linii = [l.strip() for l in f.readlines() if l.strip()]

    idx = 0
    neterminale = set(linii[idx].split()); idx += 1
    terminale   = set(linii[idx].split()); idx += 1
    nr_prod     = int(linii[idx]);         idx += 1

    productii = {}
    for _ in range(nr_prod):
        parti       = linii[idx].split()
        stanga      = parti[0]
        dreapta_raw = ' '.join(parti[1:])
        if dreapta_raw == 'λ':
            dreapta = []
        else:
            tokeni = parti[1:]
            if len(tokeni) == 1 and len(tokeni[0]) > 1 and tokeni[0] != 'λ':
                dreapta = list(tokeni[0])
            else:
                dreapta = tokeni
        if stanga not in productii:
            productii[stanga] = []
        productii[stanga].append(dreapta)
        idx += 1

    start = linii[idx]
    return neterminale, terminale, productii, start


def elimina_productii_lambda(productii, start):
    nullable = set()

    for nt, prods in productii.items():
        for prod in prods:
            if prod == []:
                nullable.add(nt)

    modificat = True
    while modificat:
        modificat = False
        for nt, prods in productii.items():
            if nt in nullable:
                continue
            for prod in prods:
                if all(s in nullable for s in prod):
                    nullable.add(nt)
                    modificat = True

    noi_productii = {}
    for nt, prods in productii.items():
        noi_productii[nt] = []
        for prod in prods:
            variante = genereaza_variante(prod, nullable)
            for v in variante:
                if v not in noi_productii[nt]:
                    noi_productii[nt].append(v)

    for nt in noi_productii:
        if [] in noi_productii[nt] and nt != start:
            noi_productii[nt].remove([])

    return noi_productii, nullable


def genereaza_variante(productie, nullable):
    variante = [[]]
    for simbol in productie:
        noi = []
        for varianta in variante:
            noi.append(varianta + [simbol])
            if simbol in nullable:
                noi.append(varianta)
        variante = noi
    return variante


def elimina_productii_unitare(productii, neterminale):
    unit_closure = {nt: {nt} for nt in neterminale}

    modificat = True
    while modificat:
        modificat = False
        for nt in neterminale:
            for prod in productii.get(nt, []):
                if len(prod) == 1 and prod[0] in neterminale:
                    b = prod[0]
                    inainte = len(unit_closure[nt])
                    unit_closure[nt] |= unit_closure[b]
                    if len(unit_closure[nt]) > inainte:
                        modificat = True

    noi_productii = {nt: [] for nt in neterminale}
    for nt in neterminale:
        for b in unit_closure[nt]:
            for prod in productii.get(b, []):
                este_unitara = (len(prod) == 1 and prod[0] in neterminale)
                if not este_unitara and prod not in noi_productii[nt]:
                    noi_productii[nt].append(prod)

    return noi_productii


def elimina_simboluri_neproductive(productii, neterminale, terminale):
    productive = set(terminale)

    modificat = True
    while modificat:
        modificat = False
        for nt in neterminale:
            if nt in productive:
                continue
            for prod in productii.get(nt, []):
                if all(s in productive for s in prod):
                    productive.add(nt)
                    modificat = True

    noi_productii = {}
    for nt in neterminale:
        if nt not in productive:
            continue
        noi_productii[nt] = []
        for prod in productii.get(nt, []):
            if all(s in productive for s in prod):
                noi_productii[nt].append(prod)

    return noi_productii, productive & neterminale


def elimina_simboluri_inaccesibile(productii, neterminale, terminale, start):
    accesibile = {start}
    coada = [start]

    while coada:
        simbol = coada.pop()
        for prod in productii.get(simbol, []):
            for s in prod:
                if s not in accesibile:
                    accesibile.add(s)
                    if s in neterminale:
                        coada.append(s)

    noi_productii = {}
    for nt in neterminale:
        if nt in accesibile:
            noi_productii[nt] = productii.get(nt, [])

    noi_neterminale = neterminale & accesibile
    noi_terminale   = terminale   & accesibile

    return noi_productii, noi_neterminale, noi_terminale


def transforma_in_fnc(productii, neterminale, terminale, start):
    counter = [0]
    noi_neterminale = set(neterminale)
    noi_productii   = {}
    terminal_la_nt  = {}

    def nt_nou():
        while True:
            counter[0] += 1
            name = f"X{counter[0]}"
            if name not in noi_neterminale:
                noi_neterminale.add(name)
                return name

    def get_nt_pentru_terminal(t):
        if t not in terminal_la_nt:
            x = nt_nou()
            terminal_la_nt[t] = x
            noi_productii[x]  = [[t]]
        return terminal_la_nt[t]

    for nt, prods in productii.items():
        noi_productii[nt] = []
        for prod in prods:
            if len(prod) == 1:
                noi_productii[nt].append(prod)
            elif len(prod) == 2:
                noua_prod = []
                for s in prod:
                    if s in terminale:
                        noua_prod.append(get_nt_pentru_terminal(s))
                    else:
                        noua_prod.append(s)
                noi_productii[nt].append(noua_prod)
            else:
                prod_cu_nt = []
                for s in prod:
                    if s in terminale:
                        prod_cu_nt.append(get_nt_pentru_terminal(s))
                    else:
                        prod_cu_nt.append(s)
                while len(prod_cu_nt) > 2:
                    x = nt_nou()
                    noi_productii[x] = [[prod_cu_nt[-2], prod_cu_nt[-1]]]
                    prod_cu_nt = prod_cu_nt[:-2] + [x]
                noi_productii[nt].append(prod_cu_nt)

    return noi_productii, noi_neterminale


def transforma_cfg_in_fnc(fisier_input, fisier_output):
    neterminale, terminale, productii, start = citeste_gramatica(fisier_input)

    productii, nullable = elimina_productii_lambda(productii, start)
    productii = elimina_productii_unitare(productii, neterminale)
    productii, neterminale = elimina_simboluri_neproductive(productii, neterminale, terminale)
    productii, neterminale, terminale = elimina_simboluri_inaccesibile(productii, neterminale, terminale, start)
    productii, neterminale = transforma_in_fnc(productii, neterminale, terminale, start)

    with open(fisier_output, 'w') as f:
        for nt, prods in sorted(productii.items()):
            for prod in prods:
                sir = ' '.join(prod) if prod else 'λ'
                f.write(f"{nt} -> {sir}\n")


if __name__ == "__main__":
    import sys
    fin  = sys.argv[1] if len(sys.argv) > 1 else "input_cfg.txt"
    fout = sys.argv[2] if len(sys.argv) > 2 else "output_fnc.txt"
    transforma_cfg_in_fnc(fin, fout)
