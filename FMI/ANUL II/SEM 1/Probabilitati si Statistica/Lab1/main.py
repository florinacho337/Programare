from itertools import permutations, combinations
from math import factorial, perm, comb
from random import sample


def aranjamente(cuv, numar, numar_total=False, aleator=False):
    if numar_total:
        print("Numarul de aranjamente: " + f"{perm(len(cuv), numar)}")
    elif aleator:
        print("Un aranjament aleatoar este: " + str(sample(cuv, numar)))
    else:
        for i in list(permutations(cuv, numar)):
            print(i)


def combinari(cuv, numar, numar_total=False, aleator=False):
    if numar_total:
        print("Numarul de combinari: " + f"{comb(len(cuv), numar)}")
    elif aleator:
        print("O combinare aleatoare este: " + str(sample(cuv, numar)))
    else:
        for i in list(combinations(cuv, numar)):
            print(i)

# # Afisati o lista cu toate permutarile cuvantului word
# cuvant = input("Introduceti un cuvant: ")
# permutari = permutations(cuvant, len(cuvant))
# print("Permutari:")
# for p in list(permutari):
#     print(p)
#
# # Afisati nr total al permutarilor cuvantului word
# nr = factorial(len(cuvant))
# print("Numarul de permutari: " + f"{nr}")
#
# # Afisati o permutare aleatoare a cuvantului word
# print("O permutare aleatoare este: " + str(sample(cuvant, len(cuvant))))

# Functii


print(aranjamente('word', 2))
print(aranjamente('word', 2, numar_total=True))
print(aranjamente('word', 2, aleator=True))
print(combinari('word', 2))
print(combinari('word', 2, numar_total=True))
print(combinari('word', 2, aleator=True))
