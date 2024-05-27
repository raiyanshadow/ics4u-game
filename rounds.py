import pygame, enemy, boss
from constants import *

class round(pygame.sprite.Sprite):
    def __init__(self):
        super(round, self).__init__()
        self.starting = False
        self.special = False
        self.roundnum = 1

    def start_round(self, dt, blinker, enemy, boss):
        self.starting = True
        text = FONT_48.render(f'round {self.roundnum} start', True, WHITE)
        if blinker: SCREEN.blit(text, (SCREEN_WIDTH//2-text.get_width()/2, 50))
        if pygame.time.get_ticks() - dt >= 3000:
            if self.roundnum % 5 == 0:
                self.special = True
                return boss.Boss()
            else:
                return enemy.Enemy()
    
    def update_round(self):
        pass

    def end_round(self):
        pass
    
        
            

