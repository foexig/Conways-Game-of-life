import random

import pygame
from pygame import gfxdraw

pygame.init()
width = 256
height = 256
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Conways von d und f")
clock = pygame.time.Clock()

white = (255 ,255 ,255)
black = (0 , 0 ,0 )
cell = 64
def random_distr():
    for w in range(width) :
        for h in range(height):
                if random.randrange(0, 100) == 1:
                    gfxdraw.pixel(screen, w, h, white)

def random_distr2():
    for w in range(width)  :
        for h in range(height):
                gfxdraw.pixel(screen, w, h, white)

def fill():
    for w in range(width):
        for h in range(height):
            gfxdraw.pixel(screen, w, h, white)

def mouse_draw():
    x , y = pygame.mouse.get_pos()
    gfxdraw.pixel(screen, x, y, white)


def rule_1():# Kill
    pass

def get_nearby_living_cells(x ,y):
    living_cells = 0
    for xw in range(x-1,x+2):
        #print(f'X: {xw}')
        for yw in range(y - 1, y + 2):
            if not(xw == x and yw == y):
                if not(xw < 0 or xw > width - 1  or yw < 0 or yw > height - 1 ):
                    #print(f'X: {xw}, Y: {yw}')

                    cell_collor = screen.get_at((xw, yw))
                    if cell_collor == (255,255,255,255) :
                        living_cells += 1

    return living_cells

def iterate():
    temp_screen = [[0 for x in range(width)] for y in range(height)]
    for xw in range(width):
        for yw in range(height):
            alive = False
            #Check Livestate of Cell
            if screen.get_at((xw, yw)) == white:
                alive = True
            #Get neighborstates
            neighbors = get_nearby_living_cells(xw, yw)
            #Check for Rule 1 (Survive)
            if alive :
                if neighbors == 2 or neighbors == 3 :
                    temp_screen[xw][yw] = True
            #Check for Rule 2 (Born)
            if not(alive):
                if neighbors == 3:
                    temp_screen[xw][yw] = True
            #Check for Rule 3 (Die)
            if alive:
                if neighbors < 2 or neighbors > 3:
                    temp_screen[xw][yw] = False
            # Check for ünnötige regel 4 (not Born)
            #if not(alive):
               #if neighbors != 3:
                  #temp_screen[xw][yw] = False
    #Apply determined state to screen
    for xw in range(width):
        for yw in range(height):
            if temp_screen[xw][yw]:
                gfxdraw.pixel(screen, xw, yw, white)
            else:
                gfxdraw.pixel(screen, xw, yw, black)

def transform():
    pass

def draw():
    pygame.display.update()


def main():
    while True:

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    iterate()
                if event.key == pygame.K_t:
                    random_distr2()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                random_distr()
            if keys[pygame.K_f]:
               fill()
            if keys[pygame.K_SPACE]:
               iterate()
            #if pygame.mouse.get_pressed():
            if keys[pygame.K_d]:
                mouse_draw()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


        draw()
        clock.tick(60)

main()