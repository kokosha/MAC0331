class Graph:
	def __init__(self):
		self.allVertex = []
		self.allEdge   = []

	def newVertex(self, x, y):
		self.allVertex.append(Vertex(x, y))

	def findVertex(self, x, y):
		for i in self.allVertex:
			if (i.getX() == x) and (i.getY() == y):
				return i
		else:
			return None

	def newEdge(self, vertex1, vertex2):
		if (vertex1 != None) and (vertex2 != None):
			self.allEdge.append(Edge(x0, y0, x1, y1))
		else:
			print ("Falhou em newEdge -- vertices errados!")

	def findNeighbor(self, v)
		for i in range(len(self.lista_Arestas)):
			start = self.allEdge[i].getStart()
			end   = self.allEdge[i].getEnd()
			if (v == start) and (end.getVisited() == False):
				end.setVisited(True)
				return end
			if (v == end) and (start.getVisited() == False):
				start.setVisited(True)
				return start
		else:
			return None

	def DFS(self, target):
		for v in self.allVertex:
			v.setVisited(False)
		for v in self.allVertex:
			if not v.getVisited():
				self.visit(v, target)

	def visit(self, u, target):
		u.setVisited(True)
		v = self.findNeighbor(u)
		while v is not None:
			v.setPrev(u)
			if (v == target):
				break
			self.visit(v, target)
			v = self.findNeighbor(u)
