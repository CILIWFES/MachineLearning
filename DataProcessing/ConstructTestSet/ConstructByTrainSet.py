from sklearn.datasets.base import Bunch
import random
from collections import Counter
from typing import List


class ConstructByTrainSet:
    # trainSet为二维数组
    # label为一维数组[index=1类别, index=2.类别],
    # Bunch trainSet与trainClass,testSet与testClass
    # c:交叉验证法,b:自助法,h:留出法
    def makeSet(self, trainSet, classSet, model, times=None) -> Bunch:
        if len(trainSet) != len(classSet):
            raise Exception("训练集个数与目标不一致")

        ret = None
        if model == "c":
            ret = self._crossValidation(trainSet, classSet, times)
        elif model == "b":
            ret = self._bootstrapping(trainSet, classSet)
        elif model == "h":
            ret = self._holdOutModel(trainSet, classSet, times)
        return ret

    # 交叉验证法
    def _crossValidation(self, trainSet, classSet, times) -> List[Bunch]:
        rets = []
        timesTemp = 0
        while times > timesTemp:
            testIndexs = []
            trainIndexs = []
            for k in set(classSet):
                # 获取所有时是lable属性的坐标
                trains = [indx for indx, label in enumerate(classSet) if label == k]
                # 测试集合抽取随机(cnt/times)个
                tests = random.sample(trains, int(len(trains) / times))
                testIndexs.extend(tests)
                # 生成样本集合
                trainIndexs.extend(list(set(trains).difference(set(tests))))

            rets.append(Bunch(trainSet=[trainSet[indx] for indx in trainIndexs],
                              trainClass=[classSet[indx] for indx in trainIndexs],
                              testSet=[trainSet[indx] for indx in testIndexs],
                              testClass=[classSet[indx] for indx in testIndexs]))
            timesTemp += 1
        return rets

    # 自助法
    def _bootstrapping(self, trainSet, classSet) -> Bunch:
        times = 0
        trainIndexs = []
        while (times < len(classSet)):
            randIndex = random.randint(0, len(trainSet) - 1)
            trainIndexs.append(randIndex)
            times += 1
        testIndexs = list(set(range(len(trainSet))).difference(set(trainIndexs)))

        bunch = Bunch(trainSet=[trainSet[indx] for indx in trainIndexs],
                      trainClass=[classSet[indx] for indx in trainIndexs],
                      testSet=[trainSet[indx] for indx in testIndexs],
                      testClass=[classSet[indx] for indx in testIndexs])
        return bunch

    # 留出法
    def _holdOutModel(self, trainSet, classSet, times) -> List[Bunch]:
        rets = []
        timesTemp = 0
        while times > timesTemp:
            testIndexs = []
            trainIndexs = []
            for k in set(classSet):
                # 获取所有时是lable属性的坐标
                trains = [indx for indx, label in enumerate(classSet) if label == k]

                # 测试集合抽取param*timesTemp~param*(timesTemp+1)个
                param = int(len(trains) / times)
                testIndexs.extend([trains[indx] for indx in range(timesTemp * param, timesTemp * param + param)])
                # 生成样本集合
                trainIndexs.extend(list(set(trains).difference(set(testIndexs))))
            rets.append(Bunch(trainSet=[trainSet[indx] for indx in trainIndexs],
                              trainClass=[classSet[indx] for indx in trainIndexs],
                              testSet=[trainSet[indx] for indx in testIndexs],
                              testClass=[classSet[indx] for indx in testIndexs]))
            timesTemp += 1
        return rets
