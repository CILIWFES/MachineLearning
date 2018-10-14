from typing import List


class TreeNode:
    def __init__(self, befor=None, key=None, value=None, next=None, siblings=None, depthIndex=None):
        self.value = value
        self.key = key
        self.next: TreeNode = next
        self.befor: TreeNode = befor
        self.siblings: List[TreeNode] = siblings
        self.__depthIndex = depthIndex

    def getDepThIndex(self):
        if self.befor is None:
            return 0
        else:
            return self.befor.getDepThIndex()+1

    def goNext(self):
        return self.next

    def returnBefor(self):
        return self.befor

    def toSiblings(self, index=None):
        if index is None:
            return self.siblings
        else:
            return self.siblings[0]


class TreeBase:
    def __init__(self):
        self.headNode = None
        self.depth = 0

    def BuildTree(self, datas):
        pass

    def Put(self, data, index=None):
        pass

    def Delete(self, index):
        pass

    def Find(self, index):
        pass

    def Update(self, index, data):
        pass

    # 在节点后面插入新节点
    def _InserNode(self, node: TreeNode, data):
        pass

    def _DeleteNode(self, node: TreeNode):
        pass

    def _UpdateNode(self, node: TreeNode, data):
        pass

    # 新增节点
    def _CreatNode(self, befor: TreeNode = None, key=None, value=None, next: TreeNode = None, siblings=None)->TreeNode:
        node: TreeNode = TreeNode(befor=befor, key=key, value=value, next=next, siblings=siblings)
        return node

    # 交换节点
    def _ExchangeNode(self, node1, node2):
        pass
