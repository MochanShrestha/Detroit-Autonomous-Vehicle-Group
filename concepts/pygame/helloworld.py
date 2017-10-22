
import cv2
import pygame
from pygame.locals import *

# Load media files
vid = cv2.VideoCapture('sample.h264')
hwimg = pygame.image.load('helloworld.png')

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

    ret, frame = vid.read()
    if (ret == False):
        break
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    img = cv2.resize(img, (infoObject.current_w, infoObject.current_h), interpolation=cv2.INTER_NEAREST)

    screen.blit(pygame.image.frombuffer(img.tostring(), img.shape[1::-1], "RGB"), (0, 0))
    screen.blit(hwimg, (100,100))

    pygame.display.flip()

pygame.quit()