# Pheromone Script
import pygame


class pheromone:
    def __init__(self, ant, grid, screen, ant_id, evaporation_rate):
        self.__tileSize = 5
        self.__pheromoneDict = {}  # Dictionary to hold all pheromone
        self.__clear_queue = []  # Queue of Pheromone that needs to be cleared as evaporated.
        self.__ant = ant  # Aggregation
        self.__grid = grid  # Aggregation
        self.__fixed_pheromone = True  # Fix strength of pheromone, so it is not constantly changing when ant moves.
        self.__pheromone_strength = 0
        self.__id = ant_id
        self.__screen = screen
        self.__evaporation_rate = evaporation_rate

    def reset(self):
        self.__fixed_pheromone = True

    def pheromone_update(self):

        if self.__fixed_pheromone and (self.__ant.get_mode() == 2) or (self.__ant.get_mode() == 6):
            self.__pheromone_strength = (1 / self.__ant.distance_from_home())*30000  # Get pheromone strength
            self.__fixed_pheromone = False
        if self.__ant.get_mode() == 2 or self.__ant.get_mode() == 6:
            self.ant_collision_with_cell(self.__ant.get_vision_center())

        for i in self.__pheromoneDict:
            if pygame.time.get_ticks() - self.__pheromoneDict[i][1] >= 7000:  # start evaporating after 7
                # seconds
                self.__pheromoneDict[i][0] -= self.__evaporation_rate * (1 / (self.__pheromone_strength / 500)) / 10
                # After some tweaking, I decided to use a different formula for evaporation other than the one
                # mentioned in my Analysis.

    def ant_collision_with_cell(self, ant_rect):
        try:
            if (int(ant_rect[1] / self.__tileSize), int(ant_rect[0] / self.__tileSize)) in self.__pheromoneDict:
                self.__pheromoneDict[int(ant_rect[1] / self.__tileSize), int(ant_rect[0] / self.__tileSize)][0] += \
                    self.__pheromone_strength
                self.__pheromoneDict[int(ant_rect[1] / self.__tileSize), int(ant_rect[0] / self.__tileSize)][1] = \
                    pygame.time.get_ticks()
            else:
                self.__pheromoneDict[int(ant_rect[1] / self.__tileSize), int(ant_rect[0] / self.__tileSize)] = \
                    [self.__pheromone_strength, pygame.time.get_ticks(), self.__id]
            #  Row, Column, Pheromone Strength, Time at pheromone drawn on screen, id
        except IndexError:
            pass

    def update_grid(self):
        for row in self.__pheromoneDict:

            try:
                if (row[1] < self.__screen.get_size()[0] / 5) and \
                        (row[0] < self.__screen.get_size()[1] / 5):
                    if self.__pheromoneDict[row][1] < 0:
                        self.enqueue(row)
                    else:
                        self.__grid.pheromone_add(self.__pheromoneDict[row], row)

            except TypeError:  # Pheromone already evaporated (prevents errors)
                self.__clear_queue.append(row)

        count = 0
        for i in self.__clear_queue:
            try:
                self.__pheromoneDict.pop(i)
                self.dequeue()
            except (KeyError, IndexError):  # Dictionary doesn't have item
                pass
            count += 1

    def enqueue(self, item):
        self.__clear_queue.append(item)

    def dequeue(self):
        self.__clear_queue.pop()
