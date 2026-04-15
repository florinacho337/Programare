function I = adaptquad(f_handle, a, b, met_handle, tol, m_const, varargin)

  MAX_RECURSION_DEPTH = 50;
  MIN_INTERVAL_WIDTH = 100*eps(max(abs(a),abs(b)));

  current_depth = 0;
  if ~isempty(varargin)
      current_depth = varargin{1};
  end

  if current_depth > MAX_RECURSION_DEPTH
      warning('adaptquad:MaxDepth', ...
              'Adancimea maxima de recursie atinsa pentru intervalul [%f, %f]. Se returneaza estimarea curenta.', a, b);
      % Returneaza estimarea mai precisa din cele doua
      I = feval(met_handle, f_handle, a, b, 2 * m_const);
      return;
  end

  % Daca intervalul este foarte mic, nu mai subdiviza
  if (b - a) < MIN_INTERVAL_WIDTH
      I = feval(met_handle, f_handle, a, b, 2 * m_const); % Foloseste estimarea mai buna
      return;
  end


  % Estimare 1 cu m_const subintervale
  integral_estim1 = feval(met_handle, f_handle, a, b, m_const);

  % Estimare 2 cu 2*m_const subintervale (mai precisa)
  integral_estim2 = feval(met_handle, f_handle, a, b, 2 * m_const);

  if abs(integral_estim1 - integral_estim2) < tol
      % Daca diferenta este suficient de mica, acceptam estimarea mai precisa
      I = integral_estim2;
  else
      % Altfel, impartim intervalul in doua si aplicam recursiv
      c = (a + b) / 2;

      % Verifica daca subdiviziunea mai are sens (c sa nu fie egal cu a sau b din cauza erorilor de rotunjire)
      if c <= a || c >= b
           warning('adaptquad:SubdivisionStuck', ...
              'Subdiviziunea nu mai progreseaza pe intervalul [%f, %f]. Se returneaza estimarea curenta.', a, b);
          I = integral_estim2; % Returneaza estimarea mai buna
          return;
      end

      I_stanga = adaptquad(f_handle, a, c, met_handle, tol, m_const, current_depth + 1);
      I_dreapta = adaptquad(f_handle, c, b, met_handle, tol, m_const, current_depth + 1);
      I = I_stanga + I_dreapta;
  end

end
