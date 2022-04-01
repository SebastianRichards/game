import pygame, sys, random

def draw_floor():
    screen.blit(floor_surface,(floor_x_pos,655))
    screen.blit(floor_surface,(floor_x_pos + 536 ,655))

def create_hook():
    random_hook_position = random.choice(hook_height)
    bottom_hook = hook_surface.get_rect(midtop = (700,random_hook_position))
    top_hook = hook_surface.get_rect(midbottom = (700,random_hook_position - 300))
    return bottom_hook,top_hook

def create_monster():
    random_monster_position = random.choice(monster_height)
    monster_position = monster_surface.get_rect(center = (700, random_monster_position))
    return monster_position

def move_monster(monsters):
    for monster in monsters:
        monster.centerx -= 6
    return monsters

def move_hooks(hooks):
    for hook in hooks:
        hook.centerx -= 5
    return hooks

def draw_monsters(monsters):
    for monster in monsters:
        screen.blit(monster_surface, monster)

def draw_hooks(hooks):
    for hook in hooks:
        if hook.bottom >= 400:
            screen.blit(hook_surface,hook)
        else:
            flip_hook = pygame.transform.flip(hook_surface,False,True)
            screen.blit(flip_hook,hook)

def check_collision(pipes, monsters):
    for pipe in pipes:
        if shark_rect.colliderect(pipe):
            death_sound.play()
            return False
    if shark_rect.top <= -100 or shark_rect.bottom >= 900:
        return False
    for monster in monsters:
        if shark_rect.colliderect(monster):
            death_sound.play()
            return False
    return True

def rotate_shark(shark):
    new_shark = pygame.transform.rotozoom(shark,shark_movement * -3,1)
    return new_shark

def shark_animation():
    new_shark = shark_frames[shark_index]
    new_shark_rect = new_shark.get_rect(center = (100,shark_rect.centery))
    return new_shark, new_shark_rect

def monster_animation():
    new_monster = monster_frames[monster_index]
    return new_monster

def coral_animation():
    new_coral = floor_frames[floor_index]
    return new_coral


def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (245,50))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}',True,(255,255,255))
        score_rect = score_surface.get_rect(center = (245,50))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f'High score: {int(high_score)}',True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (245,150))
        screen.blit(high_score_surface,high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

pygame.init()

game_font = pygame.font.Font("04B_19.ttf",40)

screen = pygame.display.set_mode((490,765))

clock = pygame.time.Clock()

#GAME VARIABLES
gravity = 0.10
shark_movement = 0
score = 0
high_score = 0

game_active = True

#the convert isnt nec essary but it can convert the data type to one more familiar in pygame and make it run faster
bg_surface = pygame.image.load('assets/background.png').convert()

#we do this to scale our image
bg_surface = pygame.transform.scale2x(bg_surface)


floor1 = pygame.image.load('assets/coral1.png').convert()
floor1 = pygame.transform.scale2x(floor1)
floor2 = pygame.image.load('assets/coral2.png').convert()
floor2 = pygame.transform.scale2x(floor2)
floor_x_pos = 0

floor_frames = [floor1, floor2]
floor_index = 0
floor_surface = floor_frames[floor_index]

CORALEVENT = pygame.USEREVENT + 2
pygame.time.set_timer(CORALEVENT, 500)

shark1 = pygame.transform.scale2x(pygame.image.load('assets/shark1.png').convert_alpha())
shark2 = pygame.transform.scale2x(pygame.image.load('assets/shark2.png').convert_alpha())
shark3 = pygame.transform.scale2x(pygame.image.load('assets/shark3.png').convert_alpha())
shark4 = pygame.transform.scale2x(pygame.image.load('assets/shark4.png').convert_alpha())
shark5 = pygame.transform.scale2x(pygame.image.load('assets/shark5.png').convert_alpha())
shark_frames = [shark1, shark2, shark3, shark4, shark5]
shark_index = 0
shark_surface = shark_frames[shark_index]
shark_rect = shark_surface.get_rect(center = (100,512))

SHARKFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(SHARKFLAP, 200)




monster1 = pygame.image.load('assets/monster1.png')
monster2 = pygame.image.load('assets/monster2.png')
monster_frames = [monster1, monster2]
monster_index = 0
monster_surface = monster_frames[monster_index]

MONSTERBITE = pygame.USEREVENT + 5
pygame.time.set_timer(MONSTERBITE, 200)

monster_list = []
monster_height = [300, 400, 500]
SPAWNMONSTER = pygame.USEREVENT + 3
pygame.time.set_timer(SPAWNMONSTER, 2400)

hook_surface = pygame.image.load('assets/hook.png')
hook_surface = pygame.transform.scale2x(hook_surface)
hook_surface = pygame.transform.flip(hook_surface, True, False)
hook_list = []
hook_height = [600,500,400]
SPAWNHOOK = pygame.USEREVENT
pygame.time.set_timer(SPAWNHOOK,1200)

event_list = ["hook", "hook", "hook", "hook", "hook", "hook", "hook", "hook", "hook", "hook", "hook", "monster"]

SPAWNSOMETHING = pygame.USEREVENT + 4
pygame.time.set_timer(SPAWNSOMETHING, 1200)

game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/gameoverscreen.png'))
game_over_rect = game_over_surface.get_rect(center = (245,375))


death_sound = pygame.mixer.Sound('sound/Nope.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
monster_sound = pygame.mixer.Sound('sound/sample.wav')


#game loop
while True:

    #we're doing this so we can create our game loop and exit it too
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            #need to use sys otherwise we get an error just with the while loop
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                shark_movement = 0
                shark_movement -= 5
            #newgame function
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                hook_list.clear()
                monster_list.clear()
                shark_rect.center = (100,512)
                shark_movement = 0
                score = 0

        #if event.type == SPAWNHOOK:
            #hook_list.extend(create_hook())
        if event.type == MONSTERBITE:
            if monster_index < 1:
                monster_index += 1
            else:
                monster_index = 0
            monster_surface = monster_animation()


        #if event.type == SPAWNMONSTER:
            #monster_list.append(create_monster())
        if event.type == SPAWNSOMETHING:
            selected_event = random.choice(event_list)
            if selected_event == "hook":
                hook_list.extend(create_hook())
            else:
                monster_list.append(create_monster())
                if game_active == True:
                    monster_sound.play()

        if event.type == SHARKFLAP:
            if shark_index < 4:
                shark_index += 1
            else:
                shark_index = 0

            shark_surface, shark_rect = shark_animation()
        if event.type == CORALEVENT:
            if floor_index < 1:
                floor_index += 1
            else:
                floor_index = 0
            floor_surface = coral_animation()





    screen.blit(bg_surface,(0,0))

    if game_active == True:
        #shark
        shark_movement += gravity
        rotated_shark = rotate_shark(shark_surface)
        shark_rect.centery += shark_movement
        screen.blit(rotated_shark,(shark_rect))
        game_active = check_collision(hook_list, monster_list)

        #hooks
        hook_list = move_hooks(hook_list)
        draw_hooks(hook_list)

        monster_list = move_monster(monster_list)
        draw_monsters(monster_list)

        #score
        score_display('main_game')
        score += 0.01
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score,high_score)
        score_display('game_over')


    #floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -536:
        floor_x_pos = 0

    pygame.display.update()
    #this limits the frame rate, no more than 120 fps
    clock.tick(120)
