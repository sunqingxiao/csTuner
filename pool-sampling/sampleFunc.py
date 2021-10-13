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


## calculate the correlation of two GPU metrics (Pearson)
def pair_metric_corr(metricVal1, metricVal2):
    pearCorr = np.corrcoef(metricVal1, metricVal2)
    return abs(pearCorr[0][1])


## sort pair metrics based on the Pearson results (ascending order)
def sort_pair_metric(para, numPara):
    numMetric = para.shape[1] - numPara
    numPair = int(numMetric*(numMetric-1)/2)
    metricVal = np.zeros((numMetric, para.shape[0]), dtype='float32')

    metricCorrIdx = np.zeros((numPair, 2), dtype='int32')
    metricCorrVal = np.zeros((numPair), dtype='float32')
    ascCorrIdx = np.zeros((numPair, 2), dtype='int32')
    ascCorrVal = np.zeros((numPair), dtype='float32')

    for i in range(0, numMetric):
        metricVal[i,:] = para[:,i+numPara]
    pairCount = 0
    for i in range(0, numMetric-1):
        for j in range(i+1, numMetric):
            metricCorrIdx[pairCount][0] = i
            metricCorrIdx[pairCount][1] = j
            metricCorrVal[pairCount] = pair_metric_corr(metricVal[i], metricVal[j])
            pairCount += 1

    ascIdx = np.argsort(metricCorrVal)
    ascCount = 0
    for i in ascIdx:
        ascCorrIdx[ascCount] = metricCorrIdx[i]
        ascCorrVal[ascCount] = metricCorrVal[i]
        ascCount += 1

    return ascCorrIdx, ascCorrVal


## group the metrics based on the ascending order
def group_metric(para, numPara, numGroup):
    ascCorrIdx, ascCorrVal = sort_pair_metric(para, numPara)
    numPair = ascCorrIdx.shape[0]
    ascDeque = collections.deque()
    for i in range(0, numPair):
        ascDeque.append(i)
    
    # creat groups according to the number of groups (pop)
    metricGroup = []
    groupCount = 0
    for i in range(0, numPair):
        tmpIdx = ascDeque.pop()
        metric1, metric2 = ascCorrIdx[tmpIdx][0], ascCorrIdx[tmpIdx][1]
        firstIn, secondIn = -1, -1
        for j in range(0, len(metricGroup)):
            if metric1 in metricGroup[j]:
                firstIn = j
                break
        for j in range(0, len(metricGroup)):
            if metric2 in metricGroup[j]:
                secondIn = j
                break

        # all of the metrics in the existing groups
        if firstIn != -1 and secondIn != -1:
            continue
        # none of the metrics in the existing groups
        elif firstIn == -1 and secondIn == -1:
            if groupCount < numGroup: # add a new group
                metricGroup.append([])
                metricGroup[groupCount].append(metric1)
                metricGroup[groupCount].append(metric2)
                groupCount += 1
            else:
                continue
        # one of the metrics in the existing groups
        else:
            if firstIn == -1:
                metricGroup[secondIn].append(metric1)
            else:
                metricGroup[firstIn].append(metric2)

    return metricGroup


## write the para/metric to the txt format input of extra-p
def write_extrap(para, numPara, metricId, fileName):
    metricIdx = numPara + metricId
    extrapFile = open(fileName, 'w')
    for i in range(0, numPara):
        extrapFile.write('PARAMETER {}\n'.format(chr(97+i)))
    extrapFile.write('\nPOINTS')
    for i in range(0, para.shape[0]):
        extrapFile.write(' ( ')
        for j in range(0, numPara):
            extrapFile.write('{} '.format(para[i][j]))
        extrapFile.write(')')
    extrapFile.write('\n\nREGION reg\nMETRIC metric\n\n')
    for i in range(0, para.shape[0]):
        extrapFile.write('DATA {}\n'.format(para[i][metricIdx]))
    extrapFile.close()


## write the PMNF regression function to the Python file
def write_pmnf(paraGroup, I, J, fileName):
    pmnfFile = open(fileName, 'w')
    pmnfFile.write('import numpy as np')
    
    # write regression functions for curve_fit and least_squares
    for funcId in range(0, 3):
        if funcId == 0: # curve_fit function
            pmnfFile.write('\n\ndef fn_cf(x');
            for i in range(0, len(paraGroup)):
                pmnfFile.write(' ,{}'.format(chr(97+i)))
            pmnfFile.write('):\n')
        elif funcId == 1: # least_squares function
            pmnfFile.write('\n\ndef fn_ls(c, x, y):\n')
        else:
            pmnfFile.write('\n\ndef fn_pred(c, x):\n')
        pmnfFile.write('    return ')
        for i in range(0, len(paraGroup)):
            if funcId == 0:
                pmnfFile.write('{} '.format(chr(97+i)))
            else:
                pmnfFile.write('c[{}] '.format(i))
            for j in range(0, len(paraGroup[i])):
                # judge the I value
                if I == 2:
                    pmnfFile.write('* (x[:,{}]**2)'.format(paraGroup[i][j]))
                elif I == 1:
                    pmnfFile.write('* x[:,{}]'.format(paraGroup[i][j]))
                else:
                    print('Nooooooooooooooooooooo exp!')
                # judge the J value
                if J == 1:
                    pmnfFile.write(' * np.log2(x[:,{}])'.format(paraGroup[i][j]))
                else:
                    print('Nooooooooooooooooooooo log!')
            if i < len(paraGroup) - 1:
                pmnfFile.write(' + ')
        if funcId == 1:
            pmnfFile.write(' - y')
    pmnfFile.close()


## output all PMNF Python files
def output_pmnf(paraGroup, outFolder):
    for I in range(0, 3):
        for J in range(0, 2):
            if I == 0 and J == 0:
                continue
            else:
                outFile = '{}/PMNF_{}_{}.py'.format(outFolder, I, J)
                write_pmnf(paraGroup, I, J, outFile)
