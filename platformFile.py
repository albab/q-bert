#platformFile
import pygame

class Platform:

    def __init__(self,row,rowPos):
        self.image = pygame.surface.Surface((35,30))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        pygame.draw.ellipse(self.image,(255,100,200),((0,10),(35,20)))
        self.row = row
        self.rowPos = rowPos
        self.myRider = None
        self.myDirection = 0
        
    def update(self):
        if 0==self.myDirection:
            return
        if 1==self.myDirection:
            if self.rect.bottom>50:
                self.rect.bottom-=2
            else:
                self.myDirection = 2
        if 2==self.myDirection:
            if self.rect.centerx> 251:
                self.rect.centerx -=2
                self.myRider.image = self.myRider.downLeft
            elif self.rect.centerx <249:
                self.rect.centerx += 2
                self.myRider.image = self.myRider.downRight
            else:
                self.myDirection = 3
                self.myRider.xVel = 0
                self.myRider.yVel = 0
        self.myRider.setPos(self.centerOfFace())

    def centerOfFace(self):
        return self.rect.center

    def carryQbert(self, Qbert):
        self.myRider = Qbert
        self.myDirection = 1
