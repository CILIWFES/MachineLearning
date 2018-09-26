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

K = 10000000
lst = [i for i in range(K)]
matrix = np.mat(lst)

sns.set_style("whitegrid")
plt.plot(np.arange(10))
plt.show()