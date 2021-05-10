#curseFile.py
import pygame

class Curse:

    def __init__(self):
        self.image = pygame.image.load("Graphics/Curses.gif")
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.iAmShowing = False
        self.counter = 0

    def update(self):
        if self.iAmShowing:
            self.counter += 1
            if self.counter>50:
                self.iAmShowing = False
                self.counter = 0
