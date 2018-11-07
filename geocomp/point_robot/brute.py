#!/usr/bin/env python
"""Algoritmo forca-bruta"""
""" Dado um conjunto de pontos de poligonos disjuntos, achar o mapa trapezoidal"""

from geocomp.common.point import Point
from geocomp.common.polygon import Polygon
from geocomp.common.segment import Segment
from geocomp.common import control
from geocomp.common.guiprim import *
import math

from geocomp.point_robot.structure import *

#def Trap(trapezio):
	#Desenha o trapézio com o delay



# Código extra da Parte 1.1
def Generate(l):
	# Dado a lista de pontos do poligono e gera todos os segmentos de retas
	lsegments = []

	for i in range(len(l) - 1):
		lsegments.append(Segmento(Pointo(l[i].x, l[i].y), Pointo(l[i+1].x, l[i+1].y)))

	return lsegments




def Brute (l):
	if len(l) < 1:
		return 0

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

	ext.hilight()
	control.sleep()
	control.sleep()
	ext.plot()


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

	print(len(Lpolygon))
	for x in Lpolygon:
		# Criando e printando o polígono simples
		blocked = Polygon(x)
		#print
		blocked.hilight()
		control.sleep()
		control.sleep()
		blocked.plot()

	# Achando o espaço livre de locomoção em mapa de trapezoidação

	# Parte 1.1 - Transformando os polígonos iniciais em arestas(segmentos de retas)
	lsegments = []
	for l in Lpolygon:
		foo = Generate(l)
		for x in foo:
			lsegments.append(x)

	# Parte 1.2 - Criando o mapa de trapezoidação
	mapa = TrapezoidoMapo(lsegments)

	# Parte 1.3 - Removendo as extensões vérticais dentro dos polígonos


	# Achando o grafo de locomoção

	# Parte 2.1 - Transformando em grafo

	# Parte 2.2 - Fazendo a query dos ponto inicial e ponto final


	return 1