import numpy as np

def fn_cf(x ,a ,b ,c ,d ,e):
    return a * x[:,3] * np.log2(x[:,3])* x[:,7] * np.log2(x[:,7])* x[:,4] * np.log2(x[:,4]) + b * x[:,0] * np.log2(x[:,0])* x[:,2] * np.log2(x[:,2]) + c * x[:,1] * np.log2(x[:,1]) + d * x[:,5] * np.log2(x[:,5])* x[:,8] * np.log2(x[:,8])* x[:,9] * np.log2(x[:,9])* x[:,10] * np.log2(x[:,10]) + e * x[:,6] * np.log2(x[:,6])

def fn_ls(c, x, y):
    return c[0] * x[:,3] * np.log2(x[:,3])* x[:,7] * np.log2(x[:,7])* x[:,4] * np.log2(x[:,4]) + c[1] * x[:,0] * np.log2(x[:,0])* x[:,2] * np.log2(x[:,2]) + c[2] * x[:,1] * np.log2(x[:,1]) + c[3] * x[:,5] * np.log2(x[:,5])* x[:,8] * np.log2(x[:,8])* x[:,9] * np.log2(x[:,9])* x[:,10] * np.log2(x[:,10]) + c[4] * x[:,6] * np.log2(x[:,6]) - y

def fn_pred(c, x):
    return c[0] * x[:,3] * np.log2(x[:,3])* x[:,7] * np.log2(x[:,7])* x[:,4] * np.log2(x[:,4]) + c[1] * x[:,0] * np.log2(x[:,0])* x[:,2] * np.log2(x[:,2]) + c[2] * x[:,1] * np.log2(x[:,1]) + c[3] * x[:,5] * np.log2(x[:,5])* x[:,8] * np.log2(x[:,8])* x[:,9] * np.log2(x[:,9])* x[:,10] * np.log2(x[:,10]) + c[4] * x[:,6] * np.log2(x[:,6])