import pygame


def block_grid():
    b_list = []
    y = 80
    for _ in range(8):
        x = -70
        y += 20
        for _ in range(14):
            x += 75
            b = pygame.Rect(x, y, 70, 15)
            b_list.append(b)
    return b_list


def color_grid():
    c_list = []
    colors = ['red', 'orange', 'green', 'yellow']
    c_index = -1
    for _ in range(4):
        c_index += 1
        for _ in range(28):
            c_list.append(colors[c_index])
    return c_list


def make_paddle():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and r_paddle.x > 5:
        l_paddle.x -= paddle_v
        r_paddle.x -= paddle_v
    if keys[pygame.K_RIGHT] and l_paddle.x < 1050 - r_paddle.width:
        r_paddle.x += paddle_v
        l_paddle.x += paddle_v
    pygame.draw.rect(surface=screen, color='blue', rect=l_paddle)
    pygame.draw.rect(surface=screen, color='blue', rect=r_paddle)


SCR_HEIGHT = 720
SCR_WIDTH = 1055

pygame.init()
screen = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
pygame.display.set_caption('Breakout!')
clock = pygame.time.Clock()
run = True
dt = 0

block_list = block_grid()
color_list = color_grid()

l_paddle = pygame.Rect(460, 660, 75, 10)
r_paddle = pygame.Rect(385, 660, 75, 10)
paddle_v = 5

ball_x = 450
ball_y = 600
ball_r = 7
ball_vx = 4
ball_vy = 4
ball_rect = pygame.Rect(ball_x - ball_r, ball_y - ball_r, 2 * ball_r, 2 * ball_r)

font = pygame.font.SysFont('arial', 35)
score = 0


while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill((0, 0, 0))

    score_text = font.render(f'Points: {score}', False, 'white')
    screen.blit(score_text, (SCR_WIDTH / 2, 20))

    make_paddle()

    ball_x -= ball_vx
    ball_y -= ball_vy
    ball = pygame.draw.circle(screen, 'white', (round(ball_x), round(ball_y)), ball_r)

    for block in block_list:
        color_index = block_list.index(block)
        pygame.draw.rect(screen, color_list[color_index], block)

    for block in block_list:
        if pygame.Rect.colliderect(ball, block):
            ball_vy *= -1
            remove_index = block_list.index(block)
            block_list.remove(block)

            if color_list[remove_index] == 'red':
                score += 7
            elif color_list[remove_index] == 'orange':
                score += 5
            elif color_list[remove_index] == 'green':
                score += 3
            elif color_list[remove_index] == 'yellow':
                score += 1
            del color_list[remove_index]

    if ball.y > 800:
        pygame.Rect.move(ball, (450, 600))
    if ball.x <= 0:
        ball_vx *= -1
    if ball.x + ball.width >= SCR_WIDTH:
        ball_vx *= -1
    if ball.y <= 0:
        ball_vy *= -1

    if pygame.Rect.colliderect(ball, l_paddle):
        ball_vy *= -1
    if pygame.Rect.colliderect(ball, l_paddle) and ball_vx > 0:
        ball_vx *= -1
    if pygame.Rect.colliderect(ball, r_paddle):
        ball_vy *= -1
    if pygame.Rect.colliderect(ball, r_paddle) and ball_vx < 0:
        ball_vx *= -1

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
