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

import tkinter as tk

from geocomp.trapezoidalmap.structure import *
from geocomp.trapezoidalmap.incremental import *


class Box_Box:

	def __init__(self):
		self.sx = None
		self.sy = None
		self.ex = None
		self.ey = None
		self.query_window = tk.Tk()
		self.query_window.title("")
		self.query_window.geometry('400x160')
		self.query_window.resizable(0, 0)

		message = tk.Label(self.query_window, text="Insira os pontos iniciais e finais")
		message.grid(column = 0, row = 0)

		m_sx = tk.Label(self.query_window, text="Coordenada X do ponto inicial")
		m_sx.grid(column = 0, row = 1)

		self.t_sx = tk.Entry(self.query_window, width = 10)
		self.t_sx.grid(column = 1, row = 1)

		m_sy = tk.Label(self.query_window, text="Coordenada Y do ponto inicial")
		m_sy.grid(column = 0, row = 2)
		
		self.t_sy = tk.Entry(self.query_window, width = 10)
		self.t_sy.grid(column = 1, row = 2)

		m_ex = tk.Label(self.query_window, text="Coordenada X do ponto final")
		m_ex.grid(column = 0, row = 3)

		
		self.t_ex = tk.Entry(self.query_window, width = 10)
		self.t_ex.grid(column = 1, row = 3)

		m_ey = tk.Label(self.query_window, text="Coordenada Y do ponto final")
		m_ey.grid(column = 0, row = 4)

		self.t_ey = tk.Entry(self.query_window, width = 10)
		self.t_ey.grid(column = 1, row = 4)


		button = tk.Button(self.query_window, text="OK", command = self.clicked)
		button.grid(column = 0, row = 5)

		print("Before")
		self.query_window.wait_window()
		print("After")


	def clicked(self):
		self.sx = self.t_sx.get()
		self.sy = self.t_sy.get()
		self.ex = self.t_ex.get()
		self.ey = self.t_ey.get()
		self.can = tk.IntVar()
		self.query_window.destroy()

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

# Código extra para printar
def Print_S_and_T(pol):
	pol.hilight()
	control.sleep()
	pol.plot('yellow')

def Brute (list_polygon):

	#####################################################################################################

	"Coloque aqui o ponto que o robô está e o ponto que o robô quer ir, respectivamente."
	"O primeiro argumento é o x do ponto e o segundo é o y do ponto"


	box = Box_Box()

	print(box.sx, box.sy, box.ex, box.ey)

	start = SPoint(int(box.sx), int(box.sy))
	target = SPoint(int(box.ex), int(box.ey))
	#####################################################################################################

	mapa = Incremental(list_polygon)


	# Parte 1.3 - Removendo as extensões vérticais dentro dos polígonos
	mapa.checking()

	# Achando o grafo de locomoção


	startTrap = mapa.query(mapa.node_list[0], start)
	targetTrap = mapa.query(mapa.node_list[0], target)


	# Parte 2.1 - Transformando em grafo
	grafo = mapa.make_graph()


	#start = Point(0, 0)
	grafo.newVertex(start.x, start.y)
	#target = Point(10, 10)
	grafo.newVertex(target.x, target.y)

	grafo.newEdge(start.x, start.y, startTrap.info.center().x, startTrap.info.center().y)
	grafo.newEdge(target.x, target.y, targetTrap.info.center().x, targetTrap.info.center().y)

	Print_S_and_T(Point(start.x, start.y))
	Print_S_and_T(Point(target.x, target.y))

	grafo.DFS(grafo.findVertex(target.x, target.y), grafo.findVertex(start.x, start.y))
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




