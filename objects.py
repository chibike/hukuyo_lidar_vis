#!/usr/bin/env python

import cv2
import math
import numpy as np
import rect_arithmetic
import matplotlib.pyplot as plt
from rect_arithmetic import Infinity
from rect_arithmetic import Undefined

#p = [Point(0, 0), Point(0, 3), Point(1,4), Point(3,4), Point(5,2)];[i.point for i in filter_points(p, 50)]

def get_corners(points):
    corners = []
    for index in range(len(points)-2):
        l1 = Line(points[index], points[index+1])
        l2 = Line(points[index+1], points[index+2])
        corners.append( (points[index+1], compare_lines(l1, l2)) )
    return corners

def get_similar():
    pass
        

def filter_points(points, threshold):
    filtered_points = []

    index = 0
    while index < len(points)-1:
        current_point = points[index]; next_point = points[index+1]
        filtered_points.append(current_point)
        current_line = Line(current_point, next_point)
        index += 1
        for i in range(index+1, len(points)):
            line = Line(current_point, points[i])
            if compare_lines(current_line, line) > threshold:
                break
            else:
                index = i
    return filtered_points

def plot_points(points):
    lines = []
    for i in range(len(points)-1):
        line = Line(points[i], points[i+1])
        lines.append( line )
        line.plot()
    return lines
        

def compare_lines(l1, l2):
    m1 = l1.get_angle()
    m2 = l2.get_angle()
    return abs(m1 - m2)

def get_closest_point(point, points):
    min_point = points[0]
    min_dist = get_distance_bwt_points(point, min_point)

    for index in range(len(points)):
        dist = get_distance_bwt_points(point, points[index])
        if dist < min_dist:
            min_dist = dist
            min_point = points[index]
    return {"min_dist":min_dist, "min_point":min_point, "points":points[0:min_index]+points[min_index+1:]}
    
def rearrange_points_by_distance(points):
    new_points_buffer = []
    points_buffer = points
    for i in range(len(points)):
        data = get_closest_point(points[i], points_buffer)
        points_buffer = data["points"]
        new_points_buffer.append(data["min_point"])

class Path(object):
    def __init__(self, raw_point_data, stroke_color=(0,255,255), fill_color=(0,255,255), thickness=1, linetype=cv2.LINE_8, closed=False):
        self.raw_point_data = raw_point_data
        self.xs,self.ys = zip(*self.raw_point_data)

        self.points = list()
        for data in self.raw_point_data:
            self.points.append(Point(data[0], data[1]))

        #Attributes
        self.stroke_color = stroke_color
        self.fill_color = fill_color
        self.thickness = thickness
        self.linetype = linetype
        self.closed = closed

    def getStartPoint(self):
        return (self.xs[0], self.ys[0])

    def getEndPoint(self):
        return (max(self.xs), max(self.ys))

    def getRectInfo(self):
        top_left_corner = (min(self.xs), min(self.ys))
        width = max(self.xs) - top_left_corner[0]
        height = max(self.ys) - top_left_corner[1]
        bottom_right_corner = (top_left_corner[0]+width, top_left_corner[1]+height)
        area = float(width * height)
        return {"top_left_corner":top_left_corner,"height":height,"width":width,"area":area,"bottom_right_corner":bottom_right_corner}

    def getCircleInfo(self):
        top_left_corner = (min(self.xs), min(self.ys))
        width = max(self.xs) - top_left_corner[0]
        height = max(self.ys) - top_left_corner[1]
        center_origin = (top_left_corner[0]+int(width/2.0), top_left_corner[1]+int(height/2.0))
        bottom_right_corner = (top_left_corner[0]+width, top_left_corner[1]+height)
        radius = (width/2.0)**2 + (height/2.0)**2
        area = 2.0*math.pi*(radius**2.0)
        return {"bottom_right_corner":bottom_right_corner, "center_origin":center_origin, "top_left_corner":top_left_corner,"height":height,"width":width,"radius":radius,"area":area}

    def drawAsRect(self, image, fill=False):
        rect_info = self.getRectInfo()
        image = cv2.rectangle(
            image,
            rect_info['top_left_corner'],
            rect_info['bottom_right_corner'],
            self.stroke_color,
            self.thickness,
            self.linetype
            )
        return image

    def drawAsCircle(self, image, fill=False):
        circle_info = self.getCircleInfo()
        image = cv2.circle(
            image,
            circle_info['center_origin'],
            int(circle_info['radius']),
            self.stroke_color,
            self.thickness,
            int(self.linetype)
        )
        return image

    def drawAsPath(self, image, fill=False):
        vertices = np.array(self.raw_point_data, np.int32)
        vertices = vertices.reshape((-1,1,2))
        image = cv2.polylines(image, [vertices], self.closed, self.stroke_color, self.thickness, self.linetype)
        return image

    def drawAsPathWithBoundaries(self, image, fill=False):
        image = self.drawAsRect(image, fill)
        image = self.drawTerminals(image, 10)
        return self.drawAsPath(image, fill)

    def drawTerminals(self, image, radius=2):
        red = (255, 0, 0)
        green = (0, 255, 0)

        # Draw start
        image = cv2.circle(
            image,
            self.getStartPoint(),
            radius,
            red,
            self.thickness,
            int(self.linetype)
        )

        # Draw end
        image = cv2.circle(
            image,
            self.getEndPoint(),
            radius+1,
            green,
            self.thickness,
            int(self.linetype)
        )

        return image

    def getPath(self):
        return self.points

    def calculateDirection(self):
        line = Line(self.points[0], self.points[-1])
        m = -1/line.get_gradient()
        print m
        #return rect_arithmetic.atanf(m)

    def plot(self, title="Path-01", flip=True):
        plt.title(title)
        plt.grid()
        #Flip y axis for graph : because img starts with 0 up
        if flip:
            plt.plot(self.xs, [max(self.ys)-y for y in self.ys])
        else:
            plt.plot(self.xs, ys)

