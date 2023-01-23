import math
import random

import pygame as pygame

WHITE = (100, 100, 100)

HEIGHT = 1020
LEN = 1920
HH = HEIGHT / 2
HL = LEN / 2


class AmmoObject(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("res/ball.png").convert_alpha()
        self.rect = self.image.get_rect()

        self.spawned = False

    def spawn(self):
        if not self.spawned:
            rando_posx = random.randint(16, LEN - 16)
            rando_posy = random.randint(16 + 100, HEIGHT)
            self.rect.x = rando_posx
            self.rect.y = rando_posy
            self.spawned = True


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("res/5322070.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = HL - 64, HH

        self.angle = 0

        self.velx, self.vely = 0, 0
        self.power = 1000

        self.max_ammo = 6
        self.ammo = self.max_ammo

    def gravity(self):
        self.vely += 0.5
        if self.vely >= 8:
            self.vely = 8

        self.rect.y += self.vely
        self.rect.x += self.velx

    def shoot(self):
        if self.ammo <= 0:
            self.ammo = 0
            return

        self.ammo -= 1

        player_center = pygame.Vector2(self.rect.center)

        mouse_pos = pygame.mouse.get_pos()
        delta = mouse_pos - player_center

        angle_to_mouse = math.atan2(delta.y, delta.x)
        looking_vector = pygame.Vector2(1, 1)
        looking_vector.xy = (100 * math.cos(angle_to_mouse), 100 * math.sin(angle_to_mouse))

        self.vely = 0

        self.velx += -looking_vector.x / 10
        self.vely += -looking_vector.y / 4

    def update(self, window):
        self.gravity()


class Game:
    def __init__(self):
        self.player = Player()
        self.ammoGO = AmmoObject()

        self.score = 0
        self.font = pygame.font.Font('freesansbold.ttf', 122)
        self.font_small = pygame.font.Font('freesansbold.ttf', 32)

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.ammoGO, self.player)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.shoot()

        return False

    def run(self, screen):
        self.ammoGO.spawn()
        self.player.update(screen)

        window_rect = screen.get_rect()
        window_rect.x = window_rect.x

        if self.ammoGO.rect.colliderect(self.player.rect):
            self.player.ammo = self.player.max_ammo
            self.score += 1

            rando_posx = random.randint(16, LEN - 16)
            rando_posy = random.randint(16 + 200, HEIGHT)
            self.ammoGO.rect.x = rando_posx
            self.ammoGO.y = rando_posy

        if not window_rect.colliderect(self.player.rect):
            self.player.velx /= 3

            if self.player.rect.x < 0:
                self.player.rect.x = LEN
            else:
                self.player.rect.x = -64

            self.player.vely /= 3

    def display_frame(self, screen):
        """ Display everything to the screen for the game. """
        screen.fill(WHITE)

        score_text = self.font.render(str(self.score), True, (200, 200, 200))
        ammo_text = self.font_small.render(str(self.player.ammo), True, (166, 166, 166))

        score_text_rect = score_text.get_rect()
        ammo_text_rect = ammo_text.get_rect()

        score_text_rect.center = (HL, HH)
        ammo_text_rect.center = (HL, HH + 82)
        screen.blit(score_text, score_text_rect)
        screen.blit(ammo_text, ammo_text_rect)

        self.all_sprites.draw(screen)

        pygame.display.flip()


def main():
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((LEN, HEIGHT))

    clock = pygame.time.Clock()

    game = Game()

    pygame.mixer.music.load("res/5759638520987648.wav")
    pygame.mixer.music.play(-1)

    done = False

    while not done:
        game.process_events()
        game.run(screen)
        game.display_frame(screen)

        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
