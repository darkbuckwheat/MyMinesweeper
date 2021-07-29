from buttons_and_inputbox import *      # import classes
from random import randint              # random for gamefield create
from time import time                   # module for counting time


def open_cell(x, y):                    # function for the player's turn
    global game_field
    if game_field[y][x][0] == 9 and not game_field[y][x][2]:
        defeat()
    if not game_field[y][x][2] and not game_field[y][x][1]:
        game_field[y][x] = (game_field[y][x][0], True, game_field[y][x][2])
        victory_chek()
        if game_field[y][x][0] == 0:
            for q in range(1, -2, -1):
                for w in range(1, -2, -1):
                    if (-1 < x - q < columns) and (-1 < y - w < rows):
                        open_cell(x - q, y - w)


def open_all(x, y):                     # open field 3x3 in one turn
    global game_field
    m = 0
    for q in range(1, -2, -1):
        for w in range(1, -2, -1):
            if (-1 < x - q < columns) and (-1 < y - w < rows):
                if game_field[y - w][x - q][-1]:
                    m += 1
    if not game_field[y][x][2] and game_field[y][x][1] and (m == game_field[y][x][0]):
        for q in range(1, -2, -1):
            for w in range(1, -2, -1):
                if (-1 < x - q < columns) and (-1 < y - w < rows):
                    open_cell(x - q, y - w)


def set_flag(x, y):                     # function for setting flag
    global game_field, flags
    if not game_field[y][x][1]:
        if game_field[y][x][2]:
            game_field[y][x] = (game_field[y][x][0], game_field[y][x][1], False)
            flags -= 1
        else:
            game_field[y][x] = (game_field[y][x][0], game_field[y][x][1], True)
            flags += 1


def field_create(x, y):                 # function for gamefield creation
    global game_field, rows, columns, mines
    n = 0
    while n < mines:
        a, b = randint(0, rows - 1), randint(0, columns - 1)
        if (a == y and b == x) or game_field[a][b][0] == 9:
            pass
        else:
            game_field[a][b] = (9, False, False)
            n += 1
    for i in range(len(game_field)):
        for j in range(len(game_field[0])):
            if game_field[i][j][0] == 9:
                pass
            else:
                m = 0
                for q in range(1, -2, -1):
                    for w in range(1, -2, -1):
                        if (-1 < i - q < rows) and (-1 < j - w < columns):
                            if game_field[i - q][j - w][0] == 9:
                                m += 1
                game_field[i][j] = (m, False, False)


def victory_chek():                     # checking victory
    global game_field, mines, end
    n = 0
    for t in game_field:
        for p in t:
            if not p[1]:
                n += 1
    if n == mines and not end:
        victory()


def victory():                          # writing data if win
    global end, now, end_text, end_draw
    end = True
    f = open('Settings.txt', mode='r')              # reading data from txt-file
    data = f.readlines()
    data = list(map(lambda x: x.strip(), data))

    s = (data[5].split(' ')[1]).split(',')
    s[dif - 1] = str(int(s[dif - 1]) + 1)           # updating the number of wins
    ss = (data[6].split(' ')[1]).split(',')
    ss[dif - 1] = str(int(ss[dif - 1]) + 1)         # updating the number of all games
    r = (data[4].split(' ')[1]).split(',')
    if r[dif - 1] == '-' or int(now) < int(r[dif - 1]):     # updating best time for chosen difficulty
        r[dif - 1] = now

    f = open('Settings.txt', mode='w')              # writing updated data
    f.write(data[0] + '\n')
    f.write(data[1] + '\n')
    f.write(data[2] + '\n')
    f.write(data[3] + '\n')
    f.write('records: ' + ','.join(r) + '\n')
    f.write('wins: ' + ','.join(s) + '\n')
    f.write('all: ' + ','.join(ss) + '\n')
    f.close()

    end_text = 'победили'               # flag for stop the game and draw victory screen
    end_draw = True


