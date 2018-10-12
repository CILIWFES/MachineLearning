from TextCategorization.StartBase import *
from Algorithm.Bayes.NaiveBayes import *

tcStart = TCStart()
tcStart.Start(NaiveBayes, loops=1, performanceModel=False)
