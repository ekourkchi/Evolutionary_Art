# /*****************************************************************
# //
# //  Author:		Ehsan Kourkchi
# //
# //  DATE:		September, 27, 2017         
# //
# //  FILE:		imfilters.py     
# //
# //  Description:      The python interface to all the C-extention functions
# //                    Run "setup.py" in order to build "filters_c" library
# //****************************************************************/


import numpy as np
from math import *

## Importing home-made image filters (needs 'filters_c.so', run 'make all' or 'python setup.py install')
import filters_c as  filt
#####################################################

# mirror flipping an image. This is useful when streaming the video from a webcam
def mirror(image):
  
  im = image.astype(np.float64)

  if len(np.shape(im)) != 2:
        raise 'error: pass a 2D numpy array'
  return filt.mirror(im)

#####################################################

# bluring an image. Higher bluring widths (bw) corresponds to more blur images.
def blur(image, bw=5):
  
  im = image.astype(np.float64)

  if len(np.shape(im)) != 2:
        raise 'error: pass a 2D numpy array'
  return filt.blur(im,bw)
#####################################################

# Convloving a 2D image by a convolution matrix, F. Factor and bias would be then applied. 
def convolve(image, F, factor=1., bias=0.):
  
  im = image.astype(np.float64)
  f  = F.astype(np.float64)

  if len(np.shape(im)) != 2:
        raise 'error: pass a 2D numpy array'
  return filt.convolve(im, f, factor, bias)
#####################################################




if __name__ == '__main__':
    import doctest
    doctest.testmod()
