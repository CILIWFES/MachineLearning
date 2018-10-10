import datetime
import time
import random
from collections import Counter
import numpy as np
import os
import math
from Analysis import *
from decimal import Decimal
import matplotlib.pyplot as plt
import seaborn as sns


# 夹角余弦
def calculate(words1, words2):
    return np.sum(np.multiply(words1, words2)) / (
        math.sqrt(np.sum(np.power(words1, 2))) * math.sqrt(np.sum(np.power(words2, 2))))


words1 = np.mat([[1, 1]])
words2 = np.mat([[0, 1]])
print(calculate(words1,words2))