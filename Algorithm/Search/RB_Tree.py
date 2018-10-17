from DataStructure.Tree import *
from typing import List


class RB_TreeNode(BinaryNode):
    RED = 0
    BLACK = 1

    def __init__(self, befor=None, key=None, value: List = None, left=None, right=None):
        if type(value) is not list:
            value = [value]
        super().__init__(befor, key, value, left, right)
        self.color = RB_TreeNode.RED


# 红黑树
class RB_Tree(BinaryTree):

    # indexFunc(返回索引值)   dataFunc(返回数据值)
    # 例如hash表
    # key                   (key,obj)
    def __init__(self, indexFunc=lambda x: x, dataFunc=lambda x: x):
        super().__init__()
        self.indexFunc = indexFunc
        self.dataFunc = dataFunc

    def BuildTree(self, reaKeys, datas: List):
        if len(datas) != len(reaKeys):
            raise Exception("长度不一")

        # 构建头节点
        # 类比hashMap
        dataTuples = [(reaKeys[i], self.dataFunc(datas[i])) for i in range(len(datas))]

        self.headNode = self._CreatNode(None)  # 头指针没有值
        # right 只是方便
        self.headNode.right = self._CreatNode(self.headNode, self.indexFunc(dataTuples[0][0]), dataTuples[0])
        self.headNode.right.color = RB_TreeNode.BLACK
        # 构建树
        for data in dataTuples[1:]:
            self._Put(data[0], data)

    def makeDic(self, node):
        dic = None
        if node.left is not None:
            dicL = self.makeDic(node.left)
            colorL = "RL" if node.left.color == RB_TreeNode.RED else "BL"
            if dic is None:
                dic = {colorL: dicL}
            else:
                dic[colorL] = dicL

        if node.right is not None:
            dicR = self.makeDic(node.right)
            colorR = "RR" if node.right.color == RB_TreeNode.RED else "BR"
            if dic is None:
                dic = {colorR: dicR}
            else:
                dic[colorR] = dicR
        return {node.key: dic}

    # 添加元素
    def Put(self, realKey, value):
        key, value = self.indexFunc(realKey), (realKey, self.dataFunc(value))
        self._Put(key, value)

    def _Put(self, key, value):
        node: RB_TreeNode = self._FindScopeNode(key)
        if node.key == key:
            node.value.append(value)
        else:
            node = self._InsertNode(node, key, value)
        return node

    # 红黑树算法核心
    # beforNode必须保证要插入的节点是根节点
    def _InsertNode(self, beforNode: RB_TreeNode, key, value) -> RB_TreeNode:
        newNode = self._CreatNode(beforNode, key, value)

        if beforNode.key > newNode.key:
            beforNode.left = newNode
        else:
            beforNode.right = newNode
        newNode.befor = beforNode

        if beforNode.color != RB_TreeNode.BLACK:
            self.RBCore(newNode)

        return newNode

    # 检查调度
    def RBCore(self, childNode: RB_TreeNode):
        befor: RB_TreeNode = childNode.befor
        beBefor: RB_TreeNode = befor.befor
        beforBroNode = befor.getSiblings()

        # 同向
        # 关系 子变父 ,父变子
        if befor == beBefor.left and childNode != befor.left:
            childNode, befor = self.Syntropy(childNode, befor, True)  # 左旋转
        elif befor == beBefor.right and childNode != befor.right:
            childNode, befor = self.Syntropy(childNode, befor, False)  # 右旋转

        elif beforBroNode is None or beforBroNode.color == RB_TreeNode.BLACK:  # 准备向黑色一方旋转
            self.RotateBLACK(befor, beBefor)
        elif beforBroNode.color == RB_TreeNode.RED:
            beBefor = self.Discoloration(befor, beBefor, beforBroNode)
            if beBefor.befor.color != RB_TreeNode.BLACK and beBefor != self.headNode.right:
                self.RBCore(beBefor)  # 递归修改
            elif beBefor == self.headNode.right:
                beBefor.color = RB_TreeNode.BLACK

    # 同向
    def Syntropy(self, childNode: RB_TreeNode, befor: RB_TreeNode, rotateLeft: bool):
        return self.Rotate(childNode, befor, rotateLeft)

    # 变色
    def Discoloration(self, befor: RB_TreeNode, beBefor: RB_TreeNode, beforBroNode: RB_TreeNode):
        befor.color = RB_TreeNode.BLACK
        beforBroNode.color = RB_TreeNode.BLACK
        beBefor.color = RB_TreeNode.RED
        return beBefor  # 再递归修改

    # 向黑旋转
    def RotateBLACK(self, befor: RB_TreeNode, beBefor: RB_TreeNode):
        rotateLeft = False if befor == beBefor.left else True
        beBefor, befor = self.Rotate(befor, beBefor, rotateLeft)
        beBefor.color = RB_TreeNode.BLACK
        befor.color = RB_TreeNode.RED

    # 旋转
    def Rotate(self, node: RB_TreeNode, befor: RB_TreeNode, isLeft: bool):

        graBefor = befor.befor
        if graBefor.right == befor:
            graBefor.right = node
        else:
            graBefor.left = node

        # 最上节点下移
        befor.befor = node
        # 父节点变为爷节点
        node.befor = graBefor
        if isLeft:  # 左旋转
            if node.left is not None:
                # 子树交换
                node.left.befor = befor
            befor.right = node.left
            # 原父节点 指向 爷节点
            node.left = befor
        else:  # 右旋转
            if node.right is not None:
                # 子树交换
                node.right.befor = befor
            befor.left = node.right
            # 原父节点 指向 爷节点
            node.right = befor
        return node, befor

    def Delete(self, key):
        pass

    def Find(self, realKey):
        key = self.indexFunc(realKey)
        findNode = self._FindScopeNode(key)
        if findNode == None:
            return None

        if findNode.key == key:
            for item in findNode.value:
                if item[0] == realKey:
                    return item[1]
        return None

    def Update(self, realKey, value):
        key = self.indexFunc(realKey)
        findNode = self._FindScopeNode(key)
        if findNode is None:
            return False  # 表示不存在

        if findNode.key == key:
            for item in findNode.value:
                if item[0] == realKey:
                    item[1] = value
                    return True  # 修改成功
        return False

    # 寻找最近范围的节点(找到key就返回,找不到就返回上一个节点)
    def _FindScopeNode(self, key) -> RB_TreeNode:
        if self.headNode.right.key == key:
            return self.headNode.right

        findingNode: RB_TreeNode = self.headNode.right
        befor: RB_TreeNode = findingNode
        while findingNode is not None:

            if key < findingNode.key:
                befor = findingNode
                findingNode = findingNode.left

            elif key > findingNode.key:
                befor = findingNode
                findingNode = findingNode.right

            elif key == findingNode.key:
                return findingNode

        # 没找到
        return befor

    def _CreatNode(self, befor: RB_TreeNode = None, key=None, value=None, left=None, right=None) -> RB_TreeNode:
        return RB_TreeNode(befor, key, value, left, right)
