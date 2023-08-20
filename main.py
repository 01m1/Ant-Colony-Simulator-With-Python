# main script


import pygame
from pygame.locals import *
from sys import exit
import Food
import Home
import Ant
import Pheromone
import PheromoneGrid
from tkinter.filedialog import askopenfilename

# Importing Other Scripts

# Setting up window

wn_width = 1500
wn_height = 900
FPS = 60

pygame.init()
screen = pygame.display.set_mode((wn_width, wn_height))
font = pygame.font.SysFont(None, 60)
clock = pygame.time.Clock()

# Default Settings
options = {
    "ant_count": 52,
    "evaporation_rate": 0.5,
    "max_speed": 4,
    "seek_force": 0.2,
    "show_pheromone": True,
    "draw_grid": True,
    "ant_size": 5,
    "dark_mode": False
}


# Function for drawing text onto screen
def draw_text(text, the_font, colour, surface, x, y):
    textobj = the_font.render(text, 1, colour)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def main_menu():
    while True:
        screen.fill((0, 0, 0))
        draw_text('Ant Colony Simulator', font, (255, 255, 255), screen, 565, 200)

        # Store mouse position.
        mx, my = pygame.mouse.get_pos()

        # Start Button
        start = pygame.image.load('images/START.png')
        start = pygame.transform.scale(start, (300, 150))
        start_rect = start.get_rect()
        start_rect.center = (780, 450)

        # Settings Button
        settings = pygame.image.load('images/SETTINGS.png')
        settings = pygame.transform.scale(settings, (200, 100))
        settings_rect = settings.get_rect()
        settings_rect.center = (785, 600)

        screen.blit(start, start_rect)
        screen.blit(settings, settings_rect)

        # Hover over button pop out effect
        if start_rect.collidepoint((mx, my)):
            start = pygame.transform.scale(start, (335, 175))
            start_rect.center = (765, 440)
            screen.blit(start, start_rect)

        if settings_rect.collidepoint((mx, my)):
            settings = pygame.transform.scale(settings, (235, 125))
            settings_rect.center = (770, 590)
            screen.blit(settings, settings_rect)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    # If Start button clicked then start the main code
                    if start_rect.collidepoint((mx, my)):
                        main(options["ant_count"], options["evaporation_rate"], options["max_speed"],
                             options["seek_force"], options["show_pheromone"], options["draw_grid"],
                             options["ant_size"], options["dark_mode"])
                    # If Settings button clicked then start the settings code
                    if settings_rect.collidepoint((mx, my)):
                        settings_run()

        pygame.display.update()
        clock.tick()


