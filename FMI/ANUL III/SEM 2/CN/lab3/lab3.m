A = [10 7 8 7;
     7 5 6 5;
     8 6 10 9;
     7 5 9 10];

A_pert = [10 7 8.1 7.2;
          7.08 5.04 6 5;
          8 5.98 9.89 9;
          6.99 4.99 9 9.98]

b = [32; 23; 33; 31];

b_tilde = [32.1; 22.9; 33.1; 30.9];

x = A \ b;
x_tilde = A \ b_tilde;

% Calculul erorii relative la intrare
error_input = norm(b_tilde - b) / norm(b);

% Calculul erorii relative la ieșire
error_output = norm(x_tilde - x) / norm(x);

% Calculul raportului erorilor
error_ratio = error_output / error_input;

disp("Problema 1");
disp("a)");
disp("Soluția inițială x:");
disp(x);
disp("Soluția perturbată x_tilde:");
disp(x_tilde);
disp("Eroarea relativă la intrare:");
disp(error_input);
disp("Eroarea relativă la ieșire:");
disp(error_output);
disp("Raportul erorilor:");
disp(error_ratio);

x_tilde = A_pert \ b;

error_input = norm(A_pert - A) / norm(A)
error_output = norm(x_tilde - x) / norm(x);
error_ratio = error_output / error_input;

disp("");
disp("b)");
disp("Soluția inițială x:");
disp(x);
disp("Soluția perturbată x_tilde:");
disp(x_tilde);
disp("Eroarea relativă la intrare:");
disp(error_input);
disp("Eroarea relativă la ieșire:");
disp(error_output);
disp("Raportul erorilor:");
disp(error_ratio);

cond_A = norm(A) * norm(inv(A));
disp(["cond(A) = ", num2str(cond_A)]);

disp("");
disp("");
disp("Problema 2");

for i=10:15
  H = hilb(i);
  H_inv = invhilb(i);
  cond_H = norm(H) * norm(H_inv);
  disp(["cond(H", num2str(i), ") = ", num2str(cond_H)]);
endfor
