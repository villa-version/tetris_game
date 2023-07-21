import pygame, time
from random import randint as random
from copy import deepcopy


run_game = True 
WIDTH, HEIGHT = 500, 700
CELL_SIZE = 25
CELL_NUMB_X, CELL_NUMB_Y = WIDTH//CELL_SIZE, HEIGHT//CELL_SIZE
screen = pygame.display.set_mode((CELL_NUMB_X*CELL_SIZE, CELL_NUMB_Y*CELL_SIZE))
figures = []
start_x, start_y = CELL_NUMB_X//2-1, CELL_NUMB_Y//2-10
figures_layouts = [[(start_x, start_y), (start_x-1, start_y),
            (start_x, start_y-1), (start_x+1, start_y)],
           [(start_x, start_y), (start_x, start_y-1),
            (start_x, start_y-2), (start_x-1, start_y-2),
            (start_x-2, start_y-2)]]
key_pressed = ''

field = []
for y in range(-1, CELL_NUMB_Y+1):
    l = []
    for x in range(-1, CELL_NUMB_X+1):
        if -1 < x < CELL_NUMB_X and -1 < y < CELL_NUMB_Y:
            l.append(0)
        else:
            l.append(-1)
    field.append(l)

field_copy = deepcopy(field)


class Rect:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.can_move = True

    def draw(self):
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(self.x*CELL_SIZE, self.y*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def fall(self):
        if self.can_move:
            self.y += 1

    def move(self):
        if self.can_move:
            if key_pressed == 'a':
                self.x -= 1
            elif key_pressed == 'd':
                self.x += 1


def update():
    global field_copy
    field_copy = deepcopy(field)
    draw_cells()
    update_figures()
    #for row in field:
    #    print(row)
    update_field()


def update_field():
    global field
    field = field_copy


def draw_cells():
    for x in range(CELL_NUMB_X):
        for y in range(CELL_NUMB_Y):
            pygame.draw.rect(screen, pygame.Color('white'),
                             pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1))


def update_figures():
    for figure in figures:
        for rect in figure:
            rect.draw()
            rect.fall()
            rect.move()
            change_numb_state(rect)
    for figure in figures:
        for i in range(len(figure)):
            if collide(figure[i].x, figure[i].y) and figure[i].can_move:
                for j in range(len(figure)):
                    figure[j].can_move = False
                create_figure(*figures_layouts[random(0, len(figures_layouts)-1)])
                break


def collide(rx, ry):
    if field[ry+2][rx+1] == -1 or field[ry+2][rx+1] == 1:
        return True
    return False


def create_figure(*args):
    global figures
    figures.append([])
    for x, y in args:
        figures[-1].append(Rect(x, y))


def change_numb_state(obj):
    global field
    if obj.can_move:
        numb = 2
    else:
        numb = 1
        field[obj.y+1][obj.x+1] = numb


def main():
    global run_game, screen, figures, key_pressed, figures_layouts, field

    create_figure(*figures_layouts[random(0, len(figures_layouts)-1)])

    while run_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    key_pressed = 'a'
                if event.key == pygame.K_d:
                    key_pressed = 'd'

        screen.fill(pygame.Color('black'))
        update()
        key_pressed = ''
        pygame.display.update()
        time.sleep(0.15)


if __name__ == '__main__':
    main()

