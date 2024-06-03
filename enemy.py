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
        self.queue_list = []
        self.queue = pygame.sprite.Group()
        self.index = 0
    def update(self):
        self.queue.update()
    def add_to_queue(self):
        self.queue.add(self.queue_list[0])

class SkeletonA(Enemy):
    def __init__(self, player: player.Player):
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
        self.hp = 200 + (75*(player.bosses_killed))
        self.frame = 0
        self.facing = True
        self.dt = pygame.time.get_ticks()
        self.walking = False
        self.oldRect = self.rect.copy()
        self.attack_hitbox = False
        self.iframes = pygame.time.get_ticks()
        self.speed = 1
        self.attack_val = 15 + (12.5*(player.bosses_killed))

    def animate(self, fps, player: player.Player):
        if self.frame == len(self.sprites[self.state]) - 1: 
            self.frame = 0
            self.state = 'Idle'
            if self.walking:
                self.walking = False
            if self.attacking: 
                self.attacking = False
            if self.hurt: self.hurt = False
            if self.dead: 
                player.score += 30 + ((player.bosses_killed + 1) * (20))
                self.kill()
        if pygame.time.get_ticks() - self.dt > fps:
            if 6 < self.frame  < 12 and self.attacking: 
                attacking_surf = pygame.Surface(self.image.get_size())
                offset = (abs(self.rect.centerx - player.rect.centerx), abs(self.rect.centery - player.rect.centery))
                attacking_mask = pygame.mask.from_surface(attacking_surf)
                if attacking_mask.overlap(player.mask, offset): 
                    player.hurt(self.attack_val)
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
        range_from_player = (abs(self.rect.centerx - player.rect.centerx + (30 if self.facing else -30)), abs(self.rect.centery - player.rect.centery + 50))
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
        sightbox = pygame.mask.from_surface(pygame.Surface((180, 100)))
        if self.attacking: self.attack(player)
        x = sightbox.overlap(sightbox, offset)
        if self.dead: 
            fps = 250
            self.animate(fps, player)
            return
        elif x and not self.attacking and abs(offset[1]) <= 20: 
            self.state = 'Attack'
            self.attacking = True
            self.frame = 0
            self.attack(player)
        elif self.mask.overlap(player.attack_hitbox, range_from_player) and not self.state == 'Hit' and player.attackBool and pygame.time.get_ticks() - self.iframes > 600: 
            self.iframes = pygame.time.get_ticks()
            self.frame = 0
            self.hurt = True
            self.walking = False
            self.attacking = False
            self.state = 'Hit'
            self.hp -= player.attack_value
            if self.hp <= 0 and not self.dead: 
                self.state = 'Dead'
                self.dead = True
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
        
    def walk(self):
        self.rect.x += self.speed * (1 if self.facing else -1)    
        
