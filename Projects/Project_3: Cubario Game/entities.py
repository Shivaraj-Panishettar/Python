import pygame

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 223, 0)
RED = (255, 0, 0)
GRAVITY = 0.8
JUMP_STRENGTH = -15
SCREEN_WIDTH = 800

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=(x, y))

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, YELLOW, (10, 10), 10)
        self.rect = self.image.get_rect(center=(x, y))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, left_bound, right_bound):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 0, 0))  # Color red for visibility
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.direction = 1
        self.speed = 2

    def update(self):
        # Print the position of each enemy to debug
        print(f"Enemy Position: {self.rect.x}, {self.rect.y}")

        self.rect.x += self.direction * self.speed
        if self.rect.left <= self.left_bound or self.rect.right >= self.right_bound:
            self.direction *= -1



class Player(pygame.sprite.Sprite):
    def __init__(self, platforms):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.vel_y = 0
        self.score = 0
        self.lives = 3
        self.alive = True
        self.platforms = platforms
        self.on_ground = False
        self.start()

    def start(self):
        self.rect.x = 100
        self.rect.bottom = self.platforms.sprites()[0].rect.top
        self.vel_y = 0

    def reset_position(self):
        self.start()

    def update(self, keys, coins, enemies):
        if not self.alive:
            return

        dx = 0
        if keys[pygame.K_LEFT]:
            dx = -5
        if keys[pygame.K_RIGHT]:
            dx = 5
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = JUMP_STRENGTH
            self.on_ground = False

        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        self.on_ground = False
        for platform in self.platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y >= 0 and self.rect.bottom <= platform.rect.bottom:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True

        self.rect.x += dx
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(SCREEN_WIDTH, self.rect.right)

        collected = pygame.sprite.spritecollide(self, coins, True)
        self.score += len(collected)

        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                if self.vel_y > 0 and self.rect.bottom <= enemy.rect.centery:
                    enemy.kill()
                    self.vel_y = JUMP_STRENGTH / 2
                else:
                    self.lives -= 1
                    if self.lives <= 0:
                        self.alive = False
                    self.reset_position()
                    break

