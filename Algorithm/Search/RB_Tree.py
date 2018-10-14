from DataStructure.Tree import *
from typing import List


# 红黑树
class RB_Tree(BinaryTree):

    # indexFunc(返回索引值)   dataFunc(返回数据值)
    def __init__(self, indexFunc=lambda x: x, dataFunc=lambda x: x):
        super().__init__()
        self.indexFunc = indexFunc
        self.dataFunc = dataFunc

    def BuildTree(self, datas: List,isSord=False):
        # if isSord:
            
        # 构建头节点
        self.headNode = self._CreatNode(None, self.indexFunction(datas[0]), self.dataFunc(datas[0]), None)

        # 从第二个开始构建
        if len(datas) > 1:
            for data in datas[1:]:
                self._Put(self.indexFunction(data), self.dataFunc(data))

    # 添加元素
    def Put(self, data=None, key=None, value=None):
        if key is None or value is None:
            key, value = self.indexFunction(data), self.dataFunc(data)
        return self._Put(key, value)

    def _Put(self, key, value):
        node: TreeNode = self._FindScope(key)
        if node.key == key:
            node.value.append(value)
        else:
            node = self.RBCore()
        return node

    # 红黑树算法核心
    def RBCore(self)->TreeNode:
        pass

    def Delete(self, key):
        pass

    def Find(self, key):
        pass

    def Update(self, key, data):
        pass

    # 寻找最近范围的节点(找到key就返回,找不到就返回上一个节点)
    def _FindScope(self, key)->TreeNode:
        pass

    def _CreatNode(self, befor: TreeNode = None, key=None, value: List = None, next: TreeNode = None)->TreeNode:
        return super()._CreatNode(befor, key, [value], next)
