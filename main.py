import player, enemy, pygame, random, constants, math, time
from pygame.locals import *
global update

def animate(update):
    rob.a_frame = (rob.a_frame + 1) % len(rob.sprites[rob.state])
    rob.image = pygame.image.load(rob.sprites[rob.state][rob.a_frame])
    rob.size = rob.image.get_size()
    rob.bigger_img = pygame.transform.scale(rob.image, (rob.size[0]*3, rob.size[1]*3))

pygame.init()

#show fps
fps = pygame.time.Clock()

#show fps

constants.SCREEN = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))

fps_font = pygame.font.SysFont("monospace", 20)

studio_image = pygame.image.load('./sprites/studio.png')
super_mountain_dusk = {'far-clouds':pygame.image.load('./sprites/Super Mountain Dusk Files/Layers/far-clouds.png'),
                       'far-mountains':pygame.image.load('./sprites/Super Mountain Dusk Files/Layers/far-mountains.png'),
                       'mountains':pygame.image.load('./sprites/Super Mountain Dusk Files/Layers/mountains.png'),
                       'near-clouds':pygame.image.load('./sprites/Super Mountain Dusk Files/Layers/near-clouds.png'),
                       'sky':pygame.image.load('./sprites/Super Mountain Dusk Files/Layers/sky.png'),
                       'trees':pygame.image.load('./sprites/Super Mountain Dusk Files/Layers/trees.png')}
round_1_ground = pygame.image.load('./sprites/ground.png')
title = pygame.image.load('./sprites/title.png')
title = pygame.transform.scale(title, (constants.SCREEN_WIDTH-200, constants.SCREEN_HEIGHT-200))
for i in super_mountain_dusk:
    super_mountain_dusk[i] = pygame.transform.scale(super_mountain_dusk[i], (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
rob = player.Player()

def show_fps(screen, clock):
    """utility function to show frames per second"""
    fps = str(int(clock.get_fps()))
    fps_surface = fps_font.render(fps, True, constants.WHITE)
    fps_rect = fps_surface.get_rect()
    fps_rect.topleft = (10, 10)
    screen.blit(fps_surface, fps_rect)


def initialize():
    centered = (constants.SCREEN_WIDTH//2-studio_image.get_width()//2, constants.SCREEN_HEIGHT//2-studio_image.get_height()//2)
    time.sleep(1)
    for i in range(255):
        constants.SCREEN.fill(constants.BLACK)
        studio_image.set_alpha(i)
        constants.SCREEN.blit(studio_image, centered)
        pygame.display.update()
        time.sleep(0.001)
    time.sleep(1.5)
    for i in range(255, 0, -1):
        constants.SCREEN.fill(constants.BLACK)
        studio_image.set_alpha(i)
        constants.SCREEN.blit(studio_image, centered)
        pygame.display.update()
        time.sleep(0.001)
    time.sleep(1)



def initial_screen():
    def render(update):
        cooldown = 150
        constants.SCREEN.blit(super_mountain_dusk['sky'], (0, 0))
        constants.SCREEN.blit(super_mountain_dusk['far-clouds'], (0, 0))
        constants.SCREEN.blit(super_mountain_dusk['near-clouds'], (0, 0))
        constants.SCREEN.blit(super_mountain_dusk['far-mountains'], (0, 0))
        constants.SCREEN.blit(super_mountain_dusk['mountains'], (0, 0))
        constants.SCREEN.blit(super_mountain_dusk['trees'], (0, 0))
        for i in range(0, math.ceil(constants.SCREEN_WIDTH/round_1_ground.get_width())):
            constants.SCREEN.blit(round_1_ground, (i*round_1_ground.get_width(), constants.SCREEN_HEIGHT-round_1_ground.get_height()))

        if pygame.time.get_ticks() - update >= cooldown:
            if rob.attacking > 1:
                rob.state = rob.attack_type
                cooldown = 90
                rob.attacking -= 1
            else:
                cooldown = 150
            update = pygame.time.get_ticks()
            animate(update)
        constants.SCREEN.blit(rob.bigger_img, (0+round_1_ground.get_width()+rob.pos.x, 0+rob.pos.y))
        constants.SCREEN.blit(title, (0, 0))

    clockobject = pygame.time.Clock()
    update = pygame.time.get_ticks()
    while True:
        
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    quit()
            elif event.type == QUIT:
                pygame.quit()
                quit()
        render(update)
        pygame.display.flip()
        clockobject.tick(60)
        
    

clockobject = pygame.time.Clock()
initialize()

initial_screen()

while True:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                quit()
        elif event.type == QUIT:
            pygame.quit()
            quit()
    show_fps(constants.SCREEN, clockobject)
    for i in range(0, math.ceil(constants.SCREEN_WIDTH/constants.BG.get_width())): 
        constants.SCREEN.blit(constants.BG, (i*constants.BG.get_width(), 0))
    pygame.display.flip()
    clockobject.tick(60)