def defeat():
    global end, end_text, end_draw
    if not end:
        end = True
        f = open('Settings.txt', mode='r')              # reading data from txt-file
        data = f.readlines()
        data = list(map(lambda x: x.strip(), data))
        ss = (data[6].split(' ')[1]).split(',')
        ss[dif - 1] = str(int(ss[dif - 1]) + 1)         # updating the number of all games

        f = open('Settings.txt', mode='w')              # writing updated data
        f.write(data[0] + '\n')
        f.write(data[1] + '\n')
        f.write(data[2] + '\n')
        f.write(data[3] + '\n')
        f.write(data[4] + '\n')
        f.write(data[5] + '\n')
        f.write('all: ' + ','.join(ss) + '\n')
        f.close()

        end_text = 'проиграли'          # flag for stop the game and draw defeat screen
        end_draw = True


def game_start():               # main function of the project. everything is preparing here for the game
    global rows, columns, mines, dif, run, new_game, screen, font, text_font, \
        flags, sx, sy, colors, start_time, game_field, \
        bar_draw, but_game, but_new, but_stats, but_settings, \
        but_out, stat_draw, close, end, settings_draw, \
        close_settings, input_1, input_2, input_3, box, end_text, end_draw, but_n_game
        # globals - the most useful and easy way to develop the game
    try:
        f = open('Settings.txt', mode='r')      # reading some data from txt-file
        data = f.readlines()
        dif = int(data[0].split()[1])
        if dif < 4:                             # if chosen one of standard difficulties
            rows = columns = dif * 10
            mines = int((rows ** 2) * (0.1 + (dif - 1) * 0.05))
        else:                                   # if chosen custom difficulty
            rows = int(data[2].split()[1])
            columns = int(data[1].split()[1])
            mines = int(data[3].split()[1])
        cx = int(data[1].split()[1])            # some variables for inputboxes
        cy = int(data[2].split()[1])
        cm = int(data[3].split()[1])
    except Exception:
        f = open('Settings.txt', mode='w')      # creation txt-file with some standard parameters if  it`s missing
        f.write('difficulty: 1\n')
        f.write('custom_x: 15\n')
        f.write('custom_y: 15\n')
        f.write('custom_mines: 27\n')
        f.write('records: -,-,-,-\n')
        f.write('wins: 0,0,0,0\n')
        f.write('all: 0,0,0,0\n')
        dif = 1
        rows = columns = 10
        cx, cy, cm = 15, 15, 27
        mines = int((rows ** 2) * (0.1 + (dif - 1) * 0.05))
    f.close()

    pygame.init()               # some pygame things
    screen = pygame.display.set_mode((columns * 16 + 80, rows * 16 + 80))
    pygame.display.set_caption('Minesweeper')

    game_field = []             # template for the gamefield
    for i in range(rows):
        game_field.append([(0, False, False)] * columns)

    run = True                  # some flags
    new_game = True
    end = False
    end_text = 'проиграли'

    font = pygame.font.Font(None, 21)           # setting useful variables
    text_font = pygame.font.Font(None, 25)
    flags = 0
    sx = 40
    sy = 30
    colors = [(0, 0, 255), (0, 140, 255), (0, 170, 0), (0, 150, 0), (255, 165, 0), (255, 120, 0), (255, 20, 0), (205, 0, 0), (0, 0, 0)]
    start_time = 0

    but_game = Button(screen, (230, 230, 230), 0, 0, 50, 20, 1, 'Игра', (0, 0, 0), 13)      # creation control buttons
    but_new = Button(screen, (230, 230, 230), 0, 14, 130, 25, 1, 'Новая игра             F2', (0, 0, 0), 13)
    but_stats = Button(screen, (230, 230, 230), 0, 38, 130, 25, 1, 'Статистика             F3', (0, 0, 0), 13)
    but_settings = Button(screen, (230, 230, 230), 0, 62, 130, 25, 1, 'Настройки             F4', (0, 0, 0), 13)
    but_out = Button(screen, (230, 230, 230), 0, 86, 130, 25, 1, 'Выход                      F5', (0, 0, 0), 13)
    but_n_game = Button(screen, (230, 230, 230), 75, 100, 90, 25, 1, 'Новая игра', (0, 0, 0), 18)

    close = Button(screen, (240, 0, 0), 300, 50, 50, 30, 1, '', (0, 0, 0), 13)         # close buttons :|
    close_settings = Button(screen, (240, 0, 0), 300, 50, 50, 30, 1, '', (0, 0, 0), 13)

    if dif in [2, 3]:               # preparing templates for game windows
        input_1 = InputBox(70, 275, 50, 30, 1, 20, str(cx))
        input_2 = InputBox(160, 275, 50, 30, 2, 20, str(cy))
        input_3 = InputBox(250, 275, 50, 30, 3, 20, str(cm))
        box = BoxOfRadioButtons(60, 90, 4, 350, 140, ['Лёгкая', 'Нормальная', 'Сложная', 'Особоая'], dif)
    else:
        input_1 = InputBox(35, 170, 35, 20, 1, 15, str(cx))
        input_2 = InputBox(95, 170, 35, 20, 2, 15, str(cy))
        input_3 = InputBox(155, 170, 35, 20, 3, 15, str(cm))
        box = BoxOfRadioButtons(35, 55, 4, 230, 68, ['Лёгкая', 'Нормальная', 'Сложная', 'Особоая'], dif)

    bar_draw = False        # flags for draw or not game windows
    stat_draw = False
    settings_draw = False
    end_draw = False


