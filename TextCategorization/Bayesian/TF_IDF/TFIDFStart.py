from TextCategorization.StartBase import *
from Algorithm.Bayes.NaiveBayes.TFIDFClassification import *

tcStart = TCStart()
tcStart.Start(TFIDF, loops=1, performanceModel=False)
