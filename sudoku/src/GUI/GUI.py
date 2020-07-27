from GUI.GUIgrid import GUIgrid

import pygame
import time


def format_time(secs):
    min = secs // 60
    sec = secs % 60
    millis = (secs * 100) % 100
    time_str = "{:02.0f}".format(min) + ":" + "{:02.0f}".format(sec) + ":" + "{:02.0f}".format(millis)
    return time_str


class GUI:
    def __init__(self, win_width, win_height, grid_size):
        self.win_width = win_width
        self.win_height = win_height
        self.grid_size = grid_size
        self.win = None
        self.GUIgrid = None
        self.start_time = None
        self.start_button = None

    def start(self):
        pygame.init()
        pygame.font.init()
        self.win = pygame.display.set_mode((self.win_width, self.win_height))
        self.GUIgrid = GUIgrid(self.win_width, self.grid_size, self.win)

        pygame.display.set_caption("Ant colony optimization sudoku solver")

    def print_message(self, msg):
        # message
        font = pygame.font.SysFont("dejavusansmono", 25)
        text_box = font.render(msg, True, (0, 0, 0))
        text_rect = text_box.get_rect()

        x = 2 * self.win_width / 3 - text_rect.width / 2
        y = (self.win_height + self.win_width) / 2 - text_rect.height / 2

        # delete old message
        thick = 4
        pygame.draw.rect(self.win, (255, 255, 255), (
        self.win_width / 3, self.win_width + thick, 2 * self.win_width / 3, self.win_height - self.win_width - thick))

        # print new message
        self.win.blit(text_box, (x, y))

        pygame.display.update()

    def final_screen(self, msg):
        self.print_message(msg)

        # wait till window is closed or start pressed again
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.MOUSEBUTTONDOWN and self.start_button.collidepoint(event.pos):
                    return True

    def screen_with_message(self, grid, msg="", wait=True, cycle=0, pher_matrix=None):
        # redraw
        self.redraw(grid, cycle, False, pher_matrix)

        # print message
        if msg != "":
            self.print_message(msg)

        # if wait is True, wait till window is closed or start pressed again
        if wait:

            saved_time = self.start_time

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return False
                    elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                        self.start_time += (time.time() - saved_time)
                        return True

    def initial_screen(self, grid, msg):
        # redraw screen
        self.redraw(grid, 0, True)

        self.print_message(msg)

        # wait till start button is clicked
        start_button_clicked = False

        while not start_button_clicked:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button.collidepoint(event.pos):
                        start_button_clicked = True
                        break

        # start counting time
        self.start_time = time.time()
        return True

    def redraw(self, grid, cycle=0, start=False, pher_matrix=None):
        self.win.fill((255, 255, 255))

        font = pygame.font.SysFont("dejavusansmono", 25)

        # time
        if start:
            play_time = 0
        else:
            play_time = time.time() - self.start_time

        text = "Time: " + format_time(play_time)
        text_box = font.render(text, True, (0, 0, 0))
        text_height = text_box.get_height()

        padding = (self.win_height - self.win_width - 3 * text_height) / 8

        x = 10
        y = self.win_width + padding
        self.win.blit(text_box, (x, y))

        # fixed cells
        text = "Fixed cells: " + str(grid.fixed_cell_cnt)
        text_box = font.render(text, True, (0, 0, 0))
        y = y + text_height + padding
        self.win.blit(text_box, (x, y))

        # cycle
        text = "Cycle: " + str(cycle)
        text_box = font.render(text, True, (0, 0, 0))
        y = y + text_height + padding
        self.win.blit(text_box, (x, y))

        # start button
        text = "Start"
        text_box = font.render(text, True, (0, 0, 0))
        x = self.win_width / 6 - (text_box.get_width() + padding) / 2
        y = y + text_height + 2 * padding

        if start:
            self.start_button = pygame.Rect(x, y, text_box.get_width() + padding, text_box.get_height() + padding)

        pygame.draw.rect(self.win, (0, 0, 0), self.start_button)
        pygame.draw.rect(self.win, (255, 255, 255), (
        self.start_button.left + 3, self.start_button.top + 3, self.start_button.width - 6,
        self.start_button.height - 6))
        self.win.blit(text_box, (x + padding / 2, y + padding / 2))

        # draw grid and board
        self.GUIgrid.draw(grid, pher_matrix, start)

        pygame.display.update()

    def end(self):
        pygame.font.quit()
        pygame.quit()
