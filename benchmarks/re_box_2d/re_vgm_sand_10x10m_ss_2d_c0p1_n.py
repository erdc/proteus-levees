from proteus import *
from proteus.default_n import *
from re_vgm_sand_10x10m_ss_2d_p import *

timeIntegration = NoIntegration

DT = 1.0

femSpaces = {0:C0_AffineLinearOnSimplexWithNodalBasis}

#appears to work with NLNI or Newton but not subgridErro
#elementQuadrature = SimplexLobattoQuadrature(nd,3)
elementQuadrature = SimplexGaussQuadrature(nd,3)

elementBoundaryQuadrature = SimplexGaussQuadrature(nd-1,3)
                            

nn=3
nLevels = 4

subgridError = None
subgridError = AdvectionDiffusionReaction_ASGS(coefficients,nd,stabFlag='2',lag=False)
#to try with PTC
#subgridError = AdvectionDiffusionReaction_ASGS(coefficients,nd,stabFlag='2',lag=False)

massLumping = False

numericalFluxType = None

shockCapturing = None
#for satform
shockCapturing = ResGrad_SC(coefficients,nd,shockCapturingFactor=0.5,lag=False)
#for headform
#shockCapturing = ResGrad_SC(coefficients,nd,shockCapturingFactor=0.5,lag=False)
#try with PTC
#shockCapturing = ResGrad_SC(coefficients,nd,shockCapturingFactor=0.5,lag=True)
#shockCapturing = ResGradQuad_SC(coefficients,nd,shockCapturingFactor=2.0,lag=False)
#shockCapturing = ResGradJuanes_SC(coefficients,nd,shockCapturingFactor=4.0,uSC=4.5,lag=False)

multilevelNonlinearSolver  = NLNI
#multilevelNonlinearSolver = Newton

levelNonlinearSolver = Newton

fullNewtonFlag = True

tolFac = 1.0e-8

nl_atol_res = 1.0e-8

maxNonlinearIts = 100#1

matrix = SparseMatrix

multilevelLinearSolver = LU

levelLinearSolver = LU

linearSmoother = Jacobi
linearSmoother = GaussSeidel
linearSmoother = StarILU

linTolFac = 0.001

#conservativeFlux = {0:'point-eval'}
conservativeFlux = {0:'pwl'}
#conservativeFlux = None

