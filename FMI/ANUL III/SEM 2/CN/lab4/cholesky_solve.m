function x = cholesky_solve(A, b)
    L = Cholesky_decomposition(A);

    y = forwardsubst(L', b);

    x = backsubst(L, y);
end
