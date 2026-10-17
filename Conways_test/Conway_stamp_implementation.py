import random
import pygame

pygame.init()
width = 640
height = 640
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Conways von d und f")
clock = pygame.time.Clock()

white = (255 ,255 ,255)
black = (50 , 50 ,50 )
grey = (93 , 93 , 93)
iteration_interval = 20

stop_uppon_click = True

glider_stamp = [

            [False, False, True],
            [True, False, True],
            [False, True, True]

        ]

exp_stamp = [

            [True, True, True],
            [True, False, True],
            [True, False, True]

                     ]
gosper_glider_gun = [
    [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,False,False,False],
    [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,True,False,True,False,False,False,False,False,False,False,False,False,False,False],
    [False,False,False,False,False,False,False,False,False,False,False,False,True,True,False,False,False,False,False,False,True,True,False,False,False,False,False,False,False,False,False,False,False,False,True,True],
    [False,False,False,False,False,False,False,False,False,False,False,True,False ,False ,False,True,False,False,False,False,True,True,False,False,False,False,False,False,False,False,False,False,False,False,True,True],
    [True,True,False,False,False,False,False,False,False,False,True,False,False,False,False ,False,True,False,False,False,True,True,False,False,False,False,False,False,False,False,False,False,False,False,False,False],
    [True,True,False,False,False,False,False,False,False,False,True,False,False,False,True ,False,True,True,False,False,False,False,True,False,True,False,False,False,False,False,False,False,False,False,False,False],
    [False,False,False,False,False,False,False,False,False,False,True,False,False,False,False,False ,True ,False,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,False,False,False],
    [False,False,False,False,False,False,False,False,False,False,False,True,False,False,False,True,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False],
    [False,False,False,False,False,False,False,False,False,False,False,False,True,True,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False],
    [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False],
]

block_stamp = [

            [True,True],
            [True,True]
    ]

stamp_list = [ glider_stamp , exp_stamp , gosper_glider_gun , block_stamp ]

def rotate_stamp(stamp, rotation):
    for _ in range(rotation % 4):
        stamp = [list(row)[::-1] for row in zip(*stamp)]  # 90° Drehung
    return stamp

class Cell:
    def __init__(self , x , y , cell_size , status=black):
        self.x = x
        self.y = y
        self.cell_size = cell_size
        self.status = status

    def draw(self):
        #
        cell_rect = pygame.Rect(self.x , self.y , self.cell_size, self.cell_size)
        pygame.draw.rect(screen, self.status, cell_rect)

    def get_nearby_living_cells(self, matrix):
        living_cells = 0
        # calculate index in matrix
        x_cord = self.x // (self.cell_size + 2)
        y_cord = self.y // (self.cell_size + 2)
        # creates a matrix for checking all the cells sorounding it
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                c_x = x_cord + dx
                c_y = y_cord + dy
                if dx == 0 and dy == 0:
                    continue  # skip own cell
                # use mod so the ends glue together
                if matrix[c_y % len(matrix)][c_x % len(matrix[0])].status == white:
                    living_cells += 1

        return living_cells

class VisualCell:
    def __init__(self , x , y , cell_size , status=black):
        self.x = x
        self.y = y
        self.cell_size = cell_size
        self.visual_status = status

    def draw(self):
        cell_rect = pygame.Rect(self.x, self.y, self.cell_size, self.cell_size)
        pygame.draw.rect(screen, self.visual_status, cell_rect)

class GameOfLive :
    def __init__(self , width , height , cell_size , gap):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.gap = gap
        self.cols = width // (cell_size + gap)
        self.rows = height // (cell_size + gap)
        self.matrix = []
        self.visual_matrix = []
        self.running = False

        for row in range(self.rows):
            row_list = []
            row_list_v = []
            for col in range(self.cols):
                x = col * (cell_size + gap)
                y = row * (cell_size + gap)
                cell = Cell(x , y , self.cell_size)
                row_list.append(cell)
                visual_cell = VisualCell(x , y , self.cell_size)
                row_list_v.append(visual_cell)
            self.matrix.append(row_list)
            self.visual_matrix.append(row_list_v)

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def handle_mouse_click(self, pos):
        if stop_uppon_click:
            self.running = False
        mx, my = pos
        col = mx // (self.cell_size + self.gap)
        row = my // (self.cell_size + self.gap)

        if 0 <= row < self.rows and 0 <= col < self.cols:
            cell = self.matrix[row][col]
            cell.status = white if cell.status == black else black

    def draw(self):
        for row in self.matrix:
            for cell in row:
                cell.draw()
        for row in self.visual_matrix:
            for visual_cell in row:
                if visual_cell.visual_status == grey:
                    visual_cell.draw()

    def stamps(self, pos, current_rot, current_stamp):
        mx, my = pos
        x_index = mx // (self.cell_size + self.gap)
        y_index = my // (self.cell_size + self.gap)

        stamp = rotate_stamp(stamp_list[current_stamp], current_rot)
        h = len(stamp)
        w = len(stamp[0])

        for y in range(h):
            for x in range(w):
                nx = x_index + x - w // 2
                ny = y_index + y - h // 2

                if 0 <= nx < self.cols and 0 <= ny < self.rows:
                    cell = self.matrix[ny][nx]
                    cell.status = white if stamp[y][x] else black

    def hover(self, pos, current_rot, current_stamp):
        mx, my = pos
        x_index = mx // (self.cell_size + self.gap)
        y_index = my // (self.cell_size + self.gap)

        stamp = rotate_stamp(stamp_list[current_stamp], current_rot)
        h = len(stamp)
        w = len(stamp[0])

        for y in range(h):
            for x in range(w):
                nx = x_index + x - w // 2
                ny = y_index + y - h // 2

                if 0 <= nx < self.cols and 0 <= ny < self.rows:
                    cell = self.matrix[ny][nx]
                    vcell = self.visual_matrix[ny][nx]
                    if cell.status == black and stamp[y][x]:
                        vcell.visual_status = grey

    def reset(self):
        for row in self.matrix:
            for cell in row:
                cell.status = black

    def update(self):
        new_states = [[cell.status for cell in row] for row in self.matrix]

        for y, row in enumerate(self.matrix):
            for x, cell in enumerate(row):
                neighbors = cell.get_nearby_living_cells(self.matrix)
                if cell.status == white:
                    if neighbors < 2 or neighbors > 3:
                        new_states[y][x] = black
                else:
                    if neighbors == 3:
                        new_states[y][x] = white

        # Status anwenden
        for y in range(self.rows):
            for x in range(self.cols):
                self.matrix[y][x].status = new_states[y][x]

