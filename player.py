import pygame, constants, os
from pygame.locals import *

class Player(pygame.sprite.Sprite):
  sprites = {'idle':['./sprites/rob/rob_idle_1.png', 
             './sprites/rob/rob_idle_2.png', 
             './sprites/rob/rob_idle_3.png', 
             './sprites/rob/rob_idle_4.png',
             './sprites/rob/rob_idle_5.png',
             './sprites/rob/rob_idle_6.png'],
             'walk':['./sprites/rob/rob_walk_1.png',
             './sprites/rob/rob_walk_2.png',
             './sprites/rob/rob_walk_3.png',
             './sprites/rob/rob_walk_4.png',
             './sprites/rob/rob_walk_5.png',]}
  def __init__(self):
    super(Player, self).__init__()
    self.surf = pygame.Surface((64*3, 64*3))
    self.rect = self.surf.get_rect()
    self.a_frame = 0
    self.state = 'idle'
    self.image = pygame.image.load(self.sprites[self.state][self.a_frame])
    self.size = self.image.get_size()
    self.bigger_img = pygame.transform.scale(self.image, (self.size[0]*3, self.size[1]*3))
    self.facing = True

  def update(self, pressed_keys):

    if pressed_keys[K_LEFT]:
        if self.facing:
            self.facing = False
        self.state = 'walk'
        self.rect.move_ip(-2, 0)
        
    elif pressed_keys[K_RIGHT]:
        if not self.facing:
           self.facing = True
        self.state = 'walk'
        self.rect.move_ip(2, 0)
    
    else:
        self.state = 'idle'
      
  
    if self.rect.left <= 0:
      self.rect.left = 0
    if self.rect.right >= constants.SCREEN_WIDTH:
      self.rect.right = constants.SCREEN_WIDTH
    if self.rect.top <= 0:
      self.rect.top = 0
    if self.rect.bottom >= constants.SCREEN_HEIGHT:
      self.rect.bottom = constants.SCREEN_HEIGHT

