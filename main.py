import pygame, sys, random, asyncio

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

def move_monster(monsters, dt):
    for monster in monsters:
        monster.centerx -= monster_speed * dt
    return monsters

def move_hooks(hooks, dt):
    for hook in hooks:
        hook.centerx -= hook_speed * dt
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
    collision_rect = shark_rect.inflate(-20, -20) 
    
    for pipe in pipes:
        if collision_rect.colliderect(pipe):
            death_sound.play()
            return False
    if shark_rect.top <= -100 or shark_rect.bottom >= 900:
        return False
    for monster in monsters:
        if collision_rect.colliderect(monster):
            death_sound.play()
            return False
    return True

def rotate_shark(shark):
    # Clamp rotation to a reasonable range for the dip effect (-30 to 30 degrees)
    rotation_angle = max(-20, min(20, shark_movement * -0.1))
    new_shark = pygame.transform.rotozoom(shark, rotation_angle, 1)
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

def check_score(hooks, monsters):
    global score, scored_hooks, scored_monsters
    
    # Check hooks - score when shark passes through the gap
    for i in range(0, len(hooks), 2):
        if i + 1 < len(hooks):  # Make sure we have a complete pair
            bottom_hook = hooks[i]
            top_hook = hooks[i + 1]
            # Check if shark has passed the hook pair and hasn't been scored yet
            if (bottom_hook.centerx < shark_rect.centerx and 
                id(bottom_hook) not in scored_hooks):
                score += 1
                scored_hooks.add(id(bottom_hook))
                scored_hooks.add(id(top_hook))
                score_sound.play()
    
    # Check monsters - score when shark passes by them
    for monster in monsters:
        if (monster.centerx < shark_rect.centerx and 
            id(monster) not in scored_monsters):
            score += 1
            scored_monsters.add(id(monster))
            score_sound.play()

pygame.init()

game_font = pygame.font.Font(None, 40)

screen = pygame.display.set_mode((490,765))

clock = pygame.time.Clock()

#GAME VARIABLES
gravity = 600.0  # pixels per second squared
shark_movement = 0
shark_jump_speed = -300.0  # pixels per second
hook_speed = 200.0  # pixels per second
monster_speed = 360.0  # pixels per second
floor_speed = 60.0  # pixels per second
score_increment = 1.0  # points per second
score = 0
high_score = 0

# Sets to track which obstacles have been scored
scored_hooks = set()
scored_monsters = set()

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


death_sound = pygame.mixer.Sound('assets/Nope.wav')
score_sound = pygame.mixer.Sound('assets/sfx_point.wav')
score_sound.set_volume(0.3)  
monster_sound = pygame.mixer.Sound('assets/sample.wav')


async def main():
    global game_active, shark_movement, score, high_score, floor_x_pos
    global hook_list, monster_list, shark_rect, shark_surface, shark_index
    global monster_surface, monster_index, floor_surface, floor_index
    global scored_hooks, scored_monsters
    
    while True:
    # Get delta time in seconds
        dt = clock.tick(120) / 1000.0  # Convert milliseconds to seconds

        #we're doing this so we can create our game loop and exit it too
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                #need to use sys otherwise we get an error just with the while loop
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_active:
                    shark_movement = shark_jump_speed
                #newgame function
                if event.key == pygame.K_SPACE and game_active == False:
                    game_active = True
                    hook_list.clear()
                    monster_list.clear()
                    scored_hooks.clear()
                    scored_monsters.clear()
                    shark_rect.center = (100,512)
                    shark_movement = 0
                    score = 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and game_active:  
                    shark_movement = shark_jump_speed
                if event.button == 1 and game_active == False:  
                    game_active = True
                    hook_list.clear()
                    monster_list.clear()
                    scored_hooks.clear()
                    scored_monsters.clear()
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
            shark_movement += gravity * dt
            rotated_shark = rotate_shark(shark_surface)
            shark_rect.centery += shark_movement * dt
            screen.blit(rotated_shark,(shark_rect))
            game_active = check_collision(hook_list, monster_list)

            #hooks
            hook_list = move_hooks(hook_list, dt)
            draw_hooks(hook_list)

            monster_list = move_monster(monster_list, dt)
            draw_monsters(monster_list)

            #score - check for passing obstacles
            check_score(hook_list, monster_list)
            score_display('main_game')
        else:
            screen.blit(game_over_surface,game_over_rect)
            high_score = update_score(score,high_score)
            score_display('game_over')


        #floor
        floor_x_pos -= floor_speed * dt
        draw_floor()
        if floor_x_pos <= -536:
            floor_x_pos = 0

        pygame.display.update()
        #this limits the frame rate, no more than 120 fps - dt already calculated above
        await asyncio.sleep(0)  # Allow other tasks to run
    #game loop

asyncio.run(main())