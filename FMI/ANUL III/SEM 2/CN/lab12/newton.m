function [z,ni] = newton(f,fd,x0,ea,er,nmax)

  if nargin < 6, nmax=50; end
  if nargin < 5, er=0; end
  if nargin < 4, ea=1e-3; end
  xp=x0(:);   %x precedent
  for k=1:nmax
      xc=xp-fd(xp)\f(xp); % x curent
      if norm(xc-xp,inf)<ea+er*norm(xc,inf)
          z=xc;
          ni=k;
          return
      end
      xp=xc;
  end
  error('S-a depasit numarul maxim de iteratii');

