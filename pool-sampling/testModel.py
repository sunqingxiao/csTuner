import numpy as np
import math
from scipy.optimize import curve_fit, least_squares
from sklearn.metrics import mean_squared_error
from sampleFunc import *
from data.PMNF_N_N import *


def main():
    paraData = read_csv('data.csv')
    numPara = 11
    numGroup = 5
    metricId = 0
    train_x = paraData[:,:numPara]
    train_y = paraData[:,numPara+metricId]
    
    print('train_x shape: {}'.format(train_x.shape))
    print('train_y.shape: {}'.format(train_y.shape))

    # nonlinear regression using curve_fit
    popt, pcov = curve_fit(fn_cf, train_x, train_y)
    print('curve_fit coefficient: {}'.format(popt))
    pred_y = fn_pred(popt, train_x)
    mse = mean_squared_error(train_y, pred_y)
    rse = math.sqrt(mse/(train_y.shape[0]-2))
    print('curve_fit rse: {}'.format(rse))

    # nolinear regression using least_squares
    c0 = np.ones(numGroup)
    res_lsq = least_squares(fn_ls, c0, loss='soft_l1', f_scale=0.1, args=(train_x, train_y))
    print('least_squares coefficient: {}'.format(res_lsq.x))
    pred_y = fn_pred(res_lsq.x, train_x)
    mse = mean_squared_error(train_y, pred_y)
    rse = math.sqrt(mse/(train_y.shape[0]-2))
    print('least_squares rse: {}'.format(rse))

if __name__=='__main__':
    main()
