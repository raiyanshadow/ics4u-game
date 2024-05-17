import pygame, os

GAME_STATE = 'initializing'
SCREEN_HEIGHT = 728
SCREEN_WIDTH = 1024
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SELECT = (255, 235, 179)
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
BG = pygame.image.load('./sprites/bg.png')
BG = pygame.transform.scale(BG, (BG.get_width(), SCREEN_HEIGHT))
SCROLL_THRESH = 300
pygame.font.init()
FONT_48 = pygame.font.Font('font/PixeloidSans.ttf', 48)
FONT_24 = pygame.font.Font('font/PixeloidSans.ttf', 24)
FONT_16 = pygame.font.Font('font/PixeloidSans.ttf', 16)
FONT_12 = pygame.font.Font('font/PixeloidSans.ttf', 12)
SCROLL = 0