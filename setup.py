# /*****************************************************************
# //
# //  Author:		Ehsan Kourkchi
# //
# //  DATE:		September, 27, 2017         
# //
# //  FILE:		setup.py        
# //
# //  Description:      Compling/Installing all the C-library extentions 
# //****************************************************************/

from distutils.core import setup, Extension
import numpy
import os.path
from numpy.distutils.misc_util import get_numpy_include_dirs
from distutils.sysconfig import get_python_inc



def strlist(s, split=' '):
    lst = s.split(split)
    lst = [i.strip() for i in lst]
    lst = [i for i in lst if len(i)]
    return lst

link = ' '.join([os.environ.get('LDFLAGS', ''),
                 os.environ.get('LDLIBS', ''),])
link = strlist(link)
objs = strlist(os.environ.get('SLIB', ''))
inc = strlist(os.environ.get('INC', ''), split='-I')
cflags = strlist(os.environ.get('CFLAGS', ''))

# Including Python Libraries
inc += [os.path.join(get_python_inc(plat_specific=1))]

# Including Numpy libraries
numpy_inc = get_numpy_include_dirs()


#link.append('-lgomp')
link.append('-shared')


#cflags.append('-fopenmp')
cflags.append('-lm')
cflags.append('-fPIC')

c_module = Extension('filters_c',
                     sources = ['filters.c'],
                     include_dirs = numpy_inc + inc,
                     extra_objects = objs,
                     extra_compile_args = cflags,
                     extra_link_args=link,
    )

setup(name = 'imfilters in Python',
      version = '1.0',
      description = 'This package contains the image filters developed in C',
      author = 'Ehsan Kourkchi',
      author_email = 'ehsan@ifa.hawaii.edu',
      url = 'http://www.ehsanoid.com',
      py_modules = [ 'imfilters' ],
      ext_modules = [c_module])