# Code for settings screen
def settings_run():
    # Putting in default settings.
    ant_count = options["ant_count"]
    evaporation_rate = options["evaporation_rate"]
    max_speed = options["max_speed"]
    seek_force = options["seek_force"]
    show_pheromone = options["show_pheromone"]
    draw_grid = options["draw_grid"]
    ant_size = options["ant_size"]
    dark_mode = options["dark_mode"]
    settings = True
    saved = False

    while settings:

        # All images with '_GREYED.png' at the end are used when you have reached a
        # maximum/minimum number of that setting.
        if ant_count == 1:
            minus_path = 'images/MINUS_GREYED.png'
        else:
            minus_path = 'images/MINUS.png'

        add_path = 'images/ADD.png'

        if evaporation_rate == 0.9:
            evap_add_path = 'images/ADD_GREYED.png'
        else:
            evap_add_path = 'images/ADD.png'
        if evaporation_rate == 0.1:
            evap_remove_path = 'images/MINUS_GREYED.png'
        else:
            evap_remove_path = 'images/MINUS.png'

        if max_speed == 5:
            max_speed_path = 'images/ADD_GREYED.png'
        else:
            max_speed_path = 'images/ADD.png'
        if max_speed == 1:
            max_speed_path_r = 'images/MINUS_GREYED.png'
        else:
            max_speed_path_r = 'images/MINUS.png'

        if seek_force == 0.5:
            seek_force_path = 'images/ADD_GREYED.png'
        else:
            seek_force_path = 'images/ADD.png'
        if seek_force == 0.1:
            seek_force_path_r = 'images/MINUS_GREYED.png'
        else:
            seek_force_path_r = 'images/MINUS.png'

        if ant_size == 6:
            ant_size_path = 'images/ADD_GREYED.png'
        else:
            ant_size_path = 'images/ADD.png'
        if ant_size == 1:
            ant_size_path_r = 'images/MINUS_GREYED.png'
        else:
            ant_size_path_r = 'images/MINUS.png'

        if show_pheromone:
            pheromone_path = 'images/TRUE.png'
        else:
            pheromone_path = 'images/FALSE.png'

        if draw_grid:
            grid_path = 'images/TRUE.png'
        else:
            grid_path = 'images/FALSE.png'

        if dark_mode:
            mode_path = 'images/TRUE.png'
        else:
            mode_path = 'images/FALSE.png'

        screen.fill((0, 0, 0))
        mx, my = pygame.mouse.get_pos()

        # Drawing everything onto screen.
        draw_text('Ants:', font, (255, 255, 255), screen, 620, 130)
        draw_text(str(ant_count), font, (255, 255, 255), screen, 810, 130)
        add_ant = pygame.image.load(add_path)
        add_ant = pygame.transform.scale(add_ant, (30, 30))
        add_ant_rect = add_ant.get_rect()
        add_ant_rect.center = (910, 130)
        add_50_ant = pygame.transform.scale(add_ant, (70, 70))
        add_50_ant_rect = add_50_ant.get_rect()
        add_50_ant_rect.center = (960, 115)
        remove_ant = pygame.image.load(minus_path)
        remove_ant = pygame.transform.scale(remove_ant, (30, 30))
        remove_ant_rect = remove_ant.get_rect()
        remove_ant_rect.center = (910, 170)
        if ant_count <= 50:
            remove_50_ant = pygame.transform.scale(pygame.image.load('images/MINUS_GREYED.png'), (70, 70))
        else:
            remove_50_ant = pygame.transform.scale(remove_ant, (70, 70))
        remove_50_ant_rect = remove_50_ant.get_rect()
        remove_50_ant_rect.center = (960, 180)
        screen.blit(add_ant, add_ant_rect)
        screen.blit(add_50_ant, add_50_ant_rect)
        screen.blit(remove_ant, remove_ant_rect)
        screen.blit(remove_50_ant, remove_50_ant_rect)

        draw_text('Pheromone Evaporation Rate:', font, (255, 255, 255), screen, 132, 230)
        draw_text(str(evaporation_rate), font, (255, 255, 255), screen, 820, 230)
        add_evap = pygame.image.load(evap_add_path)
        add_evap = pygame.transform.scale(add_evap, (30, 30))
        add_evap_rect = add_evap.get_rect()
        add_evap_rect.center = (910, 230)
        remove_evap = pygame.image.load(evap_remove_path)
        remove_evap = pygame.transform.scale(remove_evap, (30, 30))
        remove_evap_rect = remove_evap.get_rect()
        remove_evap_rect.center = (910, 270)
        screen.blit(add_evap, add_evap_rect)
        screen.blit(remove_evap, remove_evap_rect)

        draw_text('Ant Max Speed:', font, (255, 255, 255), screen, 410, 330)
        draw_text(str(max_speed), font, (255, 255, 255), screen, 850, 330)
        add_speed = pygame.image.load(max_speed_path)
        add_speed = pygame.transform.scale(add_speed, (30, 30))
        add_speed_rect = add_speed.get_rect()
        add_speed_rect.center = (910, 330)
        remove_speed = pygame.image.load(max_speed_path_r)
        remove_speed = pygame.transform.scale(remove_speed, (30, 30))
        remove_speed_rect = remove_speed.get_rect()
        remove_speed_rect.center = (910, 370)
        screen.blit(add_speed, add_speed_rect)
        screen.blit(remove_speed, remove_speed_rect)

        draw_text('Ant Seek Force:', font, (255, 255, 255), screen, 410, 430)
        draw_text(str(seek_force), font, (255, 255, 255), screen, 820, 430)
        add_seek = pygame.image.load(seek_force_path)
        add_seek = pygame.transform.scale(add_seek, (30, 30))
        add_seek_rect = add_seek.get_rect()
        add_seek_rect.center = (910, 430)
        remove_seek = pygame.image.load(seek_force_path_r)
        remove_seek = pygame.transform.scale(remove_seek, (30, 30))
        remove_seek_rect = remove_seek.get_rect()
        remove_seek_rect.center = (910, 470)
        screen.blit(add_seek, add_seek_rect)
        screen.blit(remove_seek, remove_seek_rect)

        draw_text('Show Pheromone:', font, (255, 255, 255), screen, 365, 530)
        phero_option = pygame.image.load(pheromone_path)
        phero_option = pygame.transform.scale(phero_option, (100, 50))
        phero_option_rect = phero_option.get_rect()
        phero_option_rect.center = (880, 550)
        screen.blit(phero_option, phero_option_rect)

        draw_text('Draw Grid:', font, (255, 255, 255), screen, 520, 630)
        grid_option = pygame.image.load(grid_path)
        grid_option = pygame.transform.scale(grid_option, (100, 50))
        grid_option_rect = grid_option.get_rect()
        grid_option_rect.center = (880, 650)
        screen.blit(grid_option, grid_option_rect)

        draw_text('Ant Size:', font, (255, 255, 255), screen, 540, 730)
        draw_text(str(ant_size), font, (255, 255, 255), screen, 850, 730)
        add_size = pygame.image.load(ant_size_path)
        add_size = pygame.transform.scale(add_size, (30, 30))
        add_size_rect = add_size.get_rect()
        add_size_rect.center = (910, 730)
        remove_size = pygame.image.load(ant_size_path_r)
        remove_size = pygame.transform.scale(remove_size, (30, 30))
        remove_size_rect = remove_size.get_rect()
        remove_size_rect.center = (910, 770)
        screen.blit(add_size, add_size_rect)
        screen.blit(remove_size, remove_size_rect)

        back_button = pygame.image.load('images/BACK.png')
        back_button = pygame.transform.scale(back_button, (100, 50))
        back_button_rec = back_button.get_rect()
        back_button_rec.center = (60, 40)
        screen.blit(back_button, back_button_rec)

        export_option = pygame.image.load('images/export.png')
        export_option = pygame.transform.scale(export_option, (100, 50))
        export_option_rect = export_option.get_rect()
        export_option_rect.center = (1325, 40)
        screen.blit(export_option, export_option_rect)
        if saved:
            draw_text('Settings Saved', pygame.font.SysFont(None, 15), (255, 255, 255), screen, 1290, 70)

        import_option = pygame.image.load('images/import.png')
        import_option = pygame.transform.scale(import_option, (100, 50))
        import_option_rect = import_option.get_rect()
        import_option_rect.center = (1440, 40)
        screen.blit(import_option, import_option_rect)

        draw_text('Dark Mode:', font, (255, 255, 255), screen, 495, 830)
        mode_button = pygame.image.load(mode_path)
        mode_button = pygame.transform.scale(mode_button, (100, 50))
        mode_button_rect = mode_button.get_rect()
        mode_button_rect.center = (880, 850)
        screen.blit(mode_button, mode_button_rect)

        for event in pygame.event.get():
            # Checking if button pressed
            if pygame.mouse.get_pressed()[0]:

                if export_option_rect.collidepoint((mx, my)):
                    saved = True
                    file = open("ant_colony_settings.txt", "w")
                    settings_list = [options["ant_count"], options["evaporation_rate"], options["max_speed"],
                                     options["seek_force"], options["show_pheromone"], options["draw_grid"],
                                     options["ant_size"], options["dark_mode"]]
                    for line in settings_list:
                        file.write(str(line) + "\n")
                    file.close()

                if import_option_rect.collidepoint((mx, my)):
                    file = open("ant_colony_settings.txt", "r")
                    settings_list = []
                    for line in file:
                        x = line.replace("\n", "")
                        settings_list.append(x)

                    ant_count = int(settings_list[0])
                    evaporation_rate = float(settings_list[1])
                    max_speed = int(settings_list[2])
                    seek_force = float(settings_list[3])

                    if settings_list[4] == 'False':
                        show_pheromone = False
                    else:
                        show_pheromone = True

                    if settings_list[5] == 'False':
                        draw_grid = False
                    else:
                        draw_grid = True

                    ant_size = int(settings_list[6])

                    if settings_list[7] == 'False':
                        dark_mode = False
                    else:
                        dark_mode = True

                if add_ant_rect.collidepoint((mx, my)):
                    ant_count += 1
                if add_50_ant_rect.collidepoint((mx, my)):
                    ant_count += 50
                if remove_ant_rect.collidepoint((mx, my)):
                    if ant_count > 1:
                        ant_count -= 1
                if remove_50_ant_rect.collidepoint((mx, my)):
                    if ant_count > 50:
                        ant_count -= 50

                if add_evap_rect.collidepoint((mx, my)):
                    if evaporation_rate < 0.9:
                        evaporation_rate += 0.1
                if remove_evap_rect.collidepoint((mx, my)):
                    if evaporation_rate > 0.1:
                        evaporation_rate -= 0.1

                if add_speed_rect.collidepoint((mx, my)):
                    if max_speed < 5:
                        max_speed += 1
                if remove_speed_rect.collidepoint((mx, my)):
                    if max_speed > 1:
                        max_speed -= 1

                if add_seek_rect.collidepoint((mx, my)):
                    if seek_force < 0.5:
                        seek_force += 0.1
                if remove_seek_rect.collidepoint((mx, my)):
                    if seek_force > 0.1:
                        seek_force -= 0.1

                if add_size_rect.collidepoint((mx, my)):
                    if ant_size < 6:
                        ant_size += 1
                if remove_size_rect.collidepoint((mx, my)):
                    if ant_size > 1:
                        ant_size -= 1

                if phero_option_rect.collidepoint((mx, my)):
                    show_pheromone = not show_pheromone

                if grid_option_rect.collidepoint((mx, my)):
                    draw_grid = not draw_grid

                if back_button_rec.collidepoint((mx, my)):
                    settings = False

                if mode_button_rect.collidepoint((mx, my)):
                    dark_mode = not dark_mode

            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    settings = False

        # Updating settings with new set ones from user.
        evaporation_rate = round(evaporation_rate, 1)
        seek_force = round(seek_force, 1)
        options["ant_count"] = ant_count
        options["evaporation_rate"] = evaporation_rate
        options["max_speed"] = max_speed
        options["seek_force"] = seek_force
        options["ant_size"] = ant_size
        options["show_pheromone"] = show_pheromone
        options["draw_grid"] = draw_grid
        options["dark_mode"] = dark_mode
        pygame.display.update()
        clock.tick()


