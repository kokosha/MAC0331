# -*- coding: utf-8 -*-
"""Algoritmos para o problema do Plano de locomoção de robôs:

Dado um conjunto de pontos de um poligono simples que definem um labirinto e um conjunto 
de pontos de um poligono simples que definem um robo, determinar a regiao de locomoção do
robo

Algoritmos disponveis:
- Forca Bruta
"""
from . import brute

children = [
	[ 'brute', 'Brute', 'Forca Bruta' ]
]

__all__ = [a[0] for a in children]
