from classes import Player, AI_Opponent, Bullet, TimerBar
from settings import *
import pygame
import time
pygame.init()


# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Run Game")


# Images
choice_w = WIDTH/5
player_img = pygame.image.load("assets/player_icon.png")
player_img = pygame.transform.scale(player_img, 
                (choice_w, choice_w / (player_img.get_width()/player_img.get_height())))
player_rect = player_img.get_rect(x=WIDTH/6, y=HEIGHT/1.5)
robot_img = pygame.image.load("assets/robot_icon.png")
robot_img = pygame.transform.scale(robot_img, 
                (choice_w, choice_w / (robot_img.get_width()/robot_img.get_height())))
robot_rect = robot_img.get_rect(topright=(WIDTH*(5/6), HEIGHT/1.5))


# Game class
class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()

        self.player = Player(WIDTH*(1/5), "Red")
        self.game_time = 1

        self.bullets = [Bullet() for _ in range(20)]

    def draw_choice(self):
        screen.fill(BLACK)

        # Text
        font = pygame.font.SysFont("comicsans", 50)
        txt = font.render("Select a choice", True, WHITE)

        # Blits
        screen.blit(txt, ((WIDTH-txt.get_width())/2, HEIGHT/4))
        screen.blit(player_img, player_rect.topleft)
        screen.blit(robot_img, robot_rect.topleft)
        pygame.draw.rect(screen, WHITE, player_rect, width=1)
        pygame.draw.rect(screen, WHITE, robot_rect, width=1)

        pygame.display.flip()

    def draw_welcome(self):
        screen.fill(BLACK)

        font = pygame.font.SysFont("comicsans", 50)
        wlcm = font.render("WELCOME TO", True, WHITE)
        game_name = font.render(pygame.display.get_caption()[0], True, random_color(0, 255))
        game = font.render("GAME", True, WHITE)

        for num, txt in enumerate([wlcm, game_name, game]):
            screen.blit(txt, ((WIDTH-txt.get_width())/2, HEIGHT/4 * (num+1)))

        pygame.display.flip()

    def draw_winner(self):
        screen.fill(BLACK)

        font = pygame.font.SysFont("comicsans", 60)

        if self.player.score != self.opponent.score:
            if self.player.score < self.opponent.score:
                winner = self.opponent
            elif self.opponent.score < self.player.score:
                winner = self.player

            the_winner_txt = font.render("The Winner", True, WHITE)
            is_txt = font.render("is", True, WHITE)
            winner_txt = font.render(winner.name, True, winner.color)

            for num, txt in enumerate([the_winner_txt, is_txt, winner_txt]):
                screen.blit(txt, ((WIDTH-txt.get_width())/2, HEIGHT/4 * (num+1)))
        
        else:
            txt = font.render("TIE", True, GREEN)

            screen.blit(txt, ((WIDTH-txt.get_width())/2, 
                                (HEIGHT-txt.get_height())/2))

        pygame.display.flip()

    def draw(self):
        screen.fill(BLACK)

        self.player.draw(screen)
        self.opponent.draw(screen)

        for bullet in self.bullets:
            bullet.draw(screen)

        self.timer_bar.draw(screen)

        pygame.display.flip()

    def run(self): 
        # Main Loop
        running = True
        is_started = False
        is_choosing = False
        while running:
            self.clock.tick(60)

            # Events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN and not is_started:
                    is_started = True
                    is_choosing = True
                elif event.type == pygame.MOUSEBUTTONDOWN and is_choosing:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if player_rect.collidepoint(mouse_x, mouse_y):
                        player_bool, robot_bool = True, False
                        is_choosing = False

                        self.opponent = Player(WIDTH*(4/5), "Blue")
                        self.timer_bar = TimerBar(self.game_time)
                    elif robot_rect.collidepoint(mouse_x, mouse_y):
                        player_bool, robot_bool = False, True
                        is_choosing = False

                        self.opponent = AI_Opponent(WIDTH*(4/5), "Blue")
                        self.timer_bar = TimerBar(self.game_time)

            if not is_started:
                self.draw_welcome()
                continue

            if is_choosing:
                self.draw_choice()
                continue

            # Handle Movements
            self.player.handle_movement("up", "down")
            if player_bool:
                self.opponent.handle_movement('w', 's')
            elif robot_rect:
                self.opponent.move()

            for bullet in self.bullets:
                bullet.move()

            # Mask Collision
            for bullet in self.bullets:
                for player in [self.player, self.opponent]:
                    offset = (bullet.rect.x - player.rect.x, bullet.rect.y - player.rect.y)
                    if player.mask.overlap(bullet.mask, offset):
                        player.reset_pos()

            self.timer_bar.run()

            # Time Out
            if self.timer_bar.rect.h <= 0:
                self.draw_winner()
                self.__init__()
                self.opponent.__init__(self.opponent.rect.x, "Blue")
                is_started = False

            self.draw()


game = Game()
game.run()
