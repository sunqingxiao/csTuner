import numpy as np

def fn_cf(x ,a ,b ,c ,d ,e):
    return a  * np.log2(x[:,3]) * np.log2(x[:,7]) * np.log2(x[:,4]) + b  * np.log2(x[:,0]) * np.log2(x[:,2]) + c  * np.log2(x[:,1]) + d  * np.log2(x[:,5]) * np.log2(x[:,8]) * np.log2(x[:,9]) * np.log2(x[:,10]) + e  * np.log2(x[:,6])

def fn_ls(c, x, y):
    return c[0]  * np.log2(x[:,3]) * np.log2(x[:,7]) * np.log2(x[:,4]) + c[1]  * np.log2(x[:,0]) * np.log2(x[:,2]) + c[2]  * np.log2(x[:,1]) + c[3]  * np.log2(x[:,5]) * np.log2(x[:,8]) * np.log2(x[:,9]) * np.log2(x[:,10]) + c[4]  * np.log2(x[:,6]) - y

def fn_pred(c, x):
    return c[0]  * np.log2(x[:,3]) * np.log2(x[:,7]) * np.log2(x[:,4]) + c[1]  * np.log2(x[:,0]) * np.log2(x[:,2]) + c[2]  * np.log2(x[:,1]) + c[3]  * np.log2(x[:,5]) * np.log2(x[:,8]) * np.log2(x[:,9]) * np.log2(x[:,10]) + c[4]  * np.log2(x[:,6])