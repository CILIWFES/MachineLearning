from Analysis.PerformanceMeasure import *
from Global import *
from Algorithm.Search import *
from Algorithm.SortList import *
from DataProcessing.ORM import *
import numpy as np

LoadPah = GLOCT.SUPPORT_PATH + "Algorithm/Pickle/Test/"
fileName = "test_KDTree"
# test
arrSize = (999999, 5)
target = (np.random.random((1, arrSize[1])).tolist())[-1]

performance = True
if performance:
    kdTree = KDTree.ORMLoad(LoadPah+fileName)
    array = ORM.LoadPickle(LoadPah + 'test_Array')
else:
    array = np.random.random(arrSize)
    kdTree = KDTree()
    MPoint.setPoint()
    kdTree.fit(array)
    MPoint.showPoint()

if not performance:
    kdTree.ORMSave(LoadPah, fileName)
    ORM.writePickle(LoadPah, "test_Array", array)


def calculateDistant(index):
    return np.sum(np.power(np.power(target - index, 2), 0.5))


searchCount = arrSize[0] // 10000
print(searchCount)


def test_KDTree():
    datas, distrance = kdTree.Search(target, searchModel=KDTree.COUNTS_TYPE, searchCount=searchCount,
                                     sortListType=SortList.INTERPOLATIONSEARCH)
    return distrance


def test_Array():
    sortList = SortList(getValFunc=calculateDistant, cntsLimit=searchCount, searchType=SortList.INTERPOLATIONSEARCH)
    # min=9999
    for item in array:
        sortList.put(item)
    #     mintemp=calculateDistant(item)
    #     if min>=mintemp:
    #         min=mintemp
    # return min
    return sortList.getValList()


print('________________________________')
print('测试坐标', target)

MPoint.setPoint()
print('KDT', test_KDTree())
MPoint.showPoint()

MPoint.setPoint()
print('Arr', test_Array())
MPoint.showPoint()

#
# timeM = TimeM(test_KDTree)
# timeM.StartTimeMeasure(1)
#
# timeM = TimeM(test_Array)
# timeM.StartTimeMeasure(1)
