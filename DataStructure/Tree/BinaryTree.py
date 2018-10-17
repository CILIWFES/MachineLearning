from DataStructure.Tree.Base import *


class BinaryNode(TreeNode):
    def __init__(self, befor=None, key=None, value=None, left=None, right=None, siblings=None):
        super().__init__(befor, key, value, None, siblings)
        del self.next
        self.left = left
        self.right = right

    def getNext(self, isLeft):
        if isLeft:
            return self.left
        else:
            return self.right

    def getSiblings(self):
        if self.befor == None:
            return None
        else:
            befor = self.befor
            return befor.right if befor.left == self else befor.left


class BinaryTree(TreeBase):
    # 在节点 左/右 插入新节点插入节点与子节点的位置(子节点插入addLeft中)
    def _InsertNode(self, node: BinaryNode, isLeft, addLeft, key=None, value=None):
        newNode: BinaryNode

        if addLeft is True:
            newNode = self._CreatNode(node, key, value, node.left)
        else:
            newNode = self._CreatNode(node, key, value, node.right)

        # 调整子节点
        if isLeft:
            if node.left is not None:
                node.left.befor = newNode
            node.left = newNode
        else:
            if node.right is not None:
                node.right.befor = newNode
            node.right = newNode

        return newNode

    # 不清楚应用场景(具体类型具体实现)
    def _DeleteNode(self, node: TreeNode):
        pass

    def _UpdateNode(self, node: TreeNode, key=None, value=None):
        if key is not None:
            node.key = key

        if value is not None:
            node.value = value

    def _CreatNode(self, befor: BinaryNode = None, key=None, value=None, left=None, right=None) -> TreeNode:
        return BinaryNode(befor, key, value, left, right)

    # 交换节点(交换本身与子节点,不能交换空节点,切头)
    def _ExchangeNode(self, node1: BinaryNode, node2: BinaryNode):
        node1.befor, node2.befor = node2.befor, node1.befor
