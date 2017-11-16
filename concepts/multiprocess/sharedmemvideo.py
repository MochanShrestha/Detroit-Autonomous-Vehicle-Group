
import cv2
import pygame
from pygame.locals import *
from multiprocessing import Process, Array, Value
import time
import numpy
import multiprocessing

def generate_frames(a,v, done_decoding):
    # Load video files and start producing the frames
    vid = cv2.VideoCapture('sample.h264')

    # Loop until we reach the end of the file
    while True:
        start = time.time()
        # Get the frame data
        ret, frame = vid.read()
        end = time.time()
        print("Read frame: " + str(end-start))

        # Check if we are done with the data
        if (ret == False):
            done_decoding.value = 1
            break

        start = time.time()
        # Copy over the data to the shared memory
        memoryview(a).cast('B')[:] = frame.flatten()
        end = time.time()
        print("Copy frame: " + str(end-start))

        # Increment a frame number
        v.value = v.value + 1

        print ("Decoding frame " + str(v.value))


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
    p = Process(target=generate_frames, args=(a,v, done_decoding))
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

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        display_image = cv2.resize(img, (infoObject.current_w, infoObject.current_h))

        screen.blit(pygame.image.frombuffer(display_image.tostring(), display_image.shape[1::-1], "RGB"), (0, 0))
        screen.blit(hwimg, (100,100))

        pygame.display.flip()

        print ("Showing frame " + str(frame_no))
        frame_no = frame_no + 1

        if done_decoding.value == 1:
            break

    pygame.quit()