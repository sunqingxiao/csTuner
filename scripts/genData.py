import numpy as np
import sys
import math
from scipy.optimize import curve_fit, least_squares
from sklearn.metrics import mean_squared_error
from sampleFunc import *
from data.PMNF_2_0 import *


def list2txt(fileName, para, duration):
    fileout = open(fileName, 'w')
    for i in range(len(para)):
        for j in range(len(para[i])):
            fileout.write(str(para[i][j])+',')
        fileout.write(str(duration[i]))
        fileout.write('\r\n')
    fileout.close()


def main():
    if len(sys.argv) != 2:
        exit(1)

    stencil = sys.argv[1]

    blockDim = np.zeros((2), dtype='int32') # bx * by <= 1024
    ## cyclic/block merge factor along x/y dimension
    mergeFactor = np.zeros((2), dtype='int32') # x <= N, y <= N 
    ## constant/global memory for read-only data
    readonlyMemory = -1 # {0, 1}
    ## shared memory for accelerating the computation
    useSharedMemory = -1 # {0, 1}
    ## len of the divided stream blocks
    lenStreamBlock = -1 # lenStreamBlock <= N
    ## unrolling factor over the streaming dimension
    unrollStreamDim = -1 # unrollStreamDim <= lenStreamBlock
    optMerge = -1 # cyclic merge or block merge {0, 1}
    useRetiming = -1 # {0, 1}
    usePrefetching = -1 # {0, 1}
    
    #############################
   
    paraSettings = []
    maxBlockSize = 512
    numSettings = 0
    logValue = 2

    ## generate all settings 
    for bxRange in range(0, 11):
        blockDim[0] = pow(logValue, bxRange)
        for byRange in range(0, 11):
            blockDim[1] = pow(logValue, byRange)
            if blockDim[0] * blockDim[1] > maxBlockSize:
                continue
            else:
                for optMergeRange in range(1, 3):
                    optMerge = optMergeRange
                    for mergeXRange in range(0, 9):
                        mergeFactor[0] = pow(logValue, mergeXRange)
                        for mergeYRange in range(0, 9):
                            mergeFactor[1] = pow(logValue, mergeYRange)
                            for lenStreamRange in range(0, 9):
                                lenStreamBlock = pow(logValue, lenStreamRange)
                                for unrollStreamRange in range(2, lenStreamRange+1):
                                    unrollStreamDim = pow(2, unrollStreamRange)
                                    for readonlyRange in range(1, 3):
                                        readonlyMemory = readonlyRange
                                        for useSharedRange in range(1, 3):
                                            useSharedMemory = useSharedRange
                                            for retimingRange in range(1, 3):
                                                useRetiming = retimingRange
                                                for prefetchingRange in range(1, 3):
                                                    usePrefetching = prefetchingRange
                                                    paraSettings.append([])
                                                    for i in range(0, 2):
                                                        paraSettings[numSettings].append(blockDim[i])
                                                    paraSettings[numSettings].append(optMerge)
                                                    for i in range(0, 2):
                                                        paraSettings[numSettings].append(mergeFactor[i])
                                                    paraSettings[numSettings].append(lenStreamBlock)
                                                    paraSettings[numSettings].append(unrollStreamDim)
                                                    paraSettings[numSettings].append(readonlyMemory)
                                                    paraSettings[numSettings].append(useSharedMemory)
                                                    paraSettings[numSettings].append(useRetiming)
                                                    paraSettings[numSettings].append(usePrefetching)
                                                    numSettings += 1
    print('numSettings = {}'.format(numSettings))

    coe = [0.85937149, -0.74446452, 0.49852789, 1.08190951, 0.56918949, -0.70082875]
    paraSettings = np.array(paraSettings)
    coe = np.array(coe)
    total_duration = fn_pred(coe, paraSettings)

    list2txt('data/{}.csv'.format(stencil), paraSettings, total_duration)

if __name__=='__main__':
    main()
