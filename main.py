import player, enemy, pygame, random, math, time, os, sys
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
    rob.image = pygame.image.load(rob.sprites[rob.state][rob.a_frame]).convert_alpha()
    rob.image.set_colorkey(pygame.SRCCOLORKEY)
    rob.size = rob.image.get_size()
    rob.bigger_img = pygame.transform.scale(rob.image, (rob.size[0]*3, rob.size[1]*3))

def clip_image(image, clip):
    image.set_clip(clip)
    return image.subsurface(image.get_clip())

def show_fps(screen, clock):
    """utility function to show frames per second"""
    fps = str(int(clock.get_fps()))
    fps_surface = fps_font.render(fps, True, WHITE)
    fps_rect = fps_surface.get_rect()
    fps_rect.topleft = (10, 10)
    screen.blit(fps_surface, fps_rect)

def draw_bg(scroll):
    for j in range(len(super_mountain_dusk)):
            for i in range(-maxwidth[j], maxwidth[j]):
                SCREEN.blit(super_mountain_dusk[j], ((i*super_mountain_dusk[j].get_width())-round(scroll*super_mountain_dusk_parallax_scroll[j]), 0))

def draw_ground(scroll):
    for i in range(0, math.ceil(SCREEN_WIDTH/round_1_ground.get_width())):
        for j in range(-1, 2, 1):
            SCREEN.blit(round_1_ground, (i*round_1_ground.get_width()-scroll*5-SCREEN_WIDTH*j, SCREEN_HEIGHT-round_1_ground.get_height()))

def draw_controls(borders):
    hsize = true_resize(600, borders[0][0])
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
        tmp_img = pygame.image.load('sprites/keys/'+i).convert()
        tmp_img.set_colorkey(BLACK)
        tmp_img = pygame.transform.scale(tmp_img, (tmp_img.get_width()*3, tmp_img.get_height()*3))
        controlrenders[x].append(tmp_img)
        x+=1
    borders[3][2] = pygame.transform.scale(borders[3][2], (SCREEN_WIDTH-200, hsize-100))
    controltext = FONT_24.render('Controls', True, WHITE)
    SCREEN.blit(borders[3][2], (100, 100))
    SCREEN.blit(controltext, (100+round(borders[3][2].get_width()/2-controltext.get_width()/2), 185), special_flags=BLEND_ALPHA_SDL2)
    for i in range(len(controlrenders)):
        SCREEN.blit(controlrenders[i][2], controlrenders[i][1], special_flags=BLEND_ALPHA_SDL2)
        text = FONT_16.render(controlrenders[i][0], True, WHITE)
        if controlrenders[i][1][0] < 300: SCREEN.blit(text, (controlrenders[i][1][0]+controlrenders[i][2].get_width()+15, controlrenders[i][1][1]+round(controlrenders[i][2].get_height()/2-text.get_height()/2)), special_flags=BLEND_ALPHA_SDL2)
        else: SCREEN.blit(text, (controlrenders[i][1][0]-text.get_width()-15, controlrenders[i][1][1]+10), special_flags=BLEND_ALPHA_SDL2)

pygame.init()

#show fps
fps = pygame.time.Clock()

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

fps_font = pygame.font.SysFont("monospace", 20)

studio_image = pygame.image.load('./sprites/studio.png').convert()
super_mountain_dusk = []
for fname in sorted(os.listdir('./sprites/Super Mountain Dusk Files/Layers')):
    image = pygame.image.load('./sprites/Super Mountain Dusk Files/Layers/'+fname).convert()
    image.set_colorkey(BLACK)
    super_mountain_dusk.append(image)
    hsize = true_resize(SCREEN_WIDTH, super_mountain_dusk[-1])
    super_mountain_dusk[-1] = pygame.transform.scale(super_mountain_dusk[-1], (SCREEN_WIDTH, hsize))

super_mountain_dusk_parallax_scroll = [0, 1, 2, 5, 7, 12]
maxwidth = []
for i in range(len(super_mountain_dusk)):
    maxwidth.append(math.ceil(SCREEN_WIDTH/super_mountain_dusk[i].get_width())+1+math.ceil(super_mountain_dusk_parallax_scroll[i]))

