% nodes = linspace(-pi, pi, 5); % aproximare mai putin precisa
nodes = linspace(-pi, pi, 10); % >5 - aproximare precisa

original_function = @(x) sin(x);

y = original_function(nodes);

xx = linspace(min(nodes), max(nodes), 200);

interpolated_values = baryLagrange(nodes, y, xx);

figure;

plot(xx, interpolated_values, '-b', 'LineWidth', 1.5);
hold on;

plot(xx, original_function(xx), '--k', 'LineWidth', 1, 'HandleVisibility', 'off');

plot(nodes, y, 'or', 'MarkerSize', 8, 'LineWidth', 1.5);

title('Polinom de Interpolare Lagrange Baricentrica');
xlabel('x');
ylabel('f(x) / P(x)');

legend('Polinom de Interpolare', 'Noduri de Interpolare');

hold off;

grid on;

% 14. Ajusteaza limitele axelor (optional, pentru o vizualizare mai buna)
xlim([min(nodes), max(nodes)]);
ylim([min(y)-0.5, max(y)+0.5]);
