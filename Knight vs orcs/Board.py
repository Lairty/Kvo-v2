import pygame


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.standartWidth = width
        self.standartHeight = height
        self.currentWidth = width * 40
        self.currentHeight = height * 40
        self.board = [[-1] * height for _ in range(width)]
        self.left = 0
        self.top = 0
        self.cell_size = 40
        self.color = pygame.Color("black")

    def set_view(self, left=10, top=10, cell_size=30):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for row in range(self.height):
            for col in range(self.width):
                rect = pygame.Rect(
                    self.left + self.cell_size * col,
                    self.top + self.cell_size * row,
                    self.cell_size, self.cell_size
                )
                pygame.draw.rect(screen, self.color, rect, 1)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def get_cell(self, mouse_pos):
        col = (mouse_pos[0] - self.left) // self.cell_size
        row = (mouse_pos[1] - self.top) // self.cell_size
        if 0 <= col < self.width and 0 <= row < self.height:
            return col, row

    def on_click(self, cell_coords):
        pass
