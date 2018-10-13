from TextCategorization.StartBase import *
from LearningAlgorithm.KNN import *

tcStart = TCStart(cbts='h')
tcStart.Start(KNN, loops=1, performanceModel=False, cnt=10)
