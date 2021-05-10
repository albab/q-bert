#scoreboardFile.py
import pygame

class Scoreboard:

    def resetNumImage(self):
        self.scoreNumsSurf = self.myFont.render("{0:0=6}".format(self.score),True,self.myColor)

    def resetLivesImage(self):
        if self.lives < 0:
            self.gameOver = True
        else:
            self.playerListSurf = pygame.surface.Surface((self.lives*self.miniQBImage.get_width(),self.miniQBImage.get_height()))
            for i in range(0,self.lives):
                self.playerListSurf.blit(self.miniQBImage,(i*self.miniQBImage.get_width(),0))
        
    def resetImage(self):
        width = max(self.scoreNumsSurf.get_width(),self.playerListSurf.get_width())
        self.image = pygame.surface.Surface((width,self.scoreNumsSurf.get_height() + self.playerListSurf.get_height()))
        self.image.blit(self.scoreNumsSurf,(0,0))
        self.image.blit(self.playerListSurf,(0,self.scoreNumsSurf.get_height()))
        self.rect = self.image.get_rect();

    def resetGame(self):
        self.lives = 3
        self.gameOver = False
        self.score = 0
        self.resetNumImage()
        self.resetLivesImage()
        self.resetImage()

    def __init__(self,color):
    
        self.myColor = color
        self.myFont = pygame.font.SysFont("Times",24)
        self.score = 0
        self.lives = 3
        qbImage = pygame.image.load("Graphics/QbertDownRight.gif")
        self.miniQBImage = pygame.transform.scale(qbImage,(qbImage.get_width()//2,qbImage.get_height()//2))
        self.miniQBImage.set_colorkey((255,255,255))
        self.gameOver = False
        self.resetNumImage()
        self.resetLivesImage()
        self.resetImage()

    def decrementLives(self):
        self.lives -= 1
        self.resetLivesImage()
        self.resetImage()

    def increaseScore(self, points):
        self.score += points
        self.resetNumImage()
        self.resetImage()
