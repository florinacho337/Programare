from sympy import *
import matplotlib.pyplot as plt
import numpy as np
from math import factorial

def maclaurin_sym(f, n):
    x = Symbol('x')
    return sum(f.diff(x, k).subs(x, 0) / factorial(k) * x**k for k in range(n))

def maclaurin_num(x, d):
    Pn = np.zeros_like(x, dtype=float)
    for k in range(len(d)):
        Pn += (d[k] / factorial(k)) * (x**k)
    return Pn


if __name__ == '__main__':
    x = Symbol('x')
    f = sin(x)
    n = 10
    print(maclaurin_sym(f, n))


    d = [0, 1, 0, -1, 0, 1, 0, -1, 0, 1, 0]

    x_vals = np.linspace(-5, 5, 400)
    maclaurin_sin = maclaurin_num(x_vals, d)

    plt.figure(figsize=(8, 6))
    plt.plot(x_vals, np.sin(x_vals), label="sin(x)", linestyle='dashed')
    plt.plot(x_vals, maclaurin_sin, label="MacLaurin (n=10)", color='red')
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.title("Aproximarea lui sin(x) cu polinomul MacLaurin de ordin 10")
    plt.legend()
    plt.grid()
    plt.show()