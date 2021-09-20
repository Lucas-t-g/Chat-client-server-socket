import pygame


ColorSet = {"green":[109, 241, 109], "blue":[0, 132, 252], "red":[137, 28, 36], "white":[255, 255, 255], "silver":[100, 100, 100], "black": [0, 0, 0]}
pygame.init()
FONT_ASSIST = pygame.font.Font('freesansbold.ttf', 32)
FONT_ASSIST_2 = pygame.font.Font('freesansbold.ttf', 26)


class Button(pygame.sprite.Sprite):
   def __init__(self, *groups, x, y, ctt):
      super().__init__(*groups)

      self.image = pygame.image.load("imagens/botao1-removebg-preview.png").convert_alpha()
      self.image = pygame.transform.scale(self.image, [194, 58])
      self.rect = pygame.Rect(194, 58, 194, 58)
      self.rect = self.image.get_rect()
      self.rect.center = (x, y)

      self.text = FONT_ASSIST.render(ctt, True, ColorSet["red"], None)
      self.textRect = self.text.get_rect()
      self.textRect.center = (x , y)

      self.image1 = pygame.image.load("imagens/botao1-removebg-preview.png").convert_alpha()
      self.image2 = pygame.image.load("imagens/botao2-removebg-preview.png").convert_alpha()
      self.image3 = pygame.image.load("imagens/botao3-removebg-preview.png").convert_alpha()

      self.touch = False

   def update(self):
      self.mouse = pygame.mouse.get_pressed()
      self.MousePos = pygame.mouse.get_pos()

      if self.rect.collidepoint(self.MousePos):
         if self.mouse[0]:
            self.touch = True
            pygame.mouse.get_rel()
            self.image = self.image2
         
         else:
            self.touch = False
            pygame.mouse.get_rel()
            self.image = self.image3

      else:
         self.touch = False
         self.image = self.image1

def CreateWindow(nameWindow="Sem Titulo", width = 1080, height = 720):
   win = pygame.display.set_mode( (width, height) )
   pygame.display.set_caption(nameWindow)
   win.fill( ColorSet["white"] )
   return win

def main():

   fps = pygame.time.Clock()
   MainLoop = True

   win = CreateWindow()
   
   buttonGroups = pygame.sprite.Group()
   button1 = Button(buttonGroups, x=540, y=360)
         
   while MainLoop:
      fps.tick(60)
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            MainLoop = False
            break

         buttonGroups.update()
         buttonGroups.draw(win)

         pygame.display.update()

   pygame.quit()

if __name__ == '__main__':
   main()