class Point(object):
    def __init__(self, x, y):
        if not (isinstance(x, Infinity) or isinstance(x, Undefined)):
            self.x = float(x)
        else:
            self.x = x

        if not (isinstance(x, Infinity) or isinstance(x, Undefined)):
            self.y = float(y)
        else:
            self.y = y

        self.r = math.sqrt(pow(x,2)+pow(y,2))
        if x == 0:
            if y > 0:
                self.theta = 90.0 
            elif y < 0:
                self.theta = 270.0
            else:
                self.theta = 0.0
        else:
            self.theta = rect_arithmetic.atanf(y/x)

        self.point = (self.x,self.y)
        self.point_polar = (self.r,self.theta)

    def __add__(self, other):
        if isinstance(other, tuple) and 2 == len(other):
            other = Point(other[0], other[1])
        elif not isinstance(other, type(self)):
            raise ValueError("Invalid type {0} for other".format(type(other)))

        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if isinstance(other, tuple) and 2 == len(other):
            other = Point(other[0], other[1])
        elif not isinstance(other, type(self)):
            raise ValueError("Invalid type {0} for other".format(type(other)))

        return Point(self.x - other.x, self.y - other.y)
    
    def add(self, other):
        self.x += other.x
        self.y += other.y
        self.point = (self.x,self.y)
        return self

    def sub(self, other):
        self.x -= other.x
        self.y -= other.y
        self.point = (self.x,self.y)
        return self

    def getAsPolar(self):
        return (self.r, self.theta)

class Line(object):
    def __init__(self, point1, point2):
        self.start = point1
        self.end = point2

        self.compute()

    def compute(self):
        self.line = (self.start, self.end)
        self.m = self.get_gradient()
        self.ref_point = self.start
        self.length = self.get_length()
        self.angle = self.get_angle()

    def rotate(self, angle):
        #rotate start point about midpoint
        midpoint = self.get_midpoint()
        point = self.start - midpoint
        x = round((point.x*rect_arithmetic.cosf(angle)) - (point.y*rect_arithmetic.sinf(angle)), 5)
        y = round((point.y*rect_arithmetic.cosf(angle)) + (point.x*rect_arithmetic.sinf(angle)), 5)

        #move back to midpoint
        self.start = Point(x, y) + midpoint

        #recalculate end point
        self.end = Point(((2.0*midpoint.x) - self.start.x), ((2.0*midpoint.y) - self.start.y))

        self.compute()

    def get_length(self):
        return rect_arithmetic.get_distance_bwt_points(self.start, self.end)

    def get_gradient(self):
        try:
            return float(self.end.y - self.start.y)/float(self.end.x - self.start.x)
        except ZeroDivisionError:
            if self.end.y - self.start.y > 0:
                return Infinity(1.0)
            else:
                return Infinity(-1.0)

    def get_angle(self):
        if isinstance(self.get_gradient(), Infinity):
            angle = 90.0
        else:
            angle = rect_arithmetic.atanf(self.get_gradient())
        return angle

    def get_midpoint(self):
        midpoint = Point( (self.start.x+self.end.x)/2.0, (self.start.y+self.end.y)/2.0 )
        return midpoint

    def plot(self, title="Line-01"):
        plt.title(title)
        plt.grid()
        xs = [self.start.x, self.end.x]
        ys = [self.start.y, self.end.y]
        plt.plot(xs, ys)

    def is_on_line(self, point):
        self.compute()
        x,y = point.point
        x1,y1 = self.ref_point.point
        eqn = (self.m*(x-x1)) - (y-y1)
        return eqn == 0

    def get_intersecting_point(self, other):
        def _det(x):
            '''returns the determinant of x'''
            return np.linalg.det(x)
    
        #Line 01
        x1 = self.start.x; x2 = self.end.x
        y1 = self.start.y; y2 = self.end.y

        #Line 02
        x3 = other.start.x; x4 = other.end.x
        y3 = other.start.y; y4 = other.end.y
        
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
    
