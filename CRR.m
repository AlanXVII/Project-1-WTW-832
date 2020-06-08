function opt_price = CRR(Put_Call, n, S_0, X, rfr, vol, t) 
    deltaT = t/n; 
    u = exp(vol*sqrt(deltaT));
    d = 1./u;
    R = exp(rfr*deltaT);
    p = (R-d)/(u-d);
    q = 1-p;     
    
    % simulating the underlying price paths
    S = zeros(n+1,n+1);
    S(1,1) = S_0;
    for i = 2:n+1
        S(i,1) = S(i-1,1)*u;
        for j=2:i+1
            S(i,j) = S(i-1,j-1)*d;
        end
    end
    
    % option value at final node   
    V = zeros(n+1,n+1); % V[i,j] is the option value at node (i,j)
    for j = 1:n+1
        if Put_Call=="C"
            V(n+1,j) = max(0, S(n+1,j)-X);
        elseif Put_Call=="P"
            V(n+1,j) = max(0, X-S(n+1,j));
        end
    end    
            
    for i = n:-1:1
        for j = i:-1:1
            V(i,j) = max(0, 1/R*(p*V(i+1,j)+q*V(i+1,j+1)));
        end
    end
    
    opt_price = V(1,1);
        
    return 