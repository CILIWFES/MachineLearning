from TextCategorization.StartBase import *
from LearningAlgorithm.Bayes.Multinomial import *

tcStart = TCStart(cbts='h')
tcStart.Start(MNB, loops=1, performanceModel=False)
