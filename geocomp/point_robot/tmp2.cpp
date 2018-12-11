import random
import copy
from math import fabs
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

    def is_above(self, point):
        # NEED TO RECHECK
        return ccw(self.p_left, self.p_right, point) > 0    
    def is_below(self, point):
        # NEED TO RECHECK
        return ccw(self.p_left, self.p_right, point) < 0       

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

        self.linha1 = None
        self.linha2 = None
   
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


        return lista

    #def show_point(self, color):

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


        # FUTURE CORNER CASE BB = 0 -
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
        self.linha1.plot(color)



        linha2 = []
        linha2.append(Point(p_right.x, yt_right))
        linha2.append(Point(p_right.x, yb_right))   
        linha2.append(Point(p_right.x, yt_right))

        self.linha2 = Polygon(linha2)
        self.linha2.plot(color)



        linha3 = []
        linha3.append(Point(s_top.p_left.x, s_top.p_left.y))
        linha3.append(Point(s_top.p_right.x, s_top.p_right.y))
        linha3.append(Point(s_top.p_left.x, s_top.p_left.y))

        linha3 = Polygon(linha3)
        #linha3.plot("cyan")

        linha4 = []
        linha4.append(Point(s_bottom.p_left.x, s_bottom.p_left.y))
        linha4.append(Point(s_bottom.p_right.x, s_bottom.p_right.y))
        linha4.append(Point(s_bottom.p_left.x, s_bottom.p_left.y))
        linha4 = Polygon(linha4)
        #linha4.plot("cyan")

         
        control.sleep()
        #linha3.hide()
        #linha4.hide()

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
        self.print_control = []


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
        t_start = STrapezoid(p_left, p_right, s_top, s_bottom, 1)
        t_start.blink()

        # A estrutura de busca
        self.node_list = [SNode(None, None, 0, t_start, 0)]

        # Posicao de guardar
        self.trapezoid_list = [None, t_start]

        self.removed_node_list = []
        self.removed_trapezoid_list = []
 
    # Função que constroe o mapa trapezoidal
    def construct(self):
        segments = self.segments
        #random.shuffle(segments)
        val = 0
        for seg in segments:
            print("Segmento " + str(val) + " inserido!")
            seg.show("yellow")
            self.add(self.node_list[0], seg)
            seg.hide()
            seg.show("white")

            val = val + 1

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
        p_p = segment.p_left
        # TESTANDO PROPER INTERSECTION
        p_p.x = p_p.x + 1e-9
        p_q = segment.p_right
        p_q.x = p_q.x - 1e-9
        # Search with p and q in the search structure D to find D0.
        t_d0 = self.query(node, p_p)
        print("is removed " + str(t_d0.info.remove))
        print ("follow " + str(t_d0.info.pid))
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
            print("PID")
            #print(j.t_upper_right.pid, j.t_lower_right.pid)
            p_q.debug()
            j.p_right.debug()
            if segment.is_above(j.p_right):
                j = j.t_lower_right
            else:
                j = j.t_upper_right

            if j != None :
                t_list.append(j.tid)
                print("j " + str(j.pid))
                print("is removed " + str(j.remove))
                print ("debug " + str(self.node_list[j.tid].node_type));

        return t_list
    # Procura na DAG de decisão
    # NO BUG
    def query(self, at, p_p):
        while at.node_type != 0 :
            if at.node_type == 1:
                # checar cima e embaixo
                print("query")
                at.info.debug()
                p_p.debug()
                if(at.info.is_above(p_p)):
                    at = self.node_list[at.left]
                else:
                    at = self.node_list[at.right]
            else:
                # checar esquerda e direita
                print("query")
                at.info.debug()
                p_p.debug()
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
        print("REMOVI " + str(trap.pid));
        trap.remove = 1

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
                
            # FUTURO CORNER CASE
            t_left = copy.copy(node.info)
            t_left.remove = 0
            t_left.p_right = segment.p_left
            t_left.blink()
            t_left.pid = self.get_trapezoid()

            # FUTURO CORNER CASE
            t_right = copy.copy(node.info)
            t_right.remove = 0
            t_right.p_left = segment.p_right
            t_right.blink()
            t_right.pid = self.get_trapezoid()

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
                self.trapezoid_list[t.t_upper_left.pid].t_upper_right = t_left
                self.trapezoid_list[t.t_upper_left.pid].t_lower_right = t_left

            if t.t_lower_left != None :
                self.trapezoid_list[t.t_lower_left.pid].t_upper_right = t_left
                self.trapezoid_list[t.t_lower_left.pid].t_lower_right = t_left

            if t.t_upper_right != None :
                self.trapezoid_list[t.t_upper_right.pid].t_upper_left = t_right
                self.trapezoid_list[t.t_upper_right.pid].t_lower_left = t_right

            if t.t_lower_right != None :
                self.trapezoid_list[t.t_lower_right.pid].t_upper_left = t_right               
                self.trapezoid_list[t.t_lower_right.pid].t_lower_left = t_right

            self.trapezoid_list[t_left.pid] = t_left
            self.trapezoid_list[t_right.pid] = t_right
            self.trapezoid_list[t_bottom.pid] = t_bottom
            self.trapezoid_list[t_top.pid] = t_top     

            print ("PID")
            print ("LEFT " + str(t_left.pid) + " RIGHT "  + str(t_right.pid))
            print ("BOTTOM " + str(t_bottom.pid) + " TOP "  + str(t_top.pid))


            # Trecho 2 - Atualizar a estrutura de busca


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

            self.rmv_trapezoid(t)

    def hard_case(self, l_node, segment):
        # Parte 4
        # Trecho 1 - Atualizar o mapa trapezoidal

        # Os cantos sao aqueles que mudam

        print("Fazendo o Hard Case")
        tot = len(l_node)
        print("Tot " + str(tot))

        # Achando a lista de trapezioss
        list_trap = [] 
        

        for xnode in l_node:
            if self.node_list[xnode].node_type == 0:
                # NEED TO BE PROPER INTERSECTION
                print("xnode " + str(xnode))
                
                '''
                if self.node_list[xnode].info.p_right == segment.p_left:
                    continue
                if self.node_list[xnode].info.p_left ==  segment.p_right:
                    continue 

                    '''            
                list_trap.append(self.node_list[xnode].info)
            else: 
                print("Achamos um node que não é trapézio")
                assert(0)



        lower_trap, lower_id = self.mergeDown(list_trap, segment)
        upper_trap, upper_id = self.mergeUp(list_trap, segment)

        '''
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
            if i == 0:
                # PARTE DA ESQUERDA
                at = self.node_list[l_node[0]].info

                t_left = copy.copy(at)
                t_left.remove = 0
                t_left.p_right = segment.p_left
                t_left.t_upper_left = at.t_upper_left #1
                t_left.t_lower_left = at.t_lower_left #1
                t_left.t_upper_right = upper_trap[upper_id[i]]    #1
                t_left.t_lower_right = lower_trap[lower_id[i]] #1

                t_left.pid = self.get_trapezoid()
                t_left.blink()
                self.trapezoid_list[t_left.pid] = t_left


                if at.t_upper_left != None:
                    self.trapezoid_list[at.t_upper_left.pid].t_upper_right = t_left #1
                    self.trapezoid_list[at.t_upper_left.pid].t_lower_right = t_left #1                
                if at.t_lower_left != None:
                    self.trapezoid_list[at.t_lower_left.pid].t_upper_right = t_left #1
                    self.trapezoid_list[at.t_lower_left.pid].t_lower_right = t_left #1

 


                if upper_trap[upper_id[i]] != l_top:
                    # VIZINHOS
                    upper_trap[upper_id[i]].t_lower_left = t_left #1
                    upper_trap[upper_id[i]].t_upper_left = t_left #1
                    upper_trap[upper_id[i]].t_lower_right = None  #1
                    upper_trap[upper_id[i]].t_upper_right = None  #1

                    upper_trap[upper_id[i]].pid = self.get_trapezoid()
                    upper_trap[upper_id[i]].blink()
                    self.trapezoid_list[upper_trap[upper_id[i]].pid] = upper_trap[upper_id[i]]


                if lower_trap[lower_id[i]] != l_bottom:
                    # VIZINHOS
                    lower_trap[lower_id[i]].t_lower_left = t_left #1
                    lower_trap[lower_id[i]].t_upper_left = t_left #1
                    lower_trap[lower_id[i]].t_lower_right = None  #1
                    lower_trap[lower_id[i]].t_upper_right = None  #1
                    lower_trap[lower_id[i]].pid = self.get_trapezoid()
                    lower_trap[lower_id[i]].blink()
                    print("lower_id " + str(lower_trap[lower_id[i]].pid))
                    self.trapezoid_list[lower_trap[lower_id[i]].pid] = lower_trap[lower_id[i]]


                    
                l_top = upper_trap[upper_id[i]]
                l_bottom = lower_trap[lower_id[i]]

                a = SNode(None, None, 0, t_left)
                b = SNode(None, None, 0, upper_trap[upper_id[i]])
                c = SNode(None, None, 0, lower_trap[lower_id[i]]) 

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
                t_right = copy.copy(at)
                t_right.remove = 0
                t_right.p_left = segment.p_right
                t_right.pid = self.get_trapezoid()

                t_right.t_upper_left = upper_trap[upper_id[i]] #2
                t_right.t_lower_left = lower_trap[lower_id[i]] #2
                t_right.t_upper_right = at.t_upper_right #2
                t_right.t_lower_right = at.t_lower_right #2

                t_right.blink()

                self.trapezoid_list[t_right.pid] = t_right


                if at.t_upper_right != None:
                    self.trapezoid_list[at.t_upper_right.pid].t_upper_left = t_right #2
                    self.trapezoid_list[at.t_upper_right.pid].t_lower_left = t_right #2                

                if at.t_lower_right != None:
                    self.trapezoid_list[at.t_lower_right.pid].t_upper_left = t_right #2                    
                    self.trapezoid_list[at.t_lower_right.pid].t_lower_left = t_right #2
                

                upper_trap[upper_id[i]].t_upper_right = t_right #2
                upper_trap[upper_id[i]].t_lower_right = t_right #2

                if upper_trap[upper_id[i]] != l_top:
                     # VIZINHOS
                    self.trapezoid_list[l_top.pid].t_upper_right = upper_trap[upper_id[i]] #2
                    self.trapezoid_list[l_top.pid].t_lower_right = upper_trap[upper_id[i]] #2
                    upper_trap[upper_id[i]].t_upper_left = self.trapezoid_list[l_top.pid] #2
                    upper_trap[upper_id[i]].t_lower_left = self.trapezoid_list[l_top.pid] #2

                    upper_trap[upper_id[i]].pid = self.get_trapezoid()
                    upper_trap[upper_id[i]].blink()
                    self.trapezoid_list[upper_trap[upper_id[i]].pid] = upper_trap[upper_id[i]]

                    b = SNode(None, None, 0, upper_trap[upper_id[i]])
                    id_b = self.add_node(b)

                else:                 
                    b = last_b
                    id_b = b.pid

                    
            

                if lower_trap[lower_id[i]] != l_bottom:
                    # VIZINHOS
                    self.trapezoid_list[l_bottom.pid].t_upper_right = lower_trap[lower_id[i]] #2
                    self.trapezoid_list[l_bottom.pid].t_lower_right = lower_trap[lower_id[i]] #2
                    lower_trap[lower_id[i]].t_upper_left = self.trapezoid_list[l_bottom.pid] #2
                    lower_trap[lower_id[i]].t_lower_left = self.trapezoid_list[l_bottom.pid] #2  

                    lower_trap[lower_id[i]].pid = self.get_trapezoid()
                    lower_trap[lower_id[i]].blink()
                    self.trapezoid_list[lower_trap[lower_id[i]].pid] = lower_trap[lower_id[i]]

                    c = SNode(None, None, 0, lower_trap[lower_id[i]])
                    id_c = self.add_node(c) 

                else:
                    c = last_c       
                    id_c = c.pid     


                a = SNode(None, None, 0, t_right)


                id_a = self.add_node(a)
                s = SNode(id_b, id_c, 1, segment);
                id_s = self.add_node(s)
                q = SNode(id_s, id_a, 2, segment.p_right)
                self.node_list[node.pid] = q

            else:
                # PARTE INTERNA
                if upper_trap[upper_id[i]] != l_top:
                    # VIZINHOS
                    self.trapezoid_list[l_top.pid].t_upper_right = upper_trap[upper_id[i]] #3
                    self.trapezoid_list[l_top.pid].t_lower_right = upper_trap[upper_id[i]] #3
                    upper_trap[upper_id[i]].t_upper_left = self.trapezoid_list[l_top.pid] #3
                    upper_trap[upper_id[i]].t_lower_left = self.trapezoid_list[l_top.pid] #3
                    upper_trap[upper_id[i]].t_upper_right = None #3
                    upper_trap[upper_id[i]].t_lower_right = None #3


                    upper_trap[upper_id[i]].pid = self.get_trapezoid()
                    upper_trap[upper_id[i]].blink()
                    self.trapezoid_list[upper_trap[upper_id[i]].pid] = upper_trap[upper_id[i]]

                    b = SNode(None, None, 0, upper_trap[upper_id[i]])
                    id_b = self.add_node(b)


                else:
                    b = last_b
                    id_b = b.pid

                if lower_trap[lower_id[i]] != l_bottom:
                   # VIZINHOS
                    self.trapezoid_list[l_bottom.pid].t_upper_right = lower_trap[lower_id[i]] #3
                    self.trapezoid_list[l_bottom.pid].t_lower_right = lower_trap[lower_id[i]] #3
                    lower_trap[lower_id[i]].t_upper_left = self.trapezoid_list[l_bottom.pid] #3
                    lower_trap[lower_id[i]].t_lower_left = self.trapezoid_list[l_bottom.pid] #3
                    lower_trap[lower_id[i]].t_upper_right = None #3
                    lower_trap[lower_id[i]].t_lower_right = None #3

                    lower_trap[lower_id[i]].pid = self.get_trapezoid()
                    lower_trap[lower_id[i]].blink()
                    self.trapezoid_list[lower_trap[lower_id[i]].pid] = lower_trap[lower_id[i]]

                    c = SNode(None, None, 0, lower_trap[lower_id[i]]) 
                    id_c = self.add_node(c)
 
                else:
                    c = last_c
                    id_c = c.pid

                l_top = upper_trap[upper_id[i]]
                l_bottom = lower_trap[lower_id[i]]

                last_b = b
                last_c = c


                s = SNode(id_b, id_c, 1, segment);
                id_s = self.add_node(s)
                self.node_list[node.pid] = s
        
        for x in list_trap:

            self.rmv_trapezoid(x)

    # INVARIANTE ERRADA...
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
            else:
                if last_seg == trap.s_bottom:
                    cnt = cnt + 1
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
            cnt = cnt + 1
        # MODIFY LAST SEG
        current_trap.s_bottom = last_seg
        current_trap.p_right = seg.p_right
        new_traps.append(current_trap)
        while cnt > 0:
            new_traps_id.append(cnt2)
            cnt = cnt - 1
        cnt2 = cnt2 + 1
        print("cnt "+ str(cnt2))
        return new_traps, new_traps_id

    # APARENTEMENTE CERTO
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
            else:
                if last_seg == trap.s_top:
                    cnt = cnt + 1
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
            cnt = cnt + 1

        # MODIFY LAST SEG
        current_trap.s_top = last_seg
        current_trap.p_right = seg.p_right
        new_traps.append(current_trap)
        while cnt > 0:
            new_traps_id.append(cnt2)
            cnt = cnt - 1
        cnt2 = cnt2 + 1
        print("cnt "+ str(cnt2))      
        return new_traps, new_traps_id
#FOR LATER
'''
    def make_graph(self):
        
        par = []
        for trap in self.trapezoid_list:
 


            val = trap.get_point()
            

            if trap.remove == 0:
                trap.blink("orange");
                print("trap.remove == 0" + str(trap.pid))
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

    def checking(self):
        for trap in self.trapezoid_list:

            if trap.remove == 0:  
                val = trap.get_point()
                seg_top = trap.s_top
                seg_bot = trap.s_bottom

                skip = 0
                if(seg_top.swap == 2):
                    x1 = seg_top.p_right
                    y1 = seg_top.p_left
                    skip = 1
                elif(seg_top.swap == 1):
                    x1 = seg_top.p_right
                    y1 = seg_top.p_left
                else:
                    x1 = seg_top.p_left
                    y1 = seg_top.p_right           
                n_seg_top = SSegment(x1, y1)

                if(seg_bot.swap == 2):
                    x2 = seg_top.p_right
                    y2 = seg_top.p_left
                    skip = 1
                elif(seg_bot.swap == 1):
                    x2 = seg_bot.p_right
                    y2 = seg_bot.p_left
                else:
                    x2 = seg_top.p_left
                    y2 = seg_top.p_right   
                
                n_seg_bot = SSegment(x2, y2)

                n_p = SPoint(val[0].x, val[0].y)
                # direction from x to y
                if skip == 1:
                    continue
                trap.blink("white");
                if(n_seg_top.is_above(n_p) == False or n_seg_bot.is_above(n_p) == False):
                    self.rmv_trapezoid(trap) 

'''
