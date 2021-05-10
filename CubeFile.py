# CubeFile.py
import pygame

class Cube:
    colorList = None
    sideColors = None
    topPoly = ((0,15),(24,0),(49,15),(24,30))
    leftPoly = ((0,15),(0,49),(24,64),(24,30))
    rightPoly = ((25,30),(25,64),(49,49),(49,15))

    def drawCube(self):
        self.image.fill((0,0,0))
        pygame.draw.polygon(self.image,Cube.colorList[self.currentColor],Cube.topPoly)
        pygame.draw.polygon(self.image,Cube.sideColors[0],Cube.leftPoly)
        pygame.draw.polygon(self.image,Cube.sideColors[1],Cube.rightPoly)
    
    def __init__(self, inList, inSides = ((200,200,0),(100,150,0)), selectionMode=0):
        if Cube.colorList == None:
            Cube.colorList = inList

        if Cube.sideColors == None:
            Cube.sideColors = inSides

        self.image = pygame.surface.Surface((50,65))
        self.image.set_colorkey((0,0,0))

        self.currentColor = len(Cube.colorList)-1

        self.drawCube()

        self.rect = self.image.get_rect()
        self.mode = selectionMode

    def resetColor(self):
        self.currentColor = len(Cube.colorList)-1
        self.drawCube()
        
    def advanceColor(self):
        if self.currentColor > 0:
            self.currentColor -= 1
            self.drawCube()
        else:
            if self.mode == 0:
                return
            elif self.mode == 1:
                self.currentColor = 1
                self.drawCube()
            else:
                self.resetColor()

    # Location of the center of the top face.
    def centerOfFace(self):
        return (self.rect.centerx, self.rect.top+15)

    def platformRect(self):
        return pygame.rect(self.rect.topleft,(50,30))

    def isNotClear(self):
        return (self.currentColor != 0);
