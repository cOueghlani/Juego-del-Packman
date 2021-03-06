# multiAgents.py
# --------------


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        # Comienza desde 0.
        PACMAN = 0

        def agenteMAX(state, depth):
            #En caso de perder o ganar (estados terminales)
            if state.isWin() or state.isLose():
                return state.getScore()

            # Coleccion de todas las acciones del Pacman
            acciones = state.getLegalActions(PACMAN)

            # Establecemos la puntuacion en menos infinito para obtener una puntuaci??n +alta
            mejorPuntuacion = float("-inf")

            # En caso de no haber accion se queda parado
            mejorAccion = Directions.STOP

            # Para cada accion
            for accion in acciones:

                # Calculamos la puntuacion -> llamando a agenteMIN pasandole el fantasma(siguiente nivel)
                puntuacion = agenteMIN(
                    state.generateSuccessor(PACMAN, accion), depth, 1)

                # Comprobaci??n de cual es la mejor puntuaci??n
                if puntuacion > mejorPuntuacion:
                    mejorPuntuacion = puntuacion
                    mejorAccion = accion

            #Si estamos en la raiz, devolvemos la accion
            if depth == 0:
                return mejorAccion
            #En caso contrario devolver la mejor puntuaci??n
            else:
                return mejorPuntuacion

        def agenteMIN(state, depth, ghost):

            #En caso de perder o ganar
            if state.isLose() or state.isWin():
                return state.getScore()

            # Siguiente ghost
            siguienteGhost = ghost + 1
            if ghost == state.getNumAgents() - 1:
                siguienteGhost = PACMAN

            # Coleccion de todas las acciones del ghost
            acciones = state.getLegalActions(ghost)

            # Se establece la puntuacion en menos infinito para obtener una puntuaci??n +alta
            mejorPuntuacion = float("inf")

            # Para cada accion
            for accion in acciones:

                # Si es el ultimo ghost
                if siguienteGhost == PACMAN:

                    #Si estamos en el nodo hoja
                    if depth == self.depth - 1:
                        puntuacion = self.evaluationFunction(
                            state.generateSuccessor(ghost, accion))

                    #si no estamos en el nofo hoja
                    else:
                        #Toca "jugar" al pacman
                        puntuacion = agenteMAX(
                            state.generateSuccessor(ghost, accion), depth + 1)

                #En caso de que no sea el ultimo
                else:
                    puntuacion = agenteMIN(state.generateSuccessor(
                        ghost, accion), depth, siguienteGhost)

                # Actualizamos la mejor puntuacion
                if mejorPuntuacion > puntuacion:
                    mejorPuntuacion = puntuacion

            return mejorPuntuacion

        return agenteMAX(gameState, 0)
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # Comienza desde 0.
        self.PACMAN = 0
        action = self.agenteMAX(gameState, 0, float("-inf"), float("inf"))
        return action

    def agenteMAX(self, state, depth, alpha, beta):

       #En caso de perder o ganar (estado terminal)
        if state.isLose() or state.isWin():
            return state.getScore()

        # Coleccion de todas las acciones del Pacman
        acciones = state.getLegalActions(self.PACMAN)

        # Establecemos la puntuacion en menos infinito para obtener una puntuaci??n +alta
        mejorPuntuacion = float("-inf")

        # En caso de no haber accion se inicializa en modo parado
        mejorAccion = Directions.STOP

        # Para cada accion
        for accion in acciones:

            # Calculamos la puntuacion -> llamando a agenteMIN pasandole el fantasma(siguiente nivel)
            puntuacion = self.agenteMIN(state.generateSuccessor(
                self.PACMAN, accion), depth, 1, alpha, beta)

            # Comprobaci??n de cual es la mejor puntuaci??n
            if puntuacion > mejorPuntuacion:
                mejorPuntuacion = puntuacion
                mejorAccion = accion

            # Actualizamos alpha
            if mejorPuntuacion > alpha:
                alpha = mejorPuntuacion

            #Si la puntuacion es mayor que beta, devolvemos la puntuacion
            if mejorPuntuacion > beta:
                return mejorPuntuacion

        #Si estamos en la raiz, devolvemos la accion
        if depth == 0:
            return mejorAccion
        #En caso contrario devolver la mejor puntuaci??n
        else:
            return mejorPuntuacion

    def agenteMIN(self, state, depth, ghost, alpha, beta):

        #En caso de perder o ganar (estado terminal)
        if state.isLose() or state.isWin():
            return state.getScore()

        # Siguiente ghost
        siguienteGhost = ghost + 1
        if ghost == state.getNumAgents() - 1:
            siguienteGhost = self.PACMAN

        # Coleccion de todas las acciones del ghost
        acciones = state.getLegalActions(ghost)

        # Se establece la puntuacion en infinito para obtener una puntuaci??n + baja
        mejorPuntuacion = float("inf")

        # Para cada accion
        for accion in acciones:

            # Si es el ultimo ghost
            if siguienteGhost == self.PACMAN:

                #Si estamos en el nodo hoja
                if depth == self.depth - 1:
                    puntuacion = self.evaluationFunction(
                        state.generateSuccessor(ghost, accion))

                #si no estamos en el nofo hoja
                else:
                    #Toca "jugar" al pacman
                    puntuacion = self.agenteMAX(state.generateSuccessor(
                        ghost, accion), depth + 1, alpha, beta)

            #En caso de que no sea el ultimo
            else:
                puntuacion = self.agenteMIN(state.generateSuccessor(
                    ghost, accion), depth, siguienteGhost, alpha, beta)

            # Actualizamos la mejor puntuacion
            if mejorPuntuacion > puntuacion:
                mejorPuntuacion = puntuacion

            # Actualizamos beta
            if beta > mejorPuntuacion:
                beta = mejorPuntuacion

            #Si alpha es mayor que la mejor puntuacion, devolvemos la puntuacion
            if alpha > mejorPuntuacion:
                return mejorPuntuacion

        return mejorPuntuacion
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        PACMAN = 0

        def max_agent(state, depth):
            if state.isWin() or state.isLose():
                return state.getScore()
            actions = state.getLegalActions(PACMAN)
            best_score = float("-inf")
            score = best_score
            best_action = Directions.STOP
            for action in actions:
                score = min_agent(state.generateSuccessor(
                    PACMAN, action), depth, 1)
                if score > best_score:
                    best_score = score
                    best_action = action
            if depth == 0:
                return best_action
            else:
                return best_score

        def min_agent(state, depth, ghost):
            if state.isLose():
                return state.getScore()
            next_ghost = ghost + 1
            if ghost == state.getNumAgents() - 1:
                # Although I call this variable next_ghost, at this point we are referring to a pacman agent.
                # I never changed the variable name and now I feel bad. That's why I am writing this guilty comment :(
                next_ghost = PACMAN
            actions = state.getLegalActions(ghost)
            best_score = float("inf")
            score = best_score
            for action in actions:
                prob = 1.0/len(actions)
                if next_ghost == PACMAN:  # We are on the last ghost and it will be Pacman's turn next.
                    if depth == self.depth - 1:
                        score = self.evaluationFunction(
                            state.generateSuccessor(ghost, action))
                        score += prob * score
                    else:
                        score = max_agent(state.generateSuccessor(
                            ghost, action), depth + 1)
                        score += prob * score
                else:
                    score = min_agent(state.generateSuccessor(
                        ghost, action), depth, next_ghost)
                    score += prob * score
            return score
        return max_agent(gameState, 0)
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
