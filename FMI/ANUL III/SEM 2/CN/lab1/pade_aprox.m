function P = pade_aprox(f, m, n)
  syms x;
  c = sym(zeros(m+n+1, 1));
  if m>n
    q = sym(zeros(m+1, 1));
  else
    q = sym(zeros(n+1, 1));
  endif
  p = sym(zeros(1, m+1));
  
  for k=0:m+n
    c(k+1)=subs(diff(f, k), 0)/factorial(k);
  endfor
  
  j=0:n-1;
  C = toeplitz(c(m+j+1), c(m-j+1));
  qv = -c(m+(1:n)+1);
  q(2:n+1)=C\qv;
  q(1)=1;
  
  syms j
  for j=0:m
    p(j+1)=sym('0');
    for l=0:j
      p(j+1) = p(j+1) + c(j-l+1) * q(l+1);
    endfor
  endfor

  vp = sum(p.*x.^(0:m));
  vq = sum(q(1:n+1)'.*x.^(0:n));
  P = vp/vq;
end