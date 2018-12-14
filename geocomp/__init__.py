# -*- coding: utf-8 -*-

"""Algoritmos de Geometria Computacional

Sub-modulos:
- convexhull: algoritmos para o problema do Fecho Convexo bidimensional
- farthest:   algoritmos para encontrar o par de pontos mais distante

- common:     classes e operacoes usadas por diversos algoritmos
- gui:        implementacoes das operacoes graficas
"""

from . import convexhull
from . import farthest
from . import pointrobot
from . import trapezoidalmap
from .common.guicontrol import init_display
from .common.guicontrol import plot_input
from .common.guicontrol import run_algorithm
from .common.prim import get_count
from .common.prim import reset_count

children = (   ( 'convexhull', None, 'Fecho Convexo' ),
		( 'farthest',  None, 'Par Mais Distante' ),
		( 'trapezoidalmap',  None, 'Mapa de Trapezoidação' ),
		( 'pointrobot',  None, 'Plano de Locomoção de Robôs' ),	
	)

__all__ = [p[0] for p in children]
