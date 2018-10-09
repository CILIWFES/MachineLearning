import numpy as np
from typing import List, Dict
from DataProcessing.ORM import *

import sys


class TFIDF:

    def savePickle(self, path, fileName):
        ORM.writePickle(path, fileName, self)

    @staticmethod
    def loadPickle(path):
        return ORM.loadPickle(path)

    def __init__(self):
        # 词袋模型,{name:矩阵},每个分类都有自己的词袋
        self.TfIdf = {}
        # 词名key->词袋模型中的index值
        self.wordIndex = {}
        # 类别概率
        self.classList = []
        self.classIndex = {}

    # trainSet训练集(list)
    def fit(self, trainSet: List, classSet):
        # 对类型进行归类,并计算概率
        self.classList, self.classIndex = self.categoryIndex(classSet)
        # 建立词袋索引
        self.wordIndex = self.buildWordIndex(trainSet)
        # 构建词袋类别-文件词袋dict
        classWords = self.buildClassWord(trainSet, classSet)
        # 计算文件预测词袋
        self.TfIdf = self.buildTfIdfWord(classWords)

    # 构建词袋name->index坐标索引
    def buildWordIndex(self, trainSet):
        setTemp = set()
        avgFile = 0
        for item in trainSet:
            avgFile += len(item)
            itemSet = set(item)
            setTemp.update(itemSet)
        wordIndex = {name: index for index, name in enumerate(setTemp)}
        return wordIndex

    # 建立类别索引
    def categoryIndex(self, classSet):
        classList = list(set(classSet))
        classIndex = {key: index for index, key in enumerate(classList)}
        # P(A)概率,拉普拉斯修正
        return classList, classIndex

    # 创建字典表
    def _buildWordDict(self, words: List):
        # 新建初始长度为词典表的矩阵
        lst = np.zeros((1, len(self.wordIndex)))
        for word in words:
            if word in self.wordIndex:
                lst[0, self.wordIndex[word]] += 1
        return lst[0]

    # 构建词袋模型
    def buildClassWord(self, trainSet, classSet):
        classWords = {}
        for index, item in enumerate(classSet):
            wordTemp = trainSet[index]
            word = self._buildWordDict(wordTemp)
            if item in classWords:
                classWords[item].append(word)
            else:
                classWords[item] = [word]
        return classWords

    def TF(self, classWords):
        TFClass = {}
        for key, item in classWords.items():
            words = np.sum(np.mat(item), axis=0)
            words = (words + 1 / np.sum(words)) / np.sum(words)
            TFClass[key] = words
        return TFClass

    def IDF(self, classWords):
        setWords = {}
        IDFClass = {}
        # 总文件频率
        AllSetWords = np.zeros((1, len(self.wordIndex)))
        # 总分类频率
        ClassSetWords = np.zeros((1, len(self.wordIndex)))
        fileCnt = 0
        for key, item in classWords.items():
            words = np.sum(np.mat(item).clip(max=1), axis=0)
            fileCnt += len(item)
            # 转化为词集模型
            AllSetWords = words + AllSetWords
            words = [0 if i <= 0 else 1 for i in words.tolist()[0]]
            ClassSetWords = words + ClassSetWords
        """
            # 改良后的Idf，针对类别建立(效果不好)
        #     setWords[key] = words
        # 
        # for key, item in setWords.items():
        #     # 当前分类文件分类出现次数的占比
        #     idf = np.log(AllSetWords/(AllSetWords+1/np.sum(item)-item))
        #     IDFClass[key] = idf
        # return IDFClass
        """
        # 书本上是写这个逆文件频率(文件越多越接近0)
        # return np.log(fileCnt / AllSetWords)
        # 我做的逆类别频率类别越多越接近0
        # return np.log(len(self.classList) / ClassSetWords)

        # 综合1
        # return np.log(np.multiply((fileCnt / AllSetWords), (len(self.classList) / ClassSetWords)))
        # 综合2
        return np.multiply(np.log((fileCnt / AllSetWords)), np.log((len(self.classList) / ClassSetWords)))

    # 计算核心
    def buildTfIdfWord(self, classWords: Dict):
        print("正在构建TFIDF")
        TfIdf = {}

        tf = self.TF(classWords)
        idf = self.IDF(classWords)
        for key, item in tf.items():
            # TfIdf[key] = np.multiply(item, idf[key])
            TfIdf[key] = np.multiply(item, idf)
        return TfIdf

    # 预测
    def Prediction(self, testSet):
        preClass = []
        for item in testSet:
            words = self._buildWordDict(item)
            preClass.append(self._PredictionOne(words))
        return preClass

    # 预测单个,不能调用
    def _PredictionOne(self, words):
        words += 1 / np.sum(words)
        minInfo = ["", -sys.maxsize]
        for key, tfIdf in self.TfIdf.items():
            weight = np.sum(np.multiply(words, tfIdf))
            if weight > minInfo[1]:
                minInfo = (key, weight)
        return minInfo[0]
