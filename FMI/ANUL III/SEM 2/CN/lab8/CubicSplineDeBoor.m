function c = CubicSplineDeBoor(x, f)
    n=length(x);
    if any(diff(x)<0), [x,ind]=sort(x); else ind=1:n; end
    y=f(ind); x=x(:); y=y(:);
    
    dx=diff(x);
    ddiv=diff(y)./dx;
    
    ds=dx(1:end-1);
    dd=dx(2:end);   
    
    
    dp_middle=2*(ds+dd);
    md_middle=3*(dd.*ddiv(1:end-1)+ds.*ddiv(2:end));
    x31=x(3)-x(1); % h_0 + h_1
    xn_val=x(n)-x(n-2); % h_{n-2} + h_{n-1}
    
    dp1_bc=dx(2); % Coeff of m_0
    vd1_bc=x31;   % Coeff of m_1
    md1_bc=((dx(1)+2*x31)*dx(2)*ddiv(1)+dx(1)^2*ddiv(2))/x31;
    
    dpn_bc=dx(end-1);
    vdn_bc=xn_val;    % Coeff of m_{n-1}
    mdn_bc=(dx(end)^2*ddiv(end-1)+(2*xn_val+dx(end))*dx(end-1)*ddiv(end))/xn_val;
    
    
    dp_assembled=[dp1_bc; dp_middle; dpn_bc];
    dp1_diag_assembled=[0; vd1_bc; dd]; 
    dm1_diag_assembled=[ds; vdn_bc; 0]; 
    
    A=spdiags([dm1_diag_assembled, dp_assembled, dp1_diag_assembled],-1:1,n,n);
    md_rhs=[md1_bc; md_middle; mdn_bc];
    
    
    m=A\md_rhs;
    
    c(:,4)=y(1:end-1);
    c(:,3)=m(1:end-1);
    c(:,1)=(m(2:end)+m(1:end-1)-2*ddiv)./(dx.^2);
    c(:,2)=(ddiv-m(1:end-1))./dx-dx.*c(:,1);
end