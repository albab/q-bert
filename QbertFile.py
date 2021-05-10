#QbertFile.py
import pygame

class Qbert:

    def updateRect(self):
        self.rect.centerx = int(self.xPos)
        self.rect.bottom = int (self.yPos)

    def setPos(self, pos):
        self.xPos = float(pos[0])
        self.yPos = float(pos[1])
        self.updateRect()

    def loadImages(self):
        self.upLeft = pygame.image.load("Graphics/QbertUpLeft.gif")
        self.upRight = pygame.image.load("Graphics/QbertUpRight.gif")
        self.downLeft = pygame.image.load("Graphics/QbertDownLeft.gif")
        self.downRight = pygame.image.load("Graphics/QbertDownRight.gif")
        self.upLeft.set_colorkey((255,255,255))
        self.upRight.set_colorkey((255,255,255))
        self.downLeft.set_colorkey((0,255,0))
        self.downRight.set_colorkey((255,255,255))
        
    def reset(self):
        self.setPos((250,50))
        self.xVel = 0.0
        self.yVel = 0.0
        self.IAmMoving = True
        self.IAmOnPlatform = False
        self.targetSquare = (0,0)
        self.oldSquare = self.targetSquare
        
    def __init__(self):
        self.loadImages()
        self.image = self.downRight
        self.rect = self.image.get_rect()
        self.reset()
       
        
    def update(self):
        if self.IAmMoving and not self.IAmOnPlatform:
            self.xPos += self.xVel
            self.yPos += self.yVel
            self.yVel += 0.1
            self.updateRect()

    def jumpUpRight(self):
        if self.IAmMoving == False:
            self.oldSquare = self.targetSquare
            self.targetSquare = (self.targetSquare[0]-1,self.targetSquare[1])
            self.xVel = 0.48
            self.yVel = -3.5
            self.IAmMoving = True
            self.image = self.upRight

    def jumpUpLeft(self):
        if self.IAmMoving == False:
            self.oldSquare = self.targetSquare
            self.targetSquare = (self.targetSquare[0]-1,self.targetSquare[1]-1)
            self.xVel = -0.48
            self.yVel = -3.5
            self.IAmMoving = True
            self.image = self.upLeft

    def jumpDownRight(self):
        if self.IAmMoving == False:
            self.oldSquare = self.targetSquare
            self.targetSquare = (self.targetSquare[0]+1,self.targetSquare[1]+1)
            self.xVel = +0.48
            self.yVel = -1.75
            self.IAmMoving = True
            self.image = self.downRight

    def jumpDownLeft(self):
        if self.IAmMoving == False:
            self.oldSquare = self.targetSquare
            self.targetSquare = (self.targetSquare[0]+1,self.targetSquare[1])
            self.xVel = -0.48
            self.yVel = -1.70
            self.IAmMoving = True
            self.image = self.downLeft
    
