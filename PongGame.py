import pygame

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 900,900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 120
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 200
BALL_RADIUS = 8
VEL = 7
MAX_VEL = 8
WINNING_SCORE = 3

# Font
SCORE_FONT = pygame.font.SysFont("arial", 100)
pygame.display.set_caption("Pong Game")

class Paddle:
    COLOR = WHITE

    def __init__(self, x, y):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        self.y += -VEL if up else VEL 
        self.y = max(0, min(self.y, HEIGHT - self.height))  # Prevent moving out of bounds

    def reset(self):
        self.x, self.y = self.original_x, self.original_y


class Ball:
    COLOR = WHITE

    def __init__(self, x, y):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = BALL_RADIUS
        self.x_vel = MAX_VEL
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x, self.y = self.original_x, self.original_y
        self.y_vel = 0
        self.x_vel *= -1  #Change direction on reset


def draw(win, paddles, ball, l_score, r_score):
    win.fill(BLACK)

    # Render scores
    l_score_text = SCORE_FONT.render(str(l_score), True, WHITE)
    r_score_text = SCORE_FONT.render(str(r_score), True, WHITE)

    win.blit(l_score_text, (WIDTH // 4 - l_score_text.get_width() // 2, 20))
    win.blit(r_score_text, (WIDTH * 3 // 4 - r_score_text.get_width() // 2, 20))

    # Draw paddles and ball
    for paddle in paddles:
        paddle.draw(win)
    ball.draw(win)

    # Draw centerline
    for i in range(10, HEIGHT, HEIGHT // 20 * 2):
        pygame.draw.rect(win, WHITE, (WIDTH // 2 - 5, i, 10, HEIGHT // 20))

    pygame.display.update()


def handle_collision(ball, left_paddle, right_paddle):
    # Ball bouncing off the top and bottom
    if ball.y + ball.radius >= HEIGHT or ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    # Ball collision with paddles
    if ball.x_vel < 0:  # Left paddle
        if left_paddle.y <= ball.y <= left_paddle.y + left_paddle.height and \
           ball.x - ball.radius <= left_paddle.x + left_paddle.width:
            ball.x_vel *= -1
            ball.y_vel = (left_paddle.y + left_paddle.height / 2 - ball.y) / (PADDLE_HEIGHT / 2) * MAX_VEL

    else:  # Right paddle
        if right_paddle.y <= ball.y <= right_paddle.y + right_paddle.height and \
           ball.x + ball.radius >= right_paddle.x:
            ball.x_vel *= -1
            ball.y_vel = (right_paddle.y + right_paddle.height / 2 - ball.y) / (PADDLE_HEIGHT / 2) * MAX_VEL


def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w]:
        left_paddle.move(up=True)
    if keys[pygame.K_s]:
        left_paddle.move(up=False)
    if keys[pygame.K_UP]:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN]:
        right_paddle.move(up=False)


def main():
    run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    ball = Ball(WIDTH // 2, HEIGHT // 2)

    l_score, r_score = 0, 0

    while run:
        clock.tick(FPS)
        draw(WIN, [left_paddle, right_paddle], ball, l_score, r_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)
        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        # Score Handling
        if ball.x < 0:  # Right player scores
            r_score += 1
            ball.reset()
        elif ball.x > WIDTH:  # Left player scores
            l_score += 1
            ball.reset()

        # Check for winner
        if l_score >= WINNING_SCORE or r_score >= WINNING_SCORE:
            win_text = "Left Player Wins!" if l_score >= WINNING_SCORE else "Right Player Wins!"
            text = SCORE_FONT.render(win_text, True, WHITE)
            WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(3000)  # Shorter delay
            left_paddle.reset()
            right_paddle.reset()
            ball.reset()
            l_score, r_score = 0, 0  # Reset scores

    pygame.quit()


if __name__ == "__main__":
    main()
