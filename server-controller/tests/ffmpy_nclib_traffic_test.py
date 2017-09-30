
import ffmpy
import pygame
import cv2
import subprocess
import numpy
import errno
import time
import threading
import nclib
import socket
import queue
from pygame.locals import *

import perception_pipeline as percept

pygame.init()
width = 1280
height = 720
screen = pygame.display.set_mode ( (width, height), pygame.RESIZABLE)

# ff = ffmpy.FFmpeg(inputs={'pipe:0': '-f rawvideo -pix_fmt rgb24 -s:v 640x480'}, outputs={'pipe:1': '-v:c h264 -f mp4'})
#ff = ffmpy.FFmpeg(inputs={'pipe:0': '-f h264'}, outputs={'pipe:1': '-f rawvideo -pix_fmt rgb24'})
ff = ffmpy.FFmpeg(global_options='', inputs={'pipe:0': '-f h264'}, outputs={'pipe:1': '-f rawvideo -pix_fmt rgb24'})
#ff = ffmpy.FFmpeg(inputs={'sample.h264': None}, outputs={'pipe:1': '-f rawvideo -pix_fmt rgb24'})
print (ff.cmd)

try:
    ff.process = subprocess.Popen(
        ff._cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=None
    )
except OSError as e:
    if e.errno == errno.ENOENT:
        raise ffmpy.FFExecutableNotFoundError("Executable '{0}' not found".format(ff.executable))
    else:
        raise
#ff.run(input_data=open('sample.h264', 'rb').read(), stdout=subprocess.PIPE)
nc = nclib.Netcat(listen=('', 2222))
#nc.interact()
#socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#socket.connect((self.hostname, self.port))

def write_data():
    nwritten = 0
    while(1):
        #print("Getting some data")
        fdata = nc.recv()
        #print("Trying to write some data")
        if len(fdata) == 0:
            #print("Finished writing file")
            ff.process.stdin.close()
            break;
        ff.process.stdin.write(fdata)
        #ff.process.stdin.flush()
        #nwritten = nwritten + len(fdata)
        #print("Wrote some data: " + str(nwritten))

global mutex
global raw_image
global q

mutex = threading.Lock()
raw_image = []
q = queue.LifoQueue()

def read_data():
    global mutex
    global raw_image
    global q
    while(1):
        #print("\t\tTrying to read some data")
        _raw_image = ff.process.stdout.read(width * height * 3)
        #mutex.acquire()
        #raw_image = _raw_image
        #mutex.release()
        q.queue.clear()
        q.put(_raw_image)
        #print("\t\tRead some data")
        #if len(raw_image) == 0:
        #    print("no data. exiting")
        #    break

threading._start_new_thread(write_data, ())

for i in range(125):
    raw_image = ff.process.stdout.read(width * height * 3)

threading._start_new_thread(read_data, ())

done = False
nread = 0
image = numpy.zeros((width,height,3), dtype='uint8')
while not done:
    #for i in range(10):
    #    mutex.acquite()
    #raw_image = ff.process.stdout.read(1920 * 1080 * 3)
    #    mutex.release()
    #if len(raw_image) == 0:
    #    print("no data. exiting")
    #    break
    #mutex.acquire()
    #if len(raw_image) > 0:
        #print("GOt image")

    raw_image = q.get()
    if len(raw_image) > 0:
        image = numpy.fromstring(raw_image, dtype='uint8')
    #q.task_done()
    #else:
        #print("No image")
    #    mutex.release()
    #    continue
    #mutex.release()
    #if len(image) == 0:
    #    continue
    frame = image.reshape((height,width,3))
    #nread = nread + len(raw_image)
    #print("Read some data" + str(nread))

    #ff.process.stdin.write(samplefile.read(1920 * 1080))

    #img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = frame
    #if (ret == False):
    #    break
    #display_image = cv2.resize(img, (width, height))

    x,y,w,h = percept.filter_red_box(img)
    cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

    img = percept.filter_red_rgbimage(img)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.VIDEORESIZE:
            surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            width = event.w
            height = event.h

    screen.blit(pygame.image.frombuffer(img.tostring(), img.shape[1::-1], "RGB"), (0,0))

    pygame.display.flip()