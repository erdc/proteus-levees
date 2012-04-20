from proteus import *
from proteus.default_p import *
from proteus.levees import ElastoPlastic
"""
Soil mechanics model for problem 6.4 in Smith and Griffiths
"""
nd=3
from griffiths_lane_4 import *
genMesh=True
he = 1.0
#he*=0.5
#hl = hd
#he*=0.5
#he*=0.5 about 2.5G
#he*=0.33
#he*=0.5
H=10.0
D=2.0
#2D
domain = gl_4_3d(width=he,h=H,d=D)
#3D
#domain = gl_4_3d(width=10,h=H,d=D)
domain.regionConstraints = [he**3/6,he**3/6]
domain.writePLY("gl_4_3d")
domain.writePoly("gl_4_3d_reclassify")
print domain.regionLegend
triangleOptions="VApq1.25q12fena"
print triangleOptions

#mechanical properties
SRF = 1.0#65#15
SRF_init=1.0
g = [0.0,0.0,-9.8]
rhos = 1.7347 #1000 kg/m^3
rhow = 0.998 #1000 kg/m^3
E=1.0e5 #kN/m^2 Young's modulus
nu=0.3  #- Poisson's ratio
D = E/((1.0+nu)*(1-2.0*nu))
D11 = D*(1.0 - nu)
D12 = D*nu
D44 = 0.5*D*(1.0-2*nu)
pa= 101325.0/1000.0 #kN/m^2 atmospheric pressure
#soil models
soilModelFlag=0
#Lade soil model params
mu = 0.6 
ne = 0.6 
Psi1 = 3.69 
ah=0.001 
bh=1.0/45.0 
Fyc=15 
Vr=0.1
#
#Mohr-Coulomb soil model params
soilModelFlag=1
phi_mc = 0.0#0 is what GL 99 used atan(tan((20.0/360.0)*2.0*math.pi)/SRF) #friction angle
c_mc = 0.25*rhos*fabs(g[2])*H
psi_mc = 0.0 #dilation angle
#
nMediaTypes  = len(domain.regionLegend)
alphaVGtypes = numpy.zeros((nMediaTypes,),'d')
nVGtypes     = numpy.zeros((nMediaTypes,),'d')
thetaStypes  = numpy.zeros((nMediaTypes,),'d')
thetaRtypes  = numpy.zeros((nMediaTypes,),'d')
thetaSRtypes = numpy.zeros((nMediaTypes,),'d')
KsTypes      = numpy.zeros((nMediaTypes,),'d')
smTypes      = numpy.zeros((nMediaTypes,14),'d')
smFlags      = numpy.zeros((nMediaTypes,),'i')

#soil mechanics
it=1
smFlags[it] = 1
smTypes[it,0] = E
smTypes[it,1] = nu
smTypes[it,2] = D11
smTypes[it,3] = D12
smTypes[it,4] = D44
smTypes[it,5] = phi_mc
smTypes[it,6] = c_mc
smTypes[it,7] = psi_mc
smTypes[it,12] = pa
smTypes[it,13] = rhos

it=2
smFlags[it] = 1
smTypes[it,0] = E
smTypes[it,1] = nu
smTypes[it,2] = D11
smTypes[it,3] = D12
smTypes[it,4] = D44
smTypes[it,5] = phi_mc
smTypes[it,6] = 2.0*c_mc
#smTypes[it,6] = c_mc
smTypes[it,7] = psi_mc
smTypes[it,12] = pa
smTypes[it,13] = rhos


print "smFlags",smFlags
initialConditions = None

analyticalSolution = None

# class Coefficients_gl_3(ElastoPlastic.Coefficients):
#     def __init__(self,modelType_block,modelParams_block,g,rhow,pa,nd,SRF):
#         ElastoPlastic.Coefficients.__init__(self,modelType_block,modelParams_block,g,rhow,pa,nd,SRF)
#     def postStep(self,t,firstStep=False):
#         if self.gravityStep:
#             self.cq['strain_last'][:] = self.cq['strain']
#             self.cq['plasticStrain_last'][:] = 0.0#self.cq['plasticStrain']
#             self.cebqe['strain_last'][:] = self.cebqe['strain']
#             self.cebqe['plasticStrain_last'][:] = 0.0#self.cebqe['plasticStrain']
#             self.gravityStep=False
#             self.model.u[0].dof[:]=0.0
#             self.model.u[1].dof[:]=0.0
#             self.model.u[2].dof[:]=0.0
#             self.copyInstructions = {'reset_uList':True}
#         else:
#             self.SRF += 0.05
#             print "========================SRF = "+`self.SRF`+"==============================="
#             self.materialProperties[2,5] = atan(tan(self.materialProperties_default[2,5])/self.SRF)#phi_mc
#             self.materialProperties[2,6] = self.materialProperties_default[2,6]/self.SRF#c_mc
#             self.copyInstructions = {'reset_uList':True}

