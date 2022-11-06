def f(x):
    if x < 1995:
        return (x*x)/(6+f(x+2))
    else:
        return 0


pi = 3 + f(1)
print(pi)