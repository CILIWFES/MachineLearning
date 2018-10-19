from DataStructure.Tree import *
from typing import List
import functools


#  临近距离树(可重复)
class KDTree(BinaryTree):
    # keyFunc 获取n维度key值的闭包方法
    # dataFunc 获取data值的方法
    def __init__(self, keyFunc, dataFunc, dimension):
        super().__init__()
        if dimension <= 0:
            raise Exception("len必须大于0")

        self.keyFunc = keyFunc
        self.keyFuncDict = {}
        self.dataFunc = dataFunc
        self.dimension = dimension
        self.headNode = BinaryNode()
        self.datas = None

    def KeyFuncDict(self, dimension):
        if dimension in self.keyFuncDict:
            return self.keyFuncDict[dimension]
        else:
            keyFunc = self.keyFunc(dimension)
            self.keyFuncDict[dimension] = keyFunc
            return keyFunc

    # datas 是数据集合
    # 假定是[(0,2) ,(2,5) 这样]
    # len表示有几个维度
    def BuildTree(self, datas: List):
        if len(datas) <= 1:
            raise Exception("输出数据必须大于两位!")
        # 通过第一维度,获取中位数
        key, leftDatas, rightDatas = self.GetMedian(datas, 0)


        # 先选定头节点
        self.headNode.key = key
        # 获取左节点
        node = self._MedianSeparation(leftDatas, 0 if self.dimension == 1 else 1)
        self.headNode.left = node
        self.headNode.left.befor = self.headNode

        # 获取右节点
        node = self._MedianSeparation(rightDatas, 0 if self.dimension == 1 else 1)
        self.headNode.right = node
        node.befor = self.headNode

    def GetMedian(self, datas: List, dimension):
        # 获取n维度的闭包方法
        keyFunc = self.KeyFuncDict(dimension)

        datas = sorted(datas, key=functools.cmp_to_key(keyFunc))

        size = len(datas)
        # 右多左少
        lefts = datas[0:size // 2]
        rights = datas[size // 2]
        # 关键字
        key = (keyFunc(datas[size]) + keyFunc(datas[~size])) // 2

        return key, lefts, rights

    # 中位分割
    # datas需要分割的数据
    # 分割坐标
    def _MedianSeparation(self, datas, len) -> BinaryNode:
        newNode = BinaryNode()
        key, leftDatas, rightDatas = self.GetMedian(datas, len)


        # 先选定头节点
        newNode.key = key

        # 获取左节点,维度不够就循环
        node = self._MedianSeparation(leftDatas, 0 if self.len <= len + 1 else len + 1)
        newNode.left = node
        newNode.left.befor = newNode

        # 获取右节点,维度不够就循环
        node = self._MedianSeparation(rightDatas, 0 if self.len <= len + 1 else len + 1)
        newNode.right = node
        node.befor = newNode

        return newNode

    def toDict(self, node):
        dic = None
        if node.left is not None:
            dicL = self.toDict(node.left)
            if dic is None:
                dic = {"L": dicL}
            else:
                dic["L"] = dicL

        if node.right is not None:
            dicR = self.toDict(node.right)
            if dic is None:
                dic = {"L": dicR}
            else:
                dic["L"] = dicR
        return {node.key: dic}

    def Find(self, index):
        pass

    def Update(self, index, data):
        pass

    def _InserNode(self, node: TreeNode, data):
        pass
