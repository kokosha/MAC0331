import random

# ja tem tudo vamos colocar um o no final de tudo =(
class SPoint():
    def __init__ (self, x = None, y = None):
        self.x = x
        self.y = y

class SSegment():
    def __init__ (self, pstart = None, pend = None):
        self.pstart = pstart
        self.pend = pend

class STrapezoid():
    def __init__ (self, pleft = None, pright = None, stop = None, sbottom = None):
        self.pleft = pleft
        self.pright = pright
        self.stop = stop
        self.sbottom = sbottom

class SNode():
    def __init__ (self, left = None, right = None, node_type = None, info = None):
        self.left = left
        self.right = right
        # 0 - trapezio, 1 - segmento, 2 - ponto
        self.node_type = node_type
        self.info = info


class STrapezoidMap():
    def __init__(self, segments):
        self.segments = segments

        # Achando o trapezio externo
        minX = 1e9
        minY = 1e9
        maxX = -1e9
        maxY = -1e9
        for seg in segments :
            minX = min(minX, seg.pstart.x)
            minX = min(minX, seg.pend.x)

            minY = min(minY, seg.pstart.y)
            minY = min(minY, seg.pend.y)

            maxX = max(maxX, seg.pstart.x)
            maxX = max(maxX, seg.pend.x)

            maxY = max(maxY, seg.pstart.y)
            maxY = max(maxY, seg.pend.y)

        stop = SSegment(SPoint(minX, maxY), SPoint(maxX, maxY))
        sbottom = SSegment(SPoint(minX, minY), SPoint(maxX, minY))
        pleft = SPoint(minX, maxY)
        pright = SPoint(maxX, maxY)
        trapezoid = STrapezoid(pleft, pright, stop, sbottom);

        self.root = SNode(None, None, 0, trapezoid);

        random.shuffle(segments)
        for seg in segments:
            add(seg)

    def query():

    def add(segment):
    
    def simple_case(node, segment):
        # could be 2, 3, 4 trapezoid

    def hard_case(node, segment):
