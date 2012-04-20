from proteus import *
from proteus.default_p import *
from proteus.SubsurfaceTransportCoefficients import ConservativeHeadRichardsMualemVanGenuchten
from proteus.elastoplastic import Richards
nd=3
from griffiths_lane_5 import *
genMesh=True
he = 1.0
he*=0.5
he*=0.5
#he*=0.5
#he*=0.33
H=10.0
domain = gl_5_3d(width=he,h=H)
boundaryFlags = domain.boundaryFlags
domain.regionConstraints = [(he**3)/6.0]
domain.writePoly("gl_5_3d")
triangleOptions="VApq1.25q12fena"

dimensionless_gravity  = numpy.array([0.0,
                                      0.0,
                                      -1.0])
dimensionless_density  = 1.0
#
#
nMediaTypes  = len(domain.regionLegend)
alphaVGtypes = numpy.zeros((nMediaTypes,),'d')
nVGtypes     = numpy.zeros((nMediaTypes,),'d')
thetaStypes  = numpy.zeros((nMediaTypes,),'d')
thetaRtypes  = numpy.zeros((nMediaTypes,),'d')
thetaSRtypes = numpy.zeros((nMediaTypes,),'d')
KsTypes      = numpy.zeros((nMediaTypes,3),'d')

for i in range(nMediaTypes):
    alphaVGtypes[i] = 5.470
    nVGtypes[i]     = 4.264
    thetaStypes[i]  = 0.301
    thetaRtypes[i]  = 0.308*0.301
    thetaSRtypes[i] = thetaStypes[i] - thetaRtypes[i]
    KsTypes[i,:]    = [5.04,5.04,5.04]#m/d?

useSeepageFace = True
gl_L = 0.0*H
leftHead  = H - gl_L
rightHead = 0.0*H
headInit  = leftHead
#headInit  = rightHead

def getDBC(x,flag):
    if flag == boundaryFlags['left']:
        return lambda x,t: leftHead - x[2] 
    elif flag == boundaryFlags['right']:
        if useSeepageFace:
            return lambda x,t: 0.0
        else:
            return lambda x,t: rightHead - x[2]
    else:
        return None

dirichletConditions = {0:getDBC}

class SaturatedIC:
    def uOfXT(self,x,t):
        return headInit - x[2]

initialConditions  = {0:SaturatedIC()}

fluxBoundaryConditions = {0:'mixedFlow'}

def getAFBC(x,flag):
    if flag not in [boundaryFlags['left'],
                    boundaryFlags['right']]:
        return lambda x,t: 0.0

advectiveFluxBoundaryConditions =  {0:getAFBC}

def getDFBC(x,flag):
    if flag not in [boundaryFlags['left'],
                    boundaryFlags['right']]:
        return lambda x,t: 0.0

diffusiveFluxBoundaryConditions = {0:{0:getDFBC}}

def getSeepageFace(flag):
    if useSeepageFace:
        if flag == boundaryFlags['right']:
            return 1
        else:
            return 0
    else:
        return 0

useOpt=True

if not useOpt:
    coefficients = ConservativeHeadRichardsMualemVanGenuchten(nd,
                                                              KsTypes,
                                                              nVGtypes,
                                                              alphaVGtypes,
                                                              thetaRtypes,
                                                              thetaSRtypes,
                                                              gravity=dimensionless_gravity,
                                                              density=dimensionless_density,
                                                              beta=0.0001,
                                                              diagonal_conductivity=True,
                                                              getSeepageFace=getSeepageFace)
else:
    LevelModelType = Richards.LevelModel
    coefficients = Richards.Coefficients(nd,
                                         KsTypes,
                                         nVGtypes,
                                         alphaVGtypes,
                                         thetaRtypes,
                                         thetaSRtypes,
                                         gravity=dimensionless_gravity,
                                         density=dimensionless_density,
                                         beta=0.0001,
                                         diagonal_conductivity=True,
                                         getSeepageFace=getSeepageFace)
