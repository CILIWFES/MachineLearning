from prettytable import PrettyTable
import time
import numpy as np


class TimeMeasure:
    # testFunction必须是一个闭包(闭包是为了数据)
    def __init__(self, testFunction):
        # 四舍五入参数
        self.rounding = "{0:.2f}%"
        # 阈值,次数超过__threshold个(小等于0表示不去除),去除__deleteCnt个最大值(误差较大值)
        self.__threshold = 0
        self.__deleteCnt = 0
        self.timeList = []
        self.times = 0
        self.testFunction = testFunction

    # 开始性能测试,times测试次数
    def StartTimeMeasure(self, times):
        self.times = times
        # 清空历史数据
        self.timeList.clear()
        print("""
时间测试开始
-------------------------------------------------------------------------------------\n""")
        while times > 0:
            lastTimes = time.clock()
            self.testFunction()
            durTime = time.clock()
            times -= 1
            self.timeList.append(durTime - lastTimes)

        print("""
-------------------------------------------------------------------------------------
时间测试结束""")
        # 结果预处理
        if 0 < self.__threshold <= len(self.timeList):
            deleteCnt = self.__deleteCnt
            while deleteCnt > 0:
                self.timeList.remove(max(self.timeList))
                deleteCnt -= 1
                self.times -= 1
        # 信息展示
        self.ShowResult()

    def ShowResult(self):
        if len(self.timeList) == 0:
            raise Exception("未调用时间测试")

        table = PrettyTable(["调用次数", "时间平均", "极小值", "极大值", "时间相对差"])

        table.align["统计次数"] = "c"  # 以name字段左对齐
        table.align["极大值"] = "c"  # 以name字段左对齐
        table.align["极小值"] = "c"  # 以name字段左对齐
        table.align["时间平均"] = "c"  # 以name字段左对齐
        table.align["时间标准差"] = "c"  # 以name字段左对齐
        table.padding_width = 2  # 填充宽度

        timMatrix = np.mat(self.timeList)
        avg = np.sum(timMatrix) / float(self.times)
        table.add_row(
            [self.times, avg, np.amin(timMatrix), np.amax(timMatrix),
             self.rounding.format((np.std(timMatrix, ddof=0) / avg) * 100)])
        print(table)
