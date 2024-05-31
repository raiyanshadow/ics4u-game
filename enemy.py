import pygame, random, constants, os, player
from constants import *

def initialize_sprites(path, scaler):
    fpath = './sprites/enemy/' + path
    sprites = dict()
    keys = [i.split(' ')[1] for i in os.listdir(fpath)]
    for i in keys: sprites[i] = []
    for fname in os.listdir(fpath):
        if fname.endswith('.png'):
            image = pygame.image.load(fpath + '/' + fname).convert_alpha()
            sprites[fname.split(' ')[1]].append(pygame.transform.scale(image, (image.get_width()*scaler, image.get_height()*scaler)))
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
        self.sprites = initialize_sprites('/round1-4/skeletonA', 4)
        self.image = self.sprites['Idle'][0]
        self.rect = self.image.get_rect()
        self.rect.x = random.choice([-100, 100+constants.SCREEN_WIDTH])
        self.rect.y = 540
        self.mask = pygame.mask.from_surface(self.image)
        self.dead = False
        self.attacking = False
        self.hurt = False
        self.state = 'Idle'
        self.hp = 200
        self.frame = 0
        self.facing = True
        self.dt = pygame.time.get_ticks()
        self.walking = False
        self.oldRect = self.rect.copy()
        self.attack_hitbox = False
        self.iframes = pygame.time.get_ticks()

    def animate(self, fps, player: player.Player):
        if self.frame >= len(self.sprites[self.state]) - 1: 
            self.frame = 0
            self.state = 'Idle'
            if self.walking:
                self.walking = False
            if self.attacking: 
                self.attacking = False
            if self.hurt: self.hurt = False
        if pygame.time.get_ticks() - self.dt > fps:
            if 6 < self.frame  < 12 and self.attacking: 
                attacking_surf = pygame.Surface(self.image.get_size())
                offset = (abs(self.rect.centerx - player.rect.centerx), abs(self.rect.centery - player.rect.centery))
                attacking_mask = pygame.mask.from_surface(attacking_surf)
                if attacking_mask.overlap(player.mask, offset): 
                    player.hurt(10)
            self.frame = (self.frame + 1) 
            self.image = self.sprites[self.state][self.frame]
            self.attack_hitbox = pygame.mask.from_threshold(self.image, WHITE, pygame.color.Color('gray'))
            self.dt = pygame.time.get_ticks()    
            self.rect.size = self.image.get_size()
        if self.facing: 
            SCREEN.blit(self.image, self.rect)
        else: 
            SCREEN.blit(pygame.transform.flip(self.image, True, False), self.rect)
        

    def update(self, player: player.Player):
        range_from_player = (abs(self.rect.centerx - player.rect.centerx)+50, abs(self.rect.centery - player.rect.centery))
        print(player.attack_offset, (player.rect.x, player.rect.y))
        pygame.draw.rect(SCREEN, RED, (range_from_player[0], range_from_player[1], 50, player.image.get_height()))
        if self.oldRect.size != self.rect.size:
            self.rect.top = self.rect.top + (self.oldRect.height - self.rect.height)
            if not self.facing: # if facing levfy6
                self.rect.right = self.rect.right + (self.oldRect.width - self.rect.width)
            self.oldRect = self.rect.copy()
        self.facing = (self.rect.centerx < player.rect.centerx)
        flip = 1 if self.facing else -1
        fps = 100
        offset = (abs(self.rect.centerx - player.rect.centerx), abs(self.rect.centery - player.rect.centery))
        SCREEN.blit(FONT_24.render(str(offset), False, WHITE), (SCREEN_WIDTH//2, 50))
        sightbox = pygame.mask.from_surface(pygame.Surface((100, 100)))
        if self.attacking: self.attack(player)
        x = sightbox.overlap(sightbox, offset)
        if self.dead: 
            fps = 250
            self.death_animation(fps, player)
            return
        elif x and not self.attacking and abs(offset[1]) <= 20: 
            self.state = 'Attack'
            self.attacking = True
            self.frame = 0
            self.attack(player)
        elif self.mask.overlap(player.attack_hitbox, range_from_player) and not self.state == 'Hit' and player.attackBool and pygame.time.get_ticks() - player.iframes > 400: 
            player.iframes = pygame.time.get_ticks()
            self.frame = 0
            self.hurt = True
            self.walking = False
            self.attacking = False
            self.state = 'Hit'
            self.hp -= player.attack_value
            if self.hp <= 0 and not self.dead: 
                self.frame = 0
                self.death_animation(fps, player)
        if self.walking and self.state == 'Walk':
            self.walk()
        if self.frame != 0: self.animate(fps, player)
        elif self.state == 'Idle' or self.state == 'Walk':
            choice = random.choice(['Idle', 'Walk'])
            if choice == 'Idle' and not self.state == 'Idle': 
                self.frame = 0
                self.state = choice
            elif choice == 'Walk' and not self.state == 'Walk': 
                self.state = choice
                self.walking = True
        
        self.animate(fps, player)
        
    def attack(self, player: player.Player):
        self.attacking = True

    def death_animation(self, fps, player: player.Player):
        self.state = 'Dead'
        self.dead = True
        self.animate(fps, player)
        if self.frame >= 7: self.kill()
        
    def walk(self):
        self.rect.x += 1 * (1 if self.facing else -1)    
        
class SkeletonB(Enemy):
    def __init__(self):
        super(SkeletonB, self).__init__()
        self.sprites = initialize_sprites('/round1-4/skeletonB', 4)
        self.image = self.sprites['Idle'][0]
        self.rect = self.image.get_rect()
        self.rect.x = random.choice([-100, 100+constants.SCREEN_WIDTH])
        self.rect.y = 470
        self.mask = pygame.mask.from_surface(self.image)
        self.dead = False
        self.attacking = False
        self.hurt = False
        self.state = 'Idle'
        self.hp = 400
        self.frame = 0
        self.facing = True
        self.dt = pygame.time.get_ticks()
        self.walking = False
        self.oldRect = self.rect.copy()
        self.attack_hitbox = False
        self.iframes = pygame.time.get_ticks()

    def animate(self, fps, player: player.Player):
        if self.frame >= len(self.sprites[self.state]) - 1: 
            self.frame = 0
            self.state = 'Idle'
            if self.walking:
                self.walking = False
            if self.attacking: 
                self.attacking = False
            if self.hurt: self.hurt = False
        if pygame.time.get_ticks() - self.dt > fps:
            if (5 == self.frame or self.frame == 7d)  and self.attacking: 
                attacking_surf = pygame.Surface(self.image.get_size())
                offset = (abs(self.rect.centerx - player.rect.centerx), abs(self.rect.centery - player.rect.centery))
                attacking_mask = pygame.mask.from_surface(attacking_surf)
                if attacking_mask.overlap(player.mask, offset): 
                    player.hurt(10)
            self.frame = (self.frame + 1) 
            self.image = self.sprites[self.state][self.frame]
            self.attack_hitbox = pygame.mask.from_threshold(self.image, WHITE, pygame.color.Color('gray'))
            self.dt = pygame.time.get_ticks()    
            self.rect.size = self.image.get_size()
        if self.facing: 
            SCREEN.blit(self.image, self.rect)
        else: 
            SCREEN.blit(pygame.transform.flip(self.image, True, False), self.rect)
        

    def update(self, player: player.Player):
        range_from_player = (abs(self.rect.centerx - player.rect.centerx)+50, abs(self.rect.centery - player.rect.centery))
        print(player.attack_offset, (player.rect.x, player.rect.y))
        pygame.draw.rect(SCREEN, RED, (range_from_player[0], range_from_player[1], 50, player.image.get_height()))
        if self.oldRect.size != self.rect.size:
            self.rect.top = self.rect.top + (self.oldRect.height - self.rect.height)
            if not self.facing: # if facing levfy6
                self.rect.right = self.rect.right + (self.oldRect.width - self.rect.width)
            self.oldRect = self.rect.copy()
        self.facing = (self.rect.centerx < player.rect.centerx)
        flip = 1 if self.facing else -1
        fps = 100
        offset = (abs(self.rect.centerx - player.rect.centerx), abs(self.rect.centery - player.rect.centery))
        SCREEN.blit(FONT_24.render(str(offset), False, WHITE), (SCREEN_WIDTH//2, 50))
        sightbox = pygame.mask.from_surface(pygame.Surface((100, 100)))
        if self.attacking: self.attack(player)
        x = sightbox.overlap(sightbox, offset)
        if self.dead: 
            fps = 250
            self.death_animation(fps, player)
            return
        elif x and not self.attacking and abs(offset[1]) <= 20: 
            self.state = 'Attack'
            self.attacking = True
            self.frame = 0
            self.attack(player)
        elif self.mask.overlap(player.attack_hitbox, range_from_player) and not self.state == 'Hit' and player.attackBool and pygame.time.get_ticks() - player.iframes > 400: 
            self.iframes = pygame.time.get_ticks()
            self.frame = 0
            self.hurt = True
            self.walking = False
            self.attacking = False
            self.state = 'Hit'
            self.hp -= player.attack_value
            if self.hp <= 0 and not self.dead: 
                self.frame = 0
                self.death_animation(fps, player)
        if self.walking and self.state == 'Walk':
            self.walk()
        if self.frame != 0: self.animate(fps, player)
        elif self.state == 'Idle' or self.state == 'Walk':
            choice = random.choice(['Idle', 'Walk'])
            if choice == 'Idle' and not self.state == 'Idle': 
                self.frame = 0
                self.state = choice
            elif choice == 'Walk' and not self.state == 'Walk': 
                self.frame = 0
                self.state = choice
                self.walking = True
        
        self.animate(fps, player)
        
    def attack(self, player: player.Player):
        self.attacking = True

    def death_animation(self, fps, player: player.Player):
        self.state = 'Death'
        self.dead = True
        self.animate(fps, player)
        if self.frame >= 7: self.kill()
        
    def walk(self):
        self.rect.x += 1 * (1 if self.facing else -1)    
        
