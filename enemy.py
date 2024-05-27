import pygame, random, constants, os

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


class SkeletonA(Enemy):
    def __init__(self):
        super(SkeletonA, self).__init__()
        self.sprites = initialize_sprites('round1-4/skeletonA', 5)
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
        
