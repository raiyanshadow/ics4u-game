import pygame
from constants import *

class Boss(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.type = type
        