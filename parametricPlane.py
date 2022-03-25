import numpy as np
from matrix import matrix
from parametricObject import parametricObject

#Made by: Jordan Avelar
#constructor params, width, height of plane
#getPoint creates matrix holding specific shape equations
class parametricPlane(parametricObject):

    def __init__(self,T=matrix(np.identity(4)),planeWidth=1.0,planeHeight=1.0,
                 color=(255,255,255),reflectance=(0.2,0.4,0.4,1.0),uRange=(0.0,1.0),
                 vRange=(0.0,1.0),uvDelta=(1.0/10.0,1.0/10.0)):
        super().__init__(T, color, reflectance, uRange, vRange, uvDelta)
        self.__width = planeWidth
        self.__height = planeHeight

    def getPoint(self, u, v):
        P = matrix(np.ones((4,1)))
        P.set(0, 0, self.__width*u)
        P.set(1, 0, self.__height*v)
        P.set(2, 0, 0)
        return P

    def setHeight(self, height):
        self.__height = height

    def setWidth(self, width):
        self.__width = width

    def getHeight(self):
        return self.__height

    def getWidth(self):
        return self.__width

