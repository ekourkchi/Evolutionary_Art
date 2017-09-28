/*****************************************************************
//
//  Author:		Ehsan Kourkchi
//
//  DATE:		September, 27, 2017         
//
//  FILE:		filters.c
//
//  Description:        Developed image filter in C to be called in Python 
//****************************************************************/


#include "Python.h"


#include <stdio.h>
#include <assert.h>
#include <math.h>
#include "numpy/arrayobject.h"
#include "numpy/npy_common.h"
#include "numpy/ndarrayobject.h"
#include <omp.h>
#define PI 3.14159265359



#define max(a,b) \
   ({ __typeof__ (a) _a = (a); \
       __typeof__ (b) _b = (b); \
     _a > _b ? _a : _b; })
   
#define min(a,b) \
   ({ __typeof__ (a) _a = (a); \
       __typeof__ (b) _b = (b); \
     _a < _b ? _a : _b; })
   


/*****************************************************************
//  Function name:		Array2DfromPython 
//
//  DESCRIPTION:		Converting a python 2D array object into an integer 2D array
//
//  Parameters:			array: the input 2D python array
//                              n:     output integer, # of rows
//                              d:     output integer, # of columns
//  Return values:		data:  the output integer 2D array
//
//****************************************************************/
static int* Array2DfromPython(PyArrayObject *array, int *n, int *d) {
  
  Py_Initialize();
  import_array();
  
  int* data;  
  int i, j, N, D;
 

  N = (int)PyArray_DIM(array, 0);
  D = (int)PyArray_DIM(array, 1);
  data = malloc(N * D * sizeof(int));
  for (i=0; i<N; i++) {
    for (j=0; j<D; j++) {
       double* pd = PyArray_GETPTR2(array, i, j);
       data[i*D + j] = *pd;
    }
  }
    
  
  *n = N;
  *d = D;
  return data;
     
}


/*****************************************************************
//  Function name:		Array2DtoPython 
//
//  DESCRIPTION:		Converting an integer 2D array into the python 2D array
//
//  Parameters:			data:   the input 2D integer array
//                              N:      output integer, # of rows
//                              D:      output integer, # of columns
//  Return values:		output: the output python 2D array
//
//****************************************************************/
static PyObject *Array2DtoPython(int* data, int N, int D) {
    
    Py_Initialize();
    import_array();
    
    npy_intp dims[2];
    PyObject *output;
    PyArrayObject* inds;
    int i, j;
    
    dims[0] = N;
    dims[1] = D;
    inds =  (PyArrayObject*) PyArray_SimpleNew(2, dims, PyArray_INT);
     for (i=0; i<N; i++) {
        for (j=0; j<D; j++) {   
            
            int* iptr;
    iptr = PyArray_GETPTR2(inds, i, j);
    *iptr = data[i*D + j];

    
        }}
    
    
    output = Py_BuildValue("O", inds);
    Py_DECREF(inds);
    return output;    
    
} 


/*****************************************************************
//  Function name:		filter_mirror 
//
//  DESCRIPTION:		Flipping a 2D image (2d array)
//
//  Parameters:			input:   the input python 2D array

//  Return values:		output:  the output python 2D array
//
//****************************************************************/
static PyObject *filter_mirror(PyObject *self, PyObject *args) {
    
    // The following two lines are very important
    Py_Initialize();
    import_array();
    
    int i, j;
    int N, D;
    int* data, tmp;
    PyArrayObject *array;
    

    // Grab the 2D data from Python
    if (!PyArg_ParseTuple(args, "O!", &PyArray_Type, &array)) {
          PyErr_SetString(PyExc_ValueError, "pass a 2D numpy array");
          return NULL;
    }
    data = Array2DfromPython(array, &N, &D);
    
    
    // Do somthing with the data
    for (i=0; i<N; i++) {
        for (j=0; j<D/2; j++) {   
          
            tmp = data[i*D + j];
            data[i*D + j] = data[i*D + (D-j-1)];
            data[i*D + (D-j-1)] = tmp;
            
    }}


    // Return the filterred data back to Python
    return Array2DtoPython(data, N, D);

}

