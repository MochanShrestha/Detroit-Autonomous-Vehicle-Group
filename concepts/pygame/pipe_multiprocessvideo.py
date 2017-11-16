
import cv2
import pygame
from pygame.locals import *
from multiprocessing import Process, Pipe
import time

def make_frames(conn):
    vid = cv2.VideoCapture('sample.h264')
    while (True):
        ret, frame = vid.read()
        conn.send((ret, frame))
        if (ret == False):
            conn.close()
            break

if __name__ == '__main__':
    # Load media files
    hwimg = pygame.image.load('helloworld.png')

    # Initalize pygame
    pygame.init()
    infoObject = pygame.display.Info()
    screen = pygame.display.set_mode ( (infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN)

    # Create a pipe
    parent_conn, child_conn = Pipe()
    p = Process(target=make_frames, args=(child_conn,))
    p.start()

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                break

        ret, frame = parent_conn.recv()

        if ret == False:
            break

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (infoObject.current_w, infoObject.current_h))

        screen.blit(pygame.image.frombuffer(img.tostring(), img.shape[1::-1], "RGB"), (0, 0))
        screen.blit(hwimg, (100,100))

        pygame.display.flip()

    pygame.quit()