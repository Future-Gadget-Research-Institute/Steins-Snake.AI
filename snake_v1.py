import pygame
from pygame.locals import *
import random, sys


screen_width = 480
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
R, L, U, D = 1, 2, 3, 4


def body_grows(snake):
    new = (0, 0)
    if dirc == R:
        new = (snake[0][0] + 1, snake[0][1])
    elif dirc == L:
        new = (snake[0][0] - 1, snake[0][1])
    elif dirc == U:
        new = (snake[0][0], snake[0][1] - 1)
    elif dirc == D:
        new = (snake[0][0], snake[0][1] + 1)
    snake.insert(0, new)


def food(snake):
    available_pos = []
    for i in range(int(screen_width / 20)):
        for j in range(int(screen_height / 20)):
            if (i, j) not in snake:
                available_pos.append((i, j))
    return random.choice(available_pos)


def dead(snake):
    if snake[0][0] not in range(int(screen_width / 20 + 1)) or \
        snake[0][1] not in range(int(screen_height / 20 + 1))or \
            snake[0] in snake[1:]:
        return True
    return False


def run():
    global dirc
    x, y = 10, 7
    snake = [(x, y), (x - 1, y), (x - 2, y)]
    dirc = R
    running = True
    food_pos = food(snake)
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == K_UP and dirc in (R, L):
                    dirc = U
                if event.key == K_DOWN and dirc in (R, L):
                    dirc = D
                if event.key == K_RIGHT and dirc in (U, D):
                    dirc = R
                if event.key == K_LEFT and dirc in (U, D):
                    dirc = L
        body_grows(snake)
        screen.fill(BLACK)
        draw_food(screen, food_pos)
        if snake[0] == food_pos:
            a, b = food_pos
            pygame.draw.rect(screen, BLACK, (a * 20, b * 20, 20, 20))
            food_pos = food(snake)
            draw_food(screen, food_pos)
        else:
            del snake[-1]
        if dead(snake):
            return
        draw_snake(screen, snake)
        draw_score(screen, snake)
        pygame.display.update()
        pygame.time.Clock().tick(20)
    pygame.quit()
    sys.exit()


def draw_snake(screen, snake):
    for square in snake:
        pygame.draw.rect(screen, WHITE, (square[0] * 20, square[1] * 20, 20, 20))


def draw_food(screen, food_pos):
    a, b = food_pos
    pygame.draw.rect(screen, WHITE, (a * 20, b * 20, 20, 20))


def draw_score(screen, snake):
    global score
    score = len(snake) - 3
    s = pygame.font.Font('techkr/TECHKR__.TTF', 45).render('Score: %s' % score, True, WHITE)
    screen.blit(s, (550, 10))


def startScreen():
    start = True
    screen.fill(BLACK)
    pygame.font.init()
    menu = pygame.font.Font('techkr/TECHKR__.TTF', 190).render('Snake', True, WHITE)
    play = pygame.font.Font('techkr/TECHKR__.TTF', 80).render('Play', True, BLACK)
    screen.blit(menu, (215, 30))
    play_button = pygame.draw.rect(screen, WHITE, (270, 300, 100, 50))
    screen.blit(play, (290, 270))

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
    game_over = pygame.font.Font('techkr/TECHKR__.TTF', 190).render('Game Over', True, WHITE)
    str_score = pygame.font.Font('techkr/TECHKR__.TTF', 80).render('Score: %s' % score, True, WHITE)
    exiit = pygame.font.Font('techkr/TECHKR__.TTF', 80).render('Exit', True, BLACK)
    back = pygame.font.Font('techkr/TECHKR__.TTF',35).render('Back to Menu', True, BLACK)
    screen.blit(game_over, (140, 30))
    screen.blit(str_score, (260, 180))
    exit_button = pygame.draw.rect(screen, WHITE, (140, 300, 100, 50))
    back_button = pygame.draw.rect(screen, WHITE, (400, 300, 100, 50))
    screen.blit(exiit, (163, 270))
    screen.blit(back, (410, 300))

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


def main():
    pygame.init()
    pygame.display.set_caption("SNAKE")

    while True:
        startScreen()
        run()
        gg_screen()


if __name__ == '__main__':
    main()
