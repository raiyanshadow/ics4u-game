import player, enemy, pygame, random, constants, math, time, os
from pygame.locals import *
global update

def true_resize(target_width, original_image):
    size = original_image.get_width()*original_image.get_height()
    wpercent = target_width / float(size)
    hsize = int((float(size) * float(wpercent)))
    return hsize

def animate():
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

studio_image = pygame.image.load('./sprites/studio.png').convert()
super_mountain_dusk = []
for fname in sorted(os.listdir('./sprites/Super Mountain Dusk Files/Layers')):
    super_mountain_dusk.append(pygame.image.load('./sprites/Super Mountain Dusk Files/Layers/'+fname))
    hsize = true_resize(constants.SCREEN_WIDTH, super_mountain_dusk[-1])
    super_mountain_dusk[-1] = pygame.transform.scale(super_mountain_dusk[-1], (constants.SCREEN_WIDTH, hsize))

super_mountain_dusk_parallax_scroll = [0, 2, 3, 5, 5, 8]
maxwidth = []
for i in range(len(super_mountain_dusk)):
    maxwidth.append(math.ceil(constants.SCREEN_WIDTH/super_mountain_dusk[i].get_width())+1+math.ceil(super_mountain_dusk_parallax_scroll[i]/1.2))

round_1_ground = pygame.image.load('./sprites/ground.png').convert()
title = pygame.image.load('./sprites/title.png').convert()
title = pygame.transform.scale(title, (constants.SCREEN_WIDTH-200, constants.SCREEN_HEIGHT-200)).convert()
title.set_colorkey(constants.BLACK)
prompt = pygame.image.load('./sprites/prompt_text.png').convert()
prompt.set_colorkey(constants.BLACK)
prompt = pygame.transform.scale(prompt, (prompt.get_width()/2, prompt.get_height()/2)).convert()
rob = player.Player()

def show_fps(screen, clock):
    """utility function to show frames per second"""
    fps = str(int(clock.get_fps()))
    fps_surface = fps_font.render(fps, True, constants.WHITE)
    fps_rect = fps_surface.get_rect()
    fps_rect.topleft = (10, 10)
    constants.SCREEN.blit(fps_surface, fps_rect)


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
    global scroll
    scroll = 0
    clockobject = pygame.time.Clock()
    def render(scroll):
        for j in range(len(super_mountain_dusk)):
            for i in range(maxwidth[j]):
                constants.SCREEN.blit(super_mountain_dusk[j], ((i*super_mountain_dusk[j].get_width())-round(scroll*super_mountain_dusk_parallax_scroll[j]), 0))
        for i in range(0, math.ceil(constants.SCREEN_WIDTH/round_1_ground.get_width())):
            constants.SCREEN.blit(round_1_ground, (i*round_1_ground.get_width(), constants.SCREEN_HEIGHT-round_1_ground.get_height()))
        constants.SCREEN.blit(pygame.transform.scale2x(rob.image), (0+round_1_ground.get_width()+rob.pos.x, rob.pos.y+50))
        constants.SCREEN.blit(title, (0, 0))
        if showing: constants.SCREEN.blit(prompt, (460, 580))
    
    update = pygame.time.get_ticks()
    cooldown = 150
    showing = True
    cur = 0
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    quit()
                else:
                    return
            if event.type == MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())
            elif event.type == QUIT:
                pygame.quit()
                quit()
        scroll += 1

        if abs(scroll) > constants.SCREEN_WIDTH:
            scroll = 0
        
        cur += 1
        if cur >= 10:
            showing = not showing
            cur = 0

        if pygame.time.get_ticks() - update >= cooldown:
            if rob.attacking > 1:
                rob.state = rob.attack_type
                cooldown = 90
                rob.attacking -= 1
            else:
                cooldown = 150
            update = pygame.time.get_ticks()
            animate()
        render(scroll)
        pygame.display.flip()
        clockobject.tick(75)

def menu():
    global scroll
    clockobject = pygame.time.Clock()
    def render(scroll):
        for j in range(len(super_mountain_dusk)):
            for i in range(maxwidth[j]):
                constants.SCREEN.blit(super_mountain_dusk[j], ((i*super_mountain_dusk[j].get_width())-round(scroll*super_mountain_dusk_parallax_scroll[j]), 0))
        for i in range(0, math.ceil(constants.SCREEN_WIDTH/round_1_ground.get_width())):
            constants.SCREEN.blit(round_1_ground, (i*round_1_ground.get_width(), constants.SCREEN_HEIGHT-round_1_ground.get_height()))
        constants.SCREEN.blit(pygame.transform.scale2x(rob.image), (0+round_1_ground.get_width()+rob.pos.x, rob.pos.y+50))
        constants.SCREEN.blit(title, (0, 0))
        
    
    update = pygame.time.get_ticks()
    cooldown = 150
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    quit()
            if event.type == MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())
            elif event.type == QUIT:
                pygame.quit()
                quit()
        scroll += 1

        if abs(scroll) > constants.SCREEN_WIDTH:
            scroll = 0

        if pygame.time.get_ticks() - update >= cooldown:
            if rob.attacking > 1:
                rob.state = rob.attack_type
                cooldown = 90
                rob.attacking -= 1
            else:
                cooldown = 150
            update = pygame.time.get_ticks()
            animate()
        render(scroll)
        pygame.display.flip()
        clockobject.tick(75)
        
    

clockobject = pygame.time.Clock()
initialize()

initial_screen()
menu()

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