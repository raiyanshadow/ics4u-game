import player, enemy, pygame, random, math, time, os
from constants import *
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

def clip_image(image, clip):
    image.set_clip(clip)
    return image.subsurface(image.get_clip())


pygame.init()

#show fps
fps = pygame.time.Clock()

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

fps_font = pygame.font.SysFont("monospace", 20)

studio_image = pygame.image.load('./sprites/studio.png').convert()
super_mountain_dusk = []
for fname in sorted(os.listdir('./sprites/Super Mountain Dusk Files/Layers')):
    super_mountain_dusk.append(pygame.image.load('./sprites/Super Mountain Dusk Files/Layers/'+fname))
    hsize = true_resize(SCREEN_WIDTH, super_mountain_dusk[-1])
    super_mountain_dusk[-1] = pygame.transform.scale(super_mountain_dusk[-1], (SCREEN_WIDTH, hsize))

super_mountain_dusk_parallax_scroll = [0, 2, 3, 5, 5, 8]
maxwidth = []
for i in range(len(super_mountain_dusk)):
    maxwidth.append(math.ceil(SCREEN_WIDTH/super_mountain_dusk[i].get_width())+1+math.ceil(super_mountain_dusk_parallax_scroll[i]))

round_1_ground = pygame.image.load('./sprites/ground.png').convert()
title = pygame.image.load('./sprites/title.png').convert()
title = pygame.transform.scale(title, (SCREEN_WIDTH-200, SCREEN_HEIGHT-200)).convert()
title.set_colorkey(BLACK)
prompt = FONT_48.render('press any key to start', True, WHITE, None)
fader = pygame.surface.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)).convert()
fader.fill(BLACK)
rob = player.Player()
borders = []

for i in range(5):
    borders.append([])
    for j in range(4):
        image = pygame.image.load('./sprites/borders.png').convert()
        image.set_colorkey(BLACK)
        image = clip_image(image, (j*64, i*64, 64, 64))
        borders[i].append(image)


def show_fps(screen, clock):
    """utility function to show frames per second"""
    fps = str(int(clock.get_fps()))
    fps_surface = fps_font.render(fps, True, BLACK)
    fps_rect = fps_surface.get_rect()
    fps_rect.topleft = (10, 10)
    SCREEN.blit(fps_surface, fps_rect)


