from constants import *
import pygame, player

class HealthBar():
    def __init__(self, x, y, play: player.Player):
        self.x = (x+36)+114*1.5
        self.y = (y+23)+30*1.5-2-20
        self.image = pygame.image.load(os.path.join('sprites', 'hpbar.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*1.5, self.image.get_height()*1.5))
        self.w = (238-36)*1.5
        self.h = (39-23)*1.5
        self.rect = (self.x, self.y, self.w, self.h)
        self.hp = play.hp
        self.max = play.hp
        self.play = play

    def draw(self):
        ratio = self.hp / self.max
        pygame.draw.rect(SCREEN, (0, 0, 0, 64), (self.x, self.y, self.w, self.h))
        pygame.draw.rect(SCREEN, RED, (self.x, self.y, int(self.w * ratio), self.h))
        SCREEN.blit(self.image, (150, 10))
    
    def update(self):
        self.hp = self.play.hp

        if self.hp <= 0:
            self.hp = 0

        self.draw()