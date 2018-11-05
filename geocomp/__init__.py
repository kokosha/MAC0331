# -*- coding: utf-8 -*-

"""Algoritmos de Geometria Computacional

Sub-modulos:
- convexhull: algoritmos para o problema do Fecho Convexo bidimensional
- farthest:   algoritmos para encontrar o par de pontos mais distante

- common:     classes e operacoes usadas por diversos algoritmos
- gui:        implementacoes das operacoes graficas
"""

from . import point_robot
from .common.guicontrol import init_display
from .common.guicontrol import config_canvas
from .common.guicontrol import run_algorithm
from .common.io import open_file
from .common.prim import get_count
from .common.prim import reset_count

children = (   ( 'point_robot', None, 'Plano de Locomação de Robos' ),
		( 'point_robot',  None, 'Plano de Locomação de Robos V2' ),
	)

__all__ = [p[0] for p in children]
