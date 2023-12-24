import numpy as np
from matplotlib.pyplot import show, hist, grid, xticks, plot
from scipy.stats import expon

import matplotlib.pyplot as plt
from scipy.stats import rv_discrete


def generate_discrete_random_numbers(x_values, probabilities, n):
    # Verificare lungimea listelor
    if len(x_values) != len(probabilities):
        raise ValueError("Listele x_values și probabilities trebuie să aibă aceeași lungime.")

    # Creare distribuție discretă
    xk = np.arange(len(x_values))  # Asociem fiecărei grupe sanguine un index numeric
    pk = np.array(probabilities)
    custm = rv_discrete(name='custm', values=(xk, pk))

    # Generare N numere pseudo-aleatoare
    random_numbers = custm.rvs(size=n)

    return random_numbers


# Distribuția pentru grupa sanguină
grupa_sanguina_valori = ['0', 'A', 'B', 'AB']
grupa_sanguina_probabilitati = [0.46, 0.4, 0.1, 0.04]

# Numărul de simulări
N = 1000

# Generare de N ori observarea grupei sanguine
observatii_grupa_sanguina = generate_discrete_random_numbers(grupa_sanguina_valori, grupa_sanguina_probabilitati, N)

# Calcularea frecvenței relative a apariției fiecărei grupe sanguine
frecventa_relativa = [np.sum(observatii_grupa_sanguina == grupa) / N for grupa in np.arange(len(grupa_sanguina_valori))]

# Afisarea histogramelor
plt.bar(grupa_sanguina_valori, frecventa_relativa, color='black', alpha=0.7, label='Observat')
plt.bar(grupa_sanguina_valori, grupa_sanguina_probabilitati, color='blue', alpha=0.5, label='Teoretic')

plt.xlabel('Grupa Sanguina')
plt.ylabel('Frecventa Relativa')
plt.title('Simulare Grupa Sanguina')
plt.legend()
plt.show()

# Parametrul pentru distribuția exponențială
alpha = 1 / 12

# Numărul de simulări
N = 1000

# Generare de N ori timpul de printare cu distribuția exponențială
data = - (1 / alpha) * np.log(1 - np.random.uniform(0, 1, N))

# Afișare histogramă
hist(data, bins=12, density=True, range=(0, 60))
x = np.linspace(0, 60, 1000)
plot(x, expon.pdf(x, loc=0, scale=1 / alpha), 'r-')
xticks(range(0, 60, 5))
grid()

# Estimare probabilitate pentru evenimentul E
probabilitate_E_estimata = np.sum(data >= 5) / N
print(f"Estimarea probabilității pentru evenimentul E: {probabilitate_E_estimata:.4f}")

# Calculare probabilitate teoretică pentru evenimentul E
probabilitate_E_teorica = 1 - expon.cdf(5, loc=0, scale=1 / alpha)
print(f"Probabilitatea teoretică pentru evenimentul E: {probabilitate_E_teorica:.4f}")

# Afișare
show()
