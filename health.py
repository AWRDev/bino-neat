import pygame

class HealthPickup(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.x = 850
        self.y = 350

        self.image = pygame.image.load("./assets/textures/pickup_heart_64.png")
        self.height = self.image.get_height()
        self.width = self.image.get_width()

        self.rect = self.image.get_rect()
        self.rect.center = (self.x + self.width / 2, self.y - self.height / 2)
    
    def update(self):
        self.rect.centerx -= 1
    