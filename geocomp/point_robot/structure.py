import random

class SPoint():
    def __init__ (self, x = None, y = None):
        self.x = x
        self.y = y
    def is_left(point):
        return (self.x < point.x)


def cross(p1, p2):
    return p1.x * p2.y - p2.x * p1.y;

def ccw(p1, p2, p3):
    return cross(SPoint(p2.x-p1.x, p2.y-p1.y), SPoint(p3.x-p1.x, p3.y - p1.y));

class SSegment():
    def __init__ (self, p_left = None, p_right = None):
        self.p_left = p_left
        self.p_right = p_right

    def is_above(point):
        # NEED TO RECHECK
        return ccw(self.p_left, self.p_right, p) > 0; 

class STrapezoid():
    def __init__ (self, p_left = None, p_right = None, s_top = None, s_bottom = None, vid = None):
        self.p_left = p_left
        self.p_right = p_right
        self.s_top = s_top
        self.s_bottom = s_bottom
        self.vid = vid

        self.t_upper_left = None
        self.t_lower_left = None
        self.t_upper_right = None
        self.t_upper_right = None




class SNode():
    def __init__ (self, left = None, right = None, node_type = None, info = None, vid = None):
        self.left = left
        self.right = right
        # 0 - trapezio, 1 - segmento, 2 - ponto
        self.node_type = node_type
        self.info = info
        self.vid = vid
    def query(p_p):
        at = self
        while at.node_type != 0 :
            if at.node_type == 1:
                # checar cima e embaixo
                if(at.info.is_above(p_p)):
                    at = at.left
                else:
                    at = at.right
            else:
                # checar esquerda e direita
                if(at.info.is_left(p_p)):
                    at = at.left
                else:
                    at = at.right

        return at.info

