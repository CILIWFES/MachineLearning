# _*_ coding: UTF-8 _*_

import matplotlib.pyplot as plt


# tree ={nodeName:{selectName:{nextNode....},selectName:{nextNode....},selectName:{nextNode....}}}
# 标准情况{ key:{select{ {key:{s}} }, select:{   {key:{s}}   }} }
# 完结阶段{ key:None }
class TreePlotter:
    def __init__(self):
        self.ax1 = None
        # x方向缩放系数
        self.totalW = None
        # y方向缩放系数
        self.totalD = None
        # x方向整体偏移
        self.x0ff = None
        """绘决策树的函数"""
        self.decisionNode = dict(boxstyle="sawtooth", fc="0.8")  # 定义分支点的样式
        self.leafNode = dict(boxstyle="round4", fc="0.8")  # 定义叶节点的样式
        self.arrow_args = dict(arrowstyle="<-")  # 定义箭头标识样式

    # 计算树的叶子节点数量
    # 标准情况{ key:{select{}, select:{}} }
    # 完结阶段{ key:None }
    def _getNumLeafs(self, myTree):
        numLeafs = 0
        nodeName = list(myTree.keys())[0]

        item = myTree[nodeName]
        # 完结
        if item is None:
            return 1
        for select in item.keys():
            numLeafs += self._getNumLeafs(item[select])

        return numLeafs

    # 计算树的最大深度
    # 标准情况{ key:{select{}, select:{}} }
    # 完结2阶段{ key:None }
    def _getTreeDepth(self, myTree):
        maxDepth = 0
        nodeKey = list(myTree.keys())[0]

        selectDict = myTree[nodeKey]
        if selectDict is None:
            return 1
        for select in selectDict.keys():
            thisDepth = 1 + self._getTreeDepth(selectDict[select])
            if thisDepth > maxDepth:
                maxDepth = thisDepth
        return maxDepth

    # 画出节点
    # 父节点坐标(箭头起始):parentPt
    # 字体(框体)坐标:centerPt
    # 分支点样式:bbox
    # 箭头样式:arrowprops
    def _plotNode(self, nodeTxt, centerPt, parentPt, nodeType):
        self.ax1.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction', xytext=centerPt,
                          textcoords='axes fraction', va="center", ha="center",
                          bbox=nodeType, arrowprops=self.arrow_args)

    # 标箭头上的文字
    def _plotMidText(self, cntrPt, parentPt, txtString):
        lens = len(txtString)
        xMid = (parentPt[0] + cntrPt[0]) / 2.0 - lens * 0.002
        yMid = (parentPt[1] + cntrPt[1]) / 2.0
        self.ax1.text(xMid, yMid, txtString)

    # 绘图主方法
    def _plotTree(self, myTree, parentPt, nodeTxt):
        # 标准情况{ key:{select{}, select:{}} }
        # 完结阶段{ key:None }
        numLeafs = self._getNumLeafs(myTree)
        # 节点node字体|框体 坐标
        # 加1是为了与self.x0ff初始-1间隔相互抵消
        # /2.0是为了间隔
        # / self.totalW是为了一个页面放得下的比例缩短
        cntrPt = (self.x0ff + (1 + numLeafs) / 2.0 / self.totalW, parentPt[1] - 1.0 / self.totalD)
        nodeName = list(myTree.keys())[0]

        # 完结1阶段{ key:{select:str,select:str} }(str)
        # 完结2阶段{ key:None }(None)
        if myTree[nodeName] is None:
            self.x0ff = self.x0ff + 1.0 / self.totalW

            # 绘制节点与箭头
            self._plotNode(nodeName, (self.x0ff, parentPt[1] - 1.0 / self.totalD), parentPt,
                           self.leafNode)
            # 绘制文字
            self._plotMidText((self.x0ff, parentPt[1] - 1.0 / self.totalD), parentPt,
                              str(nodeTxt))
        else:
            self._plotMidText(cntrPt, parentPt, nodeTxt)
            # 节点名称
            self._plotNode(nodeName, cntrPt, parentPt, self.decisionNode)  # 绘制当前节点

            selectDict = myTree[nodeName]

            for select in selectDict.keys():
                self._plotTree(selectDict[select], cntrPt, str(select))

    def createPlot(self, inTree):
        fig = plt.figure(1, facecolor='white')
        fig.clf()
        axprops = dict(xticks=[], yticks=[])
        self.ax1 = plt.subplot(111, frameon=False, **axprops)
        self.totalW = float(self._getNumLeafs(inTree))
        self.totalD = float(self._getTreeDepth(inTree))
        # 消去初始间隔
        self.x0ff = -1 / 2.0 / self.totalW
        self.y0ff = 1.0
        self._plotTree(inTree, (0.5, 1.0), "")
        plt.show()
