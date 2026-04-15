syms x;
f = exp(x);
n = 7;
maclaurin_poly = maclaurin_polynomial(f, n);

f = exp(x);
n = 1;
m = 1;
pade = pade_aprox(f, m, n);

disp('MacLaurin Polynomial of order 7 for sin:');
disp(maclaurin_poly);
disp('Pade aproximation of order (1,1) for exp(x)');
disp(pade)

f = log(1 + x);
disp('Pade aproximation of order (3,1) for ');
disp(f);
m = 3;
n = 1;
pade = pade_aprox(f, m, n);
disp(pade);
