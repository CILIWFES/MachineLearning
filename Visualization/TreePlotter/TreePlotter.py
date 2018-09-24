# _*_ coding: UTF-8 _*_

import matplotlib.pyplot as plt


class TreePlotter:
    def __init__(self):
        self.ax1 = None
        self.totalW = None
        self.totalD = None
        self.x0ff = None
        self.y0ff = None
        """绘决策树的函数"""
        self.decisionNode = dict(boxstyle="sawtooth", fc="0.8")  # 定义分支点的样式
        self.leafNode = dict(boxstyle="round4", fc="0.8")  # 定义叶节点的样式
        self.arrow_args = dict(arrowstyle="<-")  # 定义箭头标识样式

    # 计算树的叶子节点数量
    def getNumLeafs(self, myTree):
        numLeafs = 0
        for key in myTree.keys():
            if type(myTree[key]) == dict:
                numLeafs += self.getNumLeafs(myTree[key])
            else:
                numLeafs += 1
        return numLeafs

    # 计算树的最大深度
    def getTreeDepth(self, myTree):
        maxDepth = 0
        for key in myTree.keys():
            if type(myTree[key]) == dict:
                thisDepth = 1 + self.getTreeDepth(myTree[key])
            else:
                thisDepth = 1
            if thisDepth > maxDepth:
                maxDepth = thisDepth
        return maxDepth

    # 画出节点
    def plotNode(self, nodeTxt, centerPt, parentPt, nodeType):
        self.ax1.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction', xytext=centerPt,
                          textcoords='axes fraction', va="center", ha="center",
                          bbox=nodeType, arrowprops=self.arrow_args)

    # 标箭头上的文字
    def plotMidText(self, cntrPt, parentPt, txtString):
        lens = len(txtString)
        xMid = (parentPt[0] + cntrPt[0]) / 2.0 - lens * 0.002
        yMid = (parentPt[1] + cntrPt[1]) / 2.0
        self.ax1.text(xMid, yMid, txtString)

    def plotTree(self, myTree, parentPt, nodeTxt):
        numLeafs = self.getNumLeafs(myTree)
        firstStr = list(myTree.keys())[0]
        cntrPt = (self.x0ff + (1.0 + float(numLeafs)) / 2.0 / self.totalW, self.y0ff)
        self.plotMidText(cntrPt, parentPt, nodeTxt)
        self.plotNode(firstStr, cntrPt, parentPt, self.decisionNode)
        secondDict = myTree
        self.y0ff = self.y0ff - 1.0 / self.totalD
        for key in secondDict.keys():
            if type(secondDict[key]) == dict:
                self.plotTree(secondDict[key], cntrPt, str(key))
            else:
                self.x0ff = self.x0ff + 1.0 / self.totalW
                self.plotNode(secondDict[key], (self.x0ff, self.y0ff), cntrPt, self.leafNode)
                self.plotMidText((self.x0ff, self.y0ff), cntrPt, str(key))
        self.y0ff = self.y0ff + 1.0 / self.totalD

    def createPlot(self, inTree):
        fig = plt.figure(1, facecolor='white')
        fig.clf()
        axprops = dict(xticks=[], yticks=[])
        self.ax1 = plt.subplot(111, frameon=False, **axprops)
        self.totalW = float(self.getNumLeafs(inTree))
        self.totalD = float(self.getTreeDepth(inTree))
        self.x0ff = -0.5 / self.totalW
        self.y0ff = 1.0
        self.plotTree(inTree, (0.5, 1.0), '')
        plt.show()

