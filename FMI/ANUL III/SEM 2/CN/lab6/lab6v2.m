% Definim nodurile și valorile funcției în acele noduri
x_nodes = [1, 2, 3, 4, 5]; % Nodurile de interpolare
f_nodes = [1, 4, 9, 4, 1]; % Valorile funcției în noduri

% Interval de plotare
x_plot = linspace(min(x_nodes), max(x_nodes), 100);
y_plot = arrayfun(@(x) aitken_interpolation(x_nodes, f_nodes, x, 1e-6), x_plot);

% Punctul unde vrem să interpolăm
x_interp = 2.5;
f_interp = aitken_interpolation(x_nodes, f_nodes, x_interp, 1e-6);

% Desenăm nodurile și curba de interpolare
figure;
hold on;
plot(x_nodes, f_nodes, 'ro', 'MarkerSize', 8, 'LineWidth', 2); % Punctele nodurilor
plot(x_plot, y_plot, 'b-', 'LineWidth', 2); % Curba interpolată
plot(x_interp, f_interp, 'g*', 'MarkerSize', 10, 'LineWidth', 2); % Punctul interpolat
legend('Noduri de interpolare', 'Interpolare Aitken', 'Punct interpolat', 'Location', 'Best');
xlabel('x');
ylabel('f(x)');
title('Interpolare utilizând metoda lui Aitken');
grid on;
hold off;