/*****************************************************************
//  Function name:		filter_convolve 
//
//  DESCRIPTION:		Convolving a 2D image (2d array) by a convolution matrix, i.e. filtArr. The final image would be then multiplied by a factor plus a bias. See http://lodev.org/cgtutor/filtering.html
for more detailed information.
//
//  Parameters:			input:   the input python 2D array, factor (a 2D convolution matrix), integer factor, and integer bias

//  Return values:		output:  the output python 2D array
//
//****************************************************************/
static PyObject *filter_convolve(PyObject *self, PyObject *args) {
    
    // The following two lines are very important
    Py_Initialize();
    import_array();
    
    int h, w, x, y,hh,ww;
    int *image, *out, *filter;
    int Nsum, sum;
    PyObject *pyout;
    PyArrayObject *array, *filtArr;
    int filterY, filterX;
    int filterWidth, filterHeight;
    double factor, bias;
    
    // Grab the 2D image from Python
    if (!PyArg_ParseTuple(args, "O!O!dd", &PyArray_Type, &array, &PyArray_Type, &filtArr, &factor, &bias)) {
          PyErr_SetString(PyExc_ValueError, "pass a 2D numpy array");
          return NULL;
    }
    image = Array2DfromPython(array, &h, &w);
    filter = Array2DfromPython(filtArr, &filterHeight, &filterWidth);    // 3x3

    out = (int *) malloc(h * w * sizeof(int));    
    
  //apply the filter
  for(x = 0; x < w; x++)
  for(y = 0; y < h; y++)
  {
    double red = 0.0;

    //multiply every value of the filter with corresponding image pixel
    for(filterY = 0; filterY < filterHeight; filterY++)
    for(filterX = 0; filterX < filterWidth; filterX++)
    {
      int imageX = (x - filterWidth / 2 + filterX + w) % w;
      int imageY = (y - filterHeight / 2 + filterY + h) % h;
      red += image[imageY * w + imageX] * filter[filterY * filterWidth + filterX];

    }

    //truncate values smaller than zero and larger than 255
    out[y * w + x] = min(max(floor(factor * red + bias), 0), 255);
// out[y * w + x] = ((floor(factor * red + bias), 0), 255);
  }
      
    pyout = Array2DtoPython(out, h, w);
    
    free(image);
    free(out);
    // Return the filterred data back to Python
    return pyout;

    
}

/*****************************************************************
//  Function name:		filter_blur 
//
//  DESCRIPTION:		Blurring a 2D image (2d array) 
//
//  Parameters:			input:   the input python 2D array, bluring width (bw)

//  Return values:		output:  the output python 2D array
//
//****************************************************************/
static PyObject *filter_blur(PyObject *self, PyObject *args) {
    
    // The following two lines are very important
    Py_Initialize();
    import_array();
    
    int i, j, ii, jj;
    int N, D;
    int *data, *out;
    int Nsum, sum;
    PyObject *pyout;
    PyArrayObject *array;
    int bw=5;     // blur width
    
    
    // Grab the 2D data from Python
    if (!PyArg_ParseTuple(args, "O!i", &PyArray_Type, &array, &bw)) {
          PyErr_SetString(PyExc_ValueError, "pass a 2D numpy array");
          return NULL;
    }
    data = Array2DfromPython(array, &N, &D);
    
    out = (int *) malloc(N * D * sizeof(int));
    

        
    // Bluring along N-axis ****************
    for (i=0; i<N; i++) {
        
        j = bw;
        sum=0; Nsum=2*bw+1;
        for (jj=0; jj<2*bw+2; jj++) {
            
            sum += data[i*D + jj];
        
        }
        
        out[i*D + j] = sum;    
        
        for (j=bw+1; j<D-bw; j++) {
            
             out[i*D + j] = out[i*D + j-1]-data[i*D + j-bw-1]+data[i*D + j+bw];
        
        }
        
        for (j=bw-1; j>-1; j--) {
            
             out[i*D + j] = out[i*D + j+1]-data[i*D + j+bw+1];
        
        }        
        
        for (j=D-bw; j<D; j++) {
            
             out[i*D + j] = out[i*D + j-1]-data[i*D + j-bw-1];
        
        }          
        
    }
    

    // Bluring along D-axis ****************
    for (j=0; j<D; j++) {
        
        i = bw;
        sum=0; Nsum=2*bw+1;
        for (ii=0; ii<2*bw+2; ii++) {
            
            sum += out[ii*D + j];
        
        }
        
        data[i*D + j] = sum;    
        
        for (i=bw+1; i<N-bw; i++) {
            
             data[i*D + j] = data[(i-1)*D + j]-out[(i-bw-1)*D + j]+out[(i+bw)*D + j];
        
        }
        
        for (i=bw-1; i>-1; i--) {
            
             data[i*D + j] = data[(i+1)*D + j]-out[(i+bw+1)*D + j];
        
        }        
        
        for (i=N-bw; i<N; i++) {
            
             data[i*D + j] = data[(i-1)*D + j]-out[(i-bw-1)*D + j];
        
        }          
        
    }
        
    // Normalizing to the number of averaged pixels ****************
    for (i=0; i<N; i++) {
        for (j=0; j<D; j++) { 
            
             data[i*D + j] /= (Nsum*Nsum); 
            
             
        }}
             
             
                 
    pyout = Array2DtoPython(data, N, D);
    
    free(data);
    free(out);
    // Return the filterred data back to Python
    return pyout;

}


/////////////////////////////////////////////////
/////////////////////////////////////////////////
/////////////////////////////////////////////////
/////////////////////////////////////////////////

static PyMethodDef filterMethods[] = {



      
    { "mirror", filter_mirror, METH_VARARGS,
      "Mirror flipping the image ...." }, 
      
    { "blur", filter_blur, METH_VARARGS,
      "Mirror flipping the image ...." },      
      
    
    { "convolve", filter_convolve, METH_VARARGS,
      "Mirror flipping the image ...." },      
/////////////////////////////////////////////////
/////////////////////////////////////////////////
    
    {NULL, NULL, 0, NULL}       /* Sentinel */
};



PyMODINIT_FUNC
initfilters_c(void) {
    Py_InitModule("filters_c", filterMethods);
}
