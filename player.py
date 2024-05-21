import pygame, os, time, random
from pygame.locals import *
from constants import *

vec = pygame.math.Vector2

def extract(fname):
   res = ""
   for i in fname:
      if i.isalpha():
         res = "".join([res, i])
   return res

class Player(pygame.sprite.Sprite):
   sprites = {'idle':[], 'walk':[], 'attackA':[], 'attackB':[], 'start':[], 'hurt': [], 'dead': [], 'jump':[], 'fall':[]}
   for fname in os.listdir('./sprites/rob'):
      if fname.endswith('.png'):
         sprites[extract(fname.split('_')[1].replace('.png', ''))].append('./sprites/rob/'+fname)
   attacks = ['attackA', 'attackB']
   for i in list(sprites.keys()):
      sprites[i] = sorted(sprites[i], key = lambda x: x[-7:-4])
   
   def __init__(self):
      super(Player, self).__init__()
      self.count = 0
      self.surf = pygame.Surface((64*3, 64*3))
      self.rect = pygame.Rect(SCREEN_WIDTH//2, SCREEN_HEIGHT-64*3, 64*3, 64*3)
      self.a_frame = 0
      self.state = 'idle'
      self.image = pygame.image.load(self.sprites[self.state][self.a_frame])
      self.size = self.image.get_size()
      self.bigger_img = pygame.transform.scale(self.image, (self.size[0]*3, self.size[1]*3))
      self.facing = True
      self.attacking = 1
      self.hurting = 1
      self.attack_type = 'attackA'
      self.attackBool = False
      self.pos = vec(self.rect.x, self.rect.y)
      self.vel = vec(0, 16)
      self.acc = vec(0, 0)
      self.mask = pygame.mask.from_surface(self.bigger_img)
      self.hp = 100
      self.iframes = FRAMES*3
      self.jumpheight = self.vel.y
      self.jumping = False
      self.jumpinganim = 1

   def attack(self):
      self.a_frame = 0
      self.attackBool = True
      self.state = random.choice(self.attacks)
      self.attack_type = self.state
      self.attacking = len(self.sprites[self.state])

   def hurt(self):
      self.a_frame = 0
      self.state = 'hurt'
      self.hp -= 10
      self.hurting = len(self.sprites[self.state])

   def update(self, pressed_keys, event_update):

      if GAME_STATE == 'paused':
         return

      self.acc = vec(0, 0)

      if pressed_keys[K_LEFT]:
         self.facing = False
         self.state = 'walk'
         self.acc.x = -0.2
      
      elif pressed_keys[K_RIGHT]:
         self.facing = True
         self.state = 'walk'
         self.acc.x = 0.2
      
      else:
         self.state = 'idle'
         self.acc.x = 0

      self.vel.x += self.acc.x - 0.01*self.acc.x # friction = 0.01
      if abs(self.vel.x) >= 2:
         self.vel.x = 2 * self.vel.x / abs(self.vel.x)
      if self.acc.x == 0:
         self.vel.x *= 0.5

      self.pos.x += self.vel.x

      self.rect.centerx = self.pos.x

      if self.pos.x + (self.size[0]//2) < 0:
         self.pos.x = -(self.size[0]//2)
      if self.pos.x > SCREEN_WIDTH-(3*self.size[0]//2):
         self.pos.x = SCREEN_WIDTH-(3*self.size[0]//2)

      