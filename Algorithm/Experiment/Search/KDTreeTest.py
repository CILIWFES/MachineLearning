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

if ORM.exist(LoadPah + fileName) and performance:
    print('加载文件')
    MPoint.setPoint()
    kdTree = KDTree.ORMLoad(LoadPah + fileName)
    MPoint.showPoint()
    array = ORM.LoadPickle(LoadPah + 'test_Array')
    print('文件加载完成')
else:
    array = np.random.random(arrSize)
    kdTree = KDTree()
    print('生成KDTree中')
    MPoint.setPoint()
    kdTree.fit(array)
    MPoint.showPoint()
    print('生成KDTree完毕')

# 文件夹不存在 且为性能模式,自动保存
if not ORM.exist(LoadPah + fileName) and performance:
    print('保存KDTree中')
    MPoint.setPoint()
    kdTree.ORMSave(LoadPah, fileName)
    MPoint.showPoint()
    print('保存完毕')
    ORM.writePickle(LoadPah, "test_Array", array)


# 计算距离方法
def calculateDistant(index):
    return np.sum(np.power(np.power(target - index, 2), 0.5))


searchCount = arrSize[0] // 1000
print('搜索数量', searchCount)


# KDTree方法
def test_KDTree():
    datas, distrance = kdTree.Search(target, searchModel=KDTree.COUNTS_TYPE, searchCount=searchCount, magnification=0.1)
    return distrance


# 数组遍历方法
def test_Array():
    sortList = SortList(getValFunc=calculateDistant, cntsLimit=searchCount, searchType=SortList.INTERPOLATIONSEARCH)
    for item in array:
        sortList.put(item)
    return sortList.getValList()


print('________________________________')
print('测试坐标', target)

print('测试KD树')
MPoint.setPoint()
val = test_KDTree()
MPoint.showPoint()

print('测试顺序查找')
MPoint.setPoint()
valArr = test_Array()
MPoint.showPoint()

if valArr:
    print('正在对比')
    flag = True
    for i in range(len(val)):
        if val[i] != valArr[i]:
            print('错误:', i, 'KDTree', val, 'Array:', valArr)
            flag = False
        break
    if flag:
        print('无错误,最小值:', val[0])
#
# timeM = TimeM(test_KDTree)
# timeM.StartTimeMeasure(1)
#
# timeM = TimeM(test_Array)
# timeM.StartTimeMeasure(1)
