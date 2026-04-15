% Noduri si valori
x_vals = [-pi, -3*pi/4, -pi/2, -pi/4, 0, pi/4, pi/2, 3*pi/4, pi];  % Noduri
% x_vals = [-pi, 0, pi];  % Noduri (aproximare mai degradata)
y_vals = exp(-x_vals) .* sin(x_vals);  % Valori ale functiei
dy_vals = exp(-x_vals) .* (cos(x_vals) - sin(x_vals));  % Derivatele functiei

% Domeniul de afisare
x_range = linspace(-4, 4, 500);
y_range = arrayfun(@(x) hermite_interpolation(x_vals, y_vals, dy_vals, x), x_range);

f_real = exp(-x_range) .* sin(x_range);

% Afisare grafica
figure;
plot(x_range, y_range, 'b-', 'LineWidth', 1.5);
hold on;
plot(x_range, f_real, 'g--', 'LineWidth', 1.5);
scatter(x_vals, y_vals, 'ro', 'filled');
title('Interpolare Hermite folosind metoda Powell');
xlabel('x');
ylabel('P(x) si f(x)');
grid on;
legend('Polinom Hermite', 'Functie reala', 'Noduri de interpolare');
