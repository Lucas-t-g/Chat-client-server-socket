import pygame as pg


pg.init()
screen = pg.display.set_mode((640, 480))
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONT = pg.font.Font(None, 32)


# A classe InputBox implementa caixas onde o usuário popde inserir texto na janela pygame
class InputBox:

    def __init__(self, x, y, w, h, default_text='', color_active=None, color_inactive=None):
        self.rect = pg.Rect(x, y, w, h)
        self.color_active = color_active if color_active != None else COLOR_ACTIVE
        self.color_inactive = color_inactive if color_inactive != None else COLOR_INACTIVE

        self.color = self.color_inactive
        self.text = default_text
        self.txt_surface = FONT.render(self.text, True, self.color)
        self.active = False
        self.default_text = default_text # modificado
        self.input = ""

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
                self.text = "" # modificado
                # print("clicado")
            else:
                self.active = False
                # self.text = self.default_text # modificado

            # Change the current color of the input box.
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN and self.text != "":
                    # print(self.text)
                    self.input = self.text
                    self.text = self.default_text
                    self.txt_surface = FONT.render(self.text, True, self.color)
                    return True
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)



def main():
    clock = pg.time.Clock()
    input_box1 = InputBox(100, 100, 140, 32)
    input_box2 = InputBox(100, 300, 140, 32)
    input_boxes = [input_box1, input_box2]
    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            for box in input_boxes:
                box.handle_event(event)

        for box in input_boxes:
            box.update()

        screen.fill((30, 30, 30))
        for box in input_boxes:
            box.draw(screen)

        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    main()
    pg.quit()