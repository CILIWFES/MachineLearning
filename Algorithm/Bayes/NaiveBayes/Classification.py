import numpy as np
from typing import List, Dict
from DataProcessing.ORM import *
import sys
from collections import Counter


# 朴素贝叶斯(事件集模型,离散型)
class Classification:

    def savePickle(self, path, fileName):
        ORM.writePickle(path, fileName, self)

    @staticmethod
    def loadPickle(path):
        return ORM.loadPickle(path)

    def __init__(self):
        # 类别事件集模型,{name:矩阵},每个分类都有自己的事件集
        self.calculateModel = {}
        # 事件名key->事件集模型中的index值
        self.eventsIndex = {}
        # class
        # 类别概率
        self.classP = {}
        self.classList = []
        self.classIndex = {}

    # trainSet训练集(list)
    def fit(self, trainSet: List, classSet):
        # 对类型进行归类,并计算概率
        self.classList, self.classIndex, self.classP = self._BuildCategoryIndex(classSet)
        # 建立事件集索引
        self.eventsIndex = self._BuildEventIndex(trainSet)
        # 构建事件集类别-文件事件集dict
        classEvents = self._BuildClassEvent(trainSet, classSet)
        # 计算文件预测事件集
        self.calculateModel = self._BuildCalCulteEvent(classEvents)

    # 建立类别索引
    def _BuildCategoryIndex(self, classSet):
        classList = list(set(classSet))
        classIndex = {key: index for index, key in enumerate(classList)}
        # P(A)概率,拉普拉斯修正
        classP = {key: (v + 1) / (len(classSet) + len(classIndex)) for key, v in dict(Counter(classSet)).items()}
        return classList, classIndex, classP

    # 建立事件集索引
    def _BuildEventIndex(self, trainSet):
        setTemp = set()
        avgFile = 0
        for item in trainSet:
            avgFile += len(item)
            itemSet = set(item)
            setTemp.update(itemSet)
        EventIndex = {name: index for index, name in enumerate(setTemp)}
        return EventIndex

    # 构建类别-事件集模型
    def _BuildClassEvent(self, trainSet, classSet):
        classEvents = {}
        for index, item in enumerate(classSet):
            EventTemp = trainSet[index]
            Event = self._MakeEvent(EventTemp)
            if item in classEvents:
                classEvents[item].append(Event)
            else:
                classEvents[item] = [Event]
        return classEvents

    # 对单一事件生成事件集
    def _MakeEvent(self, events: List):
        # 新建初始长度为事件表的矩阵
        lst = np.zeros((1, len(self.eventsIndex)))
        for event in events:
            if event in self.eventsIndex:
                lst[0, self.eventsIndex[event]] = 1
        return lst[0]

    # 计算核心
    def _BuildCalCulteEvent(self, classEvents: Dict):
        setEvents = {}
        for key, item in classEvents.items():
            setEventsTemp = np.zeros((1, len(self.eventsIndex)))
            for Events in item:
                setEventsTemp += Events
            # 无拉普拉斯修正
            # setEventsTemp = setEventsTemp / (len(item))  # 除以文件数
            # setEventsTemp += 0.000000000000001  # 去0
            # 优化后的拉普拉斯修正(0.0000000000001)越小精度越高
            setEventsTemp = (setEventsTemp / len(item))
            setEvents[key] = setEventsTemp
        return setEvents
        # 预测

    def Prediction(self, testSet):
        preClass = []
        for item in testSet:
            Events = self._MakeEvent(item)
            preClass.append(self._toPrediction(Events))
        return preClass

    # 预测单个,不能调用
    def _toPrediction(self, Events):
        minInfo = ["", -sys.maxsize]
        for key, setEvents in self.calculateModel.items():
            weight = self.classP[key] * np.sum(
                np.log(np.abs(setEvents + Events - 1.0).clip(min=1 / sys.maxsize)))  # P(A/B)正比于P(A)*P(B/A)
            # 不乘P(A)效果更好,乘P(A)可能是考虑样本不均匀且大样本覆盖面比较广,只有样本显著差异时才可以预测为小样本
            # weight = np.sum(np.log(np.abs(setEvents + Events - 1)))
            if weight > minInfo[1]:
                minInfo = (key, weight)
        return minInfo[0]
