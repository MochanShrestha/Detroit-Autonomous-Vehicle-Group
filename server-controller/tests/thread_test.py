
import threading

def thread1():
    while(1):
        print("Thread 1")

def thread2():
    while(1):
        print("\tThread 2")

threading._start_new_thread(thread1, ())
threading._start_new_thread(thread2, ())

while(1):
    None