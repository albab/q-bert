#BallFile.py
import pygame,random

class Ball:
    colorList = ((255,0,0), (200,0,200), (0,250,0))

    def updateRect(self):
        self.rect.centerx = int(self.xPos)
        self.rect.bottom = int (self.yPos)

    def setPos(self, pos):
        self.xPos = float(pos[0])
        self.yPos = float(pos[1])
        self.updateRect()

    def createGraphics(self):
        self.roundImage = pygame.surface.Surface((15,15))
        self.roundImage.set_colorkey((0,0,0))
        
        pygame.draw.ellipse(self.roundImage, Ball.colorList[self.myColor], ((0,0),(15,15)))

        self.squashedImage =  pygame.surface.Surface((15,15))
        self.squashedImage.set_colorkey((0,0,0))
        
        pygame.draw.ellipse(self.squashedImage, Ball.colorList[self.myColor], ((0,4),(15,11)))


    def __init__(self, color):
        self.myColor = color
        self.createGraphics()
        self.image = self.roundImage

        self.rect = self.image.get_rect()

        self.IAmMoving = True
        self.targetSquare = (0,0)
        self.oldSquare = (0,0)

        self.setPos((250,0))

        self.xVel = 0.0
        self.yVel = 0.0
        self.paused = False

    def update(self):
        if self.IAmMoving:
            self.xPos+= self.xVel
            self.yPos+= self.yVel

            self.yVel += 0.1
            self.updateRect()
            self.image = self.roundImage
        else:
            if self.paused == False:
                self.paused = True
            else:
                self.oldsquare = self.targetSquare
                if random.randrange(10)<5:
                    self.targetSquare = (self.targetSquare[0]+1,self.targetSquare[1]+1)
                    self.xVel = +0.64
                else:
                    self.targetSquare = (self.targetSquare[0]+1,self.targetSquare[1])
                    self.xVel = -0.64
                self.yVel = -0.5
                self.IAmMoving = True
                self.paused = False
            self.image = self.squashedImage
