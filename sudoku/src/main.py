import sys

from App import App


def main():
    # command line arguments
    if len(sys.argv) != 3 or (sys.argv[2] != "gui" and sys.argv[2] != "console"):
        print("usage: " + sys.argv[0] + " <input sudoku filename> <gui/console>")
        return

    sudoku_file = sys.argv[1]
    gui_active = (sys.argv[2] == "gui")

    app = App(gui_active, sudoku_file)
    app.run()


if __name__ == "__main__":
    main()
