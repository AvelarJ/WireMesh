from math import *
import numpy as np
from matrix import matrix
from parametricObject import parametricObject

#Made by: Jordan Avelar
#constructor params, radius and height of cone
#getPoint creates matrix holding specific shape equations
class parametricCone(parametricObject):

    def __init__(self, T=matrix(np.identity(4)), height=10.0, radius=10.0, color=(255, 255, 255),
                 reflectance=(0.2, 0.4, 0.4, 1.0), uRange=(0.0, 1), vRange=(0.0, 2.0 * pi),
                 uvDelta=(pi / 18.0, pi / 18.0)):
        super().__init__(T, color, reflectance, uRange, vRange, uvDelta)
        self.__radius = radius
        self.__height = height

    def getPoint(self, u, v):
        P = matrix(np.ones((4, 1)))
        P.set(0, 0, ((self.__height*(1-u))/self.__height) * self.__radius * sin(v))
        P.set(1, 0, ((self.__height*(1-u))/self.__height) * self.__radius * cos(v))
        P.set(2, 0, self.__height * u)
        return P

    def setRadius(self, radius):
        self.__radius = radius

    def setHeight(self, height):
        self.__height = height

    def getRadius(self):
        return self.__radius

    def getHeight(self):
        return self.__height
