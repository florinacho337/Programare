# ex7 - Să se determine al k-lea cel mai mare element al unui șir de numere cu n elemente (k < n). De ex. al 2-lea
# cel mai mare element din șirul [7,4,6,3,9,1] este 7.
# merge_sort(lista)
# lista - lista de intregi
# returns: lista sortata descrescator prin interclasare
def merge_sort(lista):
    # daca lista are cel mult un element, se returneaza lista
    if len(lista) <= 1:
        return lista
    # altfel
    # se alege un mijloc si se separa lista in 2 subliste
    mid = len(lista) // 2
    stanga = lista[:mid]
    dreapta = lista[mid:]

    # se aplica sortarea pentru subliste
    stanga = merge_sort(stanga)
    dreapta = merge_sort(dreapta)
    # se returneaza rezultatul interclasarii celor doua liste sortate
    return merge(stanga, dreapta)


# merge(stanga, dreapta)
# stanga - lista de intregi
# dreapta - lista de intregi
# returns: o lista de intregi care contin elementele celor doua liste stanga si dreapta, ordonate descrescator
def merge(stanga, dreapta):
    # se initializeaza o lista rezultat, la inceput vida
    rez = []
    # se parcurg simultan cele doua liste date ca parametrii
    i = j = 0
    while i < len(stanga) and j < len(dreapta):
        # daca elementul de pe pozitia i din prima lista este mai mic decat elementul de pe pozitia j din a doua lista,
        # in lista rezultat se adauga elementul din a doua lista si se incrementeaza j-ul
        if stanga[i] < dreapta[j]:
            rez.append(dreapta[j])
            j += 1
        # altfel se adauga in lista rezultat elementul din prima lista si se incrementeaza i-ul
        else:
            rez.append(stanga[i])
            i += 1

    # se adauga restul elementelor din lista in care au mai ramas elemente in lista rezultat
    while i < len(stanga):
        rez.append(stanga[i])
        i += 1

    while j < len(dreapta):
        rez.append(dreapta[j])
        j += 1
    # se returneaza lista rezultat
    return rez


# al_k_lea_cel_mai_mare(v, k)
# v - lista de intregi
# k - intreg
# returns: False, daca k este mai mare decat lungimea listei v - 1
#          al k-lea cel mai mare element din lista v
def al_k_lea_cel_mai_mare(v, k):
    # daca k este un numar mai mare decat lungimea listei v, nu se poate afla al k-lea cel mai mare element din lista v
    # deci se returneaza False
    if k > len(v):
        return False
    # se sorteaza lista v si se returneaza elementul de pe indexul k - 1
    v = merge_sort(v)
    return v[k - 1]


# solutie generata de AI
def sortare_descrescatoare(nums):
    # Implementăm algoritmul de sortare în ordine descrescătoare (de exemplu, folosind algoritmul bubble sort)
    n = len(nums)
    for i in range(n):
        for j in range(0, n - i - 1):
            if nums[j] < nums[j + 1]:
                nums[j], nums[j + 1] = nums[j + 1], nums[j]


# solutie generata de AI
def al_k_lea_cel_mai_mare_ai(nums, k):
    if k > len(nums):
        return False

    # Sortăm lista în ordine descrescătoare
    sortare_descrescatoare(nums)

    # Returnăm al k-lea cel mai mare element
    return nums[k - 1]
