# ex8 - Să se genereze toate numerele (în reprezentare binară) cuprinse între 1 și n. De ex. dacă n = 4,
# numerele sunt: 1, 10, 11, 100.
# reprezentare_binara(nr)
# nr - intreg
# returns: un string care reprezinta reprezentarea binara a numarului nr
def reprezentare_binara(nr):
    # se initializeaza un string vid
    rez = ""
    # cat timp numarul este nenul, se adauga la inceputul string-ului rezultat restul impartirii numarului la 2, apoi se
    # continua executia cu catul impartirii numarului la 2
    while nr != 0:
        rez = str(nr % 2) + rez
        nr = nr // 2
    # se returneaza rezultatul
    return rez


# genereaza_binar(n)
# n - intreg
# returns: un string care contine toate reprezentarile binare ale numarelor de la 1 la n
def genereaza_binar(n):
    # se initializeaza un string vid in care se va tine minte rezultatul
    rez = ""
    # se parcurg numerele de la 1 la n, iar in string-ul rezultat se adauga reprezentarea binara a fiecarui numar
    for i in range(n + 1):
        rez += reprezentare_binara(i) + " "
    # se returneaza string-ul rezultat fara utimul spatiu
    return rez.strip()


# solutie generata de AI
def binar(numar):
    if numar == 0:
        return '0'

    rezultat = ''
    while numar > 0:
        rezultat = str(numar % 2) + rezultat
        numar //= 2

    return rezultat


def genereaza_binar_ai(n):
    numere_string = ""
    for i in range(1, n + 1):
        numar_binar = binar(i)
        numere_string += numar_binar + " "
    # Eliminăm ultimul spațiu adăugat
    numere_string = numere_string.strip()
    return numere_string
