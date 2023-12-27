n = int(input("Introduceti un numar: "))

p = 1
d = 2
are_factori_proprii = False
while d * d < n:
    if n % d == 0:
        p = p*d*int(n/d)
        are_factori_proprii = True
    d = d+1
if d*d == n:
    p = p*d
    are_factori_proprii = True
if not(are_factori_proprii):
    print("Numarul nu are factori proprii!")
else:
    print("Produsul factorilor proprii ai numarului " + str(n) + " este " + str(p) + ".")
