import numpy as np
from Analysis.PerformanceMeasure import TimeM, MPoint

arr = np.random.random(100000000)


ik = [kk for kk in range(1000)]
def mutipy():
    arr2 = arr[ik]




def Median():
    np.median(arr)

def Sord():
    # np.sort(arr)
     np.argsort(arr)


# Sord()
# timeM=TimeM(Sord)
# timeM.StartTimeMeasure(2)

