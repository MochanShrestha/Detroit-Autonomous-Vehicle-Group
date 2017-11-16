
from multiprocessing import Process, Value, Array
import numpy as np
import sharedmem

def f(n, a):
    n.value = 3.1415927
    for i in range(len(a)):
        a[i] = -a[i]

def f2(a):
    for i in range(len(a)):
        a[i] = -a[i]

def f3(npa):
    vals = [1,2,3]
    for i in range(len(npa)):
        npa[i] = vals[i]

if __name__ == '__main__':
    num = Value('d', 0.0)
    arr = Array('i', range(10))
    nparr = Array('d', 3)

    #p = Process(target=f, args=(num, arr))
    #p = Process(target=f2, args=(arr,))
    p = Process(target=f3, args=(nparr,))
    p.start()
    p.join()

    #print(num.value)
    #print(arr[:])
    print(nparr[:])