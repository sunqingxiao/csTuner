import os
import sys
import time
import numpy as np
from paraFunc import read_csv, group_para


def main():
    paraData = read_csv('data.csv')
    start_time = time.time()
    paraGroup = group_para(paraData)
    end_time = time.time()
    print('total cost: {}'.format(end_time - start_time))
    print(paraGroup)


if __name__=='__main__':
    main()
