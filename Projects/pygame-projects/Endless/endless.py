import pygame
import random
import sys
import time
import os
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 400
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
FONT = pygame.font.SysFont('Arial', 24)

# Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Endless Runner Ball")

SPAWN_OBSTACLE = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_OBSTACLE, 1500)
LEADERBOARD_FILE = "leaderboard.txt"

# Theme
background_colors = [(255, 255, 255), (200, 200, 255), (255, 200, 200), (200, 255, 200)]
theme_change_interval = 15
current_theme_index = 0
last_theme_change_time = time.time()

class PlayerBall:
    def __init__(self):
        self.radius = 25
        self.x = 100
        self.y = HEIGHT - 60
        self.vel_y = 0
        self.is_jumping = False

    def update(self):
        self.vel_y += 0.5
        self.y += self.vel_y
        if self.y > HEIGHT - self.radius - 10:
            self.y = HEIGHT - self.radius - 10
            self.vel_y = 0
            self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.vel_y = -10
            self.is_jumping = True

    def draw(self):
        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), self.radius)

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

class Obstacle:
    def __init__(self, x, speed):
        self.x = x
        self.y = HEIGHT - 50
        self.speed = speed
        self.type = random.choice(["rect", "circle", "triangle"])
        self.size = random.randint(30, 50)

    def move(self):
        self.x -= self.speed

    def draw(self):
        if self.type == "rect":
            pygame.draw.rect(screen, BLACK, (self.x, self.y, self.size, self.size))
        elif self.type == "circle":
            pygame.draw.circle(screen, BLACK, (int(self.x + self.size/2), int(self.y + self.size/2)), self.size // 2)
        elif self.type == "triangle":
            points = [
                (self.x, self.y + self.size),
                (self.x + self.size / 2, self.y),
                (self.x + self.size, self.y + self.size)
            ]
            pygame.draw.polygon(screen, BLACK, points)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

def draw_triangles(num):
    for i in range(num):
        x = 20 + i * 30
        points = [(x, 20), (x + 10, 0), (x + 20, 20)]
        pygame.draw.polygon(screen, RED, points)

def draw_ui(name, score, lives, player, obstacles, background_color):
    screen.fill(background_color)
    player.draw()
    for obs in obstacles:
        obs.draw()

    score_text = FONT.render(f"Score: {score}", True, BLACK)
    name_text = FONT.render(f"Player: {name}", True, BLACK)
    screen.blit(score_text, (WIDTH - 150, 10))
    screen.blit(name_text, (WIDTH - 300, 10))
    draw_triangles(lives)
    pygame.display.update()

def input_name_screen():
    name = ""
    input_box = pygame.Rect(300, 170, 200, 40)
    while True:
        screen.fill(WHITE)
        prompt = FONT.render("Enter your name:", True, BLACK)
        screen.blit(prompt, (310, 130))
        pygame.draw.rect(screen, BLACK, input_box, 2)
        name_surface = FONT.render(name, True, BLACK)
        screen.blit(name_surface, (input_box.x + 5, input_box.y + 5))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name:
                    return name
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 10:
                    name += event.unicode

def save_score(name, score):
    with open(LEADERBOARD_FILE, 'a') as f:
        f.write(f"{name},{score}\n")

def show_leaderboard_and_restart():
    screen.fill(WHITE)
    title = FONT.render("Leaderboard", True, BLACK)
    screen.blit(title, (WIDTH // 2 - 60, 20))

    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, 'r') as file:
            scores = [line.strip().split(",") for line in file.readlines()]
        scores = [(name, int(score)) for name, score in scores]
        scores.sort(key=lambda x: x[1], reverse=True)
        for i, (name, score) in enumerate(scores[:5]):
            entry = FONT.render(f"{i+1}. {name} - {score}", True, BLACK)
            screen.blit(entry, (WIDTH // 2 - 80, 60 + i * 30))
    else:
        screen.blit(FONT.render("No scores yet.", True, BLACK), (WIDTH // 2 - 80, 60))

    restart_button = pygame.Rect(WIDTH // 2 - 60, 260, 120, 40)
    pygame.draw.rect(screen, GRAY, restart_button)
    restart_text = FONT.render("Restart", True, BLACK)
    screen.blit(restart_text, (restart_button.x + 20, restart_button.y + 10))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    return

def game_loop(player_name):
    global current_theme_index, last_theme_change_time
    player = PlayerBall()
    obstacles = []
    lives = 3
    score = 0
    start_time = time.time()
    base_speed = 5
    speed_variation = 3
    speed_change_interval = 10

    while True:
        clock.tick(FPS)
        elapsed_time = time.time() - start_time
        score = int(elapsed_time)
        speed = base_speed + speed_variation * math.sin(elapsed_time / speed_change_interval)

        if time.time() - last_theme_change_time > theme_change_interval:
            current_theme_index = (current_theme_index + 1) % len(background_colors)
            last_theme_change_time = time.time()

        background_color = background_colors[current_theme_index]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_score(player_name, score)
                show_leaderboard_and_restart()
                pygame.quit(); sys.exit()
            elif event.type == SPAWN_OBSTACLE:
                obstacles.append(Obstacle(WIDTH, speed))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            player.jump()

        player.update()
        for obs in obstacles:
            obs.move()

        obstacles = [obs for obs in obstacles if obs.x + obs.size > 0]

        for obs in obstacles:
            if player.get_rect().colliderect(obs.get_rect()):
                obstacles.remove(obs)
                lives -= 1
                if lives <= 0:
                    save_score(player_name, score)
                    show_leaderboard_and_restart()
                    return

        draw_ui(player_name, score, lives, player, obstacles, background_color)

# Game Start
while True:
    player_name = input_name_screen()
    game_loop(player_name)

