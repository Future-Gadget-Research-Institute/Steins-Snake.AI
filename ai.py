from random import randint
import pygame
from pygame.locals import *
import sys


HEIGHT = 20
WIDTH = 20


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

FOOD = 0
UNDEF = int(1E3)
SNAKE = int(1E6)

LEFT = -1
RIGHT = 1
UP = -WIDTH
DOWN = WIDTH


board = [0] * HEIGHT * WIDTH                # use one dimensional list to represent 2 dimensional board
snake = [0] * (HEIGHT * WIDTH+1)
snake[0] = 1*WIDTH+1
snake_size = score = 1

vboard = [0] * HEIGHT * WIDTH
vsnake = [0] * (HEIGHT * WIDTH+1)
vsnake[0] = 1*WIDTH+1
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
    

def calc_food_dist_board(_food,_snake,_board):              # BFS
    found = False
    q = [_food]                                             # not using Queue() because it is slower
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
    global snake, board, snake_size, score
    mv_body(snake, snake_size)
    snake[0] += _mv

    if snake[0] == food:
        board[snake[0]] = SNAKE
        snake_size += 1
        score += 1
        if snake_size < HEIGHT * WIDTH:
            gen_food()
    else:
        board[snake[0]] = SNAKE
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
        vsnake[0] += move
        if vsnake[0] == food:
            vsnake_size += 1
            init_board(vsnake, vsnake_size, vboard)
            vboard[food] = SNAKE
            eaten = True
        else:
            vboard[vsnake[0]] = SNAKE
            vboard[vsnake[vsnake_size]] = UNDEF


def final_path():
    global snake, board
    v_move()
    if tail_available():
        return min_mv(snake, board)
    return follow_tail()


def run():
    while True:
        screen.fill(BLACK)
        pygame.draw.rect(screen, GREEN, (int(food / WIDTH) * 24, int(food % WIDTH) * 24, 24, 24))
        for i in range(HEIGHT * WIDTH):
            if board[i] == SNAKE:
                pygame.draw.rect(screen, WHITE, (int(i / WIDTH) * 24, int(i % WIDTH) * 24, 24, 24))
        init_board(snake, snake_size, board)

        # main logic:
        # find the distance from food to the 0 of the snake
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
    screen.fill(BLACK)
    pygame.font.init()
    menu = pygame.font.Font('techkr/TECHKR__.TTF', 160).render('Steins;Snake', True, WHITE)
    ai = pygame.font.Font('techkr/TECHKR__.TTF', 140).render('AI', True, WHITE)
    play = pygame.font.Font('techkr/TECHKR__.TTF', 80).render('Play', True, BLACK)
    screen.blit(menu, (62, 30))
    screen.blit(ai, (215, 110))
    play_button = pygame.draw.rect(screen, WHITE, (187, 300, 100, 50))
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

def gg_screen():
    gg = True
    screen.fill(BLACK)
    pygame.font.init()
    gameOver = pygame.font.Font('techkr/TECHKR__.TTF', 190).render('Game Over', True, WHITE)
    str_score = pygame.font.Font('techkr/TECHKR__.TTF', 80).render('Score: %s' % score, True, WHITE)
    exiit = pygame.font.Font('techkr/TECHKR__.TTF', 80).render('Exit', True, BLACK)
    back = pygame.font.Font('techkr/TECHKR__.TTF',35).render('Back to Menu', True, BLACK)
    screen.blit(gameOver, (60, 30))
    screen.blit(str_score, (190, 180))
    exit_button = pygame.draw.rect(screen, WHITE, (90, 300, 100, 50))
    back_button = pygame.draw.rect(screen, WHITE, (300, 300, 100, 50))
    screen.blit(exiit, (114, 270))
    screen.blit(back, (310, 300))

    while gg:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return
                if exit_button.collidepoint(event.pos):
                    gg = False
            if event.type == QUIT:
                gg = False
        pygame.display.update()
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("Steins;Snake ~ El psy congroo.")
    screen = pygame.display.set_mode((480, 456))
    while True:
        start_screen()
        run()
        gg_screen()
