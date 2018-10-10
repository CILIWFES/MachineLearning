from TextCategorization.Bayesian.NaiveBayes import *
from DataProcessing import *
from Global import *
from Analysis.PerformanceMeasure import *
import os
from time import clock

mPoint = MPoint()

print("运行开始")

TrainSearch = GLOCT.SUPPORT_PATH + "TextCategorization/TrainSet/"
TrainJieSearch = GLOCT.SUPPORT_PATH + "TextCategorization/TrainSet_Jieba/"

LoadPah = GLOCT.SUPPORT_PATH + "TextCategorization/Pickle/"
FileName = "NaiveBayes.dat"

# 获取训练集合
fileInfo = ORM.autoSearch(TrainSearch)
classSet = []
trainSet = []
for info in fileInfo:
    dir = info[0]
    fileName = info[1]
    classSet.append(dir)
    trainSet.append(Pretreatment.autoJieba(TrainJieSearch + dir + "\\", fileName, TrainSearch + dir + "\\"))
    # 去除停用词
trainSet = [Pretreatment.filterWord(item) for item in trainSet]

# 获取训练集合(不能用自助法)
Bunchs = CBTS.makeSet(trainSet, classSet, "h", 10)

print("完成加载,开始执行")
# 性能模式(线上模式开启)
performanceModel = False

preClass = []
realClass = []


def start(Bunch):
    NB = None
    if performanceModel and os.path.exists(LoadPah + FileName):
        NB = NaiveBayes.loadPickle(LoadPah + FileName)
    else:
        mPoint.set_Time_RAM_Point()
        NB = NaiveBayes()
        NB.fit(Bunch.trainSet, Bunch.trainClass)  # [words1,words2,.........,words3],[class1,class2,......,classn]
        mPoint.show_Time_RAM_Point("构建朴素贝叶斯")

    if performanceModel:
        NB.savePickle(LoadPah, FileName)

    mPoint.set_Time_RAM_Point()
    preClass = NB.Prediction(Bunch.testSet)  # [words1,words1,.........,words1]
    mPoint.show_Time_RAM_Point("预测")

    return preClass, Bunch.testClass


for times, bunch in enumerate(Bunchs):
    print("第", times + 1, "次")
    preClassTemp, realClassTemp = start(bunch)  # [preclass1,preclass2,......,preclassn],[class1,class2,......,classn]
    preClass.extend(preClassTemp)
    realClass.extend(realClassTemp)

perM = PerM()
perM.fit(preClass, realClass)
perM.printPRFData()
