from random import randint
import pygame
from pygame.locals import *
import sys


HEIGHT = 20
WIDTH = 20

HEAD = 0

FOOD = 0
UNDEF = int(1E3)
SNAKE = int(1E6)

LEFT = -1
RIGHT = 1
UP = -WIDTH
DOWN = WIDTH


board = [0] * HEIGHT * WIDTH                # use one dimensional list to represent 2 dimensional board
snake = [0] * (HEIGHT * WIDTH+1)
snake[HEAD] = 1*WIDTH+1
snake_size = 1

vboard = [0] * HEIGHT * WIDTH
vsnake = [0] * (HEIGHT * WIDTH+1)
vsnake[HEAD] = 1*WIDTH+1
vsnake_size = 1

food = 3 * WIDTH + 3

DIRC_LIST = [LEFT, UP, RIGHT, DOWN]


def can_move(pos, dirc):
    if dirc == UP and pos / WIDTH > 1:
        return True
    elif dirc == LEFT and pos % WIDTH > 1:
        return True
    elif dirc == DOWN and pos / WIDTH < HEIGHT - 2:
        return True
    elif dirc == RIGHT and pos % WIDTH < WIDTH - 2:
        return True
    return False


def init_board(_snake, _size, _board):
    for i in range(HEIGHT * WIDTH):
        if i == food:
            _board[i] = FOOD
        elif not (i in _snake[:_size]):
            _board[i] = UNDEF
        else:
            _board[i] = SNAKE
    

def calc_food_dist_board(_food,_snake,_board):
    found = False
    q = [_food]
    explored = [0] * (WIDTH * HEIGHT)
    while q:
        pos = q.pop(0)
        if explored[pos] == 1:
            continue
        explored[pos] = 1
        for dirc in DIRC_LIST:
            if can_move(pos, dirc):
                if pos + dirc == _snake[0]:
                    found = True
                if _board[pos + dirc] < SNAKE:
                    if _board[pos + dirc] > _board[pos] + 1:
                        _board[pos + dirc] = _board[pos] + 1
                    if explored[pos + dirc] == 0:
                        q.append(pos + dirc)

    return found


def min_mv(_snake, _board):
    mini = SNAKE
    mv = None
    for dirc in DIRC_LIST:
        if can_move(_snake[0], dirc) and _board[_snake[0] + dirc] < mini:
            mini = _board[_snake[0] + dirc]
            mv = dirc
    return mv


def max_mv(_snake, _board):
    maxi = -1
    mv = None
    for dirc in DIRC_LIST:
        if can_move(_snake[0], dirc) and UNDEF > _board[_snake[0] + dirc] > maxi:
            maxi = _board[_snake[0] + dirc]
            mv = dirc
    return mv


def tail_available():
    global vsnake_size, vsnake, vboard, food
    vboard[vsnake[vsnake_size - 1]] = FOOD
    vboard[food] = SNAKE
    available = calc_food_dist_board(vsnake[vsnake_size - 1], vsnake, vboard)
    for dirc in DIRC_LIST:
        if can_move(vsnake[0], dirc) and vsnake[vsnake_size - 1] == vsnake[0] + dirc and vsnake_size > 3:
            available = False
    return available


def follow_tail():
    global vboard, vsnake, food, vsnake_size
    vsnake_size = snake_size
    vsnake = snake[:]
    init_board(vsnake, vsnake_size, vboard)
    vboard[vsnake[vsnake_size - 1]] = FOOD
    vboard[food] = SNAKE
    calc_food_dist_board(vsnake[vsnake_size - 1], vsnake, vboard)
    vboard[vsnake[vsnake_size - 1]] = SNAKE

    return max_mv(vsnake, vboard)


def last_op():
    global snake_size, board, snake, food
    init_board(snake, snake_size, board)
    calc_food_dist_board(food, snake, board)
    mini = SNAKE
    mv = None
    for dirc in DIRC_LIST:
        if can_move(snake[0], dirc) and board[snake[0] + dirc] < mini:
            mini = board[snake[0] + dirc]
            mv = dirc
    return mv


def mv_body(_snake, _snake_size):
    for i in range(_snake_size, 0, -1):
        _snake[i] = _snake[i - 1]


def gen_food():
    global food, snake_size
    a = False
    while not a:
        w = randint(1, WIDTH - 2)
        h = randint(1, HEIGHT - 2)
        food = h * WIDTH + w
        a = not (food in snake[:snake_size])


def r_move(_mv):
    global snake, board, snake_size
    mv_body(snake, snake_size)
    snake[HEAD] += _mv

    if snake[HEAD] == food:
        board[snake[HEAD]] = SNAKE
        snake_size += 1
        if snake_size < HEIGHT * WIDTH:
            gen_food()
    else:
        board[snake[HEAD]] = SNAKE
        board[snake[snake_size]] = UNDEF


def v_move():
    global snake, board, snake_size, vsnake, vboard, vsnake_size, food
    vsnake_size = snake_size
    vsnake = snake[:]
    vboard = board[:]
    init_board(vsnake, vsnake_size, vboard)

    eaten = False
    while not eaten:
        calc_food_dist_board(food, vsnake, vboard)
        move = min_mv(vsnake, vboard)
        mv_body(vsnake, vsnake_size)
        vsnake[HEAD] += move
        if vsnake[HEAD] == food:
            vsnake_size += 1
            init_board(vsnake, vsnake_size, vboard)
            vboard[food] = SNAKE
            eaten = True
        else:
            vboard[vsnake[HEAD]] = SNAKE
            vboard[vsnake[vsnake_size]] = UNDEF


def final_path():
    global snake, board
    v_move()
    if tail_available():
        return min_mv(snake, board)
    return follow_tail()


def run():
    while True:
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (0, 255, 0), (int(food / WIDTH) * 24, int(food % WIDTH) * 24, 24, 24))
        for i in range(HEIGHT * WIDTH):
            if board[i] == SNAKE:
                pygame.draw.rect(screen, (255, 255, 255), (int(i / WIDTH) * 24, int(i % WIDTH) * 24, 24, 24))
        init_board(snake, snake_size, board)

        # main logic:
        # find the distance from food to the head of the snake
        # if succeed:   check if the snake can reach its tail
        #               if succeed: go to the food through the minimum move
        #               if not: follow the movement of the tail
        # if not:
        #       follow the movement of the tail
        # if the snake cannot reach either the food or its tail, then move one block randomly and check again

        best_move = final_path() if calc_food_dist_board(food, snake, board) else follow_tail()
        if best_move is None:
            best_move = last_op()
        if best_move is not None:
            r_move(best_move)
        else:
            break

        pygame.display.update()


def start_screen():
    start = True
    screen.fill((0, 0, 0))
    pygame.font.init()
    menu = pygame.font.Font('techkr/TECHKR__.TTF', 160).render('Steins;Snake', True, (255, 255, 255))
    ai = pygame.font.Font('techkr/TECHKR__.TTF', 140).render('AI', True, (255, 255, 255))
    play = pygame.font.Font('techkr/TECHKR__.TTF', 80).render('Play', True, (0, 0, 0))
    screen.blit(menu, (62, 30))
    screen.blit(ai, (215, 110))
    play_button = pygame.draw.rect(screen, (255, 255, 255), (187, 300, 100, 50))
    screen.blit(play, (207, 270))

    while start:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    return
            if event.type == QUIT:
                start = False
        pygame.display.update()
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("Steins;Snake ~ El psy congroo.")
    screen = pygame.display.set_mode((480, 456))
    start_screen()
    run()


