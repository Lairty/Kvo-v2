import pygame


class BackImage(pygame.sprite.Sprite):

    def __init__(self, group, image, coords):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect = coords

    def update(self):
        pass
