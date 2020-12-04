import random
from copy import deepcopy
from util import Vertex
from util import Edge
from util import Graph
from util import IncidentEdges, GetVertex

class Tree:
   class Tree:
    def __init__(self, data):
        self.children = []
        self.data = data

class PercolationPlayer:
	def ChooseVertexToColor(graph, player):
		return random.choice([v for v in graph.V if v.color == -1])

	def ChooseVertexToRemove(graph, player):
		print(createGame_tree(graph, player))

	def gameOver(graph):
		node = graph.V[0]
		if graph.adjEdges(node) == null:
			return True 
		return False

	def Percolate(graph, v):
		# Get attached edges to this vertex, remove them.
		for e in graph.IncidentEdges(v):
			graph.E.remove(e)
    	# Remove this vertex.
		graph.V.remove(v)
   		# Remove all isolated vertices.
		to_remove = {u for u in graph.V if len(graph.IncidentEdges(u)) == 0}
		graph.V.difference_update(to_remove)

	def createGame_StateTree(graph, player):
		root = Tree(graph)
		verts = [v for v in graph.V if v.color == active_player]
		for v in verts:
			newState = copy.deepcopy(graph)
			Percolate(newState,v)
			editedState = copy.deepcopy(newState)
			root.children.append(editedState)
			createGame_Statetree((editedState), 1 - active_player)
		return Tree(graph)