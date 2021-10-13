import os
import sys
import numpy as np
import time
from sampleFunc import *

def main():
    # test metric grouping
    paraData = read_csv('data.csv')
    numPara = 11
    numGroup = 2
    metricGroup = group_metric(paraData, numPara, numGroup)
    print(metricGroup)
    
    # test PMNF function outputs
    metricId = 0
    outFolder = 'data'
    paraGroup = [[3, 7, 4], [0, 2], [1], [5, 8, 9, 10], [6]]
    output_pmnf(paraGroup, outFolder)


if __name__=='__main__':
    main()
