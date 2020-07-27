from GUI.GUIcube import GUICube

import pygame

class GUIgrid:
    def __init__(self, win_size, grid_size, win):
        self.win_size = win_size
        self.grid_size = grid_size
        self.win = win
        self.cube_size = self.win_size / self.grid_size
        self.cubes = [[GUICube(win, row, col, self.cube_size) for col in range(self.grid_size)] for row in range(self.grid_size)]

    def draw(self, grid, pher_matrix=None, start=False):
        # set cells with value returned by best ant and highest value based on pheromone matrix
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                cell = grid.get_cell((row, col))
                cube = self.cubes[row][col]

                pher_val = 0

                if pher_matrix:
                    pher_vals = pher_matrix[row][col]

                    # value with the highest pheromone value
                    if len(set(pher_vals)) != 1:
                        pher_val = pher_vals.index(max(pher_vals)) + 1

                # Draw Cubes
                if cell.fixed():
                    if start:
                        cube.initial_cell = True

                    cube.draw(cell.get_val(), pher_val)
                else:
                    cube.draw(0, pher_val)

        # Draw Grid Lines
        for i in range(self.grid_size + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1

            pygame.draw.line(self.win, (0,0,0), (0, i * self.cube_size), (self.win_size, i * self.cube_size), thick)
            pygame.draw.line(self.win, (0, 0, 0), (i * self.cube_size, 0), (i * self.cube_size, self.win_size), thick)
