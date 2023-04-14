import pygame

border_color = (255, 255, 255)

class Cat(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("./assets/textures/bino_128.png")
        self.image = pygame.transform.flip(self.image, True, False)
        self.height = self.image.get_height()
        self.width = self.image.get_width()

        self.rect = self.image.get_rect()
        self.rect.center = (x + self.width / 2, y - self.height / 2)

        self.mask = pygame.mask.from_surface(self.image)


        self.init_x = x
        self.init_y = y - self.height

        self.x = x
        self.y = y - self.height

        self.velocity_y = 0

        self.gravity = 0.15
        self.jump_velocity = -10

        self.delta_time = 1

    def update(self):
        self.rect.centery += self.velocity_y
        self.velocity_y += self.gravity

        
        # Check for collisions with the ground
        if self.rect.centery >= self.init_y:
            self.rect.centery = self.init_y
            self.velocity_y = 0
    
    def update_new(self):
        print(self.delta_time)
        self.rect.centery -= self.velocity_y * self.delta_time - 0.5 * self.gravity * self.delta_time**2
        self.delta_time += 1

        if self.rect.centery >= self.init_y:
            self.rect.centery = self.init_y
            self.velocity_y = 0
            self.delta_time = 1

    def jump(self):
        # if self.y >= self.init_y:
        if self.rect.centery >= self.init_y:
            self.velocity_y = self.jump_velocity

    # def draw(self, screen):
    #     screen.blit(self.texture, (self.x, self.y))
    #     pygame.draw.rect(screen, border_color, self.rect, 2)

    def draw_rect(self, screen):
        pygame.draw.rect(screen, border_color, self.rect, 2)
