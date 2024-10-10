import random

# Harita ayarları
GRID_SIZE = 20
GRID_WIDTH = 40
GRID_HEIGHT = 30
SCREEN_WIDTH = GRID_WIDTH * GRID_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * GRID_SIZE

def generate_environment():
    environment = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    # Engelleri ekler
    for _ in range(100):
        r = random.randint(0, GRID_HEIGHT - 1)
        c = random.randint(0, GRID_WIDTH - 1)
        environment[r][c] = 1

    return environment