def draw_bar(bar_draw):     # drawing the bar with settings on top of the screen
    global screen, but_new, but_stats, but_settings, but_out
    if bar_draw:
        pygame.draw.rect(screen, (230, 230, 230), [0, 14, 130, 96])
        but_new.draw_all(screen, (230, 230, 230), 130, 25, 0, 14, 1, 'Новая игра             F2', (0, 0, 0), 13)
        but_stats.draw_all(screen, (230, 230, 230), 130, 25, 0, 38, 1, 'Статистика             F3', (0, 0, 0), 13)
        but_settings.draw_all(screen, (230, 230, 230), 130, 25, 0, 62, 1, 'Настройки             F4', (0, 0, 0), 13)
        but_out.draw_all(screen, (230, 230, 230), 130, 25, 0, 86, 1, 'Выход                      F5', (0, 0, 0), 13)


def draw_stat():            # drawing the statistics window
    global screen, stat_draw, close
    if stat_draw:
        f = open('Settings.txt', mode='r')      # reading data from txt-file
        data = f.readlines()
        dif = int(data[0].split()[1])

        if dif in [2, 3]:                       # resizing statistic window
            close = Button(screen, (240, 0, 0), 300, 50, 50, 30, 1, '', (0, 0, 0), 13)
            pygame.draw.rect(screen, (230, 230, 230), [50, 50, 300, 200])
            close.draw_all(screen, (240, 0, 0), 50, 30, 300, 50, 1, '', (0, 0, 0), 13)
            pygame.draw.line(screen, (255, 255, 255), (315, 55), (335, 75), 5)
            pygame.draw.line(screen, (255, 255, 255), (315, 75), (335, 55), 5)

            local_font = pygame.font.Font(None, 30)
            text = local_font.render('Статистика', True, (0, 0, 0))
            screen.blit(text, [55, 55])

            local_font = pygame.font.Font(None, 25)
            text = local_font.render(f'Ваша сложность {dif}', True, (0, 0, 0))
            screen.blit(text, [75, 90])
            text = local_font.render(f'Всего игр сыграно {(data[6].split()[1]).split(",")[dif - 1]}', True, (0, 0, 0))
            screen.blit(text, [75, 120])
            text = local_font.render(f'Игр выиграно {(data[5].split()[1]).split(",")[dif - 1]}', True, (0, 0, 0))
            screen.blit(text, [75, 150])
            try:
                text = local_font.render(f'Процент побед {round(int((data[5].split()[1]).split(",")[dif - 1]) / int((data[6].split()[1]).split(",")[dif - 1]), 4) * 100}%', True, (0, 0, 0))
            except ZeroDivisionError:
                text = local_font.render(f'Процент побед {0}%', True, (0, 0, 0))
            screen.blit(text, [75, 180])
            text = local_font.render(f'Рекорд {(data[4].split()[1]).split(",")[dif - 1]}', True, (0, 0, 0))
            screen.blit(text, [75, 210])
        else:
            close = Button(screen, (240, 0, 0), 195, 25, 25, 25, 1, '', (0, 0, 0), 13)
            pygame.draw.rect(screen, (230, 230, 230), [20, 25, 200, 150])
            close.draw_all(screen, (240, 0, 0), 25, 25, 195, 25, 1, '', (0, 0, 0), 13)
            pygame.draw.line(screen, (255, 255, 255), (200, 30), (215, 45), 5)
            pygame.draw.line(screen, (255, 255, 255), (200, 45), (215, 30), 5)

            local_font = pygame.font.Font(None, 25)
            text = local_font.render('Статистика', True, (0, 0, 0))
            screen.blit(text, [25, 30])

            local_font = pygame.font.Font(None, 20)
            text = local_font.render(f'Ваша сложность {dif}', True, (0, 0, 0))
            screen.blit(text, [35, 60])
            text = local_font.render(f'Всего игр сыграно {(data[6].split()[1]).split(",")[dif - 1]}', True, (0, 0, 0))
            screen.blit(text, [35, 82])
            text = local_font.render(f'Игр выиграно {(data[5].split()[1]).split(",")[dif - 1]}', True, (0, 0, 0))
            screen.blit(text, [35, 104])
            try:
                text = local_font.render(
                    f'Процент побед {round(int((data[5].split()[1]).split(",")[dif - 1]) / int((data[6].split()[1]).split(",")[dif - 1]), 4) * 100}%',
                    True, (0, 0, 0))
            except ZeroDivisionError:
                text = local_font.render(f'Процент побед {0}%', True, (0, 0, 0))
            screen.blit(text, [35, 126])
            text = local_font.render(f'Рекорд {(data[4].split()[1]).split(",")[dif - 1]}', True, (0, 0, 0))
            screen.blit(text, [35, 148])
        f.close()


