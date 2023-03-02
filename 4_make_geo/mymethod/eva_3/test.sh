cython3 -X language_level=3 _criterion.pyx 
gcc -shared -pthread -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing -I/usr/include/python3.10 -I/usr/lib/python3.10/site-packages/numpy/core/include -o _criterion.so _criterion.c
rm -rf _criterion.c
