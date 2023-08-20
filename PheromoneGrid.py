# Pheromone Grid Script
import sys

import pygame
import pygame.gfxdraw
from numpy import zeros
from random import choices

clock = pygame.time.Clock()  # Used for evaporating pheromone over time
vec = pygame.Vector2


#  Grid system for drawing pheromone on screen

class pheromoneGrid:
    def __init__(self, width, height, screen, show_pheromone):
        self.__tileSize = 5
        self.__gridWidth = width
        self.__gridHeight = height
        self.__screen = screen
        # Grid Matrix
        self.__grid_matrix = zeros((int(self.__gridHeight / self.__tileSize),
                                    int(self.__gridWidth / self.__tileSize)))
        self.__wall_list = []
        self.__show_pheromone = show_pheromone

    def get_tile_size(self):
        return self.__tileSize

    def draw_grid(self):
        # Draw grid onto screen if option chosen
        for x in range(0, self.__gridWidth, self.__tileSize):
            pygame.gfxdraw.line(self.__screen, x, 0, x, self.__gridHeight, (128, 128, 128, 25))
        for y in range(0, self.__gridHeight, self.__tileSize):
            pygame.gfxdraw.line(self.__screen, 0, y, self.__gridWidth, y, (128, 128, 128, 25))

    def pheromone_add(self, row, row_coords):
        # Adding pheromone to grid
        try:
            self.__grid_matrix[row_coords[0], row_coords[1]] = row[0]
        except IndexError:  # Attempts to draw outside grid
            pass
        if self.__grid_matrix[row_coords[0], row_coords[1]] > 254:
            self.__grid_matrix[row_coords[0], row_coords[1]] = 255  # Cap Pheromone Strength

        if self.__show_pheromone:
            # Pheromone strength
            grid_colour = (144, 238, 144, self.__grid_matrix[row_coords[0], row_coords[1]])
        else:
            grid_colour = (0, 0, 0, 0)
        pygame.gfxdraw.box(self.__screen, ((5 * int(row_coords[1])),
                                           (5 * int(row_coords[0])), self.__tileSize, self.__tileSize),
                           grid_colour)
        return self.__grid_matrix[row_coords[0], row_coords[1]]

    def get_pheromone_strength(self, coord_x, coord_y):
        try:
            if self.__grid_matrix[coord_x][coord_y] > 1:
                return self.__grid_matrix[coord_x][coord_y]
        except IndexError:  # Outside screen
            pass

    def collide_item(self, center):
        # Code for when ant checks for pheromone.
        grid_center0 = int((self.__tileSize * round(center[0] / self.__tileSize) / self.__tileSize))
        grid_center1 = int((self.__tileSize * round(center[1] / self.__tileSize)) / self.__tileSize)
        sub_matrix = self.__grid_matrix[grid_center1 - 3:grid_center1 + 4, grid_center0 - 3:grid_center0 + 4]
        value_dict = {}
        for y_index, row in enumerate(sub_matrix):
            for x_index, value in enumerate(row):
                if value > 0:  # only add values that are not 0 (no pheromone) or below 0 (wall)
                    value_dict[(y_index, x_index)] = value

        if len(value_dict) > 0:
            probabilities = list(value_dict.values())
            path = choices(list(value_dict.items()), weights=probabilities)
            y_index = path[0][0][0] - 3
            x_index = path[0][0][1] - 3
            grid_center1 += y_index
            grid_center0 += x_index
            return grid_center0 * self.__tileSize, grid_center1 * self.__tileSize

    def add_wall(self, centre):
        # Add wall onto grid
        top_left = (centre[0]-4, centre[1]-4)
        if (top_left[0], top_left[1]) in self.__wall_list:
            pass
        else:
            for i in range(0, 5):
                for x in range(0, 5):
                    try:
                        # Create a 9x9 wall
                        self.__grid_matrix[centre[1] + x, centre[0] + i] = -100
                        self.__grid_matrix[centre[1] + x, centre[0] - i] = -100
                        self.__grid_matrix[centre[1] - x, centre[0] + i] = -100
                        self.__grid_matrix[centre[1] - x, centre[0] - i] = -100
                    except IndexError:  # User attempts to draw outside of grid.
                        pass

            self.__wall_list.append((top_left[0], top_left[1]))

    def remove_wall(self, coords):
        # Remove wall from grid

        if self.__grid_matrix[coords[1], coords[0]] == -100:
            for wall in self.__wall_list:
                if abs(coords[0] - (wall[0]+4)) <= 4:
                    if abs(coords[1] - (wall[1]+4)) <= 4:
                        self.__wall_list.pop(self.__wall_list.index(wall))
                        break

    def draw_walls(self):
        for wall in self.__wall_list:
            pygame.draw.rect(self.__screen, (194, 197, 204), ((self.__tileSize * int(wall[0])),
                                                              (self.__tileSize * int(wall[1])),
                                                              self.__tileSize * 9,
                                                              self.__tileSize * 9)
                             )

    def get_wall_list(self):
        return self.__wall_list
