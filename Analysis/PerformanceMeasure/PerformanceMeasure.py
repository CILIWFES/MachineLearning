import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from prettytable import PrettyTable
from typing import List


class PerformanceMeasure:
    def __init__(self):

        # 四舍五入参数
        self.rounding = "{0:.2f}"

        # +---------------+----------+
        #         | 预测正例 | 预测反例 |
        # +---------------+----------+
        # 实际正例| TP(真正例) | FN(假反例) |
        # 实际反例| FP(假正例) | TN(真反例) |
        # +---------------+----------+

        # 构建分布图时生成
        # map{key,索引}
        self.classIndex = {}
        # List[key,key]
        self.classList = {}
        # 混淆矩阵内部坐标
        self.TP = 0  # 真正例,当前正确预测
        self.FP = 1  # 假正例,当前错误预测
        self.FN = 2  # 假反例,其他错误预测
        self.TN = 3  # 真反例,其他正确预测
        self.PRECISION = 4  # 查准率
        self.RECALL = 5  # 查全率
        self.Fb = 6  # 调和平均
        # 分布图
        self.distributionMatrix = None
        # 混淆矩阵
        self.confusions = []

    def makeDistributionMatrix(self, predictions: List, realClass: List):
        allList = predictions + realClass
        counter = Counter(allList)

        self.classList = [key for key in counter.keys()]
        self.classIndex = {key: index for index, key in enumerate(self.classList)}

        classIndex = self.classIndex
        self.distributionMatrix = np.zeros((len(self.classIndex), len(self.classIndex)))
        for index, pre in enumerate(predictions):
            preIndex = classIndex[pre]
            realIndex = classIndex[realClass[index]]
            self.distributionMatrix[realIndex, preIndex] += 1

    # 构造混淆矩阵
    # B为调和平均测试B,表示查全的权重是查准的B倍(贝塔值>1对查全率影响大,B<1对准确率影响大)
    def makeconfusions(self, B=1):
        if self.distributionMatrix is None:
            raise Exception("请先构造混淆矩阵")
        for index, name in enumerate(self.classList):
            TP = self.distributionMatrix[index, index]  # 真正例,当前正确预测
            FP = np.sum(self.distributionMatrix[index]) - TP  # 假正例,当前错误预测
            FN = np.sum(self.distributionMatrix[:, index]) - TP  # 假反例,其他错误预测
            TN = np.sum(self.distributionMatrix) - TP + FP + FN  # 真反例,其他正确预测
            # 查准率
            Precision = TP / float(TP + FN) if TP + FN != 0 else 0
            # 查全率
            Recall = TP / float(TP + FP) if TP + FP != 0 else 0
            Fb = (1 + B ** 2) * Precision * Recall / float(
                B ** 2 * Precision + Recall) if B ** 2 * Precision + Recall != 0 else 0
            # 请维护顺序
            self.confusions.append((TP, FP, FN, TN, Precision, Recall, Fb))

    def fit(self, preClass, realClass, B=1):
        if len(realClass) != len(preClass):
            raise Exception("长度不一致")
        # 构造分布图
        self.makeDistributionMatrix(preClass, realClass)
        # 构造混淆矩阵
        self.makeconfusions(B)

    # 绘制查准率\查全率\调和平均Fb 表格
    def printPRFData(self):
        table = PrettyTable(["类名", "查准率", "查全率", "调和Fb", "测试数量"])

        table.align["查准率"] = "c"  # 以name字段左对齐
        table.align["查全率"] = "c"  # 以name字段左对齐
        table.align["测试数量"] = "c"  # 以name字段左对齐
        table.padding_width = 2  # 填充宽度
        p_avg = 0
        r_avg = 0
        f_avg = 0
        file_all = 0
        confusionLen = len(self.confusions)
        for index in range(confusionLen):
            item = self.confusions[index]
            table.add_row(
                [self.classList[index], self.rounding.format(item[self.PRECISION]),
                 self.rounding.format(item[self.RECALL]),
                 self.rounding.format(item[self.Fb]), item[self.TP] + item[self.FN]])
            # 计算平均值
            p_avg += item[self.PRECISION]
            r_avg += item[self.RECALL]
            f_avg += item[self.Fb]
            file_all += item[self.TP] + item[self.FN]
        table.add_row(
            ["avg", self.rounding.format(p_avg / float(confusionLen)),
             self.rounding.format(r_avg / float(confusionLen)),
             self.rounding.format(f_avg / float(confusionLen)), file_all])
        print(table)

    # 绘制PR散点图
    # x=查全,y=查准
    def showPRFigure(self):
        precisions = []
        recalls = []
        confusionLen = len(self.confusions)
        for index in range(confusionLen):  # 计算假反例oat(
            item = self.confusions[index]
            precisions.append(item[self.PRECISION])
            recalls.append(item[self.RECALL])

        # 绘图
        fig = plt.figure()
        # 把画布分成1行1列 1x1块,当前画布处于第1块
        ax = fig.add_subplot(1, 1, 1)
        # 绘制散点图x=查全,y=查准
        ax.scatter(recalls, precisions, s=10, color='red', marker='o')
        # 绘制图线
        # ax.plot(recalls, precisions, color='r')
        x = np.linspace(0, 1, 100)
        ax.plot(x, x, color='g')
        plt.show()
