# Home Script
import pygame


class Home(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.__position = position
        self.image = pygame.Surface((100, 100))
        self.__original_image = self.image
        self.image.fill(0)
        self.image.set_colorkey(0)
        self.__radius = 50
        #  Draw home
        pygame.draw.circle(self.image, (225, 198, 153), (50, 50), self.__radius)
        self.rect = self.image.get_rect()
        self.rect.center = self.__position

    def get_position(self):
        return self.__position

    def get_radius(self):
        return self.__radius

    def get_the_rect(self):
        return self.rect
