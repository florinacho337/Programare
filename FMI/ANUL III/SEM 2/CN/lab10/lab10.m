clear all; clc; close all;

%f_integrat = @(x) sin(x);
%a = 0;
%b = pi;
%valoare_exacta = 2;

% f_integrat = @(x) exp(x);
% a = 0;
% b = 1;
% valoare_exacta = exp(1) - exp(0);

% f_integrat = @(x) 1./(1+x.^2);
% a = 0;
% b = 1;
% valoare_exacta = atan(1) - atan(0); % pi/4

 f_integrat = @(x) sqrt(x);
 a = 0;
 b = 4;
 valoare_exacta = (2/3)*4^(3/2); % 16/3

fprintf('Functie: %s\n', func2str(f_integrat));
fprintf('Interval: [%.2f, %.2f]\n', a, b);
fprintf('Valoare exacta: %f\n\n', valoare_exacta);

% --- Parametri pentru metoda adaptiva ---
toleranta = 1e-6;
m_val = 4; % Constanta m din pseudocod.


fprintf('Parametri adaptivi:\n');
fprintf('Toleranta (tol): %e\n', toleranta);
fprintf('Constanta m (m_val): %d\n\n', m_val);

% --- Testare cu Metoda Trapezului Adaptiva ---
disp('--- Trapez Adaptiv ---');
I_trap_adapt = adaptquad(f_integrat, a, b, @trapez_repetat, toleranta, m_val);
fprintf('Rezultat: %f\n', I_trap_adapt);
fprintf('Eroare absoluta: %e\n', abs(I_trap_adapt - valoare_exacta));

% --- Testare cu Metoda Simpson Adaptiva ---
disp('--- Simpson Adaptiv ---');
% Pentru Simpson, m_val trebuie sa fie par.
m_val_simpson = m_val;
if mod(m_val_simpson, 2) ~= 0
    warning('m_val (%d) este impar. Pentru Simpson se va folosi m_val+1 (%d).', m_val, m_val+1);
    m_val_simpson = m_val_simpson + 1; % Ajustare pentru a fi par
end
I_simp_adapt = adaptquad(f_integrat, a, b, @simpson_repetat, toleranta, m_val_simpson);
fprintf('Rezultat: %f\n', I_simp_adapt);
fprintf('Eroare absoluta: %e\n', abs(I_simp_adapt - valoare_exacta));

% --- Testare cu Metoda Dreptunghiului (Mijloc) Adaptiva ---
disp('--- Dreptunghi (Mijloc) Adaptiv ---');
I_drep_adapt = adaptquad(f_integrat, a, b, @dreptunghi_repetat, toleranta, m_val);
fprintf('Rezultat: %f\n', I_drep_adapt);
fprintf('Eroare absoluta: %e\n', abs(I_drep_adapt - valoare_exacta));

% --- Testare cu Metoda Romberg ---
disp('--- Romberg ---');
max_iter_romberg = 15;
fprintf('Parametri specifici Romberg:\n');
fprintf('Toleranta (tol): %e (aceeasi ca mai sus)\n', toleranta);
fprintf('Max iteratii: %d\n', max_iter_romberg);
[I_romberg, nfev_romberg] = romberg(f_integrat, a, b, toleranta, max_iter_romberg);
fprintf('Rezultat: %f\n', I_romberg);
fprintf('Numar evaluari functie (nfev): %d\n', nfev_romberg);
fprintf('Eroare absoluta: %e\n', abs(I_romberg - valoare_exacta));

disp('--- Octave quad() ---');
I_builtin = quad(f_integrat, a, b, toleranta);
fprintf('Rezultat: %f\n', I_builtin);
fprintf('Eroare absoluta: %e\n', abs(I_builtin - valoare_exacta));

