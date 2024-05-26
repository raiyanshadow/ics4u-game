import pygame.camera
import player, enemy, pygame, random, math, time, os, sys, barrier_line, healthbar, grounds
from constants import *
from pygame.locals import *
global update

done = False

def true_resize(target_width, original_image):
    size = original_image.get_width()*original_image.get_height()
    wpercent = target_width / float(size)
    hsize = int((float(size) * float(wpercent)))
    return hsize

def animate():
    if not rob.dead: rob.a_frame = (rob.a_frame + 1) % len(rob.sprites[rob.state])
    rob.image = rob.sprites[rob.state][rob.a_frame]
    rob.mask = pygame.mask.from_surface(rob.image)
    rob.size = rob.image.get_size()

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
        render(scroll)
        pygame.display.flip()

death_done = 0

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
        
        scroll += 0.2

        if abs(scroll) > SCREEN_WIDTH:
            scroll = 0

        render(scroll)
        
        pygame.display.flip()
        clockobject.tick(FRAMES)

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
        pygame.display.flip()
        clockobject.tick(60)
    fade = 0

    GAME_STATE = 'playing'
    return
deathfade = 0

def play():
    global GAME_STATE, controls
    rob_profile = pygame.image.load(os.path.join('sprites', 'rob_profile.png')).convert_alpha()
    rob_profile = pygame.transform.scale(rob_profile, (112, 112))
    stagex = SCREEN_WIDTH*2
    stageposx = 0
    hbar = healthbar.HealthBar(0, 0, rob)
    startscrollingposx = SCREEN_WIDTH/2
    playerposx = SCREEN_WIDTH/2-rob_profile.get_width()/2
    fade = 255
    SCREEN.fill((0,0,0))
    scroll = 0
    clockobject = pygame.time.Clock()
    next_dash_frame = 0
    dash_frame = 0
    hsize = true_resize(600, borders[1][2])
    paused = False
    pausetexts = ['resume', 'view controls', 'quit to main menu', 'quit to desktop']
    warningtexts = ['yes', 'no']
    controls = False
    selected = 0
    selected2 = 0
    warning = False
    rad = 0.1
    barrierleft = pygame.draw.rect(SCREEN, WHITE, (20, 0, 5, SCREEN_HEIGHT))
    barrierright = pygame.draw.rect(SCREEN, WHITE, (SCREEN_WIDTH-20, 0, 5, SCREEN_HEIGHT))
    ground_group = pygame.sprite.Group()
    for i in range(0, math.ceil(SCREEN_WIDTH/64)):
        for j in range(-1, 2, 1):
            ground_group.add(grounds.Ground(i*64, SCREEN_HEIGHT-64, (0, 1), scroll))
    ground_group.add(grounds.Ground(SCREEN_WIDTH//2-200, 455, (0, 2), scroll), grounds.Ground(SCREEN_WIDTH//2+275, 455, (0, 2), scroll), 
                     grounds.Ground(SCREEN_WIDTH//2-200-64, 455, (0, 1), scroll), grounds.Ground(SCREEN_WIDTH//2+275-64, 455, (0, 1), scroll),
                     grounds.Ground(SCREEN_WIDTH//2-200-64*2, 455, (0, 0), scroll), grounds.Ground(SCREEN_WIDTH//2+275-64*2, 455, (0, 0), scroll))
    heartbeatfps = 30
    heart_anim = 1

    def render(scroll, dash_frame, heart_anim):
        global fader
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
        ground_group.draw(SCREEN)
        b_img = pygame.transform.scale2x(borders[0][0])
        p_img = clip_image(rob.image, (56*2,6*2,29*2,23*2))
        hbar.update()
        heartpos = (25+b_img.get_width()+10, hbar.image.get_height())
        SCREEN.blit(pygame.image.load(f'./sprites/heart{heart_anim+1}.png').convert_alpha(), heartpos)
        SCREEN.blit(FONT_24.render(str(rob.no_hpcharges), True, WHITE), (heartpos[0] + 60, heartpos[1] + 20))
        SCREEN.blit(b_img, (25, 25))
        SCREEN.blit(rob_profile, (25 + b_img.get_width()/2 - rob_profile.get_width()/2, p_img.get_height()))
        if rob.facing: 
            SCREEN.blit(rob.mask.to_surface(setcolor=(255, 255, 255, 255), unsetcolor=(0, 0, 0, 0)), rob.rect)
            SCREEN.blit(rob.image, rob.rect)
        else: 
            SCREEN.blit(pygame.transform.flip(rob.mask.to_surface(setcolor=(255, 255, 255, 255), unsetcolor=(0, 0, 0, 0)), True, False), rob.rect)
            SCREEN.blit(pygame.transform.flip(rob.image, True, False), rob.rect)
        if rob.dead: 
            if pygame.time.get_ticks() - death_done > 1000:
                fader = pygame.surface.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)).convert()
                fader.fill(BLACK)
                fader.set_alpha(fade)
                SCREEN.blit(fader, (0, 0))
        if rob.dashing and rob.facing:
            SCREEN.blit(pygame.transform.scale2x(pygame.image.load(f'./sprites/dash_fx{dash_frame+1}.png').convert_alpha()), (rob.rect.x, rob.rect.y))
        elif rob.dashing:
            SCREEN.blit(pygame.transform.flip(pygame.transform.scale2x(pygame.image.load(f'./sprites/dash_fx{dash_frame+1}.png').convert_alpha()), True, False), (rob.rect.x, rob.rect.y))
        fader.set_alpha(fade)
        SCREEN.blit(fader, (0, 0))
        return True
        
    updatea = pygame.time.get_ticks()
    updateb = pygame.time.get_ticks()
    JUMP_TIMER = pygame.time.get_ticks()
    cooldown = 150
    fps = 150
    while True:
        collided = []
        for obstacle in ground_group:
            rob.falling = False
            collision = pygame.sprite.collide_mask(rob, obstacle)
            if collision: collided.append(obstacle)
        for col in collided:
            if (rob.rect.top < col.rect.bottom and rob.rect.bottom > col.rect.bottom):
                rob.rect.top = col.rect.bottom
                rob.vel.y = 0
                rob.falling = True
                rob.jumping = False
                
            if (rob.rect.bottom-25 > col.rect.top and rob.rect.top < col.rect.top):
                rob.rect.y = col.rect.y-rob.rect.height
                rob.vel.y = 0
                rob.jumping = False
        if len(collided) == 0 and not rob.falling:
            fps = 15
            rob.falling = True       
        
        x = pygame.event.get()
        for event in x:
            if event.type == QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:
                if event.key == K_z and not rob.jumping and not rob.falling:
                    rob.vel.y = 22
                    rob.a_frame = 0
                    rob.jumping = True
                    rob.falling = False
                    rob.jumpinganim = len(rob.sprites['jump'])

                if event.key == K_ESCAPE:
                    if controls:
                        controls = False
                        continue
                    if warning: 
                        warning = False
                        continue
                    if GAME_STATE == 'playing': GAME_STATE = 'paused'
                    else: GAME_STATE = 'playing'
                
                if event.key == K_LSHIFT:
                    rob.dashing = True
                    rob.dash_time = pygame.time.get_ticks()
                    rob.veldash = 15*(-1 if not rob.facing else 1)
                    next_dash_frame = rob.dash_time
                
                if event.key == K_c and rob.no_hpcharges > 0:
                    rob.a_frame = 0
                    rob.healing = True
                    rob.state == 'heal'
                    rob.heal_time = pygame.time.get_ticks()

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
                if event.key == K_x and not rob.attackBool:
                    rob.attack()
            if event.type == MOUSEBUTTONDOWN:
                rob.hurt()
                print(pygame.mouse.get_pos())
        rob.update(pygame.key.get_pressed(), JUMP_TIMER)
        if rob.dead:
                death()
                return
        if fade > 0: fade -= 0.5
        if pygame.time.get_ticks() - updatea > fps:
            if rob.state == 'walk':
                fps = 150
            if rob.attacking > 1:
                rob.attacking -= 1
                rob.state = rob.attack_type
                fps = 50
            if rob.attacking == 1 and rob.attackBool:
                rob.attackBool = False
                rob.state = 'idle'
            if rob.hurting > 1 and rob.hp > 0:
                rob.hurting -= 1
                rob.state = 'hurt'
                fps = 100
            if rob.jumping == True:
                fps = 15
                rob.jump_update(fps)
            if collided == [] and not rob.jumping and rob.falling:
                fps = 15
                rob.fall()
            if rob.dashing:
                rob.dash(pygame.time.get_ticks())
                if pygame.time.get_ticks() - next_dash_frame > 120:
                    dash_frame = (dash_frame + 1) % 3
                fps = 15
            if rob.healing: 
                rob.heal(pygame.time.get_ticks())
                rob.state = 'heal'
                fps = 90
            if (not rob.hurting > 1 and not rob.attackBool and rob.state != 'walk' and rob.state != 'jump' and rob.state != 'deathanimation' 
                and not rob.falling and not rob.dashing and not rob.healing):
                rob.state = 'idle'
                fps = 150
            
            animate()
            updatea = pygame.time.get_ticks()

        if pygame.time.get_ticks() - updateb > 200:
            heart_anim = (heart_anim + 1) % 4
            print(heart_anim)
            updateb = pygame.time.get_ticks()
        
        if not render(scroll, dash_frame, heart_anim): 
            show_fps(SCREEN, clockobject)
            pygame.display.flip()
            clockobject.tick(FRAMES)
            continue
        i = 1
        

        show_fps(SCREEN, clockobject)
        pygame.display.flip()
        clockobject.tick(FRAMES)

def death():
    global fader, fade, GAME_STATE, scroll
    ground_group = pygame.sprite.Group()
    for i in range(0, math.ceil(SCREEN_WIDTH/64)):
        for j in range(-1, 2, 1):
            ground_group.add(grounds.Ground(i*64, SCREEN_HEIGHT-64, (0, 1), scroll))
    ground_group.add(grounds.Ground(SCREEN_WIDTH//2-325, 455, (0, 2), scroll), grounds.Ground(SCREEN_WIDTH//2+325, 455, (0, 2), scroll), 
                     grounds.Ground(SCREEN_WIDTH//2-325-64, 455, (0, 1), scroll), grounds.Ground(SCREEN_WIDTH//2+325-64, 455, (0, 1), scroll),
                     grounds.Ground(SCREEN_WIDTH//2-325-64*2, 455, (0, 0), scroll), grounds.Ground(SCREEN_WIDTH//2+325-64*2, 455, (0, 0), scroll))
    fadebg = 0
    fade = 0
    rob_profile = pygame.image.load(os.path.join('sprites', 'rob_profile.png')).convert_alpha()
    rob_profile = pygame.transform.scale(rob_profile, (112, 112))
    hbar = healthbar.HealthBar(0, 0, rob)
    rob.rect.y += 15
    playerposx = rob.rect.x
    SCREEN.fill((0,0,0))
    clockobject = pygame.time.Clock()
    hsize = true_resize(600, borders[1][2])
    texts = ['quit to menu', 'quit to desktop']
    controls = False
    selected = 0
    rad = 0.1
    scroll = 0
    timer = [0] * 6
    animdone = False
    timerbool = [False] * 5
    rob.a_frame = 0
    death = pygame.image.load(os.path.join('sprites', 'death.png')).convert_alpha()
    death = pygame.transform.scale(death, (SCREEN_WIDTH, death.get_height()))
    death.set_alpha(0)
    selected = 0
                        
    def render(scroll):
        draw_bg(scroll)
        ground_group.draw(SCREEN)
        b_img = pygame.transform.scale2x(borders[0][0])
        p_img = clip_image(rob.image, (0, 0,29,23))
        p_img = pygame.transform.scale(rob_profile, (p_img.get_width()*3, p_img.get_height()*3))
        hbar.update()
        SCREEN.blit(b_img, (25, 25))
        SCREEN.blit(p_img, (25 + b_img.get_width()/2 - rob_profile.get_width()/2, p_img.get_height()))
        rob.state = 'deathanimation'
        rob.a_frame = min(rob.a_frame+1, len(rob.sprites[rob.state])-1)
        rob.image = rob.sprites[rob.state][rob.a_frame].convert_alpha()
        rob.mask = pygame.mask.from_surface(rob.image)
        if rob.facing: 
            SCREEN.blit(rob.mask.to_surface(setcolor=(255, 255, 255, 255), unsetcolor=(0, 0, 0, 0)), rob.rect)
            SCREEN.blit(rob.image, rob.rect)
        else: 
            SCREEN.blit(pygame.transform.flip(rob.mask.to_surface(setcolor=(255, 255, 255, 255), unsetcolor=(0, 0, 0, 0)), True, False), rob.rect)
            SCREEN.blit(pygame.transform.flip(rob.image, True, False), rob.rect)

    def parta():
        global animdone
        render(scroll)
        pygame.display.flip()
    
    def partb():
        render(scroll)
        fader.set_alpha(fadebg)
        SCREEN.blit(fader, (0, 0))
        pygame.display.flip()
        
    def partc():
        render(scroll)
        fader.set_alpha(fadebg)
        SCREEN.blit(fader, (0, 0))
        death.set_alpha(fade)
        SCREEN.blit(death, (0, SCREEN_HEIGHT//2 - death.get_height()//2))
        pygame.display.flip()

    def partd():
        render(scroll)
        fader.set_alpha(fadebg)
        SCREEN.blit(fader, (0, 0))
        death.set_alpha(fade)
        SCREEN.blit(death, (0, SCREEN_HEIGHT//2 - death.get_height()//2))
        for i in range(len(texts)):
            text = 0
            if i == selected: 
                text = FONT_24.render(texts[i], True, SELECT)
            else: 
                text = FONT_24.render(texts[i], True, WHITE)
            SCREEN.blit(text, (430*i+200, SCREEN_HEIGHT//2+155), special_flags=BLEND_ALPHA_SDL2)
        pygame.display.flip()
        
    timer[0] = pygame.time.get_ticks()
    while animdone == False:
        if pygame.time.get_ticks() - timer[0] > 400:
            if animdone:
                break
            timer[0] = pygame.time.get_ticks()
            parta()
            continue
        if rob.a_frame == len(rob.sprites[rob.state])-1:
            animdone = True
        
    timer[1] = pygame.time.get_ticks()
    while not timerbool[0]:
        if pygame.time.get_ticks() - timer[1] > 250:
            timer[1] = pygame.time.get_ticks()
            timerbool[0] = True
    
    timer[2] = pygame.time.get_ticks()
    while not timerbool[1]:
        if fadebg == 124:
            timerbool[1] = True
        else: 
            if pygame.time.get_ticks() - timer[2] > 50:
                timer[2] = pygame.time.get_ticks()
                fadebg = min(fadebg+2, 124)
                partb()
    timer[3] = pygame.time.get_ticks()
    while not timerbool[2]:
        if pygame.time.get_ticks() - timer[3] > 250:
            timer[3] = pygame.time.get_ticks()
            timerbool[2] = True
    timer[4] = pygame.time.get_ticks()
    while not timerbool[3]:
        if pygame.time.get_ticks() - timer[4] > 25:
            timer[4] = pygame.time.get_ticks()
            fade = min(fade+5, 255)
            partc()
        if fade == 255: timerbool[3] = True
    timer[5] = pygame.time.get_ticks()
    while not timerbool[4]:
        if pygame.time.get_ticks() - timer[5] > 1000:
            timer[5] = pygame.time.get_ticks()
            timerbool[4] = True
        
    
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    selected += 1
                    if selected >= len(texts): selected = 0
                if event.key == K_LEFT:
                    selected -= 1
                    if selected < 0: selected = len(texts)-1
                if event.key == K_RETURN:
                    if selected == 0:
                        GAME_STATE = 'menu'
                        rob.__init__()
                        return
                    else:
                        pygame.quit()
                        quit()
        partd()
        
            
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

