def crescator(a, b):
    return a < b


def relativ_prim_intre_ele(a, b):
    while b:
        aux = a % b
        a = b
        b = aux
    return a == 1


def proprietate1(lst):
    i = 0
    f = 1
    lungime_max = 1
    while f <= len(lst):
        if f < len(lst) and relativ_prim_intre_ele(lst[f - 1], lst[f]):
            f = f + 1
        else:
            lungime = f - i
            if lungime > lungime_max:
                lungime_max = lungime
                rez = lst[i: f]
            i = f
            f = i + 1
    return rez


def proprietate3(lst):
        i = 0
        f = 1
        lungime_max = 1
        while f <= len(lst):
            if f < len(lst) and crescator(lst[f - 1], lst[f]):
                f = f + 1
            else:
                lungime = f - i
                if lungime > lungime_max:
                    lungime_max = lungime
                    rez = lst[i: f]
                i = f
                f = i + 1
        return rez


def modulul_diferentei(a, b):
    rez = a - b
    if rez < 0:
        return rez * -1
    else:
        return rez


def este_prim(a):
    d = 2
    nr_div = 1
    while a > 1:
        p = 0
        while a % d == 0:
            p = p + 1
            a = a / d
        nr_div = nr_div * (p+1)
        d = d + 1
        if d * d > a:
            d = a
    return nr_div == 2


def proprietate2(lst):
    i = 0
    f = 1
    lungime_max = 1
    rez = []
    while f <= len(lst):
        if f < len(lst) and este_prim(modulul_diferentei(lst[f - 1], lst[f])):
            f = f + 1
        else:
            lungime = f - i
            if lungime > lungime_max:
                lungime_max = lungime
                rez = lista[i: f]
            i = f
            f = i + 1
    return rez


def introducere_lista(lst):
    n = int(input("Cate elemente doresti sa aiba lista? "))
    print("Introdu, pe rand, elementele listei:")
    for i in range(0, n):
        el = int(input())
        lst.append(el)


def ruleaza_teste_relativ_prim_intre_ele():
    print("Se realizeaza testele...\n")
    assert(proprietate1([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5])
    assert(proprietate1([1, 4, 6, 2, 10, 3, 5, 7]) == [10, 3, 5, 7])
    assert(proprietate1([5, 10, 11, 13, 17, 20, 6]) == [10, 11, 13, 17, 20])
    print("Teste finalizate cu succes!\n")


ruleaza_teste_relativ_prim_intre_ele()


n = int(input("Alegeti o optiune: \n1.Citeste o lista de numere intregi\n5.Iesi din program\n"))

while not(n == 5):
    if n == 1:
        lista = []
        introducere_lista(lista)
        rez = []
    n = int(input("Alegeti o optiune:\n1.Citeste o noua lista de numere intregi\n2.Gaseste secventa de lungime maxima cu proprietatea ca oricare doua elemente consecutive sunt relativ prime intre ele\n3.Gaseste secventa de lungime maxima cu proprietatea ca oricare doua elemente consecutive difera printr-un numar prim\n4.Gaseste secventa de lungime maxima cu proprietatea x[i] < x[i+1] < ... < x[i+p]\n5.Iesi din program\n"))
    if n == 2:
        print(proprietate1(lista))
    if n == 3:
        print(proprietate2(lista))
    if n == 4:
        print(proprietate3(lista))
