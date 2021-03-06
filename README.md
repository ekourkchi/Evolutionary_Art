# Evolutionary Art

This package is written as a demonstration for an user directed evolutionary art. The idea is to evolve an existing Video or Image where the user plays the selection role using a GUI. In the current version, the user can only choose one image/video which would be then mutated to produce more options. As the user plays along, (s)he can guide the evolution in order to magnify the desired features, (s)he is looking for.

In order to simplify the evolution process, we filter images using the convolution matrices along with other parameters, i.e. factor and bias. The process is discussed in detail here: http://lodev.org/cgtutor/filtering.html

We use a 5x5 convolution matrix which would be then evolved based on the user preferences. The state of each panel can be defined based on the convolution matrix (A), factor and bias. For having the identity transformation, these parameters as following:

     A = {                   factor = 1   and  bias = 0
          0, 0, 0, 0, 0,
          0, 0, 0, 0, 0,
          0, 0, 1, 0, 0,
          0, 0, 0, 0, 0,
          0, 0, 0, 0, 0,
          };

To see how we do the mutation, [Click Here](https://github.com/ekourkchi/Evolutionary_Art/files/1339615/evolutionary.pdf)
The evolutionary part is in Python, while the filter and caculation intense part is in C to accelerate the process.

In the following example, the original image is always displayed on bottom-left panel. The chosen images is displayed to the right of the original image and all other panels are generated by mutating the selected image.

           python evolveImage.py cat.png
         
 ![Evolutionary Images](https://user-images.githubusercontent.com/13570487/30950224-307380a6-a3b7-11e7-9082-d9dca6fcb743.png?raw=true "Evolutionary Images")

# How to Install __imfilters__ python package

Since the extension part of this package is written in C, you need to first compile and install this part.

           python setup.py install

This would compile the C library and make the library available for your Python compiler. You can also separately install the C extension using the *Makefile*. In this case, you would probably need to add the Python and Numpy libraries to "C_INCLUDE_PATH" environmental variable

           export C_INCLUDE_PATH='<Python_Directory>/python/include/python2.7/'
           export C_INCLUDE_PATH=$C_INCLUDE_PATH':<Python_Directory>/variants/common/lib/python2.7/site-packages/numpy/core/include/'

and then to compile and make *filters_c.so* use

           make all

You can test if you have successfully installed the required python package by the following line in your python

           import imfilters as imf

## Other examples:

           python evolveImage.py dog.jpg
 ![Evolutionary Images](https://user-images.githubusercontent.com/13570487/30950390-4702a21a-a3b8-11e7-82a7-7ba36d13e71b.png?raw=true "Evolutionary Dog")

           python evolveImage.py lena.jpg

 ![Evolutionary Images](https://user-images.githubusercontent.com/13570487/30950373-268641fe-a3b8-11e7-9c9a-934fd453b347.png?raw=true "Evolutionary Lena")



 * Evolutionary Video

The same idea can be applied when displaying a Video or Streaming online movies. The same filters can be then applied frame-by-frame. To have a better performance when filtering videos, all filters are implemented in C which has a better performance compared to python.

In the following example, the videos are displayed in 4 panels. The chosen one is then displayed on the upper-left panel and the mutated ones are displayed in the other panels.

           python evolveVideo.py sample.mp4
 
 ![Evolutionary Video](https://user-images.githubusercontent.com/13570487/30950403-5be46cb8-a3b8-11e7-8f09-edf7a3085040.png?raw=true "Evolutionary Video")

To capture the video from an external camera (e.g. your laptop webcam), use this command:
 
           python evolveVideo.py 0

 ## Installing The Required Pancakes for Video Streaming

The main program is in Python. The evolutionary part can be also written in Python, as long as it's fast. However to apply the resulting filters whiles streaming videos, it's easier to use a faster Python extension like C/C++.

This program uses two Python packages, i.e. imageio and visvis to capture and stream videos. I found it easier to install Python through Anaconda or Miniconda. Then installing the above package are simple. To install Miniconda click here:  https://conda.io/miniconda.html. I have tried Python 2.7.

At the end you may need to edit your .bashrc or .cshrc or .tcshrc files to include the Miniconda codes.

After you are done with the installation, you should have access to these programs in your terminal: *pip* and *conda*. These help you to install the other packages as wll.

Commands to install the required packages:

    pip install visvis
    pip install imageio
    conda install pyside
    conda install ffmpeg -c conda-forge

Other useful python packages:

    conda install numpy
    conda install matplotlib
    conda install panda

In general, to install other useful Python packages:

    conda install <python-package>

- - - -
 * Copyright 2017
 * Author: Ehsan Kourkchi <ekourkchi@gmail.com>



