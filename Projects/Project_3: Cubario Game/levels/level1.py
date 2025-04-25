from entities import Platform, Coin, Enemy

def create():
    platforms = [
        Platform(0, 580, 800, 20),
        Platform(150, 450, 200, 20),
        Platform(400, 350, 150, 20),
        Platform(600, 250, 150, 20),
    ]
    coins = [
        Coin(200, 410), Coin(450, 310),
        Coin(650, 210), Coin(100, 540)
    ]
    enemies = [
        Enemy(200, 450, 150, 350),
        Enemy(420, 350, 400, 550)
    ]
    return platforms, coins, enemies

