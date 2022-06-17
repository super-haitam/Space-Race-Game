from settings import *
import pygame


class Player:
    def __init__(self, x):
        image = pygame.image.load("assets/spaceship.png")
        ratio = image.get_width()/image.get_height()
        width = WIDTH/10
        
        self.image = pygame.transform.scale(image, (width, width * ratio))
        self.rect = self.image.get_rect(centerx=x, y=HEIGHT*(4/5))

        self.speed = 2

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

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
