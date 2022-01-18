import pygame as p

from sprite import AbstractGroup


class Button(p.sprite.Sprite):
    def __init__(self, screen: p.surface, pos: tuple, text_value: str, size: tuple, color_top: tuple,
                 color_bottom: tuple, color_text: tuple, *groups: AbstractGroup):
        super().__init__(*groups)
        self.button_h = pos[1]
        self.screen = screen
        self.pos = pos
        self.text_value = text_value
        self.size = size
        self.color_top = color_top
        self.color_top_original = color_top
        self.color_bottom = color_bottom
        self.color_text = color_text
        self.clicked = False
        self.text_font = p.font.Font(None, 30)
        self.static_rect = p.Rect(self.pos, self.size)
        self.animated_rect = p.Rect((self.pos[0], self.pos[1]), self.size)
        self.static_rect = p.Rect((self.pos[0], self.pos[1] + 6), self.size)
        self.text = self.text_font.render(self.text_value, True, self.color_text)


    # drawing button:
    def draw(self):
        self.click()
        btn_y = self.button_h + (self.size[1] / 2.5)
        self.animated_rect.y = self.button_h

        p.draw.rect(self.screen, self.color_bottom, self.static_rect, border_radius=12)
        p.draw.rect(self.screen, self.color_top, self.animated_rect, border_radius=12)
        self.screen.blit(self.text, (self.pos[0] + (0.2 * self.size[0]), btn_y))

    def click(self):
        mouse = p.mouse.get_pos()
        if self.animated_rect.collidepoint(mouse):
            self.hovering()
            if p.mouse.get_pressed()[0] is True:
                self.button_h = self.pos[1] + 6
                self.clicked = True
            else:
                if self.clicked:
                    self.button_h = self.pos[1]
                    self.color_top = self.color_top_original
                    self.clicked = False
        else:
            self.clicked = False
            self.color_top = self.color_top_original

    def hovering(self):
        if self.color_top[1] + 50 > 255:
            hovering_color = self.color_top[0], 255, self.color_top[2]
        else:
            hovering_color = self.color_top[0], self.color_top[1] + 50, self.color_top[2]
        self.color_top = hovering_color
