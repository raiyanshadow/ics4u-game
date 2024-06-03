import pygame, enemy, boss
from constants import *

class round(pygame.sprite.Sprite):
    def __init__(self):
        super(round, self).__init__()
        self.starting = False
        self.special = False
        self.ended = False
        self.roundnum = 0
        self.end_dt = pygame.time.get_ticks()
        self.start_dt = pygame.time.get_ticks()

    def start_round(self, blinker, e: enemy.Enemy, boss: boss.Boss):
        self.starting = True
        text = FONT_48.render(f'round {self.roundnum} start', True, WHITE)
        if blinker: SCREEN.blit(text, (SCREEN_WIDTH//2-text.get_width()/2, 100))
        if pygame.time.get_ticks() - self.start_dt >= 3000:
            self.starting = False
            if self.roundnum % 5 == 1:
                e.queue_list = [[enemy.Bringer()], [enemy.SkeletonA()]]
            if self.roundnum % 5 == 2:
                e.queue_list = [[enemy.SkeletonB(), enemy.Bat()], [enemy.SkeletonA(), enemy.SkeletonB()]]
            if self.roundnum % 5 == 3:
                e.queue_list = [[enemy.SkeletonB(), enemy.SkeletonB()], [enemy.SkeletonA(), enemy.SkeletonB(), enemy.SkeletonB()]]
            if self.roundnum % 5 == 4:
                e.queue_list = [[enemy.Bringer()], [enemy.SkeletonA(), enemy.SkeletonB(), enemy.Bat()], [enemy.Bringer()]]
            e.queue.add(e.queue_list[0])
                
    
    def update_round(self):
        self.ended = True
        self.end_dt = pygame.time.get_ticks()

    def end_round(self):
        if pygame.time.get_ticks() - self.end_dt >= 2000:
            self.ended = False
            self.roundnum += 1
            self.dt = pygame.time.get_ticks()
            self.starting = True
            self.special = False
            self.start_dt = pygame.time.get_ticks()
    
        
            

