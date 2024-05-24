import pygame, os, time

globals = globals(); 
GAME_STATE = 'initializing'
ISPAUSED = False
SCREEN_HEIGHT = 728
SCREEN_WIDTH = 1024
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SELECT = (217, 172, 67)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.font.init()
FONT_48 = pygame.font.Font('font/PixeloidSans.ttf', 48)
FONT_24 = pygame.font.Font('font/PixeloidSans.ttf', 24)
FONT_16 = pygame.font.Font('font/PixeloidSans.ttf', 16)
FONT_12 = pygame.font.Font('font/PixeloidSans.ttf', 12)
PLAYER_SCROLL = 0
SCROLL_THRESH = 300
FRAMES = 144
GRAVITY = 1
JUMP_TIMER = 0

def clip_image(image, clip):
    image.set_clip(clip)
    return image.subsurface(image.get_clip())