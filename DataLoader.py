file_name = 'data/groceries.csv'
file2_name = 'data/处方数据.csv'


# 读取‘groceries.csv’
def loadDataSet1():
    dataSet = []
    with open(file_name) as file_obj:
        for content in file_obj:
            content = content.rstrip().split(',')
            dataSet.append(content)
    return dataSet


# 读取‘处方数据.csv’
def loadDataSet2():
    dataSet = []
    with open(file2_name) as file2_obj:
        for content in file2_obj:
            content = content.rstrip().split(',')[1]
            content = content.split(':;')
            itemList = []
            for item in content:
                item = item.split(':')[0]
                itemList.append(item)
            if itemList[0] != 'NULL':
                dataSet.append(itemList[:len(itemList) - 1])
    return dataSet
