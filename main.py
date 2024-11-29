import pygame
import sys


def display_score():
    curr_time = pygame.time.get_ticks()
    score = (curr_time - start_time) // 1000
    score_surf = font.render(f'Score: {score}', False, 'Black')
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return score


def setup():
    global start_time
    player_rect.midbottom = (80,300)
    snail_rect.midbottom = (720,300)
    start_time = pygame.time.get_ticks()


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

player_surf = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom=(80, 300))
player_speed = 0

snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surf.get_rect(midbottom=(720, 300))

player_stand_surf = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
#player_stand_surf = pygame.transform.scale(player_stand_surf, (120,144)) -> Free width, height selection
#player_stand_surf = pygame.transform.scale2x(player_stand_surf) -> Scaling by twice the size only
player_stand_surf = pygame.transform.rotozoom(player_stand_surf, 0, 2) # -> Scaling by a free factor and rotation of 0 deg.
player_stand_rect = player_stand_surf.get_rect(center=(400,200))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            if game_over: 
                setup()
                game_over = False
            elif event.key == pygame.K_SPACE and player_rect.bottom == 300:
                player_speed = -20

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

        snail_rect.left -= 7
        if snail_rect.right <= 0: snail_rect.left = 800
        screen.blit(snail_surf, snail_rect)

        player_speed += GRAVITY
        player_rect.bottom += player_speed
        if player_rect.bottom > 300:
            player_rect.bottom = 300
            player_speed = 0
        screen.blit(player_surf, player_rect)

        if player_rect.colliderect(snail_rect):
            game_over = True

    pygame.display.update()
    clock.tick(60)