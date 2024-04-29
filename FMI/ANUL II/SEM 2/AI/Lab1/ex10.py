# ex10 - Considerându-se o matrice cu n x m elemente binare (0 sau 1) sortate crescător pe linii, să se identifice
# indexul liniei care conține cele mai multe elemente de 1.
# index_max(matrice)
# matrice - matrice de n x m elemente binare, sortate crescator pe linii
# returns: intreg, indicele liniei care contine cei mai multi de 1
def index_max(matrice):
    # se initializeaza o variabila i pentru salvarea index-ului liniei unde se gaseste numarul maxim de elemente 1,
    i = -1
    # una pentru index-ul curent
    k = 0
    # si alta pentru salvarea numarului maxim de elemente de 1
    maxim = 0
    # se parcurge fiecare linie din matrice
    for line in matrice:
        # se parcurge linia de la final spre inceput, cat timp se gaseste o valoare de 1 si se salveaza intr-o variabila
        # n ce reprezinta numarul de elemente 1 gasite
        j = len(line) - 1
        nr = 0
        while line[j] == 1 and j >= 0:
            nr += 1
            j -= 1
        # daca n este mai mare decat maximul, atunci indicele i ia valoarea indicelui curent, iar maximul va lua
        # valoarea n
        if nr > maxim:
            i = k
            maxim = nr
        # se actualizeaza index-ul curent
        k += 1
    # se returneaza index-ul liniei unde se gaseste numarul maxim de elemente 1
    return i


# solutie generata de AI
def index_max_ai(matrice):
    max_1_count = 0
    index_max_1_linie = -1

    for linie in range(len(matrice)):
        count_1 = sum(matrice[linie])
        if count_1 > max_1_count:
            max_1_count = count_1
            index_max_1_linie = linie

    return index_max_1_linie
