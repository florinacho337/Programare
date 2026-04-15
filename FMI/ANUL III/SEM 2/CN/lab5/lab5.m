n = 5;
A = hilb(n);
%A = [
%    10, -1,  2,  0,  0;
%    -1, 11, -1,  3,  0;
%     2, -1, 10, -1,  0;
%     0,  3, -1,  8, -2;
%     0,  0,  0, -2,  6
%];
b = ones(n, 1);

tol = 1e-3;
max_iter = 573;
omega = 0.1553;

disp("A:");
disp(A);

disp("b");
disp(b);

x = A \ b;
disp("Solutia A\\b:");
disp(x);

disp("Soluția aproximată cu Jacobi:");
[iter, x_sol] = jacobi(A, b, tol, max_iter)

disp("Soluția aproximată cu Succesive Overrelaxation:");
[iter, x_sol] = sor(A, b, omega, tol, max_iter)

disp("Concluzie: Jacobi nu converge, probabil pentru ca matricea Hilbert nu este diagonal dominanta.");
