import getopt
import sys
from Apriori import apriori
from AprioriHash import aprioriHash
from AprioriReduce import aprioriReduce
from AprioriReduce2 import aprioriReduce2
from FP_growth import fpTree
from DataLoader import *
from ResultOutput import *

if __name__ == '__main__':
    # 默认数据集编号
    dataSetNum = 2

    # 默认算法
    alogrithm = "fpTree"

    # 默认最小支持度和最小置信度
    minSupport = 0.06
    minConfidence = 0.3

    arg = [dataSetNum, alogrithm, minSupport, minConfidence]
    if len(sys.argv) != 1:
        for i in range(len(sys.argv)):
            if i < 4:
                arg[i] = sys.argv[i + 1]
        dataSetNum = int(arg[0])
        alogrithm = arg[1]
        minSupport = float(arg[2])
        minConfidence = float(arg[3])

    # 数据读取及清洗
    if dataSetNum == 1:
        dataSet = loadDataSet1()
    else:
        dataSet = loadDataSet2()

    # 调用算法
    if alogrithm == "apriori":
        frequentList, supportDictionary = apriori(dataSet, minSupport)
    elif alogrithm == "aprioriHash":
        frequentList, supportDictionary = aprioriHash(dataSet, minSupport)
    elif alogrithm == "aprioriReduce":
        frequentList, supportDictionary = aprioriReduce(dataSet, minSupport)
    elif alogrithm == "aprioriReduce2":
        frequentList, supportDictionary = aprioriReduce2(dataSet, minSupport)
    else:
        frequentList, supportDictionary = fpTree(dataSet, minSupport)

    # 数据输出
    out_file_name = 'result.txt'
    outputResult(out_file_name, supportDictionary, minConfidence)
