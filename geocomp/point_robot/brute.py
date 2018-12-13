#!/usr/bin/env python
"""Algoritmo forca-bruta"""
""" Dado um conjunto de pontos de poligonos disjuntos, achar o mapa trapezoidal"""

from geocomp.common.point import Point
from geocomp.common.polygon import Polygon
from geocomp.common.segment import Segment
from geocomp.common.graph import Graph
from geocomp.common.vertex import Vertex
from geocomp.common import control
from geocomp.common.guiprim import *
import math

from geocomp.point_robot.structure import *

# Código extra para printar
def Print(polygon_1):
	polygon_1.plot('green')
	control.sleep()
	polygon_1.plot('magenta')

def Hide(pol):
	pol.hide()

# Código extra da Parte 1.1
def Generate(l):
	# Dado a lista de pontos do poligono e gera todos os segmentos de retas
	lsegments = []
	n = len(l)
	if (n == 2) :
		lsegments.append(SSegment(SPoint(l[0].x, l[0].y), SPoint(l[1].x, l[1].y)))
		seg = Segment(Point(l[0].x, l[0].y), Point(l[1].x, l[1].y))
		seg.plot('green')
		control.sleep()
	else:
		for i in range(n):
			lsegments.append(SSegment(SPoint(l[i%n].x, l[i%n].y), SPoint(l[(i+1)%n].x, l[(i+1)%n].y)))
			seg = Segment(Point(l[i%n].x, l[i%n].y), Point(l[(i+1)%n].x, l[(i+1)%n].y))
			seg.plot('green')
			control.sleep()
	return lsegments



def Brute (list_polygon):

	# JIANG TERMINA AQUI, tem que pegar a entrada e colocar nesses pontos
	start = "onde o robo vai começar"
	target = "onde o robo quer terminar"

	# isso aqui vc tem que procurar com o DAG, eu n sei procurar nele :(
	startTrap = "trapezio em que o robo comecou"
	targetTrap = "trapezio em que o robo quer terminar"

	# Criando e printando o retangulo externo
	oeste = list_polygon[0].pts.x
	leste = list_polygon[0].pts.x
	norte = list_polygon[0].pts.y
	sul   = list_polygon[0].pts.y

	for polygon in list_polygon:
		for point in polygon.vertices():
			if point.x < oeste: oeste = point.x
			if point.x > leste: leste = point.x
			if point.y < sul  :   sul = point.y
			if point.y > norte: norte = point.y

	exterior = []

	exterior.append(Point(oeste-1, sul-1))
	exterior.append(Point(leste+1, sul-1))
	exterior.append(Point(leste+1, norte+1))
	exterior.append(Point(oeste-1, norte+1))

	ext = Polygon(exterior)
	Print(ext)


	# Printando os polígonos simples
	for polygon in list_polygon:
		Print(polygon)


	# Parte 1.1 - Transformando os polígonos iniciais em arestas(segmentos de retas)
	lsegments = []
	for polygon in list_polygon:
		foo = Generate(polygon.vertices())
		for x in foo:
			p1 = x.p_left
			p2 = x.p_right
			x.swap = 0

			if p1.x > p2.x or (p1.x == p2.x and p1.y > p2.y):
				x.p_left = p2
				x.p_right = p1
				x.swap = 1
			if len(polygon.vertices()) == 2:
				x.swap = 0
			lsegments.append(x)

	# Parte 1.2 - Criando o mapa de trapezoidação

	print("lsegments size is " + str(len(lsegments)))
	mapa = STrapezoidMap(lsegments)
	mapa.construct()


	# Parte 1.3 - Removendo as extensões vérticais dentro dos polígonos
	mapa.checking()
	# Achando o grafo de locomoção

	# Parte 2.1 - Transformando em grafo
	grafo = mapa.make_graph()

	grafo.DFS(target, start)
	'''
	# TESTE DO GRAFO

	grafo = Graph()
	condition = 0

	for x in val:
		grafo.newVertex(x[0].x, x[0].y)
		grafo.newVertex(x[1].x, x[1].y)
		grafo.newEdge(grafo.findVertex(x[0].x, x[0].y), grafo.findVertex(x[1].x, x[1].y))		
		seg = Segment(Point(x[0].x, x[0].y), Point(x[1].x, x[1].y))
		seg.plot('cyan')
		control.sleep()


	# Parte 2.2 - Achando o caminho	
	s = SPoint(1, 2)
	e = SPoint(2, 2)



	sn = mapa.query(mapa.node_list[0], s)
	en = mapa.query(mapa.node_list[0], e)
	if (-1e9 > s.x or 1e9 < s.x) :
		print("Outside boundary");
	elif (-1e9 > e.x or 1e9 < e.x) :
		print("Outside boundary");	
	elif sn.info.remove == 1:
		print("Outside boundary");
	elif en.info.remove == 1:
		print("Outside boundary");
	if sn.info == en.info:
		grafo.newVertex(e.x, e.y)
		grafo.newVertex(s.x, s.y)
		grafo.newEdge(grafo.findVertex(s.x, s.y), grafo.findVertex(e.x, e.y))
		seg = Segment(Point(s.x, s.y), Point(e.x, e.y))
		seg.plot('red')
		control.sleep()
	else:		
		if sn.node_type == 0 :
			x = sn.info.get_point()
			grafo.newVertex(x[0].x, x[0].y)
			grafo.newVertex(s.x, s.y)
			grafo.newEdge(grafo.findVertex(s.x, s.y), grafo.findVertex(x[0].x, x[0].y))

			seg = Segment(Point(s.x, s.y), Point(x[0].x, x[0].y))
			seg.plot('red')
			control.sleep()
		else:
			print("WRONG TYPE")
		if en.node_type == 0 :
			x = en.info.get_point()
			grafo.newVertex(x[0].x, x[0].y)
			grafo.newVertex(e.x, e.y)
			grafo.newEdge(grafo.findVertex(x[0].x, x[0].y), grafo.findVertex(e.x, e.y))
			seg = Segment(Point(x[0].x, x[0].y), Point(e.x, e.y))
			seg.plot('red')
			control.sleep()
		else:
			print("WRONG TYPE")

	grafo.DFS(grafo.findVertex(s.x, s.y), grafo.findVertex(e.x, e.y))
    #

	grafo.newVertex(3, 4)
	grafo.newVertex(4, 3)
	grafo.newVertex(3, 3)
	grafo.newVertex(4, 4)

	grafo.newEdge(grafo.findVertex(3, 4), grafo.findVertex(3, 3))
	grafo.newEdge(grafo.findVertex(3, 4), grafo.findVertex(4, 4))
	grafo.newEdge(grafo.findVertex(3, 4), grafo.findVertex(4, 3))

	grafo.newVertex(4, 2)
	grafo.newEdge(grafo.findVertex(4, 3), grafo.findVertex(4, 2))
	grafo.newVertex(4, 1)
	grafo.newEdge(grafo.findVertex(4, 2), grafo.findVertex(4, 1))

	grafo.newVertex(2, 4)
	grafo.newEdge(grafo.findVertex(3, 4), grafo.findVertex(2, 4))



	'''




