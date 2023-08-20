# Food Script
import pygame


class Food(pygame.sprite.Sprite):
    def __init__(self, position, delete_food):
        super().__init__()
        self.__position = position
        self.__delete_food = delete_food
        self.image = pygame.Surface((10, 10))
        self.image.fill(0)
        self.image.set_colorkey(0)
        #  Draw food
        pygame.draw.circle(self.image, (0, 255, 0), (5, 5), 5)
        self.rect = self.image.get_rect(center=position)

    def pick(self):
        if self.__delete_food:
            self.kill()

    def destroy(self):
        self.kill()

    def get_food_rect(self):
        return self.rect

    def get_position(self):
        return self.__position
