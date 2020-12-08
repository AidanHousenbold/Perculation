import random
import copy
from util import Vertex
from util import Edge
from util import Graph

class PercolationPlayer:
	class Tree:
		def __init__(self, data):
			self.children = []
			self.data = data
		def getChildren(self):
			return self.children
		def getData(self):
			return self.data
		def __repr__(self):
			return self.data

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
	        #print ("AlphaBeta:  Best State is: " + best_state.Name)
	        return best_state

	    def max_value(self, node, alpha, beta):
	        #print "AlphaBeta-->MAX: Visited Node :: " + node.Name
	        if self.isTerminal(node):
	            return self.getUtility(node)
	        infinity = float('inf')
	        value = -infinity

	        successors = self.getSuccessors(node)
	        for state in successors:
	            value = max(value, self.min_value(state, alpha, beta))
	            if value >= beta:
	                return value
	            alpha = max(alpha, value)
	        return value

	    def min_value(self, node, alpha, beta):
	        #print "AlphaBeta-->MIN: Visited Node :: " + node.Name
	        if self.isTerminal(node):
	            return self.getUtility(node)
	        infinity = float('inf')
	        value = infinity

	        successors = self.getSuccessors(node)
	        for state in successors:
	            value = min(value, self.max_value(state, alpha, beta))
	            if value <= alpha:
	                return value
	            beta = min(beta, value)

	        return value
	    #                     #
	    #   UTILITY METHODS   #
	    #                     #

	    # successor states in a game tree are the child nodes...
	    def getSuccessors(self, node):
	        assert node is not None
	        print("got here")
	        print(node.getChildren())
	        return node.getChildren()

	    # return true if the node has NO children (successor states)
	    # return false if the node has children (successor states)
	    def isTerminal(self, node):
	        assert node is not None
	        return len(node.children) == 0

	    def getUtility(self, node):
	        assert node is not None
	        return node.value
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

	def createGame_StateTree(graph, player, depth):
		if depth == 2:
			return PercolationPlayer.Tree(None)
		root = PercolationPlayer.Tree(graph)
		verts = [v for v in graph.V if v.color == player]
		for v in verts:
			newState = copy.deepcopy(graph)
			PercolationPlayer.Percolate(newState,newState.GetVertex(v.index))
			editedState = copy.deepcopy(newState)
			root.children.append(editedState)
			PercolationPlayer.createGame_StateTree((editedState), 1 - player, depth + 1)
		return PercolationPlayer.Tree(graph)

	def ChooseVertexToColor(graph, player): 
		return random.choice([v for v in graph.V if v.color == -1])

	def ChooseVertexToRemove(graph, player):
		print("got to Remove")
		tree = PercolationPlayer.createGame_StateTree(graph, player, 0)
		MM1 = PercolationPlayer.AlphaBeta(tree)
		print("got here")
		return MM1.alpha_beta_search(tree)


