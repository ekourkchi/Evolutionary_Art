# /*****************************************************************
# //
# //  Author:		Ehsan Kourkchi
# //
# //  DATE:		September, 27, 2017         
# //
# //  FILE:		evolveVideo.py     
# //
# //  Description:      Evolving Videos. Videos can also be streamed from a camera.
# //                    use '-h' flag to see all the possible options
# //                    
# //****************************************************************/


import imageio
import visvis as vv

## See here for documentation
## http://imageio.readthedocs.io/en/latest/examples.html

import copy
import numpy as np
import time
import random
import sys
import os
import subprocess

## Importing home-made image filters (needs imfilters.py)
import imfilters as imf

#####################################################
# Handling the command line arguments
#####################################################

if (len(sys.argv) < 2): 
    print "\nNot enough input arguments ..."
    print >> sys.stderr, "Use \"python "+sys.argv[0]+" -h\" for help ... ' \n"
    exit(1)
    
if sys.argv[1]=='-h':
    print
    print "Usage ..."
    print "Use \"python "+sys.argv[0]+" 0\" to use your webcam ..."
    print "Use \"python "+sys.argv[0]+" <filename.mp4>\" to open a mp4 file ..."
    print "Use \"python "+sys.argv[0]+" -h\" to see this help."
    print
    exit(1)

try:   
    if int(sys.argv[1])==0:
        try:
           reader = imageio.get_reader('<video0>')
        except:
           print "Could not find your webcam."
           print "Make sure you have a functioning camera attached."
           print >> sys.stderr, "Use \"python "+sys.argv[0]+" -h\" to see the other options ... ' \n"
           exit(1)
        
except:
    try: 
       filename = sys.argv[1]
       reader = imageio.get_reader(filename,  'ffmpeg')
    except:
       print "Could not open \""+filename+"\""
       print "Make sure about the file name and its format (mp4)."
       print >> sys.stderr, "Use \"python "+sys.argv[0]+" -h\" to see the other options ... ' \n"
       exit(1)       


#####################################################

fig = vv.figure()
fig.position.w = 1000
fig.position.h = 600

St = [0,0,1,2]       # Filtering State of panels
close = False        # quit the program if True
A = np.zeros((5,5))
factor = 1.
bias = 0.

A_lst      = []
factor_lst = []
bias_lst   = []
A[2][2] = 1

for p in range(4):
    A_lst.append(A)
    factor_lst.append(factor)
    bias_lst.append(bias)

#####################################################
# mutating the chosen panel 3 times
# The chosen panel is then moved to the top-left panel
# with other mutated panels in the other panels
def Mutate(panelNo):
    
    global A_lst, factor_lst, bias_lst
    

    A_tmp      = np.copy(A_lst[panelNo])
    factor_tmp = factor_lst[panelNo]
    bias_tmp   = bias_lst[panelNo]
    
    # the chosen panel sits on top-left, p=0
    p = 0
    A_lst[p] = np.copy(A_tmp)
    factor_lst[p] = factor_tmp
    bias_lst[p] = bias_tmp    
    
    
    for p in range(1,4):
        A_lst[p] = np.copy(A_tmp)
        factor_lst[p] = factor_tmp
        bias_lst[p] = bias_tmp
        

        #####
        i = np.random.randint(4)
        j = np.random.randint(4)
        
        randMutate = np.random.randint(2, size=(2,2))
              
        for i in range(2):
            for j in range(2):
                randMutate[i][j] *= random.choice([-1, 1])        
        
        
        A_lst[p][i:i+2,j:j+2] = A_lst[p][i:i+2,j:j+2] + randMutate
        
        # randomly changing factor
        factor_lst[p] = np.random.normal(factor_lst[p], 0.05, 1)[0]
        if factor_lst[p] < 0:
            factor_lst[p] = 0.1
        
        # randomly changing bias
        bias_lst[p] = abs(np.random.normal(bias_lst[p], 5, 1)[0])
    

#####################################################
## Evolutionary part that changes the state array (i.e. St).
## The state of all panels can be changes together or individually 
## depending on the selected panel. 
## "panelNo" is the panel number: 
##           0)top-left 1)top-right 2)bottom-left 3)bottom-right
def Set(panelNo):
    
        global St, close, A_lst, factor_lst, bias_lst
    

        St[0] = 1
        A_lst[panelNo] = np.random.randint(3, size=(5,5))
        
        mu, sigma = 1, 0.5
        f = np.random.normal(mu, sigma, 1)
        factor_lst[panelNo] = f[0]
        if factor_lst[panelNo]>1:
            factor_lst[panelNo] = 2 -  factor_lst[panelNo]
        if factor_lst[panelNo] < 0:
            factor_lst[panelNo] = 1
            
        mu, sigma = 0, 100
        b = np.random.normal(mu, sigma, 1)
        bias_lst[panelNo] = abs(b[0])
        
        for i in range(5):
            for j in range(5):
                A_lst[panelNo][i][j] *= random.choice([-1, 1])
                
        print "Setting ....", "Panel: ", panelNo
        print A_lst[panelNo]         

