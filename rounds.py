import pygame, enemy, boss, math, player, random, healthbar
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
        self.one_third = 1/3
        self.one_eigth = 1/8
        self.changing = False
        self.bosses_killed = 0

    def start_round(self, blinker, e: enemy.Enemy, boss: boss.Boss, p: player.Player):
        self.starting = True
        text = FONT_48.render(f'round {self.roundnum} start', True, WHITE)
        if blinker: SCREEN.blit(text, (SCREEN_WIDTH//2-text.get_width()/2, 100))
        if pygame.time.get_ticks() - self.start_dt >= 3000:
            if self.roundnum == 0: return
            self.starting = False
            if self.roundnum % 5 == 1:
                e.queue_list = [[enemy.Bat(p)]*min(math.ceil(self.bosses_killed+1 * 0.6), 8), [enemy.SkeletonA(p)]*min(math.ceil(self.bosses_killed+1 * 0.8), 5)]
                for i in range(math.ceil(self.bosses_killed * (self.one_third))):
                    e.queue_list.append([enemy.SkeletonB(p)]*min(self.bosses_killed, 5))
            if self.roundnum % 5 == 2:
                e.queue_list = [[enemy.SkeletonB(p), enemy.Bat(p)]*min(math.ceil(self.bosses_killed * 0.5), 4), [enemy.SkeletonA(p), enemy.SkeletonB(p), *[([enemy.Bringer(p)]*min(math.ceil(self.bosses_killed * 0.5), 3)) if self.bosses_killed > 0 else enemy.Bat(p)]]]
            if self.roundnum % 5 == 3:
                e.queue_list = [[enemy.SkeletonB(p), enemy.SkeletonB(p)], [enemy.SkeletonA(p), enemy.SkeletonB(p), enemy.SkeletonB(p)]]
                for i in range(min(math.ceil(self.bosses_killed * (self.one_eigth)), 3)):
                    e.queue_list.append([enemy.Bat(p), enemy.Bat(p)]*min(math.ceil(self.bosses_killed * 0.6), 5))
            if self.roundnum % 5 == 4:
                e.queue_list = [[enemy.Bringer(p)], [enemy.SkeletonA(p), enemy.SkeletonB(p), enemy.Bat(p)], [enemy.Bringer(p)]]
                for i in range(min(math.ceil(self.bosses_killed * (self.one_third)), 2)):
                    e.queue_list.append([enemy.SkeletonB(p), enemy.SkeletonB(p), enemy.Bringer(p)]*min(math.ceil(self.bosses_killed * 0.4), 3))
            if self.roundnum % 5 == 0:
                self.changing = True
                e.queue_list = [[enemy.SkeletonA(p), enemy.SkeletonB(p), enemy.Bringer(p)]*min(math.ceil(self.bosses_killed * 0.6), 2)]
                for i in range(math.ceil(self.bosses_killed * (self.one_third))):
                    e.queue_list.append([enemy.Bat(p), enemy.SkeletonA(p),enemy.Bringer(p)]*min(math.ceil(self.bosses_killed * 0.4), 3))
            e.queue.add(e.queue_list[0])
                
    
    def update_round(self):
        self.ended = True
        self.end_dt = pygame.time.get_ticks()

    def end_round(self, player : player.Player, hbar: healthbar.HealthBar):
        if self.changing: 
            player.bosses_killed += 1
            self.bosses_killed += 1
            player.hp_change = (random.randint(20, 30) * self.bosses_killed)
            player.hp += player.hp_change 
            player.maxhp += player.hp_change
            hbar.hp = player.hp
            hbar.max = player.maxhp
            player.no_hpcharges_change = min(10, player.max_no_hpcharges+1)
            player.no_hpcharges_change = player.no_hpcharges_change - player.max_no_hpcharges
            player.max_no_hpcharges += player.no_hpcharges_change
            player.no_hpcharges = player.max_no_hpcharges
            player.attack_value_change = (random.randint(10, 20) * self.bosses_killed)
            player.attack_value += player.attack_value_change
            self.changing = False
            self.special = True
        if self.special:
            SCREEN.blit(FONT_48.render(f'+{player.hp_change} HP', True, WHITE), (SCREEN_WIDTH//2-100, 100))
            SCREEN.blit(FONT_48.render(f'+{player.attack_value_change} ATK', True, WHITE), (SCREEN_WIDTH//2-100, 150))
            if player.no_hpcharges_change > 0: SCREEN.blit(FONT_48.render(f'+{player.no_hpcharges_change} HP CHARGES', True, WHITE), (SCREEN_WIDTH//2-100, 200))
        
        if pygame.time.get_ticks() - self.end_dt >= (10000 if self.special else 3000):
            self.ended = False
            self.roundnum += 1
            self.dt = pygame.time.get_ticks()
            self.starting = True
            self.special = False
            self.start_dt = pygame.time.get_ticks()
            