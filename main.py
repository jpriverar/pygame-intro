import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((800,400))
clock = pygame.time.Clock()

title_font = pygame.font.Font('font/Pixeltype.ttf', 50)
title_surf = title_font.render('My Game', False, 'Black')
title_rect = title_surf.get_rect(midtop=(400, 50))

sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

player_surf = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom=(80, 300))

snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surf.get_rect(midbottom=(720, 300))

GRAVITY = 1

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pass

    screen.blit(sky_surf, (0,0))
    screen.blit(ground_surf, (0,300))
    screen.blit(title_surf, title_rect)

    snail_rect.left -= 4
    if snail_rect.right <= 0: snail_rect.left = 800
    screen.blit(snail_surf, snail_rect)

    screen.blit(player_surf, player_rect)

    pygame.display.update()
    clock.tick(60)