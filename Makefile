# /*****************************************************************
# //
# //  Author:		Ehsan Kourkchi
# //
# //  DATE:		September, 27, 2017         
# //
# //  FILE:		Makefile       
# //
# //  Description:      Making filters_c.so to be called in Python
# //
# //  Details: 		probably you need to add the Python and Numpy 
# // 			libraries to "C_INCLUDE_PATH" environmental variable
# // 			export C_INCLUDE_PATH='<Python_Directory>/python/include/python2.7/'
# // 			export C_INCLUDE_PATH=$C_INCLUDE_PATH':<Python_Directory>/variants/common/lib/python2.7/site-packages/numpy/core/include/'
# //****************************************************************/

all: filters.o
	gcc -shared -lgomp -Wl,-soname,filters_c.so -o filters_c.so filters.o

filters.o: filters.c
	gcc -lm -fopenmp -fPIC -c filters.c -o filters.o
	
clean: 
	rm *.o