def main(ant_count, evaporation_rate, max_speed, seek_force, show_pheromone, draw_grid, ant_size, dark_mode):
    food_count = 1
    ant_sizes = {1: (5, 2), 2: (10, 2), 3: (10, 5), 4: (15, 5), 5: (15, 10), 6: (25, 15)}
    food_list = []
    foods = pygame.sprite.Group()

    homes = pygame.sprite.Group()
    home_x, home_y = 750, 450
    ant_home = Home.Home((home_x, home_y))
    homes.add(ant_home)

    ant_group = pygame.sprite.Group()
    grid = PheromoneGrid.pheromoneGrid(1500, 900, screen, show_pheromone)

    pheromone_list = []
    draw_ants = True
    timer = 500
    started = pygame.time.get_ticks()

    for i in range(ant_count):
        # Spawn in ants.
        Ant.TheAnt(ant_home.get_position(), ant_home.get_position(), ant_group, wn_width, wn_height, screen, max_speed,
                   seek_force, ant_sizes[ant_size])

    Queen = Ant.QueenAnt(ant_home.get_position(), ant_home.get_position(), ant_group, wn_width, wn_height, screen,
                         max_speed, seek_force, ant_sizes[ant_size])

    id_count = 0
    for ant in ant_group:
        # Add to pheromone list an Object of the Pheromone class for each ant.
        pheromone_list.append(Pheromone.pheromone(ant, grid, screen, id_count, evaporation_rate))
        id_count += 1

    running = 1
    pygame.display.set_caption("Ant Simulator")

    show_vectors = False
    show_vision = False
    delete_food = False

    while running:
        clock.tick(FPS)
        wall_list = grid.get_wall_list()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == pygame.K_v:
                    show_vectors = not show_vectors
                if event.key == pygame.K_b:
                    show_vision = not show_vision
                if event.key == pygame.K_x:
                    delete_food = not delete_food
                if event.key == pygame.K_z:
                    draw_ants = not draw_ants

            if pygame.time.get_ticks() - started > timer:  # Doesn't allow user to place food until a full second has
                # passed.
                if pygame.mouse.get_pressed()[0]:  # Add Food onto screen
                    mouse_position = pygame.mouse.get_pos()
                    foods.add(Food.Food((mouse_position[0], mouse_position[1]), delete_food))
                    food_list.extend(foods.sprites())
                if pygame.mouse.get_pressed()[1]:  # Add Wall onto screen
                    mouse_position = pygame.mouse.get_pos()
                    grid_position = (round(mouse_position[0] / 5),
                                     round(mouse_position[1] / 5))
                    grid.add_wall(grid_position)

            if pygame.mouse.get_pressed()[2]:  # Destroy Food
                mouse_position = pygame.mouse.get_pos()
                for food_bit in food_list:
                    if pygame.Vector2(mouse_position).distance_to(food_bit.get_food_rect().center) < 10:
                        food_bit.destroy()
                grid.remove_wall((round(mouse_position[0] / 5), round(mouse_position[1] / 5)))

        if food_count % 51 == 0:  # Spawn New Ant in for every 50 food.
            queen_pos = (Queen.get_position()[0], Queen.get_position()[1])
            Ant.TheAnt(queen_pos, ant_home.get_position(), ant_group, wn_width, wn_height, screen, max_speed,
                       seek_force, ant_sizes[ant_size])
            id_count += 1
            food_count = 1
            pheromone_list.append(Pheromone.pheromone(ant, grid, screen, id_count, evaporation_rate))

        ant_group.update()
        if dark_mode:
            screen.fill((0, 0, 0))
        else:
            screen.fill((255, 255, 255))
        if draw_grid:
            grid.draw_grid()

        grid.draw_walls()

        if show_vectors:
            for sprite in ant_group:
                sprite.draw_vectors()
        if show_vision:
            for sprite in ant_group:
                sprite.draw_vision()

        # Ant sees wall or food
        for ant in ant_group:
            for wall in wall_list:
                if not isinstance(ant, Ant.QueenAnt):
                    if ant.wall_circle_collide(Rect((5 * int(wall[0])),
                                                    (5 * int(wall[1])), 5 * 9,
                                                    5 * 9)):
                        ant.set_mode(5)
                        ant.wander((((5 * int(wall[0])) + (4 * 5)),
                                    ((5 * int(wall[1])) + (4 * 5))))

            for food_bit in food_list:

                if not ant.get_holding_food() and not isinstance(ant, Ant.QueenAnt):
                    if ant.vision_circle_collide(food_bit.get_food_rect()):  # Ant sees food
                        ant.set_mode(1)
                        food = food_bit
                        ant.wander(food.get_position())  # Ant should go to food
                    if ant.get_ant_rect().colliderect(food_bit):
                        food_bit.pick()  # Pick up food
                        food_count += 1
                        ant.set_holding(True)
                        ant.stop()  # slow down ant
                        ant.set_mode(2)

        count = -1
        for ant in ant_group:  # If ant touches home then drop food of and wander again.

            count += 1
            pheromone_list[count].pheromone_update()  # Update list of pheromone
            pheromone_list[count].update_grid()
            if ant.get_mode() == 0 and not isinstance(ant, Ant.QueenAnt):

                pheromone = grid.collide_item(ant.get_vision_center())
                if pheromone:
                    ant.set_mode(3)
                    ant.wander(pheromone)

            if ant.get_mode() == 2 or ant.get_mode() == 6:
                if ant.distance_from_home() <= ant_home.get_radius():
                    pheromone_list[count].reset()
                    ant.set_mode(0)  # ant set back to wandering again
                    ant.bounce_off()  # bounce ant off home.

            if ant.get_mode() == 3:  # Fix ant
                pheromone = grid.collide_item(ant.get_vision_center())
                if pheromone is None:
                    ant.set_mode(0)
                else:
                    ant.wander(pheromone)

        # Draw to screen
        if draw_ants:
            ant_group.draw(screen)
            Queen.draw_circle()

        food_list = foods.sprites()
        foods.draw(screen)
        homes.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main_menu()
