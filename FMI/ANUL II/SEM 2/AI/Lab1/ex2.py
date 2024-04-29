import math


# ex2 - Să se determine distanța Euclideană între două locații identificate prin perechi de numere. De ex. distanța
# între (1,5) și (4,1) este 5.0
# distanta(p1, p2)
# p1 - vector cu 2 elemente [x1, y1]
# p2 - vector cu 2 elemente [x2, y2]
# returns: False, daca len(p1) != 2 sau len(p2) != 2
#          distanta Euclideană intre punctele p1 si p2, altfel
def distanta(p1, p2):
    # daca len(p1) == len(p2) == 2 atunci calculeaza si returneaza distanta
    if len(p1) == len(p2) == 2:
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
    # altfel returneaza False
    return False


# solutie generata de AI
def distanta_ai(p1, p2):
    if len(p1) == len(p2) == 2:
        x1, y1 = p1
        x2, y2 = p2
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return False
