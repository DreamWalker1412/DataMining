# Apriori算法实现
from numpy import *
from DataLoader import *
from ResultOutput import *


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
def candidateGenerate(ListK, k, supportDictionary, lenOfData):
    ListK = list(map(frozenset, ListK))

    for item in ListK:
        for element in item:
            element = frozenset([element])
            numOfElement = supportDictionary[element] * lenOfData
            if numOfElement <= k:
                ListK.remove(item)  # 若对于候选项集k+1中元素而言少于k+1个，则从List去掉。
                continue
    frequentList = []
    lenListK = len(ListK)
    for i in range(lenListK):
        for j in range(i + 1, lenListK):
            L1 = list(ListK[i])[:k - 2]
            L2 = list(ListK[j])[:k - 2]
            L1.sort()
            L2.sort()
            if L1 == L2:
                frequentList.append(ListK[i] | ListK[j])  # 取出并比较两个集合的前k-1个元素，若相同则合并
    return frequentList


# 找出候选集中的频繁项集
def scanDataSet(dataSet, candidateK, minSupport):
    countDictionary = {}  # 候选项计数字典
    for line in dataSet:
        for candidate in candidateK:
            if candidate.issubset(line):
                countDictionary[candidate] = countDictionary.get(candidate, 0) + 1  # 计数字典
    itemNum = float(len(dataSet))
    frequentList = []
    supportDictionary = {}
    for key in countDictionary:
        support = countDictionary[key] / itemNum
        if support >= minSupport:
            frequentList.insert(0, key)  # 将频繁项集插入返回列表的首部
            supportDictionary[key] = support
    return frequentList, supportDictionary  # 返回频繁项集及其支持度


# 获取事务集中的所有的频繁项集
def aprioriReduce2(dataSet, minSupport):
    candidate1 = findCandidate1(dataSet)  # 从事务集中获取候选1项集
    dataSet = list(map(set, dataSet))  # 将事务集转化为list，每个元素为set
    frequentList1, supportDictionary = scanDataSet(dataSet, candidate1, minSupport)  # 获取频繁1项集和对应的支持度
    frequentList = [frequentList1]  # 初始化频繁集列表
    k = 1
    while len(frequentList[k - 1]) > 0:
        candidateK = candidateGenerate(frequentList[k - 1], k + 1, supportDictionary, len(dataSet))  # 根据K频繁项集生成K+1候选项集
        frequentListK, supportK = scanDataSet(dataSet, candidateK, minSupport)  # 得到K+1频繁项集及其支持度
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
    frequentList, supportDictionary = aprioriReduce2(dataSet1, minSupport)

    # 数据输出
    out_file_name = 'groceriesResult.txt'
    outputResult(out_file_name, supportDictionary, minConfidence)
