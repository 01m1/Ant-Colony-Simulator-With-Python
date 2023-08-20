# Ant Script
import pygame
import pygame.gfxdraw
from math import hypot
from random import randint, uniform

vector = pygame.math.Vector2


class TheAnt(pygame.sprite.Sprite):
    def __init__(self, start_position, home_coords, ant_group, wn_width, wn_height, screen, max_speed, seek_force,
                 ant_size):
        super().__init__()
        self.__dist = 0  # distance between wall and ant.
        self._screen = screen
        self.__group = ant_group
        pygame.sprite.Sprite.__init__(self, self.__group)
        self.__max_speed = max_speed
        self.__seek_force = seek_force
        self._position = start_position  # Where ant spawns
        self.__home = home_coords  # Save home coordinates

        self.__ant_size = ant_size
        self._default_image_path = "images/ant.png"
        self.image = pygame.image.load(self._default_image_path).convert_alpha()  # Loading image of ant
        self.image = pygame.transform.scale(self.image, self.__ant_size)  # Shrinking size of ant image
        self._original_image = self.image
        self.__holding_food = False
        self.__wn_width = wn_width
        self.__wn_height = wn_height

        self.__wander_mode = 0

        self.rect = self.image.get_rect()  # Save image for later
        self.__velocity = vector(self.__max_speed, 0).rotate(
            uniform(0, 360))  # How many pixels ant will move every frame, starts facing right then rotates randomly 360
        self.__acceleration = vector(0, 0)  # How much velocity changes each frame
        self.rect.center = self._position
        self.__target = (randint(0, self.__wn_width), randint(0, self.__wn_height))
        self.__desired = vector(0, 0)
        self.__wander_ring_distance = 200  # Distance away from randomly generated target (circle) that ant should
        # wander towards
        self.__wander_ring_radius = 50  # Radius of circle (target)
        self.__vision_ring_radius = 50  # Radius of ant vision circle
        self.__vision_ring_distance = 15  # Distance away vision is from ant
        self.__displacement = []
        self.__bounce = False
        self.__bounces = 0

        self.__vision_center = self._position + self.__velocity.normalize() * self.__vision_ring_distance
        self.__vision_circle = pygame.draw.circle(screen, (155, 0, 155), (int(self.__vision_center.x),
                                                                          int(self.__vision_center.y)),
                                                  self.__vision_ring_radius,
                                                  width=1)
        self.__wall_detect_circle = pygame.draw.circle(screen, (155, 0, 155),
                                                       (int(self.__vision_center.x), int(self.__vision_center.y)),
                                                       1,
                                                       width=1)

        self.__angle_turn = 0  # Used by pygame to determine how much the image of the ant should rotate by.
        self.__flee_radius = 50  # Radius of circle around wall which determines when ant can switch back to original
        # state once it has left the circle

    def flee(self, target):  # Code for ant avoiding wall
        steer = vector(0, 0)
        self.__desired = vector(0, 0)
        self.__dist = self._position - target
        if self.__dist.length() < self.__flee_radius:
            self.__desired = self.__dist.normalize() * self.__max_speed
            steer = self.__desired - self.__velocity
            if steer.length() > self.__seek_force:
                steer.scale_to_length(self.__seek_force)
        else:
            if self.__holding_food:
                self.__bounce = True  # When ant hits wall it bounces off it to help with getting around wall.
                self.set_mode(2)
            else:
                self.set_mode(0)
        return steer

    def seek(self):
        # Move towards target, movement looks natural
        self.__desired = (self.__target - self._position).normalize() * self.__max_speed
        steer = (self.__desired - self.__velocity)
        if steer.length() > self.__seek_force:
            steer.scale_to_length(self.__seek_force)
        return steer

    def wander(self, item):  # Go towards item
        if (self._position[0] > self.__wn_width) or (self._position[0] < 0) \
                or (self._position[1] > self.__wn_height) \
                or (self._position[1] < 0):
            # Prevent ant going off-screen
            self.__target = vector(randint(0, self.__wn_width), randint(0, self.__wn_height))
            return self.seek()
        else:
            if self.__wander_mode == 0:  # Mode for randomly moving
                circle_position = self._position + self.__velocity.normalize() * self.__wander_ring_distance
                self.__target = circle_position + vector(self.__wander_ring_radius, 0).rotate(uniform(0, 360))
                self.__displacement = self.__target
                return self.seek()
            if self.__wander_mode == 1:  # Mode for moving towards food once in ant vision.
                self.__target = item
            if self.__wander_mode == 3:
                self.__target = item
            if self.__wander_mode == 5:
                self.__target = item

    def stop(self):
        self.__velocity.scale_to_length(1)

    def bounce_off(self):
        self.__velocity = -self.__velocity

    def distance_from_home(self):
        return abs(hypot((self._position[0] - self.__home[0]), (self._position[1] - self.__home[1])))

    def get_ant_rect(self):  # Used for collision detection
        return self.rect

    def update(self):
        self.__angle_turn = self.__velocity.normalize().angle_to(pygame.Vector2(1, 0))
        self.image = pygame.transform.rotate(self._original_image,
                                             self.__angle_turn)

        if self.__wander_mode == 0:  # Wandering around randomly
            self.__holding_food = False
            self.__bounces = 0

            self.__acceleration = self.wander(None)

            self.__velocity += self.__acceleration

            if self.__velocity.length() > self.__max_speed:
                self.__velocity.scale_to_length(self.__max_speed)  # If velocity exceeds max speed then cap the speed
            self._position += self.__velocity  # Update position

        if self.__wander_mode == 1:  # Go to food once spotted.
            if self.rect.collidepoint(self.__target):
                self.set_mode(0)  # If an ant is approaching food and the food gets destroyed then reset to mode 0.
            self.__acceleration = self.seek()
            self.__velocity += self.__acceleration
            if self.__velocity.length() > self.__max_speed:
                self.__velocity.scale_to_length(self.__max_speed)  # If velocity exceeds max speed then cap the speed
            self._position += self.__velocity

        if self.__wander_mode == 2:  # Going home

            self.__holding_food = True
            bouncer = 1
            if self.__bounce:
                self.__bounces += 1
                if self.__bounces < 1000:
                    bouncer = self.__bounces * 10
                else:
                    self.__bounces = 0
                new_circle_position = self.__home + self.__velocity.normalize() * bouncer  # the addition of a
                # velocity is useful for when ant is struggling to get past a wall on the way back home
            else:
                new_circle_position = self.__home
            self.__target = new_circle_position + vector(60, 10).rotate(uniform(0, 360))  # the addition of the
            # vector makes the ant aim for different parts of the home circle for realistic movement
            # will make the ant move around a bit when it is attempting to go home.
            self.__acceleration = self.seek()
            self.__velocity += self.__acceleration
            if self.__velocity.length() > self.__max_speed:
                self.__velocity.scale_to_length(self.__max_speed)  # If velocity exceeds max speed then cap the speed
            self._position += self.__velocity

        if self.__wander_mode == 3:  # Follow Pheromone
            self.__bounces = 0
            self.__acceleration = self.seek()
            self.__velocity += self.__acceleration
            if self.__velocity.length() > self.__max_speed:
                self.__velocity.scale_to_length(self.__max_speed)  # If velocity exceeds max speed then cap the speed
            self._position += self.__velocity

        if self.__wander_mode == 5:  # Ant avoiding wall
            if self.rect.collidepoint(self.__target):
                self.set_mode(0)
            self.__acceleration = self.flee(self.__target)
            self.__velocity += self.__acceleration
            if self.__velocity.length() > 1.5:
                self.__velocity.scale_to_length(1.5)
            self._position += self.__velocity

        self.rect.center = self._position

        vision_center = self._position + self.__velocity.normalize() * self.__vision_ring_distance
        self.__vision_circle = pygame.draw.circle(self._screen, (155, 0, 155), (int(vision_center.x),
                                                                                int(vision_center.y)),
                                                  self.__vision_ring_radius,
                                                  width=1)
        self.__wall_detect_circle = pygame.draw.circle(self._screen, (155, 0, 155),
                                                       (int(vision_center.x), int(vision_center.y)),
                                                       1,
                                                       width=1)

    def get_mode(self):
        return self.__wander_mode

    def get_holding_food(self):
        return self.__holding_food

    def get_vision_center(self):
        return self.__vision_circle.center

    def set_holding(self, mode):
        self.__holding_food = mode

    def set_mode(self, mode):
        self.__wander_mode = mode

    def vision_circle_collide(self, item):
        return self.__vision_circle.colliderect(item)

    def wall_circle_collide(self, item):
        return self.__wall_detect_circle.colliderect(item)

    def draw_vectors(self):
        # Draw Vectors
        if (self.__displacement[0] < self.__wn_width) and (self.__displacement[0] > 0) and \
                (self.__displacement[1] < self.__wn_height) and (self.__displacement[1] > 0):
            if self.__wander_mode == 0:
                center = self._position + self.__velocity.normalize() * self.__wander_ring_distance
                pygame.draw.circle(self._screen, (155, 0, 155), (int(center.x), int(center.y)),
                                   self.__wander_ring_radius,
                                   width=1)
                pygame.draw.line(self._screen, (255, 255, 0), center, self.__displacement, 5)
                # Show Ant's target position

    def draw_vision(self):
        # Draw Vision
        vision_center = self._position + self.__velocity.normalize() * self.__vision_ring_distance
        self.__vision_circle = pygame.draw.circle(self._screen, (155, 0, 155), (int(vision_center.x),
                                                                                int(vision_center.y)),
                                                  self.__vision_ring_radius, width=1)
        self.__wall_detect_circle = pygame.draw.circle(self._screen, (155, 0, 255),
                                                       (int(vision_center.x), int(vision_center.y)),
                                                       1,
                                                       width=1)


# Queen Ant Class

class QueenAnt(TheAnt):
    def __init__(self, start_position, home_coords, ant_group, wn_width, wn_height, screen, max_speed, seek_force,
                 ant_size):
        super().__init__(start_position, home_coords, ant_group, wn_width, wn_height, screen, max_speed, seek_force,
                         ant_size)
        self._default_image_path = "images/queen_ant.png"
        self.image = pygame.image.load(self._default_image_path).convert_alpha()  # Loading image of ant
        self.image = pygame.transform.scale(self.image, ant_size)  # Shrinking size of ant image
        self._original_image = self.image

    def flee(self, target):  # Overriding the flee method to allow queen to fly over wall.
        self.set_mode(0)
        return self.wander(None)

    def get_position(self):
        return self._position

    def draw_circle(self):
        pygame.draw.circle(self._screen, (50, 0, 200),
                           (int(self._position[0]), int(self._position[1])),
                           10,
                           width=1)
