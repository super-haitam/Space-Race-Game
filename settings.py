import random


WIDTH, HEIGHT = 550, 630

# Initial y pos of players
init_y = int(HEIGHT*(5/6))

# Colors
random_color = lambda a, b: tuple(random.randint(a, b) for _ in range(3))

WHITE, BLACK = (255, 255, 255), (0, 0, 0)
PSEUDO_WHITE = random_color(200, 255)
RED, BLUE = (255, 0, 0), (0, 0, 255)
GREEN = (0, 255, 0)
PSEUDO_BLACK = (30, 30, 30)
