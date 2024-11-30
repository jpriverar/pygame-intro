import pygame
import sys
from random import randint
from player import Player
from obstacle import *


def display_score():
    curr_time = pygame.time.get_ticks()
    score = (curr_time - start_time) // 1000
    score_surf = font.render(f'Score: {score}', False, 'Black')
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return score


def check_collisions():
    return pygame.sprite.spritecollide(player, obstacle_group, False)


pygame.init()
screen = pygame.display.set_mode((800,400))
clock = pygame.time.Clock()
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.1)
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

player = Player()
player_group = pygame.sprite.GroupSingle()
player_group.add(player)

obstacle_group = pygame.sprite.Group()

player_stand_surf = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
#player_stand_surf = pygame.transform.scale(player_stand_surf, (120,144)) -> Free width, height selection
#player_stand_surf = pygame.transform.scale2x(player_stand_surf) -> Scaling by twice the size only
player_stand_surf = pygame.transform.rotozoom(player_stand_surf, 0, 2) # -> Scaling by a free factor and rotation of 0 deg.
player_stand_rect = player_stand_surf.get_rect(center=(400,200))

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1000)

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
                player.reset()
                obstacle_group.empty()
                game_over = False
                bg_music.play(loops=-1)
                start_time = pygame.time.get_ticks()
        else:
            if event.type == obstacle_timer:
                if randint(0,1):
                    obstacle = Obstacle(ObstacleType.SNAIL)
                else:
                    obstacle = Obstacle(ObstacleType.FLY)
                obstacle_group.add(obstacle)

    if game_over:
        bg_music.stop()
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

        obstacle_group.update()
        obstacle_group.draw(screen)

        player_group.update()
        player_group.draw(screen)

        game_over = check_collisions()

    pygame.display.update()
    clock.tick(60)