# ex3 - Să se determine produsul scalar a doi vectori rari care conțin numere reale. Un vector este rar atunci când
# conține multe elemente nule. Vectorii pot avea oricâte dimensiuni. De ex. produsul scalar a 2 vectori
# unidimensionali [1,0,2,0,3] și [1,2,0,3,1] este 4.
# produs_scalar(v1, v2)
# v1 - vector de numere
# v2 - vector de numere
# returns: False, daca len(v1) != len(v2)
#          produsul scalar al vectorilor v1 si v2
def produs_scalar(v1, v2):
    # daca lungimile celor 2 vectori sunt diferite returneaza False
    if len(v1) != len(v2):
        return False
    # se face produsul scalar al vectorilor
    x = 0
    for i in range(len(v1)):
        x += v1[i] * v2[i]
    return x


# solutie generata de AI
def produs_scalar_ai(vector1, vector2):
    # Verificăm dacă vectorii au aceeași lungime
    if len(vector1) != len(vector2):
        return False

    # Inițializăm suma produselor
    suma_produse = 0

    # Parcurgem elementele non-nule ale ambilor vectori
    for elem1, elem2 in zip(vector1, vector2):
        # Dacă ambele elemente sunt non-nule, înmulțim și adăugăm la suma produselor
        if elem1 != 0 and elem2 != 0:
            suma_produse += elem1 * elem2

    return suma_produse
