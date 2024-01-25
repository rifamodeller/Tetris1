import pygame
import sys
import random

white = (255, 255, 255)
black = (0, 0, 0)

clrs = [(199, 14, 33),
        (35, 234, 10),
        (55, 220, 230),
        (140, 179, 188),
        (225, 92, 26),
        (15, 220, 48),
        (200, 40, 60)
        ]

lvl = 1
ltc = 1

background = pygame.image.load('tetrs.png')


class Tetris:
    clearedlines = 0
    score = 0
    check = "start"
    field = []
    sy = 50
    sx = 100
    z = 20
    fig = None

    def __init__(self, height, width):
        self.field = []
        self.fig = None
        self.width = width
        self.height = height
        for i in range(height):
            newline = []
            for j in range(width):
                newline.append(0)
            self.field.append(newline)

    def new_block(self):
        self.fig = Figura(3, 0)

    def intersection(self):
        yn = False
        for i in range(4):
            for j in range(4):
                if (i * 4) + j in self.fig.image():
                    if (i + self.fig.y) > (self.height - 1) or \
                            (j + self.fig.x) > (self.width - 1) or \
                            (j + self.fig.x) < 0 or \
                            self.field[i + self.fig.y][j + self.fig.x] > 0:
                        yn = True
        return yn

    def stop(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.fig.image():
                    self.field[i + self.fig.y][j + self.fig.x] = self.fig.clr
        self.delite_line()
        self.new_block()
        if self.intersection():
            self.check = 'gameover'

    def delite_line(self):
        ln = 0
        for i in range(1, self.height):
            zr = 0
            for j in range(0, self.width):
                if self.field[i][j] == 0:
                    zr += 1
            if zr == 0:
                ln += 1
                for x in range(i, 1, -1):
                    for g in range(self.width):
                        self.field[x][g] = self.field[x - 1][g]
        self.score += ln ** 2
        self.clearedlines += ln
        self.lvl_check()

    def lvl_check(self):
        global ltc, lvl
        if lvl <= self.clearedlines:
            lvl += 1
            ltc = lvl
            self.clearedlines = 0
            return True
        else:
            ltc = lvl - self.clearedlines
            return False

    def space_down(self):
        while not self.intersection():
            self.fig.y += 1
        self.fig.y -= 1
        self.stop()

    def down(self):
        self.fig.y += 1
        if self.intersection():
            self.fig.y -= 1
            self.stop()

    def sideways(self, d):
        xx = self.fig.x
        self.fig.x += d
        if self.intersection():
            self.fig.x = xx

    def rotate(self):
        if self.check == 'start':
            rr = self.fig.rotation
            self.fig.rotate()
            if self.intersection():
                self.fig.rotate = rr


class Figura:
    figures = [
        [[4, 5, 6, 7], [1, 5, 9, 13]], [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 8, 9], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [3, 5, 6, 7], [2, 6, 10, 11], [5, 6, 7, 9]], [[5, 6, 9, 10]],
        [[1, 2, 4, 5], [0, 4, 5, 9], [5, 6, 8, 9], [1, 5, 6, 10]],
        [[1, 2, 6, 7], [3, 6, 7, 10], [5, 6, 10, 11], [2, 5, 6, 9]]]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)
        self.clr = random.randint(1, len(clrs) - 1)
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % (len(self.figures[self.type]))


class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


def get_font(size):
    return pygame.font.Font('font.ttf', size)


def main_menu():
    pygame.display.set_caption('Tetris')
    win = pygame.display.set_mode((400, 500))
    pygame.font.init()
    while True:
        win.blit(background, (0, 0))
        mouse = pygame.mouse.get_pos()

        MENU_TEXT = get_font(60).render("Tetris", True, white)
        MENU_RECT = MENU_TEXT.get_rect(center=(200, 120))

        PLAY_BUTTON = Button(image=pygame.image.load("Play Rect.png"), pos=(200, 250),
                             text_input="PLAY", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("Quit Rect.png"), pos=(200, 400),
                             text_input="QUIT", font=get_font(40), base_color="#d7fcd4", hovering_color="White")

        win.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(mouse)
            button.update(win)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(mouse):
                    main()
                if QUIT_BUTTON.checkForInput(mouse):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


def main():
    global lvl, ltc
    pygame.display.set_caption('Tetris')
    swidth = 500
    sheight = 400
    gwidth = 10
    gheight = 20
    pressing = False
    over = False
    count = 0
    FPS = 10

    pygame.init()
    win = pygame.display.set_mode((sheight, swidth))
    clock = pygame.time.Clock()
    playing = Tetris(gheight, gwidth)
    pygame.mixer.music.load('Tetris.mp3')
    pygame.mixer.music.play(-1)

    while not over:
        if playing.fig is None:
            playing.new_block()
        count += 1
        if count >= 100001:
            count = 0

        if pressing or count % (FPS // lvl // 2) == 0:
            if playing.check == 'start':
                playing.down()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                over = True
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    playing.rotate()

                if event.key == pygame.K_RETURN:
                    if playing.check == 'gameover':
                        lvl = 1
                        main()

                if event.key == pygame.K_DOWN:
                    pressing = True

                if event.key == pygame.K_LEFT:
                    playing.sideways(-1)

                if event.key == pygame.K_RIGHT:
                    playing.sideways(1)

                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    lvl = 1
                    main_menu()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    pressing = False

        win.blit(background, (0, 0))
        pygame.draw.rect(win, black, [playing.sx + playing.z - 20,
                                      playing.sy + playing.z - 20,
                                      playing.z + 180,
                                      playing.z + 380])
        for j in range(playing.height):
            for g in range(playing.width):
                #   pygame.draw.rect(win, white, [playing.sx + playing.z * g,
                #                               playing.sy + playing.z * j,
                #                               playing.z,
                #                               playing.z], 1)
                if playing.field[j][g] > 0:
                    pygame.draw.rect(win, clrs[playing.field[j][g]],
                                     [playing.sx + playing.z * g, playing.sy + playing.z * j, playing.z - 2,
                                      playing.z - 1]
                                     )

        if playing.fig is not None:
            for i in range(4):
                for j in range(4):
                    f = i * 4 + j
                    if f in playing.fig.image():
                        pygame.draw.rect(win, clrs[playing.fig.clr],
                                         [
                                             playing.sx + playing.z * (j + playing.fig.x) + 1,
                                             playing.sy + playing.z * (i + playing.fig.y) + 1,
                                             playing.z - 2,
                                             playing.z - 2
                                         ])

        font = pygame.font.SysFont('Comic Sans MS', 18, bold=True)

        win.blit(font.render("Score: " + str(playing.score), True, white), [5, 80])
        win.blit(font.render("Level: " + str(lvl), True, white), [10, 105])
        if playing.lvl_check():
            main()

        if playing.check == 'gameover':
            pygame.draw.rect(win, black, [playing.sx + playing.z - 20,
                                          playing.sy + playing.z - 20,
                                          playing.z + 180,
                                          playing.z + 380])
            win.blit(font.render("Game Over", True, white), [150, 100])
            win.blit(font.render("Press ENTER", True, white), [145, 200])
            win.blit(font.render("to replay", True, white), [160, 230])
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main_menu()

