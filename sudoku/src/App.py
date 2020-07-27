from logic.Grid import Grid
from logic.AntSolver import AntSolver
from Constants import *
from GUI.GUI import GUI


class App:
    def __init__(self, gui_active, sudoku_file):
        self.gui_active = gui_active

        self.sudoku_file = sudoku_file

    def run(self):
        gui = GUI(WIN_WIDTH, WIN_HEIGHT, GRID_SIZE)

        if self.gui_active:
            gui.start()

        while True:
            grid = Grid(GRID_SIZE)

            if not grid.read_grid(self.sudoku_file):
                msg = "Sudoku not in valid format"

                if self.gui_active:
                    gui.print_message(msg)
                else:
                    print(msg)

                break

            msg = "Initial sudoku grid"
            if self.gui_active:
                if not gui.initial_screen(grid, msg):
                    break
            else:
                print(msg)
                grid.print()

            # perform constraint propagation
            grid.propagate_constraints_all_cells()

            msg = "After constraint propagation"
            if self.gui_active:
                if not gui.screen_with_message(grid, msg):
                    break
            else:
                print(msg)
                grid.print()

            # try deducing values of some cells
            grid.deduce_vals_all_cells()

            msg = "After deducing values"
            if self.gui_active:
                if not gui.screen_with_message(grid, msg):
                    break
            else:
                print(msg)
                grid.print()

            if grid.not_solvable():
                msg = "Sudoku not solvable"

                if self.gui_active:
                    if gui.final_screen(msg):
                        continue
                    else:
                        break
                else:
                    print(msg)

            if grid.all_cells_fixed():
                msg = "Sudoku solved"

                if self.gui_active:
                    if gui.final_screen(msg):
                        continue
                    else:
                        break
                else:
                    print(msg)

            # solve using ant colony system
            msg = "Ant colony system"
            if self.gui_active:
                gui.print_message(msg)
            else:
                print(msg)

            solver = AntSolver(grid, GLOBAL_PHER_UPDATE, BEST_PHER_EVAPORATION, NUM_OF_ANTS, gui, self.gui_active)
            solution = solver.solve(LOCAL_PHER_UPDATE, GREEDINESS)

            if solution.is_valid():
                msg = "Sudoku solved!"

                if self.gui_active:
                    if gui.final_screen(msg):
                        continue
                    else:
                        break
                else:
                    print(msg)
                    break
            else:
                msg = "Sudoku solution not valid"

                if self.gui_active:
                    if gui.final_screen(msg):
                        continue
                    else:
                        break
                else:
                    print(msg)
                    break

        if self.gui_active:
            gui.end()
