import datetime
import time
import random
from collections import Counter
import numpy as np
import os
import math
from Analysis import *

K = 10000000
lst = [i for i in range(K)]
matrix = np.mat(lst)


def makeTest1():
    def test1():
        print(np.sum(matrix + matrix, dtype=float))
    return test1


def makeTest2():
    def test2():
        for i in lst:
            lst[i] += lst[i]
        print(sum(lst))

    return test2


test1Time = TimeM(makeTest1())
test1Time.StartTimeMeasure(1)

test2Time = TimeM(makeTest2())
test2Time.StartTimeMeasure(1)
