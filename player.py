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
      self.a_frame = 0
      self.state = 'idle'
      self.image = self.sprites[self.state][self.a_frame]
      self.rect = self.image.get_rect()
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
      self.iframes = pygame.time.get_ticks()
      self.jumpheight = self.vel.y
      self.jumping = False
      self.jumpinganim = 1
      self.dead = False
      self.falling = False
      self.dashing = False
      self.dash_time = 0
      self.veldash = 0
      self.hpcharge = 60
      self.healing = False
      self.heal_time = 0
      self.no_hpcharges = 3
      self.attack_hitbox = pygame.mask.from_surface(pygame.Surface((50, self.image.get_height())))
      self.attack_offset = (self.rect.centerx + 100, abs(self.rect.centery - self.image.get_height()//2))
      self.attack_value = 66
      self.jump_hitbox = pygame.mask.from_surface(pygame.Surface((30, 30)))
      self.score = 0
      self.bosses_killed = 0
      self.player_sound = pygame.mixer
      self.player_sound.init()
      self.crit = False
      self.heartbeat = pygame.mixer.Sound('./sound/rob/Heartbeat.mp3')
      self.heartbeat.play(-1)
      self.heartbeat.set_volume(0)
      self.dash_sound = [pygame.mixer.Sound('./sound/rob/Dash.wav'), False]
      self.hurt_sound = [pygame.mixer.Sound('./sound/rob/Hurt.wav'), False]
      self.jump_sound = [pygame.mixer.Sound('./sound/rob/Jump.wav'), False]
      self.walk_sound = [pygame.mixer.Sound('./sound/rob/Walk.wav'), False]
      self.attack_sound = [pygame.mixer.Sound('./sound/rob/Attack.mp3'), False]
      self.heal_sound = [pygame.mixer.Sound('./sound/rob/Heal.mp3'), False]

   def attack(self):
      self.attack_sound[0].play()
      self.attack_sound[0].set_volume(5000)
      self.a_frame = 0
      self.attackBool = True
      self.state = random.choice(self.attacks)
      self.attack_type = self.state
      self.attacking = len(self.sprites[self.state])

   def hurt(self, hit_value):
      if not self.hurt_sound[1]: 
         self.hurt_sound[0].play()
         self.hurt_sound[0].set_volume(100)
         self.hurt_sound[1] = True
      if pygame.time.get_ticks() - self.iframes > 1000:
         self.a_frame = 0
         self.hurt_sound[1] = False
         self.state = 'hurt'
         self.hp -= hit_value
         self.hurting = len(self.sprites[self.state])
         if self.hp / self.maxhp <= 0.4 and not self.crit:
            self.heartbeat.set_volume(10)
            self.crit = True
         if self.hp <= 0 and self.dead == False:
            self.dead = True
            self.state = 'deathanimation'
            self.player_sound.music.load('./sound/rob/Death.wav')
            self.player_sound.music.play()
         self.iframes = pygame.time.get_ticks()

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
      if not self.dash_sound[1]: 
         self.dash_sound[0].play()
         self.dash_sound[0].set_volume(100)
         self.dash_sound[1] = True
      self.rect.x += self.veldash
      self.veldash -= 0.1
      if dt - self.dash_time >= 300:
         self.dash_sound[1] = False
         self.veldash = 0
         self.dashing = False
         self.dash_time = 0
   
   def heal(self, dt):
      self.state == 'heal'
      threshold = False
      if dt - self.heal_time >= 1300:
         self.heal_sound[0].play()
         if self.hp / self.maxhp <= 0.4:
            threshold = True
         self.hp += self.hpcharge
         self.hp = min(self.hp, self.maxhp)
         if threshold:
            self.heartbeat.set_volume(0)
            self.crit = False
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
      self.attack_offset = (self.rect.centerx + 100*(1 if self.facing else -1), abs(self.rect.centery - self.image.get_height()//2))
      

   def animate(self):
      if not self.dead:
         self.a_frame = (self.a_frame + 1) % len(self.sprites[self.state])
         self.image = self.sprites[self.state][self.a_frame]
         self.mask = pygame.mask.from_surface(self.image)
         self.size = self.image.get_size()
         

      