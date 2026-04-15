function P = maclaurin_polynomial(f, n)
    syms x k; % Define k as a symbolic variable
    P = 0;
    for k = 0:n
      P = P + (subs(diff(f, k), 0) / factorial(k)) * x^k;
    endfor
end