import pygame, random, constants, os, player
from constants import *

def initialize_sprites(path):
    fpath = './sprites/enemy/' + path
    sprites = dict()
    keys = [i.split(' ')[1] for i in os.listdir(fpath)]
    for i in keys: sprites[i] = []
    for fname in os.listdir(fpath):
        if fname.endswith('.png'):
            image = pygame.image.load(fpath + '/' + fname).convert_alpha()
            sprites[fname.split(' ')[1]].append(pygame.transform.scale(image, (image.get_width()*4, image.get_height()*4)))
    return sprites

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.queue = pygame.sprite.Group()
    def update(self, player: player.Player):
        self.queue.update(player)


class SkeletonA(Enemy):
    def __init__(self):
        super(SkeletonA, self).__init__()
        self.surf = pygame.Surface((64, 64))
        self.sprites = initialize_sprites('/round1-4/skeletonA')
        self.image = self.sprites['Idle'][0]
        self.rect = self.surf.get_rect()
        self.rect.x = random.choice([-100, 100+constants.SCREEN_WIDTH])
        self.rect.y = 540
        self.mask = pygame.mask.from_surface(self.image)
        self.dead = False
        self.attacking = False
        self.hurt = False
        self.state = 'Idle'
        self.hp = 100
        self.frame = 0
        self.facing = True
        self.dt = pygame.time.get_ticks()
        self.walking = False

    def animate(self, fps):
        if self.frame >= len(self.sprites[self.state]) - 1: 
            self.frame = 0
            self.state = 'Idle'
            if self.walking:
                self.walking = False
            if self.attacking: 
                self.attacking = False
            if self.hurt: self.hurt = False
        if pygame.time.get_ticks() - self.dt > fps:
            self.frame = (self.frame + 1) 
            self.image = self.sprites[self.state][self.frame]
            self.attack_hitbox = pygame.mask.from_threshold(self.image, WHITE, pygame.color.Color('gray'))
            self.dt = pygame.time.get_ticks()
        if self.facing: 
            SCREEN.blit(self.image, self.rect)
        else: 
            SCREEN.blit(pygame.transform.flip(self.image, True, False), self.rect)

    def update(self, player: player.Player):
        self.facing = (self.rect.x < player.rect.x)
        flip = 1 if self.facing else -1
        fps = 100
        offset = (self.rect.x - player.rect.x - (self.image.get_width() if self.facing else 0), self.rect.y - player.rect.y)
        print(offset)
        sightbox = pygame.mask.from_surface(pygame.Surface((100, 100)))
        SCREEN.blit(pygame.Surface((100, 100)), (self.rect.x - player.rect.x - 40*flip, self.rect.y - player.rect.y))
        x = sightbox.overlap(sightbox, offset)
        if self.dead: 
            fps = 250
            self.death_animation(fps)
            return
        elif x and not self.attacking and abs(offset[1]) <= 20: 
            self.state = 'Attack'
            self.attacking = True
            self.frame = 0
            self.attack(player)
        elif x and self.state == 'Attack' and not player.state == 'hurt':  
            fps = 200
            player.hurt(15)
            print('hurt')
        elif self.mask.overlap(player.mask, offset) and not self.state == 'Hit' and player.attackBool: 
            self.frame = 0
            self.hurt = True
            self.walking = False
            self.attacking = False
            self.state = 'Hit'
            self.hp -= player.attack_value
            if self.hp <= 0 and not self.dead: 
                self.frame = 0
                self.death_animation(fps)
        if self.walking and self.state == 'Walk':
            self.walk()
        if self.frame != 0: self.animate(fps)
        elif self.state == 'Idle' or self.state == 'Walk':
            choice = random.choice(['Idle', 'Walk'])
            if choice == 'Idle' and not self.state == 'Idle': 
                self.frame = 0
                self.state = choice
            elif choice == 'Walk' and not self.state == 'Walk': 
                self.state = choice
                self.walking = True
        self.animate(fps)
        
    def attack(self, player: player.Player):
        self.attacking = True
        attacking_surf = pygame.Surface(self.image.get_size())
        offset = (self.rect.x - player.rect.x - 50*(1 if self.facing else -1), self.rect.y - player.rect.y)
        print(offset)
        attacking_mask = pygame.mask.from_surface(attacking_surf)
        pygame.draw.circle(attacking_surf, RED, (10, 10), 10)
        if attacking_mask.overlap(player.mask, offset): 
            player.hurt(10)

    def death_animation(self, fps):
        self.state = 'Dead'
        self.dead = True
        self.animate(fps)
        if self.frame >= 7: self.kill()
        
    def walk(self):
        self.rect.x += 1 * (1 if self.facing else -1)    
        
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
        
