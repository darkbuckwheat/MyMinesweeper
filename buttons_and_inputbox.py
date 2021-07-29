import pygame           # the most important import in project


class Button:           # class for creating buttons
    def __init__(self, surface, color, x, y, length, height, width, text, text_color, font_size):
        self.draw_all(surface, color, length, height, x, y, width, text, text_color, font_size)
        self.rect = pygame.Rect(x, y, length, height)

    def write_text(self, surface, text, text_color, length, height, x, y, font_size):
        myFont = pygame.font.SysFont("Calibri", font_size)
        myText = myFont.render(text, 1, text_color)
        surface.blit(myText, ((x+length/2) - myText.get_width()/2, (y+height/2) - myText.get_height()/2))

    def draw_button(self, surface, color, length, height, x, y, width):
        s = pygame.Surface((length, height))
        s.fill(color)
        pygame.draw.rect(s, color, (x, y, length, height), width)
        surface.blit(s, (x, y))
        pygame.draw.rect(surface, color, (x, y, length, height), 0)
        pygame.draw.rect(surface, (190, 190, 190), (x, y, length, height), 1)

    def draw_all(self, surface, color, length, height, x, y, width, text, text_color, font_size):
        s = pygame.Surface((length, height))
        s.fill(color)
        pygame.draw.rect(s, color, (x, y, length, height), width)
        surface.blit(s, (x, y))
        pygame.draw.rect(surface, color, (x, y, length, height), 0)
        pygame.draw.rect(surface, (190, 190, 190), (x, y, length, height), 1)
        myFont = pygame.font.SysFont("Calibri", font_size)
        myText = myFont.render(text, 1, text_color)
        surface.blit(myText, ((x + length / 2) - myText.get_width() / 2, (y + height / 2) - myText.get_height() / 2))

    def pressed(self, mouse):           # click check
        if mouse[0] > self.rect.topleft[0]:
            if mouse[1] > self.rect.topleft[1]:
                if mouse[0] < self.rect.bottomright[0]:
                    if mouse[1] < self.rect.bottomright[1]:
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False


class InputBox:                 # my class for creating inputbox
    def __init__(self, x, y, w, h, par, font_size, text='', text_color=(0, 0, 0)):
        self.font = pygame.font.SysFont("Calibri", font_size)
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color('lightskyblue3')
        self.par = par
        self.text = text
        self.text_color = text_color
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def mouse_event(self, event):           # function for check activation inputbox
        messege = False
        if self.rect.collidepoint(event.pos):
            self.active = True
            messege = True
        else:
            self.active = False
        self.color = (240, 240, 240) if self.active else pygame.Color('lightskyblue3')
        return messege

    def key_event(self, event):             # function for input text
        messege = False
        if self.active:
            messege = True
            if event.key == pygame.K_RETURN:
                f = open('Settings.txt', mode='r')
                data = f.readlines()
                data = list(map(lambda x: x.strip(), data))
                rows = int(data[2].split()[1])
                columns = int(data[1].split()[1])
                if (self.par < 3 and 10 < int(self.text) < 30) or \
                        (self.par == 3 and round(rows * columns * 0.05) < int(self.text) < rows * columns):
                    f = open('Settings.txt', mode='w')
                    f.write(data[0] + '\n')
                    if self.par == 1:
                        f.write('custom_x: ' + self.text + '\n')
                    else:
                        f.write(data[1] + '\n')
                    if self.par == 2:
                        f.write('custom_y: ' + self.text + '\n')
                    else:
                        f.write(data[2] + '\n')
                    if self.par == 3:
                        f.write('custom_mines: ' + self.text + '\n')
                    else:
                        f.write(data[3] + '\n')
                    f.write(data[4] + '\n')
                    f.write(data[5] + '\n')
                    f.write(data[6] + '\n')
                else:
                    self.text = data[self.par].split()[1]
                f.close()

                self.active = False
                self.color = pygame.Color('lightskyblue3')
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if len(self.text) < 3:
                    self.text += event.unicode
            self.txt_surface = self.font.render(self.text, True, self.text_color)
        return messege

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 1)
        self.txt_surface = self.font.render(self.text, True, self.text_color)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 4))


class BoxOfRadioButtons:            # my class for easy radiobutton control
    def __init__(self, *args):
        attr = ['x', 'y', 'n', 'w', 'h', 'texts', 'check_nom']
        for ia, a in enumerate(attr):
            self.__setattr__(a, args[ia])
        m = 0
        for i in self.texts:
            if len(i) > m:
                m = len(i)
        self.font_size = (self.w - 20) // m
        self.buttons = []
        for i in range(1, self.n + 1):
            checked = False
            if i == self.check_nom:
                checked = True
            a = RadioButton(i, self.w, self.h // self.n, self.font_size, self.texts[i - 1], checked)
            self.buttons.append(a)

    def draw(self, screen):
        for i in range(len(self.buttons)):
            self.buttons[i].draw(screen, self.x, self.y + (self.h // self.n - 1) * i)

    def click(self, pos):           # function for change active radiobutton
        if self.x < pos[0] < self.x + self.w and self.y < pos[1] < self.y + self.h:
            n = (pos[1] - self.y) // (self.h // self.n) + 1

            self.buttons[self.check_nom - 1].checked = False
            self.check_nom = n
            self.buttons[self.check_nom - 1].checked = True

            f = open('Settings.txt', mode='r')
            data = f.readlines()
            data = list(map(lambda x: x.strip(), data))
            f = open('Settings.txt', mode='w')
            f.write('difficulty: ' + str(n) + '\n')
            f.write(data[1] + '\n')
            f.write(data[2] + '\n')
            f.write(data[3] + '\n')
            f.write(data[4] + '\n')
            f.write(data[5] + '\n')
            f.write(data[6] + '\n')
            f.close()

            return True
        else:
            return False

    def print(self):            # function for easy print information about radiobuttons(very useful for debug)
        for i in self.buttons:
            print(i.n, i.w, i.h, i.font_size, i.text)


class RadioButton:              # my class for creation radiobutton
    def __init__(self, *args):
        attr = ['n', 'w', 'h', 'font_size', 'text', 'checked']
        for ia, a in enumerate(attr):
            self.__setattr__(a, args[ia])
        self.font = pygame.font.Font(None, self.font_size)

    def draw(self, screen, x, y):
        if self.checked:
            pygame.draw.rect(screen, ('#34D800'), [x + 5, y + 5, 10, 10])
        else:
            pygame.draw.rect(screen, (255, 255, 255), [x + 5, y + 5, 10, 10])
        pygame.draw.rect(screen, (0, 0, 0), [x + 5, y + 5, 10, 10], 1)
        t = self.font.render(self.text, True, (0, 0, 0))
        screen.blit(t, (x + 20, y))