def draw_settings():            # drawing the settings window
    global screen, dif, settings_draw, close_settings, input_1, input_2, input_3, box
    if settings_draw:
        if dif in [2, 3]:                   # resizing settings window
            close_settings = Button(screen, (240, 0, 0), 300, 50, 50, 30, 1, '', (0, 0, 0), 13)
            pygame.draw.rect(screen, (230, 230, 230), [50, 50, 300, 270])
            close_settings.draw_all(screen, (240, 0, 0), 50, 30, 300, 50, 1, '', (0, 0, 0), 13)
            pygame.draw.line(screen, (255, 255, 255), (315, 55), (335, 75), 5)
            pygame.draw.line(screen, (255, 255, 255), (315, 75), (335, 55), 5)

            local_font = pygame.font.Font(None, 30)
            text = local_font.render('Настройки', True, (0, 0, 0))
            screen.blit(text, [55, 55])

            local_font = pygame.font.Font(None, 27)
            text = local_font.render('Настройка осбого режима:', True, (0, 0, 0))
            screen.blit(text, [60, 225])
            local_font = pygame.font.Font(None, 22)
            text = local_font.render('Ширина', True, (0, 0, 0))
            screen.blit(text, [65, 255])
            text = local_font.render('Высота', True, (0, 0, 0))
            screen.blit(text, [155, 255])
            text = local_font.render('Мины', True, (0, 0, 0))
            screen.blit(text, [255, 255])

            input_1.draw(screen)
            input_2.draw(screen)
            input_3.draw(screen)
            box.draw(screen)
        else:
            close_settings = Button(screen, (240, 0, 0), 195, 25, 25, 25, 1, '', (0, 0, 0), 13)
            pygame.draw.rect(screen, (230, 230, 230), [20, 25, 200, 180])
            close_settings.draw_all(screen, (240, 0, 0), 25, 25, 195, 25, 1, '', (0, 0, 0), 13)
            pygame.draw.line(screen, (255, 255, 255), (200, 30), (215, 45), 5)
            pygame.draw.line(screen, (255, 255, 255), (200, 45), (215, 30), 5)

            local_font = pygame.font.Font(None, 25)
            text = local_font.render('Настройки', True, (0, 0, 0))
            screen.blit(text, [25, 30])

            local_font = pygame.font.Font(None, 20)
            text = local_font.render('Настройка осбого режима:', True, (0, 0, 0))
            screen.blit(text, [30, 130])
            local_font = pygame.font.Font(None, 18)
            text = local_font.render('Ширина', True, (0, 0, 0))
            screen.blit(text, [30, 155])
            text = local_font.render('Высота', True, (0, 0, 0))
            screen.blit(text, [90, 155])
            text = local_font.render('Мины', True, (0, 0, 0))
            screen.blit(text, [155, 155])

            input_1.draw(screen)
            input_2.draw(screen)
            input_3.draw(screen)
            box.draw(screen)


