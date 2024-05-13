import player, enemy, pygame, random, constants
from pygame.locals import *
global update

def animate(update):
    rob.a_frame = (rob.a_frame + 1) % len(rob.sprites[rob.state])
    rob.image = pygame.image.load(rob.sprites[rob.state][rob.a_frame])
    rob.size = rob.image.get_size()
    rob.bigger_img = pygame.transform.scale(rob.image, (rob.size[0]*3, rob.size[1]*3))

pygame.init()

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
        update = pygame.time.get_ticks()
        animate(update)

    if rob.facing: constants.SCREEN.blit(rob.bigger_img, rob.rect)
    else: constants.SCREEN.blit(pygame.transform.flip(rob.bigger_img, True, False), rob.rect)

    pygame.display.flip()
    clockobject.tick(60)