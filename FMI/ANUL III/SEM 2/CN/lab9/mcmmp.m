function P = mcmmp(x_vals, y_vals, n, x)
  % Calculam matricea Vandermonde
  A = zeros(length(x_vals), n + 1);
  for i = 0:n
    A(:, i + 1) = x_vals.^i;
  end

  % Calculam coeficientii folosind metoda celor mai mici patrate
  coeffs = (A' * A) \ (A' * y_vals(:));

  % Calculam valoarea aproximata a polinomului in punctul x
  P = sum(coeffs' .* (x .^ (0:n)));
end
