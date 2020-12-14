import random
import copy
from util import Vertex
from util import Edge
from util import Graph
import cProfile
import time

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

	# Gets the edges attached to a given vertex
	def getEdges(graph, vertex):
	 	listofedges = []
	 	for edge in graph.E:
	 		if edge.a == vertex:
	 			listofedges.append(edge)
	 		elif edge.b == vertex:
	 			listofedges.append(edge)
	 	return listofedges

	 # Returns the incident edges on a vertex.
	def IncidentEdges(graph, v):
		return [e for e in graph.E if (e.a == v or e.b == v)]
	# Gets the other vertex on an edge from a given edge and vertex
	def getOtherVertex(edge, vertex):
		if edge.a == vertex:
			return edge.b
		else:
			return edge.a

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
			ally = [v for v in node.data.V if v.color == self.active_player]
			opponent = [v for v in node.data.V if v.color == 1 - self.active_player]
			total = len(ally) + len(opponent)
			if len(node.data.E) == total + total*(total - 3)/2:
				return self.allEdgesHueristic(node,total)
			if node.data in self.getWinningStates(self.active_player):
				return 10000000000000
			if node.data in self.getLosingStates(self.active_player):
				return -10000000000000
			num_ally_edges = 0
			numgoodedges = 0
			numbadedges = 0

			for v in ally:
				for edge in PercolationPlayer.getEdges(node.data, v):
					if PercolationPlayer.getOtherVertex(edge, v).color == self.active_player:
						numgoodedges += 1
					else:
						numbadedges +=1


			return (numgoodedges - numbadedges) + (len(ally) - len(opponent)) 
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
			winningStates = []
			#WINNING STATE 1 (2 Vertices)
			a1 = Vertex("a", activePlayer)
			b1 = Vertex("b", 1 - activePlayer)
			e1 = Edge(a1, b1)
			V1 = {a1, b1}
			E1 = {e1}
			winningState1 = Graph(V1, E1)
			winningStates.append(winningState1)


			#WINNING STATE 2 (3 Vertices)
			a2 = Vertex("a", activePlayer)
			b2 = Vertex("b", activePlayer)
			c2 = Vertex("c", 1 - activePlayer)
			e1 = Edge(a2, b2)
			e2 = Edge(a2, c2)
			V2 = {a2, b2, c2}
			E2 = {e1, e2}
			winningState2 = Graph(V2, E2)
			winningStates.append(winningState2)

			#WINNING STATE 3 (4 Vertices)
			a4 = Vertex("a", activePlayer)
			b4 = Vertex("b", activePlayer)
			c4 = Vertex("c", 1 - activePlayer)
			d4 = Vertex("d", 1 - activePlayer)

			e1 = Edge(a4, b4)
			e2 = Edge(a4, c4)
			e3 = Edge(a4, d4)
			e4 = Edge(c4, d4)
			e5 = Edge(b4, c4)

			V4 = {a4, b4, c4, d4}
			E3 = {e1, e2, e3}
			winningState3 = Graph(V4, E3)
			winningStates.append(winningState3)
			#ADD ON 3
			
			E4 = {e1, e2, e3, e4}
			winningStates.append(Graph(V4, E4))

			E5 = {e1, e2, e3, e4, e5}
			winningStates.append(Graph(V4, E5))

			#WINNING STATE 3
			return winningStates
		def getLosingStates(self, activePlayer):
			losingStates = []
			#LOSING STATE 1
			a1 = Vertex("a", activePlayer)
			b1 = Vertex("b", activePlayer)
			c1 = Vertex("c", 1 - activePlayer)
			d1 = Vertex("d", 1 - activePlayer)
			e1 = Edge(a1, b1)
			e2 = Edge(b1, c1)
			e3 = Edge(c1, d1)
			V1 = {a1, b1, c1, d1}
			E1 = {e1, e2, e3}
			losingState1 = Graph(V1, E1)
			losingStates.append(losingState1)

			#LOSING STATE 2
			a1 = Vertex("a", activePlayer)
			b1 = Vertex("b", 1 - activePlayer)
			c1 = Vertex("c", activePlayer)
			e1 = Edge(a1, b1)
			e2 = Edge(b1, c1)
			V1 = {a1, b1, c1}
			E1 = {e1, e2}
			losingState2 = Graph(V1, E1)
			losingStates.append(losingState2)

			#LOSING STATE 3 (4 Vertices)
			a3 = Vertex("a", 1 - activePlayer)
			b3 = Vertex("b", 1 - activePlayer)
			c3 = Vertex("c", activePlayer)
			d3 = Vertex("d", activePlayer)

			e1 = Edge(a3, b3)
			e2 = Edge(a3, c3)
			e3 = Edge(a3, d3)
			e4 = Edge(c3, d3)
			e5 = Edge(b3, d3)

			V4 = {a3, b3, c3, d3}
			E3 = {e1, e2, e3}
			losingState3 = Graph(V4, E3)
			losingStates.append(losingState3)
			#ADD ON 
			
			E4 = {e1, e2, e3, e4}
			losingStates.append(Graph(V4, E4))
			
			E3a = {e1, e2, Edge(b3, d3)}
			losingStates.append(Graph(V4, E3a))

			E5 = {e1, e4}
			losingStates.append(Graph(V4, E5))

			E6 = {e2, e5}
			losingStates.append(Graph(V4, E5))
			#LOSING STATE 5
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
		tic = time.perf_counter()
		uncolored = [v for v in graph.V if v.color == -1]
		champ = uncolored[0]
		for v in uncolored:
			if (len(PercolationPlayer.getEdges(graph, v))) > len(PercolationPlayer.getEdges(graph, champ)):
				champ = v
		toc = time.perf_counter()
		if toc - tic > 0.5:
			print("colorTooLong")
		return champ

	def ChooseVertexToRemove(graph, player): 
		tic = time.perf_counter()
		tree = PercolationPlayer.createGame_StateTree(graph, player, 0, None, None)
		#toc = time.perf_counter()
		#print(f"TreeCreat{toc - tic:0.4f} seconds")
		#tic = time.perf_counter()
		MM1 = PercolationPlayer.AlphaBeta(tree, player)
		#toc = time.perf_counter()
		#print(f"initialize{toc - tic:0.4f} seconds")
		#tic = time.perf_counter()
		Vertexs_new = MM1.alpha_beta_search(tree)
		toc = time.perf_counter()
		if(toc - tic) > 0.5:
			print("toolong")
			print(f"AlphaBeta{toc - tic:0.4f} seconds")
		#print("OG Graph")
		#print(graph.V)
		#print("_________________________________________")
		#print("vertex")
		#print(Vertexs_new.move)
		
	
		return Vertexs_new.move 



