import pygame, random, constants

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((20, 10))
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect(center = (constants.SCREEN_WIDTH+10, random.randint(0, constants.SCREEN_HEIGHT)))
        self.speed = random.randint(5, 10)
    
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()