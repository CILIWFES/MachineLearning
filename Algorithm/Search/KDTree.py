from DataStructure.Tree import *
from DataProcessing.ORM import *
import numpy as np
from Analysis.PerformanceMeasure import *
from Global import *


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


class SearchSpace:
    # 最小距离
    MINFLAG = 0
    # 距离模式
    DISTANCEFLAG = MINFLAG + 1

    # flag:0 表示普通最小距离模式
    def __init__(self, searchModel=MINFLAG, searchDistance=None, merge=False):
        self.space = list()
        # 最小/最大距离
        self.minDistance = None
        self.maxDistance = None
        # 搜索模式
        self.searchModel = searchModel
        # 搜索的最小距离
        self.searchDistance = searchDistance
        # 相同距离允许合并
        self.merge = merge

    # 三种模式
    def put(self, data, distance):

        # 程序前处理
        if len(self.space) <= 0:
            self.minDistance = distance
            self.maxDistance = distance

        # ---------------------------前处理
        if self.searchModel == SearchSpace.DISTANCEFLAG \
                and self.searchDistance < distance:
            # 距离模式,长度超过距离
            if len(self.space) <= 0:
                # 默认就要清零
                self.minDistance = None
                self.maxDistance = None
            return
        # ---------------------------中间流程
        # 开始插入
        if distance <= self.minDistance:
            # 小于最小要单独统计最小值
            self.space.insert(0, (data, distance))
            self.minDistance = distance

        elif distance >= self.maxDistance:
            self.space.append((data, distance))
            self.maxDistance = distance
        else:
            isInser = False
            # 排序插入
            for index, item in enumerate(self.space):
                if item[1] > distance:
                    self.space.insert(index, (data, distance))
                    isInser = True
                    break
                elif item[1] == distance:  # 距离相等判断是否合并
                    if self.merge:  # 开始合并
                        item[0] = np.vstack((item[0], data))
                    else:  # 取消合并
                        self.space.insert(index, (data, distance))
                    isInser = True
                    break

            if not isInser:
                self.space.append((data, distance))

        # ---------------------------后处理
        pass

    def getSpace(self):
        return self.space

    def getSelectDistance(self):
        if self.searchModel == SearchSpace.MINFLAG:
            return self.minDistance
        elif self.searchModel == SearchSpace.DISTANCEFLAG:
            return self.searchDistance


class KDSearch:
    # 最小距离
    MINFLAG = SearchSpace.MINFLAG

    # 距离模式
    DISTANCEFLAG = SearchSpace.DISTANCEFLAG

    # 数量模式
    COUNTSFLAG = DISTANCEFLAG + 1

    # 所有元素搜索模式(相当于排序)
    ALLFLAG = COUNTSFLAG + 1

    def __init__(self, kdTree, searchModel=MINFLAG, searchCount=10, magnification=1, searchDistance=None, merge=False):
        self.searcheadNode = kdTree.headNode
        # 搜索模式
        self.searchModel = searchModel
        # 搜索数量/搜索模式距离放大倍数
        self.searchCount = searchCount
        self.magnification = magnification
        # 搜索距离
        self.searchDistance = searchDistance
        self.searchSpace = SearchSpace(searchModel=searchModel, searchDistance=searchDistance, merge=merge)

    # 以下有优先级判断
    # target         一维tuple
    # distant        距离
    # typeCounts     类型数量
    # realCounts     真实数量
    def Search(self, target: tuple):
        # 最小值模式
        if self.searchModel == KDSearch.MINFLAG:
            self._Search(target, self.searcheadNode)
            space = self.searchSpace.getSpace()
        # 距离模式
        elif self.searchModel == KDSearch.DISTANCEFLAG:
            self._Search(target, self.searcheadNode)
            space = self.searchSpace.getSpace()
        # 数量模式(不推荐)
        elif self.searchModel == KDSearch.COUNTSFLAG:
            space = self._SearchByCounts(target)
        else:
            raise Exception("请输入搜索模式")

        return space

    def _SearchByCounts(self, target):
        # 数量搜索模式本质上是距离与最小型的组合搜索
        if self.searchCount == self.searcheadNode.len:
            self.searchModel = KDSearch.ALLFLAG
            self._Search(target, self.searcheadNode)
            space = self.searchSpace.getSpace()

        # 直接报错
        elif self.searchCount > self.searcheadNode.len:
            raise Exception("错误,数量超出长度")
        else:
            self.searchModel = KDSearch.MINFLAG
            self.searchSpace.searchModel = KDSearch.MINFLAG
            self._Search(target, self.searcheadNode)
            space = self.searchSpace.getSpace()
            spaceLength = len(space)
            while spaceLength < self.searchCount:
                self.searchSpace.space = []
                self.searchModel = KDSearch.DISTANCEFLAG
                # 下一次的搜索距离是 当前最大距离(需要查找的元素总数/当前搜索出的元素数)*放大倍数
                self.searchDistance = space[-1][1] * (self.searchCount / spaceLength) * self.magnification

                self.searchSpace.searchModel = KDSearch.DISTANCEFLAG
                self.searchSpace.searchDistance = self.searchDistance

                self._Search(target, self.searcheadNode)
                space = self.searchSpace.getSpace()
                # 获取最大距离简单查询
                spaceLength = len(space)
        self.searchModel = KDSearch.COUNTSFLAG
        self.searchDistance = None
        return space[0:self.searchCount]

    def _Search(self, target: tuple, node):
        if node.key is None:
            minDistrance = self.calculateDistant(node.value[-1], target)
            self.searchSpace.put(node.value, minDistrance)
            return
        distance = target[node.key] - node.value
        if distance < 0:
            self._Search(target, node.left)
            if self.searchSpace.getSelectDistance() >= -distance:
                self._Search(target, node.right)

        elif distance > 0:
            self._Search(target, node.right)
            if self.searchSpace.getSelectDistance() >= distance:
                self._Search(target, node.left)
        else:
            self._Search(target, node.left)
            self._Search(target, node.right)

    def calculateDistant(self, target, index):
        return np.sum(np.power(np.power(target - index, 2), 0.5))


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
arrSize = (9999, 2)

array = np.random.random(arrSize)

target = (np.random.random((1, arrSize[1])).tolist())[-1]
print('测试坐标', target)

performance = False
if performance:
    kdTree = KDTree.ORMLoad(LoadPah, fileName)
    array = ORM.LoadPickle(LoadPah + 'test_Array')
else:
    kdTree = KDTree()
    MPoint.setPoint()
    kdTree.fit(array)
    MPoint.showPoint()

if performance:
    kdTree.ORMSave(LoadPah, fileName)
    ORM.writePickle(LoadPah, "test_Array", array)

print('________________________________')


def calculateDistant(target, index):
    return np.sum(np.power(np.power(target - index, 2), 0.5))


def test_KDTree():
    return kdTree.Search(target, searchModel=KDSearch.COUNTSFLAG, searchCount=20)


def test_Array():
    lst=[]
    for item in array:
        mintemp = calculateDistant(item, target)
        lst.append(mintemp)
    return lst


print(test_KDTree())
print(test_Array())
timeM = TimeM(test_KDTree)
timeM.StartTimeMeasure(1)
timeM = TimeM(test_Array)
timeM.StartTimeMeasure(1)
