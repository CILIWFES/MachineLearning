from DataStructure.Tree import *
from DataProcessing.ORM import *
import numpy as np
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
    MIN_TYPE = 0
    # 距离模式
    DISTANCE_TYPE = MIN_TYPE + 1

    # 数量模式
    COUNTS_TYPE = DISTANCE_TYPE + 1

    def __init__(self, kdTree, searchColums, searchModel=MIN_TYPE,
                 searchCount=10, magnification=1, searchDistance=None,
                 merge=False):
        self.sortList = None
        self.merge = merge
        self.searcheadNode = kdTree.headNode
        self.kdTree = kdTree
        # 搜索模式
        self.searchModel = searchModel
        # 搜索数量/搜索模式距离放大倍数
        self.searchCount = searchCount
        self.magnification = magnification
        # 搜索距离
        self.searchDistance = searchDistance
        # 有效计算列
        self.searchColums = searchColums

    # 以下有优先级判断
    # target         一维tuple
    # distant        距离
    # typeCounts     类型数量
    # realCounts     真实数量
    def Search(self, target, searchType):
        self.sortList = self.buildSortList(target, searchType)
        # 最小值模式
        if self.searchModel == KDSearch.MIN_TYPE:
            self._SearchByDistance(target, self.searcheadNode)
            retList = self.sortList.getAllList()
        # 距离模式
        elif self.searchModel == KDSearch.DISTANCE_TYPE:
            self._SearchByDistance(target, self.searcheadNode)
            retList = self.sortList.getAllList()
        # 数量模式(不推荐)
        elif self.searchModel == KDSearch.COUNTS_TYPE:
            retList = self._SearchByCounts(target)
        else:
            raise Exception("请输入搜索模式")
        return self.conversionList(retList)

    # 适配target输入格式
    def buildRealTarget(self, target):
        target = np.asarray(target)
        if target.shape[1] == len(self.kdTree.searchColums):
            return target
        else:
            return target[:, self.kdTree.searchColums]

    def buildSortList(self, target, searchType=SortList.INTERPOLATIONSEARCH):
        # 构造计算方法
        def calculateDistant(index):
            index = self.getData(index)
            return self.calculateDistant(index, target)

        if self.merge:
            mergeFunction = self.mergeFunction
        else:
            mergeFunction = None

        return SortList(searchType=searchType, getValFunc=calculateDistant, mergeFunc=mergeFunction, model=SortList.MIN,
                        cntsLimit=self.searchCount)

    def _SearchByCounts(self, target):
        # 数量搜索模式本质上是距离与最小型的组合搜索
        if self.searchCount == self.searcheadNode.len:
            raise Exception("错误,数量等于长度")
        # 直接报错
        elif self.searchCount > self.searcheadNode.len:
            raise Exception("错误,数量超出长度")
        else:
            self.searchModel = KDSearch.MIN_TYPE
            self._SearchByDistance(target, self.searcheadNode)
            allList = self.sortList.getAllList()

            allList = allList[0:self.searchCount]
            list_Len = len(allList)
            self.searchDistance = allList[-1][SortList.ValueIndex] * (self.searchCount / list_Len) * self.magnification
            list_Len = 0
            while list_Len < self.searchCount:
                self.sortList.clear()
                self.searchModel = KDSearch.DISTANCE_TYPE

                self._SearchByDistance(target, self.searcheadNode)
                allList = self.sortList.getAllList()

                list_Len = len(allList)
                # 下一次的搜索距离是 当前最大距离(需要查找的元素总数/当前搜索出的元素数)*放大倍数
                self.searchDistance = allList[-1][SortList.ValueIndex] * (
                        self.searchCount / list_Len) * self.magnification

        self.searchModel = KDSearch.COUNTS_TYPE
        self.searchDistance = None
        return self.sortList.getAllList()[0:self.searchCount]

    # 对距离进行搜索
    def _SearchByDistance(self, target, node):
        if node.key is None:
            # 转化真实坐标
            node_data = self.getData(node.value)
            minDistrance = self.calculateDistant(node_data[-1], target)
            # 存入索引,以value来维护
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
        if self.searchModel == KDSearch.MIN_TYPE:
            val = self.sortList.getMinVal()
        # 距离模式
        elif self.searchModel == KDSearch.DISTANCE_TYPE:
            val = self.searchDistance
        else:
            raise Exception("搜索模式错误")
        return val

    # 根据坐标获取真实数据
    # 返回数据点,距离
    def conversionList(self, retList):
        indexs = np.asarray([], dtype=int)
        for item in retList:
            indexs = np.hstack((item[SortList.DataIndex], indexs))
        distances = [item[SortList.ValueIndex] for item in retList]
        datas = self.kdTree.datas[indexs].tolist()
        return datas, distances

        # 根据坐标获取真实数据

    def getData(self, index):
        return self.kdTree.datas[index]

    def calculateDistant(self, index, target):
        return np.sum(np.power(np.power(index - target, 2), 0.5))

    def mergeFunction(self, merge1, merge2):
        return np.vstack((merge1, merge2))