def draw_endgame():             # drawing the endgame window
    global screen, end_text, end_draw, dif, but_n_game
    if end_draw:
        s = 'Вы ' + end_text
        if dif == 2:
            pygame.draw.rect(screen, (230, 230, 230), [130, 130, 140, 80])
            pygame.draw.rect(screen, (20, 20, 20), [130, 130, 140, 80], 2)
            but_n_game = Button(screen, (230, 230, 230), 150, 175, 100, 25, 1, 'Новая игра', (0, 0, 0), 20)

            local_font = pygame.font.Font(None, 25)
            text = local_font.render(s, True, (0, 0, 0))
            screen.blit(text, [140, 140])
        elif dif == 3:
            pygame.draw.rect(screen, (230, 230, 230), [210, 200, 140, 80])
            pygame.draw.rect(screen, (20, 20, 20), [210, 200, 140, 80], 2)
            but_n_game = Button(screen, (230, 230, 230), 235, 245, 90, 25, 1, 'Новая игра', (0, 0, 0), 18)

            local_font = pygame.font.Font(None, 23)
            text = local_font.render(s, True, (0, 0, 0))
            screen.blit(text, [230, 210])
        else:
            pygame.draw.rect(screen, (230, 230, 230), [50, 60, 140, 80])
            pygame.draw.rect(screen, (20, 20, 20), [50, 60, 140, 80], 2)
            but_n_game.draw_all(screen, (230, 230, 230), 90, 25, 75, 100, 1, 'Новая игра', (0, 0, 0), 18)

            local_font = pygame.font.Font(None, 23)
            text = local_font.render(s, True, (0, 0, 0))
            screen.blit(text, [70, 70])


game_start()            # starting the game

