#CoilyFile.py
import pygame, random

class Coily:

    def updateRect(self):
        self.rect.centerx = int(self.xPos)
        self.rect.bottom = int (self.yPos)

    def setPos(self, pos):
        self.xPos = float(pos[0])
        self.yPos = float(pos[1])
        self.updateRect()

    def __init__(self, prey):
        self.tallImage = pygame.image.load("Graphics/CoilyTall.gif")
        self.tallImage.set_colorkey((255,255,255))

        self.shortImage = pygame.image.load("Graphics/CoilyShort.gif")
        self.shortImage.set_colorkey((255,255,255))

        self.image = self.tallImage
        
        self.rect = self.image.get_rect()
        self.bounceCounter = 0

        self.xVel = 0.0
        self.yVel = 0.0

        self.IAmMoving = False
        self.bounceCounter = 0
        self.targetSquare = (0,0)
        self.oldSquare = (0,0)

        self.myPrey = prey

    def jumpUpRight(self):
        if self.IAmMoving == False:
           # print "jump up right"
            self.oldSquare = self.targetSquare
            self.targetSquare = (self.targetSquare[0]-1,self.targetSquare[1])
            self.xVel = 0.48
            self.yVel = -3.5
            self.IAmMoving = True

    def jumpUpLeft(self):
        if self.IAmMoving == False:
            self.oldSquare = self.targetSquare
            self.targetSquare = (self.targetSquare[0]-1,self.targetSquare[1]-1)
            self.xVel = -0.48
            self.yVel = -3.5
            self.IAmMoving = True

    def jumpDownRight(self):
        if self.IAmMoving == False:
            self.oldSquare = self.targetSquare
            self.targetSquare = (self.targetSquare[0]+1,self.targetSquare[1]+1)
            self.xVel = +0.48
            self.yVel = -1.75
            self.IAmMoving = True

    def jumpDownLeft(self):
        if self.IAmMoving == False:
            self.oldSquare = self.targetSquare
            self.targetSquare = (self.targetSquare[0]+1,self.targetSquare[1])
            self.xVel = -0.48
            self.yVel = -1.70
            self.IAmMoving = True

    def update(self):
        if self.IAmMoving:
            self.xPos+= self.xVel
            self.yPos+= self.yVel

            self.yVel += 0.1
            if self.bounceCounter<5:
                self.bounceCounter+=1
            else:
                self.image=self.tallImage
            self.updateRect()
        else:
            self.image=self.shortImage
            if self.bounceCounter%2 == 0:
                self.xVel =0
                self.yVel = -1.5
                
            else:
                leftRightCriteria = self.targetSquare[0]-self.myPrey.targetSquare[0] - 2*(self.targetSquare[1]-self.myPrey.targetSquare[1])
               # print "Coily's position is {0}, prey at {1}, l-r criteria is {2}".format(self.targetSquare,self.myPrey.targetSquare, leftRightCriteria)
                if self.targetSquare[0]>self.myPrey.targetSquare[0]:
                    if leftRightCriteria<0:
                        self.jumpUpLeft()
                    elif leftRightCriteria>0 or random.randrange(10)<5:
                        self.jumpUpRight()
                    else:
                        self.jumpUpLeft()
                elif self.targetSquare[0] <6 and (self.targetSquare[0]<self.myPrey.targetSquare[0] or random.randrange(10)<5):
                    if leftRightCriteria<0:
                        self.jumpDownLeft()
                    elif leftRightCriteria>0 or random.randrange(10)<5:
                        self.jumpDownRight()
                    else:
                        self.jumpDownLeft()
                else:
                    if self.targetSquare[1] >self.myPrey.targetSquare[1]:
                        print(self.jumpUpLeft())
                    else:
                        print(self.jumpUpRight())
            self.IAmMoving = True
            self.bounceCounter += 1
