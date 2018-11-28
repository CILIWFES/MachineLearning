from Algorithm.SortList import *
from random import randint
import numpy as np
from Analysis.PerformanceMeasure import *

times = 10000
arr = [randint(0, times) for i in range(times)]
arrNp = np.array(arr)
degreeOfPolymerization = (1 - np.unique(arrNp).size / len(arr)) * 100
uniformity = (1 - np.std(arrNp) / np.mean(arrNp)) * 100
gradient = np.sum(arrNp[1:] - arrNp[0:-1]) / (max(arr) - min(arr))
print('重合度量:', degreeOfPolymerization, '%')
print('均匀度量:', uniformity, '%')
print('梯度度量:', gradient)

print('----插入查找-------------------')
sortList = SortList(searchType=SortList.INTERPOLATIONSEARCH)
MPoint.setPoint()
for i in arr:
    sortList.put(i)
MPoint.showPoint()
# print(sortList.getValList())

print('----二分查找-------------------')
sortList = SortList(searchType=SortList.BINARYSEARCH)
MPoint.setPoint()
for i in arr:
    sortList.put(i)
MPoint.showPoint()
# print(sortList.getValList())

print('----顺序查找------------------')
sortList = SortList(searchType=SortList.SEQUENTIALSEARCH)
MPoint.setPoint()
for i in arr:
    sortList.put(i)
MPoint.showPoint()
# print(sortList.getValList())
