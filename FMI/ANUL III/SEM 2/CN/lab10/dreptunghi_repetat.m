function I = dreptunghi_repetat(f, a, b, n)
  h = (b - a) / n;
  suma = 0;
  for k = 1:n
    xk = a + (k - 0.5) * h; % punctul de mijloc
    suma = suma + f(xk);
  end
  I = h * suma;
end
