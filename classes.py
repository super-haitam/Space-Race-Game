from settings import *
import pygame
import random
import time


class SpaceShip:
    def __init__(self, x, color_name, color: tuple, name: str):
        image = pygame.image.load(f"assets/{color_name}spaceship.png")
        ratio = image.get_width()/image.get_height()
        width = WIDTH/10
        
        self.image = pygame.transform.scale(image, (width, width * ratio))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(centerx=x, y=init_y)

        self.speed = 2
        self.score = 0
        self.color = color
        self.name = name

    def reset_pos(self):
        self.rect.y = init_y

    def handle_crossing_line(self):
        if self.rect.midbottom[1] <= 0:
            self.score += 1
            self.reset_pos()

    def draw(self, screen):
        font = pygame.font.SysFont("comicsans", 50)
        score_txt = font.render(str(self.score), True, PSEUDO_WHITE)
        screen.blit(score_txt, (self.rect.centerx-score_txt.get_width()/2, 
                                    (HEIGHT + self.rect.midbottom[1])/2 - score_txt.get_height()/2))

        screen.blit(self.image, self.rect.topleft)


class Player(SpaceShip):
    def __init__(self, x, color_name):
        super().__init__(x, color_name, RED, "Player1")

    def handle_movement(self, up_key: str, down_key: str):
        dictionary = {"up": pygame.K_UP, "down": pygame.K_DOWN, 
                      'w': pygame.K_w, 's': pygame.K_s}

        pressed = pygame.key.get_pressed()
        
        if pressed[dictionary[up_key]]:
            self.rect.y -= self.speed
        elif pressed[dictionary[down_key]]:
            self.rect.y += self.speed

        # So that it doesn't go off screen by bottom
        self.rect.y = min(self.rect.midbottom[1], HEIGHT) - self.rect.h

        self.handle_crossing_line()


class AI_Opponent(SpaceShip):
    def __init__(self, x, color_name):
        super().__init__(x, color_name, BLUE, "Player2")

    def move(self):
        self.rect.y -= self.speed

        self.handle_crossing_line()


class Bullet:
    def __init__(self):
        image = pygame.image.load("assets/bullet.png")
        size = WIDTH/25

        self.image = pygame.transform.scale(image, (size, size))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        
        self.speed = 3

        self.spawn()

    def spawn(self):
        # "left" * 3 and "right" * 1 Cuz before there were only ~4 balls going left
        #  without appearent explication giving the advantage to one of the spaceships
        self.direction = random.choice(["left", "right", "left", "left"])

        if self.direction == "right":
            self.rect.x = -1 * random.randint(0, 600)
        elif self.direction == "left":
            self.rect.x = WIDTH + random.randint(0, 600)

        self.rect.y = random.randrange(init_y - self.rect.h)

    def move(self):
        if self.direction == "right":
            self.rect.x += self.speed
        elif self.direction == "left":
            self.rect.x -= self.speed

        if self.rect.topright[0] < 0 or WIDTH < self.rect.x:
            self.spawn()

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)


class TimerBar:
    def __init__(self, duration):
        self.duration = duration
        self.start_time = time.time()

        self.rect = pygame.Rect([0, 0, WIDTH/40, HEIGHT])
        self.rect.x = WIDTH/2 - self.rect.w/2

    def run(self):
        dt = time.time() - self.start_time

        self.rect.h = HEIGHT * (self.duration-dt) / self.duration
        self.rect.y = HEIGHT - self.rect.h

    def draw(self, screen):
        pygame.draw.rect(screen, PSEUDO_WHITE, self.rect)
