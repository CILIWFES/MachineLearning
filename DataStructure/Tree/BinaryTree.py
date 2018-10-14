from DataStructure.Tree.Base import *


class BinaryTree(TreeBase):
    # 在节点后面插入新节点
    def _InserNode(self, node: TreeNode, key=None, value=None):
        newNode = self._CreatNode(node.befor, key, value, node.next)
        if node.next is not None:
            node.next.befor = newNode
        node.next = newNode
        return node

    def _DeleteNode(self, node: TreeNode):
        if node.next is not None:
            node.next.befor = node.befor
        node.befor.next = node.next

    def _UpdateNode(self, node: TreeNode, key=None, value=None):
        node.key = key
        node.value = value

    def _CreatNode(self, befor: TreeNode = None, key=None, value=None, next: TreeNode = None)->TreeNode:
        return super()._CreatNode(befor, key, value, next, None)

    # 交换
    def _ExchangeNode(self, node1: TreeNode, node2: TreeNode):
        node1.befor, node1.next, node2.befor, node2.next = node2.befor, node2.next, node1.befor, node1.next
