# -- coding: UTF-8 --
# mira.py
# -------


# Mira implementation
import util
PRINT = True

class MiraClassifier:
    """
    Mira classifier.

    Note that the variable 'datum' in this code refers to a counter of features
    (not to a raw samples.Datum).
    """
    def __init__( self, legalLabels, max_iterations):
        self.legalLabels = legalLabels
        self.type = "mira"
        self.automaticTuning = False
        self.C = 0.001
        self.legalLabels = legalLabels
        self.max_iterations = max_iterations
        self.initializeWeightsToZero()

    def initializeWeightsToZero(self):
        "Resets the weights of each label to zero vectors"
        self.weights = {}
        for label in self.legalLabels:
            self.weights[label] = util.Counter() # this is the data-structure you should use

    def train(self, trainingData, trainingLabels, validationData, validationLabels):
        "Outside shell to call your method. Do not modify this method."

        self.features = trainingData[0].keys() # this could be useful for your code later...

        if (self.automaticTuning):
            Cgrid = [0.002, 0.004, 0.008]
        else:
            Cgrid = [self.C]

        return self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, Cgrid)

    def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, Cgrid):
        """
        This method sets self.weights using MIRA.  Train the classifier for each value of C in Cgrid,
        then store the weights that give the best accuracy on the validationData.

        Use the provided self.weights[label] data structure so that
        the classify method works correctly. Also, recall that a
        datum is a counter from features to values for those features
        representing a vector of values.
        """
        "*** YOUR CODE HERE ***"
        #Inicializamos el contador de pesos
        peso = util.Counter()

        #Recorremos la lista de valores constantes
        for c in Cgrid:
            #Asignamos su peso correspondiente
            peso[c] = self.weights

            #Definimos el nº maximo de iteraciones que va a tener nuestro algoritmo
            maxIteracion = range(self.max_iterations)

            #Por cada i que sea menor o igual al max_iterations
            for i in maxIteracion:

                #Definimos el tamaño del conjunto de entrenamiento
                entrenamientoTam = range(len(trainingData))

                #Por cada individuo del conjunto de entrenamiento
                for entT in entrenamientoTam:
                    #Definimos el vector de puntuaciones
                    puntuaciones = util.Counter()

                    #Guardamos las clases posibles para ser predecidas
                    clases = self.legalLabels

                    #Lista de atributos de cada individuo del conjunto de entrenamiento
                    listaVariables = trainingData[entT]

                    #Guardamos las clases reales de cada individuo (no las predecidas)
                    clasesReales = trainingLabels[entT]

                #Para todas las clases
                for cl in clases:
                    #Obtenemos la puntuacion de la clase que estamos evaluando realizando la multiplicacion
                    # de la matriz de pesos por el vector de variables
                    puntuaciones[cl] = peso[c][cl] * listaVariables

                #Obtenemos la clase a predecir obteniendo el valor más grande del vector de puntuaciones
                val = puntuaciones.argMax()

                #Obtenencion de los valores del vector de pesos asociado a la clase predecida y a la
                # clase correcta
                for l in listaVariables:
                    p = peso[c][val]
                    pReal = peso[c][clasesReales]

                #Calculamos el valor de la actualizacion eligiendo el mínimo entre el valor constante
                # y el valor de la fórmula
                T = min(c, ((p - pReal) * listaVariables + 1.0) /
                        (2 * (listaVariables*listaVariables)))

                #Actualizamos los vectores de pesos utilizando el valor que acabamos de obtener en T
                variable = listaVariables.copy()
                for v in variable:
                    variable[v] *= T

                #Actualizamos el vectore de pesos asociados a la clase predecida y a la clase correcta
                # utilizando el valor obtenido en variable
                peso[c][val] -= variable
                peso[c][clasesReales] += variable

        #util.raiseNotDefined()

    def classify(self, data ):
        """
        Classifies each datum as the label that most closely matches the prototype vector
        for that label.  See the project description for details.

        Recall that a datum is a util.counter...
        """
        guesses = []
        for datum in data:
            vectors = util.Counter()
            for l in self.legalLabels:
                vectors[l] = self.weights[l] * datum
            guesses.append(vectors.argMax())
        return guesses


