from TextCategorization.StartBase import *
from Algorithm.Bayes.Multinomial import *

tcStart = TCStart()
tcStart.Start(MNB, loops=1, performanceModel=False)