def initialize():
    centered = (SCREEN_WIDTH//2-studio_image.get_width()//2, SCREEN_HEIGHT//2-studio_image.get_height()//2)
    time.sleep(1)
    for i in range(255):
        SCREEN.fill(BLACK)
        studio_image.set_alpha(i)
        SCREEN.blit(studio_image, centered)
        pygame.display.update()
        time.sleep(0.001)
    time.sleep(1.5)
    for i in range(255, 0, -1):
        SCREEN.fill(BLACK)
        studio_image.set_alpha(i)
        SCREEN.blit(studio_image, centered)
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
                SCREEN.blit(super_mountain_dusk[j], ((i*super_mountain_dusk[j].get_width())-round(scroll*super_mountain_dusk_parallax_scroll[j]), 0))
        for i in range(0, math.ceil(SCREEN_WIDTH/round_1_ground.get_width())):
            SCREEN.blit(round_1_ground, (i*round_1_ground.get_width()-scroll, SCREEN_HEIGHT-round_1_ground.get_height()))
            SCREEN.blit(round_1_ground, (i*round_1_ground.get_width()-scroll+SCREEN_WIDTH, SCREEN_HEIGHT-round_1_ground.get_height()))
        SCREEN.blit(pygame.transform.scale2x(rob.image), (0+round_1_ground.get_width()+rob.pos.x, rob.pos.y+75))
        SCREEN.blit(title, (0, 0))
        if showing: SCREEN.blit(prompt, (350, 600), special_flags=BLEND_ALPHA_SDL2)
        fader.set_alpha(fade)
        SCREEN.blit(fader, (0, 0))
    
    update = pygame.time.get_ticks()
    cooldown = 150
    showing = True
    cur = 0
    global fade
    fade = 254
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN: return 
            if event.type == MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())
            elif event.type == QUIT:
                pygame.quit()
                quit()
        scroll += 2
        if fade > 0: fade -= 5

        if abs(scroll) > SCREEN_WIDTH:
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
    selected = 0
    controls = False
    clockobject = pygame.time.Clock()
    hsize = true_resize(600, borders[0][0])
    def render(scroll):
        for j in range(len(super_mountain_dusk)):
            for i in range(maxwidth[j]):
                SCREEN.blit(super_mountain_dusk[j], ((i*super_mountain_dusk[j].get_width())-round(scroll*super_mountain_dusk_parallax_scroll[j]), 0))
        for i in range(0, math.ceil(SCREEN_WIDTH/round_1_ground.get_width())):
            SCREEN.blit(round_1_ground, (i*round_1_ground.get_width(), SCREEN_HEIGHT-round_1_ground.get_height()))
        SCREEN.blit(pygame.transform.scale2x(rob.image), (0+round_1_ground.get_width()+rob.pos.x, rob.pos.y+75))
        SCREEN.blit(title, (0, 0))
        for i in range(len(texts)): 
            if i == selected: SCREEN.blit(FONT_24.render(texts[i], True, SELECT), (SCREEN_WIDTH//2+250, SCREEN_HEIGHT//2+185+i*50), special_flags=BLEND_ALPHA_SDL2)
            else: SCREEN.blit(FONT_24.render(texts[i], True, WHITE), (SCREEN_WIDTH//2+250, SCREEN_HEIGHT//2+185+i*50), special_flags=BLEND_ALPHA_SDL2)
        if controls:
            borders[3][2] = pygame.transform.scale(borders[3][2], (SCREEN_WIDTH-200, hsize-100))
            controltext = FONT_24.render('Controls', True, WHITE)
            SCREEN.blit(borders[3][2], (100, 100))
            SCREEN.blit(controltext, (100+round(borders[3][2].get_width()/2-controltext.get_width()/2), 185), special_flags=BLEND_ALPHA_SDL2)
            for i in range(len(controlrenders)):
                SCREEN.blit(controlrenders[i][2], controlrenders[i][1], special_flags=BLEND_ALPHA_SDL2)
                text = FONT_16.render(controlrenders[i][0], True, WHITE)
                if controlrenders[i][1][0] < 300: SCREEN.blit(text, (controlrenders[i][1][0]+controlrenders[i][2].get_width()+15, controlrenders[i][1][1]+round(controlrenders[i][2].get_height()/2-text.get_height()/2)), special_flags=BLEND_ALPHA_SDL2)
                else: SCREEN.blit(text, (controlrenders[i][1][0]-text.get_width()-15, controlrenders[i][1][1]+10), special_flags=BLEND_ALPHA_SDL2)
        
    texts = ["new game", "view controls", "quit game"]
    
    controlrenders = [["move", (220, 235)],
                    ["heal", (765,355)],
                    ["select", (210,345)], 
                    ["exit", (220,465)], 
                    ["pickup/interact", (765,295)], 
                    ["dash", (735, 235)], 
                    ["inventory", (210,405)], 
                    ["attack", (765,415)], 
                    ["jump", (765,475)]]
    x = 0
    for i in os.listdir('sprites/keys/'):
        tmp_img = pygame.image.load('sprites/keys/'+i)
        tmp_img = pygame.transform.scale(tmp_img, (tmp_img.get_width()*3, tmp_img.get_height()*3))
        controlrenders[x].append(tmp_img)
        x+=1

    update = pygame.time.get_ticks()
    cooldown = 150
    while True:
        for event in pygame.event.get():
            if controls:
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        controls = False
                if event.type == MOUSEBUTTONDOWN:
                    print(pygame.mouse.get_pos())
                elif event.type == QUIT:
                    pygame.quit()
                    quit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == K_UP:
                    selected -= 1
                if event.key == K_DOWN:
                    selected += 1
                if selected > 2: selected = 0
                elif selected < 0: selected = 2
                if event.key == K_RETURN and selected == 0:
                    GAME_STATE = 'awaken'
                    return
                if event.key == K_RETURN and selected == 1:
                    controls = True
                if event.key == K_RETURN and selected == 2:
                    pygame.quit()
                    quit() 
            elif event.type == MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())
            elif event.type == QUIT:
                pygame.quit()
                quit()
        scroll += 2

        if abs(scroll) > SCREEN_WIDTH:
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
        clockobject.tick(144)
        
clockobject = pygame.time.Clock()

initialize()
initial_screen()
menu()

pygame.quit()