#  临近距离树(可重复,二叉树)
class KDTree(BinaryTree):
    # 忽略标准差选取长度
    IGNORESTD_LEN = 32
    # 最小距离
    MIN_TYPE = KDSearch.MIN_TYPE
    # 距离模式
    DISTANCE_TYPE = KDSearch.DISTANCE_TYPE

    # 数量模式
    COUNTS_TYPE = KDSearch.COUNTS_TYPE

    # dimension:维度
    # datas:二维数据集合
    # 头节点即第一道分界线
    def __init__(self):
        self.headNode = KDNode(None, None, None, None, None)
        # 计算数据
        self.datas = []
        # 总数据列
        self.datasAll = []
        # 搜索坐标集合
        self.searchColums: list = None

    @staticmethod
    def ORMLoad(path, fileName):
        return ORM.LoadPickle(path + fileName)

    def ORMSave(self, path, fileName):
        ORM.writePickle(path, fileName, self)

    def fit(self, datas, ignorColums: list = None):
        if len(datas) <= 0:
            raise Exception("请输入数据")

        datas = np.asanyarray(datas)
        self.datasAll = datas
        # 构建搜索列
        self.searchColums: list = self.buildAvailableColums(datas.shape[1], ignorColums)
        # 构建计算信息列
        self.datas = datas[:, self.searchColums]
        # 构建坐标索引
        datas = np.hstack((self.datas, np.arange(datas.shape[0]).reshape(datas.shape[0], 1)))
        self.toSplitTree(self.headNode, datas)

    def toSplitTree(self, node: KDNode, datas):
        # 记录数组数量
        node.len = datas.shape[0]
        if len(datas) == 1:
            node.key = None
            # 保持索引
            node.value = datas[:, -1].astype(int)
            return
        else:
            splitIndex = self.selectColumnByStd(datas)

        if splitIndex is None:
            node.key = None
            # 保持索引
            node.value = datas[:, -1].astype(int)
        else:
            leftRows, rightRows, median = self.Median(splitIndex, datas)
            leftNode, rightNode = self.creatNextNode(node, splitIndex, median)
            node.key = splitIndex
            node.value = median
            self.toSplitTree(leftNode, leftRows)
            self.toSplitTree(rightNode, rightRows)

    def buildAvailableColums(self, columsSize, ignorColums: list) -> list:
        if ignorColums is None:
            ignorColums = []
        self.ignorColums = ignorColums
        return [i for i in range(columsSize) if i not in ignorColums]

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

    # 返回标准差最大的列
    # 若皆小于0表示数组皆相等,返回None作为标志
    def selectColumnByStd(self, datas):
        shape = np.shape(datas)
        # 最小列信息,列坐标/标准差
        maxColumn_Info = [0, 0]

        for i in self.searchColums:
            std = np.std(datas[:, i])
            # 选取最大特征列
            if std > maxColumn_Info[1]:
                maxColumn_Info[0] = i
                maxColumn_Info[1] = std
                # 小于忽略长度不需要挨个计算节省算力
                if len(datas) <= KDTree.IGNORESTD_LEN:
                    break

        return maxColumn_Info[0] if maxColumn_Info[1] != 0 else None

    # magnification放大倍数
    def Search(self, target, searchModel=MIN_TYPE, searchCount=None, magnification=1, searchDistance=None,
               merge=False, sortListType=SortList.INTERPOLATIONSEARCH):
        search = KDSearch(self, self.searchColums, searchModel, searchCount, magnification, searchDistance, merge)
        return search.Search(target, searchType=sortListType)
