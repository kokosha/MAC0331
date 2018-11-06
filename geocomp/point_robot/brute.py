#!/usr/bin/env python
"""Algoritmo forca-bruta"""
""" Dado um conjunto de pontos de poligonos disjuntos, achar o mapa trapezoidal"""

from geocomp.common.point import Point
from geocomp.common.polygon import Polygon
from geocomp.common.segment import Segment
from geocomp.common import control
from geocomp.common.guiprim import *
import math

#def Trap(trapezio):
	#Desenha o trapézio com o delay

def Brute (l):

	#criando e printando o polígono inicial
	blocked = Polygon(l)
		#print
	blocked.hilight()
	control.sleep()
	control.sleep()
	blocked.plot()

	#criando e printando o retangulo externo
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

	return 1