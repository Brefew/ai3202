In order to run Assignment 3 on the command line:
python astar_search.py worldname heuristic

Heuristic can be either 1 or 2

Second heuristic seeks out the direct diagonal movement first, before finishing with vertical or horizontal movement. Due to geometry, the hypotenuse of a triangle is guarenteed to be shorter than the sum of its two sides. So, given the destination node, and the current node's coordinates, this heuristic goes diagonally as far is it can in a straight line before using vertical or horizontal movements to reach the destination. 

This version of a heuristic gave the same path cost, however it lowered the amount of nodes that needed to be expanded and checked greatly.
