from DataStructure.Tree import *
from typing import List
import numpy as np


# KD树,二叉树,左树为小等于,右侧为大等于
# key:特征列坐标
# value(list):为空表示其下还有分支
# leftNode: 小等于
# rightNode:大等于
class KDNode(BinaryNode):
    def __init__(self, befor, key, value, leftNode, rightNode):
        super().__init__(befor=befor, key=key, value=value, left=leftNode, right=rightNode)


#  临近距离树(可重复,二叉树)
class KDTree(BinaryTree):
    # dimension:维度
    # datas:二维数据集合
    def __init__(self):
        self.dimesion = 0
        self.headNode = KDNode(None, 'Head', None, None, None)

    def fit(self, datas: List[List[float]]):
        if len(datas) <= 0:
            raise Exception("请输入数据")
        datas = np.asarray(datas)

    # numpy直接选取第一位
    def Median(self, columm, datas):
        # 获取列数据
        datasColumn = datas[:, columm]
        # 获取中位数
        median = np.median(datasColumn)
        # 拆分列
        leftRowIndex = datas[:, datasColumn < median]
        difference = datasColumn.shape[1] // 2 - leftRowIndex.shape[1]
        if difference != 0:
            rightRowIndex = datas[:, datasColumn > median]
            medianRowIndex = datas[:, datasColumn == median]
            # 合并difference+1个到leftRowIndex,
            np.vstack((leftRowIndex, medianRowIndex[0:difference + 1]))
            # 剩下的去rightRowIndex
            np.vstack((rightRowIndex, medianRowIndex[difference + 1:]))
        else:
            rightRowIndex = datas[:, datasColumn >= median]

        return leftRowIndex, rightRowIndex

    # 通过快排的原理预估第一位
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
            if std > maxColumn_Info:
                maxColumn_Info[0] = i
                maxColumn_Info[1] = std

        return maxColumn_Info[0] if maxColumn_Info[1] != 0 else None
