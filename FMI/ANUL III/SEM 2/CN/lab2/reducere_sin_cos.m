function [s, c] = reducere_sin_cos(x)
  k = floor(x/2/pi);
  r = x - 2 * pi * k;
  
  syms x;
  f_sin = sin(x);
  f_cos = cos(x);
  
  maclaurin_sin = maclaurin_polynomial(f_sin, 15);
  maclaurin_cos = maclaurin_polynomial(f_cos, 15);
  
  s = double(subs(maclaurin_sin, x, r));
  c = double(subs(maclaurin_cos, x, r));
  