class STrapezoidMap():
    def __init__(self, segments):
        self.segments = segments
        self.trapezoid_number = 0

        # Achando o trapezio externo
        minX = 1e9
        minY = 1e9
        maxX = -1e9
        maxY = -1e9
        for seg in segments :
            minX = min(minX, seg.p_left.x)
            minX = min(minX, seg.p_right.x)

            minY = min(minY, seg.p_left.y)
            minY = min(minY, seg.p_right.y)

            maxX = max(maxX, seg.p_left.x)
            maxX = max(maxX, seg.p_right.x)

            maxY = max(maxY, seg.p_left.y)
            maxY = max(maxY, seg.p_right.y)

        s_top = SSegment(SPoint(minX, maxY), SPoint(maxX, maxY))
        s_bottom = SSegment(SPoint(minX, minY), SPoint(maxX, minY))
        p_left = SPoint(minX, maxY)
        p_right = SPoint(maxX, maxY)
        t_start = STrapezoid(p_left, p_right, s_top, s_bottom, 0)


        # Estrutura de Busca
        self.node_list = [SNode(None, None, 0, t_start, 0)]

        # Posicao de guardar
        self.trapezoid_list = [t_start]
        self.trapezoid_number += 1;


        random.shuffle(segments)
        for seg in segments:
            add(seg)


    def follow_segment(segment):
        # Let p and q be the left and right endpoint of si.
        p_p = segment.p_left
        p_q = segment.p_right
        # Search with p and q in the search structure D to find D0.
        t_d0 = self.root.query(p_p)
        t_list = []
        if t_d0 == None : 
            return t_list
        t_list.append(t_d0)

        # while q lies to the right of rightp(Dj)
        # do if rightp(Dj) lies above si
        #then Let Dj+1 be the lower right neighbor of Dj lies.
        #else Let Dj+1 be the upper right neighbor of Dj lies.
        j = t_d0

    def add(segment):
        t_list = follow_segment(segment)
        if len(t_list) == 1:
            simple_case(t_list, segment)
        else:
            hard_case(t_list, segment)

    
    def simple_case(node, segment):
        # could be 2, 3, 4 trapezoid

        if (node.node_type == 0) :
            # Criando os novos trapezios podem ter 2, 3, 4 trapezios
            # Vamos primeiro supor que não existe coordenada x igual.

            # Note que se um ou ambos os pontos do segmentos for igual a p_left(D) or p_right(D)
            # Então pode acontecer de ter 2 ou 3 trapezios.
            # Note também que se existir um segmento que está contido em outro segmento
            # Então pode acontecer de ter 1 trapezios

            t = node.info
            # REMOVER TRAP LIST DEPOIS..

            # Trecho 1 - Atualizar o mapa trapezoidal
            # Trecho 1.1 - Parte de botar os segmentos e pontos dos trapézios no lugar certo
            
            # FUTURO CORNER CASE
            t_left = node.info
            self.trapezoid = self.trapezoid + 1
            t_left.vid = self.trapezoid
            t_left.pright = segment.s_left
            self.trapezoid_list.append(t_left)

            # FUTURO CORNER CASE
            t_right = node.info
            self.trapezoid = self.trapezoid + 1
            t_right.vid = self.trapezoid
            t_right.p_left= segment.s_right 
            self.trapezoid_list.append(t_right)

            t_bottom = node.info
            self.trazezoid = self.trapezoid + 1
            t_bottom.vid = self.trapezoid
            t_bottom.s_top = segment;
            t_bottom.p_right = segment.s_left
            t_bottom.p_left = segment.s_right
            self.trapezoid_list.append(t_bottom)


            t_top = node.info
            self.trapezoid = self.trapezoid + 1
            t_top.vid = self.trapezoid
            t_top.s_bot = segment;
            t_top.p_right = segment.s_left
            t_top.p_left = segment.s_right
            self.trapezoid_list.append(t_top)


            # Trecho 1.2 - Parte de botar as relações dos trapézios no lugar certo

            t_left.t_upper_left = t.t_upper_left.vid
            t_left.t_lower_left = t.t_lower_left.vid
            t_left.t_upper_right = t_top.vid
            t_left.t_lower_right = t_bottom.vid

            t_right.t_upper_left = t_top.vid
            t_right.t_lower_left = t_bottom.vid
            t_right.t_upper_right = t.t_upper_right.vid
            t_right.t_lower_right = t.t_lower_right.vid

            t_bottom.t_upper_left = t_left.vid
            t_bottom.t_lower_left = t_left.vid
            t_bottom.t_upper_right = t_right.vid
            t_bottom.t_lower_right = t_right.vid

            t_top.t_upper_left = t_left.vid
            t_top.t_lower_left = t_left.vid
            t_top.t_upper_right = t_right.vid
            t_top.t_lower_right = t_right.vid

            # Trecho 1.3 - Adicionar a relação inversa
            if t.t_upper_left != None :
                if t.t_upper_left.upper_right == t:
                    t.t_upper_left.upper_right = t_left.vid
                if t.t_upper_left.lower_right == t:
                    t.t_upper_left.lower_right = t_left.vid

            if t.t_lower_left != None :
                if t.t_lower_left.upper_right == t:
                    t.t_lower_left.upper_right = t_left.vid
                if t.t_lower_left.lower_right == t:
                    t.t_lower_left.lower_right = t_left.vid

            if t.t_upper_right != None :
                if t.t_upper_right.upper_left == t:
                    t.t_upper_right.upper_left = t_right.vid
                if t.t_upper_right.lower_left == t:
                    t.t_upper_right.lower_left = t_right.vid

            if t.t_lower_right != None :
                if t.t_lower_right.upper_left == t:
                    t.t_lower_right.upper_left = t_right.vid
                if t.t_lower_right.lower_left == t:                 
                    t.t_lower_right.lower_left = t_right.vid

            # Trecho 2 - Atualizar a estrutura de busca

            
            

'''
    def hard_case(node, segment):
         # Trecho 1 - Atualizar o mapa trapezoidal
         for x in node:


        else:
            assert(1)
'''
