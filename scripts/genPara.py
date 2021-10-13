import os
import sys
import random
import math
import numpy as np

def list2txt(fileName="", myfile=[]):
    fileout = open(fileName, 'w')
    for i in range(len(myfile)):
        for j in range(len(myfile[i])):
            if j == len(myfile[i]) - 1:
                fileout.write(str(myfile[i][j]))
            else:
                fileout.write(str(myfile[i][j]) + ' , ')
        fileout.write('\r\n')
    fileout.close()

def main():
    ## blockdim(x, y)
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
    logValue = 2
    N = 512 # stencil input dimension
    logN = 2
    #logN = int(math.log(N, logValue))
    maxBlockSize = 512
    logBlockSize = int(math.log(maxBlockSize, logValue))
   
    paraSettings = []
    numSettings = 0

    ## generate all settings 
    for bxRange in range(3, logBlockSize+1):
        blockDim[0] = pow(logValue, bxRange)
        for byRange in range(3, logBlockSize+1):
            blockDim[1] = pow(logValue, byRange)
            if blockDim[0] * blockDim[1] > maxBlockSize:
                continue
            else:
                for optMergeRange in range(0, 2):
                    optMerge = optMergeRange
                    for mergeXRange in range(0, logN+1):
                        mergeFactor[0] = pow(logValue, mergeXRange)
                        for mergeYRange in range(0, logN+1):
                            mergeFactor[1] = pow(logValue, mergeYRange)
                            for lenStreamRange in range(3, 6):
                                lenStreamBlock = pow(logValue, lenStreamRange)
                                for unrollStreamRange in range(2, lenStreamRange+1):
                                    unrollStreamDim = pow(2, unrollStreamRange)
                                    for readonlyRange in range(0, 2):
                                        readonlyMemory = readonlyRange
                                        for useSharedRange in range(0, 2):
                                            useSharedMemory = useSharedRange
                                            for retimingRange in range(0, 2):
                                                useRetiming = retimingRange
                                                for prefetchingRange in range(0, 2):
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
   
    ## randomly generate the execution time
    exeTime = []
    for i in range(0, numSettings):
        exeTime.append(random.random())

    ## write to csv file
    myfile = []
    for i in range(0, numSettings):
        myfile.append([])
        for j in range(0, len(paraSettings[0])):
            myfile[i].append(paraSettings[i][j]+1)
        myfile[i].append(exeTime[i])
    list2txt('parasettings.csv', myfile)


if __name__=='__main__':
    main()
