% Noduri si valori pentru o functie reala
x_vals = linspace(0, 4, 3);  % Noduri (aproximare degradata)
%x_vals = linspace(0, 4, 10);  % Noduri

y_vals = exp(-x_vals);  % Valori reale ale functiei f(x) = e^{-x}

% Gradul polinomului
n = 3;  % Gradul polinomului

% Domeniul de afisare
x_range = linspace(min(x_vals), max(x_vals), 500);
y_range = arrayfun(@(x) mcmmp(x_vals, y_vals, n, x), x_range);
f_real = exp(-x_range);  % Functia reala pentru comparatie

% Afisare grafica
figure;
plot(x_range, y_range, 'b-', 'LineWidth', 1.5);
hold on;
plot(x_range, f_real, 'g--', 'LineWidth', 1.5);
scatter(x_vals, y_vals, 'ro', 'filled');
title('Aproximare cu metoda celor mai mici patrate vs. Functia reala: f(x) = e^{-x}');
xlabel('x');
ylabel('P(x) si f(x)');
grid on;
legend('Polinom MCMMP', 'Functie reala', 'Noduri de interpolare');

