import operator
from math import *
import numpy as np
from matrix import matrix

class cameraMatrix:

    def __init__(self,window,UP,E,G,nearPlane=10.0,farPlane=50.0,theta=90.0):
        self.__UP = UP.normalize()
        self.__E = E
        self.__G = G
        self.__np = nearPlane
        self.__fp = farPlane
        self.__width = window.getWidth()
        self.__height = window.getHeight()
        self.__theta = theta
        self.__aspect = self.__width/self.__height
        self.__npHeight = self.__np*(pi/180.0*self.__theta/2.0)
        self.__npWidth = self.__npHeight*self.__aspect

        Mp = self.__setMp(self.__np,farPlane)
        T1 = self.__setT1(self.__np,self.__theta,self.__aspect)
        S1 = self.__setS1(self.__np,self.__theta,self.__aspect)
        T2 = self.__setT2()
        S2 = self.__setS2(self.__width,self.__height)
        W2 = self.__setW2(self.__height)

        self.__N = (self.__E - self.__G).removeRow(3).normalize()
        self.__U = self.__UP.removeRow(3).crossProduct(self.__N).normalize()
        self.__V = self.__N.crossProduct(self.__U)

        self.__Mv = self.__setMv(self.__U,self.__V,self.__N,self.__E)
        self.__C = W2*S2*T2*S1*T1*Mp
        self.__M = self.__C*self.__Mv

    #Made by: Jordan Avelar
    # setting up camera transformation matrix, with rotation and translation
    # U holds x values, V holds y values, N holds z values
    def __setMv(self,U,V,N,E):
        #create a 4x4 identity matrix
        __Mv = matrix(np.identity(4))

        #first row
        __Mv.set(0, 0, U.get(0, 0))
        __Mv.set(0, 1, U.get(1, 0))
        __Mv.set(0, 2, U.get(2, 0))
        #fourth column is summation of each value in e and its corrisponding UVN values
        __Mv.set(0, 3, -(E.get(0, 0) * U.get(0, 0) + E.get(1, 0) * U.get(1, 0) + E.get(2, 0) * U.get(2, 0)))
        #second row
        __Mv.set(1, 0, V.get(0, 0))
        __Mv.set(1, 1, V.get(1, 0))
        __Mv.set(1, 2, V.get(2, 0))
        __Mv.set(1, 3, -(E.get(0, 0) * V.get(0, 0) + E.get(1, 0) * V.get(1, 0) + E.get(2, 0) * V.get(2, 0)))
        #third row
        __Mv.set(2, 0, N.get(0, 0))
        __Mv.set(2, 1, N.get(1, 0))
        __Mv.set(2, 2, N.get(2, 0))
        __Mv.set(2, 3, -(E.get(0, 0) * N.get(0, 0) + E.get(1, 0) * N.get(1, 0) + E.get(2, 0) * N.get(2, 0)))
        #fourth row stays same (0,0,0,1)
        return __Mv

    #handle transforming a point based on the view plane
    #params: nearPlane and farPlane floats representing F and N
    def __setMp(self,nearPlane,farPlane):
        __Mp = matrix(np.identity(4))

        #set values
        __Mp.set(0, 0, nearPlane)
        __Mp.set(1, 1, nearPlane)
        __Mp.set(2, 2, -(nearPlane + farPlane) / (farPlane - nearPlane))
        __Mp.set(2, 3, -2 * (farPlane * nearPlane) / (farPlane - nearPlane))
        __Mp.set(3, 2, -1)
        __Mp.set(3, 3, 0)

        return __Mp

    #translation matrix setup
    #params nearPlane, theta, aspect
    def __setT1(self,nearPlane,theta,aspect):
        __T1 = matrix(np.identity(4))

        #set values
        __T1.set(0, 3, -((aspect * (nearPlane * tan(pi / 180.0 * theta / 2.0))) - (aspect * (nearPlane * tan(pi / 180.0 * theta / 2.0)))) / 2.0)
        __T1.set(1, 3, -((nearPlane * tan(pi / 180.0 * theta / 2.0)) - (nearPlane * tan(pi / 180.0 * theta / 2.0))) / 2.0)

        return __T1

    # scaling matrix setup
    #params same as translation
    def __setS1(self,nearPlane,theta,aspect):
        __S1 = matrix(np.identity(4))

        #set values
        __S1.set(0, 0, 2.0 / ((aspect * (nearPlane * tan(pi / 180.0 * theta / 2.0))) + (aspect * (nearPlane * tan(pi / 180.0 * theta / 2.0)))))
        __S1.set(1, 1, 2.0 / ((nearPlane * tan(pi / 180.0 * theta / 2.0)) + (nearPlane * tan(pi / 180.0 * theta / 2.0))))

        return __S1

    #positive translation matrix setup
    #params, just self
    def __setT2(self):
        __T2 = matrix(np.identity(4))

        #set values
        __T2.set(0, 3, 1.0)
        __T2.set(1, 3, 1.0)

        return __T2

    #scaling matrix to fit in the space defined by width and height
    #params, width and height of viewing plane
    def __setS2(self,width,height):
        __S2 = matrix(np.identity(4))

        #set values
        __S2.set(0, 0, width/2.0)
        __S2.set(1, 1, height/2.0)

        return __S2

    #transform to handle origin in top left corner rather than default bottom left
    #params, height for origin
    def __setW2(self,height):
        __W2 = matrix(np.identity(4))

        #set values
        __W2.set(1, 1, -1)
        __W2.set(1, 3, height)

        return __W2
        
    def worldToViewingCoordinates(self,P):
        return self.__Mv*P

    def worldToImageCoordinates(self,P):
        return self.__M*P

    def worldToPixelCoordinates(self,P):
        return self.__M*P.scalarMultiply(1.0/(self.__M*P).get(3,0))

    def viewingToImageCoordinates(self,P):
        return self.__C*P

    def viewingToPixelCoordinates(self,P):
        return self.__C*P.scalarMultiply(1.0/(self.__C*P).get(3,0))

    def imageToPixelCoordinates(self,P):
        return P.scalarMultiply(1.0/P.get(3,0))

    def getUP(self):
        return self.__UP

    def getU(self):
        return self.__U

    def getV(self):
        return self.__V

    def getN(self):
        return self.__N

    def getE(self):
        return self.__E

    def getG(self):
        return self.__G

    def getMv(self):
        return self.__Mv

    def getC(self):
        return self.__C

    def getM(self):
        return self.__M

    def getNp(self):
        return self.__np

    def getFp(self):
        return self.__fp

    def getTheta(self):
        return self.__theta

    def getAspect(self):
        return self.__aspect

    def getWidth(self):
        return self.__width

    def getHeight(self):
        return self.__height

    def getNpHeight(self):
        return self.__npHeight

    def getNpWidth(self):
        return self.__npWidth