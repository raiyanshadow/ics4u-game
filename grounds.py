import pygame, math
from constants import *

class Ground(pygame.sprite.Sprite):
    ground = [[clip_image(pygame.image.load('./sprites/ground_big.png').convert_alpha(), (j*32, i*32, 32, 32)) for j in range(3)] for i in range(3)]
    
    for i in range(len(ground)):
        for j in range(len(ground[i])):
            ground[i][j] = pygame.transform.scale(ground[i][j], (64, 64))

    def __init__(self, x, y, type, scroll):
        super().__init__()
        self.type = type
        self.groundmasks = [[pygame.mask.from_surface(self.ground[i][j]) for j in range(3)] for i in range(3)]
        self.image = self.ground[self.type[0]][self.type[1]]
        self.rect = self.image.get_rect(topleft = (x, y))
        self.mask = pygame.mask.from_surface(self.image)
        
        
    def draw(self):
        SCREEN.blit(self.mask.to_surface(setcolor=(255, 255, 255, 0), unsetcolor=(0, 0, 0, 0)), self.rect)
        SCREEN.blit(self.image, self.rect)