class SkeletonB(Enemy):
    def __init__(self, player):
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
        self.speed = 1
        self.attack_val = 25

    def animate(self, fps, player: player.Player):
        if self.frame == len(self.sprites[self.state]) - 1: 
            self.frame = 0
            self.state = 'Idle'
            if self.walking:
                self.walking = False
            if self.attacking: 
                self.attacking = False
            if self.hurt: self.hurt = False
            if self.dead: 
                player.score += 50 + ((player.bosses_killed + 1) * (20))
                self.kill()
        if pygame.time.get_ticks() - self.dt > fps:
            if (4 == self.frame or self.frame == 8)  and self.attacking: 
                attacking_surf = pygame.Surface(self.image.get_size())
                offset = (abs(self.rect.centerx - player.rect.centerx ), abs(self.rect.centery - player.rect.centery))
                attacking_mask = pygame.mask.from_surface(attacking_surf)
                if attacking_mask.overlap(player.mask, offset): 
                    player.hurt(self.attack_val)
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
        range_from_player = (abs(self.rect.centerx - player.rect.centerx + 100*(1 if self.facing else -1)), abs(self.rect.centery - player.rect.centery + 100))
        if self.oldRect.size != self.rect.size:
            self.rect.top = self.rect.top + (self.oldRect.height - self.rect.height)
            if not self.facing: # if facing levfy6
                self.rect.right = self.rect.right + (self.oldRect.width - self.rect.width)
            self.oldRect = self.rect.copy()
        self.facing = (self.rect.centerx < player.rect.centerx)
        flip = 1 if self.facing else -1
        fps = 100
        offset = (abs(self.rect.centerx - player.rect.centerx), abs(self.rect.centery - player.rect.centery+20))
        SCREEN.blit(FONT_24.render(str(offset), False, WHITE), (SCREEN_WIDTH//2, 50))
        sightbox = pygame.mask.from_surface(pygame.Surface((100, 100)))
        if self.attacking: self.attack(player)
        x = sightbox.overlap(sightbox, offset)
        if self.dead: 
            fps = 250
            self.animate(fps, player)
            return
        elif x and not self.attacking and abs(offset[1]) <= 20: 
            self.state = 'Attack'
            self.attacking = True
            self.frame = 0
            self.attack(player)
        elif self.mask.overlap(player.attack_hitbox, range_from_player) and not self.state == 'Hit' and player.attackBool and pygame.time.get_ticks() - self.iframes > 600: 
            self.iframes = pygame.time.get_ticks()
            self.frame = 0
            self.hurt = True
            self.walking = False
            self.attacking = False
            self.state = 'Hit'
            self.hp -= player.attack_value
            if self.hp <= 0 and not self.dead: 
                self.dead = True
                self.state = 'Death'
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
        
    def walk(self):
        self.rect.x += self.speed * (1 if self.facing else -1)    
        
class Bat(Enemy):
    def __init__(self, player: player.Player):
        super(Bat, self).__init__()
        self.sprites = initialize_sprites('/round1-4/bat', 4)
        self.image = self.sprites['Idle'][0]
        self.rect = self.image.get_rect()
        self.rect.x = random.choice([-100, 100+constants.SCREEN_WIDTH])
        self.rect.y = -100
        self.mask = pygame.mask.from_surface(self.image)
        self.dead = False
        self.attacking = False
        self.hurt = False
        self.state = 'Idle'
        self.hp = 50
        self.frame = 0
        self.facing = True
        self.dt = pygame.time.get_ticks()
        self.moving = False
        self.oldRect = self.rect.copy()
        self.attack_hitbox = False
        self.iframes = pygame.time.get_ticks()
        self.speed = 1
        self.attack_val = 10
        self.attack_sound = [pygame.mixer.Sound('./sound/enemy/round1-4/bat/Attack.wav'), False]
        self.hurt_sound = [pygame.mixer.Sound('./sound/enemy/round1-4/bat/Hurt.wav'), False]
        self.move_sound = [pygame.mixer.Sound('./sound/enemy/round1-4/bat/Move.wav'), False]

    def animate(self, fps, player: player.Player):
        if self.frame == len(self.sprites[self.state]) - 1: 
            self.frame = 0
            self.state = 'Idle'
            if self.moving:
                self.moving = False
            if self.attacking: 
                self.attacking = False
                self.attack_sound[1] = False
            if self.hurt: self.hurt = False
            if self.dead: 
                player.score += 15 + ((player.bosses_killed + 1) * (20))
                self.attack_sound[0].stop()
                self.hurt_sound[0].stop()
                self.move_sound[0].stop()
                self.kill()
        if pygame.time.get_ticks() - self.dt > fps:
            if (3 < self.frame < 5) and self.attacking: 
                attacking_surf = pygame.Surface((self.image.get_width() + 30, self.image.get_height()))
                offset = (abs(self.rect.centerx - player.rect.centerx), abs(self.rect.centery - player.rect.centery))
                attacking_mask = pygame.mask.from_surface(attacking_surf)
                if attacking_mask.overlap(player.mask, offset): 
                    player.hurt(self.attack_val)
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
        range_from_player = (abs(self.rect.centerx - player.rect.centerx + 50*(1 if self.facing else -1)), abs(self.rect.centery - player.rect.centery - 30))
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
            self.animate(fps, player)
            return
        elif x and not self.attacking and abs(offset[1]) <= 20: 
            self.state = 'Attack'
            self.attacking = True
            self.frame = 0
            self.attack(player)
        elif self.mask.overlap(player.attack_hitbox, range_from_player) and not self.state == 'Hit' and player.attackBool and pygame.time.get_ticks() - self.iframes > 600: 
            self.iframes = pygame.time.get_ticks()
            self.frame = 0
            self.hurt = True
            self.moving = False
            self.attacking = False
            self.state = 'Hit'
            self.hp -= player.attack_value
            self.hurt_sound[0].play()
            if self.hp <= 0 and not self.dead: 
                self.dead = True
                self.state = 'Death'
        if self.moving and self.state == 'Move':
            if not self.move_sound[1]:
                self.move_sound[0].play(-1) 
                self.move_sound[0].set_volume(100)
                self.move_sound[1] = True
            self.move_X()
            if self.rect.y <= player.rect.y: self.move_Y()
            
        if self.frame != 0: self.animate(fps, player)
        elif self.state == 'Idle' or self.state == 'Move':
            choice = random.choice(['Idle', 'Move'])
            if choice == 'Idle' and not self.state == 'Idle' and self.rect.y > player.rect.y:  
                self.frame = 0
                self.state = choice
                if self.move_sound[1]: 
                    self.move_sound[0].stop()
                    self.move_sound[1] = False
            elif choice == 'Move' and not self.state == 'Move': 
                self.frame = 0
                self.state = choice
                self.moving = True
        
        self.animate(fps, player)
        
    def attack(self, player: player.Player):
        if not self.attack_sound[1]: 
            self.attack_sound[0].play()
            self.attack_sound[0].set_volume(0.2)
            self.attack_sound[1] = True
        self.attacking = True
        
    def move_X(self):
        self.rect.x += self.speed * (1 if self.facing else -1)    
    
    def move_Y(self):
        self.rect.y += self.speed
        
class Bringer(Enemy):
    def __init__(self, player: player.Player):
        super(Bringer, self).__init__()
        self.sprites = initialize_sprites('/round1-4/bringerofdeath', 3)
        self.image = self.sprites['Idle'][0]
        self.rect = self.image.get_rect()
        self.rect.x = random.choice([-150, constants.SCREEN_WIDTH - 50])
        self.rect.y = 400
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
        self.speed = 1
        self.raw_attack_val = 30
        self.spell_attack_val = 20
        self.casting = False
        self.spell = False
        self.spellframe = 0
        self.spelllocation = 0
        self.spelldt = pygame.time.get_ticks()
        self.attack_sound = [pygame.mixer.Sound('./sound/enemy/round1-4/bringerofdeath/Attack.wav'), False]
        self.hurt_sound = [pygame.mixer.Sound('./sound/enemy/round1-4/bringerofdeath/Hurt.mp3'), False]
        self.spell_sound = [pygame.mixer.Sound('./sound/enemy/round1-4/bringerofdeath/Spell.mp3'), False]
        self.walk_sound = [pygame.mixer.Sound('./sound/enemy/round1-4/bringerofdeath/Walk.wav'), False]
        self.death_sound = [pygame.mixer.Sound('./sound/enemy/round1-4/bringerofdeath/Death.mp3'), False]

    def animate(self, fps, player: player.Player):
        if self.frame == len(self.sprites[self.state]) - 1: 
            self.frame = 0
            self.state = 'Idle'
            if self.walking:
                self.walking = False
            if self.attacking: 
                self.attack_sound[0].stop()
                self.attack_sound[1] = False
                self.attacking = False
            if self.hurt: 
                self.hurt = False
                self.hurt_sound[0].stop()
                self.hurt_sound[1] = False
            if self.dead: 
                player.score += 120 + ((player.bosses_killed + 1) * (20))
                self.kill()
            if self.casting: 
                self.casting = False
                self.spell = True
                self.spellframe = -1
        if self.spellframe == len(self.sprites['Spell']) - 1 and self.spell:
            self.spell = False
            self.spell_sound[1] = False
            self.spell_sound[0].stop()
        if pygame.time.get_ticks() - self.spelldt > 200 and self.spell:
            if 0 < self.spellframe < 3 or 13 < self.spellframe < 16:
                attacking_surf = pygame.Surface((100, 200))
                attacking_mask = pygame.mask.from_surface(attacking_surf)
                offset = (abs(self.spelllocation[0] - player.rect.centerx + 200), abs(self.spelllocation[1] - player.rect.centery + 250))
                if attacking_mask.overlap(player.mask, offset):
                    player.hurt(self.spell_attack_val)
            self.spellframe = (self.spellframe + 1)
            self.spelldt = pygame.time.get_ticks()
        if pygame.time.get_ticks() - self.dt > fps:
            if (5 < self.frame < 7)  and self.attacking: 
                attacking_surf = pygame.Surface(self.image.get_size())
                offset = (abs(self.rect.centerx - player.rect.centerx-100*(1 if self.facing else -1)), abs(self.rect.centery - player.rect.centery))
                attacking_mask = pygame.mask.from_surface(attacking_surf)
                if attacking_mask.overlap(player.mask, offset): 
                    player.hurt(self.raw_attack_val)
            self.frame = (self.frame + 1) 
            self.image = self.sprites[self.state][self.frame]
            self.dt = pygame.time.get_ticks()    
            self.rect.size = self.image.get_size()
        if not self.facing: 
            SCREEN.blit(self.image, self.rect)
        else: 
            SCREEN.blit(pygame.transform.flip(self.image, True, False), self.rect)
        if self.spell: 
            SCREEN.blit(self.sprites['Spell'][self.spellframe], self.spelllocation)

    def update(self, player: player.Player):
        range_from_player = (abs(self.rect.centerx - player.rect.centerx - 250*(1 if self.facing else -1)), abs(self.rect.centery - player.rect.centery + 200))
        if self.oldRect.size != self.rect.size:
            self.rect.top = self.rect.top + (self.oldRect.height - self.rect.height)
            if not self.facing: # if facing levfy6
                self.rect.right = self.rect.right + (self.oldRect.width - self.rect.width)
            self.oldRect = self.rect.copy()
        self.facing = (self.rect.centerx < player.rect.centerx)
        fps = 100
        offset = (abs(self.rect.centerx - player.rect.centerx), abs(self.rect.centery - player.rect.centery+70))
        SCREEN.blit(FONT_24.render(str(offset), False, WHITE), (SCREEN_WIDTH//2, 50))
        sightbox = pygame.mask.from_surface(pygame.Surface((100, 100)))
        if self.attacking: self.attack(player)
        x = sightbox.overlap(sightbox, offset)
        if self.casting: fps = 300
        if self.dead: 
            fps = 250
            self.animate(fps, player)
            return
        if self.hurt:
            self.state = 'Hurt' 
            self.animate(fps, player)
            return
        elif x and not self.attacking and abs(offset[1]) <= 20: 
            self.state = 'Attack'
            self.attacking = True
            self.frame = 0
            self.attack(player)
        elif self.mask.overlap(player.attack_hitbox, range_from_player) and not self.state == 'Hurt' and player.attackBool and pygame.time.get_ticks() - self.iframes > 600: 
            self.iframes = pygame.time.get_ticks()
            self.frame = -1
            self.hurt = True
            self.walking = False
            self.attacking = False
            self.state = 'Hurt'
            self.hp -= player.attack_value
            if not self.hurt_sound[1]:
                self.hurt_sound[0].play()
                self.hurt_sound[1] = True
            if self.hp <= 0 and not self.dead: 
                self.dead = True
                self.walk_sound[0].stop()
                self.attack_sound[0].stop()
                self.hurt_sound[0].stop()
                self.death_sound[0].play()
                self.death_sound[0].set_volume(0.5)
                self.state = 'Death'
        if random.randint(0, 1000) == 1 and not self.casting and not self.spell and not self.attacking and not self.hurt: 
            if not self.spell_sound[1]:
                self.spell_sound[0].play()
                self.spell_sound[1] = True
            fps = 300
            self.frame = -1
            self.casting = True
            self.state = 'Cast'
            self.spelllocation = (player.rect.x-50, player.rect.y - 200)
        if self.walking and self.state == 'Walk':
            if offset[0] > 20: 
                if not self.walk_sound[1]: 
                    self.walk_sound[0].play()
                    self.walk_sound[0].set_volume(100)
                    self.walk_sound[1] = True
                self.walk()
        if self.frame != 0: self.animate(fps, player)
        elif self.state == 'Idle' or self.state == 'Walk':
            choice = random.choice(['Idle', 'Walk'])
            if choice == 'Idle' and not self.state == 'Idle': 
                self.frame = 0
                self.state = choice
                self.walk_sound[1] = False
            elif choice == 'Walk' and not self.state == 'Walk': 
                self.frame = 0
                self.state = choice
                self.walking = True
        
        self.animate(fps, player)
        
    def attack(self, player: player.Player):
        if not self.attack_sound[1]:
            self.attack_sound[0].play()
            self.attack_sound[0].set_volume(100)
            self.attack_sound[1] = True
        self.attacking = True
        
    def walk(self):
        self.rect.x += self.speed * (1 if self.facing else -1)    