function c = CubicSplineNatural(x, f)

    der = [0, 0];

    n=length(x);
    if any(diff(x)<0), [x,ind]=sort(x); else ind=1:n; end
    y=f(ind); x=x(:); y=y(:);
    
    dx=diff(x);
    ddiv=diff(y)./dx;
    ds=dx(1:end-1);
    dd=dx(2:end);
    dp_middle=2*(ds+dd);
    md_middle=3*(dd.*ddiv(1:end-1)+ds.*ddiv(2:end));
    
    dp1_bc=2; % Coefficient of m_0 in the first equation
    dpn_bc=2; % Coefficient of m_n in the last equation
    vd1_bc=1; % Coefficient of m_1 in the first equation
    vdn_bc=1; % Coefficient of m_{n-1} in the last equation
    md1_bc=3*ddiv(1)-0.5*dx(1)*der(1);
    mdn_bc=3*ddiv(end)+0.5*dx(end)*der(2);
    
    dp_assembled=[dp1_bc; dp_middle; dpn_bc];
    dp1_diag_assembled=[0; vd1_bc; dd];
    dm1_diag_assembled=[ds; vdn_bc; 0];
    md_rhs=[md1_bc; md_middle; mdn_bc];
    
    A=spdiags([dm1_diag_assembled,dp_assembled,dp1_diag_assembled],-1:1,n,n);
    m=A\md_rhs;
    
    c(:,4)=y(1:end-1);
    c(:,3)=m(1:end-1);
    c(:,1)=(m(2:end)+m(1:end-1)-2*ddiv)./(dx.^2);
    c(:,2)=(ddiv-m(1:end-1))./dx-dx.*c(:,1);
end