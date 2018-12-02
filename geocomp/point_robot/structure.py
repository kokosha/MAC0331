import random
import copy
from geocomp.common.polygon import Polygon
from geocomp.common.point import Point
from geocomp.common import control

# SHALLOW COPY - orz

# Estrutura SPoint - Cada ponto tem sua coordenada x e coordenada y

class SPoint():
    def __init__ (self, x = None, y = None):
        self.x = x
        self.y = y

    def debug(self):
        print("SPoint")
        print(self.x, self.y)

    def is_left(self, point):
        return (self.x > point.x)

# Faz o produto vetorial de dois vetores p1 e p2

def cross(p1, p2):
    return p1.x * p2.y - p2.x * p1.y;

# Acha se o ponto p3 está em sentido anti-horário ou horário da reta p1 e p2

def ccw(p1, p2, p3):
    return cross(SPoint(p2.x - p1.x, p2.y - p1.y), SPoint(p3.x - p1.x, p3.y - p1.y));


# Estrutura SSegment - Cada segmento tem seu ponto mais a esquerda e o ponto mais a direita

class SSegment():
    def __init__ (self, p_left = None, p_right = None):
        self.p_left = p_left
        self.p_right = p_right

        self.linha = None

    def is_above(self, point):
        # NEED TO RECHECK
        return ccw(self.p_left, self.p_right, point) > 0

    def debug(self):
        print("SSegment")
        print(self.p_left.x, self.p_left.y, self.p_right.x, self.p_right.y)

    def show(self):
        p_left = self.p_left
        p_right = self.p_right
        linha = []
        linha.append(Point(p_left.x, p_left.y))
        linha.append(Point(p_right.x, p_right.y))
        linha.append(Point(p_left.x, p_left.y)) 

        self.linha = Polygon(linha)
        self.linha.plot('white')
        control.sleep()
        self.linha.plot('yellow')

    def hide(self):
        self.linha.hide()

# Estrutura STrapezoid - Guarda o trapezio baseado em quatro informacoes 
# O ponto mais a esquerda e o ponto mais a direita
# O segmento do topo e o segmento da esquerda
# Tem um dado especial que é o indice do trapézio
# Também possue links para os trapezios adjacentes

class STrapezoid():
    def __init__ (self, p_left = None, p_right = None, s_top = None, s_bottom = None, pid = None):
        self.p_left = p_left
        self.p_right = p_right
        self.s_top = s_top
        self.s_bottom = s_bottom
        self.pid = pid
        self.tid = 0

        self.t_upper_left = None
        self.t_upper_right = None
        self.t_lower_left = None
        self.t_lower_right = None

        self.linha1 = None
        self.linha2 = None

    def show(self):
        trapezio = self
        s_top = trapezio.s_top
        s_bottom = trapezio.s_bottom
        p_left = trapezio.p_left
        p_right = trapezio.p_right


        #trapezio.debug()
        # Encontra equacao de reta de s_top e s_bottom ax+by+c = 0

        # y = (-c-a*x)/b
        At = s_top.p_right
        Bt = s_top.p_left
        at = Bt.y - At.y
        bt = At.x - Bt.x
        ct = - (at * At.x + bt * At.y)
        #print ("top equation")
        #print (at, bt, ct)


        # FUTURO CORNER CASE BT = 0
        yt_left = (-ct-at*p_left.x)/(bt)
        yt_right = (-ct-at*p_right.x)/(bt)

        Ab = s_bottom.p_right
        Bb = s_bottom.p_left
        ab = Bb.y - Ab.y
        bb = Ab.x - Bb.x
        cb = - (ab * Ab.x + bb * Ab.y)


        #print ("bottom equation")
        #print (ab, bb, cb)


        # CORNER CASE BT = 0
        yb_left = 1.0*(-cb - ab * p_left.x)/(bb)
        yb_right = 1.0*(-cb - ab * p_right.x)/(bb)


        linha1 = []
        linha1.append(Point(p_left.x, yt_left))
        linha1.append(Point(p_left.x, yb_left))
        linha1.append(Point(p_left.x, yt_left))     

        self.linha1 = Polygon(linha1)
        self.linha1.plot('red')
        control.sleep()
        self.linha1.plot('blue')


        linha2 = []
        linha2.append(Point(p_right.x, yt_right))
        linha2.append(Point(p_right.x, yb_right))   
        linha2.append(Point(p_right.x, yt_right))

        self.linha2 = Polygon(linha2)
        self.linha2.plot('red')
        control.sleep()
        self.linha2.plot('blue')

    def hide(self):
        self.linha1.hide()
        self.linha2.hide()
    
    def debug(self):
        print ("s_top")
        print(self.s_top.p_left.x, self.s_top.p_left.y, self.s_top.p_right.x, self.s_top.p_right.y)

        print ("s_bottom")
        print(self.s_bottom.p_left.x, self.s_bottom.p_left.y, self.s_bottom.p_right.x, self.s_bottom.p_right.y)

        print ("p_left")
        print(self.p_left.x, self.p_left.y)

        print ("p_right")
        print(self.p_right.x, self.p_right.y)





