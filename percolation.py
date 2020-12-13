import random
import copy
from util import Vertex
from util import Edge
from util import Graph

class PercolationPlayer:
	class Tree:
		def __init__(self, data, move, parent):
			self.children = []
			self.data = data
			self.move = move
			self.parent = parent

		def __repr__(self):
			graph = self.data
			children = []
			for child in self.children:
				#children.append("Graph({0}, {1})".format(child.data.V, child.data.E))
				children.append(child.data.V)
			#returnList = ["Graph({0}, {1})".format(graph.V, graph.E), children]
			returnList = [graph.V, children]
			return str(returnList)

	 # Returns the incident edges on a vertex.
	def IncidentEdges(graph, v):
		return [e for e in graph.E if (e.a == v or e.b == v)]

##########################
###### MINI-MAX A-B ######
##########################

	class AlphaBeta:
	    # print utility value of root node (assuming it is max)
	    # print names of all nodes visited during search
		def __init__(self, game_tree, active_player):
			self.game_tree = game_tree
			self.active_player = active_player

		def alpha_beta_search(self, node):
			infinity = 100000000000
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
			infinity = 100000000000
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
			infinity = 100000000000
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
			graph = node.data
			ally = 0
			opponent = 0
			for v in node.data.V:
				if v.color == self.active_player:
					ally += 1
				opponent +=1
			total = ally + opponent

			if len(node.data.E) == total + total*(total - 3)/2:
				return self.allEdgesHueristic(node,total)
			return ally - opponent

		def allEdgesHueristic(self, node, total):
			if total % 2 == 0:
				if node.move.color == self.active_player:
					return 1000
				else:
					return -1000
			else:
				if node.move.color == self.active_player:
					return -1000
				else:
					return 1000

		def getWinningStates(self, activePlayer):
			#a = Vertex("a",4)
			#f = Vertex("f", 3)
			#e1 = Edge(a,d,5)
			#e2 = Edge(a, b, 7)
			#e3 = Edge(b, d, 9)
			#V = {a,b,c}
			#E = {e1, e2, e3, e4, e5, e6, e7}
			#G = Graph(V, E)
			winningStates = []
			#WINNING STATE 1
			a1 = Vertex("a", activePlayer)
			b1 = Vertex("b", 1 - activePlayer)
			e1 = Edge(a1, b1)
			V1 = {a1, b1}
			E1 = {e1}
			winningState1 = Graph(V1, E1)
			winningStates.append(winningState1)

			#WINNING STATE 2
			a2 = Vertex("a", activePlayer)
			b2 = Vertex("b", activePlayer)
			c2 = Vertex("c", 1 - activePlayer)
			e1 = Edge(a2, b2)
			e2 = Edge(a2, c2)
			V2 = {a2, b2, c2}
			E2 = {e1, e2}
			winningState2 = Graph(V2, E2)
			winningStates.append(winningState2)

			return winningStates

			#WINNING STATE 3
			
		def getLosingStates(self, activePlayer):
			losingStates = []
			#LOSING STATE 1
			return losingStates
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

	def getPotentialVerticies(graph):
		verts ={vertex: 0 for vertex in graph.V}
		return verts

	def createGame_StateTree(graph, player, depth, parent, move):
		if depth == 2:
			return PercolationPlayer.Tree(graph, move, parent)
		root = PercolationPlayer.Tree(graph, move, parent)
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
		MM1 = PercolationPlayer.AlphaBeta(tree, player)
		Vertexs_new = MM1.alpha_beta_search(tree)
		#print("OG Graph")
		#print(graph.V)
		#print("_________________________________________")
		#print("vertex")
		#print(Vertexs_new.move)
		return Vertexs_new.move 



