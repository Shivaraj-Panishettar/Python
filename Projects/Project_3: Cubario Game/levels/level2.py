from entities import Platform, Coin, Enemy

def create():
    platforms = [
        Platform(0, 580, 800, 20),
        Platform(100, 480, 150, 20),
        Platform(300, 400, 150, 20),
        Platform(550, 320, 200, 20),
        Platform(350, 200, 150, 20)
    ]

    coins = [
        Coin(125, 440),
        Coin(325, 360),
        Coin(600, 280),
        Coin(400, 160),
        Coin(720, 540)
    ]

    enemies = [
        # Make sure enemies are above platforms
        Enemy(120, 450, 100, 250),
        Enemy(300, 370, 300, 450),
        Enemy(550, 290, 550, 750)
    ]
    
    return platforms, coins, enemies

