# /*****************************************************************
# //
# //  Author:		Ehsan Kourkchi
# //
# //  DATE:		September, 27, 2017         
# //
# //  FILE:		evolveImage.py    
# //
# //  Description:      Evolving Imeges.
# //                    use '-h' flag to see all the possible options
# //****************************************************************/



## See here for documentation
## http://imageio.readthedocs.io/en/latest/examples.html

from pylab import *
import matplotlib as mpl
from matplotlib.widgets import Slider, Button, RadioButtons
import matplotlib.pyplot as plt
from PIL import Image#, ImageTk
import matplotlib.patches as patches


from subprocess import Popen, PIPE
import sys
import os
import subprocess
from math import *

import copy
import numpy as np
import time
import random

## Importing home-made image filters (needs imfilters.py)
import imfilters as imf

# Global variable, an array of all Images
# each Image is an object defined by the class My_ax
# The most important Image characteristics:
# 1) image  -> the 2d image array
# 2) A      -> the convolution matrix
# 3) factor -> the factor parameter
# 4) bias   -> the bias parameter
# The displayed image would be then:
#     factor x (A * image) + bias,
# where '*' is the convolution matrix
Images = []

im     = None

#################################################
class My_ax:
    
    def __init__(self, fig, position, image, flip=False):
        
        self.position = position
        self.image = image
        
        self.ax = fig.add_axes(position)
        
        self.A = np.zeros((5,5))
        self.A[1,1] = 1
        self.factor = 1
        self.bias   = 0


        col = 'lightgray'
        self.ax.spines['bottom'].set_color(col)
        self.ax.spines['top'].set_color(col)
        self.ax.spines['right'].set_color(col)
        self.ax.spines['left'].set_color(col)
        self.ax.tick_params('off')
        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        
        
        #self.ax.set_xlim(0,512)
        #self.ax.set_ylim(0,512)
        
        if flip:
            image = np.flipud(image)   # flips an array
        
        self.ax.imshow(image)
        
    def setImage(self, A, factor, bias):
        
        self.A = A
        self.factor = factor
        self.bias = bias
        
        im = np.copy(self.image)
        im[:,:,0] = imf.convolve(self.image[:,:,0], A, factor=factor, bias=bias)
        im[:,:,1] = imf.convolve(self.image[:,:,1], A, factor=factor, bias=bias)
        im[:,:,2] = imf.convolve(self.image[:,:,2], A, factor=factor, bias=bias)
        self.ax.imshow(im)                
        

#####################################################
# Given A, factor and bias, this function produces a new set of 
# mutated parameters.
def Mutate(A, factor, bias):
    

    A_new  = np.copy(A)
    do = True
    rnd = random.choice(range(10))
    
    if rnd < 2:  # 20% chance (A unchanged, factor and bias are mutated dramatically)
        do = False
        
        #A_new = np.random.randint(3, size=(5,5))
        mu, sigma = 1, 0.3
        f = np.random.normal(mu, sigma, 1)
        factor = f[0]
        if factor>1:
            factor = 2 - factor
        
        mu, sigma = 0, 50
        b = np.random.normal(mu, sigma, 1)
        bias = abs(b[0])
        
    elif rnd >= 8: # 20% chance (factor and bias are uncahnged, A is slightly mutated)
        do = False
        #####
        i = np.random.randint(4)
        j = np.random.randint(4)
        
        randMutate = np.random.randint(2, size=(2,2))
        

        
        for i in range(2):
            for j in range(2):
                randMutate[i][j] *= random.choice([-1, 1])        
        
        
        A_new[i:i+2,j:j+2] = A_new[i:i+2,j:j+2] + randMutate        
         
    
    if do: # 60% chance (All parameters are slightly mutated)
        #####
        i = np.random.randint(4)
        j = np.random.randint(4)
        
        randMutate = np.random.randint(2, size=(2,2))
        

        
        for i in range(2):
            for j in range(2):
                randMutate[i][j] *= random.choice([-1, 1])        
        
        
        A_new[i:i+2,j:j+2] = A_new[i:i+2,j:j+2] + randMutate
        
        
        
        factor = np.random.normal(factor, 0.05, 1)[0]
        if factor < 0:
            factor = 0.1

        bias = abs(np.random.normal(bias, 5, 1)[0])
    
    return A_new, factor, bias
 
      
############################################
#################################################
# Given the image name, this function opens the image and returns a 2d array
def open_image(file, flip=False):
   
   image = Image.open(file)

   if flip:
      image = np.flipud(image)   # flips an array
   
   return image
############################################
# randomly initializind the convolution matrix (A), factor and bias
def randInit():
   
   # All A-elements are initially either 0 or 1  
   A = np.random.randint(2, size=(5,5))
        
   mu, sigma = 1, 0.1
   f = np.random.normal(mu, sigma, 1)
   factor = f[0]
   if factor>1:
      factor = 2 -  factor
   if factor < 0:
      factor = 1
            
   mu, sigma = 0, 100
   b = np.random.normal(mu, sigma, 1)
   bias = abs(b[0])    
   
   factor = 1
   bias = 0 
   
   return A, factor, bias
    
############################################
# when clicking on a panel, that panel would be chosen, and displayed 
# on the 2nd from left panel in the most buttom row.
# The original image is always displayed on the left buttom corner
# The rest of the images are the mutated version of the chosen picture.
def on_click(event): 
    
    global Images, im
    
    for i in range(len(Images)):
        if event.inaxes == Images[i].ax and i>0:
            #Images[i].ax.imshow(im)  
            
            A, factor, bias = Images[i].A, Images[i].factor, Images[i].bias
            Images[1].setImage(A, factor, bias)
            
            for j in range(2,15):
                A_new, factor_new, bias_new = Mutate(A, factor, bias)
                Images[j].setImage(A_new, factor_new, bias_new)
            
            draw()
            break


############################################
# making the main window
# consisting an array of 3x5 images
# the buttom left corner image always shows the original image
# and all other panels show the mutated images
def make_window():
   
   global Images, im
   
   fig = plt.figure(figsize=(12, 8), dpi=100)
   fig.patch.set_facecolor('black')
   
   for row in range(3):
       for col in range(5):
           Images.append(My_ax(fig, [0.03+0.19*col, 0.07+row*0.3, 0.18, 0.27], im))
           
   A, factor, bias = Images[0].A, Images[0].factor, Images[0].bias
   
   for p in range(1,15):

       A_new, factor_new, bias_new = Mutate(A, factor, bias)
       Images[p].setImage(A_new, factor_new, bias_new)
       
       
   
   fig.canvas.mpl_connect('button_press_event', on_click)
   
    
   plt.show()  

#####################################################
# Handling the command line arguments 
# and initializing the main graphical window
if __name__ == '__main__':


   if (len(sys.argv) < 2): 
        print "\nNot enough input arguments ..."
        print >> sys.stderr, "Use \"python "+sys.argv[0]+" -h\" for help ... ' \n"
        exit(1)
        
   if sys.argv[1]=='-h':
        print
        print "Usage ..."
        print "Use \"python "+sys.argv[0]+" <image>\" to open an image."
        print "Use \"python "+sys.argv[0]+" -h\" to see this help."
        print
        exit(1)
   
   try: 
        filename = sys.argv[1]
        im = open_image(filename, flip=True)
        im = np.flipud(im)
   except:
        print "Could not open \""+filename+"\""
        print "Make sure about the file name and its format."
        print >> sys.stderr, "Use \"python "+sys.argv[0]+" -h\" to see the other options ... ' \n"
        exit(1)            
    
   # making the main window and get ready for the user actions
   make_window()
    
    