# Estrutura SNode - Guarda os nós com a informações de busca e também guarda seu indices

class SNode():
    def __init__ (self, left = None, right = None, node_type = None, info = None, pid = None):
        self.left = left
        self.right = right
        # 0 - trapezio, 1 - segmento, 2 - ponto
        self.node_type = node_type
        self.info = info
        self.pid = pid

    def query(self, p_p):
        at = self
        while at.node_type != 0 :
            print ("q "+ str(at.node_type))
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

        return at


# Estrutura STrapezoidMap guarda as informações 


class STrapezoidMap():

    def __init__(self, segments):
        self.segments = segments


        # Parte 1
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

        minX = minX - 1
        minY = minY - 1
        maxX = maxX + 1
        maxY = maxY + 1

        s_top = SSegment(SPoint(minX, maxY), SPoint(maxX, maxY))
        s_bottom = SSegment(SPoint(minX, minY), SPoint(maxX, minY))
        p_left = SPoint(minX, maxY)
        p_right = SPoint(maxX, maxY)


        # Criando o trapezio
        t_start = STrapezoid(p_left, p_right, s_top, s_bottom, 0)
        t_start.show()


        # A estrutura de busca
        self.node_list = [SNode(None, None, 0, t_start, 0)]

        # Posicao de guardar
        self.trapezoid_list = [t_start]

        self.removed_node_list = []
        self.removed_trapezoid_list = []
    

    
    def follow_segment(self, node, segment):
        # Let p and q be the left and right endpoint of si.
        p_p = segment.p_left
        p_q = segment.p_right
        # Search with p and q in the search structure D to find D0.
        t_d0 = node.query(p_p)
        print ("follow " + str(t_d0.info.tid))
        t_list = []
        if t_d0 == None : 
            return t_list
        t_list.append(t_d0.info.tid)

        # while q lies to the right of rightp(Dj)
        # do if rightp(Dj) lies above si
        # then Let Dj+1 be the lower right neighbor of Dj lies.
        # else Let Dj+1 be the upper right neighbor of Dj lies.
        j = t_d0.info
        print("WAR " + str(j.pid))


        while j != None and (j.p_right != None and p_q.is_left(j.p_right)):
            #print(j.t_upper_left.pid, j.t_lower_left.pid)
            p_q.debug()
            j.p_right.debug()
            if segment.is_above(j.p_right):
                j = j.t_lower_right
            else:
                j = j.t_upper_right

            if j != None :
                t_list.append(j.tid)
            


        return t_list

    def add_node(self, node):
        v = -1
        if len(self.removed_node_list) > 0:
            v = self.removed_node_list[-1]
            self.removed_node_list.pop()
        else :
            v = len(self.node_list)
            self.node_list.append(SNode())
        # Mudando o posicao do trapezio e adicionando na lista
        node.pid = v
        if node.node_type == 0:
            node.info.tid = v
        self.node_list[v] = node
        return v


    def get_trapezoid(self):
        v = -1
        # Achando a posicao do trapezio na lista
        if len(self.removed_trapezoid_list) > 0:
            v = self.removed_trapezoid_list[-1]
            self.removed_trapezoid_list.pop()
        else :
            v = len(self.trapezoid_list)
            self.trapezoid_list.append(STrapezoid())
        return v
        ''''
    def add_trapezoid(self, trap):
        v = -1
        # Achando a posicao do trapezio na lista
        if len(self.removed_trapezoid_list) > 0:
            v = self.removed_trapezoid_list[-1]
            self.removed_trapezoid_list.pop()
        else :
            v = len(self.trapezoid_list)
            self.trapezoid_list.append(STrapezoid())

        # Mudando o posicao do trapezio e adicionando na lista
        trap.pid = v
        print("rs "+str(trap.pid))
        print(str(trap.t_upper_right.pid))
        print(str(trap.t_lower_right.pid))      
        self.trapezoid_list[v] = trap

        return v

    '''

        
    def simple_case(self, l_node, segment):
        # Parte 3

        print("Simple Case")
        node = self.node_list[l_node[0]]
        print("l_node "+str(l_node[0]))
        if (node.node_type == 0) :
            # Criando os novos trapezios podem ter 2, 3, 4 trapezios
            # Vamos primeiro supor que não existe coordenada x igual.

            # Note que se um ou ambos os pontos do segmentos for igual a p_left(D) or p_right(D)
            # Então pode acontecer de ter 2 ou 3 trapezios.
            # Note também que se existir um segmento que está contido em outro segmento
            # Então pode acontecer de ter 1 trapezios


            # Remover t
            t = node.info
            t.hide()
            # Adicionar t_top, t_bottom, t_left, t_right
                
            # FUTURO CORNER CASE
            t_left = copy.copy(node.info)
            t_left.p_right = segment.p_left
            t_left.show()
            t_left.pid = self.get_trapezoid()

            # FUTURO CORNER CASE
            t_right = copy.copy(node.info)
            t_right.p_left = segment.p_right
            t_right.show()
            t_right.pid = self.get_trapezoid()

            t_bottom = copy.copy(node.info)
            t_bottom.s_top = segment
            t_bottom.p_right = segment.p_right
            t_bottom.p_left = segment.p_left
            t_bottom.show()
            t_bottom.pid = self.get_trapezoid()

            t_top = copy.copy(node.info)
            t_top.s_bottom = segment
            t_top.p_right = segment.p_right
            t_top.p_left = segment.p_left
            t_top.show()
            t_top.pid = self.get_trapezoid()

            # Trecho 1.2 - Parte de botar as relações dos trapézios no lugar certo
            t_left.t_upper_left = t.t_upper_left
            t_left.t_lower_left = t.t_lower_left
            t_left.t_upper_right = t_top
            t_left.t_lower_right = t_bottom


            t_right.t_upper_left = t_top
            t_right.t_lower_left = t_bottom
            t_right.t_upper_right = t.t_upper_right
            t_right.t_lower_right = t.t_lower_right

            t_bottom.t_upper_left = t_left
            t_bottom.t_lower_left = t_left
            t_bottom.t_upper_right = t_right
            t_bottom.t_lower_right = t_right

            t_top.t_upper_left = t_left
            t_top.t_lower_left = t_left
            t_top.t_upper_right = t_right
            t_top.t_lower_right = t_right

            # Trecho 1.3 - Adicionar a relação inversa
            if t.t_upper_left != None :
                if t.t_upper_left.t_upper_right == t:
                    t.t_upper_left.t_upper_right = t_left
                if t.t_upper_left.t_lower_right == t:
                    t.t_upper_left.t_lower_right = t_left

            if t.t_lower_left != None :
                if t.t_lower_left.t_upper_right == t:
                    t.t_lower_left.t_upper_right = t_left
                if t.t_lower_left.t_lower_right == t:
                    t.t_lower_left.t_lower_right = t_left

            if t.t_upper_right != None :
                if t.t_upper_right.t_upper_left == t:
                    t.t_upper_right.t_upper_left = t_right
                if t.t_upper_right.t_lower_left == t:
                    t.t_upper_right.t_lower_left = t_right

            if t.t_lower_right != None :
                if t.t_lower_right.t_upper_left == t:
                    t.t_lower_right.t_upper_left = t_right
                if t.t_lower_right.t_lower_left == t:                 
                    t.t_lower_right.t_lower_left = t_right

            self.trapezoid_list[t_left.pid] = t_left
            self.trapezoid_list[t_right.pid] = t_right
            self.trapezoid_list[t_bottom.pid] = t_bottom
            self.trapezoid_list[t_top.pid] = t_top     

            print ("PID")
            print (t_left.pid, t_right.pid, t_bottom.pid, t_top.pid)


            # Trecho 2 - Atualizar a estrutura de busca


            a = SNode(None, None, 0, t_left)
            b = SNode(None, None, 0, t_right)
            c = SNode(None, None, 0, t_top)
            d = SNode(None, None, 0, t_bottom)
            s = SNode(c, d, 1, segment);
            q = SNode(s, b, 2, segment.p_right)
            p = SNode(a, q, 2, segment.p_left)

            self.node_list[node.pid] = p
            self.add_node(a)
            self.add_node(b)
            self.add_node(c)
            self.add_node(d)
            self.add_node(s)
            self.add_node(q)


    def hard_case(node, l_node, segment):


        # Parte 4
        # Trecho 1 - Atualizar o mapa trapezoidal


        # Os cantos sao aqueles que mudam

        print("Hard Case")
        tot = len(l_node)
        cnt = 0

        upper_trap = []
        lower_trap = []
        for x in l_node:
            at = self.node_list[x].info
            if cnt == 0:
                # QUEBRA O TRAPEZIO EM TRES PEDACOS
                t_left = copy.copy(at)
                t_left.p_right = segment.p_left

                t_bottom = copy.copy(at)
                t_bottom.s_top = segment
                t_bottom.p_right = segment.p_left
                t_bottom.p_left = segment.p_right

                t_top = copy.copy(at)
                t_top.s_bottom = segment
                t_top.p_right = segment.p_left
                t_top.p_left = segment.p_right



                upper_trap.append(t_top)
                lower_trap.append(t_bottom)

                    
            elif cnt == tot - 1:
                # QUEBRA O TRAPEZIO EM TRES PEDACOS
                t_left = copy.copy(at)
                t_left.p_left = segment.p_right

                t_bottom = copy.copy(at)
                t_bottom.s_top = segment
                t_bottom.p_right = segment.p_left
                t_bottom.p_left = segment.p_right

                t_top = copy.copy(at)
                t_top.s_bottom = segment
                t_top.p_right = segment.p_left
                t_top.p_left = segment.p_right

                upper_trap.append(t_top)
                lower_trap.append(t_bottom)


            else:
                # QUEBRA O TRAPEZIO EM DOIS PEDACOS
                t_bottom = copy.copy(at)
                t_bottom.s_top = segment
                t_bottom.p_right = segment.p_left
                t_bottom.p_left = segment.p_right

                t_top = copy.copy(at)
                t_top.s_bottom = segment
                t_top.p_right = segment.p_left
                t_top.p_left = segment.p_right

                upper_trap.append(t_top)
                lower_trap.append(t_bottom)

            cnt = cnt + 1

        merge(upper_trap)
        merge(lower_trap)


    def add(self, node, segment):

        # Parte 2
        t_list = self.follow_segment(node, segment)
        print("Add "+ str(len(t_list)))
        if len(t_list) == 1:
            self.simple_case(t_list, segment)
        else:
            self.hard_case(t_list, segment)




    def construct(self):
        segments = self.segments
        random.shuffle(segments)
        for seg in segments:
            seg.show()
            self.add(self.node_list[0], seg)
            seg.hide()

   