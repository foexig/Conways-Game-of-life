import random
import pygame
from pygame import gfxdraw

pygame.init()
width = 640
height = 640
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Conways von d und f")
clock = pygame.time.Clock()

white = (255 ,255 ,255)
black = (50 , 50 ,50 )
gray = (30, 30, 30)

class Cell:
    def __init__(self , x , y , cell_size , status=black):
        self.x = x
        self.y = y
        self.cell_size = cell_size
        self.status = status

    def draw(self):
        cell_rect = pygame.Rect(self.x , self.y , self.cell_size, self.cell_size)
        pygame.draw.rect(screen, self.status, cell_rect)

    def get_nearby_living_cells(self, grid):
        living_cells = 0
        x_index = self.x // (self.cell_size + 2)
        y_index = self.y // (self.cell_size + 2)

        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                nx = x_index + dx
                ny = y_index + dy
                if dx == 0 and dy == 0:
                    continue
                if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
                    if grid[ny][nx].status == white:
                        living_cells += 1
        return living_cells

class GameOfLive:
    def __init__(self , width , height , cell_size , gap):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.gap = gap
        self.cols = width // (cell_size + gap)
        self.rows = height // (cell_size + gap)
        self.grid = []
        self.running = False
        self.level = 1
        self.placement_zone_cols = self.cols // 3
        self.won = False
        self.play_button_rect = pygame.Rect(0, 0, 0, 0)

        for row in range(self.rows):
            row_list = []
            for col in range(self.cols):
                x = col * (cell_size + gap)
                y = row * (cell_size + gap)
                cell = Cell(x , y , self.cell_size)
                row_list.append(cell)
            self.grid.append(row_list)

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def handle_mouse_click(self, pos):
        mx, my = pos
        if self.play_button_rect.collidepoint(pos):
            self.running = not self.running
            return

        col = mx // (self.cell_size + self.gap)
        row = my // (self.cell_size + self.gap)

        if col < self.placement_zone_cols:  # Nur linke Seite erlaubt
            if 0 <= row < self.rows and 0 <= col < self.cols:
                cell = self.grid[row][col]
                cell.status = white if cell.status == black else black

    def draw(self):
        screen.fill(gray)
        for row in self.grid:
            for cell in row:
                grid_x = cell.x // (self.cell_size + self.gap)
                if grid_x < self.placement_zone_cols:
                    pygame.draw.rect(screen, (80, 80, 80), pygame.Rect(cell.x, cell.y, self.cell_size, self.cell_size))
                cell.draw()

        # Play/Pause Button
        font = pygame.font.SysFont(None, 32)
        label = "Pause" if self.running else "Play"
        text = font.render(label, True, white)
        text_rect = text.get_rect(topleft=(10, 10))
        screen.blit(text, text_rect)
        self.play_button_rect = text_rect

        if self.won:
            win_text = font.render("Level 1: Gewonnen!", True, (0, 255, 0))
            screen.blit(win_text, (screen.get_width() // 2 - 80, 10))

    def reset(self):
        for row in self.grid:
            for cell in row:
                cell.status = black
        self.won = False
        self.running = False

    def update(self):
        new_states = [[cell.status for cell in row] for row in self.grid]

        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                neighbors = cell.get_nearby_living_cells(self.grid)
                if cell.status == white:
                    if neighbors < 2 or neighbors > 3:
                        new_states[y][x] = black
                else:
                    if neighbors == 3:
                        new_states[y][x] = white

        for y in range(self.rows):
            for x in range(self.cols):
                self.grid[y][x].status = new_states[y][x]

        for row in self.grid:
            if row[-1].status == white:
                self.running = False
                self.won = True

    def random_distr(self):
        for row in self.grid:
            for cell in row:
                if random.randrange(1, 3) == 1:
                    cell.status = white

cell_size = 8
gap = 2
game = GameOfLive(640, 640, cell_size, gap)

def main():
    update_timer = 0
    update_interval = 10

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    game.random_distr()
                if event.key == pygame.K_q:
                    game.update()
                if event.key == pygame.K_SPACE:
                    game.running = not game.running
                if event.key == pygame.K_r:
                    game.reset()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                game.handle_mouse_click(pygame.mouse.get_pos())

        current_time = pygame.time.get_ticks()
        if game.running and current_time - update_timer > update_interval:
            game.update()
            update_timer = current_time

        game.draw()
        pygame.display.flip()
        clock.tick(60)

main()
