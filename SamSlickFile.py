#SamSlick.py
import pygame,random

class SamSlick:

    def updateRect(self):
        self.rect.centerx = int(self.xPos)
        self.rect.bottom = int (self.yPos)

    def setPos(self, pos):
        self.xPos = float(pos[0])
        self.yPos = float(pos[1])
        self.updateRect()

    def createGraphics(self):
        self.samImage = pygame.surface.Surface((25,30))
        self.samImage.fill((0,156,0))

        self.slickImage =  pygame.surface.Surface((25,30))
        self.slickImage.fill((0,156,0))

        pygame.draw.rect(self.slickImage,(0,0,0),((0,10),(25,8)))


    def __init__(self, who):
        self.who = who
        self.createGraphics()
        if (0==who):
            self.image = self.samImage
        else:
            self.image = self.slickImage

        self.rect = self.image.get_rect()

        self.IAmMoving = True
        self.targetSquare = (0,0)
        self.oldSquare = (0,0)

        self.setPos((250,50))

        self.xVel = 0.0
        self.yVel = 0.0
        self.paused = False

    def update(self):
        if self.IAmMoving:
            self.xPos+= self.xVel
            self.yPos+= self.yVel

            self.yVel += 0.1
            self.updateRect()
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
