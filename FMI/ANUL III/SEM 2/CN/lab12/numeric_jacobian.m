function J = numeric_jacobian(g, x0)
    n = length(x0);
    fx = g(x0);
    J = zeros(n, n);
    h = 1e-6;
    for i = 1:n
        xh = x0;
        xh(i) = xh(i) + h;
        J(:, i) = (g(xh) - fx) / h;
    end
end
