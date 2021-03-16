from DataLoader import *
from ResultOutput import *


# 正则化数据集
def normDataSet(dataSet):
    dataDictionary = {}  # 创建字典
    for line in dataSet:
        dataDictionary[frozenset(line)] = 1
    return dataDictionary


# FP树类
class treeNode:
    def __init__(self, nameValue, times, parentNode):
        self.name = nameValue  # 节点名称
        self.count = times  # 出现次数
        self.nodeBother = None  # 指向下一个同级节点的指针
        self.parent = parentNode  # 指向父节点的指针，在构造时初始化为给定值
        self.children = {}  # 指向子节点的字典，键为子节点的元素名，值为指向子节点的指针

    # 增加节点的出现次数值
    def addCount(self, times):
        self.count += times

    # 输出节点和子节点的FP树结构
    def disp(self, numOfSpace=1):
        if self.name != "Root":
            print(' ' * numOfSpace, self.name, ' ', self.count)
        else:
            print(' ' * numOfSpace, self.name)
        for child in self.children.values():
            child.disp(numOfSpace + 4)


# FP树构建
# 更新头指针块,添加到同级链表的尾部
def updateHeader(nodeToTest, targetNode):
    while nodeToTest.nodeBother is not None:
        nodeToTest = nodeToTest.nodeBother
    nodeToTest.nodeBother = targetNode


# 根据一个排序后的频繁项更新FP树
def updateTree(items, node, headerTable, count):
    if items[0] in node.children:
        node.children[items[0]].addCount(count)   # 有该项时计数值+1
    else:
        node.children[items[0]] = treeNode(items[0], count, node)   # 没有时则创建一个新节点
        if headerTable[items[0]][1] is None:  # 如果是第一次出现，则在头指针表中增加对该节点的指向
            headerTable[items[0]][1] = node.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], node.children[items[0]])
    if len(items) > 1:
        # 对剩下的元素项迭代调用updateTree函数
        updateTree(items[1::], node.children[items[0]], headerTable, count)


# 创建FP树
def createTree(dataSet, minSup):
    # 第一次遍历数据集，创建头指针表
    headerTable = {}
    for line in dataSet:
        for item in line:
            headerTable[item] = headerTable.get(item, 0) + dataSet[line]

    # 移除不满足最小支持度的元素项
    keys = list(headerTable.keys())
    for item in keys:
        if headerTable[item] < minSup:
            del (headerTable[item])

    freqItemSet = set(headerTable.keys())
    if len(freqItemSet) == 0:
        return None, None   # 若不存在任何频繁项集，返回空

    # 在头指针表中添加用于存放指向兄弟节点指针
    for item in headerTable:
        headerTable[item] = [headerTable[item], None]  # 每个键的值，第一个为个数，第二个为下一个节点的位置

    rootTree = treeNode('Root', 0, None)  # 根节点

    # 第二次遍历数据集，创建FP树
    for data, count in dataSet.items():
        countDictionary = {}  # 记录频繁1项集的全局频率，用于排序
        for item in data:
            if item in freqItemSet:  # 只考虑频繁项
                countDictionary[item] = headerTable[item][0]
        if len(countDictionary) > 0:
            orderedItems = [v[0] for v in sorted(countDictionary.items(), key=lambda p: p[1], reverse=True)]  # 排序
            updateTree(orderedItems, rootTree, headerTable, count)  # 更新FP树
    return rootTree, headerTable


# 递归添加其父节点。
def ascendTree(leafNode, prefixPath):
    if leafNode.parent is not None:
        prefixPath.append(leafNode.name)    # prefixPath就是一条从treeNode到根节点的路径，但不包含根节点
        ascendTree(leafNode.parent, prefixPath)


# 返回条件模式基，用一个字典表示，键为前缀路径，值为计数值。
def findPrefixPath(treeNode):
    condPats = {}  # 存储条件模式基
    while treeNode is not None:
        prefixPath = []  # 用于存储前缀路径
        ascendTree(treeNode, prefixPath)  # 生成前缀路径
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.count  # 出现的数量就是当前叶子节点的数量
        treeNode = treeNode.nodeBother  # 遍历下一个相同元素
    return condPats


# 递归查找频繁项集
# preFix请传入一个空集合（set([])），将在函数中用于保存当前前缀。
# freqItemList请传入一个空列表（[]），将用来储存生成的频繁项集。
def findFreqItem(headerTable, minSup, preFix, freqItemList):
    # 对频繁项按出现的数量进行排序进行排序
    sorted_headerTable = sorted(headerTable.items(), key=lambda p: p[1][0])  # 返回重新排序的列表
    freqSet = [v[0] for v in sorted_headerTable]  # 获取频繁项
    for base in freqSet:
        newFreqSet = preFix.copy()  # 新的频繁项集
        newFreqSet.add(base)  # 当前前缀添加一个新元素
        freqItemList.append(newFreqSet)  # 所有的频繁项集列表
        condPattBases = findPrefixPath(headerTable[base][1])  # 获取条件模式基。就是base元素的所有前缀路径。它像一个新的事务集
        rootTree, myHead = createTree(condPattBases, minSup)  # 创建条件FP树
        if myHead is not None:
            findFreqItem(myHead, minSup, newFreqSet, freqItemList)  # 递归直到不再有元素


# 获取频繁集支持度
def getSupportData(freqItems,dataSet):
    freqItems = list(map(frozenset, freqItems))
    countDictionary = {}  # 记录每个候选项的个数
    for line in dataSet:
        for item in freqItems:
            if item.issubset(line):
                countDictionary[item] = countDictionary.get(item, 0) + 1  # 计数字典
    supportDictionary = {}
    for key in countDictionary:
        supportDictionary[key] = countDictionary[key] / len(dataSet)
    return supportDictionary


def fpTree(dataSet, minSupport):
    minSup = int(len(dataSet) * minSupport)
    initSet = normDataSet(dataSet)  # 转化为符合格式的事务集
    rootFPtree, headerFPtree = createTree(initSet, minSup)  # 初始化FP树，得到头指针表

    preFix = set([])  # 用于存储前缀
    freqItems = []  # 用于存储频繁项集
    findFreqItem(headerFPtree, minSup, preFix, freqItems)  # 获取频繁项集
    supportDictionary = getSupportData(freqItems, dataSet)
    return freqItems, supportDictionary


if __name__ == '__main__':
    # 默认最小支持度和最小置信度
    minSupport = 0.04
    minConfidence = 0.3

    # 加载数据集
    dataSet = loadDataSet1()

    # 调用算法
    frequentList, supportDictionary = fpTree(dataSet, minSupport)

    out_file_name = "fp_result.txt"
    outputResult(out_file_name, supportDictionary, minConfidence)
