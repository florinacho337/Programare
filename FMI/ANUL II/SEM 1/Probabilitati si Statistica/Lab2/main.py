# 1a
import random
from math import dist

import matplotlib.pyplot as plt
from matplotlib.pyplot import axis, plot

def genereaza(n):
    d = {}
    for count in range(n):
        nr = random.randint(1, 366)
        if nr not in d:
            d[nr] = 1
        else:
            d[nr] += 1
    return d


k = 0
# 50 de repetari
for j in range(100):
    check = False
    date_de_nastere = genereaza(23)
    for data in date_de_nastere:
        if date_de_nastere[data] >= 2:
            check = True
    if check:
        k += 1
print(f"Probabilitatea pentru 100 incercari este: {k/100}")
k = 0
for j in range(1000):
    check = False
    date_de_nastere = genereaza(23)
    for data in date_de_nastere:
        if date_de_nastere[data] >= 2:
            check = True
    if check:
        k += 1
print(f"Probabilitatea pentru 1000 incercari este: {k/1000}")
k = 0
for j in range(10000):
    check = False
    date_de_nastere = genereaza(23)
    for data in date_de_nastere:
        if date_de_nastere[data] >= 2:
            check = True
    if check:
        k += 1
print(f"Probabilitatea pentru 10000 incercari este: {k/10000}")
k = 0
for j in range(100000):
    check = False
    date_de_nastere = genereaza(23)
    for data in date_de_nastere:
        if date_de_nastere[data] >= 2:
            check = True
    if check:
        k += 1
print(f"Probabilitatea pentru 100000 incercari este: {k/100000}")


# 1b
q = 1
for i in range(23):
    q *= (365-i) / 365
print(f"Probabilitatea este: {1-q}")
