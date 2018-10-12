from TextCategorization.StartBase import *
from Algorithm.KNN import *

tcStart = TCStart()
tcStart.Start(KNN, loops=1, performanceModel=False, cnt=10)
