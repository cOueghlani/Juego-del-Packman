# -- coding: UTF-8 --
# perceptron_pacman.py
# --------------------


# Perceptron implementation for apprenticeship learning
import util
from perceptron import PerceptronClassifier
from pacman import GameState

PRINT = True


class PerceptronClassifierPacman(PerceptronClassifier):
    def __init__(self, legalLabels, maxIterations):
        PerceptronClassifier.__init__(self, legalLabels, maxIterations)
        self.weights = util.Counter()

    def classify(self, data ):
        """
        Data contains a list of (datum, legal moves)
        
        Datum is a Counter representing the features of each GameState.
        legalMoves is a list of legal moves for that GameState.
        """
        guesses = []
        for datum, legalMoves in data:
            vectors = util.Counter()
            for l in legalMoves:
                vectors[l] = self.weights * datum[l] #changed from datum to datum[l]
            guesses.append(vectors.argMax())
        return guesses


    def train( self, trainingData, trainingLabels, validationData, validationLabels ):
        self.features = trainingData[0][0]['Stop'].keys() # could be useful later
        # DO NOT ZERO OUT YOUR WEIGHTS BEFORE STARTING TRAINING, OR
        # THE AUTOGRADER WILL LIKELY DEDUCT POINTS.

        for iteration in range(self.max_iterations):
            print "Starting iteration ", iteration, "..."
            for i in range(len(trainingData)):
                "*** YOUR CODE HERE ***"
                #Para cada variable
                variable = trainingLabels[i]

                #Para cada dato
                dato = trainingData[i]

                #Guardamos la clasifica del individuo
                clasificacionIndi = self.classify([dato])[0]

                #Si lo que he predecido es DISTINTO al valor "real"
                if clasificacionIndi != variable:

                    # Para la acción correcta
                    self.weights += dato[0][variable]
                    # Para la acción predecida
                    self.weights -= dato[0][clasificacionIndi]
                #util.raiseNotDefined()
