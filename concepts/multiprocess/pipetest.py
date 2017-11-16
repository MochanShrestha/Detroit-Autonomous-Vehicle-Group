
from multiprocessing import Process, Pipe
import numpy as np

def f(conn):
    #conn.send([42, None, 'hello'])
    data = np.array([3,2,1.5])
    conn.send(data)
    conn.close()

if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    p = Process(target=f, args=(child_conn, ))
    p.start()
    print (parent_conn.recv())
    p.join()
