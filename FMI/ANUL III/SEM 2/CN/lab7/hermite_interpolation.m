function P = hermite_interpolation(x_vals, y_vals, dy_vals, x)
  n = length(x_vals);
  Q = zeros(2 * n, 2 * n);
  z = zeros(2 * n, 1);

  % Construirea vectorului z si matricei Q
  for i = 1:n
    z(2 * i - 1) = x_vals(i);
    z(2 * i) = x_vals(i);
    Q(2 * i - 1, 1) = y_vals(i);
    Q(2 * i, 1) = y_vals(i);
    Q(2 * i, 2) = dy_vals(i);

    if i > 1
      Q(2 * i - 1, 2) = (Q(2 * i - 1, 1) - Q(2 * i - 2, 1)) / (z(2 * i - 1) - z(2 * i - 2));
    end
  end

  % Completarea restului matricei Q
  for j = 3:(2 * n)
    for i = j:2 * n
      Q(i, j) = (Q(i, j - 1) - Q(i - 1, j - 1)) / (z(i) - z(i - j + 1));
    end
  end

  % Calculul polinomului de interpolare in punctul x
  P = Q(1, 1);
  product = 1;
  for i = 2:(2 * n)
    product = product * (x - z(i - 1));
    P = P + Q(i, i) * product;
  end
end
