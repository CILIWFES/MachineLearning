from Categorization.Bayesian.NaiveBayes import *
from DataProcessing import *
from Global import *
from Analysis.PerformanceMeasure import *
import os

print("运行开始")

TrainSearch = GLOCT.ROOT_PATH + "FileSupport/Bayes/NaiveBayes/TrainSet/"
TestSearch = GLOCT.ROOT_PATH + "FileSupport/Bayes/NaiveBayes/TestSet/"
TrainJieSearch = GLOCT.ROOT_PATH + "FileSupport/Bayes/NaiveBayes/TrainSet_Jieba/"
TestJieSearch = GLOCT.ROOT_PATH + "FileSupport/Bayes/NaiveBayes/TestSet_Jieba/"

LoadPah = GLOCT.ROOT_PATH + "FileSupport/Bayes/NaiveBayes/Pickle/"
FileName = "NaiveBayes.dat"
# 性能模式
performanceModel = False

# 获取训练集合
fileInfo = ORM.autoSearch(TrainSearch)
classSet = []
trainSet = []
for info in fileInfo:
    dir = info[0]
    fileName = info[1]
    classSet.append(dir)
    trainSet.append(Pretreatment.autoJieba(TrainJieSearch + dir + "\\", fileName, TrainSearch + dir + "\\"))

# 获取训练集合
fileInfo = ORM.autoSearch(TestSearch)
realClass = []
testSet = []
for info in fileInfo:
    dir = info[0]
    fileName = info[1]
    realClass.append(dir)
    testSet.append(Pretreatment.autoJieba(TestJieSearch + dir + "\\", fileName, TestSearch + dir + "\\"))

print("完成加载")
NB = None
if performanceModel:
    if os.path.exists(LoadPah + FileName):
        NB = NaiveBayes.loadPickle(LoadPah + FileName)
    else:
        NB = NaiveBayes()
        NB.fit(trainSet, classSet)
else:
    NB = NaiveBayes()
    NB.fit(trainSet, classSet)

if performanceModel:
    NB.savePickle(LoadPah + FileName)

print("开始预测")
preClass = NB.Prediction(testSet)

perM = PerM()
perM.fit(preClass, realClass)
perM.printPRFData()
