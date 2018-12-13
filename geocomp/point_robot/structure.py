import random
import copy
from math import fabs
from geocomp.common.polygon import Polygon
from geocomp.common.point import Point
from geocomp.common import control
from geocomp.common.graph import Graph
from geocomp.common.vertex import Vertex

# Estrutura SPoint - Cada ponto tem sua coordenada x e coordenada y

class SPoint():
    def __init__ (self, x = None, y = None):
        self.x = x
        self.y = y
    def __ne__(self, other):
        if(other == None):
            if (self == None):
                return False
            else:
                return True
        else:
            return self.x != other.x or self.y != other.y
    def debug(self):
        print("SPoint")
        print(self.x, self.y)

    def is_left(self, point):
        return (self.x > point.x) or (self.x == point.x and self.y > point.y) 

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
        self.swap = 0

        self.linha = None

    def is_above(self, point, point_2):
        # NEED TO RECHECK
        return ccw(self.p_left, self.p_right, point) > 0  or (ccw(self.p_left, self.p_right, point) == 0  and ccw(self.p_left, self.p_right, point_2) > 0 )
    def is_below(self, point):
        # NEED TO RECHECK
        return ccw(self.p_left, self.p_right, point) < 0  
    def is_equal(self, point):
        return ccw(self.p_left, self.p_right, point) == 0            

    def debug(self):
        print("SSegment")
        print(self.p_left.x, self.p_left.y, self.p_right.x, self.p_right.y)

    def show(self, color):
        p_left = self.p_left
        p_right = self.p_right
        linha = []
        linha.append(Point(p_left.x, p_left.y))
        linha.append(Point(p_right.x, p_right.y))
        linha.append(Point(p_left.x, p_left.y)) 

        self.linha = Polygon(linha)
        self.linha.plot(color)
        control.sleep()


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
        self.remove = 0

        self.t_upper_left = None
        self.t_upper_right = None
        self.t_lower_left = None
        self.t_lower_right = None

        self.left_comp = None
        self.right_comp = None

        self.linha1 = None
        self.linha2 = None

        # Saber se a varredura já passou por ele
        self.visited = False
   
    def center(self):
        return self.get_point()[0]

    def extPoints(self, mode):

        #Calcula os pontos extremos da esquerda
        if mode == "left":

            #Ponto superior
            p1up = self.s_top.p_left
            p2up = self.s_top.p_right
            mup = (p2up.y - p1up.y)/(p2up.x - p1up.x)
            yup = mup*(self.p_left.x - p2up.x) + p2up.y

            #Ponto inferior
            p1down = self.s_bottom.p_left
            p2down = self.s_bottom.p_right
            mdown = (p2down.y - p1down.y)/(p2down.x - p1down.x)
            ydown = mdown*(self.p_left.x - p2down.x) + p2down.y

            return self.p_left.x, yup, ydown

        #Calcula os pontos extremos da direita
        elif mode == "right":

            #Ponto superior
            p1up = self.s_top.p_left
            p2up = self.s_top.p_right
            mup = (p2up.y - p1up.y)/(p2up.x - p1up.x)
            yup = mup*(self.p_right.x - p2up.x) + p2up.y

            #Ponto inferior
            p1down = self.s_bottom.p_left
            p2down = self.s_bottom.p_right
            mdown = (p2down.y - p1down.y)/(p2down.x - p1down.x)
            ydown = mdown*(self.p_right.x - p2down.x) + p2down.y

            return self.p_right.x, yup, ydown

        #ERRO
        else:
            print("erro em extPoints - mandou mode errado!")

    def get_point(self):
        trapezio = self
        s_top = trapezio.s_top
        s_bottom = trapezio.s_bottom
        p_left = trapezio.p_left
        p_right = trapezio.p_right

        # Encontra equacao de reta de s_top e s_bottom ax+by+c = 0

        # y = (-c-a*x)/b
        At = s_top.p_right
        Bt = s_top.p_left
        at = Bt.y - At.y
        bt = At.x - Bt.x
        ct = - (at * At.x + bt * At.y)
        #print ("top equation")
        #print (at, bt, ct)


        # FUTURO CORNER CASE BT = 0 -
        if bt != 0:
            yt_left = (-ct-at*p_left.x)/(bt)
            yt_right = (-ct-at*p_right.x)/(bt)
        else:
            yt_left = p_right.y;
            yt_right = p_right.y;

        Ab = s_bottom.p_right
        Bb = s_bottom.p_left
        ab = Bb.y - Ab.y
        bb = Ab.x - Bb.x
        cb = - (ab * Ab.x + bb * Ab.y)


        #print ("bottom equation")
        #print (ab, bb, cb)


        # FUTURE CORNER CASE BB = 0 -
        if bb != 0:
            yb_left = 1.0*(-cb - ab * p_left.x)/(bb)
            yb_right = 1.0*(-cb - ab * p_right.x)/(bb)
        else:
            yb_left = p_left.y;
            yb_right = p_left.y;

        lista = []
        P1X = p_left.x
        P2X = p_left.x
        P3X = p_right.x
        P4X = p_right.x
        P5X = p_left.x
        P6X = p_right.x
        P1Y = yt_left
        P2Y = yb_left
        P3Y = yt_right
        P4Y = yb_right
        P5Y = p_left.y
        P6Y = p_right.y


        lista.append(Point((P1X+P2X+P3X+P4X)/4.0,(P1Y+P2Y+P3Y+P4Y)/4.0))
        if(P1X == P5X and P1Y == P5Y):
            lista.append(Point(1e9, 1e9))
        else:
            lista.append(Point((P1X+P5X)/2.0,(P1Y+P5Y)/2.0))
        if(P2X == P5X and P2Y == P5Y):
            lista.append(Point(1e9, 1e9))
        else:
            lista.append(Point((P2X+P5X)/2.0,(P2Y+P5Y)/2.0))
        if(P3X == P6X and P3Y == P6Y):
            lista.append(Point(1e9, 1e9))
        else:
            lista.append(Point((P3X+P6X)/2.0,(P3Y+P6Y)/2.0))  
        if(P4X == P6X and P4Y == P6Y):
            lista.append(Point(1e9, 1e9))
        else:       
            lista.append(Point((P4X+P6X)/2.0,(P4Y+P6Y)/2.0))    

        lista.append(P1X)
        lista.append(P2X)
        lista.append(P3X)
        lista.append(P4X)
        lista.append(P5X)
        lista.append(P6X)
        lista.append(P1Y)
        lista.append(P2Y)
        lista.append(P3Y)
        lista.append(P4Y)
        lista.append(P5Y)
        lista.append(P6Y)

        return lista
    def show(self, color):
        trapezio = self
        s_top = trapezio.s_top
        s_bottom = trapezio.s_bottom
        p_left = trapezio.p_left
        p_right = trapezio.p_right

        # trapezio.debug()
        # Encontra equacao de reta de s_top e s_bottom ax+by+c = 0

        # y = (-c-a*x)/b
        At = s_top.p_right
        Bt = s_top.p_left
        at = Bt.y - At.y
        bt = At.x - Bt.x
        ct = - (at * At.x + bt * At.y)
        #print ("top equation")
        #print (at, bt, ct)


        # FUTURO CORNER CASE BT = 0 -
        if bt != 0:
            yt_left = (-ct-at*p_left.x)/(bt)
            yt_right = (-ct-at*p_right.x)/(bt)
        else:
            yt_left = p_right.y;
            yt_right = p_right.y;

        Ab = s_bottom.p_right
        Bb = s_bottom.p_left
        ab = Bb.y - Ab.y
        bb = Ab.x - Bb.x
        cb = - (ab * Ab.x + bb * Ab.y)

        #print ("bottom equation")
        #print (ab, bb, cb)


        # FUTURO CORNER CASE BB = 0
        if bb != 0:
            yb_left = 1.0*(-cb - ab * p_left.x)/(bb)
            yb_right = 1.0*(-cb - ab * p_right.x)/(bb)
        else:
            yb_left = p_left.y;
            yb_right = p_left.y;

        linha1 = []
        linha1.append(Point(p_left.x, yt_left))
        linha1.append(Point(p_left.x, yb_left))
        linha1.append(Point(p_left.x, yt_left))     

        self.linha1 = Polygon(linha1)
        self.linha1.hide()
        self.linha1.plot(color)

        linha2 = []
        linha2.append(Point(p_right.x, yt_right))
        linha2.append(Point(p_right.x, yb_right))   
        linha2.append(Point(p_right.x, yt_right))

        self.linha2 = Polygon(linha2)
        self.linha2 .hide()
        self.linha2.plot(color)
        control.sleep()

    def hide(self):
        self.linha1.hide()
        self.linha2.hide()

    def blink(self, color = None):
        self.show("red")
        self.hide()
        if color == None :
            self.show("blue")
        else:
            self.show(color)
    
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
        self.remove = 0


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
        s_top.swap = 2
        s_bottom = SSegment(SPoint(minX, minY), SPoint(maxX, minY))
        s_bottom.swap = 2
        p_left = SPoint(minX, maxY)
        p_right = SPoint(maxX, maxY)


        # Criando o trapezio
        t_start = STrapezoid(p_left, p_right, s_top, s_bottom, 0)
        t_start.blink()

        # A estrutura de busca
        self.node_list = [SNode(None, None, 0, t_start, 0)]

        # Posicao de guardar
        self.trapezoid_list = [t_start]

        self.removed_node_list = []
        self.removed_trapezoid_list = []
 
    # Função que constroe o mapa trapezoidal
    def construct(self):
        segments = self.segments
        random.shuffle(segments)
        val = 0
        for seg in segments:
            print("Segmento " + str(val) + " inserido!")
            seg.show("yellow")
            self.add(self.node_list[0], seg)
            seg.hide()
            seg.show("white")
            val = val + 1


    # Constrói no grafo uma edge entre o centro do trapézio e 
    # a aresta que tem um trapézio como vizinho
    def medium_grapher(self, cTrap, X1, Y1, X2, Y2, graph):
        pM = Point((X1+X2)/2,(Y1+Y2)/2)
        graph.newVertex(pM.x, pM.y)
        graph.newEdge(cTrap.x, cTrap.y, pM.x, pM.y)
        return pM

    # Constrói o grafo resursivamente
    def grapher(self, trap, graph, prev):

        trap.visited = True
        trap.show('yellow')
        trap.hide()


        if (trap.center().x == prev.center().x and trap.center().y == prev.center().y):
            cTrap1 = trap.center()
        else:
            cTrap1 = prev.center()

        #check se existe vizinhos à direita
        if (trap.t_upper_right != None): cTrap2 = trap.t_upper_right.center()
        else: cTrap2 = None #vizinho de cima na direita
        if (trap.t_lower_right != None): cTrap3 = trap.t_lower_right.center()
        else: cTrap3 = None #vizinho de baixo na direita

        #   Caso exista, pode-se ter 3 casos: os dois existem (1), logo precisa ver se apontam
        #para o mesmo trapezio (1.1) e os outros dois somente se um dos dois existirem (2) e (3)

        #(1)
        if (cTrap2 != None and cTrap3 != None):
            trap.t_upper_right.show('light green')
            trap.t_upper_right.hide()
            trap.t_lower_right.show('orange')
            trap.t_lower_right.hide()

            tURx, tURty, tURby = trap.t_upper_right.extPoints("left")
            tLRx, tLRty, tLRby = trap.t_lower_right.extPoints("left")

            #(1.1)
            if (cTrap2.x == cTrap3.x and cTrap2.y == cTrap3.y):
                pM2 = Point((tURx+trap.t_upper_right.p_left.x)/2,(tURty+trap.t_upper_right.p_left.y)/2)
                a, b, c = trap.extPoints("right")
                #TALVEZ TENHA UM ERRO NESSA CONDICAO
                if (b > pM2.y):
                    if ((trap.t_upper_right.p_right.x - trap.t_upper_right.p_left.x) > 0):
                        pM = self.medium_grapher(cTrap1, tURx, tURty, trap.t_upper_right.p_left.x, trap.t_upper_right.p_left.y, graph)
                        if (not trap.t_upper_right.visited):
                            graph.newVertex(cTrap2.x, cTrap2.y)
                            self.grapher(trap.t_upper_right, graph, trap.t_upper_right)
                        graph.newEdge(pM.x, pM.y, cTrap2.x, cTrap2.y)
                    else:
                        self.grapher(trap.t_upper_right, graph, trap)

                else:
                    if ((trap.t_lower_right.p_right.x - trap.t_lower_right.p_left.x) > 0):
                        pM = self.medium_grapher(cTrap1, tLRx, tLRby, trap.t_lower_right.p_left.x, trap.t_lower_right.p_left.y, graph)
                        if (not trap.t_lower_right.visited):
                            graph.newVertex(cTrap3.x, cTrap3.y)
                            self.grapher(trap.t_lower_right, graph, trap.t_lower_right)
                        graph.newEdge(pM.x, pM.y, cTrap3.x, cTrap3.y)
                    else:
                        self.grapher(trap.t_lower_right, graph, trap)   
            
            else:
                if (trap.t_upper_right != None):
                    if ((trap.t_upper_right.p_right.x - trap.t_upper_right.p_left.x) > 0):
                        pM = self.medium_grapher(cTrap1, tURx, tURty, trap.t_upper_right.p_left.x, trap.t_upper_right.p_left.y, graph)
                        if (not trap.t_upper_right.visited):
                            graph.newVertex(cTrap2.x, cTrap2.y)
                            self.grapher(trap.t_upper_right, graph, trap.t_upper_right)
                        graph.newEdge(pM.x, pM.y, cTrap2.x, cTrap2.y)
                    else:
                        self.grapher(trap.t_upper_right, graph, trap)

                if (trap.t_lower_right != None):
                    if ((trap.t_lower_right.p_right.x - trap.t_lower_right.p_left.x) > 0):
                        pM = self.medium_grapher(cTrap1, tLRx, tLRby, trap.t_lower_right.p_left.x, trap.t_lower_right.p_left.y, graph)
                        if (not trap.t_lower_right.visited):
                            graph.newVertex(cTrap3.x, cTrap3.y)
                            self.grapher(trap.t_lower_right, graph, trap.t_lower_right)
                        graph.newEdge(pM.x, pM.y, cTrap3.x, cTrap3.y)
                    else:
                        self.grapher(trap.t_lower_right, graph, trap) 
            
        
        #(2)
        elif (cTrap2 != None and cTrap3 == None):
            tURx, tURty, tURby = trap.t_upper_right.extPoints("left")

            if (trap.t_upper_right != None):
                if ((trap.t_upper_right.p_right.x - trap.t_upper_right.p_left.x) > 0):
                    pM = self.medium_grapher(cTrap1, tURx, tURty, trap.t_upper_right.p_left.x, trap.t_upper_right.p_left.y, graph)
                    if (not trap.t_upper_right.visited):
                        graph.newVertex(cTrap2.x, cTrap2.y)
                        self.grapher(trap.t_upper_right, graph, trap.t_upper_right)
                    graph.newEdge(pM.x, pM.y, cTrap2.x, cTrap2.y)
                else:
                    self.grapher(trap.t_upper_right, graph, trap)


        #(3)
        elif (cTrap2 == None and cTrap3 != None):
            tLRx, tLRty, tLRby = trap.t_lower_right.extPoints("left")

            if (trap.t_lower_right != None):
                if ((trap.t_lower_right.p_right.x - trap.t_lower_right.p_left.x) > 0):
                    pM = self.medium_grapher(cTrap1, tLRx, tLRby, trap.t_lower_right.p_left.x, trap.t_lower_right.p_left.y, graph)
                    if (not trap.t_lower_right.visited):
                        graph.newVertex(cTrap3.x, cTrap3.y)
                        self.grapher(trap.t_lower_right, graph, trap.t_lower_right)
                    graph.newEdge(pM.x, pM.y, cTrap3.x, cTrap3.y)
                else:
                    self.grapher(trap.t_lower_right, graph, trap)         
     
    # Cria o grafo
    def make_graph(self):
        base = self.trapezoid_list[0]
        for i in self.trapezoid_list:
            if i.p_left.x < base.p_left.x:
                base = i
            elif i.p_left.x == base.p_left.x:
                if i.p_left.y < base.p_left.y:
                    base = i
                elif i.p_left.y == base.p_left.y:
                    if i.p_right.x < base.p_right.x:
                        base = i
                    elif i.p_right.y < base.p_right.y:
                        base = i

        #self.debug_relations(base)

        grafo = Graph()
        grafo.newVertex(base.center().x, base.center().y)
        self.grapher(base, grafo, base)

        return grafo

    def debug_relations(self, base):
        base.visited = True
        base.show('light blue')
        base.hide()
        base.show('orange')

        if (base.t_upper_right != None):
            if (not base.t_upper_right.visited):
                self.debug_relations(base.t_upper_right)
                base.t_upper_right.visited = True

        if (base.t_lower_right != None):
            if (not base.t_lower_right.visited):
                self.debug_relations(base.t_lower_right)
                base.t_lower_right.visited = True

    # Função que faz o incremento de um segmento
    def add(self, node, segment):
        t_list = self.follow_segment(node, segment)
        if len(t_list) == 1:
            self.simple_case(t_list, segment)
        else:
            self.hard_case(t_list, segment)

    # Função que acha os trapezios que intersecta dado um segmento
    # BUG?
    def follow_segment(self, node, segment):
        # Let p and q be the left and right endpoint of si.
        p_p = copy.deepcopy(segment.p_left)
        p_q = copy.deepcopy(segment.p_right)

        # SE FOR IGUAL NAO DA PARA SABER A POSICAO EM CIMA E EM BAIXO
        # TESTANDO PROPER INTERSECTION

        '''
        p_p.x = p_p.x + (p_q.x - p_p.x)*1e-9 
        p_p.y = p_p.y + (p_q.y - p_p.y)*1e-9 

        p_q.x = p_q.x + (p_p.x - p_q.x)*1e-9 
        p_q.y = p_q.y + (p_p.y - p_q.y)*1e-9
        '''

        # Search with p and q in the search structure D to find D0.
        t_d0 = self.query(node, p_p, p_q)
        t_list = []
        if t_d0 == None : 
            return t_list
        t_list.append(t_d0.info.tid)
        # while q lies to the right of rightp(Dj)
        # do if rightp(Dj) lies above si
        # then Let Dj+1 be the lower right neighbor of Dj lies.
        # else Let Dj+1 be the upper right neighbor of Dj lies.
        j = t_d0.info

        while j != None and (j.p_right != None and p_q.is_left(j.p_right)):
            if segment.is_above(j.p_right, None):
                j = j.t_lower_right
            else:
                j = j.t_upper_right

            if j != None :
                t_list.append(j.tid)

        return t_list

    # Procura na DAG de decisão
    def query(self, at, p_p, p_q):
        while at.node_type != 0 :
            if at.node_type == 1:
                # checar cima e embaixo
                if(at.info.is_above(p_p, p_q)):
                    at = self.node_list[at.left]
                else:
                    at = self.node_list[at.right]
            else:
                # checar esquerda e direita
                if(at.info.is_left(p_p)):
                    at = self.node_list[at.left]
                else:
                    at = self.node_list[at.right]
        return at
    


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


    def rmv_trapezoid(self, trap):
        trap.remove = 1
        trap.lower_right = None
        trap.lower_left = None
        trap.upper_right = None
        trap.upper_left = None

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

    # CASO SIMPLES
    # NO BUG

    def simple_case(self, l_node, segment):
        print("Fazendo o Simple Case")
        node = self.node_list[l_node[0]]
        if (node.node_type == 0) :
            # Remove o trapezio inicial
            # never used
            t = node.info
            t.hide()

            # Adicionar t_top, t_bottom, t_left, t_right
                
            # FUTURO CORNER CASE - OK
            if segment.p_left.x != t.p_left.x or segment.p_left.y != t.p_left.y:
                # INICIAL
                t_left = copy.copy(node.info)
                t_left.remove = 0
                t_left.p_right = segment.p_left
                t_left.blink()
                t_left.pid = self.get_trapezoid()
                exist_left = 1
            else:
                exist_left = 0


            # FUTURO CORNER CASE - OK
            if segment.p_right.x != t.p_right.x or segment.p_right.y != t.p_right.y:
                # INICIAL
                t_right = copy.copy(node.info)
                t_right.remove = 0
                t_right.p_left = segment.p_right
                t_right.blink()
                t_right.pid = self.get_trapezoid()
                exist_right = 1
            else:
                exist_right = 0


            # DEBUG
            '''
            if exist_left == 1:
                print("exist_left")

            if exist_right == 1:
                print("exist_right")
            '''


            t_bottom = copy.copy(node.info)
            t_bottom.remove = 0
            t_bottom.s_top = segment
            t_bottom.p_right = segment.p_right
            t_bottom.p_left = segment.p_left
            t_bottom.blink()
            t_bottom.pid = self.get_trapezoid()

            t_top = copy.copy(node.info)
            t_top.remove = 0
            t_top.s_bottom = segment
            t_top.p_right = segment.p_right
            t_top.p_left = segment.p_left
            t_top.blink()
            t_top.pid = self.get_trapezoid()

            # Trecho 1.2 - Parte de botar as relações dos trapézios no lugar certo
            if exist_left == 1 :
                t_left.t_upper_left = t.t_upper_left
                t_left.t_lower_left = t.t_lower_left
                t_left.t_upper_right = t_top
                t_left.t_lower_right = t_bottom

            if exist_right == 1:
                t_right.t_upper_left = t_top
                t_right.t_lower_left = t_bottom
                t_right.t_upper_right = t.t_upper_right
                t_right.t_lower_right = t.t_lower_right

            if exist_left == 1:
                t_bottom.t_upper_left = t_left
                t_bottom.t_lower_left = t_left
            else:
                if t_bottom.s_bottom.p_left != segment.p_left or t_bottom.s_top.p_left != segment.p_left:
                    t_bottom.t_upper_left = t.t_lower_left
                    t_bottom.t_lower_left = t.t_lower_left
                else:
                    t_bottom.t_upper_left = None
                    t_bottom.t_lower_left = None


            if exist_right == 1:
                t_bottom.t_upper_right = t_right
                t_bottom.t_lower_right = t_right
            else:
                if t_bottom.s_bottom.p_right != segment.p_right or t_bottom.s_top.p_right != segment.p_right:
                    t_bottom.t_upper_right = t.t_lower_right
                    t_bottom.t_lower_right = t.t_lower_right
                else:
                    t_bottom.t_upper_right = None
                    t_bottom.t_lower_right = None

            if exist_left == 1:
                t_top.t_upper_left = t_left
                t_top.t_lower_left = t_left
            else:
                if t_top.s_top.p_left != segment.p_left or t_top.s_bottom.p_left != segment.p_right:
                    t_top.t_upper_left = t.t_upper_left
                    t_top.t_lower_left = t.t_upper_left
                else:
                    t_top.t_upper_left = None
                    t_top.t_lower_left = None                        

            if exist_right == 1:
                t_top.t_upper_right = t_right
                t_top.t_lower_right = t_right
            else:
                if t_top.s_top.p_right != segment.p_right or t_top.s_bottom.p_right != segment.p_right:
                    t_top.t_upper_right = t.t_upper_right
                    t_top.t_lower_right = t.t_upper_right
                else:
                    t_top.t_upper_right = None
                    t_top.t_lower_right = None        

            # Trecho 1.3 - Adicionar a relação inversa
            if exist_left == 1:

                if t.t_upper_left != None :
                    if t.t_upper_left.t_upper_right == t :
                        t.t_upper_left.t_upper_right = t_left                    
                    if t.t_upper_left.t_lower_right == t :                
                        t.t_upper_left.t_lower_right = t_left

                if t.t_lower_left != None :
                    if t.t_lower_left.t_upper_right == t :
                        t.t_lower_left.t_upper_right = t_left
                    if t.t_lower_left.t_lower_right == t :
                        t.t_lower_left.t_lower_right = t_left

            else:
                # Se os dois forem diferentes entao existe uma reta que separa os dois trapezios
                if t.t_lower_left != t.t_upper_left:
                    if t.t_upper_left != None :
                        if t_top.s_top.p_left != segment.p_left or t_top.s_bottom.p_left != segment.p_left:
                            if t.t_upper_left.t_upper_right == t :
                                t.t_upper_left.t_upper_right = t_top                    
                            if t.t_upper_left.t_lower_right == t :    
                                t.t_upper_left.t_lower_right = t_top
                        else:
                            if t.t_upper_left.t_upper_right == t :
                                t.t_upper_left.t_upper_right = None                  
                            if t.t_upper_left.t_lower_right == t :    
                                t.t_upper_left.t_lower_right = None

                    if t.t_lower_left != None :
                        if t_bottom.s_bottom.p_left != segment.p_left or t_bottom.s_top.p_left != segment.p_left:
                            if t.t_lower_left.t_upper_right == t :
                                t.t_lower_left.t_upper_right = t_bottom
                            if t.t_lower_left.t_lower_right == t :
                                t.t_lower_left.t_lower_right = t_bottom 
                        else:
                            if t.t_lower_left.t_upper_right == t :
                                t.t_lower_left.t_upper_right = None
                            if t.t_lower_left.t_lower_right == t :
                                t.t_lower_left.t_lower_right = None
                else:
                    # A 
                    if t.t_upper_left != None and t.t_lower_left != None:
                        if (t_top.s_top.p_left != segment.p_left or t_top.s_bottom.p_left != segment.p_left) == False:
                            if t.t_lower_left.t_lower_right == t :
                                t.t_lower_left.t_lower_right = t_bottom                    
                        elif (t_bottom.s_bottom.p_left != segment.p_left or t_bottom.s_top.p_left != segment.p_left) == False:
                            if t.t_upper_left.t_upper_right == t :
                                t.t_upper_left.t_upper_right = t_top 
                        else:
                            assert(0)    
            if exist_right == 1:
                if t.t_upper_right != None :
                    if t.t_upper_right.t_upper_left == t :
                        t.t_upper_right.t_upper_left = t_right
                    if t.t_upper_right.t_lower_left == t :
                        t.t_upper_right.t_lower_left = t_right

                if t.t_lower_right != None :
                    if t.t_lower_right.t_upper_left == t:
                        t.t_lower_right.t_upper_left = t_right
                    if t.t_lower_right.t_lower_left == t:
                        t.t_lower_right.t_lower_left = t_right
            else:
                if t.t_lower_right != t.t_upper_right:
                    if t.t_upper_right != None :
                        if t_top.s_top.p_right != segment.p_right or t_top.s_bottom.p_right != segment.p_right:
                            if t.t_upper_right.t_upper_left == t :
                                t.t_upper_right.t_upper_left = t_top
                            if t.t_upper_right.t_lower_left == t :
                                t.t_upper_right.t_lower_left = t_top
                        else:
                            if t.t_upper_right.t_upper_left == t :
                                t.t_upper_right.t_upper_left = None
                            if t.t_upper_right.t_lower_left == t :
                                t.t_upper_right.t_lower_left = None                     

                    if t.t_lower_right != None :
                        if t_bottom.s_bottom.p_right != segment.p_right or t_bottom.s_top.p_right != segment.p_right:
                            if t.t_lower_right.t_upper_left == t:
                                t.t_lower_right.t_upper_left = t_bottom      
                            if t.t_lower_right.t_lower_left == t:
                                t.t_lower_right.t_lower_left = t_bottom
                        else:
                            if t.t_lower_right.t_upper_left == t:
                                t.t_lower_right.t_upper_left = None      
                            if t.t_lower_right.t_lower_left == t:
                                t.t_lower_right.t_lower_left = None  
                else:
                    # A 
                    if t.t_upper_right != None and t.t_lower_right != None:
                        if (t_top.s_top.p_right != segment.p_right or t_top.s_bottom.p_right != segment.p_right) == False:
                            if t.t_lower_right.t_lower_left == t :
                                t.t_lower_right.t_lower_left = t_bottom                    
                        elif (t_bottom.s_bottom.p_right != segment.p_right or t_bottom.s_top.p_right != segment.p_right) == False:
                            if t.t_upper_right.t_upper_left == t :
                                t.t_upper_right.t_upper_left = t_top
                        else:
                            assert(0)                          

            if exist_left == 1:
                self.trapezoid_list[t_left.pid] = t_left
            if exist_right == 1:
                self.trapezoid_list[t_right.pid] = t_right
            self.trapezoid_list[t_bottom.pid] = t_bottom
            self.trapezoid_list[t_top.pid] = t_top   

            # DEBUG
            if exist_right == 1:
                print("t_right simple_case")
                self.relation_trap(t_right)
            if exist_left == 1:
                print("t_left simple_case")
                self.relation_trap(t_left)

            print("t_bottom simple_case")
            self.relation_trap(t_bottom) 

            print("t_top simple_case")      
            self.relation_trap(t_top)   

            print ("PID")
            if exist_left == 1:
                print ("LEFT " + str(t_left.pid))
            if exist_right == 1:
                print("RIGHT "  + str(t_right.pid))
            print ("BOTTOM " + str(t_bottom.pid) + " TOP "  + str(t_top.pid))
            # Trecho 2 - Atualizar a estrutura de busca
            if exist_left == 0 and exist_right == 0:
                c = SNode(None, None, 0, t_top)
                d = SNode(None, None, 0, t_bottom)
                id_c = self.add_node(c)
                id_d = self.add_node(d)
                s = SNode(id_c, id_d, 1, segment);
                self.node_list[node.pid] = s

            elif exist_left == 0 and exist_right == 1:
                b = SNode(None, None, 0, t_right)
                c = SNode(None, None, 0, t_top)
                d = SNode(None, None, 0, t_bottom)
                id_b = self.add_node(b)
                id_c = self.add_node(c)
                id_d = self.add_node(d)
                s = SNode(id_c, id_d, 1, segment);
                id_s = self.add_node(s)
                q = SNode(id_s, id_b, 2, segment.p_right)
                self.node_list[node.pid] = q                      

            elif exist_left == 1 and exist_right == 0:
                a = SNode(None, None, 0, t_left)
                c = SNode(None, None, 0, t_top)
                d = SNode(None, None, 0, t_bottom)
                id_a = self.add_node(a)
                id_c = self.add_node(c)
                id_d = self.add_node(d)
                s = SNode(id_c, id_d, 1, segment);
                id_s = self.add_node(s)
                p = SNode(id_a, id_s, 2, segment.p_left)
                self.node_list[node.pid] = p
 

            elif exist_left == 1 and exist_right == 1:
                a = SNode(None, None, 0, t_left)
                b = SNode(None, None, 0, t_right)
                c = SNode(None, None, 0, t_top)
                d = SNode(None, None, 0, t_bottom)
                id_a = self.add_node(a)
                id_b = self.add_node(b)
                id_c = self.add_node(c)
                id_d = self.add_node(d)
                s = SNode(id_c, id_d, 1, segment);
                id_s = self.add_node(s)
                q = SNode(id_s, id_b, 2, segment.p_right)
                id_q = self.add_node(q)
                p = SNode(id_a, id_q, 2, segment.p_left)
                self.node_list[node.pid] = p
            else:
                assert(0)


            self.rmv_trapezoid(t)

    def update_relation(self, l_trap, t_trap):
        # LAST TRAPEZOID LOWER RIGHT
        if l_trap.right_comp.t_lower_right == t_trap.left_comp :
            l_trap.t_lower_right = t_trap #3
        else:
            l_trap.t_lower_right = l_trap.right_comp.t_lower_right # 3

            if l_trap.right_comp.t_lower_right != None:
                if l_trap.right_comp.t_lower_right.t_upper_left == l_trap.right_comp:
                    l_trap.right_comp.t_lower_right.t_upper_left = l_trap
                if l_trap.right_comp.t_lower_right.t_lower_left == l_trap.right_comp:
                    l_trap.right_comp.t_lower_right.t_lower_left = l_trap                                  

        # LAST TRAPEZOID UPPER RIGHT
        if l_trap.right_comp.t_upper_right == t_trap.left_comp :
            l_trap.t_upper_right = t_trap #3
        else:
            l_trap.t_upper_right = l_trap.right_comp.t_upper_right # 3 
            if l_trap.right_comp.t_upper_right != None:
                if l_trap.right_comp.t_upper_right.t_upper_left == l_trap.right_comp:
                    l_trap.right_comp.t_upper_right.t_upper_left = l_trap
                if l_trap.right_comp.t_upper_right.t_lower_left == l_trap.right_comp:
                    l_trap.right_comp.t_upper_right.t_lower_left = l_trap
        
        # ATUAL TRAPEZOID LOWER LEFT
        if t_trap.left_comp.t_lower_left == l_trap.right_comp:
            t_trap.t_lower_left = l_trap
        else:
            t_trap.t_lower_left = t_trap.left_comp.t_lower_left  
            if t_trap.left_comp.t_lower_left != None:
                if t_trap.left_comp.t_lower_left.t_upper_right == t_trap.left_comp:
                    t_trap.left_comp.t_lower_left.t_upper_right = t_trap
                if t_trap.left_comp.t_lower_left.t_lower_right == t_trap.left_comp:
                    t_trap.left_comp.t_lower_left.t_lower_right = t_trap

        # ATUAL TRAPEZOID UPPER LEFT 
        if t_trap.left_comp.t_upper_left == l_trap.right_comp:
            t_trap.t_upper_left = l_trap
        else:
            t_trap.t_upper_left = t_trap.left_comp.t_upper_left
            if t_trap.left_comp.t_upper_left != None:
                if t_trap.left_comp.t_upper_left.t_upper_right == t_trap.left_comp:
                    t_trap.left_comp.t_upper_left.t_upper_right = t_trap
                if t_trap.left_comp.t_upper_left.t_lower_right == t_trap.left_comp:
                    t_trap.left_comp.t_upper_left.t_lower_right = t_trap

    def hard_case(self, l_node, segment):
        # Parte do Hard Case

        print("Fazendo o Hard Case")
        tot = len(l_node)

        # Achando a lista de trapezioss
        list_trap = [] 
        

        for xnode in l_node:
            if self.node_list[xnode].node_type == 0:
                # NEED TO BE PROPER INTERSECTION JA ARRUMEI NA QUERY
                list_trap.append(self.node_list[xnode].info)
            else: 
                print("Achamos um node que não é trapézio")
                assert(0)

        lower_trap, lower_id = self.mergeDown(list_trap, segment)
        upper_trap, upper_id = self.mergeUp(list_trap, segment)

        # DEBUG
        '''
        for x in list_trap:
            x.blink("green")
            control.sleep()
            x.hide()       

        for x in lower_trap:
            x.blink()
            control.sleep()
            x.hide()

        for x in upper_trap:
            x.blink()
            control.sleep()
            x.hide()
        '''

        l_top = None
        l_bottom = None

        last_b = None
        last_c = None

        for i in range(len(lower_id)):
            node = self.node_list[l_node[i]]
            node.info.hide()
            t_top = upper_trap[upper_id[i]]
            t_bottom = lower_trap[lower_id[i]]
            if i == 0:
                # PARTE DA ESQUERDA
                at = self.node_list[l_node[0]].info

                if segment.p_left.x != at.p_left.x or segment.p_left.y != at.p_left.y:
                    t_left = copy.copy(at)
                    t_left.remove = 0
                    t_left.p_right = segment.p_left
                    t_left.t_upper_left = at.t_upper_left #1
                    t_left.t_lower_left = at.t_lower_left #1
                    t_left.t_upper_right = t_top #1
                    t_left.t_lower_right = t_bottom #1


                    t_left.pid = self.get_trapezoid()
                    t_left.blink()

                    # DEBUG
                    
                    print("Case 1 - LEFT")
                    self.relation_trap(t_left)
                    


                    self.trapezoid_list[t_left.pid] = t_left
                    exist_left = 1
                else:
                    exist_left = 0

                if exist_left == 1:
                    print("Entrei")
                    if at.t_upper_left != None:
                        if at.t_upper_left.t_upper_right == at:
                            at.t_upper_left.t_upper_right = t_left #1                       
                        if at.t_upper_left.t_lower_right == at:   
                            at.t_upper_left.t_lower_right = t_left #1 
                                                          
                    if at.t_lower_left != None:
                        if at.t_lower_left.t_upper_right == at:
                            at.t_lower_left.t_upper_right = t_left #1
                        if at.t_lower_left.t_lower_right == at:
                            at.t_lower_left.t_lower_right = t_left #1

                else:
                    if at.t_lower_left != at.t_upper_left:
                        if at.t_upper_left != None:
                            if t_top.s_top.p_left != segment.p_left or t_top.s_bottom.p_left != segment.p_left:
                                if at.t_upper_left.t_upper_right == at:
                                        at.t_upper_left.t_upper_right = t_top #1                      
                                if at.t_upper_left.t_lower_right == at:   
                                        at.t_upper_left.t_lower_right = t_top #1  
                            else:
                                if at.t_upper_left.t_upper_right == at:
                                        at.t_upper_left.t_upper_right = None #1                      
                                if at.t_upper_left.t_lower_right == at:   
                                        at.t_upper_left.t_lower_right = None #1                            
                                                              
                        if at.t_lower_left != None:
                            if t_bottom.s_bottom.p_left != segment.p_left or t_bottom.s_top.p_left != segment.p_left:
                                if at.t_lower_left.t_upper_right == at:
                                    at.t_lower_left.t_upper_right = t_bottom #1
                                if at.t_lower_left.t_lower_right == at:
                                    at.t_lower_left.t_lower_right = t_bottom #1
                            else:
                                if at.t_lower_left.t_upper_right == at:
                                    at.t_lower_left.t_upper_right = None #1
                                if at.t_lower_left.t_lower_right == at:
                                    at.t_lower_left.t_lower_right = None #1
                    else:
                        if at.t_upper_left != None and at.t_lower_left != None:
                            if (t_top.s_top.p_left != segment.p_left or t_top.s_bottom.p_left != segment.p_left) == False:
                                if at.t_lower_left.t_lower_right == at :
                                    at.t_lower_left.t_lower_right = t_bottom                    
                            elif (t_bottom.s_bottom.p_left != segment.p_left or t_bottom.s_top.p_left != segment.p_left) == False:
                                if at.t_upper_left.t_upper_right == at :
                                    at.t_upper_left.t_upper_right = t_top
                            else:
                                assert(0)                    


                if t_top != l_top:
                    # VIZINHOS
                    if exist_left == 1:
                        t_top.t_lower_left = t_left #1
                        t_top.t_upper_left = t_left #1
                        t_top.t_lower_right = None  #1
                        t_top.t_upper_right = None  #1
                    else:
                        if t_top.s_top.p_left != segment.p_left or t_top.s_bottom.p_left != segment.p_left:
                            t_top.t_lower_left = at.t_upper_left #1
                            t_top.t_upper_left = at.t_upper_left #1
                        else:
                            t_top.t_lower_left = None #1
                            t_top.t_upper_left = None #1
                        t_top.t_lower_right = None  #1
                        t_top.t_upper_right = None  #1                     

                    t_top.pid = self.get_trapezoid()
                    t_top.blink()
                    # DEBUG
                    
                    print("Case 1 - UPPER")
                    self.relation_trap(t_top)
                    

                    self.trapezoid_list[t_top.pid] = t_top


                if t_bottom != l_bottom:
                    # VIZINHOS
                    if exist_left == 1:
                        t_bottom.t_lower_left = t_left #1
                        t_bottom.t_upper_left = t_left #1
                        t_bottom.t_lower_right = None  #1
                        t_bottom.t_upper_right = None  #1
                    else:
                        if t_bottom.s_bottom.p_left != segment.p_left or t_bottom.s_top.p_left != segment.p_left:
                            t_bottom.t_lower_left = at.t_lower_left #1
                            t_bottom.t_upper_left = at.t_lower_left #1
                        else:
                            t_bottom.t_lower_left = None #1
                            t_bottom.t_upper_left = None #1                         
                        t_bottom.t_lower_right = None  #1
                        t_bottom.t_upper_right = None  #1                      
                    t_bottom.pid = self.get_trapezoid()
                    t_bottom.blink()
                    # DEBUG
                    
                    print("Case 1 - LOWER")
                    self.relation_trap(t_bottom)
                    


                    self.trapezoid_list[t_bottom.pid] = t_bottom


                    
                l_top = t_top
                l_bottom = t_bottom

                if exist_left == 0:
                    b = SNode(None, None, 0, t_top)
                    c = SNode(None, None, 0, t_bottom) 

                    last_b = b
                    last_c = c
                    id_b = self.add_node(b)
                    id_c = self.add_node(c)     
                    s = SNode(id_b, id_c, 1, segment);
                    self.node_list[node.pid] = s

                elif exist_left == 1:
                    a = SNode(None, None, 0, t_left)
                    b = SNode(None, None, 0, t_top)
                    c = SNode(None, None, 0, t_bottom) 

                    last_b = b
                    last_c = c
                    id_a = self.add_node(a)
                    id_b = self.add_node(b)
                    id_c = self.add_node(c)     
                    s = SNode(id_b, id_c, 1, segment);
                    id_s = self.add_node(s)
                    p = SNode(id_a, id_s, 2, segment.p_left)
                    self.node_list[node.pid] = p

            elif i == tot - 1:
                # PARTE DA DIREITA

                at = self.node_list[l_node[tot-1]].info
                if segment.p_right.x != at.p_right.x or segment.p_right.y != at.p_right.y:
                    t_right = copy.copy(at)
                    t_right.remove = 0
                    t_right.p_left = segment.p_right
                    t_right.pid = self.get_trapezoid()

                    t_right.t_upper_left = t_top #2
                    t_right.t_lower_left = t_bottom #2
                    t_right.t_upper_right = at.t_upper_right #2
                    t_right.t_lower_right = at.t_lower_right #2

                    t_right.blink()

                    # DEBUG
                    
                    print("Case 2 - RIGHT")
                    self.relation_trap(t_right)
                    

                    self.trapezoid_list[t_right.pid] = t_right
                    exist_right = 1 
                else:
                    exist_right = 0

                if exist_right == 1:
                    if at.t_upper_right != None:
                        if at.t_upper_right.t_upper_left == at:
                            at.t_upper_right.t_upper_left = t_right #2
   
                        if at.t_upper_right.t_lower_left == at:   
                            at.t_upper_right.t_lower_left = t_right #2                

                    if at.t_lower_right != None:
                        if at.t_lower_right.t_upper_left == at:
                            at.t_lower_right.t_upper_left = t_right #2  
                        if at.t_lower_right.t_lower_left == at:                                         
                            at.t_lower_right.t_lower_left = t_right #2
                else:
                    if at.t_upper_right != at.t_lower_right:
                        if at.t_upper_right != None:
                            if t_top.s_top.p_right != segment.p_right or t_top.s_bottom.p_right != segment.p_right:
                                if at.t_upper_right.t_upper_left == at:
                                    at.t_upper_right.t_upper_left = t_top #2
           
                                if at.t_upper_right.t_lower_left == at:   
                                    at.t_upper_right.t_lower_left = t_top #2      
                            else:
                                if at.t_upper_right.t_upper_left == at:
                                    at.t_upper_right.t_upper_left = None #2
                                if at.t_upper_right.t_lower_left == at:   
                                    at.t_upper_right.t_lower_left = None #2 

                        if at.t_lower_right != None:
                            if t_bottom.s_bottom.p_right != segment.p_right or t_bottom.s_top.p_right != segment.p_right:
                                if at.t_lower_right.t_upper_left == at:
                                    at.t_lower_right.t_upper_left = t_bottom #2  
                                if at.t_lower_right.t_lower_left == at:                                         
                                    at.t_lower_right.t_lower_left = t_bottom #2   
                            else:
                                if at.t_lower_right.t_upper_left == at:
                                    at.t_lower_right.t_upper_left = None #2  
                                if at.t_lower_right.t_lower_left == at:                                         
                                    at.t_lower_right.t_lower_left = None #2
                    else:
                        if at.t_upper_right != None and at.t_lower_right != None:
                            if (t_top.s_top.p_right != segment.p_right or t_top.s_bottom.p_right != segment.p_right) == False:
                                if at.t_lower_right.t_lower_left == at :
                                    at.t_lower_right.t_lower_left = t_bottom                    
                            elif (t_bottom.s_bottom.p_right != segment.p_right or t_bottom.s_top.p_right != segment.p_right) == False:
                                if at.t_upper_right.t_upper_left == at :
                                    at.t_upper_right.t_upper_left = t_top
                            else:
                                assert(0)                                           
                
                if exist_right == 1:
                    t_top.t_upper_right = t_right #2
                    t_top.t_lower_right = t_right #2
                else:
                    if t_top.s_top.p_right != segment.p_right or t_top.s_bottom.p_right != segment.p_right:
                        t_top.t_upper_right = at.t_upper_right #2
                        t_top.t_lower_right = at.t_upper_right #2  
                    else:
                        t_top.t_upper_right = None #2
                        t_top.t_lower_right = None #2                

                if t_top != l_top:
                    # VIZINHOS
                    self.update_relation(l_top, t_top)
                        
                    t_top.pid = self.get_trapezoid()
                    t_top.blink()

                    # DEBUG
                    
                    print("Case 2 - UPPER")
                    self.relation_trap(t_top)

                    

                    self.trapezoid_list[t_top.pid] = t_top

                    b = SNode(None, None, 0, t_top)
                    id_b = self.add_node(b)

                else:                 
                    b = last_b
                    id_b = b.pid

                    
                if exist_right == 1:
                    t_bottom.t_upper_right = t_right #2
                    t_bottom.t_lower_right = t_right #2
                else:
                    if t_bottom.s_bottom.p_right != segment.p_right or t_bottom.s_top.p_right != segment.p_right:
                        t_bottom.t_upper_right = at.t_lower_right #2
                        t_bottom.t_lower_right = at.t_lower_right #2
                    else:
                        t_bottom.t_upper_right = None #2
                        t_bottom.t_lower_right = None #2                       

                if t_bottom != l_bottom:
                    # VIZINHOS
                    self.update_relation(l_bottom, t_bottom)

                    t_bottom.pid = self.get_trapezoid()
                    t_bottom.blink()

                    # DEBUG
                    
                    print("Case 2 - LOWER")
                    self.relation_trap(t_bottom)
                    


                    self.trapezoid_list[t_bottom.pid] = t_bottom

                    c = SNode(None, None, 0, t_bottom)
                    id_c = self.add_node(c) 

                else:
                    c = last_c       
                    id_c = c.pid     

                if exist_right == 0:

                    s = SNode(id_b, id_c, 1, segment);
                    self.node_list[node.pid] = s                
                elif exist_right == 1:

                    a = SNode(None, None, 0, t_right)
                    id_a = self.add_node(a)
                    s = SNode(id_b, id_c, 1, segment);
                    id_s = self.add_node(s)
                    q = SNode(id_s, id_a, 2, segment.p_right)
                    self.node_list[node.pid] = q

            else:
                # PARTE INTERNA
                if t_top != l_top:
                    # VIZINHOS
                    self.update_relation(l_top, t_top)

                    t_top.t_upper_right = None #3
                    t_top.t_lower_right = None #3                                           


                    t_top.pid = self.get_trapezoid()
                    t_top.blink()
                    # DEBUG
                    
                    print("Case 3 - UPPER")
                    self.relation_trap(t_top)
                    
                
                    self.trapezoid_list[t_top.pid] = t_top

                    b = SNode(None, None, 0, t_top)
                    id_b = self.add_node(b)


                else:
                    b = last_b
                    id_b = b.pid

                if t_bottom != l_bottom:
                    # VIZINHOS
                    self.update_relation(l_bottom, t_bottom)

                    if l_bottom.right_comp.t_lower_right == t_bottom.left_comp :
                        l_bottom.t_lower_right = t_bottom #3
                    else:
                        l_bottom.t_lower_right = l_bottom.right_comp.t_lower_right # 3

                        if l_bottom.right_comp.t_lower_right != None:
                            if l_bottom.right_comp.t_lower_right.t_upper_left == l_bottom.right_comp:
                                l_bottom.right_comp.t_lower_right.t_upper_left = l_bottom
                            if l_bottom.right_comp.t_lower_right.t_lower_left == l_bottom.right_comp:
                                l_bottom.right_comp.t_lower_right.t_lower_left = l_bottom  

                    if l_bottom.right_comp.t_upper_right == t_bottom.left_comp :
                        l_bottom.t_upper_right = t_bottom #3
                    else:
                        l_bottom.t_upper_right = l_bottom.right_comp.t_upper_right # 3 
                        if l_bottom.right_comp.t_upper_right != None:
                            if l_bottom.right_comp.t_upper_right.t_upper_left == l_bottom.right_comp:
                                l_bottom.right_comp.t_upper_right.t_upper_left = l_bottom
                            if l_bottom.right_comp.t_upper_right.t_lower_left == l_bottom.right_comp:
                                l_bottom.right_comp.t_upper_right.t_lower_left = l_bottom  

                    if t_bottom.left_comp.t_lower_left == l_bottom.right_comp:
                        t_bottom.t_lower_left = l_bottom
                    else:
                        t_bottom.t_lower_left = t_bottom.left_comp.t_lower_left  
                        if t_bottom.left_comp.t_lower_left != None:
                            if t_bottom.left_comp.t_lower_left.t_upper_right == t_bottom.left_comp:
                                t_bottom.left_comp.t_lower_left.t_upper_right = t_bottom
                            if t_bottom.left_comp.t_lower_left.t_lower_right == t_bottom.left_comp:
                                t_bottom.left_comp.t_lower_left.t_lower_right = t_bottom

                    if t_bottom.left_comp.t_upper_left == l_bottom.right_comp:
                        t_bottom.t_upper_left = l_bottom
                    else:
                        t_bottom.t_upper_left = t_bottom.left_comp.t_upper_left
                        if t_bottom.left_comp.t_upper_left != None:
                            if t_bottom.left_comp.t_upper_left.t_upper_right == t_bottom.left_comp:
                                t_bottom.left_comp.t_upper_left.t_upper_right = t_bottom
                            if t_bottom.left_comp.t_upper_left.t_lower_right == t_bottom.left_comp:
                                t_bottom.left_comp.t_upper_left.t_lower_right = t_bottom


                    t_bottom.t_upper_right = None #3
                    t_bottom.t_lower_right = None #3  

                    t_bottom.pid = self.get_trapezoid()
                    t_bottom.blink()
        
                    # DEBUG
                    print("Case 3 - LOWER")
                    self.relation_trap(t_bottom)

                    self.trapezoid_list[t_bottom.pid] = t_bottom

                    c = SNode(None, None, 0, t_bottom) 
                    id_c = self.add_node(c)
 
                else:
                    c = last_c
                    id_c = c.pid

                l_top = t_top
                l_bottom = t_bottom

                last_b = b
                last_c = c


                s = SNode(id_b, id_c, 1, segment);
                id_s = self.add_node(s)
                self.node_list[node.pid] = s
        
        for x in list_trap:

            self.rmv_trapezoid(x)

    # Para debugar as relacoes dos trapezios
    def relation_trap(self, trap):
        '''
        print("Testando trapezio original")
        trap.blink("green")
        control.sleep()

        print("Testando sua esquerda superior")
        if trap.t_upper_left != None:
            trap.t_upper_left.blink("green")
            trap.t_upper_left.hide()
            control.sleep()
 
        print("Testando sua esquerda inferior")
        if trap.t_lower_left != None:
            trap.t_lower_left.blink("green")
            trap.t_lower_left.hide()
            control.sleep()

        print("Testando sua direita superior")
        if trap.t_upper_right != None:
            trap.t_upper_right.blink("green")
            trap.t_upper_right.hide()
            control.sleep()
 
        print("Testando sua direita inferior")
        if trap.t_lower_right != None:
            trap.t_lower_right.blink("green")
            trap.t_lower_right.hide()
            control.sleep()
        trap.hide()
        '''

    def mergeDown(self, list_trap, seg):
        new_traps = []
        new_traps_id = []
        left_ext = seg.p_left
        last_seg = None
        current_trap = STrapezoid(left_ext, None, seg, None)
        cnt = 0
        cnt2 = 0
        for trap in list_trap:
            if last_seg == None:
                last_seg = trap.s_bottom
                #AUXILIAR
                current_trap.left_comp = trap
                current_trap.right_comp = trap
            else:
                if last_seg == trap.s_bottom:
                    cnt = cnt + 1
                    #AUXILIAR
                    current_trap.right_comp = trap
                    continue
                else:
                    # MODIFY
                    current_trap.s_bottom = last_seg
                    current_trap.p_right = trap.p_left
                    new_traps.append(current_trap)
                    while cnt > 0:
                        new_traps_id.append(cnt2)
                        cnt = cnt - 1
                    cnt2 = cnt2 + 1
                    last_seg = trap.s_bottom
                    left_ext = trap.p_left
                    current_trap = STrapezoid(left_ext, None, seg, None)
                    #AUXILIAR
                    current_trap.left_comp = trap
                    current_trap.right_comp = trap
            cnt = cnt + 1
        # MODIFY LAST SEG
        current_trap.s_bottom = last_seg
        current_trap.p_right = seg.p_right
        # AUXILIAR
        current_trap.right_comp = trap
        new_traps.append(current_trap)
        while cnt > 0:
            new_traps_id.append(cnt2)
            cnt = cnt - 1
        cnt2 = cnt2 + 1
        return new_traps, new_traps_id

    def mergeUp(self,list_trap, seg):
        new_traps = []
        new_traps_id = []
        left_ext = seg.p_left
        last_seg = None
        current_trap = STrapezoid(left_ext, None, None, seg)
        cnt = 0
        cnt2 = 0
        for trap in list_trap:
            if last_seg == None:
                last_seg = trap.s_top
                #AUXILIAR
                current_trap.left_comp = trap
                current_trap.right_comp = trap
            else:
                if last_seg == trap.s_top:
                    cnt = cnt + 1
                    #AUXILIAR
                    current_trap.right_comp = trap
                    continue
                else:
                    # MODIFY
                    current_trap.s_top = last_seg
                    current_trap.p_right = trap.p_left
                    new_traps.append(current_trap)
                    while cnt > 0:
                        new_traps_id.append(cnt2)
                        cnt = cnt - 1
                    cnt2 = cnt2 + 1
                    last_seg = trap.s_top
                    left_ext = trap.p_left
                    current_trap = STrapezoid(left_ext, None, None, seg)
                    #AUXILIAR
                    current_trap.left_comp = trap
                    current_trap.right_comp = trap
            cnt = cnt + 1

        # MODIFY LAST SEG
        current_trap.s_top = last_seg
        current_trap.p_right = seg.p_right
        # AUXILIAR
        current_trap.right_comp = trap
        new_traps.append(current_trap)
        while cnt > 0:
            new_traps_id.append(cnt2)
            cnt = cnt - 1
        cnt2 = cnt2 + 1
        return new_traps, new_traps_id

    def checking(self):
        for trap in self.trapezoid_list:
            if trap.remove == 0:  
                seg_top = trap.s_top

                if seg_top.swap == 1:
                    trap.hide()
                    if trap.t_lower_right != None:
                        if trap.t_lower_right.t_lower_left == trap:
                            trap.t_lower_right.t_lower_left = None
                        if trap.t_lower_right.t_upper_left == trap:
                            trap.t_lower_right.t_upper_left = None     
                    if trap.t_lower_left != None:      
                        if trap.t_lower_left.t_lower_right == trap:
                            trap.t_lower_left.t_lower_right = None
                        if trap.t_lower_left.t_upper_right == trap:
                            trap.t_lower_left.t_upper_right = None      
                    if trap.t_upper_right != None:            
                        if trap.t_upper_right.t_lower_left == trap:
                            trap.t_upper_right.t_lower_left = None
                        if trap.t_upper_right.t_upper_left == trap:
                            trap.t_upper_right.t_upper_left = None      
                    if trap.t_upper_left != None:     
                        if trap.t_upper_left.t_lower_right == trap:
                            trap.t_upper_left.t_lower_right = None
                        if trap.t_upper_left.t_upper_right == trap:
                            trap.t_upper_left.t_upper_right = None  
                    self.rmv_trapezoid(trap)

        '''
        for trap in self.trapezoid_list:
            if trap.remove == 0:
                trap.show("green")
                self.relation_trap(trap)
                '''
        
