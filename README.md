# Juego-del-Packman
1.BUSQUEDA PACMAN
-Buscando un punto de comida fijo usando Depth First Search
python pacman.py -l tinyMaze -p SearchAgent
python pacman.py -l mediumMaze -p SearchAgent
python pacman.py -l bigMaze -z .5 -p SearchAgent
-Breadth First Search
python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs
python pacman.py -l bigMaze -p SearchAgent -a fn=bfs -z .5
-Algoritmo de búsqueda en grafo de coste uniforme (UCS)
python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs
python pacman.py -l mediumDottedMaze -p StayEastSearchAgent
python pacman.py -l mediumScaryMaze -p StayWestSearchAgent
-Busqueda A* (A* Search)
python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar
python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
-Buscando todas las esquinas (all the corners)
python pacman.py -l tinyCorners -p SearchAgent -a fn=bfs,prob=CornersProblem
python pacman.py -l mediumCorners -p SearchAgent -a fn=bfs,prob=CornersProblem
Problema de las cuatro esquinas: Heurístico (Corners Problem: Heurístico)
python pacman.py -l mediumCorners -p AStarCornersAgent -z 0.5
-Comiendo todos los puntos (Eating All The Dots: Heurístico)
python pacman.py -l testSearch -p AStarFoodSearchAgent
python pacman.py -l trickySearch -p AStarFoodSearchAgent
-Búsqueda subóptima (Suboptimal Search)
python pacman.py -l bigSearch -p ClosestDotSearchAgent -z .5

2.BUSQUEDA PACKAN MULTI-AGENTE
-Agente Reflex
python pacman.py -p ReflexAgent -l testClassic
Prueba el agente ReflexAgent en el tablero mediumClassic con un fantasma o dos:
python pacman.py -p ReflexAgent -k 1
python pacman.py -p ReflexAgent -k 2
python autograder.py -q q1
Para ejecutarlo sin gráficos, usa: python autograder.py -q q1 –no-graphics
-Minimax
python autograder.py -q q2
python autograder.py -q q2 –no-graphics
python pacman.py -p MinimaxAgent -l minimaxClassic -a depth=4
-Podado Alpha-Beta
python pacman.py -p AlphaBetaAgent -a depth=3 -l smallClassic
Para probar y depurar tu programa, ejecuta: python autograder.py -q q3
Esto te mostrará qué hace tu algoritmo en varios árboles pequeños, y también en un juego pacman. Para ejecutarlo sin gráficos, usa: python autograder.py -q q3 --no-graphics
-Expectimax
python pacman.py -p ExpectimaxAgent -l minimaxClassic -a depth=3
python pacman.py -p AlphaBetaAgent -l trappedClassic -a depth=3 -q -n 10
python pacman.py -p ExpectimaxAgent -l trappedClassic -a depth=3 -q -n 10
-Función de evaluación
python autograder.py -q q5
python autograder.py -q q5 –no-graphics

3.CLASIFICACIÓN
-Perceptron
python dataClassifier.py -c perceptron 
-Analisis del perceptron
python dataClassifier.py -c perceptron -w 
-MIRA
python dataClassifier.py -c mira --autotune 
-Clonando el comportamiento del Pacman
python dataClassifier.py -c perceptron -d pacman

Programa de autoevaluación: python autograder.py
