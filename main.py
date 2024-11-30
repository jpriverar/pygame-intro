import pygame
import sys
from random import randint


def display_score():
    curr_time = pygame.time.get_ticks()
    score = (curr_time - start_time) // 1000
    score_surf = font.render(f'Score: {score}', False, 'Black')
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return score


def move_obstacles(obstacle_rects):
    for rect, type in obstacle_rects:
        rect.x -= 7
        if type == 'snail':
            screen.blit(snail_surf, rect)
        elif type == 'fly':
            screen.blit(fly_surf, rect)

    obstacle_rects = [(rect, type) for rect, type in obstacle_rects if rect.right > 0]
    return obstacle_rects


def check_collisions(player, obstacles):
    for rect, _ in obstacle_rects:
        if player.colliderect(rect):
            return True
    return False


def player_animation():
    global player_walk_index, player_surf
    if player_rect.bottom >= 300:
        #player_walk_index ^= 1
        player_walk_index += 0.1
        if player_walk_index > len(player_walk): player_walk_index = 0
        player_surf = player_walk[int(player_walk_index)]
    else:
        player_surf = player_jump


GRAVITY = 1
pygame.init()
screen = pygame.display.set_mode((800,400))
clock = pygame.time.Clock()
game_over = True
start_time = 0
score = None

font = pygame.font.Font('font/Pixeltype.ttf', 50)
title_surf = font.render('Pixel Runner', False, 'black')
title_rect = title_surf.get_rect(center=(400,50))
instructions_surf = font.render('Press any key to start', False, 'black')
instructions_rect = instructions_surf.get_rect(center=(400,350))

sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

player_jump = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_walk = [pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha(),
               pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()]
player_walk_index = 0
player_surf = player_walk[player_walk_index]
player_rect = player_surf.get_rect(midbottom=(80, 300))
player_speed = 0

snail_frames = [pygame.image.load('graphics/snail/snail1.png').convert_alpha(), 
                pygame.image.load('graphics/snail/snail2.png').convert_alpha()]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

fly_frames = [pygame.image.load('graphics/Fly/Fly1.png').convert_alpha(),
              pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

player_stand_surf = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
#player_stand_surf = pygame.transform.scale(player_stand_surf, (120,144)) -> Free width, height selection
#player_stand_surf = pygame.transform.scale2x(player_stand_surf) -> Scaling by twice the size only
player_stand_surf = pygame.transform.rotozoom(player_stand_surf, 0, 2) # -> Scaling by a free factor and rotation of 0 deg.
player_stand_rect = player_stand_surf.get_rect(center=(400,200))

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1000)

#player_animation_timer = pygame.USEREVENT + 2
#pygame.time.set_timer(player_animation_timer, 200)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        if game_over: 
            if event.type == pygame.KEYDOWN:
                player_rect.midbottom = (80, 300)
                obstacle_rects = []
                game_over = False
                start_time = pygame.time.get_ticks()
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                    player_speed = -20

            elif event.type == obstacle_timer:
                if randint(0,1):
                    obstacle_rects.append((snail_surf.get_rect(bottomleft=(randint(800,1100), 300)), 'snail'))
                else:
                    obstacle_rects.append((fly_surf.get_rect(bottomleft=(randint(800,1100), 150)), 'fly'))

            elif event.type == snail_animation_timer:
                snail_frame_index ^= 1
                snail_surf = snail_frames[snail_frame_index]

            elif event.type == fly_animation_timer:
                fly_frame_index ^= 1
                fly_surf = fly_frames[fly_frame_index]

    if game_over:
        screen.fill((94,129,162))
        screen.blit(title_surf, title_rect)
        screen.blit(player_stand_surf, player_stand_rect)
        if score is None:
            screen.blit(instructions_surf, instructions_rect)
        else:
            score_msg = font.render(f'Your score: {score}', False, 'black')
            score_msg_rect = score_msg.get_rect(center=(400, 350))
            screen.blit(score_msg, score_msg_rect)
        
    else:
        screen.blit(sky_surf, (0,0))
        screen.blit(ground_surf, (0,300))
        score = display_score()

        # snail_rect.left -= 7
        # if snail_rect.right <= 0: snail_rect.left = 800
        # screen.blit(snail_surf, snail_rect)
        obstacle_rects = move_obstacles(obstacle_rects)

        player_speed += GRAVITY
        player_rect.bottom += player_speed
        if player_rect.bottom > 300:
            player_rect.bottom = 300
            player_speed = 0
        player_animation()
        screen.blit(player_surf, player_rect)

        # if player_rect.colliderect(snail_rect):
        #     game_over = True
        game_over = check_collisions(player_rect, obstacle_rects)

    pygame.display.update()
    clock.tick(60)