while run:
    for event in pygame.event.get():        # event processing
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_F5):
            run = False
        elif event.type == pygame.KEYDOWN:
            if settings_draw and (input_1.key_event(event) or input_2.key_event(event) or input_3.key_event(event)):    # blocking game while changing settings
                pass
            elif event.key == pygame.K_F2:      # starting new game
                game_start()
            elif event.key == pygame.K_F3:      # setting flag for drawing statistic
                stat_draw = True
                bar_draw = False
            elif event.key == pygame.K_F4:      # setting flag for drawing settings
                settings_draw = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if settings_draw and (input_1.mouse_event(event) or input_2.mouse_event(event) or input_3.mouse_event(event)):
                pass
            if settings_draw and box.click(pygame.mouse.get_pos()):     # processing radiobuttons event
                pass
            elif but_n_game.pressed(pygame.mouse.get_pos()) and end_draw:   # starting new game after end
                end_draw = False
                game_start()
            elif but_game.pressed(pygame.mouse.get_pos()):  # switching window with buttons
                bar_draw = not bar_draw
            elif but_out.pressed(pygame.mouse.get_pos()) and bar_draw:  # close game event
                run = False
            elif but_new.pressed(pygame.mouse.get_pos()) and bar_draw:  # starting new game
                game_start()
            elif but_stats.pressed(pygame.mouse.get_pos()) and bar_draw:    # setting flag for drawing statistic
                stat_draw = True
                bar_draw = False
            elif but_settings.pressed(pygame.mouse.get_pos()) and bar_draw:     # setting flag for drawing settings
                settings_draw = True
                bar_draw = False
            elif close.pressed(pygame.mouse.get_pos()) and stat_draw:       # closing statistic window
                stat_draw = False
            elif close_settings.pressed(pygame.mouse.get_pos()) and settings_draw:   # restarting game after changing settings
                settings_draw = False
                game_start()
            elif settings_draw:     # blocking game while changing settings
                pass
            elif new_game and event.button == 1 and (sx - 1 < pygame.mouse.get_pos()[0] < sx + 16 * columns) \
                    and (sy - 1 < pygame.mouse.get_pos()[1] < sy + 16 * rows) and not end:      # processing first player turn
                x, y = (pygame.mouse.get_pos()[0] - sx) // 16, (pygame.mouse.get_pos()[1] - sy) // 16
                field_create(x, y)
                open_cell(x, y)
                start_time = time() // 1        # I just didn't want to use round()
                end = False
                new_game = False
                bar_draw = False
            elif event.button == 1 and (sx - 1 < pygame.mouse.get_pos()[0] < sx + 16 * columns) \
                    and (sy - 1 < pygame.mouse.get_pos()[1] < sy + 16 * rows) and not end:      # processing player turn, if open one cell
                x, y = (pygame.mouse.get_pos()[0] - sx) // 16, (pygame.mouse.get_pos()[1] - sy) // 16
                open_cell(x, y)
                bar_draw = False
            elif event.button == 3 and (sx - 1 < pygame.mouse.get_pos()[0] < sx + 16 * columns) \
                    and (sy - 1 < pygame.mouse.get_pos()[1] < sy + 16 * rows) and not end:      # processing player turn, if setting flag
                x, y = (pygame.mouse.get_pos()[0] - sx) // 16, (pygame.mouse.get_pos()[1] - sy) // 16
                set_flag(x, y)
            elif event.button == 2 and (sx < pygame.mouse.get_pos()[0] < sy + 16 * columns) \
                    and (sx < pygame.mouse.get_pos()[1] < sy + 16 * rows) and not end:      # processing player turn, if open 3x3 field
                x, y = (pygame.mouse.get_pos()[0] - sx) // 16, (pygame.mouse.get_pos()[1] - sy) // 16
                open_all(x, y)

    screen.fill((206, 228, 235))        # updating screen

    for i in range(len(game_field) + 1):        # drawing gamefield lines
        pygame.draw.line(screen, (0, 0, 0), (sx - 1, sy - 1 + i * 16), (sx - 1 + 16 * columns, sy - 1 + i * 16), 1)
    for i in range(len(game_field[0]) + 1):
        pygame.draw.line(screen, (0, 0, 0), (sx - 1 + i * 16, sy - 1), (sx - 1 + i * 16, sy - 1 + rows * 16), 1)

    for i in range(len(game_field)):            # drawing gamefield
        for j in range(len(game_field[0])):
            if game_field[i][j][1]:
                pygame.draw.rect(screen, (230, 230, 230), [sx + 16 * j, sy + 16 * i, 15, 15])
                if game_field[i][j][0] != 0:
                    text = font.render(str(game_field[i][j][0]), True, colors[game_field[i][j][0] - 1])
                    screen.blit(text, [sx + 4 + 16 * j, sy + 1 + 16 * i])
            else:
                pygame.draw.rect(screen, (0, 0, 255), [sx + 16 * j, sy + 16 * i, 15, 15])
                if game_field[i][j][2]:
                    text = font.render('F', True, (255, 0, 0))
                    screen.blit(text, [sx + 4 + 16 * j, sy + 1 + 16 * i])

    pygame.draw.rect(screen, (230, 230, 230), [0, 0, columns * 16 + 80, 15])        # drawing the top bar
    pygame.draw.line(screen, (180, 180, 180), (0, 14), (columns * 16 + 80, 14), 1)
    but_game.draw_button(screen, (230, 230, 230,), 50, 15, 0, 0, 1)
    but_game.write_text(screen, 'Игра', (0, 0, 0), 50, 15, 0, 0, 13)

    text = text_font.render('Time:', True, (0, 0, 0))       # drawing time and mines
    screen.blit(text, [sx, rows * 16 + 80 - 35])
    if start_time == 0:
        now = '0'
    elif end:
        pass
    else:
        now = str(int(time() // 1 - start_time))
    text = text_font.render(now, True, (0, 0, 0))
    screen.blit(text, [sx + 10 + 40, rows * 16 + 80 - 35])
    text = text_font.render('Mines:', True, (0, 0, 0))
    screen.blit(text, [columns * 16 + sx - 80, rows * 16 + 80 - 35])
    c = mines - flags
    if c < 0:
        c = 0
    text = text_font.render(str(c), True, (0, 0, 0))
    screen.blit(text, [columns * 16 + sx - 20, rows * 16 + 80 - 35])

    draw_bar(bar_draw)          # drawing all optional windows
    draw_stat()
    draw_settings()
    draw_endgame()

    pygame.display.flip()
pygame.quit()