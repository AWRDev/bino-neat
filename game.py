import math
import pygame

from cat import Cat
from scorpio import Scorpio
from health import HealthPickup

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
        self.player_immune = False
        self.enemy = Scorpio(500, window_height - self.bt_height)

        self.player_g = pygame.sprite.Group()
        self.player_g.add(self.player)

        self.pickups = pygame.sprite.Group()

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
    
    def _draw_live_counter(self):
        font = pygame.font.SysFont("Comic Sans", 24)
        text_surface = font.render("Lives: " + str(self.player.lives), True, (0, 0, 0))
        # blit the text surface to the top-left corner of the screen
        self.window.blit(text_surface, (700, 10))

    def _draw_ui(self):
        self._draw_background()
        self._draw_score()
        self._draw_live_counter()

    def _get_offset(self, obj1: pygame.sprite.Sprite, obj2: pygame.sprite.Sprite):
        return (obj2.rect.x-obj1.rect.x, obj2.rect.y-obj1.rect.y)
    def draw(self):
        self._draw_ui()
        self._draw_base()
        self.player_g.draw(self.window)
        self.player.draw_rect(self.window)
        self.enemy.draw(self.window)
        self.pickups.draw(self.window)
    def gen_pickups(self, level):
        if level<0:
            return
        else:
            match level:
                case 1:
                    if (len(self.pickups)>=1):
                        return
                    self.pickups.add(HealthPickup())

        
    def update(self):
        self.gen_pickups(self.level)
        self.enemy.update()
        self.player.update()
        self.pickups.update()
        if self.enemy.x <= 0:
            self.player_immune = False
            self.enemy.respawn()
            self.score += 1
            if self.score != 0 and self.score % 20 == 0:
                self.level += 1
                self.enemy.velocity_x += 2
        if self.player.rect.colliderect(self.enemy.rect):
            if self.player.mask.overlap(self.enemy.mask, self._get_offset(self.player,self.enemy)):
                if not self.player_immune:
                    self.player.lives -= 1
                self.player_immune = True
                if self.player.lives == 0:
                    self.playing = False
        collected_pickups = pygame.sprite.spritecollide(self.player, self.pickups, False)
        if collected_pickups:
                self.player.lives += 1
                self.pickups.remove(collected_pickups[0])
        

if __name__ == "__main__":
    g = Game(window, width, height)
    while g.playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    g.player.jump()

        keys = pygame.key.get_pressed()
            
        if keys[pygame.K_a]:
            g.enemy.move(1)
        if keys[pygame.K_d]:
            g.enemy.move(-1)
                
        g.update()
        g.draw()
        # overlap_mask = g.player.mask.overlap_mask(g.enemy.mask, g._get_offset(g.player,g.enemy))
        # overlap_surf = overlap_mask.to_surface(setcolor= (255, 0, 0))
        # overlap_surf.set_colorkey((0, 0, 0))
        # window.blit(overlap_surf, g.player.rect)
        pygame.display.flip()
    
