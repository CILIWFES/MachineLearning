from sklearn.datasets.base import Bunch
import random
from collections import Counter
from typing import List


class ConstructByTrainSet:
    # trainSet为二维数组
    # label为一维数组[index=1类别, index=2.类别],
    # Bunch trainSet与trainLabel,testSet与testLabel
    # c:交叉验证法,b:自助法,h:留出法
    def makeSet(self, trainSet, labels, model=None, times=None) -> Bunch:
        if len(trainSet) != len(labels):
            raise Exception("训练集个数与目标不一致")

        ret = None
        if model is "c":
            ret = self.crossValidation(trainSet, labels)
        elif model is "b":
            ret = self.bootstrapping(trainSet, labels)
        elif model is "h":
            ret = self.holdOutModel(trainSet, labels)
        return ret

    # 交叉验证法
    def crossValidation(self, trainSet, labels, times) -> List[Bunch]:
        rets = []
        timesTemp = 0
        countDict = dict(Counter(labels))
        while times > timesTemp:
            testIndexs = []
            trainIndexs = []
            for k, cnt in countDict.items():
                # 获取所有时是lable属性的坐标
                trains = [indx for indx, label in enumerate(labels) if label == k]
                # 测试集合抽取随机(cnt/times)个
                testIndexs.extend(random.sample(trains, cnt / times))
                # 生成样本集合
                trainIndexs.extend(list(set(range(len(labels))).difference(set(testIndexs))))

            rets.append(Bunch(trainSet=[trainSet[indx] for indx in trainIndexs],
                              trainLabel=[labels[indx] for indx in trainIndexs],
                              testSet=[trainSet[indx] for indx in testIndexs],
                              testLabel=[labels[indx] for indx in testIndexs]))
            timesTemp += 1
        return rets

    # 自助法
    def bootstrapping(self, trainSet, labels) -> Bunch:
        times = 0
        trainIndexs = []
        testIndexs = []
        while (times < len(labels)):
            randIndex = random.randint(0, len(labels) - 1)
            trainIndexs.append(randIndex)
            times += 1
        testIndexs = list(set(range(len(labels))).difference(set(trainIndexs)))

        bunch = Bunch(trainSet=[trainSet[indx] for indx in trainIndexs],
                      trainLabel=[labels[indx] for indx in trainIndexs],
                      testSet=[trainSet[indx] for indx in testIndexs],
                      testLabel=[labels[indx] for indx in testIndexs])
        return bunch

    # 留出法
    def holdOutModel(self, trainSet, labels, times) -> List[Bunch]:
        rets = []
        timesTemp = 0
        countDict = dict(Counter(labels))
        while times > timesTemp:
            testIndexs = []
            trainIndexs = []
            for k, cnt in countDict.items():
                # 获取所有时是lable属性的坐标
                trains = [indx for indx, label in enumerate(labels) if label == k]

                # 测试集合抽取param*timesTemp~param*(timesTemp+1)个
                param = (cnt / times)
                testIndexs.extend([trains[indx] for indx in range(timesTemp * param, timesTemp * param + param)])
                # 生成样本集合
                trainIndexs.extend(list(set(range(len(trains))).difference(set(testIndexs))))
            rets.append(Bunch(trainSet=[trainSet[indx] for indx in trainIndexs],
                              trainLabel=[labels[indx] for indx in trainIndexs],
                              testSet=[trainSet[indx] for indx in testIndexs],
                              testLabel=[labels[indx] for indx in testIndexs]))
            timesTemp += 1
        return rets
