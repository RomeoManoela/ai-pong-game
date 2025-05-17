import pygame

pygame.init()

HEIGHT, WIDTH = 600, 800
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BALL_RADIUS = 20
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
WINNING_SCORE = 5
SCORE_FONT = pygame.font.SysFont("comicsans", 50)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")


def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    if ball.y - ball.radius <= 0:
        ball.y_vel *= -1
    if ball.x_vel < 0:
        if left_paddle.y <= ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel
    else:
        if right_paddle.y <= ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel


def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_z] and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.move(up=True)
    if (
        keys[pygame.K_w]
        and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT
    ):
        left_paddle.move(up=False)
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up=True)
    if (
        keys[pygame.K_DOWN]
        and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT
    ):
        right_paddle.move(up=False)


class Paddle:
    COLOR = WHITE
    VEL = 4

    def __init__(self, x, y, height, width):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.height = height
        self.width = width

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y


class Ball:
    MAX_VEL = 5
    COLOR = WHITE

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.x_vel *= -1
        self.y_vel = 0


def draw(win, paddles, ball, left_score, right_score):
    win.fill(BLACK)
    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
    win.blit(left_score_text, (WIDTH // 4 - left_score_text.get_width() // 2, 20))
    win.blit(
        right_score_text,
        (WIDTH * (3 / 4) - right_score_text.get_width() // 2, 20),
    )
    pygame.draw.line(win, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))
    ball.draw(win)
    for paddle in paddles:
        paddle.draw(win)
    pygame.display.update()


def main():
    is_running = True
    left_score = 0
    right_score = 0
    left_paddle = Paddle(
        10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_HEIGHT, PADDLE_WIDTH
    )
    right_paddle = Paddle(
        WIDTH - 10 - PADDLE_WIDTH,
        HEIGHT // 2 - PADDLE_HEIGHT // 2,
        PADDLE_HEIGHT,
        PADDLE_WIDTH,
    )
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)
    clock = pygame.time.Clock()

    while is_running:
        clock.tick(FPS)
        draw(WIN, (left_paddle, right_paddle), ball, left_score, right_score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                break
        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)
        ball.move()
        handle_collision(ball, left_paddle, right_paddle)
        if ball.x < 0:
            right_score += 1
            ball.reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()

        won = False
        win_text = ""
        if left_score >= WINNING_SCORE:
            won = True
            win_text = "Left Player Won!"
        elif right_score >= WINNING_SCORE:
            won = True
            win_text = "Right Player Won!"

        if won:
            text = SCORE_FONT.render(win_text, 1, WHITE)
            WIN.blit(
                text,
                (
                    WIDTH // 2 - text.get_width() // 2,
                    HEIGHT // 2 - text.get_height() // 2,
                ),
            )
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0
    pygame.quit()


if __name__ == "__main__":
    main()
