import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker - Toty Fruity")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
COLORS = [RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE]

# Fonts
font = pygame.font.SysFont("comicsans", 40)
small_font = pygame.font.SysFont("comicsans", 30)

# Game variables
clock = pygame.time.Clock()


# High score
def load_high_score():
    try:
        with open("highscore.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0


def save_high_score(score):
    with open("highscore.txt", "w") as file:
        file.write(str(score))


high_score = load_high_score()


def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def draw_button(text, font, color, x, y, width, height):
    pygame.draw.rect(screen, color, (x, y, width, height))
    draw_text(text, font, WHITE, x + 10, y + 10)


def main_menu():
    global high_score
    while True:
        screen.fill((30, 30, 30))  # Dark background
        draw_text("Brick Breaker", font, WHITE, WIDTH // 2 - 120, 50)
        draw_text("Created by Toty Fruity", small_font, WHITE,
                  WIDTH // 2 - 120, 100)
        draw_text(f"High Score: {high_score}", small_font, WHITE,
                  WIDTH // 2 - 80, 150)

        # Single Player button
        single_player_button = pygame.Rect(WIDTH // 2 - 100, 250, 200, 50)
        draw_button("Single Player", small_font, GREEN, single_player_button.x,
                    single_player_button.y, single_player_button.width,
                    single_player_button.height)

        # Player vs Computer button
        vs_computer_button = pygame.Rect(WIDTH // 2 - 100, 350, 200, 50)
        draw_button("Player vs Computer", small_font, BLUE,
                    vs_computer_button.x, vs_computer_button.y,
                    vs_computer_button.width, vs_computer_button.height)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if single_player_button.collidepoint(mouse_pos):
                    score = single_player()
                    if score > high_score:
                        high_score = score
                        save_high_score(high_score)
                elif vs_computer_button.collidepoint(mouse_pos):
                    player_vs_computer()


def single_player():
    # Paddle
    paddle_width, paddle_height = 100, 20
    paddle_x = (WIDTH - paddle_width) // 2
    paddle_y = HEIGHT - 50
    paddle_speed = 8

    # Ball
    ball_radius = 10
    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2
    ball_speed_x = 5 * random.choice([-1, 1])
    ball_speed_y = -5

    # Bricks
    brick_width, brick_height = 75, 30
    brick_rows = 5
    brick_cols = WIDTH // brick_width
    bricks = []
    for row in range(brick_rows):
        for col in range(brick_cols):
            brick_color = random.choice(COLORS)
            brick = pygame.Rect(col * brick_width, row * brick_height + 50,
                                brick_width, brick_height)
            bricks.append((brick, brick_color))

    # Game variables
    score = 0
    lives = 3
    level = 1

    running = True
    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Paddle movement by mouse
        paddle_x = pygame.mouse.get_pos()[0] - paddle_width // 2
        if paddle_x < 0:
            paddle_x = 0
        if paddle_x > WIDTH - paddle_width:
            paddle_x = WIDTH - paddle_width

        # Ball movement
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Ball collision with walls
        if ball_x - ball_radius <= 0 or ball_x + ball_radius >= WIDTH:
            ball_speed_x *= -1
        if ball_y - ball_radius <= 0:
            ball_speed_y *= -1

        # Ball collision with paddle
        if paddle_x <= ball_x <= paddle_x + paddle_width and paddle_y <= ball_y + ball_radius <= paddle_y + paddle_height:
            ball_speed_y *= -1

        # Ball out of bounds (lose a life)
        if ball_y + ball_radius >= HEIGHT:
            lives -= 1
            if lives == 0:
                draw_text("Game Over!", font, WHITE, WIDTH // 2 - 80,
                          HEIGHT // 2)
                pygame.display.flip()
                pygame.time.wait(3000)
                running = False
            ball_x, ball_y = WIDTH // 2, HEIGHT // 2
            ball_speed_x = 5 * random.choice([-1, 1])
            ball_speed_y = -5

        # Ball collision with bricks
        for brick, color in bricks[:]:
            if brick.collidepoint(ball_x, ball_y):
                bricks.remove((brick, color))
                ball_speed_y *= -1
                score += 10
                break

        # Draw everything
        pygame.draw.rect(screen, WHITE,
                         (paddle_x, paddle_y, paddle_width, paddle_height))
        pygame.draw.circle(screen, WHITE, (ball_x, ball_y), ball_radius)
        for brick, color in bricks:
            pygame.draw.rect(screen, color, brick)
        draw_text(f"Score: {score}", small_font, WHITE, 10, 10)
        draw_text(f"Lives: {lives}", small_font, WHITE, WIDTH - 100, 10)
        draw_text(f"Level: {level}", small_font, WHITE, WIDTH // 2 - 40, 10)

        # Check for level completion
        if not bricks:
            level += 1
            ball_speed_x *= 1.1  # Increase ball speed
            ball_speed_y *= 1.1
            bricks = create_bricks(
                50, level)  # Generate new bricks for the next level

        pygame.display.flip()
        clock.tick(60)

    return score


def player_vs_computer():
    # Player setup
    paddle_width, paddle_height = 100, 20
    player_paddle = pygame.Rect(WIDTH // 4 - paddle_width // 2, HEIGHT - 50,
                                paddle_width, paddle_height)
    player_ball = pygame.Rect(WIDTH // 4, HEIGHT // 2, 10, 10)
    player_ball_speed = [5 * random.choice([-1, 1]), -5]
    player_bricks = create_bricks(50, 1, WIDTH // 2)
    player_score = 0
    player_lives = 3

    # Computer setup
    computer_paddle = pygame.Rect(3 * WIDTH // 4 - paddle_width // 2,
                                  HEIGHT - 50, paddle_width, paddle_height)
    computer_ball = pygame.Rect(3 * WIDTH // 4, HEIGHT // 2, 10, 10)
    computer_ball_speed = [5 * random.choice([-1, 1]), -5]
    computer_bricks = create_bricks(50, 1, WIDTH // 2, WIDTH // 2)
    computer_score = 0
    computer_lives = 3

    running = True
    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Player paddle movement by mouse
        player_paddle.x = pygame.mouse.get_pos()[0] - paddle_width // 2
        if player_paddle.x < 0:
            player_paddle.x = 0
        if player_paddle.x > WIDTH // 2 - paddle_width:
            player_paddle.x = WIDTH // 2 - paddle_width

        # Computer paddle movement (simple AI)
        if computer_ball.x > computer_paddle.x + paddle_width // 2 and computer_paddle.right < WIDTH:
            computer_paddle.x += 6
        elif computer_ball.x < computer_paddle.x + paddle_width // 2 and computer_paddle.left > WIDTH // 2:
            computer_paddle.x -= 6

        # Player ball movement
        player_ball.x += player_ball_speed[0]
        player_ball.y += player_ball_speed[1]

        # Player ball collision with walls
        if player_ball.left <= 0 or player_ball.right >= WIDTH // 2:
            player_ball_speed[0] *= -1
        if player_ball.top <= 0:
            player_ball_speed[1] *= -1

        # Player ball collision with paddle
        if player_paddle.colliderect(player_ball):
            player_ball_speed[1] *= -1

        # Player ball out of bounds (lose a life)
        if player_ball.y + 10 >= HEIGHT:
            player_lives -= 1
            if player_lives == 0:
                draw_text("Computer Wins!", font, BLUE, WIDTH // 2 - 80,
                          HEIGHT // 2)
                pygame.display.flip()
                pygame.time.wait(3000)
                running = False
            player_ball.x, player_ball.y = WIDTH // 4, HEIGHT // 2
            player_ball_speed = [5 * random.choice([-1, 1]), -5]

        # Player ball collision with bricks
        for brick, color in player_bricks[:]:
            if brick.colliderect(player_ball):
                player_bricks.remove((brick, color))
                player_ball_speed[1] *= -1
                player_score += 10
                break

        # Computer ball movement
        computer_ball.x += computer_ball_speed[0]
        computer_ball.y += computer_ball_speed[1]

        # Computer ball collision with walls
        if computer_ball.left <= WIDTH // 2 or computer_ball.right >= WIDTH:
            computer_ball_speed[0] *= -1
        if computer_ball.top <= 0:
            computer_ball_speed[1] *= -1

        # Computer ball collision with paddle
        if computer_paddle.colliderect(computer_ball):
            computer_ball_speed[1] *= -1

        # Computer ball out of bounds (lose a life)
        if computer_ball.y + 10 >= HEIGHT:
            computer_lives -= 1
            if computer_lives == 0:
                draw_text("Player Wins!", font, RED, WIDTH // 2 - 80,
                          HEIGHT // 2)
                pygame.display.flip()
                pygame.time.wait(3000)
                running = False
            computer_ball.x, computer_ball.y = 3 * WIDTH // 4, HEIGHT // 2
            computer_ball_speed = [5 * random.choice([-1, 1]), -5]

        # Computer ball collision with bricks
        for brick, color in computer_bricks[:]:
            if brick.colliderect(computer_ball):
                computer_bricks.remove((brick, color))
                computer_ball_speed[1] *= -1
                computer_score += 10
                break

        # Draw split-screen line
        pygame.draw.line(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT),
                         2)

        # Draw player area
        pygame.draw.rect(screen, RED, player_paddle)
        pygame.draw.circle(screen, RED, (player_ball.x, player_ball.y), 10)
        for brick, color in player_bricks:
            pygame.draw.rect(screen, color, brick)
        draw_text(f"Player: {player_score}", small_font, RED, 10, 10)
        draw_text(f"Lives: {player_lives}", small_font, RED, WIDTH // 4 - 50,
                  10)

        # Draw computer area
        pygame.draw.rect(screen, BLUE, computer_paddle)
        pygame.draw.circle(screen, BLUE, (computer_ball.x, computer_ball.y),
                           10)
        for brick, color in computer_bricks:
            pygame.draw.rect(screen, color, brick)
        draw_text(f"Computer: {computer_score}", small_font, BLUE,
                  WIDTH // 2 + 10, 10)
        draw_text(f"Lives: {computer_lives}", small_font, BLUE,
                  3 * WIDTH // 4 - 50, 10)

        # Check for win conditions
        if not player_bricks:
            draw_text("Player Wins!", font, RED, WIDTH // 2 - 80, HEIGHT // 2)
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False
        if not computer_bricks:
            draw_text("Computer Wins!", font, BLUE, WIDTH // 2 - 80,
                      HEIGHT // 2)
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False

        pygame.display.flip()
        clock.tick(60)


def create_bricks(y_offset, level=1, width=WIDTH, x_offset=0):
    bricks = []
    brick_width, brick_height = 75, 30
    brick_rows = 3 + level  # Increase rows with level
    brick_cols = width // brick_width
    for row in range(brick_rows):
        for col in range(brick_cols):
            brick_color = random.choice(COLORS)
            brick = pygame.Rect(x_offset + col * brick_width,
                                row * brick_height + y_offset, brick_width,
                                brick_height)
            bricks.append((brick, brick_color))
    return bricks


# Run the main menu
main_menu()
pygame.quit()
