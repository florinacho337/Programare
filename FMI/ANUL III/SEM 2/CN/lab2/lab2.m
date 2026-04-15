x = 12532.14;
[s, c] = reducere_sin_cos(x);
disp(["sin(", num2str(x), ") = ", num2str(sin(x))]);
disp(["cos(", num2str(x), ") = ", num2str(cos(x))]);

disp("");
disp("Aproximari cu reducere de argument:");
disp(["sin(", num2str(x), ") = ", num2str(s)]);
disp(["cos(", num2str(x), ") = ", num2str(c)]);