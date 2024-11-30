import pygame
from enum import Enum
from random import randint


class ObstacleType(Enum):
    SNAIL = 1
    FLY = 2


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type: ObstacleType) -> None:
        super().__init__()

        if type == ObstacleType.SNAIL:
            self.__frames = [pygame.image.load('graphics/snail/snail1.png').convert_alpha(), 
                             pygame.image.load('graphics/snail/snail2.png').convert_alpha()]
            self.__y_pos = 300

        elif type == ObstacleType.FLY:
            self.__frames = [pygame.image.load('graphics/Fly/Fly1.png').convert_alpha(),
                             pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()]
            self.__y_pos = 150

        self.__frame_index = 0
        self.image = self.__frames[self.__frame_index]
        self.rect = self.image.get_rect(midbottom=(randint(800, 1100), self.__y_pos))


    def animate(self) -> None:
        self.__frame_index += 0.1
        if self.__frame_index >= len(self.__frames):
            self.__frame_index = 0
        self.image = self.__frames[int(self.__frame_index)]

    
    # Method override
    def update(self) -> None:
        self.animate()
        self.rect.x -= 5
        if self.rect.right < 0:
            self.kill()