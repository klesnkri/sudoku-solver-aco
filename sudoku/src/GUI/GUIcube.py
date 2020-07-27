import pygame

class GUICube:
    def __init__(self, win, row, col, size):
        self.win = win
        self.row = row
        self.col = col
        self.size = size
        self.initial_cell = False



    def draw(self, val, pher_val):
        font = pygame.font.SysFont("dejavusansmono", 40)

        x = self.col * self.size
        y = self.row * self.size

        if self.initial_cell:
            pygame.draw.rect(self.win, (252, 211, 3), (x, y, self.size, self.size))

        if val == 0:
            text = font.render(" ", 1, (0, 0, 0))
        else:
            text = font.render(str(val), 1, (0, 0, 0))

        self.win.blit(text, (x + (self.size /2 - text.get_width()/2), y + (self.size/2 - text.get_height()/2)))

        font = pygame.font.SysFont("dejavusansmono", 20)

        if pher_val == 0:
            text = font.render(" ", 1, (0, 0, 0))
        else:
            text = font.render(str(pher_val), 1, (0, 0, 0))

        self.win.blit(text, (x + self.size - text.get_width(), y))