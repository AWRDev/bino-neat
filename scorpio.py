import random
import pygame

class Scorpio(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.image = pygame.image.load("./assets/textures/scorpio_64.png")
        self.height = self.image.get_height()
        self.width = self.image.get_width()

        self.rect = self.image.get_rect()
        self.rect.center = (x + self.width / 2, y - self.height / 2)

        self.init_x = x
        self.init_y = y - self.height

        self.x = x
        self.y = y - self.height
        
        self.velocity_x = 2

    def respawn(self):
        self.x = random.randint(800, 1600)
        self.rect.centerx = self.x

    def update(self):
        self.rect.centerx -= self.velocity_x
        self.x = self.rect.centerx


    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
