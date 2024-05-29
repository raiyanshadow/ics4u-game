import pygame, random, constants, os, player
from constants import *

def initialize_sprites(path):
    fpath = './sprites/enemy/' + path
    sprites = dict()
    keys = [i.split(' ')[1] for i in os.listdir(fpath)]
    for i in keys: sprites[i] = []
    for fname in os.listdir(fpath):
        if fname.endswith('.png'):
            sprites[fname.split(' ')[1]].append(pygame.transform.scale(pygame.image.load(fpath + '/' + fname).convert_alpha(), (128, 128)))
    return sprites

def unique(lst):
    return list(set(lst))

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.queue = pygame.sprite.Group()
    def update(self, player: player.Player):
        self.queue.update(player)


class SkeletonA(Enemy):
    def __init__(self):
        super(SkeletonA, self).__init__()
        self.sprites = initialize_sprites('/round1-4/skeletonA')
        self.surf = pygame.Surface((128, 128))
        self.image = self.sprites['Idle'][0]
        self.rect = self.surf.get_rect()
        self.rect.x = random.choice([1, -1]) * 100
        self.rect.y = 560
        self.mask = pygame.mask.from_surface(self.image)
        self.dead = False
        self.attacking = False
        self.state = 'Idle'
        self.attack_hitbox = pygame.mask.from_threshold(self.image, WHITE, pygame.color.Color('gray'))
        self.hp = 100
        self.frame = 0
        self.facing = True
        self.dt = pygame.time.get_ticks()
        self.animqueue = []

    def animate(self, fps):
        if self.animqueue != []: self.state = self.animqueue[-1]
        if pygame.time.get_ticks() - self.dt > fps:
            self.frame = (self.frame + 1) % len(self.sprites[self.state])
            self.image = self.sprites[self.state][self.frame]
            self.attack_hitbox = pygame.mask.from_threshold(self.image, WHITE, pygame.color.Color('gray'))
            self.dt = pygame.time.get_ticks()
        if self.frame == len(self.sprites[self.state]) - 1 and self.state != 'Dead': self.state = 'Idle'
        if self.facing: 
            SCREEN.blit(self.image, self.rect)
            SCREEN.blit(self.attack_hitbox.to_surface(setcolor=(255, 255, 255, 255), unsetcolor=(0, 0, 0, 0)), self.rect)
        else: 
            SCREEN.blit(pygame.transform.flip(self.image, True, False), self.rect)
            SCREEN.blit(pygame.transform.flip(self.attack_hitbox.to_surface(setcolor=(255, 255, 255, 255), unsetcolor=(0, 0, 0, 0)), True, False), self.rect)

    def update(self, player: player.Player):
        self.facing = (self.rect.x < player.rect.x)
        fps = 100
        offset = (self.rect.x - player.rect.x, self.rect.y - player.rect.y)
        print(offset)
        x = self.attack_hitbox.overlap(player.mask, offset)
        if self.dead: 
            fps = 250
            self.death_animation(fps)
            return
        elif abs(offset[0]) <= 50 and not self.state == 'Attack' and abs(offset[1]) <= 20: 
            self.state = 'Attack'
            self.frame = 0
        elif x and self.state == 'Attack' and not player.state == 'hurt':  
            fps = 200
            pygame.draw.circle(SCREEN, RED, (offset[0] + self.rect.x, offset[1] + self.rect.y), 10)
            player.hurt(15)
        elif self.mask.overlap(player.mask, offset) and not self.state == 'Hit' and player.attackBool: 
            self.frame = 0
            self.state = 'Hit'
            self.hp -= player.attack_value
            if self.hp <= 0: 
                self.frame = 0
                self.death_animation(fps)
        
        if self.state == 'Walk':
                self.frame = 0
                self.walk()
        if self.frame != 0: self.animate(fps)
        elif self.state == 'Idle' or self.state == 'Walk':
            choice = random.choice(['Idle', 'Walk'])
            if choice == 'Idle' and not self.state == 'Idle': 
                self.frame = 0
                self.state = choice
            elif choice == 'Walk' and not self.state == 'Walk': self.state = choice
        self.animate(fps)
        
    def death_animation(self, fps):
        self.state = 'Dead'
        self.dead = True
        self.animate(fps)
        if self.frame == len(self.sprites[self.state]) - 1: 
            self.kill()
        
    def walk(self):
        print(self.rect)
        self.rect.x += 2 * (1 if self.facing else -1)    
        
class SkeletonB(Enemy):
    def __init__(self):
        super(SkeletonB, self).__init__()
        self.sprites = initialize_sprites('round1-4/skeletonB', 5)
        self.image = self.sprites['idle'][0]
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100
        self.mask = pygame.mask.from_surface(self.image)
        self.dead = False
        self.attacking = False

    def animate(self):
        if not self.dead: self.a_frame = (self.a_frame + 1) % len(self.sprites[self.state])
        self.image = self.sprites[self.state][self.a_frame]
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.animate()

    def death_animation(self):
        self.state = 'death'
        
