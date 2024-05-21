from constants import *
import pygame

class Line(pygame.sprite.Sprite):
    def __init__(self, startx, starty, endx, endy):
        super(Line, self).__init__()
        self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 128))
        self.startx = startx
        self.starty = starty
        self.endx = endx
        self.endy = endy
        self.rect = self.image.get_rect(center = (startx, starty))
        
    def update(self):
        pygame.draw.line(SCREEN, (255, 255, 255), (self.startx, self.starty), (self.endx, self.endy), 1)
        self.mask = pygame.mask.from_surface(self.image)