#FOR LATER
'''
    def make_graph(self):
        
        par = []
        for trap in self.trapezoid_list:
    
            val = trap.get_point()
            

            if trap.remove == 0:
                #trap.blink("orange");
                #print("trap.remove == 0" + str(trap.pid))
                #par.append((Point(0,0), val[0]))

                if (trap.t_lower_right != None and trap.t_upper_right != None):
                    if trap.t_lower_right.remove == 0 and trap.t_upper_right.remove == 0:

                        #trap.t_lower_right.debug()
                        #trap.t_upper_right.debug()
                        if (trap.t_lower_right == trap.t_upper_right):
                            if(val[3] != Point(1e9, 1e9)):
                                par.append((val[0], val[3]))
                                par.append((val[3], trap.t_lower_right.get_point()[0]))
                            else:
                                par.append((val[0], val[4]))
                                par.append((val[4], trap.t_lower_right.get_point()[0]))
                        else:
                            par.append((val[0], val[3]))
                            par.append((val[3], trap.t_lower_right.get_point()[0]))
                            par.append((val[0], val[4]))
                            par.append((val[4], trap.t_upper_right.get_point()[0]))

                if (trap.t_lower_left != None and trap.t_upper_left != None):
                    if trap.t_lower_left.remove == 0 and trap.t_upper_left.remove == 0:
                        #trap.t_lower_left.debug()
                        #trap.t_upper_left.debug()
                        if (trap.t_lower_left == trap.t_upper_left):
                            if(val[1] != Point(1e9, 1e9)):
                                par.append((val[0], val[1]))
                                par.append((val[1], trap.t_lower_left.get_point()[0]))
                            else:
                                par.append((val[0], val[2]))
                                par.append((val[2], trap.t_lower_left.get_point()[0]))
                        else:
                            par.append((val[0], val[1]))
                            par.append((val[1], trap.t_lower_left.get_point()[0]))
                            par.append((val[0], val[2]))
                            par.append((val[2], trap.t_upper_left.get_point()[0]))                   
        return par
'''



