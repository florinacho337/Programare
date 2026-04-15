pkg load symbolic
syms t
format long

f = @(x) cos(x) ./ sqrt(1 - x.^2);
n = 10;
ve = int(cos(t) / sqrt(1 - t^2), t, -1, 1);

fprintf('Valoare exacta: %10.6f\n', double(ve));

% ---Gauss Legendre---
disp('Gauss Legendre');
[gn, gc] = gaussLegendre(n);
v = gc * f(gn);
fprintf('Valoare aproximata: %10.6f\n', v);
fprintf('Diferenta  dintre valoarea exacta si cea calculata: %10.6f\n', abs(double(ve) - v));

% ---Gauss Cebisev 1---
disp('Gauss Cebisev 1');
[gn, gc] = gaussCheb1(n);
v = gc * f(gn);
fprintf('Valoare aproximata: %10.6f\n', v);
fprintf('Diferenta  dintre valoarea exacta si cea calculata: %10.6f\n', abs(double(ve) - v));

% ---Gauss Cebisev 2---
disp('Gauss Cebisev 2');
[gn, gc] = gaussCheb2(n);
v = gc * f(gn);
fprintf('Valoare aproximata: %10.6f\n', v);
fprintf('Diferenta  dintre valoarea exacta si cea calculata: %10.6f\n', abs(double(ve) - v));

% ---Gauss Laguerre---
disp('Gauss Laguerre');
[gn, gc] = gaussLaguerre(n);
v = gc * f(gn);
fprintf('Valoare aproximata: %10.6f\n', v);
fprintf('Diferenta  dintre valoarea exacta si cea calculata: %10.6f\n', abs(double(ve) - v));

% ---Gauss Hermite---
disp('Gauss Hermite');
[gn, gc] = gaussHermite(n);
v = gc * f(gn);
fprintf('Valoare aproximata: %10.6f\n', v);
fprintf('Diferenta  dintre valoarea exacta si cea calculata: %10.6f\n', abs(double(ve) - v));

% ---Gauss Jacobi---
disp('Gauss Jacobi');
[gn, gc] = gaussJacobi(n, 0, 0);
v = gc * f(gn);
fprintf('Valoare aproximata: %10.6f\n', v);
fprintf('Diferenta  dintre valoarea exacta si cea calculata: %10.6f\n', abs(double(ve) - v));

