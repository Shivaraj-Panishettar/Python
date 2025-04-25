import pygame
import sys
from level_manager import load_level
from entities import Player

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Modular Platformer")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

def game_loop():
    level_number = 1
    running = True

    while running:
        result = load_level(level_number)
        if not result:
            win_screen()
            return
        platform_list, coin_list, enemy_list = result

        platforms = pygame.sprite.Group(platform_list)
        coins = pygame.sprite.Group(coin_list)
        enemies = pygame.sprite.Group(enemy_list)
        player = Player(platforms)

        while True:
            clock.tick(60)
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if not player.alive and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    return game_loop()

            if player.alive:
                player.update(keys, coins, enemies)
                enemies.update()

            if len(coins) == 0:
                # Level complete
                msg = font.render(f"Level {level_number} Complete!", True, (0, 200, 0))
                screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, SCREEN_HEIGHT // 2))
                pygame.display.flip()
                pygame.time.delay(1500)

                level_number += 1
                break

            screen.fill(WHITE)
            platforms.draw(screen)
            coins.draw(screen)
            enemies.draw(screen)
            screen.blit(player.image, player.rect)

            score = font.render(f"Coins: {player.score}", True, BLACK)
            lives = font.render(f"Lives: {player.lives}", True, BLACK)
            screen.blit(score, (10, 10))
            screen.blit(lives, (10, 40))

            if not player.alive:
                over = font.render("Game Over! Press R to Restart", True, (255, 0, 0))
                screen.blit(over, (SCREEN_WIDTH // 2 - over.get_width() // 2, SCREEN_HEIGHT // 2))

            pygame.display.flip()

            # Reset lives for new level
            if len(coins) == 0:
                player.lives = 3

def win_screen():
    screen.fill(WHITE)
    win_text = font.render("You Win! Thanks for playing!", True, (0, 200, 0))
    screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    pygame.time.delay(3000)

def main_menu():
    screen.fill(WHITE)
    title = font.render("Modular Platformer", True, BLACK)
    prompt = font.render("Press SPACE to Start", True, BLACK)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 200))
    screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 260))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

main_menu()
game_loop()

