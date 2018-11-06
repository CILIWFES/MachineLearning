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
        self.datas = None
        self.headNode = KDNode(None, 'Head', None, None, None)

    def fit(self, datas: List[List[float]]):
        if len(datas) <= 0:
            raise Exception("请输入数据")
        # self.dimesion =
