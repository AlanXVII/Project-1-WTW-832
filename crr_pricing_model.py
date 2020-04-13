# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import math as mat
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def CRR(call_put, n, S, K, r, vol,  t):
    delT = t / n
    R = mat.exp(r*delT)
    u = mat.exp(vol*delT)
    d = 1/u
    p = (R-d)/(u-d) 
    q = 1-p  
        
    if R > u or R < d:
        print("Error: Risk-free-rate and associated u&d values do not satisfy the following: d<r<u")
        return  
    
    C = 0      
        
    for j in range(0, n):
        i = n-j
        fact_term = mat.factorial(n)/(mat.factorial(j)*mat.factorial(i))
        x = fact_term*(p**j)*(q**i)*max(0,(u**j)*(d**i)*S-K)
        C += x
        
    if call_put == "call":
        opt_price = C/R**n
    elif call_put == "put":
        opt_price = C/R**n - S - K/R
        
    return opt_price

def BSM(call_put, S, K, rfr, vol, t):
    d_one = (mat.log(S/K)+(rfr+vol**2/2)*t)/(vol*mat.sqrt(t))
    d_two = d_one - vol*mat.sqrt(t)
    
    if call_put == "call":
        opt_price = S*norm.cdf(d_one) - K*mat.exp(-rfr*t)*norm.cdf(d_two)
    elif call_put == "put":
        opt_price = K*mat.exp(-rfr*t)*norm.cdf(-d_two) - S*norm.cdf(-d_one)
    
    return opt_price

def Price_Error(call_put, S, K, rfr, vol, t, n):
    
    error = BSM(call_put, S, K, rfr, vol, t)-CRR(call_put, int(n), S, K, rfr, vol,  t)
    
    return error

#Plotting BSM v CRR v Strike Prices
N = np.linspace(1,100,100)
error_otm = [Price_Error("call",100, 150, 0.1, 0.2, 10, n) for n in N]
error_itm = [Price_Error("call",100, 50, 0.1, 0.2, 10, n) for n in N]
error_atm = [Price_Error("call",100, 100, 0.1, 0.2, 10, n) for n in N]

plt.title("Pricing Error", fontsize=24) 
plt.xlabel("Number of Steps", fontsize=18) 
plt.ylabel("Error", fontsize=18)

plt.plot(N, error_atm, 'k-', error_itm, 'r-', error_itm, 'b-')

plt.show()

# plt.legend(["BSM", "CRR"])
# plt.show() 
# plt.savefig('bsm_vs_crr.png')



# plt.plot(strikes, bsm_prices, 'k-') 

# plt.title("Pricing Error vs Binomial Steps", fontsize=24) 
# plt.xlabel("Number of Steps", fontsize=18) 
# plt.ylabel("Pricing Error", fontsize=18)

# bsm_prices = [BSM("call",100,x,0.1,0.2,10) for x in strikes]
# crr_prices = [CRR("call",10,100,x,0.1,0.2,10) for x in strikes]


# plt.show() 