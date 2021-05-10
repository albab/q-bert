import pygame, sys, os
from pygame.locals import *

#----- pygame setup example file

#----- readEvents
def readEvents(events):
    for event in events:
        if event.type == QUIT:
            pygame.quit() #close window
            sys.exit(0)   #quit program.

#------ updateScreen
def updateScreen():
    screen = pygame.display.get_surface()
    screen.fill ((0,0,0)) # clear the screen with black --> (0,0,0)
    pygame.display.flip()

#------ initialize
# Start pygame
def initialize():
    pygame.init()
    global window
    window = pygame.display.set_mode((500,400))
    
    

#------ animateStep
def animateStep():
    pass

#------ gameLoop
def gameLoop(checkEvents=True, animateObjects=True, refreshScreen=True):
    while(True):
        if (checkEvents):
            readEvents(pygame.event.get())
        if (animateObjects):
            animateStep()
        if (refreshScreen):
            updateScreen()
            
initialize()
updateScreen()

gameLoop(True,False,False)



