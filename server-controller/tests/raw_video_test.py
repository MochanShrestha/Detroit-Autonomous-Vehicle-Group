
import pygame
import cv2
import numpy
#from pygame.locals import *

pygame.init()
width = 1920
height = 1080
screen = pygame.display.set_mode ( (width, height), pygame.RESIZABLE)

f = open("out.raw", "rb")

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.VIDEORESIZE:
            surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            width = event.w
            height = event.h

    raw_image = f.read(1920 * 1080 * 3)
    image = numpy.fromstring(raw_image, dtype='uint8')
    frame = image.reshape((1080,1920,3))

    #img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = frame
    #if (ret == False):
    #    break
    #display_image = cv2.resize(img, (width, height))

    screen.blit(pygame.image.frombuffer(img.tostring(), img.shape[1::-1], "RGB"), (0,0))

    pygame.display.flip()