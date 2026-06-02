from collections import deque

def citeste_pda(fisier_input):
    with open(fisier_input) as f:
        linii = [l.strip() for l in f.readlines() if l.strip()]

    idx = 0
    stari = set(linii[idx].split()); idx += 1
    alfabet = set(linii[idx].split()); idx += 1
    nr_tranzitii = int(linii[idx]); idx += 1

    tranzitii = []
    for _ in range(nr_tranzitii):
        parti = linii[idx].split()
        stare_cur    = parti[0]
        simbol_citit = parti[1]
        simbol_varf  = parti[2]
        stare_urm    = parti[3]
        sir_stiva    = parti[4]
        tranzitii.append((stare_cur, simbol_citit, simbol_varf, stare_urm, sir_stiva))
        idx += 1

    stare_initiala       = linii[idx]; idx += 1
    simbol_initial_stiva = linii[idx]; idx += 1
    stari_finale         = set(linii[idx].split()); idx += 1
    mod_acceptare        = linii[idx]; idx += 1
    cuvant               = linii[idx]; idx += 1

    if cuvant == 'λ':
        cuvant = ''

    return stari, alfabet, tranzitii, stare_initiala, simbol_initial_stiva, stari_finale, mod_acceptare, cuvant


def simuleaza_pda(fisier_input):
    stari, alfabet, tranzitii, stare_init, simbol_init_stiva, stari_finale, mod, cuvant = citeste_pda(fisier_input)

    config_init = (stare_init, 0, (simbol_init_stiva,))
    coada    = deque([config_init])
    vizitate = set([config_init])

    while coada:
        stare, poz, stiva = coada.popleft()

        if poz == len(cuvant):
            if verifica_acceptare(stare, stiva, stari_finale, mod):
                return "Acceptat"

        for (st_cur, sim_citit, sim_varf, st_urm, sir_stiva) in tranzitii:
            if st_cur != stare:
                continue
            if not stiva or stiva[0] != sim_varf:
                continue

            if sim_citit == 'λ':
                new_poz = poz
            else:
                if poz >= len(cuvant) or cuvant[poz] != sim_citit:
                    continue
                new_poz = poz + 1

            stiva_noua = list(stiva[1:])
            if sir_stiva != 'λ':
                stiva_noua = list(sir_stiva) + stiva_noua
            stiva_noua = tuple(stiva_noua)

            new_config = (st_urm, new_poz, stiva_noua)
            if new_config not in vizitate:
                vizitate.add(new_config)
                coada.append(new_config)

    return "Respins"


def verifica_acceptare(stare, stiva, stari_finale, mod):
    in_stare_finala = stare in stari_finale
    stiva_goala     = len(stiva) == 0

    if mod == "stare finala":
        return in_stare_finala
    elif mod == "stiva goala":
        return stiva_goala
    elif mod == "ambele":
        return in_stare_finala and stiva_goala
    return False


if __name__ == "__main__":
    import sys
    fisier = sys.argv[1] if len(sys.argv) > 1 else "input_pda.txt"
    print(simuleaza_pda(fisier))
