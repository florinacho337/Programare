function G = gauss_elimination(A)
  [n, m] = size(A);
  for i = 1:n-1
    [~, p] = max(abs(A(i:n, i)));
    p = p + i - 1;

    if A(p, i) == 0
      error('Sistemul nu are sol unica');
    endif

    if p ~= i
      A([i, p], :) = A([p, i], :);
    endif

    for j = i+1:n
      mji = A(j, i) / A(i, i);
      A(j, :) = A(j, :) - mji * A(i, :);
    endfor
  endfor

  if A(n, n) == 0
    error('Sistemul nu are sol unica');
  endif

  G = zeros(n, 1);
  G(n) = A(n, end) / A (n, n);
  for i = n-1:-1:1
    G(i) = (A(i, end) - sum(A(i, i+1:n) .* G(i+1:n)')) / A(i, i);
  endfor
end
