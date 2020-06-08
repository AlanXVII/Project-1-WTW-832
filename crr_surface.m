tenors = linspace(0.01,1,100);
strikes = linspace(51,150,100);
crr_vals = zeros(100,100);

for t = 1:100
    for x = 1:100
        crr_vals(x,t) = CRR("P", 10, 100, strikes(x), 0.05, 0.2, tenors(t));
    end
end

surf(tenors,strikes,crr_vals)