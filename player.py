import pygame, constants, os, time, random
from pygame.locals import *

vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
  sprites = {'idle':[], 'walk':[], 'attackA':[], 'attackB':[]}
  for fname in os.listdir('./sprites/rob'):
    if fname.endswith('.png'):
      if fname.startswith('rob_idle'):
        sprites['idle'].append('./sprites/rob/'+fname)
      elif fname.startswith('rob_walk'):
        sprites['walk'].append('./sprites/rob/'+fname)
      elif fname.startswith('rob_attackA'):
        sprites['attackA'].append('./sprites/rob/'+fname)
      elif fname.startswith('rob_attackB'):
        sprites['attackB'].append('./sprites/rob/'+fname)
  attacks = ['attackA', 'attackB']
  for i in list(sprites.keys()):
     sprites[i] = sorted(sprites[i], key = lambda x: x[-7:-4])
  
  def __init__(self):
    super(Player, self).__init__()
    self.surf = pygame.Surface((64*3, 64*3))
    self.rect = pygame.Rect(32, constants.SCREEN_HEIGHT-64*3, 64*3, 64*3)
    self.a_frame = 0
    self.state = 'idle'
    self.image = pygame.image.load(self.sprites[self.state][self.a_frame])
    self.size = self.image.get_size()
    self.bigger_img = pygame.transform.scale(self.image, (self.size[0]*3, self.size[1]*3))
    self.facing = True
    self.attacking = 1
    self.attack_type = 'attackA'
    self.pos = vec(self.rect.x, self.rect.y)
    self.vel = vec(0, 0)
    self.acc = vec(0, 0)

  def update(self, pressed_keys):
    self.acc = vec(0, 0)
    if pressed_keys[K_x] and self.state != 'attackA' and self.state != 'attackB':
        self.state = random.choice(self.attacks)
        self.attack_type = self.state
        if self.state == 'attackA':
            self.attacking = 12
        elif self.state == 'attackB':
            self.attacking = 13

    if pressed_keys[K_LEFT]:
        if self.facing:
            self.facing = False
        self.state = 'walk'
        self.acc.x = -0.3
        
    elif pressed_keys[K_RIGHT]:
        if not self.facing:
           self.facing = True
        self.state = 'walk'
        self.acc.x = 0.3
        
    else:
        self.state = 'idle'
    
    if self.rect.right >= constants.SCROLL_THRESH:
       constants.SCROLL = -3.5
    elif self.rect.left <= constants.SCROLL_THRESH:
       constants.SCROLL = 3.5
    
    self.acc += self.vel * -0.05  # friction = 0.12
    self.vel += self.acc
    self.pos += self.vel + 0.5 * self.acc

    if self.pos.x+self.size[0]*3 >= constants.SCREEN_WIDTH:
        self.pos.x = constants.SCREEN_WIDTH-self.size[0]*3
    if self.pos.x <= 0:
        self.pos.x = 0

    self.rect.centerx = self.pos.x
