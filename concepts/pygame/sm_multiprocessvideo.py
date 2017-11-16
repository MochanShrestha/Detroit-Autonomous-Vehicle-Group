
import cv2
import pygame
from pygame.locals import *
from multiprocessing import Process, Array
import time
import numpy as np

def make_frames(sm):
    print("Starting frame production ...")
    frame_no = 0
    vid = cv2.VideoCapture('sample.h264')
    while (True):
        ret, frame = vid.read()
        sm = frame
        if (ret == False):
            break
        time.sleep(0.02)
        frame_no = frame_no + 1
        #print("Frame " + str(frame_no))

if __name__ == '__main__':
    # Load media files
    hwimg = pygame.image.load('helloworld.png')

    # Initalize pygame
    pygame.init()
    infoObject = pygame.display.Info()
    screen = pygame.display.set_mode ( (infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN)

    # Make the shared memory
    image_size = 1920 * 1080 * 3
    print("Creating shared memory of size " + str(image_size) + " ...")
    sm = Array('d', image_size)
    print("Starting process ...")
    p = Process(target=make_frames, args=(sm,))
    p.start()

    # Main loop
    print("Starting main loop ...")
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                break

        frame = np.frombuffer(sm.get_obj())
        print(type(sm))
        print(type(frame))
        print(frame.size)

        #if ret == False:
        #    break

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (infoObject.current_w, infoObject.current_h))

        screen.blit(pygame.image.frombuffer(img.tostring(), img.shape[1::-1], "RGB"), (0, 0))
        screen.blit(hwimg, (100,100))

        pygame.display.flip()

    pygame.quit()