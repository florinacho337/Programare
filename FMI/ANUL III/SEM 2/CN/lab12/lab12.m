% --- Rezolvare ecuatie sin(x) - cos(x) = 4 * x prin metoda aproximatiilor succesive ---
disp('Rezolvare ecuatie sin(x) - cos(x) = 4 * x prin metoda aproximatiilor succesive');

% Rescriem ecuatia sub forma x = g(x)
g = @(x) (sin(x) - cos(x)) / 4;

disp('Punct initial: 0.5');
x0 = 0.5;
[z, ni] = succesive_aprox(g, x0);

fprintf('Solutia aproximata: %12.10f\n', z);
fprintf('Numar iteratii: %d\n', ni);

disp('Daca mutam mebrul drept al ecuatiei in stanga si inlocuim valoarea aproximata in aceasta, ar trebui sa obtinem o valoare cat mai apropiata de 0.');
eroare = sin(z) - cos(z) - 4*z;
fprintf('Eroare: %e\n\n', eroare);

% --- EX 2, Sectiunea 2.4, fisier ECUA.pdf ---
disp('EX 2, Sectiunea 2.4, fisier ECUA.pdf');
% Definirea functiilor
f = @(x) [ 9*x(1)^2 + 36*x(2)^2 + 4*x(3)^2 - 36;
           x(1)^2 - 2*x(2)^2 - 20*x(3);
           x(1)^2 - x(2)^2 + x(3)^2 ];

% Jacobian
fd = @(x) [ 18*x(1), 72*x(2), 8*x(3);
            2*x(1), -4*x(2), -20;
            2*x(1), -2*x(2), 2*x(3) ];

x0_list = [1, 1, 0; 1, -1, 0; -1, 1, 0; -1, -1, 0];

for i=1:size(x0_list,1)
    x0 = x0_list(i,:)';
    J = fd(x0);
    lambda = -J \ eye(3); % inversa lui Jacobian în x0

    g = @(x) x + lambda * f(x);
    [sol1, ni1] = newton(f, fd, x0);
    [sol2, ni2] = succesive_aprox(g, x0);
    fprintf('\nSolutia %d:\n', i);
    disp('---NEWTON---');
    fprintf('x = %.6f, y = %.6f, z = %.6f\n', sol1(1), sol1(2), sol1(3));
    fprintf('Numar iteratii: %d\n', ni1);
    disp('---METODA APROXIMATIILOR SUCCESIVE---');
    fprintf('x = %.6f, y = %.6f, z = %.6f\n', sol2(1), sol2(2), sol2(3));
    fprintf('Numar iteratii: %d\n', ni2);
end