cell_size = 1
game = GameOfLive(640  , 640 , cell_size  ,2)

def main(iteration_interval):
    stamp_on = False
    update_timer = 0  # Zeit seit letztem Schritt
    current_rot = 0
    current_stamp = 1
    def draw(game , stamp_on , current_stamp):
        screen.fill((0, 0, 0))

        for row in game.visual_matrix: # stamp hover setback
            for vcell in row :
                vcell.visual_status = black

        if stamp_on:
           game.hover(pygame.mouse.get_pos() , current_rot % 4 , current_stamp - 1 )

        game.draw()
        pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
             # Key events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u:
                    game.update()
                elif event.key == pygame.K_SPACE:
                    game.running = not game.running  # Start/Stop toggle
                elif event.key == pygame.K_r:
                    game.reset()
                elif event.key == pygame.K_s:
                    stamp_on = not stamp_on
                elif event.key == pygame.K_o:
                    options(iteration_interval)
                elif event.key == pygame.K_1 :
                    current_stamp = 1
                elif event.key == pygame.K_2:
                    current_stamp = 2
                elif event.key == pygame.K_3:
                    current_stamp = 3
                elif event.key == pygame.K_4:
                    current_stamp = 4

                    # Mouse events
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1  and not stamp_on:
                    game.handle_mouse_click(pygame.mouse.get_pos())

                if event.button == 1 and stamp_on:
                    game.stamps(pygame.mouse.get_pos(), current_rot % 4 , current_stamp - 1 )

                if event.button == 4 : # 4 up 5 down
                    current_rot += 1

                if event.button == 5 : # 4 up 5 down
                    current_rot -= 1

        current_time = pygame.time.get_ticks()
        if game.running and current_time - update_timer > iteration_interval:
            game.update()
            update_timer = current_time

        draw(game , stamp_on , current_stamp)
        clock.tick(60)

def menu(iteration_interval):
    screen.fill((0 ,0 ,0))
    font = pygame.font.Font("fonts/DS-DIGIT.TTF", 60)
    label_s = "Press Tab to start"
    start_text = font.render(label_s, True, white)
    start_text_rect = start_text.get_rect(midbottom=(width // 2 , height // 2 - 100 ))

    font = pygame.font.Font("fonts/DS-DIGIT.TTF", 30)
    label_o = "Press O for options "
    opt_text = font.render(label_o, True, white)
    opt_text_rect = opt_text.get_rect(center=(width // 2, height // 2  ))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    main(iteration_interval)
                if event.key == pygame.K_o:
                    options(iteration_interval)
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.blit(start_text, start_text_rect)
        screen.blit(opt_text, opt_text_rect)
        pygame.display.flip()
        clock.tick(60)

def options(iteration_interval):
    screen.fill((0 ,0 ,0))

    font = pygame.font.Font("fonts/DS-DIGIT.TTF", 15)
    label_s = "Press Tab to start"
    start_text = font.render(label_s, True, white)
    start_text_rect = start_text.get_rect(center=(width // 5 , height // 10 ))
    stop_uppon_click
    font = pygame.font.Font("fonts/DS-DIGIT.TTF", 50)
    while True:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    main(iteration_interval)
                if event.key == pygame.K_BACKSPACE:
                    menu(iteration_interval)

                if event.key == pygame.K_UP:
                    iteration_interval += 10
                if event.key == pygame.K_DOWN and iteration_interval > 0 :
                    iteration_interval -= 10

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        label_interv = f'intervall time (ms) : {iteration_interval}'
        int_text = font.render(label_interv, True, white)
        int_text_rect = int_text.get_rect(center=(width // 2, height // 2))


        screen.blit(start_text, start_text_rect)
        screen.blit(int_text, int_text_rect)

        pygame.display.flip()
        clock.tick(60)

menu(iteration_interval)