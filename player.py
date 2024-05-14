import pygame, constants, os, time, random
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
             './sprites/rob/rob_walk_5.png',],
             'attackA':['./sprites/rob/rob_attackA_1.png',
             './sprites/rob/rob_attackA_2.png',
             './sprites/rob/rob_attackA_3.png',
             './sprites/rob/rob_attackA_4.png',
             './sprites/rob/rob_attackA_5.png',
             './sprites/rob/rob_attackA_6.png',
             './sprites/rob/rob_attackA_7.png',
             './sprites/rob/rob_attackA_8.png',
             './sprites/rob/rob_attackA_9.png',
             './sprites/rob/rob_attackA_10.png',
             './sprites/rob/rob_attackA_11.png',
             './sprites/rob/rob_attackA_12.png',],
             'attackB':['./sprites/rob/rob_attackB_1.png',
             './sprites/rob/rob_attackB_2.png',
             './sprites/rob/rob_attackB_3.png',
             './sprites/rob/rob_attackB_4.png',
             './sprites/rob/rob_attackB_5.png',
             './sprites/rob/rob_attackB_6.png',
             './sprites/rob/rob_attackB_7.png',
             './sprites/rob/rob_attackB_8.png',
             './sprites/rob/rob_attackB_9.png',
             './sprites/rob/rob_attackB_10.png',
             './sprites/rob/rob_attackB_11.png',
             './sprites/rob/rob_attackB_12.png',
             './sprites/rob/rob_attackB_13.png']}
  attacks = ['attackA', 'attackB']
  
  def __init__(self):
    super(Player, self).__init__()
    self.surf = pygame.Surface((64*3, 64*3))
    self.rect = pygame.Rect(0, 720-3*64-32, 128, 128)
    self.a_frame = 0
    self.state = 'idle'
    self.image = pygame.image.load(self.sprites[self.state][self.a_frame])
    self.size = self.image.get_size()
    self.bigger_img = pygame.transform.scale(self.image, (self.size[0]*3, self.size[1]*3))
    self.facing = True
    self.attacking = 1
    self.attack_type = 'attackA'

  def update(self, pressed_keys):

    if pressed_keys[K_x]:
        self.state = random.choice(self.attacks)
        self.attack_type = self.state
        self.attacking = 12

    if pressed_keys[K_LEFT]:
        if self.facing:
            self.facing = False
        self.state = 'walk'
        self.rect.move_ip(-3.5, 0)
        
    elif pressed_keys[K_RIGHT]:
        if not self.facing:
           self.facing = True
        self.state = 'walk'
        self.rect.move_ip(3.5, 0)
        
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
    
    if self.rect.right >= constants.SCROLL_THRESH:
       constants.SCROLL = -3.5
    elif self.rect.left <= constants.SCROLL_THRESH:
       constants.SCROLL = 3.5

