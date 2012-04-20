#! /usr/bin/env python
import math
from proteus import Domain

def gl_3_3d(width,h=10.0):
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
                      [0.0,0.0,h],#1
                      [0.0,0.0,2*h],#2
                      [0.6*h,0.0,2*h],#3
                      [0.8*h,0.0,2*h],#4
                      [2.0*h,0.0,2*h],#5
                      [4.0*h,0.0,h],#6
                      [5.2*h,0.0,h],#7
                      [5.4*h,0.0,h],#8
                      [6.0*h,0.0,h],#9
                      [6.0*h,0.0,0],#10
                      [0.8*h + 2*(2*h-0.6*h),0.0,0.6*h],#11
                      [5.2*h - 0.4*h,0.0,0.6*h],#12
                      [5.2*h - 0.4*h,0.0,0.4*h],#13
                      [0.6*h + 2.0*(2.0*h - 0.4*h),0.0,0.4*h]]#14
    vertexFlags_front = [boundaryLegend['left'],
                         boundaryLegend['left'],
                         boundaryLegend['left'],
                         boundaryLegend['top'],
                         boundaryLegend['top'],
                         boundaryLegend['top'],
                         boundaryLegend['top'],
                         boundaryLegend['top'],
                         boundaryLegend['top'],
                         boundaryLegend['right'],
                         boundaryLegend['right'],
                         boundaryLegend['inner'],
                         boundaryLegend['inner'],
                         boundaryLegend['inner'],
                         boundaryLegend['inner']]
    vertices_back = [[v[0],width,v[2]] for v in vertices_front]
    vertexFlags_back = vertexFlags_front
    vertices = vertices_front + vertices_back
    vertexFlags = vertexFlags_front + vertexFlags_back
    facets = [[[0,1,2,3,14,13,8,9,10]],#front 1 
              [[3,4,11,12,7,8,13,14]],#front 2 
              [[4,5,6,7,12,11]],#front 3 
              [[15,16,17,18,29,28,23,24,25]],#back 1
              [[18,19,26,27,22,23,28,29]],#back 2
              [[19,20,21,22,27,26]],#back 3
              [[0,1,2,17,16,15]],#left
              [[10,9,24,25]],#right
              [[0,15,25,10]],#bottom
              [[2,17,18,3]],#top 1
              [[3,18,19,4]],#top 2
              [[4,19,20,5]],#top 3
              [[5,20,21,6]],#top 4
              [[6,21,22,7]],#top 5
              [[7,22,23,8]],#top 6
              [[8,23,24,9]],#top 7
              [[3,18,29,14]],#innner left
              [[4,19,26,11]],#innner right
              [[11,26,27,12]],#inner top
              [[14,29,28,13]],#inner bottom
              [[12,27,22,7]],#inner left top
              [[13,28,23,8]]]#inner right bottom
    facetFlags = [boundaryLegend['front'],
                  boundaryLegend['front'],
                  boundaryLegend['front'],
                  boundaryLegend['back'],
                  boundaryLegend['back'],
                  boundaryLegend['back'],
                  boundaryLegend['left'],
                  boundaryLegend['right'],
                  boundaryLegend['bottom'],
                  boundaryLegend['top'],
                  boundaryLegend['top'],
                  boundaryLegend['top'],
                  boundaryLegend['top'],
                  boundaryLegend['top'],
                  boundaryLegend['top'],
                  boundaryLegend['top'],
                  boundaryLegend['inner'],
                  boundaryLegend['inner'],
                  boundaryLegend['inner'],
                  boundaryLegend['inner'],
                  boundaryLegend['inner'],
                  boundaryLegend['inner']]
    regions = [[h/2.0,width/2.0,h/2],
               [4.0*h,width/2.0,0.5*h],
               [4.0*h,width/2.0,0.75*h]]
    regionFlags = [1,2,3]
    domain = Domain.PiecewiseLinearComplexDomain(vertices=vertices,
                                                 vertexFlags=vertexFlags,
                                                 facets=facets,
                                                 facetFlags=facetFlags,
                                                 regions=regions,
                                                 regionFlags=regionFlags)
    domain.boundaryFlags=boundaryLegend
    domain.regionLegend = {'levee':1,'leveeFace':3,'defect':2,'default':0}
    return domain

if __name__=='__main__':
    import os
    domain =  gl_3_3d(width=10,h=10)
    domain.writeAsymptote("gl_3_3d")
    domain.writePoly("gl_3_3d")
    domain.writePLY("gl_3_3d")
    print domain.boundaryFlags
    #os.system("asy -V gl_3_3d")
    os.system("tetgen -KVApfen gl_3_3d.poly")
