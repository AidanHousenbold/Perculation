import random
import copy
from util import Vertex
from util import Edge
from util import Graph

class PercolationPlayer:
	class Tree:
		def __init__(self, data, move, parent, player):
			self.children = []
			self.data = data
			self.move = move
			self.parent = parent
			self.player = player
		def __repr__(self):
			graph = self.data
			children = []
			for child in self.children:
				#children.append("Graph({0}, {1})".format(child.data.V, child.data.E))
				children.append(child.data.V)
			#returnList = ["Graph({0}, {1})".format(graph.V, graph.E), children]
			returnList = [graph.V, children]
			return str(returnList)

##########################
###### MINI-MAX A-B ######
##########################

	class AlphaBeta:
	    # print utility value of root node (assuming it is max)
	    # print names of all nodes visited during search
		def __init__(self, game_tree):
			self.game_tree = game_tree  # GameTree

		def alpha_beta_search(self, node):
			infinity = float('inf')
			best_val = -infinity
			beta = infinity

			successors = self.getSuccessors(node)
			best_state = None
			for state in successors:
				value = self.min_value(state, best_val, beta)
				if value > best_val:
					best_val = value
					best_state = state
			#print ("AlphaBeta:  Utility Value of Root Node: = " + str(best_val))
			#print ("AlphaBeta:  Best State is: ")
			#print(best_state.data.V)
			return best_state

		def max_value(self, node, alpha, beta):
	        #print "AlphaBeta-->MAX: Visited Node :: " + node.Name
			if self.isTerminal(node):
				return self.getUtility(node)
			infinity = float('inf')
			value = -infinity

			successors = self.getSuccessors(node)
			for state in successors:
				#print("State")
				#print(state.data.V)

				value = max(value, self.min_value(state, alpha, beta))
				if value >= beta:
					#print("Value 1")
					#print(value)
					return value
				alpha = max(alpha, value)
				#print("Value 2")
				#print(value)
			return value

		def min_value(self, node, alpha, beta):
			#print "AlphaBeta-->MIN: Visited Node :: " + node.Name
			if self.isTerminal(node):
				return self.getUtility(node)
			infinity = float('inf')
			value = infinity

			successors = self.getSuccessors(node)
			for state in successors:
				#print("State")
				#print(state.data.V)
				value = min(value, self.max_value(state, alpha, beta))
				if value <= alpha:
					#print("Value 1")
					#print(value)
					return value
				beta = min(beta, value)
				#print("Value 2")
				#print(value)
			return value
	    #                     #
	    #   UTILITY METHODS   #
	    #                     #

	    # successor states in a game tree are the child nodes...
		def getSuccessors(self, node):
			assert node is not None
			return node.children

		# return true if the node has NO children (successor states)
		# return false if the node has children (successor states)
		def isTerminal(self, node):
			assert node is not None
			return len(node.children) == 0

		def getUtility(self, node):
			winningStates = []
			loosingStates = []
			if node in winningStates:
				return float('inf')
			elif node in winningStates:
				infinity = float('inf')
				return -infinity
			else:
				return random.randint(-100,100)
#EXIT MINI MAX
	def gameOver(graph):
		node = graph.V[0]
		if graph.adjEdges(node) == null:
			return True 
		return False

	def GetVertex(graph, i):
	    for v in graph.V:
	        if v.index == i:
	            return v
	    return None

	def IncidentEdges(graph, v):
	    return [e for e in graph.E if (e.a == v or e.b == v)]

	def Percolate(graph, v):
		# Get attached edges to this vertex, remove them.
		for e in graph.IncidentEdges(v):
			graph.E.remove(e)
    	# Remove this vertex.
		graph.V.remove(v)
   		# Remove all isolated vertices.
		to_remove = {u for u in graph.V if len(graph.IncidentEdges(u)) == 0}
		graph.V.difference_update(to_remove)

	def createGame_StateTree(graph, player, depth, parent, move):
		if depth == 2:
			return PercolationPlayer.Tree(graph, move, parent, player)
		root = PercolationPlayer.Tree(graph, move, parent, player)
		verts = [v for v in graph.V if v.color == player]
		for v in verts:
			newState = copy.deepcopy(graph)
			PercolationPlayer.Percolate(newState, newState.GetVertex(v.index))
			newTree = PercolationPlayer.createGame_StateTree(newState, 1 - player, depth + 1, graph, v)
			root.children.append(newTree)
		return root

	def ChooseVertexToColor(graph, player): 
		return random.choice([v for v in graph.V if v.color == -1])

	def ChooseVertexToRemove(graph, player):
		tree = PercolationPlayer.createGame_StateTree(graph, player, 0, None, None)
		MM1 = PercolationPlayer.AlphaBeta(tree)
		Vertexs_new = MM1.alpha_beta_search(tree)
		#print("OG Graph")
		#print(graph.V)
		#print("_________________________________________")
		#print("vertex")
		#print(Vertexs_new.move)
		return Vertexs_new.move 



