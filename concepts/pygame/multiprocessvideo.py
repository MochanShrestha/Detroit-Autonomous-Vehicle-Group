
import cv2
import pygame
from pygame.locals import *
from multiprocessing import Process, Queue

def make_frames(q):
    vid = cv2.VideoCapture('sample.h264')
    while (True):
        ret, frame = vid.read()
        q.put((ret, frame))
        if (ret == False):
            break

if __name__ == '__main__':
    # Load media files
    hwimg = pygame.image.load('helloworld.png')

    # Multiprocess stuff
    q = Queue()
    p = Process(target=make_frames, args=(q,))
    p.start()

    # Initalize pygame
    pygame.init()
    infoObject = pygame.display.Info()
    screen = pygame.display.set_mode ( (infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN)

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                break

        ret, frame = q.get()
        if (ret == False):
            break
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #img = cv2.resize(img, (infoObject.current_w, infoObject.current_h))

        screen.blit(pygame.image.frombuffer(img.tostring(), img.shape[1::-1], "RGB"), (0, 0))
        screen.blit(hwimg, (100,100))

        pygame.display.flip()

    pygame.quit()