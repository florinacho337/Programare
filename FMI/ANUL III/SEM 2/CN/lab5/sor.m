function [iter, x] = sor(A, b, omega, tol, max_iter)
    M = 1 / omega*diag(diag(A)) + tril(A, -1);
    N = M - A;

    x = zeros(size(b)); % Inițializare soluție cu zero
    for k = 1:max_iter
      x0 = x;
      x = M \ (N*x0 + b);
      if norm(x-x0, inf) < tol * norm(x, inf)
        iter = k;
        return
      endif
    endfor

    iter = max_iter;
    warning('iteration number exceeded');
endfunction
