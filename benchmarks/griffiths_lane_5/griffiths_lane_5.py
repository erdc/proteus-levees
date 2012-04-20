#! /usr/bin/env python
import math
from proteus import Domain

def gl_5_3d(width,h):
    """
    A 3d levee profile for the sacramento levee modeling
    """
    boundaryLegend = {'left':1,
                      'right':2,
                      'front':3,
                      'back':4,
                      'bottom':5,
                      'top':6}
    vertices_front = [[0.0,0.0,0.0],#0
                      [0.0,0.0,h],#1
                      [1.2*h,0.0,h],#2
                      [3.2*h,0.0,0.0]]#3
    vertexFlags_front = [boundaryLegend['left'],
                         boundaryLegend['left'],
                         boundaryLegend['top'],
                         boundaryLegend['top']]
    vertices_back = [[v[0],width,v[2]] for v in vertices_front]
    vertexFlags_back = vertexFlags_front
    vertices = vertices_front + vertices_back
    vertexFlags = vertexFlags_front + vertexFlags_back
    facets = [[[0,1,2,3]],#front
              [[4,5,6,7]],#back
              [[0,1,5,4]],#left
              [[3,2,6,7]],#right
              [[0,4,7,3]],#bottom
              [[1,5,6,2]]]#top
    facetFlags = [boundaryLegend['front'],
                  boundaryLegend['back'],
                  boundaryLegend['left'],
                  boundaryLegend['top'],
                  boundaryLegend['bottom'],
                  boundaryLegend['top']]
    regions = [[h,width/2.0,h]]
    regionFlags = [1]
    print vertices,vertexFlags,facets,facetFlags,regions,regionFlags
    domain = Domain.PiecewiseLinearComplexDomain(vertices=vertices,
                                                 vertexFlags=vertexFlags,
                                                 facets=facets,
                                                 facetFlags=facetFlags,
                                                 regions=regions,
                                                 regionFlags=regionFlags)
    domain.boundaryFlags=boundaryLegend
    domain.regionLegend = {'levee':1,'default':0}
    return domain

if __name__=='__main__':
    import os
    domain =  gl_5_3d(5.0,5.0)
    domain.writeAsymptote("gl_5_3d")
    domain.writePoly("gl_5_3d")
    domain.writePLY("gl_5_3d")
    print domain.boundaryFlags
    #os.system("asy -V gl_5_3d")
    os.system("tetgen -KVApfen gl_5_3d.poly")
