function c = CubicSplineComplete(x, f, der)
    n=length(x);
    if any(diff(x)<0), [x,ind]=sort(x); else ind=1:n; end %order nodes if needed
    y=f(ind); x=x(:); y=y(:);
    
    %auxiliary unknowns - values of the spline derivative (actually M_i = s_i'')
    dx=diff(x);  %compute delta_x
    ddiv=diff(y)./dx; %divided differences
    
    ds=dx(1:end-1); % dx_i
    dd=dx(2:end);   % dx_{i+1}
    % Main diagonal for internal points i = 1, ..., n-2 (0-indexed for x, so x_1 to x_{n-1})
    % Corresponds to equations for m_1, ..., m_{n-2}
    dp_middle=2*(ds+dd);
    % Right-hand side for internal points
    md_middle=3*(dd.*ddiv(1:end-1)+ds.*ddiv(2:end));
    
    dp1_bc=1; % Coefficient of m_0 in the first equation (m_0 = der(1))
    dpn_bc=1; % Coefficient of m_n in the last equation (m_n = der(2))
    vd1_bc=0; % Coefficient of m_1 in the first equation
    vdn_bc=0; % Coefficient of m_{n-1} in the last equation
    md1_bc=der(1); % RHS for first equation
    mdn_bc=der(2); % RHS for last equation
    
    dp_assembled=[dp1_bc; dp_middle; dpn_bc];
    dp1_diag_assembled=[0; vd1_bc; dd]; 
    dm1_diag_assembled=[ds; vdn_bc; 0]; 
    
    A=spdiags([dm1_diag_assembled, dp_assembled, dp1_diag_assembled],-1:1,n,n);
    md_rhs=[md1_bc; md_middle; mdn_bc];
    
    m=A\md_rhs;
    
    c(:,4)=y(1:end-1); % d_j = y_j
    c(:,3)=m(1:end-1); % c_j = m_j
    c(:,1)=(m(2:end)+m(1:end-1)-2*ddiv)./(dx.^2); % a_j
    c(:,2)=(ddiv-m(1:end-1))./dx-dx.*c(:,1);     % b_j
end