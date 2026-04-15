function I = trapez_repetat(f, a, b, n)
  h = (b - a) / n;
  suma = (f(a) + f(b)) / 2;
  for k = 1:(n - 1)
    suma = suma + f(a + k * h);
  end
  I = h * suma;
end
