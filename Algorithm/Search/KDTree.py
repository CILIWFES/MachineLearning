from DataStructure.Tree import *
from DataProcessing.ORM import *
import numpy as np
from Analysis.PerformanceMeasure import *
from Global import *
from Algorithm.SortList import *


# KD树,二叉树,左树为小等于,右侧为大等于
# key:特征列坐标
# value(list):为空表示其下还有分支
# leftNode: 小等于
# rightNode:大等于
class KDNode(BinaryNode):
    def __init__(self, befor, key, value, leftNode, rightNode):
        super().__init__(befor=befor, key=key, value=value, left=leftNode, right=rightNode)
        self.max = None
        self.min = None
        self.len = None


class KDSearch:
    # 最小距离
    MINFLAG = 0

    # 距离模式
    DISTANCEFLAG = MINFLAG + 1

    # 数量模式
    COUNTSFLAG = DISTANCEFLAG + 1

    # 所有元素搜索模式(相当于排序)
    ALLFLAG = COUNTSFLAG + 1

    def __init__(self, kdTree, searchModel=MINFLAG, searchCount=10, magnification=1, searchDistance=None, merge=False):
        self.sortList = None
        self.merge = merge
        self.searcheadNode = kdTree.headNode
        # 搜索模式
        self.searchModel = searchModel
        # 搜索数量/搜索模式距离放大倍数
        self.searchCount = searchCount
        self.magnification = magnification
        # 搜索距离
        self.searchDistance = searchDistance

    # 以下有优先级判断
    # target         一维tuple
    # distant        距离
    # typeCounts     类型数量
    # realCounts     真实数量
    def Search(self, target: tuple):
        self.sortList = self.buildSortList(target)
        # 最小值模式
        if self.searchModel == KDSearch.MINFLAG:
            self._SearchByDistance(target, self.searcheadNode)
            retList = self.sortList.getAllList()
        # 距离模式
        elif self.searchModel == KDSearch.DISTANCEFLAG:
            self._SearchByDistance(target, self.searcheadNode)
            retList = self.sortList.getAllList()
        # 数量模式(不推荐)
        elif self.searchModel == KDSearch.COUNTSFLAG:
            retList = self._SearchByCounts(target)
        else:
            raise Exception("请输入搜索模式")

        return retList

    def buildSortList(self, target):
        # 构造计算方法
        def calculateDistant(index):
            return self.calculateDistant(index, target)

        mergeFunction = None
        if self.merge:
            mergeFunction = self.mergeFunction

        return SortList(calculateDistant, mergeFunc=mergeFunction, model=SortList.MIN, cntsLimit=self.searchCount)

    def _SearchByCounts(self, target):
        # 数量搜索模式本质上是距离与最小型的组合搜索
        if self.searchCount == self.searcheadNode.len:
            raise Exception("错误,数量等于长度")
        # 直接报错
        elif self.searchCount > self.searcheadNode.len:
            raise Exception("错误,数量超出长度")
        else:
            self.searchModel = KDSearch.MINFLAG
            self._SearchByDistance(target, self.searcheadNode)
            allList = self.sortList.getAllList()

            allList = allList[0:self.searchCount]
            list_Len = len(allList)
            self.searchDistance = allList[-1][SortList.ValueIndex] * (self.searchCount / list_Len) * self.magnification
            list_Len = 0
            while list_Len < self.searchCount:
                self.sortList.clear()
                self.searchModel = KDSearch.DISTANCEFLAG

                self._SearchByDistance(target, self.searcheadNode)
                allList = self.sortList.getAllList()

                list_Len = len(allList)
                # 下一次的搜索距离是 当前最大距离(需要查找的元素总数/当前搜索出的元素数)*放大倍数
                self.searchDistance = allList[-1][SortList.ValueIndex] * (
                        self.searchCount / list_Len) * self.magnification

        self.searchModel = KDSearch.COUNTSFLAG
        self.searchDistance = None
        return self.sortList.getAllList()[0:self.searchCount]

    # 对距离进行搜索
    def _SearchByDistance(self, target: tuple, node):
        if node.key is None:
            minDistrance = self.calculateDistant(node.value[-1], target)
            self.sortList.put(node.value, minDistrance)
            return
        distance = target[node.key] - node.value
        if distance < 0:
            self._SearchByDistance(target, node.left)
            if self.judgmentDistance() >= -distance:
                self._SearchByDistance(target, node.right)

        elif distance > 0:
            self._SearchByDistance(target, node.right)
            if self.judgmentDistance() >= distance:
                self._SearchByDistance(target, node.left)
        else:
            self._SearchByDistance(target, node.left)
            self._SearchByDistance(target, node.right)

    def judgmentDistance(self):
        # 最小值模式
        if self.searchModel == KDSearch.MINFLAG:
            val = self.sortList.getMinVal()
        # 距离模式
        elif self.searchModel == KDSearch.DISTANCEFLAG:
            val = self.searchDistance
        else:
            raise Exception("搜索模式错误")

        return val

    def calculateDistant(self, target, index):
        return np.sum(np.power(np.power(target - index, 2), 0.5))

    def mergeFunction(self, merge1, merge2):
        return np.vstack((merge1, merge2))


