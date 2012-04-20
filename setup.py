from distutils.core import setup, Extension
from Cython.Distutils import build_ext
import numpy

## \file setup.py setup.py
#  \brief The python script for building proteus
#
#  Set the DISTUTILS_DEBUG environment variable to print detailed information while setup.py is running.
#
try:
    import sys,os.path
    sys.path.append(os.path.join(sys.prefix,'proteusConfig'))
    from config import *
except:
    raise RuntimeError("Missing or invalid config.py file. See proteusConfig for examples")

from distutils import sysconfig

setup(name='proteus_levees',
      version='0.0.1',
      description='Proteus modules for simulating levees',
      author='Chris Kees',
      author_email='chris.kees@us.army.mil',
      url='http://proteus.usace.army.mil',
      packages=['proteus.levees'],
      package_dir={'proteus.levees':'src'},
      ext_package='proteus.levees',
      cmdclass = {'build_ext':build_ext},
      ext_modules=[Extension("cElastoPlastic",["src/cElastoPlastic.pyx"], 
                             language="c++",
                             define_macros=[('PROTEUS_LAPACK_H',PROTEUS_LAPACK_H),
                                            ('PROTEUS_LAPACK_INTEGER',PROTEUS_LAPACK_INTEGER),
                                            ('PROTEUS_BLAS_H',PROTEUS_BLAS_H)],
                             include_dirs=[numpy.get_include(),os.getenv('PROTEUS')+'/proteusModule/src',
                                           os.getenv('PROTEUS')+'/proteusModule/include']),
                   Extension("cRichards",["src/cRichards.pyx"], 
                             language="c++",
                             define_macros=[('PROTEUS_LAPACK_H',PROTEUS_LAPACK_H),
                                            ('PROTEUS_LAPACK_INTEGER',PROTEUS_LAPACK_INTEGER),
                                            ('PROTEUS_BLAS_H',PROTEUS_BLAS_H)],
                             include_dirs=[numpy.get_include(),os.getenv('PROTEUS')+'/proteusModule/src',
                                           os.getenv('PROTEUS')+'/proteusModule/include']),
                   ],
      requires=['numpy']
      )
