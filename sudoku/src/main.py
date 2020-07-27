import sys

from logic.Grid import Grid
from logic.AntSolver import AntSolver
from logic.Constants import *
from GUI.GUI import GUI


def main():
    # command line arguments
    if len(sys.argv) != 3 or (sys.argv[2] != "gui" and sys.argv[2] != "console"):
        print("usage: " + sys.argv[0] + " <input sudoku filename> <gui/console>")
        return

    gui = GUI(WIN_WIDTH, WIN_HEIGHT, GRID_SIZE)

    gui_active = (sys.argv[2] == "gui")

    if gui_active:
        gui.start()

    while True:
        grid = Grid(GRID_SIZE)

        if not grid.read_grid(sys.argv[1]):
            msg = "Sudoku not in valid format"

            if gui_active:
                gui.print_message(msg)
            else:
                print(msg)

            break

        msg = "Initial sudoku grid"
        if gui_active:
            if not gui.initial_screen(grid, msg):
                break
        else:
            print(msg)
            grid.print()

        # perform constraint propagation
        grid.propagate_constraints_all_cells()

        msg = "After constraint propagation"
        if gui_active:
            if not gui.screen_with_message(grid, msg):
                break
        else:
            print(msg)
            grid.print()

        # try deducing values of some cells
        grid.deduce_vals_all_cells()

        msg = "After deducing values"
        if gui_active:
            if not gui.screen_with_message(grid, msg):
                break
        else:
            print(msg)
            grid.print()

        if grid.not_solvable():
            msg = "Sudoku not solvable"

            if gui_active:
                if gui.final_screen(msg):
                    continue
                else:
                    break
            else:
                print(msg)

        if grid.all_cells_fixed():
            msg = "Sudoku solved"

            if gui_active:
                if gui.final_screen(msg):
                    continue
                else:
                    break
            else:
                print(msg)

        # solve using ant colony system
        msg = "Ant colony system"
        if gui_active:
            gui.print_message(msg)
        else:
            print(msg)

        solver = AntSolver(grid, GLOBAL_PHER_UPDATE, BEST_PHER_EVAPORATION, NUM_OF_ANTS, gui, gui_active)
        solution = solver.solve(LOCAL_PHER_UPDATE, GREEDINESS)

        if solution.is_valid():
            msg = "Sudoku solved!"

            if gui_active:
                if gui.final_screen(msg):
                    continue
                else:
                    break
            else:
                print(msg)
                break
        else:
            msg = "Sudoku solution not valid"

            if gui_active:
                if gui.final_screen(msg):
                    continue
                else:
                    break
            else:
                print(msg)
                break

    if gui_active:
        gui.end()


if __name__ == "__main__":
    main()
