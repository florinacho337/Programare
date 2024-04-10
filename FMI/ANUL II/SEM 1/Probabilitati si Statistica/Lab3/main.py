from itertools import product
from random import choices, sample, randrange
from math import comb, perm
from matplotlib.pyplot import bar, hist, grid, show, legend
from scipy.stats import binom

# 1.i)
favorabile = 0
posibile = 0
for i in range(1000):
    bile_existente = sample(['red', 'blue', 'green'], counts=[5, 3, 2], k=3)
    if 'red' in bile_existente:
        posibile = posibile + 1
    toate_rosii = True
    for culoare in bile_existente:
        if culoare != 'red':
            toate_rosii = False

    if toate_rosii:
        favorabile = favorabile + 1

print(favorabile / posibile)

# print(choices(bile_existente))
# 1.ii)
# P(B|A) = P(B intersectat A) / P(A)
# P(B intersectat A) = comb(5, 3) / comb(10, 3)
favorabile = comb(5,3) / comb(10, 3)
# P(A) = 1 - P(A') = 1 - comb(5, 3)/comb(10, 3)
posibile = 1 - comb(5, 3) / comb(10, 3)
# P(B|A)
rezultat = favorabile / posibile
print(rezultat)

# 2
data = [randrange(1, 7) for _ in range(500)]
bin_edges = [k+0.5 for k in range(7)]
hist(data, bin_edges, density=True, rwidth=0.9, color='green', edgecolor='black', alpha=0.5, label='frecvente relative')

distribution = dict([(i, 1/6) for i in range(1, 7)])

bar(distribution.keys(), distribution.values(), width=0.85, color='red', edgecolor='black', alpha=0.6, label='probabilitati')

legend(loc='lower left')
grid()
show()

# 3
n = 5
p = 0.6
X = binom.rvs(n, p, size=1000)
# a
print(X)


# b
def pb3():
    bin_edges = [k+0.5 for k in range(-1, 6)]
    hist(X, bin_edges, density=True, rwidth=0.9, color='green', edgecolor='black', alpha=0.5, label='frecvente relative')
    distribution = dict([(i, binom.pmf(i, n, p)) for i in range(6)])

    bar(distribution.keys(), distribution.values(), width=0.85, color='red', edgecolor='black', alpha=0.6, label='probabilitati')
    legend(loc='lower left')
    grid()
    show()


pb3()

# c

print(binom.cdf(5, n, p) - binom.cdf(2, n, p))
# 4
data = [sum(choices(range(1, 7), k=3)) for k in range(1000)]
bin_edges = [k+0.5 for k in range(2, 19)]
hist(data, bin_edges, density=True, rwidth=0.9, color='green', edgecolor='black', alpha=0.5, label='frecvente relative')
distribution = dict([i, 0] for i in range(3, 19))
for z in product(range(1, 7), repeat=3):
    distribution[sum(z)] += 1/216

bar(distribution.keys(), distribution.values(), width=0.85, color='red', edgecolor='black', alpha=0.6, label='probabilitati')
legend(loc='lower left')
grid()
show()

