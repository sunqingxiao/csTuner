import numpy as np
import collections


## read para csv file
def read_csv(filename):
    try:
        data = np.loadtxt(filename, delimiter=',')
    except:
        print('Can not find csv file')
    finally:
        return data


## obtain the optimal parameter setting
def opt_para_setting(para):
    numPara = para.shape[1] - 1
    optIdx = np.argmin(para[:,numPara])
    return para[optIdx]


## extract the pair parameters and the corresponding duration
def pair_para_dur(firstIdx, secondIdx, para, optPara):
    numPara = para.shape[1] - 1
    pairIdx = 0
    pairPara = []
    for i in range(0, para.shape[0]):
        otherOpt = True
        for j in range(0, numPara):
            if j != firstIdx and j != secondIdx:
                if optPara[j] != para[i][j]:
                    otherOpt = False
                    break
        if otherOpt:
            pairPara.append([])
            pairPara[pairIdx].append(para[i][firstIdx])
            pairPara[pairIdx].append(para[i][secondIdx])
            pairPara[pairIdx].append(para[i][numPara])
            pairIdx += 1
    return np.array(pairPara)


## obtain the optimal value of one parameter when another parameter fixed
def opt_pair_para(uniqIdx, pairPara):
    fixedPara = []
    for i in uniqIdx:
        fixedPara.append(pairPara[i])
    fixedPara = np.array(fixedPara)
    optIdx = np.argmin(fixedPara[:,2])
    return fixedPara[optIdx][0]


## calculate the correlation of two parameters (coefficient of variation)
def pair_para_corr(firstIdx, secondIdx, para):
    optPara = opt_para_setting(para)
    pairPara = pair_para_dur(firstIdx, secondIdx, para, optPara)

    optParaVal = []
    for i in np.unique(pairPara[:,1]):
        uniqueIdx = np.argwhere(pairPara[:,1] == i)
        uniqueIdx = np.squeeze(uniqueIdx, 1)
        optParaVal.append(opt_pair_para(uniqueIdx, pairPara))
    optParaVal = np.array(optParaVal)
    return np.std(optParaVal) / np.mean(optParaVal)


## sort pair parameters based on the correlation results (ascending order)
def sort_pair_para(para):
    numPara = para.shape[1] - 1
    paraCorrIdx = np.zeros((numPara*(numPara-1), 2), dtype='int32')
    paraCorrVal = np.zeros((numPara*(numPara-1)), dtype='float32')
    ascCorrIdx = np.zeros((numPara*(numPara-1), 2), dtype='int32')
    ascCorrVal = np.zeros((numPara*(numPara-1)), dtype='float32')
    
    pairCount = 0
    for i in range(0, numPara):
        for j in range(0, numPara):
            if i != j:
                paraCorrIdx[pairCount][0] = i
                paraCorrIdx[pairCount][1] = j
                paraCorrVal[pairCount] = pair_para_corr(i, j, para)
                pairCount += 1
    ascIdx = np.argsort(paraCorrVal)
    ascCount = 0
    for i in ascIdx:
        ascCorrIdx[ascCount] = paraCorrIdx[i]
        ascCorrVal[ascCount] = paraCorrVal[i]
        ascCount += 1

    return ascCorrIdx, ascCorrVal


## group the parameters based on the ascending order
def group_para(para):
    ascCorrIdx, ascCorrVal = sort_pair_para(para)
    numPair = ascCorrIdx.shape[0]
    ascDeque = collections.deque()
    for i in range(0, numPair):
        ascDeque.append(i)
    
    numGroup = 0
    paraGroup = []
    for i in range(0, numPair):
        # pop the top/bottom pair parameters in the queue
        tmpIdx = ascDeque.pop() if i % 2 == 1 else ascDeque.popleft() 
        firstPara, secondPara = ascCorrIdx[tmpIdx][0], ascCorrIdx[tmpIdx][1]
        firstIn, secondIn = -1, -1
        for j in range(0, len(paraGroup)):
            if firstPara in paraGroup[j]:
                firstIn = j
                break
        for j in range(0, len(paraGroup)):
            if secondPara in paraGroup[j]:
                secondIn = j
                break           

        # group the parameters with low variation
        if i % 2 == 0:
            # none of the paras in the existing groups
            if firstIn == -1 and secondIn == -1:
                paraGroup.append([])
                paraGroup[numGroup].append(firstPara)
                paraGroup[numGroup].append(secondPara)
                numGroup += 1
            # all the paras in the existing groups
            elif firstIn != -1 and secondIn != -1:
                continue
            # one of the paras in the existing groups
            else:
                if firstIn == -1:
                    paraGroup[secondIn].append(firstPara)
                else:
                    paraGroup[firstIn].append(secondPara)
        # split the parameters with high variation
        else:
            # none of the paras in the existing groups
            if firstIn == -1 and secondIn == -1:
                paraGroup.append([])
                paraGroup[numGroup].append(firstPara)
                numGroup += 1
                paraGroup.append([])
                paraGroup[numGroup].append(secondPara)
                numGroup += 1
            # all the paras in the existing groups
            elif firstIn != -1 and secondIn != -1:
                continue
            # one of the paras in the existing groups
            else:
                paraGroup.append([])
                if firstIn == -1:
                    paraGroup[numGroup].append(firstPara)
                else:
                    paraGroup[numGroup].append(secondPara)
                numGroup += 1

    return paraGroup
