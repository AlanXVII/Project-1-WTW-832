# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 10:35:35 2020

@author: alanw
"""

import numpy as np
from scipy.stats import norm
############
# CRR Model
############

def CRR(Put_Call, n, S_0, X, rfr, vol, t, AMN_EUR):  
    deltaT = t/n 
    u = np.exp(vol*np.sqrt(deltaT))
    d = 1./u
    R = np.exp(rfr*deltaT)
    p = (R-d)/(u-d)
    q = 1-p     
    
    # simulating the underlying price paths
    S = np.zeros((n+1,n+1))
    S[0,0] = S_0
    for i in range(1,n+1):
        S[i,0] = S[i-1,0]*u
        for j in range(1,i+1):
            S[i,j] = S[i-1,j-1]*d
    
    # option value at final node   
    V = np.zeros((n+1,n+1)) # V[i,j] is the option value at node (i,j)
    for j in range(n+1):
        if Put_Call=="C":
            V[n,j] = max(0, S[n,j]-X)
        elif Put_Call=="P":
            V[n,j] = max(0, X-S[n,j])
            
    # European Otpion: backward induction to the option price V[0,0]        
    if AMN_EUR == "E":            
    
        for i in range(n-1,-1,-1):
            for j in range(i+1):
                    V[i,j] = max(0, 1/R*(p*V[i+1,j]+q*V[i+1,j+1]))
        opt_price = V[0,0]
    # American Otpion: backward induction to the option price V[0,0] 
    elif AMN_EUR == "A":
        for i in range(n-1,-1,-1):
            for j in range(i+1):
                    if Put_Call=="P":
                        V[i,j] = max(0, X-S[i,j], 
                                     1/R*(p*V[i+1,j]+q*V[i+1,j+1]))
                    elif Put_Call=="C":
                        V[i,j] = max(0, S[i,j]-X,
                                     1/R*(p*V[i+1,j]+q*V[i+1,j+1]))
        opt_price = V[0,0]
        
    return opt_price

#############
# BSM Model
#############
def BSM(Put_Call, S_0, X, rfr, vol, t):
    d_one = (np.log(S_0/X)+(rfr+vol**2/2)*t)/(vol*np.sqrt(t))
    d_two = d_one - vol*np.sqrt(t)
    
    if Put_Call == "C":
        opt_price = S_0*norm.cdf(d_one) - X*np.exp(-rfr*t)*norm.cdf(d_two)
    elif Put_Call == "P":
        opt_price = X*np.exp(-rfr*t)*norm.cdf(-d_two) - S_0*norm.cdf(-d_one)
    
    return opt_price
################
# Pricing Error
################
def Price_Error(Put_Call, n, S_0, X, rfr, vol, t):
    AMN_EUR = "E"    
    error = BSM(Put_Call, S_0, X, rfr, vol, t)-CRR(Put_Call, n, S_0, X, rfr,
                                                   vol, t, AMN_EUR)
    
    return error

################
#Avg Even/Odd
###############
def Avg_Even_Odd_Error(Put_Call, n, S_0, X, rfr, vol, t):
    AMN_EUR = "E"    
    error = BSM(Put_Call, S_0, X, rfr, vol, t)-
    ((CRR(Put_Call, n, S_0, X, rfr, vol, t, AMN_EUR)+
      CRR(Put_Call, n+1, S_0, X, rfr, vol, t, AMN_EUR))/2)
    
    return error
