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
   sprites = {'idle':[], 'walk':[], 'attackA':[], 'attackB':[], 'start':[], 'hurt': [], 'deathanimation': [], 'jump':[],
              'heal': []}
   for fname in os.listdir('./sprites/rob'):
      if fname.endswith('.png'):
         sprites[extract(fname.split('_')[1].replace('.png', ''))].append('./sprites/rob/'+fname)
   attacks = ['attackA', 'attackB']
   for i in list(sprites.keys()):
      sprites[i] = sorted(sprites[i], key = lambda x: x[-7:-4])
      index = 0
      for sprite in sprites[i]:
         sprites[i][index] = pygame.transform.scale2x(pygame.image.load(sprite).convert_alpha())
         index += 1
   
   def __init__(self):
      super(Player, self).__init__()
      self.count = 0
      self.surf = pygame.Surface((128*2, 64*2))
      self.rect = self.surf.get_rect()
      self.a_frame = 0
      self.state = 'idle'
      self.image = self.sprites[self.state][self.a_frame]
      self.rect.x = SCREEN_WIDTH//2-self.image.get_width()//2
      self.rect.y = 560
      self.size = self.image.get_size()
      self.facing = True
      self.attacking = 1
      self.hurting = 1
      self.attack_type = 'attackA'
      self.attackBool = False
      self.vel = vec(0, 22)
      self.acc = vec(0, 0)
      self.mask = pygame.mask.from_surface(self.image)
      self.hp = 100
      self.maxhp = 100
      self.iframes = FRAMES*3
      self.jumpheight = self.vel.y
      self.jumping = False
      self.jumpinganim = 1
      self.dead = False
      self.falling = False
      self.dashing = False
      self.dash_time = 0
      self.veldash = 0
      self.hpcharge = 25
      self.healing = False
      self.heal_time = 0
      self.no_hpcharges = 3

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
      if self.hp <= 0 and self.dead == False:
         self.dead = True
         self.state = 'deathanimation'

   def jump_update(self, fps):
      
      self.state = 'jump'
      self.rect.y -= self.vel.y
      self.vel.y -= GRAVITY
      if self.vel.y < -self.jumpheight:
         self.jumping = False
         self.vel.y = 10

   def fall(self):
      self.vel.y = -abs(self.vel.y)
      self.rect.y -= self.vel.y
      self.vel.y -= GRAVITY

   def dash(self, dt):
      self.rect.x += self.veldash
      self.veldash -= 0.1
      if dt - self.dash_time >= 300:
         self.veldash = 0
         self.dashing = False
         self.dash_time = 0
   
   def heal(self, dt):
      self.state == 'heal'
      if dt - self.heal_time >= 1300:
         self.hp += self.hpcharge
         self.hp = min(self.hp, self.maxhp)
         self.healing = False
         self.heal_time = 0
         self.no_hpcharges = max(0, self.no_hpcharges-1)

   def update(self, pressed_keys, event_update):

      if GAME_STATE == 'paused':
         return

      self.acc = vec(0, 0)
      if not self.healing:
         if pressed_keys[K_LEFT]:
            self.facing = False
            self.state = 'walk'
            self.acc.x = -0.2
            if self.facing:
               self.mask = pygame.transform.flip(self.mask, True, False)
         elif pressed_keys[K_RIGHT]:
            self.facing = True
            self.state = 'walk'
            self.acc.x = 0.2
            if not self.facing:
               self.mask = pygame.transform.flip(self.mask, True, False)
         else:
            self.state = 'idle'
            self.acc.x = 0

      self.vel.x += self.acc.x
      if abs(self.vel.x) >= 2:
         self.vel.x = 2 * self.vel.x / abs(self.vel.x)
      if self.acc.x == 0:
         self.vel.x *= 0.5

      if self.rect.x < -40:
         self.rect.x = -40
      if self.rect.x > SCREEN_WIDTH - self.size[0] + 40:
         self.rect.x = SCREEN_WIDTH - self.size[0] + 40

      self.rect.x += self.vel.x
      