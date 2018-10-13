__all__ = ["KNN"]
from .KNNClassifier import KNNClassifier, KNN_RAM, KNN_TrainTime

# KNN选择
KNN = KNN_TrainTime
# KNN = KNN_RAM
# KNN = KNNClassifier
