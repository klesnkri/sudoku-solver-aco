from logic.Cell import Cell

import math

class Grid:
    def __init__(self, grid_size):
        # initialize empty sudoku 9x9 grid
        self.grid_size = grid_size
        self.cell_cnt = grid_size ** 2
        self.fixed_cell_cnt = 0
        self.failed_cell_cnt = 0
        self.grid = [[Cell() for cols in range(self.grid_size)] for rows in range(self.grid_size)]

    def get_cell(self, pos):
        return self.grid[pos[0]][pos[1]]

    def set_cell_val(self, pos, val):
        cell = self.get_cell(pos)

        if not cell.failed():
            if not cell.fixed():
                self.fixed_cell_cnt += 1

            cell.set_val(val)

    def all_cells_fixed(self):
        return self.fixed_cell_cnt == self.cell_cnt

    def not_solvable(self):
        return self.failed_cell_cnt > 0

    def propagate_constraints_row(self, pos):
        cell_to_reduce = self.get_cell(pos)

        for col in range(self.grid_size):
            if cell_to_reduce.failed():
                return

            if col is not pos[1]:
                cell_coo = (pos[0], col)
                cell = self.get_cell(cell_coo)

                if not cell.failed():
                    if cell.fixed():
                        cell.delete(cell_to_reduce.get_val())

                        if cell.failed():
                            self.failed_cell_cnt += 1
                            self.fixed_cell_cnt -= 1

                    else:
                        cell.delete(cell_to_reduce.get_val())

                        if cell.fixed():
                            self.fixed_cell_cnt += 1
                            self.propagate_constraints_cell(cell_coo)

    def propagate_constraints_col(self, pos):
        cell_to_reduce = self.get_cell(pos)

        for row in range(self.grid_size):
            if cell_to_reduce.failed():
                return

            if row is not pos[0]:
                cell_coo = (row, pos[1])
                cell = self.get_cell(cell_coo)

                if not cell.failed():
                    if cell.fixed():
                        cell.delete(cell_to_reduce.get_val())

                        if cell.failed():
                            self.failed_cell_cnt += 1
                            self.fixed_cell_cnt -= 1

                    else:
                        cell.delete(cell_to_reduce.get_val())

                        if cell.fixed():
                            self.fixed_cell_cnt += 1
                            self.propagate_constraints_cell(cell_coo)

    def propagate_constraints_square(self, pos):
        cell_to_reduce = self.get_cell(pos)

        square_size = int(math.sqrt(self.grid_size))
        square_start_row = pos[0] // square_size * square_size
        square_start_col = pos[1] // square_size * square_size

        for row in range(square_start_row, square_start_row + square_size):
            for col in range(square_start_col, square_start_col + square_size):
                if cell_to_reduce.failed():
                    return

                if row != pos[0] or col != pos[1]:
                    cell_coo = (row, col)
                    cell = self.get_cell(cell_coo)

                    if not cell.failed():
                        if cell.fixed():
                            cell.delete(cell_to_reduce.get_val())

                            if cell.failed():
                                self.failed_cell_cnt += 1
                                self.fixed_cell_cnt -= 1

                        else:
                            cell.delete(cell_to_reduce.get_val())

                            if cell.fixed():
                                self.fixed_cell_cnt += 1
                                self.propagate_constraints_cell(cell_coo)

    # propagate constraints after setting cell
    def propagate_constraints_cell(self, pos):
        self.propagate_constraints_row(pos)
        self.propagate_constraints_col(pos)
        self.propagate_constraints_square(pos)

    def propagate_constraints_all_cells(self):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                cell = self.get_cell((row, col))

                if cell.fixed() and not cell.failed():
                    self.propagate_constraints_cell((row, col))

    def deduce_val_row(self, pos, val):
        for col in range(self.grid_size):
            if col != pos[1]:
                cell = self.get_cell((pos[0], col))

                if cell.can_contain(val):
                    return False

        return True

    def deduce_val_col(self, pos, val):
        for row in range(self.grid_size):
            if row != pos[0]:
                cell = self.get_cell((row, pos[1]))

                if cell.can_contain(val):
                    return False

        return True

    def deduce_val_square(self, pos, val):
        square_size = int(math.sqrt(self.grid_size))
        square_start_row = pos[0] // square_size * square_size
        square_start_col = pos[1] // square_size * square_size

        for row in range(square_start_row, square_start_row + square_size):
            for col in range(square_start_col, square_start_col + square_size):
                if row != pos[0] or col != pos[1]:
                    cell = self.get_cell((row, col))

                    if cell.can_contain(val):
                        return False

        return True

    def deduce_val_cell(self, pos):
        cell = self.get_cell(pos)

        for val in cell.possible_vals:
            if self.deduce_val_row(pos, val) or self.deduce_val_col(pos, val) or self.deduce_val_square(pos, val):
                self.set_cell_val(pos, val)
                self.propagate_constraints_cell(pos)
                return

    def deduce_vals_all_cells(self):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                cell = self.get_cell((row, col))

                if not cell.fixed() and not cell.failed():
                    self.deduce_val_cell((row, col))

    # read sudoku grid
    def read_grid(self, sudoku_file):
        input_grid = open(sudoku_file, "r")

        for row, vals in enumerate(input_grid.readlines()):
            if len(vals) - 1 != self.grid_size:
                input_grid.close()
                return False

            for col in range(self.grid_size):
                val = vals[col]

                # not valid sudoku value
                if not (vals[col] == '-' or (val.isdigit() and 1 <= int(val) <= self.grid_size)):
                    input_grid.close()
                    return False

                if val != '-':
                    self.set_cell_val((row, col), int(val))

        input_grid.close()
        return True

    def print(self):
        for row in range(self.grid_size):
            if row % math.sqrt(self.grid_size) == 0:
                print("-------------------------")

            for col in range(self.grid_size):
                if col % math.sqrt(self.grid_size) == 0:
                    print("|", end=" ")

                val = self.grid[row][col]

                if val.fixed():
                    print(val.get_val(), end=" ")
                else:
                    print("-", end=" ")

            print("|")

        print("-------------------------")

    def is_valid(self):
        self.propagate_constraints_all_cells()

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                cell = self.get_cell((row, col))

                if not cell.fixed():
                    return False

        return True
