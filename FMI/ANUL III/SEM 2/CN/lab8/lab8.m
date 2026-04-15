clear all; close all; clc;

f = @(x) x.^2.*sin(2*pi*x);
fd = @(x) 2*x.*sin(2*pi*x) + 2*x.^2*pi.*cos(2*pi*x);
fdd = @(x) 2*sin(2*pi*x) - 4*x.^2*pi^2.*sin(2*pi*x) + 8*x*pi.*cos(2*pi*x);

t=linspace(-1,1,200);
m_nodes=10; % Renamed from m to avoid conflict with m solution vector
k=1:m_nodes;
x_nodes=sort(cos((2*k-1)*pi/(2*m_nodes))); % Renamed x to x_nodes
y_nodes=f(x_nodes); % Renamed y to y_nodes

fd1_vals=fd([-1,1]); % Renamed fd1
fd2_vals=fdd([-1,1]); % Renamed fd2

disp('Calculating Complete Spline...');
cc1=CubicSplineComplete(x_nodes,y_nodes,fd1_vals);
disp('Calculating Second Derivative Spline...');
cc2=CubicSplineSecondDerivatives(x_nodes,y_nodes,fd2_vals);
disp('Calculating Natural Spline...');
cc3=CubicSplineNatural(x_nodes,y_nodes);
disp('Calculating DeBoor Spline...');
cc4=CubicSplineDeBoor(x_nodes,y_nodes);

disp('Evaluating splines...');
z1=evalsplinec(x_nodes,cc1,t);
z2=evalsplinec(x_nodes,cc2,t);
z3=evalsplinec(x_nodes,cc3,t);
z4=evalsplinec(x_nodes,cc4,t);

ft_exact=f(t'); % Renamed ft

figure(1)
subplot(2,1,1)
plot(x_nodes,y_nodes,'o',t,f(t),t,[z1,z2,z3,z4])
legend('noduri','f','complete','D2','natural','deBoor','Location','bestoutside');
title('spline')
subplot(2,1,2)
plot(t',abs(repmat(ft_exact,1,4)-[z1,z2,z3,z4]))
legend('complet','D2','natural','deBoor','Location','bestoutside');
title('error')

figure(2)
subplot(2,1,1)
plot(x_nodes,y_nodes,'o',t,f(t),t,[z1,z2,z3,z4])
legend('noduri','f','complete','D2','natural','deBoor','Location','bestoutside');
xlim([-1,-0.95])
title('Zoom stânga')
subplot(2,1,2)
plot(x_nodes,y_nodes,'o',t,f(t),t,[z1,z2,z3,z4])
legend('noduri','f','complet','D2','natural','deBoor','Location','bestoutside');
xlim([0.95,1])
title('Zoom dreapta')

disp('Test script finished.');