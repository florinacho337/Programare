from scipy.stats import bernoulli, hypergeom, geom
from matplotlib.pyplot import hist, grid, show, legend


# i)
def mersaleator(p, nr_pasi):
    pozitii = [0]
    for _ in range(nr_pasi):
        x = bernoulli.rvs(p)
        pas = 2 * x - 1
        pozitii.append(pozitii[-1] + pas)
    return pozitii


print(mersaleator(0.5, 10))


# ii)
def deplasareLinie():
    data = [mersaleator(0.5, 10)[-1] for _ in range(500)]
    bin_edges = [k+0.5 for k in range(-10, 11)]
    hist(data, bin_edges, density=False, rwidth=0.9, color='green', edgecolor='black', alpha=0.5,
         label='pozitii finale')

    legend(loc='lower left')
    grid()
    show()


deplasareLinie()


# iii)
def deplasareCerc(n):
    data = [mersaleator(0.5, 11)[-1] % n for _ in range(500)]
    bin_edges = [k + 0.5 for k in range(-1, n)]
    hist(data, bin_edges, density=False, rwidth=0.9, color='green', edgecolor='black', alpha=0.5,
         label='pozitii finale')

    legend(loc='lower left')
    grid()
    show()


deplasareCerc(7)

# 2
p = 0
for i in range(3, 7):
    p += hypergeom.pmf(i, 49, 6, 6)
print("Lista biletelor necastigatoare:")
z = geom.rvs(p, size=500)
print(z)

nr = 0
for n in z:
    if n >= 10:
        nr += 1
print(
    "Estimare cel putin 10 bilete succesive sa fie necastigatoare pana cand jucatorul primeste un bilet castigator: " + str(
        nr / z.size))
print(
    "Probabilitatea ca cel putin 10 bilete succesive sa fie necastigatoare pana cand jucatorul primeste un bilet castigator: " + str(
        1 - geom.cdf(9, p)))
