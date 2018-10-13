from TextCategorization.StartBase import *
from LearningAlgorithm.Bayes.NaiveBayes.TFIDFClassification import *

tcStart = TCStart(cbts='h')
tcStart.Start(TFIDF, loops=1, performanceModel=False)
