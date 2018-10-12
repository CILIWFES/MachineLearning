from TextCategorization.StartBase import *
from Algorithm.KNN import *

tcStart = TCStart(cbts='h')
tcStart.Start(KNN, loops=1, performanceModel=False, cnt=10)
