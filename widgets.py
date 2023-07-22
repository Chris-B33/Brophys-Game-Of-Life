import pygame

class Text:
    def __init__(self, text, color, x, y,screen, font) -> None:
        self.text = text
        self.color = color
        self.x = x
        self.y = y
        self.screen = screen
        self.font = font
    
    def draw(self) -> None:
        txt = self.font.render(self.text, True, self.color)
        self.screen.blit(txt, (self.x, self.y))


class Button(Text):
    def __init__(self, text, color_text, color_bg, x, y, width, height, screen, font, func) -> None:
        super().__init__(text, color_text, x, y, screen, font)
        self.width = width
        self.height = height
        self.color_bg = color_bg
        self.func = func
    
    def draw(self) -> None:
        pygame.draw.rect(self.screen, self.color_bg, (self.x - self.width / 4, self.y - self.height / 3, self.width, self.height))
        super().draw()

    def process(self, pos) -> None:
        mx = pos[0]
        my = pos[1]

        rx = self.x - self.width / 4
        ry = self.y - self.height / 3

        if (rx <= mx <= rx + self.width) and (ry <= my <= ry + self.height):
            self.func()



