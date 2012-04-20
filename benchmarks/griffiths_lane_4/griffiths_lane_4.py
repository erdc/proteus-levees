#! /usr/bin/env python
import math
from proteus import Domain

def gl_4_3d(width,h=10.0,d=1.5):
    """
    A 3d levee profile for the sacramento levee modeling
    """
    boundaryLegend = {'left':1,
                      'right':2,
                      'front':3,
                      'back':4,
                      'bottom':5,
                      'top':6,
                      'inner':0}
    vertices_front = [[0.0,0.0,0.0],#0
                      [0.0,0.0,d*h-h],#1
                      [0.0,0.0,d*h],#2
                      [2.0*h,0.0,d*h],#3
                      [4.0*h,0.0,d*h-h],#4
                      [6.0*h,0.0,d*h-h],#5
                      [6.0*h,0.0,0.0]]#6
    vertexFlags_front = [boundaryLegend['left'],
                         boundaryLegend['left'],
                         boundaryLegend['left'],
                         boundaryLegend['top'],
                         boundaryLegend['top'],
                         boundaryLegend['right'],
                         boundaryLegend['right']]
    vertices_back = [[v[0],width,v[2]] for v in vertices_front]
    vertexFlags_back = vertexFlags_front
    vertices = vertices_front + vertices_back
    vertexFlags = vertexFlags_front + vertexFlags_back
    facets = [[[0,1,4,5,6]],#front 1
              [[1,2,3,4]],#front 2
              [[7,8,11,12,13]],#back 1
              [[8,9,10,11]],#back 2
              [[0,1,2,9,8,7]],#left
              [[6,5,12,13]],#right
              [[0,7,13,6]],#bottom
              [[2,9,10,3]],#top
              [[3,10,11,4]],#top
              [[4,11,12,5]],#top
              [[1,8,11,4]]]#inner
    facetFlags = [boundaryLegend['front'],
                  boundaryLegend['front'],
                  boundaryLegend['back'],
                  boundaryLegend['back'],
                  boundaryLegend['left'],
                  boundaryLegend['right'],
                  boundaryLegend['bottom'],
                  boundaryLegend['top'],
                  boundaryLegend['top'],
                  boundaryLegend['inner'],
                  boundaryLegend['top']]
    regions = [[h/2.0,width/2.0,h*3.0/2.0],[h/2.0,width/2.0,h/2.0]]
    regionFlags = [1,2]
    domain = Domain.PiecewiseLinearComplexDomain(vertices=vertices,
                                                 vertexFlags=vertexFlags,
                                                 facets=facets,
                                                 facetFlags=facetFlags,
                                                 regions=regions,
                                                 regionFlags=regionFlags)
    domain.boundaryFlags=boundaryLegend
    domain.regionLegend = {'u1':1,'u2':2,'default':0}
    return domain

if __name__=='__main__':
    import os
    domain =  gl_4_3d(width=10,h=10,d=1.5)
    domain.writeAsymptote("gl_4_3d")
    domain.writePoly("gl_4_3d")
    domain.writePLY("gl_4_3d")
    print domain.boundaryFlags
    #os.system("asy -V gl_4_3d")
    os.system("tetgen -KVApfen gl_4_3d.poly")
