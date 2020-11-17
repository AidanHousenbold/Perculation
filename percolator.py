import random
"""
You'll want to implement a smarter decision logic. This is skeleton code that you should copy and replace in your repository.
"""
class PercolationPlayer:
    def ChooseVertexToColor(graph, player):
        return random.choice([v for v in graph.V if v.color == -1])

    def ChooseVertexToRemove(graph, player):
        return random.choice([v for v in graph.V if v.color == player])
