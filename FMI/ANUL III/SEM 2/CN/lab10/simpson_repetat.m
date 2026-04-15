function I = simpson_repetat(f, a, b, n)
  if mod(n, 2) ~= 0
    error('n trebuie sa fie par pentru formula lui Simpson.');
  end
  h = (b - a) / n;
  suma = f(a) + f(b);
  for k = 1:2:(n - 1)
    suma = suma + 4 * f(a + k * h);
  end
  for k = 2:2:(n - 2)
    suma = suma + 2 * f(a + k * h);
  end
  I = (h / 3) * suma;
end
