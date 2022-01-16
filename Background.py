import pygame as p


class Background(p.sprite.Sprite):
    def __init__(self, surface: p.surface):
        self.surface = surface
        p.sprite.Sprite.__init__(self)

        self.image = p.image.load("images/ground.png")
        self.rect = self.image.get_rect()
        self.surface.blit(self.image, p.Rect((0, 0, 700, 700)))