#####################################################

def OnDown_0(event):
    #print event.button, event.x
    nun = 1
    if event.button==1:   # left click
       Mutate(0)
    elif event.button==2: # right click
       Set(0)             # 1st degree mutation from the original image
#####################################################
    
def OnDown_1(event):
    if event.button==1:
       Mutate(1)
    elif event.button==2: 
       Set(1)
#####################################################
    
def OnDown_2(event):
    if event.button==1:
       Mutate(2)
    elif event.button==2: 
       Set(2)
#####################################################
   
def OnDown_3(event):
    if event.button==1:
       Mutate(3)
    elif event.button==2: 
       Set(3)

#####################################################
# Exit the program, when right double-click 
def on_exit(event):
    global fig, close
    if event.button == 2:  # right double-click
      vv.closeAll()
      fig.Destroy()
      close = True
    

#####################################################
# defining the video panels and streaming loop
def main():
    
    global A_lst, factor_lst, bias_lst
    
    
    # initializing all the panels
    p = reader.get_next_data()
    
    vv.subplot(221); tv0 = vv.imshow(p, clim=(0, 255))
    panel0 = vv.gca(); panel0.eventMouseDown.Bind(OnDown_0)

    vv.subplot(222); tv1 = vv.imshow(p, clim=(0, 255))
    panel1 = vv.gca(); panel1.eventMouseDown.Bind(OnDown_1)

    vv.subplot(223); tv2 = vv.imshow(p, clim=(0, 255))
    panel2 = vv.gca(); panel2.eventMouseDown.Bind(OnDown_2)

    vv.subplot(224); tv3 = vv.imshow(p, clim=(0, 255))
    panel3 = vv.gca(); panel3.eventMouseDown.Bind(OnDown_3)

    panels = [panel0, panel1, panel2, panel3]
    for panel in panels:
        panel.eventDoubleClick.Bind(on_exit)

    
    ## streaming the videos
    for im in reader:
        
        if close:
            break
        
        u = vv.processEvents()  
        
        im[:,:,0] = imf.mirror(im[:,:,0])
        im[:,:,1] = imf.mirror(im[:,:,1])
        im[:,:,2] = imf.mirror(im[:,:,2])
        
        # TV0
        im1 = np.copy(im)
        im1[:,:,0] = imf.convolve(im1[:,:,0], A_lst[0], factor=factor_lst[0], bias=bias_lst[0])
        im1[:,:,1] = imf.convolve(im1[:,:,1], A_lst[0], factor=factor_lst[0], bias=bias_lst[0])
        im1[:,:,2] = imf.convolve(im1[:,:,2], A_lst[0], factor=factor_lst[0], bias=bias_lst[0])    
        tv0.SetData(im1)
         
        # TV1
        im2 = np.copy(im)
        im2[:,:,0] = imf.convolve(im2[:,:,0], A_lst[1], factor=factor_lst[1], bias=bias_lst[1])
        im2[:,:,1] = imf.convolve(im2[:,:,1], A_lst[1], factor=factor_lst[1], bias=bias_lst[1])
        im2[:,:,2] = imf.convolve(im2[:,:,2], A_lst[1], factor=factor_lst[1], bias=bias_lst[1])    
        tv1.SetData(im2)
        
        # TV2
        im3 = np.copy(im)
        im3[:,:,0] = imf.convolve(im3[:,:,0], A_lst[2], factor=factor_lst[2], bias=bias_lst[2])
        im3[:,:,1] = imf.convolve(im3[:,:,1], A_lst[2], factor=factor_lst[2], bias=bias_lst[2])
        im3[:,:,2] = imf.convolve(im3[:,:,2], A_lst[2], factor=factor_lst[2], bias=bias_lst[2])    
        tv2.SetData(im3)
        
        # TV3
        im4 = np.copy(im)
        im4[:,:,0] = imf.convolve(im4[:,:,0], A_lst[3], factor=factor_lst[3], bias=bias_lst[3])
        im4[:,:,1] = imf.convolve(im4[:,:,1], A_lst[3], factor=factor_lst[3], bias=bias_lst[3])
        im4[:,:,2] = imf.convolve(im4[:,:,2], A_lst[3], factor=factor_lst[3], bias=bias_lst[3])    
        tv3.SetData(im4)
        
        


#####################################################
if __name__ == '__main__':
    
    Set(1)
    Set(2)
    Set(3)
    # The initial state of te system
    St = [0,0,1,2]
    main()

    
    
