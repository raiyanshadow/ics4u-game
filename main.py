import player, enemy, pygame, random, constants, math
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

fps_font = pygame.font.SysFont("monospace", 15)

def show_fps(screen, clock):
    """utility function to show frames per second"""
    fps = str(int(clock.get_fps()))
    fps_surface = fps_font.render(fps, True, constants.WHITE)
    fps_rect = fps_surface.get_rect()
    fps_rect.topleft = (10, 10)
    screen.blit(fps_surface, fps_rect)

clockobject = pygame.time.Clock()

rob = player.Player()

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 255)

enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(rob)

update = pygame.time.get_ticks()
cooldown = 150
frame = 0

while True:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                quit()
        elif event.type == QUIT:
            pygame.quit()
            quit()
        elif event.type == ADDENEMY:
            new_enemy = enemy.Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    rob.update(pygame.key.get_pressed())
    enemies.update()

    if pygame.sprite.spritecollideany(rob, enemies):
        rob.kill()

    constants.SCREEN.fill((200, 200, 200))

    if pygame.time.get_ticks() - update >= cooldown:
        if rob.attacking > 1:
            rob.state = rob.attack_type
            cooldown = 90
            rob.attacking -= 1
        else:
            cooldown = 150
        update = pygame.time.get_ticks()
        animate(update)

    for i in range(0, math.ceil(constants.SCREEN_WIDTH/constants.BG.get_width())): 
        constants.SCREEN.blit(constants.BG, (i*constants.BG.get_width(), 0))

    if rob.facing: constants.SCREEN.blit(rob.bigger_img, rob.pos)
    else: constants.SCREEN.blit(pygame.transform.flip(rob.bigger_img, True, False), rob.pos)
    show_fps(constants.SCREEN, clockobject)
    pygame.display.flip()
    clockobject.tick(60)