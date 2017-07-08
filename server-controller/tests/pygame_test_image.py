
import pygame
import cv2
#from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode ( (400, 300), pygame.RESIZABLE)

sample_image = cv2.imread("sample.jpg")
sample_image = cv2.cvtColor(sample_image, cv2.COLOR_BGR2RGB)
display_image = cv2.resize(sample_image, (400, 300))

done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.VIDEORESIZE:
            surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            display_image = cv2.resize(sample_image, (event.w, event.h))

    screen.blit(pygame.image.frombuffer(display_image.tostring(), display_image.shape[1::-1], "RGB"), (0,0))

    pygame.display.flip()