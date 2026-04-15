function [g_nodes,g_coeff]=gaussCheb2(n)
  beta=[pi/2,1/4*ones(1,n-1)];
  alpha=zeros(n,1);
  [g_nodes,g_coeff]=Gaussquad(alpha,beta);

