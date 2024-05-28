import pygame, random, constants, os, player
from constants import *

def initialize_sprites(path, sep):
    sprites = dict()
    for i in os.listdir('./sprites/enemy/' + path):
        sprites[i.split(' ')[1].remove('.png')] = []
    for i in list(sprites.keys()):
        image = pygame.image.load('./sprites/enemy/'+path+'/'+i+'.png').convert_alpha()
        for j in range(image.get_width()//(8*sep)):
            sprites[i].append(image.subsurface(j*(8*sep), 0, 8*sep, image.get_height()))


class Enemy(pygame.sprite.Sprite):
    def __init__(self, type):
        super(Enemy, self).__init__()
        self.type = type
        self.queue = []
    def make_group(self):
        return pygame.sprite.Group(self.queue)
    def update(self, dt, group: pygame.sprite.Group, player: player.Player):
        group.update(dt, player)


class SkeletonA(Enemy):
    def __init__(self):
        super(SkeletonA, self).__init__()
        self.sprites = initialize_sprites('round1-4/skeletonA', 5)
        self.surf = pygame.Surface(())
        self.image = self.sprites['Idle'][0]
        self.rect = self.surf.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.image.get_width())
        self.rect.y = 560
        self.mask = pygame.mask.from_surface(self.image)
        self.dead = False
        self.attacking = False
        self.state = 'idle'
        self.sightbox = pygame.Rect(self.rect.x//2, self.rect.y//2, 30, 20)
        self.mask_sightbox = pygame.mask.from_surface(self.sightbox)
        self.attack_hitbox = pygame.mask.from_threshold(self.image, WHITE, pygame.color('gray'))
        self.hp = 100
        self.frame = 0
        self.facing = True

    def animate(self, dt, fps):
        if pygame.time.get_ticks() - dt > fps:
            if not self.dead: self.a_frame = (self.a_frame + 1) % len(self.sprites[self.state])
            self.image = self.sprites[self.state][self.a_frame]
            self.mask = pygame.mask.from_surface(self.image)
        if self.facing: SCREEN.blit(self.image, self.rect)
        else: SCREEN.blit(pygame.transform.flip(self.image, True, False), self.rect)

    def update(self, dt, player: player.Player):
        self.facing = not player.facing
        fps = 150
        if self.dead: 
            self.death_animation(dt, fps)
            return
        if pygame.sprite.collide_mask(self.mask_sightbox, player.mask) and not self.state == 'Attack': 
            self.frame = 0
            self.state = 'Attack'
        elif pygame.sprite.collide_mask(self.attack_hitbox, player.mask) and not self.state == 'Attack' and not player.state == 'hurt':  
            self.frame = 0
            player.hurt()
        elif pygame.sprite.collide_mask(self.mask, player.attack_hitbox) and not self.state == 'Hit': 
            self.frame = 0
            self.state = 'Hit'
            self.hp -= player.attack_value
            if self.hp <= 0: 
                self.frame = 0
                self.death_animation(dt, fps)
        else:
            choice = random.choice(['Idle', 'Walk'])
            if choice == 'Idle' and not self.state == 'Idle': 
                self.state = choice
            elif choice == 'Walk' and not self.state == 'Walk': self.state = choice
            if self.state == 'Walk':
                self.walk()
        self.animate(dt, self.state, fps)
        
    def death_animation(self, dt, fps,):
        self.state = 'death'
        self.dead = True
        self.animate(dt, fps)
        if self.frame == len(self.sprites[self.state]) - 1: 
            self.kill()
        
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
        
