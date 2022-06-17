from classes import Player
from settings import *
import pygame
pygame.init()


# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Colors
WHITE, BLACK = (255, 255, 255), (0, 0, 0)


# Game class
class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()

        self.player = Player(WIDTH*(1/6))
        self.opponent = Player(WIDTH*(5/6))

    def draw_welcome(self):
        screen.fill(BLACK)
        pygame.display.flip()

    def draw(self):
        screen.fill(BLACK)

        self.player.draw(screen)
        self.opponent.draw(screen)

        pygame.display.flip()

    def run(self): 
        # Main Loop
        running = True
        is_started = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN and not is_started:
                    is_started = True

            if not is_started:
                self.draw_welcome()
                continue

            self.draw()


game = Game()
game.run()
