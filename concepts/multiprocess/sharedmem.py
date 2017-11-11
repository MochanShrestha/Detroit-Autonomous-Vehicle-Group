from multiprocessing import Process, Array
import scipy
import numpy as np
import multiprocessing as mp

def f(a):
    a[0] = a[0]+1

if __name__ == '__main__':
    # Create the array
    #N = int(10)
    #unshared_arr = scipy.rand(N)
    #a = Array('d', unshared_arr)
    #print ("Originally, the first two elements of arr = %s"%(a[:2]))

    a = mp.Array(np.ctypeslib.ctypes.c_uint8, 10)

    # Create, start, and finish the child process
    p = Process(target=f, args=(a,))
    p.start()
    p.join()

    # Print out the changed values
    print ("Now, the first two elements of arr = %s"%a[:2])

    b = a.get_obj()

    b[0] = 10

    print (a[0])