#  临近距离树(可重复,二叉树)
class KDTree(BinaryTree):
    # 忽略标准差选取长度
    IGNORESTDLEN = 32

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
        if len(datas) == 1:
            # 长度1不需要计算
            node.value = datas
            node.key = None
            return
        else:
            splitIndex = self.selectColumnByStd(datas)

        if splitIndex is None:
            node.key = None
            node.value = datas
            node.len = datas.shape[1]
        else:
            leftRows, rightRows, median, min, max = self.Median(splitIndex, datas)
            node.min = min
            node.max = max
            node.len = datas.shape[0]
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
        max = np.max(datasColumn)
        min = np.min(datasColumn)
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

        return leftRows, rightRows, median, min, max

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
                # 小于忽略长度不需要挨个计算节省算力
                if len(datas) <= KDTree.IGNORESTDLEN:
                    break

        return maxColumn_Info[0] if maxColumn_Info[1] != 0 else None

    def Search(self, target, searchModel=KDSearch.MINFLAG, searchCount=None, magnification=1, searchDistance=None,
               merge=False):

        search = KDSearch(self, searchModel, searchCount, magnification, searchDistance, merge)
        return search.Search(target)


LoadPah = GLOCT.SUPPORT_PATH + "Algorithm/Pickle/Test/"
fileName = "test_KDTree"
# test
arrSize = (999999, 5)

target = (np.random.random((1, arrSize[1])).tolist())[-1]


performance = True
if performance:
    kdTree = KDTree.ORMLoad(LoadPah, fileName)
    array = ORM.LoadPickle(LoadPah + 'test_Array')
else:
    array = np.random.random(arrSize)
    kdTree = KDTree()
    MPoint.setPoint()
    kdTree.fit(array)
    MPoint.showPoint()

if not performance:
    kdTree.ORMSave(LoadPah, fileName)
    ORM.writePickle(LoadPah, "test_Array", array)


def calculateDistant(index):
    return np.sum(np.power(np.power(target - index, 2), 0.5))


def test_KDTree():
    return [i[-1] for i in kdTree.Search(target, searchModel=KDSearch.COUNTSFLAG, searchCount=10)]


def test_Array():
    sortList = SortList(getValFunc=calculateDistant, cntsLimit=1)
    for item in array:
        sortList.put(item)
    return sortList.getValList()


print('________________________________')
print('测试坐标', target)
print('KD', test_KDTree())
print('Arr', test_Array())
timeM = TimeM(test_KDTree)
timeM.StartTimeMeasure(1)
timeM = TimeM(test_Array)
timeM.StartTimeMeasure(1)
