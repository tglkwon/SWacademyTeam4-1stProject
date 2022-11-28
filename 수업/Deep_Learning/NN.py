from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import Perceptron
from sklearn.neural_network import MLPClassifier

voting = VotingClassifier()
grid = GridSearchCV()
perc = Perceptron()
