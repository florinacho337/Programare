# ex9 - Considerându-se o matrice cu n x m elemente întregi și o listă cu perechi formate din coordonatele a 2 căsuțe
# din matrice ((p,q) și (r,s)), să se calculeze suma elementelor din sub-matricile identificate de fieare pereche.
# suma_submatrice(matrice, pereche)
# matrice - matrice m x n elemente numere intregi
# pereche - pereche de coordonate data sub forma [[a, b], [c, d]]
# returns: un intreg reprezentand suma elementelor din matrice determinate de coordonatele [a, b] si [c, d]
def suma_submatrice(matrice, pereche):
    # daca coordonatele perechii pereche nu sunt incluse in matrice, atunci se returneaza 0
    if (pereche[0][0] > len(matrice) or pereche[0][1] > len(matrice[0]) or pereche[1][0] > len(matrice) or pereche[1][1]
            > len(matrice[0])):
        return False
    # se initializeaza o variabila suma cu 0
    suma = 0
    # se parcug elementele submatricii determinate de perechea de coordonate si se adauga la suma
    for i in range(pereche[0][0], pereche[1][0] + 1):
        for j in range(pereche[0][1], pereche[1][1] + 1):
            suma += matrice[i][j]
    # se returneaza suma
    return suma


# suma_submatrice_main(matrice, perechi)
# matrice - matrice m x n elemente numere intregi
# perechi - lista de perechi (data sub forma [p1, p2..., pn], unde pi = [[a, b], [c, d]]
# returns: o lista cu rezultatele sumelor generate de numerele din submatricile determinate de perechi
def suma_submatrice_main(matrice, perechi):
    # se initializeaza o lista vida
    rez = []
    # pentru fiecare pereche din lista de perechi se salveaza in lista rezultat suma determinata de coordonatele din
    # perechea respectiva
    for p in perechi:
        rez.append(suma_submatrice(matrice, p))
    # se returneaza lista rezultat
    return rez


# solutie generata de AI
def suma_submatrice_main_ai(matrice, liste_coord):
    sume = []
    for coord1, coord2 in liste_coord:
        p, q = coord1
        r, s = coord2

        # Verificăm dacă cel puțin una dintre coordonate este în afara matricei
        if p < 0 or p >= len(matrice) or q < 0 or q >= len(matrice[0]) or r < 0 or r >= len(
                matrice) or s < 0 or s >= len(matrice[0]):
            sume.append(False),
            continue

        suma_submatrice1 = 0
        for i in range(p, r + 1):
            for j in range(q, s + 1):
                suma_submatrice1 += matrice[i][j]

        sume.append(suma_submatrice1)

    return sume
