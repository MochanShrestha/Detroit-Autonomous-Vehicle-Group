
import ffmpy
import pygame
import cv2
import subprocess
import numpy
import errno
import time
import threading
from pygame.locals import *

# ff = ffmpy.FFmpeg(inputs={'pipe:0': '-f rawvideo -pix_fmt rgb24 -s:v 640x480'}, outputs={'pipe:1': '-v:c h264 -f mp4'})
#ff = ffmpy.FFmpeg(inputs={'pipe:0': '-f h264'}, outputs={'pipe:1': '-f rawvideo -pix_fmt rgb24'})
ff = ffmpy.FFmpeg(inputs={'pipe:0': '-f h264'}, outputs={'pipe:1': '-f rawvideo -pix_fmt rgb24'})
#ff = ffmpy.FFmpeg(inputs={'sample.h264': None}, outputs={'pipe:1': '-f rawvideo -pix_fmt rgb24'})
print (ff.cmd)
try:
    ff.process = subprocess.Popen(
        ff._cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
except OSError as e:
    if e.errno == errno.ENOENT:
        raise ffmpy.FFExecutableNotFoundError("Executable '{0}' not found".format(ff.executable))
    else:
        raise
#ff.run(input_data=open('sample.h264', 'rb').read(), stdout=subprocess.PIPE)

samplefile = open('sample.h264', 'rb')

def write_data():
    while(1):
        print("Trying to write some data")
        fdata = samplefile.read(1920*1080)
        if len(fdata) == 0:
            print("Finished writing file")
            ff.process.stdin.close()
            break;
        ff.process.stdin.write(fdata)
        print("Wrote some data")

threading._start_new_thread(write_data, ())

pygame.init()
width = 1920
height = 1080
screen = pygame.display.set_mode ( (width, height), pygame.RESIZABLE)

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.VIDEORESIZE:
            surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            width = event.w
            height = event.h

    print("Trying to read some data")
    raw_image = ff.process.stdout.read(1920 * 1080 * 3)
    print("Read some data")
    if len(raw_image) == 0:
        break
    image = numpy.fromstring(raw_image, dtype='uint8')
    frame = image.reshape((1080,1920,3))

    #ff.process.stdin.write(samplefile.read(1920 * 1080))

    #img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = frame
    #if (ret == False):
    #    break
    #display_image = cv2.resize(img, (width, height))

    screen.blit(pygame.image.frombuffer(img.tostring(), img.shape[1::-1], "RGB"), (0,0))

    pygame.display.flip()