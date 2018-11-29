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

    def __init__(self, kdTree, searchColums, searchModel, searchCount, magnification, searchDistance, merge):
        #  排序数组
        self.sortList = None
        # 是否合并
        self.merge = merge
        # 计算数据
        self.calculateDatas = kdTree.calculateDatas
        # 真实数据
        self.datas = kdTree.datas
        # 搜索起始节点
        self.searcheadNode = kdTree.headNode
        # 搜索模式 最小距离/距离模式/数量模式
        self.searchModel = searchModel
        # 搜索数量
        self.searchCount = searchCount
        # 搜索距离
        self.searchDistance = searchDistance
        # 多次搜索模式距离放大倍数
        self.magnification = magnification
        # 有效计算列
        self.searchColums = searchColums

    # 开始搜索
    def Search(self, target, searchType):
        target = self._buildRealTarget(target)

        # 建立排序数值
        self.sortList = self._buildSortList(target, searchType, self.searchCount)
        # 最小值模式
        if self.searchModel == KDSearch.MIN_TYPE:
            # 通过本质距离搜索
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
        return self._getDatasList(retList)

    # 通过邻近数量来搜索
    def _SearchByCounts(self, target):
        # 数量搜索模式本质上是距离与最小型的组合搜索
        if self.searchCount == self.searcheadNode.len:
            raise Exception("错误,数量等于长度")
        # 直接报错
        elif self.searchCount > self.searcheadNode.len:
            raise Exception("错误,数量超出长度")
        else:
            magnTemp = self.magnification
            # 先简单搜索
            self.searchModel = KDSearch.MIN_TYPE
            # 查询最近距离数组
            self._SearchByDistance(target, self.searcheadNode)
            allList = self.sortList.getAllList()
            list_Len = len(allList)
            while list_Len < self.searchCount or self.searchModel == KDSearch.MIN_TYPE:
                lastVal = allList[-1][SortList.ValueIndex]
                self.sortList.clear()
                # 自动调整搜索范围
                self.searchDistance, magnTemp = self.increaseByDegrees(lastVal, list_Len, magnTemp)
                # 切换距离搜索
                self.searchModel = KDSearch.DISTANCE_TYPE
                self._SearchByDistance(target, self.searcheadNode)
                allList = self.sortList.getAllList()
                list_Len = len(allList)
        self.searchModel = KDSearch.COUNTS_TYPE
        self.searchDistance = None
        return self.sortList.getAllList()[0:self.searchCount]

    # 计算递增放大倍数
    def increaseByDegrees(self, lastVal, search_List_Len: int, magnification):
        distrance = lastVal * (self.searchCount / search_List_Len) * magnification
        magnification += self.magnification
        return distrance, magnification

    # 对距离进行搜索(最小距离与邻近距离)
    def _SearchByDistance(self, target, node):
        # 节点值为空,表示存在数据
        if node.key is None:
            #  获取计算坐标坐标
            node_data = self._getCalculateData(node.value)
            # 计算距离
            minDistrance = self._calculateDistant(node_data[-1], target)
            # 存入索引,以value来维护
            self.sortList.put(node.value, minDistrance)
            return
        distance = target[node.key] - node.value
        # 在树左节点
        if distance < 0:
            self._SearchByDistance(target, node.left)
            # 判定选择的距离类型
            if self._judgmentDistance() >= -distance:
                self._SearchByDistance(target, node.right)
        # 树右节点
        elif distance > 0:
            self._SearchByDistance(target, node.right)
            # 判定选择的距离类型
            if self._judgmentDistance() >= distance:
                self._SearchByDistance(target, node.left)
        # 相等左右互搜
        else:
            self._SearchByDistance(target, node.left)
            self._SearchByDistance(target, node.right)

    # 判定选择的距离类型
    def _judgmentDistance(self):
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
    def _getDatasList(self, retList):
        indexs = np.asarray([], dtype=int)
        distances = [item[SortList.ValueIndex] for item in retList]
        datas = self.datas[indexs].tolist()
        return datas, distances

    # 适配target输入格式
    def _buildRealTarget(self, target):
        target = np.asarray(target)
        if target.shape[-1] == len(self.searchColums):
            return target
        else:
            return target[:, self.searchColums]

    # 建立排序数组
    # target 目标数据
    # searchType 排序引擎
    def _buildSortList(self, target, searchType, cntsLimit):
        # 构造闭包计算
        def calculateDistant(index):
            index = self._getCalculateData(index)
            return self._calculateDistant(index, target)

        # 检查是否提供合并方法
        if self.merge:
            mergeFunction = self._mergeFunction
        else:
            mergeFunction = None
        # 构建排序列表
        return SortList(searchType=searchType, getValFunc=calculateDistant, mergeFunc=mergeFunction,
                        model=SortList.MIN,
                        cntsLimit=cntsLimit)

    # 获取计算数据
    def _getCalculateData(self, index):
        return self.calculateDatas[index]

    # 计算距离方程
    def _calculateDistant(self, index, target):
        return np.sum(np.power(np.power(index - target, 2), 0.5))

    # 合并方法
    def _mergeFunction(self, merge1, merge2):
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

    def __init__(self):
        self.headNode = KDNode(None, None, None, None, None)
        # 计算数据
        self.calculateDatas = []
        # 总数据列
        self.datas = []
        # 搜索坐标集合
        self.searchColums: list = None

    @staticmethod
    def ORMLoad(path):
        kDTree: KDTree = ORM.LoadPickle(path)
        kDTree._initKDTree()
        return kDTree

    # 加载搜索列表,构建计算数据
    def _initKDTree(self):
        if self.searchColums is None:
            self.calculateDatas = self.datas
        else:
            self.calculateDatas = self.datas[:, self.searchColums]
        return self.calculateDatas

    def ORMSave(self, path, fileName):
        # 这个数据不需要保存
        dataTemp = self.calculateDatas
        ORM.writePickle(path, fileName, self)
        self.calculateDatas = dataTemp

    # 方法入口
    # datas:数据集(二维数组)
    # ignorColums: 忽略列坐标

    def fit(self, datas, ignorColums: list = None):
        # 长度为0无意义
        if len(datas) <= 0:
            raise Exception("请输入数据")

        # 转化为narrys类型
        datas = np.asanyarray(datas)
        self.datas = datas
        # 构建搜索列
        self.searchColums: list = self._buildAvailableColums(datas.shape[1], ignorColums)
        # 构建计算数据
        self.calculateDatas = self._initKDTree()
        # 添加坐标索引在尾部(-1)
        datas = np.hstack((self.calculateDatas, np.arange(datas.shape[0]).reshape(datas.shape[0], 1)))
        # 开始分割KDTree
        self._toSplitTree(self.headNode, datas)

    # 分割KDTree
    def _toSplitTree(self, node: KDNode, datas):
        # 记录数组数量
        node.len = datas.shape[0]
        # 长度为1直接处插入
        if len(datas) == 1:
            node.key = None
            # 插入索引
            node.value = datas[:, -1].astype(int)
            return

        # 选择分割坐标
        splitIndex = self._selectColumnByStd(datas)
        # 为空表示全部相等
        if splitIndex is None:
            node.key = None
            # 插入索引
            node.value = datas[:, -1].astype(int)
        else:
            leftRows, rightRows, median = self._Median(splitIndex, datas)
            # 创建节点
            leftNode, rightNode = self._creatNextNode(node, splitIndex, median)
            # 拆封坐标
            node.key = splitIndex
            # 中间值
            node.value = median
            # 分割左
            self._toSplitTree(leftNode, leftRows)
            # 分割右
            self._toSplitTree(rightNode, rightRows)

    # 构建可用搜索数组
    def _buildAvailableColums(self, columsSize, ignorColums: list) -> list:
        if ignorColums is None:
            ignorColums = []
        self.ignorColums = ignorColums
        return [i for i in range(columsSize) if i not in ignorColums]

    # 添加节点
    def _creatNextNode(self, beforNode: KDNode, key, value):
        leftNode = KDNode(beforNode, key, value, None, None)
        rightNode = KDNode(beforNode, key, value, None, None)
        beforNode.left = leftNode
        beforNode.right = rightNode
        return leftNode, rightNode

    # numpy直接选取第一位
    def _Median(self, columm, datas):
        # 获取列数据
        datasColumn = datas[:, columm]
        # 获取中位数
        median = np.median(datasColumn)
        # 拆分列
        leftRows = datas[datasColumn < median]
        # 计算是否均分数据集
        difference = datasColumn.shape[-1] // 2 - leftRows.shape[-1]
        if difference != 0:
            rightRows = datas[datasColumn > median]
            medianRowIndex = datas[datasColumn == median]
            # 合并difference+1个到leftRowIndex,
            leftRows = np.vstack((leftRows, medianRowIndex[0:difference + 1]))
            # 剩下的去rightRowIndex
            rightRows = np.vstack((rightRows, medianRowIndex[difference + 1:]))
        else:
            # 均分的话,直接拆
            rightRows = datas[datasColumn >= median]

        return leftRows, rightRows, median

    # 返回标准差最大的列
    # 若皆小于0表示数组皆相等,返回None作为标志
    def _selectColumnByStd(self, datas):
        # 最小列信息,列坐标/标准差
        maxColumn_Info = [0, 0]

        for i in self.searchColums:
            std = np.std(datas[:, i])
            # 选取最大特征列
            if std > maxColumn_Info[1]:
                maxColumn_Info[0] = i
                maxColumn_Info[1] = std
                # 忽略长度不需要逐个计算
                if len(datas) <= KDTree.IGNORESTD_LEN:
                    break
        # 返回方差最大列,若为0表示皆相等
        return maxColumn_Info[0] if maxColumn_Info[1] != 0 else None

    # searchModel搜索模式 最邻近/数量邻近/距离邻近
    # searchCount 数量筛选,数量邻近不能为空/其他可以为空
    # searchDistance 距离,距离模式不能为空,其他可以为空
    # magnification 放大倍数,若一次搜索小于数量模式 ,将结合长度进行等比放大
    # sortListType 存储引擎类型,插值,顺序,二分
    # merge 合并类型
    def Search(self, target, searchModel=MIN_TYPE, searchCount=None, magnification=0.5, searchDistance=None,
               merge=False, sortListType=SortList.INTERPOLATIONSEARCH):
        search = KDSearch(self, self.searchColums, searchModel, searchCount, magnification, searchDistance, merge)
        return search.Search(target, searchType=sortListType)
