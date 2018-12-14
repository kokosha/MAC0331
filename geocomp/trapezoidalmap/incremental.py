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

from geocomp.pointrobot.structure import *


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


def Incremental(list_polygon):

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

	return mapa
