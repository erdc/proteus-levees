import os
import sys


from distutils.core import setup, Extension
from Cython.Distutils import build_ext
import numpy

## \file setup.py setup.py
#  \brief The python script for building proteus
#
#  Set the DISTUTILS_DEBUG environment variable to print detailed information while setup.py is running.
#

# Get Proteus configuration information
try:
    proteus_prefix = sys.prefix
    sys.path.insert(0, os.path.join(proteus_prefix, 'proteusConfig'))
    from config import *
except:
    raise RuntimeError("Missing or invalid config.py file. See proteusConfig for examples")

###to turn on debugging in c++
##\todo Finishing cleaning up setup.py/setup.cfg, config.py...
from distutils import sysconfig
cv = sysconfig.get_config_vars()

# Get include flags for building Proteus Extensions

import proteus

try:
    import proteus.util
    proteus_include_dir = proteus.util.get_include_dir()
    proteus_model_kernel = [proteus_include_dir + '/ModelFactory.h', proteus_include_dir + '/CompKernel.h']
except:
    import sys
    sys.stderr.write("Unable to import `get_include_dir` from Proteus, is your Proteus up to date?")
    raise

# Ensure that Proteus namespace init.py has been symbolically linked in
if not os.path.exists(os.path.join('.','proteus','__init__.py')) or not os.path.exists(os.path.join('.','proteus','__init__.pyc')):
    # Symbolically link in Proteus __init__.py file
    proteus_init = proteus.__file__
    # if pyc, use py instead if available
    if proteus_init.endswith('pyc') and os.path.exists(proteus_init[:-1]):
        proteus_init = proteus_init[:-1]
    proteus_init_name = os.path.split(proteus_init)[-1]
    os.symlink(proteus_init, os.path.join('.', 'proteus', proteus_init_name))


setup(name='proteus_levees',
      version='0.9.0',
      description='Proteus modules for simulating free surface fluid/structure interaction',
      author='Chris Kees',
      author_email='chris.kees@us.army.mil',
      url='http://proteus.usace.army.mil',
      packages=['proteus.levees'],
      ext_package='proteus.levees',
      cmdclass = {'build_ext':build_ext},
      ext_modules=[Extension("cElastoPlastic",["proteus/levees/cElastoPlastic.pyx"],
                             depends=["proteus/levees/ElastoPlastic.h","proteus/levees/cElastoPlastic.h","proteus/levees/mohrCoulomb.h","proteus/levees/tresca.h","proteus/levees/vonMises.h","proteus/levees/druckerPrager.h","proteus/levees/mcdp.h","proteus/levees/mohrCoulomb2.h"]+proteus_model_kernel,
                             language="c++",
                             define_macros=[('PROTEUS_LAPACK_H',PROTEUS_LAPACK_H),
                                            ('PROTEUS_LAPACK_INTEGER',PROTEUS_LAPACK_INTEGER),
                                            ('PROTEUS_BLAS_H',PROTEUS_BLAS_H)],
                             include_dirs=[numpy.get_include(),proteus_include_dir],
                             extra_compile_args=PROTEUS_EXTRA_COMPILE_ARGS+['-g'],
                             extra_link_args=PROTEUS_EXTRA_LINK_ARGS+['-g']),
                   Extension("cRichards",["proteus/levees/cRichards.pyx"],
                             depends=["proteus/levees/Richards.h"]+proteus_model_kernel,
                             language="c++",
                             include_dirs=[numpy.get_include(), proteus_include_dir],
                             extra_compile_args=PROTEUS_EXTRA_COMPILE_ARGS+['-g'],
                             extra_link_args=PROTEUS_EXTRA_LINK_ARGS+['-g']),
                   ],
      requires=['numpy']
      )
