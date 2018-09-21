import numpy as np
import matplotlib.pyplot as plt
from prettytable import PrettyTable


class JudegeClass:
    def __init__(self):
        # +---------------+----------+
        #         | 预测正例 | 预测反例 |
        # +---------------+----------+
        # 实际正例| TP(真正例) | FN(假反例) |
        # 实际反例| FP(假正例) | TN(真反例) |
        # +---------------+----------+
        # 这些是坐标
        self.TP = 0  # 真正例,当前正确预测
        self.FP = 1  # 假正例,当前错误预测
        self.TN = 2  # 真反例,其他错误预测
        self.FN = 3  # 假反例,其他正确预测
        self.PRECISION = 4  # 查准率
        self.RECALL = 5  # 查全率
        self.Fb = 6  # 调和平均
        self.dataDict = {}
    # B为调和平均测试B,表示查全的权重是查准的B倍(贝塔值>1对查全率影响大,B<1对准确率影响大)
    def Judege(self, predictions, realClass, B=1):
        if len(predictions) is not len(realClass):
            raise Exception("预测值与实际值长度不一")
        dic = {}
        for index in range(len(predictions)):
            realName = realClass[index]

            preName = predictions[index]

            if realName not in dic:
                dic[realName] = [0, 0, 0, 0, 0, 0, 0]
            if preName not in dic:
                dic[preName] = [0, 0, 0, 0, 0, 0, 0]

            if realName == preName:
                dic[preName][self.TP] += 1  # 正确,真正例+1
            elif realName != preName:
                dic[preName][self.FP] += 1  # 其他错误,假正例
                dic[realName][self.FN] += 1  # 错误,假反例+1

        allCnt = len(predictions)
        precisions = []
        recalls = []

        for k, lst in dic.items():  # 计算假反例
            lst[self.TN] = allCnt - sum(lst)  # 假反例,其他正确预测
            lst[self.PRECISION] = 0 if lst[self.TP] + lst[self.FP] == 0 else lst[self.TP] / (
            float(lst[self.TP] + lst[self.FP]))
            lst[self.RECALL] = 0 if lst[self.TP] + lst[self.FN] == 0 else lst[self.TP] / (
            float(lst[self.TP] + lst[self.FN]))  # 假反例,其他正确预测
            lst[self.Fb] = 0 if lst[self.PRECISION] + lst[self.RECALL] == 0 else (1 + B ** 2) * lst[self.PRECISION] * \
                                                                                 lst[self.RECALL] / float(
                B ** 2 * lst[self.PRECISION] + lst[self.RECALL])  # 假反例,其他正确预测
            precisions.append(lst[self.PRECISION])
            recalls.append(lst[self.RECALL])
        self.dataDict = dic

    def printData(self):
        table = PrettyTable(["类名", "查准率", "查全率", "调和平均Fb", "测试数量"])

        table.align["查准率"] = "c"  # 以name字段左对齐
        table.align["查全率"] = "c"  # 以name字段左对齐
        table.align["测试数量"] = "c"  # 以name字段左对齐
        table.padding_width = 2  # 填充宽度
        p_avg = 0
        r_avg = 0
        f_avg = 0
        file_all = 0
        for k, lst in self.dataDict.items():  # 计算假反例
            table.add_row([k, "{0:.2f}".format(lst[self.PRECISION]), "{0:.2f}".format(lst[self.RECALL]),
                           "{0:.2f}".format(lst[self.Fb]), lst[self.TP] + lst[self.FN]])
            p_avg += lst[self.PRECISION]
            r_avg += lst[self.RECALL]
            f_avg += lst[self.Fb]
            file_all += lst[self.TP] + lst[self.FN]
        dataLen = len(self.dataDict)
        table.add_row(
            ["avg", "{0:.3f}".format(p_avg / float(dataLen)), "{0:.3f}".format(r_avg / float(dataLen)),
             "{0:.3f}".format(f_avg / float(dataLen)), file_all])
        print(table)

    # 绘制散点图
    def showFigure(self):
        precisions = []
        recalls = []
        for k, lst in self.dataDict.items():  # 计算假反例oat(
            precisions.append(lst[self.PRECISION])
            recalls.append(lst[self.RECALL])

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