#from SoilMechanics import LinearElasticitySF
#from SoilMechanics import ElasticPlasticSF
#coefficients = LinearElasticitySF(E=317986,nu=0.31,g=g,nd=nd)#stokes_2D_tube_p.Stokes2D()
#coefficients = ElasticPlasticSF(modelType_block=smFlags,modelParams_block=smTypes,g=g,rhow=rhow,pa=pa,nd=nd)
LevelModelType = ElastoPlastic.LevelModel
coefficients = ElastoPlastic.Coefficients(modelType_block=smFlags,modelParams_block=smTypes,g=g,rhow=rhow,pa=pa,nd=nd,SRF=SRF_init)

bfs = domain.boundaryFlags

def getDBC_u(x,flag):
    if flag in [bfs['left'],bfs['right'],bfs['bottom']]:
        return lambda x,t: 0.0

def getDBC_v(x,flag):
    if flag in [bfs['front'],bfs['back'],bfs['bottom']]:
        return lambda x,t: 0.0

def getDBC_w(x,flag):
    if flag == bfs['bottom']:
        return lambda x,t: 0.0

dirichletConditions = {0:getDBC_u,
                       1:getDBC_v,
                       2:getDBC_w}

def stress_u(x,flag):
    if flag in [bfs['left'],bfs['right'],bfs['bottom']]:
        return None
    else:
        return lambda x,t: 0.0#[0.0,0.0,0.0]

def stress_v(x,flag):
    if flag in [bfs['front'],bfs['back'],bfs['bottom']]:
        return None
    else:
        return lambda x,t: 0.0#[0.0,0.0,0.0]

def stress_w(x,flag):
    if flag == bfs['bottom']:
        return None
    else:
        return lambda x,t: 0.0#[0.0,0.0,0.0]

stressFluxBoundaryConditions = {0:stress_u,
                                1:stress_v,
                                2:stress_w}

T=1

#cek todo add max diplacement, maybe create field of element centered stress and strain for viz
class PlasticWork(AuxiliaryVariables.AV_base):
    def __init__(self):
        pass
    def attachModel(self,model,ar):
        self.model=model
        self.ar=ar
        self.writer = Archiver.XdmfWriter()
        self.nd = model.levelModelList[-1].nSpace_global
        m = self.model.levelModelList[-1]
        return self
    def calculate(self):
        eps = numpy.zeros((6,),"d")
        eps_p = numpy.zeros((6,),"d")
        sig = numpy.zeros((6,),"d")
        max_displacement = 0.0
        for m in self.model.levelModelList:
            if self.nd ==3:
                plasticWork=0.0
                totalWork=0.0
                for eN in range(m.mesh.nElements_global):
                    for k in range(m.nQuadraturePoints_element):
                        max_displacement = max(max_displacement,
                                               sqrt(m.q[('u',0)][eN,k]**2 + m.q[('u',1)][eN,k]**2 + m.q[('u',2)][eN,k]**2))
                        eps[0] = m.q[('grad(u)',0)][eN,k,0]
                        eps[1] = m.q[('grad(u)',1)][eN,k,1]
                        eps[2] = m.q[('grad(u)',2)][eN,k,2]
                        eps[3] = m.q[('grad(u)',0)][eN,k,1] + m.q[('grad(u)',1)][eN,k,0]
                        eps[4] = m.q[('grad(u)',0)][eN,k,2] + m.q[('grad(u)',2)][eN,k,0]
                        eps[3] = m.q[('grad(u)',1)][eN,k,2] + m.q[('grad(u)',2)][eN,k,1]
                        sig[0] = m.q['sigma'][eN,k,0,0]
                        sig[1] = m.q['sigma'][eN,k,1,1]
                        sig[2] = m.q['sigma'][eN,k,2,2]
                        sig[3] = m.q['sigma'][eN,k,0,1]
                        sig[4] = m.q['sigma'][eN,k,0,2]
                        sig[5] = m.q['sigma'][eN,k,1,2]
                        eps_p[0] = m.q['eps_p'][eN,k,0,0]
                        eps_p[1] = m.q['eps_p'][eN,k,1,1]
                        eps_p[2] = m.q['eps_p'][eN,k,2,2]
                        eps_p[3] = m.q['eps_p'][eN,k,0,1]
                        eps_p[4] = m.q['eps_p'][eN,k,0,2]
                        eps_p[5] = m.q['eps_p'][eN,k,1,2]
                        for I in range(6):
                            plasticWork += sig[I]*eps_p[I]*m.q[('dV_u',0)][eN,k]
                            totalWork += sig[I]*eps[I]*m.q[('dV_u',0)][eN,k]
            if fabs(totalWork) < 1.0e-8: totalWork = 1.0e-8#make sure denom is nonzero
            log("Plastic Work = %12.5e, Total Work = %12.5e, Ratio = %12.5e" % (plasticWork,totalWork,plasticWork/totalWork))
            log("Max Displacement = %12.5e"  % (max_displacement,))
