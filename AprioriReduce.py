# AprioriHash算法实现
from numpy import *
from DataLoader import *
from ResultOutput import *


# 设计哈希函数
def hashFunc(x, y, order):
    return (131*(order[x]) + order[y]) % 77


# 获取候选1项集，dataSet为事务集
def findCandidate1(dataSet):
    candidate1 = []
    for line in dataSet:
        for item in line:
            if not [item] in candidate1:
                candidate1.append([item])
    candidate1.sort()
    return list(map(frozenset, candidate1))  # 返回list，每个元素为frozenset


# 通过频繁k项集生成候选项集k+1。
def candidateGenerate(ListK, k, hashTable, minSup, order, supportDictionary, lenOfData):
    ListK = list(map(frozenset, ListK))
    for item in ListK:
        for element in item:
            element = frozenset([element])
            numOfElement = supportDictionary[element]*lenOfData
            if numOfElement <= k:
                ListK.remove(item)      # 若对于候选项集k+1中元素而言少于k+1个，则从List去掉。
                continue

    candidateList = []
    lenListK = len(ListK)
    count = 0
    for i in range(lenListK):
        for j in range(i + 1, lenListK):
            L1 = list(ListK[i])[:k - 2]
            L2 = list(ListK[j])[:k - 2]
            L1.sort()
            L2.sort()
            if L1 == L2:
                hashValue = hashFunc(ListK[i], ListK[j], order)
                candidate = ListK[i] | ListK[j]

                if hashTable[hashValue] >= minSup:
                    candidateList.append(candidate)
                else:
                    print("remove", end=" ")
                    print(candidate)
    return candidateList, count


# 找出候选集中的频繁项集
def scanDataSet(dataSet, candidateK, minSup):
    countDictionary = {}  # 候选项计数字典
    hashTable = {}
    order = {}
    i=1
    for candidate in candidateK:
        order[candidate] = order.get(candidate, 0) + i
        i += 1

    for line in dataSet:
        candidateLine = []
        for candidate in candidateK:
            if candidate.issubset(line):
                candidateLine.append(candidate)
                countDictionary[candidate] = countDictionary.get(candidate, 0) + 1  # 计数字典
        if len(candidateLine) > 1:
            for i in range(len(candidateLine)):
                for j in range(i + 1, len(candidateLine)):
                    hashValue = hashFunc(candidateLine[i], candidateLine[j], order)
                    hashTable[hashValue] = hashTable.get(hashValue, 0) + 1

    itemNum = float(len(dataSet))
    frequentList = []
    supportDictionary = {}
    for key in countDictionary:
        support = countDictionary[key] / itemNum
        if support >= minSup:
            frequentList.insert(0, key)  # 将频繁项集插入返回列表的首部
            supportDictionary[key] = support
    return frequentList, supportDictionary, hashTable, order  # 返回频繁项集及其支持度


# 获取事务集中的所有的频繁项集
def aprioriReduce(dataSet, minSupport):
    candidate1 = findCandidate1(dataSet)  # 从事务集中获取候选1项集
    minSup = minSupport*len(dataSet)
    dataSet = list(map(set, dataSet))  # 将事务集转化为list，每个元素为set
    frequentList1, supportDictionary, hashTable, order = scanDataSet(dataSet, candidate1, minSupport)  # 获取频繁1项集和对应的支持度
    frequentList = [frequentList1]  # 初始化频繁集列表
    k = 1
    countAll = 0
    while len(frequentList[k - 1]) > 0:
        candidateK, count = candidateGenerate(frequentList[k - 1], k + 1, hashTable, minSup, order, supportDictionary,len(dataSet))  # 根据K频繁项集生成K+1候选项集
        countAll += count
        frequentListK, supportK, hashTable, order = scanDataSet(dataSet, candidateK, minSupport)  # 得到K+1频繁项集及其支持度
        frequentList.append(frequentListK)  # 添加新频繁项集
        supportDictionary.update(supportK)  # 更新支持度
        k += 1
    return frequentList, supportDictionary


if __name__ == '__main__':
    # 默认最小支持度和最小置信度
    minSupport = 0.04
    minConfidence = 0.3

    # 数据读取及清洗
    dataSet1 = loadDataSet1()

    # 调用算法
    frequentList, supportDictionary = aprioriReduce(dataSet1, minSupport)

    # 数据输出
    out_file_name = 'groceriesResult.txt'
    outputResult(out_file_name, supportDictionary, minConfidence)
