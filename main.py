import pygame
import sys

GRAVITY = 1

pygame.init()
screen = pygame.display.set_mode((800,400))
clock = pygame.time.Clock()
game_over = True

title_font = pygame.font.Font('font/Pixeltype.ttf', 50)
title_surf = title_font.render('My Game', False, 'Black')
title_rect = title_surf.get_rect(center=(400, 50))

sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

player_surf = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom=(80, 300))
player_speed = 0

snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surf.get_rect(midbottom=(720, 300))

def setup():
    player_rect.midbottom = (80,300)
    snail_rect.midbottom = (720,300)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if game_over: 
                setup()
                game_over = False
            elif event.key == pygame.K_SPACE and player_rect.bottom == 300:
                player_speed = -20

    if game_over:
        screen.fill('Yellow')
    else:
        screen.blit(sky_surf, (0,0))
        screen.blit(ground_surf, (0,300))

        pygame.draw.rect(screen, 'Cyan', title_rect)
        screen.blit(title_surf, title_rect)

        snail_rect.left -= 4
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