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
def Printo(pol):
	pol.hilight()
	control.sleep()
	pol.plot('magenta')

# Código extra da Parte 1.1
def Generate(l):
	# Dado a lista de pontos do poligono e gera todos os segmentos de retas
	lsegments = []

	for i in range(len(l) - 1):
		lsegments.append(SSegment(SPoint(l[i].x, l[i].y), SPoint(l[i+1].x, l[i+1].y)))

	return lsegments



def Brute (l):

	# Criando e printando o retangulo externo
	oeste = l[0].x
	leste = l[0].x
	norte = l[0].y
	sul   = l[0].y

	for i in l:
		if i.x < oeste: oeste = i.x
		if i.x > leste: leste = i.x
		if i.y < sul  :   sul = i.y
		if i.y > norte: norte = i.y

	exterior = []

	exterior.append(Point(oeste-1, sul-1))
	exterior.append(Point(leste+1, sul-1))
	exterior.append(Point(leste+1, norte+1))
	exterior.append(Point(oeste-1, norte+1))

	ext = Polygon(exterior)
	Printo(ext)


	# Achando o conjunto de polígonos simples
	Lpolygon = []
	at = []
	pt = 0
	while pt < len(l):
		while len(at) == 0 or (pt < len(l) and at[0] != l[pt]):
			if len(at) != 0 and at[0].x == l[pt].x and at[0].y == l[pt].y:
				break
			at.append(l[pt])
			pt = pt + 1
		pt = pt + 1
		Lpolygon.append(at)
		at = []

	# Printando os polígonos simples
	for x in Lpolygon:
		blocked = Polygon(x)
		Printo(blocked)

	# Achando o espaço livre de locomoção em mapa de trapezoidação

	# Parte 1.1 - Transformando os polígonos iniciais em arestas(segmentos de retas)
	lsegments = []
	for l in Lpolygon:
		foo = Generate(l)
		for x in foo:
			lsegments.append(x)

	# Parte 1.2 - Criando o mapa de trapezoidação

	print("lsegments size is " + str(len(lsegments)))
	mapa = STrapezoidMap(lsegments)
	mapa.construct()
	# PRINT TRAPEZODATIO

	control_cnt = 0
	for trapezio in mapa.trapezoid_list:

		s_top = trapezio.s_top
		s_bottom = trapezio.s_bottom
		p_left = trapezio.p_left
		p_right = trapezio.p_right

		print("")
		print("Trapezio " + str(control_cnt))
		trapezio.debug()
		# Encontra equacao de reta de s_top e s_bottom ax+by+c = 0

		# y = (-c-a*x)/b
		At = s_top.p_right
		Bt = s_top.p_left
		at = Bt.y - At.y
		bt = At.x - Bt.x
		ct = - (at * At.x + bt * At.y)
		print ("top equation")
		print (at, bt, ct)


		# FUTURO CORNER CASE BT = 0
		yt_left = (-ct-at*p_left.x)/(bt)
		yt_right = (-ct-at*p_right.x)/(bt)

		Ab = s_bottom.p_right
		Bb = s_bottom.p_left
		ab = Bb.y - Ab.y
		bb = Ab.x - Bb.x
		cb = - (ab * Ab.x + bb * Ab.y)


		print ("bottom equation")
		print (ab, bb, cb)


		# CORNER CASE BT = 0
		yb_left = 1.0*(-cb - ab * p_left.x)/(bb)
		yb_right = 1.0*(-cb - ab * p_right.x)/(bb)


		linha1 = []
		linha1.append(Point(p_left.x, yt_left))
		linha1.append(Point(p_left.x, yb_left))
		linha1.append(Point(p_left.x, yt_left))		

		Printo(Polygon(linha1))		

		linha2 = []
		linha2.append(Point(p_right.x, yt_right))
		linha2.append(Point(p_right.x, yb_right))	
		linha2.append(Point(p_right.x, yt_right))

		Printo(Polygon(linha2))	

		control_cnt = control_cnt + 1

	# Parte 1.3 - Removendo as extensões vérticais dentro dos polígonos


	# Achando o grafo de locomoção

	# Parte 2.1 - Transformando em grafo

	# Parte 2.2 - Fazendo a query dos ponto inicial e ponto final





	# TESTE DO GRAFO
	'''
	grafo = Graph()
	condition = 0

	grafo.newVertex(12, 16)
	grafo.newVertex(16, 12)
	grafo.newVertex(12, 12)
	grafo.newVertex(16, 16)

	grafo.newEdge(grafo.findVertex(12, 16), grafo.findVertex(12, 12))
	grafo.newEdge(grafo.findVertex(12, 16), grafo.findVertex(16, 16))
	grafo.newEdge(grafo.findVertex(12, 16), grafo.findVertex(16, 12))

	grafo.newVertex(16, 8)
	grafo.newEdge(grafo.findVertex(16, 12), grafo.findVertex(16, 8))
	grafo.newVertex(16, 4)
	grafo.newEdge(grafo.findVertex(16, 8), grafo.findVertex(16, 4))

	grafo.newVertex(8, 16)
	grafo.newEdge(grafo.findVertex(12, 16), grafo.findVertex(8, 16))

	grafo.DFS(grafo.findVertex(16, 4), grafo.findVertex(16, 16))
	
	return 1
	'''




