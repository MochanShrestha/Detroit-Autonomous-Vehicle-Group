
import cv2
import pygame
from pygame.locals import *
from multiprocessing import Process, Array, Value
import time
import numpy
import multiprocessing

#from framesopencv import generate_frames
#from framesffmpy import generate_frames_ffmpy
from framesffmpynclib import generate_frames_ffmpynclib


if __name__ == '__main__':
    # Read the image to super-impose
    hwimg = pygame.image.load('helloworld.png')

    # Initalize pygame
    pygame.init()
    infoObject = pygame.display.Info()
    screen = pygame.display.set_mode ( (infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN)

    # Setup the shared memory and Create, start, and finish the child process
    v = Value('i', 0)
    done_decoding = Value('i', 0)
    a = multiprocessing.RawArray(numpy.ctypeslib.ctypes.c_uint8, 1080*1920*3)
    #p = Process(target=generate_frames, args=(a,v, done_decoding))
    #p = Process(target=generate_frames_ffmpy, args=(a, v, done_decoding))
    p = Process(target=generate_frames_ffmpynclib, args=(a, v, done_decoding))
    p.start()

    frame_no = 0

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                break

        frame = numpy.frombuffer(a, numpy.ctypeslib.ctypes.c_uint8)
        frame.shape = (1080, 1920, 3)

        # OpenCV is the only one that decodes as BGR and has to be reversed
        #img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        img = frame
        display_image = cv2.resize(img, (infoObject.current_w, infoObject.current_h), interpolation=cv2.INTER_NEAREST)

        screen.blit(pygame.image.frombuffer(display_image.tostring(), display_image.shape[1::-1], "RGB"), (0, 0))
        screen.blit(hwimg, (100,100))

        pygame.display.flip()
        frame_no = v.value

        #print ("Showing frame " + str(frame_no))

        if done_decoding.value == 1:
            break

    pygame.quit()