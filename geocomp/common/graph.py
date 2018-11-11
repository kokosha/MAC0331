from geocomp.common.polygon import Polygon
from geocomp.common.segment import Segment
from geocomp.common.point import Point
from geocomp.common.vertex import Vertex
from geocomp.common.edge import Edge
from geocomp.common import control

# Código extra para printar
def Printo(pol):
	pol.hilight()
	control.sleep()
	pol.plot('magenta')

class Graph:
	def __init__(self):
		self.allVertex = []
		self.allEdge   = []

	def newVertex(self, x, y):
		self.allVertex.append(Vertex(x, y))
		Printo(Point(x, y))
		
	def findVertex(self, x, y):
		for i in self.allVertex:
			if (i.getX() == x) and (i.getY() == y):
				return i
		else:
			return None

	def newEdge(self, vertex1, vertex2):
		if (vertex1 != None) and (vertex2 != None):
			self.allEdge.append(Edge(vertex1, vertex2))
			point1 = Point(vertex1.getX(), vertex1.getY())
			point2 = Point(vertex2.getX(), vertex2.getY())
			Printo(Segment(point1, point2))
		else:
			print ("Falhou em newEdge -- vertices errados!")

	# ESTA COM BUG - Procura um vértice que ainda não foi visitado
	def findNeighbor(self, v):
		for i in range(len(self.allEdge)):
			print(self.allEdge[i])
			start = self.allEdge[i].getStart()
			end   = self.allEdge[i].getEnd()
			if (v.getX() == start.getX()) and (v.getY() == start.getY()) and (end.getVisited() == False):
				end.setVisited(True)
				#debug
				print(end.x)
				print(end.y)
				print("---")
				#
				return end
			if (v.getX()==end.getX()) and (v.getY()==end.getY()) and (start.getVisited()==False):
				start.setVisited(True)
				#debug
				print(start.x)
				print(start.y)
				print("---")
				#
				return start
		return print("Falhou em findNeighbor -- não tem mais vizinhos!")

	# Algoritmo base do DFS
	def DFS(self, target, start):
		for v in self.allVertex:
			v.setVisited(False)
		if (self.visit(start, target) == 1):
			print("O robô chegou no destino!")
		else:
			print("Falhou em visit -- não achou o caminho :(")


	def visit(self, u, target):
		u.setVisited(True)
		v = self.findNeighbor(u)
		while v is not None:
			# Printando o segmento atual do grafo
			seg = Segment(Point(u.x, u.y), Point(v.x, v.y))
			seg.plot('cyan')
			control.sleep()

			# Continuar o DFS
			if (v == target):
				return 1
			return self.visit(v, target)

			# Retirando o print do segmento
			seg.hide()
			control.sleep()

			# Pegar o próximo vizinho
			v = self.findNeighbor(u)
		return 0
