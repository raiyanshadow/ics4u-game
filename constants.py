import pygame

SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1280
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
BG = pygame.image.load('./sprites/bg.png')
BG = pygame.transform.scale(BG, (BG.get_width(), SCREEN_HEIGHT))
SCROLL_THRESH = 300
SCROLL = 0