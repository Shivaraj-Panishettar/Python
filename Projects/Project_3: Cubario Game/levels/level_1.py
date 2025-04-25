from entities import Platform, Coin, Enemy

def create():
    platforms = [
        Platform(0, 580, 800, 20),    # Bottom platform at y=580
        Platform(150, 450, 200, 20),  # Platform at y=450
        Platform(400, 350, 150, 20),  # Platform at y=350
        Platform(600, 250, 150, 20),  # Platform at y=250
    ]
    
    coins = [
        Coin(200, 410), Coin(450, 310),
        Coin(650, 210), Coin(100, 540)
    ]
    
    enemies = [
        Enemy(200, 420, 150, 400),  # Enemy just above platform at y=420
        Enemy(420, 310, 400, 450),  # Enemy just above platform at y=310
    ]
    
    return platforms, coins, enemies

