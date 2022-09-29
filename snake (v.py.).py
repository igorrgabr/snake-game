import pygame, random
from pygame.locals import *

WINDOW_SIZE = (600, 600)
PIXEL_SIZE = 10

def collision(pos1, pos2):
    return (pos1[0] == pos2[0]) and (pos1[1] == pos2[1])

def random_on_grid():
    x = random.randint(0, 59)
    y = random.randint(0, 59)
    return (x * 10, y * 10)

def restart_game():
    global snake_pos
    global apple_pos
    global snake_direction
    global score
    global game_over
    snake_pos = [(200, 200), (210, 200), (220, 200)]
    snake_direction = LEFT
    apple_pos = random_on_grid()
    score = 0
    game_over = False

def gameover():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    return True

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Jogo da Cobrinha ~by Igu')

snake_pos = [(200, 200), (210, 200), (220, 200)]
snake_surface = pygame.Surface((PIXEL_SIZE, PIXEL_SIZE))
snake_surface.fill((0, 255, 0))

apple_surface = pygame.Surface((PIXEL_SIZE, PIXEL_SIZE))
apple_surface.fill((255, 0, 0))
apple_pos = random_on_grid()

snake_direction = LEFT
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 18)
score = 0
record = []
game_over = False

while True:
    clock.tick(15)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
            
        if event.type == KEYDOWN:
            if event.key == K_UP and snake_direction != DOWN:
                snake_direction = UP
            if event.key == K_DOWN and snake_direction != UP:
                snake_direction = DOWN
            if event.key == K_RIGHT and snake_direction != LEFT:
                snake_direction = RIGHT
            if event.key == K_LEFT and snake_direction != RIGHT:
                snake_direction = LEFT

    if collision(snake_pos[0], apple_pos):
        snake_pos.append((0, 0))
        apple_pos = random_on_grid()
        score += 1

    if snake_pos[0][0] == 600 or snake_pos[0][1] == 600 or snake_pos[0][0] < 0 or snake_pos[0][1] < 0:
        game_over = True

    for i in range(1, len(snake_pos) - 1):
        if snake_pos[0][0] == snake_pos[i][0] and snake_pos[0][1] == snake_pos[i][1]:
            game_over = True

    for i in range(len(snake_pos) - 1, 0, -1):
        snake_pos[i] = (snake_pos[i-1][0], snake_pos[i-1][1])

    if snake_direction == UP:
        snake_pos[0] = (snake_pos[0][0], snake_pos[0][1] - PIXEL_SIZE)
    elif snake_direction == DOWN:
        snake_pos[0] = (snake_pos[0][0], snake_pos[0][1] + PIXEL_SIZE)
    elif snake_direction == LEFT:
        snake_pos[0] = (snake_pos[0][0] - PIXEL_SIZE, snake_pos[0][1])
    elif snake_direction == RIGHT:
        snake_pos[0] = (snake_pos[0][0] + PIXEL_SIZE, snake_pos[0][1])

    screen.fill((0, 0, 0))
    screen.blit(apple_surface, apple_pos)

    for x in range(0, 600, PIXEL_SIZE):
        pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, 600))
    for y in range(0, 600, PIXEL_SIZE):
        pygame.draw.line(screen, (40, 40, 40), (0, y), (600, y))

    score_font = font.render(f'Score: {score}', True, (255, 255, 255))
    score_rect = score_font.get_rect()
    score_rect.topleft = (WINDOW_SIZE[0] - 120, PIXEL_SIZE)
    screen.blit(score_font, score_rect)
    record.append(score)

    for pos in snake_pos:
            screen.blit(snake_surface, pos)

    pygame.display.update()

    if game_over:
        game_over_font = pygame.font.Font('freesansbold.ttf', 70)
        game_over_screen = game_over_font.render('Game Over!', True, (255, 255, 255))
        game_over_rect = game_over_screen.get_rect(center=(WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2 - 25))
        screen.blit(game_over_screen, game_over_rect)
    
        message_font = pygame.font.Font('freesansbold.ttf', 20)
        message_screen = message_font.render('Press SPACE to try again.', True, (255, 255, 255))
        message_rect = message_screen.get_rect(center=(WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2 + 25))
        screen.blit(message_screen, message_rect)

        record_font = pygame.font.Font('freesansbold.ttf', 15)
        record_screen = record_font.render(f'Record: {max(record)}', True, (255, 255, 255))
        record_rect = record_screen.get_rect(center=(WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2 + 50))
        screen.blit(record_screen, record_rect)
        
        pygame.display.update()

        if gameover():
            restart_game()