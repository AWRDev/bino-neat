import math
import pygame

from cat import Cat
from scorpio import Scorpio

pygame.init()
width, height = 800, 600
window = pygame.display.set_mode((width, height))


class Game:
    def __init__(self, window: pygame.Surface, window_width, window_height) -> None:

        self.window_width = window_width
        self.window_height = window_height
        self.window = window

        self.base_texture = pygame.image.load("./assets/textures/bino_base_64.png")
        self.base_texture = pygame.transform.scale2x(self.base_texture)
        self.bt_height = self.base_texture.get_rect().height
        self.bt_width = self.base_texture.get_rect().width

        self.base_count = math.ceil(self.window_width / self.bt_width)

        self.background = pygame.image.load("./assets/textures/background_1024.jpg")
        self.offset = 0

        self.player = Cat(50, window_height)
        self.enemy = Scorpio(500, window_height - self.bt_height)

        self.player_g = pygame.sprite.Group()
        self.player_g.add(self.player)

        self.score = 0
        self.level = 1
        self.playing = True


    def _draw_background(self):
        self.window.blit(self.background, (0,0))
    
    def _draw_base(self):
        for i in range(self.base_count):
            self.window.blit(self.base_texture, (self.bt_width*i - self.offset,self.window_height- self.bt_height))

    def _draw_score(self):
        font = pygame.font.SysFont("Arial", 24)
        text_surface = font.render("Score: " + str(self.score), True, (0, 0, 0))
        # blit the text surface to the top-left corner of the screen
        self.window.blit(text_surface, (10, 10))

    def draw(self):
        self._draw_background()
        self._draw_score()
        self._draw_base()
        self.player_g.draw(self.window)
        self.player.draw_rect(self.window)
        self.enemy.draw(self.window)
    
    def update(self):
        self.enemy.update()
        self.player.update()
        if self.enemy.x <= 0:
            self.enemy.respawn()
            self.score += 1
            if self.score != 0 and self.score % 20 == 0:
                self.level += 1
                self.enemy.velocity_x += 2
        if self.player.rect.colliderect(self.enemy.rect):
            self.playing = False
        

if __name__ == "__main__":
    g = Game(window, width, height)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    g.player.jump()
        g.update()
        g.draw()
        pygame.display.flip()
    
