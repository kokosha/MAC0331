import random

# ja tem tudo vamos colocar um o no final de tudo =(
class Pointo():
    def __init__ (self, x = None, y = None):
        self.x = x
        self.y = y

class Segmento():
    def __init__ (self, pstart = None, pend = None):
        self.pstart = pstart
        self.pend = pend

class Trapezoido():
    def __init__ (self, pleft = None, pright = None, stop = None, sbottom = None):
        self.pleft = pleft
        self.pright = pright
        self.stop = stop
        self.sbottom = sbottom

class Nodeo():
    def __init__ (self, left = None, right = None):
        self.left = left
        self.right = right


class TrapezoidoMapo():
    def __init__(self, segments):
        self.segments = segments
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

        stop = Segmento(Pointo(minX, maxY), Pointo(maxX, maxY))
        sbottom = Segmento(Pointo(minX, minY), Pointo(maxX, minY))
        pleft = Pointo(minX, maxY)
        pright = Pointo(maxX, maxY)
        trap = Trapezoido(pleft, pright, stop, sbottom);

        """ Random SHUFFLING """
        random.shuffle(segments)

        #for seg in segments:
            # findTrapezoid(seg)