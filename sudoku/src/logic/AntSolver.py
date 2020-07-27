from logic.Ant import Ant

import random
import copy


class AntSolver:
    def __init__(self, grid, global_pher_update, best_pher_evaporation, num_of_ants, gui, gui_active):
        # grid
        self.grid = grid

        self.global_pher_update = global_pher_update

        self.best_pher_evaporation = best_pher_evaporation

        self.num_of_ants = num_of_ants

        self.gui = gui

        self.gui_active = gui_active

        # array of ants
        self.ants = [Ant() for i in range(self.num_of_ants)]

        # initial pheromone matrix val
        self.initial_pher_val = 1 / self.grid.cell_cnt

        # pheromone matrix
        self.pher_matrix = [
            [[self.initial_pher_val for vals in range(self.grid.grid_size)] for cols in
             range(self.grid.grid_size)]
            for rows in range(self.grid.grid_size)]

        self.solution = self.grid

        self.best_pher_to_add = 0

    def print_pher_matrix(self):
        print("Pheromone matrix:")

        for row_nr, row in enumerate(self.pher_matrix):
            print("row ", row_nr, ":")

            for col_nr, pher_vals in enumerate(row):
                print("col ", col_nr, ":", end="")

                for pher_val in pher_vals:
                    print("{0:.2f} ".format(pher_val), end="")

                print()

    def global_pher_matrix_update(self):
        for row in range(self.grid.grid_size):
            for col in range(self.grid.grid_size):
                sol_cell = self.solution.get_cell((row, col))

                # update pheromone matrix
                if not sol_cell.failed():
                    self.pher_matrix[row][col][sol_cell.get_val() - 1] = self.pher_matrix[row][col][
                                                                             sol_cell.get_val() - 1] * (
                                                                                 1 - self.global_pher_update) + self.global_pher_update * self.best_pher_to_add

    def solve(self, local_pher_update, greediness):
        solved = False
        cycle = 1

        while not solved:

            if not self.gui_active:
                print("cycle: ", cycle)

            for i in range(self.num_of_ants):
                # randomly selected position where ant will start solving sudoku
                start_pos = (random.randint(0, self.grid.grid_size - 1), random.randint(0, self.grid.grid_size - 1))

                # add ant
                self.ants[i] = Ant(self.pher_matrix, self.initial_pher_val, local_pher_update, greediness,
                                   copy.deepcopy(self.grid), start_pos)

            # step with each ant by one cell until they fill all the cells on the grid
            for step in range(self.grid.cell_cnt):
                for ant in self.ants:
                    ant.step()

            # find best performing ant
            best_ant_fixed_cnt = 0
            best_ant = None

            for idx, ant in enumerate(self.ants):
                num_fixed = ant.get_fixed_cnt()

                # sudoku is solved
                if num_fixed == self.grid.cell_cnt:
                    self.solution = ant.grid

                    if self.gui_active:
                        self.gui.screen_with_message(self.solution, "", False, cycle, self.pher_matrix)
                    else:
                        self.solution.print()
                        print(self.solution.fixed_cell_cnt, "fixed cells")
                        # self.print_pher_matrix()

                    return self.solution

                # new best
                if num_fixed > best_ant_fixed_cnt:
                    best_ant = ant
                    best_ant_fixed_cnt = num_fixed

            pher_to_add = self.grid.cell_cnt / (self.grid.cell_cnt - best_ant_fixed_cnt)

            if pher_to_add > self.best_pher_to_add:
                self.solution = best_ant.grid
                self.best_pher_to_add = pher_to_add

            # do global pheromone update
            self.global_pher_matrix_update()

            # do best value evaporation
            self.best_pher_to_add *= (1 - self.best_pher_evaporation)

            if self.gui_active:
                self.gui.screen_with_message(self.solution, "", False, cycle, self.pher_matrix)
            else:
                self.solution.print()
                print(self.solution.fixed_cell_cnt, "fixed cells")
                # self.print_pher_matrix()

            cycle += 1