round_1_ground = pygame.image.load('./sprites/ground_big.png').convert()
round_1_ground.set_colorkey(WHITE)
round_1_ground = clip_image(round_1_ground, (32, 0, 32, 32))
round_1_ground = pygame.transform.scale(round_1_ground, (64, 64))
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
    startTime = time.time()
    centered = (SCREEN_WIDTH//2-studio_image.get_width()//2, SCREEN_HEIGHT//2-studio_image.get_height()//2)
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN: return
        currentTime = time.time() - startTime
        if currentTime < 1:
            SCREEN.fill(BLACK)
            studio_image.set_alpha(currentTime*255)
            SCREEN.blit(studio_image, centered)
            pygame.display.update()
        elif 2.5 < currentTime < 3.5:
            SCREEN.fill(BLACK)
            studio_image.set_alpha( (1 - (currentTime-2.5)) * 255)
            SCREEN.blit(studio_image, centered)
            pygame.display.update()
        elif currentTime > 3.5:
            break

def initial_screen():
    global scroll
    scroll = 0
    clockobject = pygame.time.Clock()
    def render(scroll):
        draw_bg(scroll)
        SCREEN.blit(title, (0, 0))
        if showing: SCREEN.blit(prompt, (350, 575), special_flags=BLEND_ALPHA_SDL2)
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
        scroll += 0.2
        if fade > 0: fade -= 0.5

        if abs(scroll) > SCREEN_WIDTH:
            scroll = 0
        
        cur += 1
        if cur >= 100:
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

def menu():
    global scroll
    global GAME_STATE
    selected = 0
    controls = False
    clockobject = pygame.time.Clock()
    def render(scroll):
        draw_bg(scroll)
        SCREEN.blit(title, (0, 0))
        for i in range(len(texts)): 
            if i == selected: SCREEN.blit(FONT_24.render(texts[i], True, SELECT), (SCREEN_WIDTH//2+230, SCREEN_HEIGHT//2+155+i*50), special_flags=BLEND_ALPHA_SDL2)
            else: SCREEN.blit(FONT_24.render(texts[i], True, WHITE), (SCREEN_WIDTH//2+225, SCREEN_HEIGHT//2+155+i*50), special_flags=BLEND_ALPHA_SDL2)
        if controls:
            draw_controls(borders)
            
    texts = ["new game", "view controls", "quit game"]
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
                selected = selected - (event.key == K_UP) + (event.key == K_DOWN)
                if selected > 2: selected = 0
                elif selected < 0: selected = 2
                if event.key == K_RETURN and selected == 0:
                    GAME_STATE = 'playing'
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
        
        if pygame.time.get_ticks() - update >= cooldown: update = pygame.time.get_ticks(); animate()
        scroll += 0.2

        if abs(scroll) > SCREEN_WIDTH:
            scroll = 0

        render(scroll)
        
        pygame.display.flip()
        clockobject.tick(60)

def fadeout():
    fade = 0
    SCREEN.fill((0,0,0))
    scroll = 0
    clockobject = pygame.time.Clock()
    update_ticks = pygame.time.get_ticks()
    def update():
        nonlocal scroll
        global fade
        scroll += 0.2
        fade += 0.5
        clockobject.tick(60)
        if abs(scroll) > SCREEN_WIDTH:
            scroll = 0
        SCREEN.fill((0,0,0))
        render(scroll)
        pygame.display.flip()

    def render(scroll):
        draw_bg(scroll)
        SCREEN.blit(title, (0, 0))
        fader.set_alpha(fade)
        SCREEN.blit(fader, (0, 0))
    while fade < 255:
        fade += 5
        update()
        if pygame.time.get_ticks() -  update_ticks >= 150: 
            animate()
            update_ticks = pygame.time.get_ticks()
        pygame.display.flip()
        clockobject.tick(60)
    fade = 0

    GAME_STATE = 'playing'
    return

def play():
    global GAME_STATE, controls
    rob_profile = pygame.image.load(os.path.join('sprites', 'rob_profile.png')).convert_alpha()
    rob_profile = pygame.transform.scale(rob_profile, (rob_profile.get_width()*3, rob_profile.get_height()*3))
    stagex = SCREEN_WIDTH*2
    stageposx = 0
    fade = 255
    SCREEN.fill((0,0,0))
    scroll = 0
    clockobject = pygame.time.Clock()
    rob.pos = pygame.Vector2(SCREEN_WIDTH/2-rob.image.get_width()/2, rob.pos.y+round_1_ground.get_height()-55)
    hsize = true_resize(600, borders[1][2])
    paused = False
    pausetexts = ['resume', 'view controls', 'quit to main menu', 'quit to desktop']
    warningtexts = ['yes', 'no']
    controls = False
    selected = 0
    selected2 = 0
    warning = False
    def render(scroll):
        if GAME_STATE == 'paused': 
            if controls:
                draw_controls(borders)
            elif warning:
                warning_text = FONT_24.render('warning: all progress will be lost, are you sure?', True, RED)
                SCREEN.blit(warning_text, (225, 225))
                for i in range(len(warningtexts)):
                    text = FONT_24.render(warningtexts[i], True, WHITE)
                    if i == selected2:
                        text = FONT_24.render(warningtexts[i], True, SELECT) 
                        SCREEN.blit(text, (round((borders[2][3].get_width())/2-text.get_width()/2+25)+i*150, -5+round(hsize/2-text.get_height()/2)), special_flags=BLEND_ALPHA_SDL2)
                    else: SCREEN.blit(text, (round((borders[2][3].get_width())/2-text.get_width()/2+25)+i*150, -5+round(hsize/2-text.get_height()/2)), special_flags=BLEND_ALPHA_SDL2)
            else:
                borders[2][3] = pygame.transform.scale(borders[2][3], (SCREEN_WIDTH-200, hsize-100))
                SCREEN.blit(borders[2][3], (100, 100))
                SCREEN.blit(FONT_48.render('paused', True, WHITE), (round((borders[2][3].get_width())/2-FONT_48.render('paused', True, WHITE).get_width()/2+115), 25))
                for i in range(len(pausetexts)):
                    text = FONT_24.render(pausetexts[i], True, WHITE)
                    if i == selected:
                        text = FONT_24.render(pausetexts[i], True, SELECT) 
                        SCREEN.blit(text, (round((borders[2][3].get_width())/2-text.get_width()/2+115), 35+round(hsize/2-text.get_height()/2)+i*50), special_flags=BLEND_ALPHA_SDL2)
                    else: SCREEN.blit(text, (round((borders[2][3].get_width())/2-text.get_width()/2+115), 35+round(hsize/2-text.get_height()/2)+i*50), special_flags=BLEND_ALPHA_SDL2)
            return False
        draw_bg(scroll)
        draw_ground(scroll)
        b_img = pygame.transform.scale2x(borders[0][0])
        p_img = clip_image(rob.image, (56,6,29,23))
        p_img = pygame.transform.scale(p_img, (p_img.get_width()*3, p_img.get_height()*3))
        SCREEN.blit(b_img, (25, 25))
        SCREEN.blit(p_img, (25 + b_img.get_width()/2 - rob_profile.get_width()/2, p_img.get_height()))
        if rob.facing: SCREEN.blit(pygame.transform.scale2x(rob.image), rob.pos)
        else: SCREEN.blit(pygame.transform.flip(pygame.transform.scale2x(rob.image), True, False), rob.pos)
        fader.set_alpha(fade)
        SCREEN.blit(fader, (0, 0))
        return True
        
    update = pygame.time.get_ticks()
    cooldown = 150
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if controls:
                        controls = False
                        continue
                    if warning: 
                        warning = False
                        continue
                    if GAME_STATE == 'playing': GAME_STATE = 'paused'
                    else: GAME_STATE = 'playing'
                if GAME_STATE == 'paused' and not controls and not warning:
                    selected = selected - (event.key == K_UP) + (event.key == K_DOWN)
                    if selected > 3: selected = 0
                    elif selected < 0: selected = 3
                    if event.key == K_RETURN and selected == 0:
                        GAME_STATE = 'playing'
                        continue
                    if event.key == K_RETURN and selected == 1:
                        controls = True
                        continue
                    if event.key == K_RETURN and selected == 2:
                        warning = True
                        continue
                    if event.key == K_RETURN and selected == 3:
                        warning = True
                        continue
                if warning:
                    selected2 = selected2 - (event.key == K_LEFT) + (event.key == K_RIGHT)
                
                    if selected2 > 1: selected2 = 0
                    elif selected2 < 0: selected2 = 1
                
                    if event.key == K_RETURN and selected2 == 1:
                        warning = False
                    if event.key == K_RETURN and selected2 == 0:
                        if selected == 2:
                            GAME_STATE = 'menu'
                            return 
                        if selected == 3:
                            pygame.quit()
                            quit()
        rob.update(pygame.key.get_pressed())
        if fade > 0: fade -= 0.5
        if pygame.time.get_ticks() - update >= cooldown:
            if rob.attacking > 1:
                rob.state = rob.attack_type
                cooldown = 75
                rob.attacking -= 1
            else:
                cooldown = 150
            update = pygame.time.get_ticks()
            animate()
        if not render(scroll): 
            show_fps(SCREEN, clockobject)
            pygame.display.flip()
            clockobject.tick(144)
            continue
            
        if int(stageposx) > 50 and rob.facing: rob.vel.x = 0
        elif int(stageposx) < -50 and not rob.facing: rob.vel.x = 0
        elif rob.vel.x != 0: scroll += int(rob.vel.x/abs(rob.vel.x))*0.2; stageposx += int(rob.vel.x/abs(rob.vel.x))*0.2
        
        
        show_fps(SCREEN, clockobject)
        pygame.display.flip()
        clockobject.tick(144)

clockobject = pygame.time.Clock()

initialize()
initial_screen()
menu()
fadeout()
rob.state = 'idle'
GAME_STATE = 'playing'
while True:
    if GAME_STATE == 'playing':
        play()
    elif GAME_STATE == 'menu':
        fadeout()
        menu()

