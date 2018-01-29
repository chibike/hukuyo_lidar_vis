#!/usr/bin/env python
import math
import numpy as np
import matplotlib.pyplot as plt

def sinf(x):
    return math.sin(math.radians(x))

def cosf(x):
    return math.cos(math.radians(x))

def tanf(x):
    return math.tan(math.radians(x))

def asinf(x):
    return math.degrees(math.asin(x))

def acosf(x):
    return math.degrees(math.acos(x))

def atanf(x):
    return math.degrees(math.atan(x))

def get_distance_bwt_points(point_1, point_2):
    distance = math.sqrt(pow(point_2.x - point_1.x, 2) + pow(point_2.y - point_1.y, 2))
    return distance

def plot(title, x, y):
    plt.title(title)
    plt.plot(x, y)
    plt.grid()
    plt.show()

def rotate_about_the_origin(point, angle):
    x = round((point.x*cosf(angle)) - (point.y*sinf(angle)), 3)
    y = round((point.y*cosf(angle)) + (point.x*sinf(angle)), 3)
    return Point(x, y)

def get_shaded_rect(rect_coord, num_of_lines, angle):
    x,y,width,height = rect_coord
    foo = np.linspace(x,x+width,2+num_of_lines)
    lines = []
    for index,p in enumerate(foo):
        top_vertex = Point(p,y)
        bottom_vertex = Point(p,y+height)
        print "{0} -> {1}".format(top_vertex.point, bottom_vertex.point)
        line = Line(top_vertex, bottom_vertex)
        #lines.append(line)
        
##    for line in lines:
##        line.rotate(angle)
##    return lines


class Infinity(object):
    def __init__(self, sign=1.0):
        self.sign = str(sign/abs(sign))[0]
        if self.sign.startswith('1'):
            self.sign = '+'
        else:
            self.sign = '-'

    def __add__(self, other):
        if isinstance(other, type(self)):
            if self.sign == other.sign: return self
            else: return 0.0
        else:
            return self

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, type(self)):
            if self.sign == other.sign: return 0.0
            elif self.sign.startswith('-'): return self
            else: return Infinity(1.0)
        else:
            return self

    def __rsub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        if isinstance(other, type(self)):
            if self.sign == other.sign: return Infinity(1.0)
            else: return Infinity(-1.0)
        else:
            if other == 0: return 0
            else: return self

    def __rmul__(self, other):
        return self.__mul__(other)

    def __div__(self, other):
        if isinstance(other, type(self)):
            if self.sign == other.sign: return 1.0
            else: return -1.0
        else:
            if other == 0: return 0
            else: return self

    def __rdiv__(self, other):
        return self.__div__(other)

    def __abs__(self):
        return Infinity(1.0)

    def __float__(self):
        return self

    def __neg__(self):
        if self.sign.startswith('-'):
            return Infinity(1.0)
        else:
            return Infinity(-1.0)

    def __pos__(self):
        return self

    def __lt__(self, other):
        if isinstance(other, type(self)):
            if self.sign == other.sign: return False
            elif self.sign == '+': return True
            else: return False
        else:
            return self.sign.startswith('+')

    def ___le__(self, other):
        if isinstance(other, type(self)):
            if self.sign == other.sign: return True
            elif self.sign == '+': return True
            else: return False
        else:
            return self.sign.startswith('+')

    def __eq__(self, other):
        if isinstance(other, type(self)):
            if self.sign == other.sign: return True
            else: return False
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return not self.__le__()

    def __ge__(self, other):
        return not self.__lt__()

    def print_self(self):
        print "{0}Inf".format(self.sign)

class Undefined(object):
    def __init__(self):
        pass

    def __add__(self, other):
        return self

    def __sub__(self, other):
        return self

    def __mul__(self, other):
        if other == 0: return 0.0
        else: return self

    def __div__(self, other):
        if isinstance(other, type(self)): return 1.0
        else: return self

    def __abs__(self):
        return self

    def __float__(self):
        return self

    def __neg__(self):
        return self

    def __pos__(self):
        return self

    def __lt__(self, other):
        return self

    def ___le__(self, other):
        return self

    def __eq__(self, other):
        return self

    def __ne__(self, other):
        return self

    def __gt__(self, other):
        return self

    def __ge__(self, other):
        return self

    def print_self(self):
        print "Undefined"


def get_intersecting_point(l1, l2):
    def _det(x):
        '''returns the determinant of x'''
        return np.linalg.det(x)
    
    #Line 01
    x1 = l1.start.x; x2 = l1.end.x
    y1 = l1.start.y; y2 = l1.end.y

    #Line 02
    x3 = l2.start.x; x4 = l2.end.x
    y3 = l2.start.y; y4 = l2.end.y
    
    a = np.array([[x1, y1], [x2, y2]])
    b = np.array([[x1,  1], [x2,  1]])
    c = np.array([[x3, y3], [x4, y4]])
    d = np.array([[x3,  1], [x4,  1]])
    e = np.array([[y1,  1], [y2,  1]])
    f = np.array([[y3,  1], [y4,  1]])

    A = np.array([[_det(a), _det(b)], [_det(c), _det(d)]])
    B = np.array([[_det(b), _det(e)], [_det(d), _det(f)]])

    x = _det(A)/_det(B)

    C = np.array([[_det(a), _det(e)], [_det(c), _det(f)]])

    y = _det(C)/_det(B)

    return Point(x,y)
