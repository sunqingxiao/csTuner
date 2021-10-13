import numpy as np

def fn_cf(x ,a ,b ,c ,d ,e):
    return a * (x[:,3]**2)* (x[:,7]**2)* (x[:,4]**2) + b * (x[:,0]**2)* (x[:,2]**2) + c * (x[:,1]**2) + d * (x[:,5]**2)* (x[:,8]**2)* (x[:,9]**2)* (x[:,10]**2) + e * (x[:,6]**2)

def fn_ls(c, x, y):
    return c[0] * (x[:,3]**2)* (x[:,7]**2)* (x[:,4]**2) + c[1] * (x[:,0]**2)* (x[:,2]**2) + c[2] * (x[:,1]**2) + c[3] * (x[:,5]**2)* (x[:,8]**2)* (x[:,9]**2)* (x[:,10]**2) + c[4] * (x[:,6]**2) - y

def fn_pred(c, x):
    return c[0] * (x[:,3]**2)* (x[:,7]**2)* (x[:,4]**2) + c[1] * (x[:,0]**2)* (x[:,2]**2) + c[2] * (x[:,1]**2) + c[3] * (x[:,5]**2)* (x[:,8]**2)* (x[:,9]**2)* (x[:,10]**2) + c[4] * (x[:,6]**2)