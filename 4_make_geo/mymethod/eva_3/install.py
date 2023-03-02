import os
import sys
import numpy
import sysconfig

numpy_path = os.path.dirname(numpy.__file__)
include_path = sysconfig.get_paths()['include']

os.system(f'cython3 -X language_level=3 _criterion.pyx')
os.system(f'gcc -shared -pthread -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing -I{include_path} -I{numpy_path}/core/include -o _criterion.so _criterion.c')
os.system(f'rm -rf _criterion.c')
