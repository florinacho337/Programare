from scipy.stats import norm, expon, uniform
from scipy.integrate import quad
from numpy import mean, std, linspace, multiply, exp
from matplotlib.pyplot import show, hist, grid, legend, xticks, plot
import math

#1

data = norm.rvs(loc=165, scale=10, size=5000)
hist(data, bins=16, range=(130, 210), density=True, alpha=0.5)
x = linspace(130, 210)
plot(x, norm.pdf(x, loc=165, scale=10))


print("Valoarea medie simulata: " + str(data.mean()))
print("Deviatia standard simulata: " + str(data.std()))
print("Proportia in intervalul [160, 170]: " + str(mean((data >= 160) & (data <= 170))))

grid()
legend()
xticks(range(130, 211, 10))
show()
print("----------------")
#2
x1 = expon.rvs(loc=0, scale=5, size=10000)
x2 = uniform.rvs(loc=4, scale=2, size=10000)
# mean_t = multiply(0.4, x1.mean()) + multiply(0.6, x2.mean())
# std_t = multiply(0.4, x1.std()) + multiply(0.6, x2.std())

k = 0.4*x1 + 0.6*x2
print("Valoarea medie a timpului de printare: " + str(mean(k)) + " secunde")
print("Deviatia standard a timpului de printare: " + str(std(k)) + " secunde")

# pb1 = 0
# for n in len(mean_t):
#     if n < 5:
#         pb1 += 1
print("Probabilitatea ca timpul de printare sa fie mai mic de 5 sec este: " + str(mean(k<5.0)))
# print(mean(x<5.0))
probabilitate = 0.4*expon.cdf(5, loc=0, scale=5) + 0.6 * (5-4)/(6-4)
print("Probabilitatea teoretica ca timpul de printare sa fie mai mic de 5 sec este: " + str(probabilitate))

print("---------------------")
#3
def f(k):
    return exp(-k ** 2)


samples = uniform.rvs(loc=-1, scale=4, size=5000)
values = f(samples)

monte_carlo = (3 - (-1)) * mean(values)

integral, _ = quad(f, -1, 3)
print("Estimarea Monte Carlo a integralei: " + str(monte_carlo))
print("Valoarea exacta a integralei: " + str(integral))



