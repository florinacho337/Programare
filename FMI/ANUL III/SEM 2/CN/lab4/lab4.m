% matrice Hilbert 5x5 , b - vector de 1

n = 5;

H = hilb(n);

b = ones(n, 1);  % vector de 1

fprintf("Rezolvare cu eliminare Gaussiana:\n");
H_ext = [H, b]; % H extins
x_gauss = gauss_elimination(H_ext);
disp(x_gauss);

fprintf("Rezolvare cu descompunere LUP:\n");
[L, U, P] = LUP_decomposition(H);
[~, p_vec] = max(P, [], 2); % transformare P in vector cu indicii unde apare 1
x_lup = lup_solve(L, U, b, p_vec);
disp(x_lup);

fprintf("Rezolvare cu descompunere Cholesky:\n");
x_cholesky = cholesky_solve(H, b);
disp(x_cholesky);
