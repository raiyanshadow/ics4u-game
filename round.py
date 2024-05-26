import pygame, enemy, boss
from constants import *

class round(pygame.sprite.Sprite):
    def __init__(self):
        super(round, self).__init__()
        self.image = pygame.image.load('./sprites/round.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def start_round(self, round_num):
        if round_num % 5 == 0:
            return boss.Boss(round_num)
        else:
            return enemy.Enemy(round_num)
        
    
    def update_round(self):
        pass

    def end_round(self):
        pass

