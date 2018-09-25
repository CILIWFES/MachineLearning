import datetime
import time
import random
from collections import Counter
import numpy as np
import os
from Analysis import *

ddd = time.clock()


def ff():
    for i in range(1000):
        print(i)


ff()
dd2 = time.clock()

timeM = TimeM(ff)
timeM.StartTimeMeasure(1)
print("Test", dd2 - ddd)
