import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.GRAVITY = 1

        self.__jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.__jump_sound.set_volume(0.2)
        
        self.__jump_surf = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
        self.__walk_surf = [pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha(),
                       pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()]
        self.__walk_surf_index = 0

        self.image = self.__walk_surf[self.__walk_surf_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.speed = 0

    '''
    The player should be able to jump when the space bar is pressed, as long as the player
    is touching the ground, so no double jumps.
    '''
    def process_input(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.speed = -20
            self.__jump_sound.play()


    def apply_gravity(self) -> None:
        self.speed += self.GRAVITY
        self.rect.bottom += self.speed
        if self.rect.bottom > 300:
            self.rect.bottom = 300
            self.speed = 0


    def animate(self) -> None:
        if self.rect.bottom >= 300:
            #player_walk_index ^= 1
            self.__walk_surf_index += 0.1
            if self.__walk_surf_index > len(self.__walk_surf): 
                self.__walk_surf_index = 0
            self.image = self.__walk_surf[int(self.__walk_surf_index)]
        else:
            self.image = self.__jump_surf

    # Method override
    def update(self) -> None:
        self.apply_gravity()
        self.process_input()
        self.animate()

    
    def reset(self) -> None:
        self.rect.midbottom=(80, 300)
        self.speed = 0