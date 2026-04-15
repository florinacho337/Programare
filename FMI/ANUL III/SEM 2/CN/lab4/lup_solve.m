function x = lup_solve(L, U, b, P)
  n = length(b);
  y = zeros(n, 1);
  x = zeros(n, 1);
  
  for i = 1:n
    y(i) = b(P(i)) - sum(L(i, 1:i-1) .* y(1:i-1)');
  endfor
  
  for i = n:-1:1
    x(i) = (y(i) - sum(U(i, i+1:n) .* x(i+1:n)')) / U(i, i);
  end
end