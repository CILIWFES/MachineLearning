from DataStructure.Tree import *
from DataProcessing.ORM import *
import numpy as np
from Global import *


# KD树,二叉树,左树为小等于,右侧为大等于
# key:特征列坐标
# value(list):为空表示其下还有分支
# leftNode: 小等于
# rightNode:大等于
class KDNode(BinaryNode):
    def __init__(self, befor, key, value, leftNode, rightNode):
        super().__init__(befor=befor, key=key, value=value, left=leftNode, right=rightNode)


class SearchSpace:
    def __init__(self, spaceLength=None):
        self.space = list()
        # 没有距离会比-1小
        self.minDistance = None
        self.spaceLength = spaceLength

    def put(self, data, distance):

        if self.minDistance is None:
            self.minDistance = distance

        if distance <= self.minDistance:
            self.minDistance = distance
            self.space.insert(0, (data, distance))
        else:
            isInser = False
            # 排序插入
            for index, item in enumerate(self.space):
                if item[1] > distance:
                    self.space.insert(index, (data, distance))
                    isInser = True
                    break
                elif item[1] == distance:  # 距离相等归一化
                    item[0] = np.vstack((item[0], data))
                    isInser = True
                    break
            if not isInser:
                self.space.append((data, distance))
        # 长度很重要的话
        if self.spaceLength is not None and self.spaceLength > len(self.space):
            self.space.pop(-1)

    def getALl(self):
        return self.space

    def getMinDistance(self):
        return self.minDistance


class KDSearch:
    def __init__(self, kdTree):
        self.searcheadNode = kdTree.headNode
        self.searchSpace = SearchSpace()

    # 以下有优先级判断
    # target         一维tuple
    # distant        距离
    # typeCounts     类型数量
    # realCounts     真实数量
    def Search(self, target: tuple):
        self._Search(target, self.searcheadNode)
        return self.searchSpace.space

    def _Search(self, target: tuple, node):
        if node.key is None:
            minDistrance = self.calculateDistant(node.value[-1], target)
            self.searchSpace.put(node.value, minDistrance)
            return
        distance = target[node.key] - node.value
        if distance < 0:
            self._Search(target, node.left)
            if self.searchSpace.getMinDistance() >= -distance:
                self._Search(target, node.right)

        elif distance > 0:
            self._Search(target, node.right)
            if self.searchSpace.getMinDistance() >= distance:
                self._Search(target, node.left)
        else:
            self._Search(target, node.left)
            self._Search(target, node.right)

    def calculateDistant(self, target, index):
        return np.sum(np.power(np.power(target - index, 2), 0.5))


#  临近距离树(可重复,二叉树)
class KDTree(BinaryTree):
    # dimension:维度
    # datas:二维数据集合
    # 头节点即第一道分界线
    def __init__(self):
        self.headNode = KDNode(None, None, None, None, None)

    @staticmethod
    def ORMLoad(path, fileName):
        return ORM.LoadPickle(path + fileName)

    def ORMSave(self, path, fileName):
        ORM.writePickle(path, fileName, self)

    def fit(self, datas):
        if len(datas) <= 0:
            raise Exception("请输入数据")
        datas = np.asanyarray(datas)
        self.toSplitTree(self.headNode, datas)

    def toSplitTree(self, node: KDNode, datas):
        splitIndex = self.selectColumnByStd(datas)
        if splitIndex is None:
            node.value = datas
            node.key = None
        else:
            leftRows, rightRows, median = self.Median(splitIndex, datas)
            leftNode, rightNode = self.creatNextNode(node, splitIndex, median)
            node.key = splitIndex
            node.value = median
            self.toSplitTree(leftNode, leftRows)
            self.toSplitTree(rightNode, rightRows)

    def creatNextNode(self, beforNode: KDNode, key, value):
        leftNode = KDNode(beforNode, key, value, None, None)
        rightNode = KDNode(beforNode, key, value, None, None)
        beforNode.left = leftNode
        beforNode.right = rightNode
        return leftNode, rightNode

    # numpy直接选取第一位
    def Median(self, columm, datas):
        # 获取列数据
        datasColumn = datas[:, columm]
        # 获取中位数
        median = np.median(datasColumn)
        # 拆分列
        leftRows = datas[datasColumn < median]
        difference = datasColumn.shape[-1] // 2 - leftRows.shape[-1]
        if difference != 0:
            rightRows = datas[datasColumn > median]
            medianRowIndex = datas[datasColumn == median]
            # 合并difference+1个到leftRowIndex,
            leftRows = np.vstack((leftRows, medianRowIndex[0:difference + 1]))
            # 剩下的去rightRowIndex
            rightRows = np.vstack((rightRows, medianRowIndex[difference + 1:]))
        else:
            rightRows = datas[datasColumn >= median]

        return leftRows, rightRows, median

    # 通过快排预估中间位
    def forecastMedian(self):
        pass

    # 返回标准差最大的列
    # 若皆小于0表示数组皆相等,返回None作为标志
    def selectColumnByStd(self, datas):
        shape = np.shape(datas)
        # 最小列信息,列坐标/标准差
        maxColumn_Info = [0, 0]

        for i in range(shape[1]):
            std = np.std(datas[:, i])
            # 选取最大特征列
            if std > maxColumn_Info[1]:
                maxColumn_Info[0] = i
                maxColumn_Info[1] = std

        return maxColumn_Info[0] if maxColumn_Info[1] != 0 else None

    def Search(self, target):
        search = KDSearch(self)
        return search.Search(target)


LoadPah = GLOCT.SUPPORT_PATH + "Algorithm/Pickle/Test/"
fileName = "KDTree"
# test
per = False
if per:
    kdTree = KDTree.ORMLoad(LoadPah, fileName)
    arr = ORM.LoadPickle(LoadPah + 'testArr')
else:
    arr = np.random.random((999999, 4))
    kdTree = KDTree()

kdTree.fit(arr)
if per:
    kdTree.ORMSave(LoadPah, fileName)
    ORM.writePickle(LoadPah, "testArr", arr)

print('________________________________')
print(kdTree.Search((0.123, 0.33, 0.22, 0.33)))


def calculateDistant(target, index):
    return np.sum(np.power(np.power(target - index, 2), 0.5))


min = 999
minIndex = None
for item in arr:
    mintemp = calculateDistant(item, (0.123, 0.33, 0.22, 0.33))
    if mintemp < min:
        min = mintemp
        minIndex = item

print(min)
print(minIndex)
