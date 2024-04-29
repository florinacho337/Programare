# ex6 - Pentru un șir cu n numere întregi care conține și duplicate, să se determine elementul majoritar (care apare
# de mai mult de n / 2 ori). De ex. 2 este elementul majoritar în șirul [2,8,7,2,2,5,2,3,1,2,2].
# element_majoritar(vector)
# vector - vector de numere
# returns: valoarea care apare > len(vector) / 2, daca exista o astfel de valoare
#          False, altfel
def element_majoritar(vector):
    # se numara aparitiile numerelor si se salveaza intr-un dictionar ale caror chei sunt numerele
    aparitii_numere = {}
    for nr in vector:
        if nr in aparitii_numere:
            aparitii_numere[nr] += 1
        else:
            aparitii_numere[nr] = 1
    # se returneaza numarul care are aparitiile > lungimea vectorului / 2
    for c in aparitii_numere:
        if aparitii_numere[c] > len(vector) // 2:
            return c
    # daca nu exista un astfel de numar se returneaza False
    return False


# solutie generata de AI
def element_majoritar_ai(nums):
    candidate = None
    count = 0

    # Identificăm candidatul pentru elementul majoritar
    for num in nums:
        if count == 0:
            candidate = num
            count = 1
        elif num == candidate:
            count += 1
        else:
            count -= 1

    # Verificăm dacă candidatul este elementul majoritar
    count = 0
    for num in nums:
        if num == candidate:
            count += 1
    if count > len(nums) // 2:
        return candidate
    else:
        return False
