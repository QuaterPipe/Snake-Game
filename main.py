#                         #
#  Game: Snake            #
#  By: Jason Gali         #
#  Published: 11/10/2020  #
#                         #
try:
    import pygame
    from random import randint
    import math
    from math import floor
    import time
    import json

    pygame.init()
    pygame.font.init()

    with open('Data/gameData.json', 'r') as f:
        gameData = json.load(f)
    with open('Data/gameConfig.json', 'r') as f:
        gameConfig = json.load(f)

    # Textures#
    # Snake textures#
    snake_head = pygame.image.load('textures/snake_textures/{}/snake_head.png'.format(gameConfig["colour"]))
    snake_head_up = pygame.image.load('textures/snake_textures/{}/snake_head_up.png'.format(gameConfig["colour"]))
    snake_head_down = pygame.image.load('textures/snake_textures/{}/snake_head_down.png'.format(gameConfig["colour"]))
    snake_head_right = pygame.image.load('textures/snake_textures/{}/snake_head_right.png'.format(gameConfig["colour"]))
    snake_tail = pygame.image.load('textures/snake_textures/{}/snake_tail.png'.format(gameConfig["colour"]))
    snake_eat = pygame.image.load('textures/snake_textures/{}/snake_eat.png'.format(gameConfig["colour"]))
    snake_dead = pygame.image.load('textures/snake_textures/{}/snake_dead.png'.format(gameConfig["colour"]))
    apple_pic = pygame.image.load('textures/snake_textures/apple.png')

    # Menu textures#
    icon = pygame.image.load('iconpic.png')
    bg = pygame.image.load('textures/menu_textures/background.png')
    death_scr = pygame.image.load('textures/menu_textures/death_screen.png')
    welcome_screen = pygame.image.load('textures/menu_textures/welcome_screen.png')
    end_screen = pygame.image.load('textures/menu_textures/end_screen.png')
    pause_screen = pygame.image.load('textures/menu_textures/pause_screen.png')
    statistics = pygame.image.load('textures/menu_textures/statistics.png')

    top_bar = pygame.image.load('textures/menu_textures/top_bar.png')

    unpause_button = pygame.image.load('textures/menu_textures/unpause_button.png')
    pause_button = pygame.image.load('textures/menu_textures/pause_button.png')
    play_button = pygame.image.load('textures/menu_textures/play_button.png')
    exit_button = pygame.image.load('textures/menu_textures/exit.png')
    stats_button = pygame.image.load('textures/menu_textures/stats_button.png')
    bar = pygame.image.load('textures/menu_textures/bar.png')
    slider = pygame.image.load('textures/menu_textures/slider.png')
    off = pygame.image.load('textures/menu_textures/off.png')
    on = pygame.image.load('textures/menu_textures/on.png')
    # sounds#
    apple_spawn = pygame.mixer.Sound('sounds/apple_spawn.wav')
    death_sound = pygame.mixer.Sound('sounds/death.wav')
    eat = pygame.mixer.Sound('sounds/eat.wav')
    startup = pygame.mixer.Sound('sounds/startup.wav')
    click_sound = pygame.mixer.Sound('sounds/click.wav')
    end_sound = pygame.mixer.Sound('sounds/end.wav')
    # screen#
    win = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Snake")
    pygame.display.set_icon(icon)
    clock = pygame.time.Clock()

    # END of screen#
    # classes#


    class apple(object):
        def __init__(self, x, y):
            self.x = x
            self.y = y


    class button(object):
        def __init__(self, x, y, width, height):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.minx = x
            self.maxX = width + x
            self.miny = y
            self.maxy = y + height

        def clicked(self):
            click = pygame.mouse.get_pressed()
            if click[0]:
                mouse = pygame.mouse.get_pos()
                if (mouse[0] >= self.minx) and (mouse[0] <= self.maxX) and (mouse[1] >= self.miny) and (
                        mouse[1] <= self.maxy):
                    return True
            return False

    class snake(object):

        def __init__(self, x, y, width, height):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.vel = gameConfig["speed"]
            self.face = 90
            self.eatCount = 0
            self.moving = True
            self.living = True
            self.fps = 10
            self.head = snake_head
            self.tail = snake_tail
            self.trailX = []
            self.trailY = []
            self.trailDict = {}

        def trail(self):
            self.trailDict.clear()
            self.trailX.append(self.x)
            self.trailY.append(self.y)
            if len(self.trailY) > self.eatCount:
                del self.trailY[0]
                del self.trailX[0]
            a_num = 0
            e_num = 0
            for a in range(len(self.trailY)):
                a_num += 1
                if player.y == self.trailY[a]:
                    for e in range(len(self.trailX)):
                        e_num += 1
                        if player.x == self.trailX[e]:
                            break
                        break
                    break
            for i in range(len(self.trailY)):
                self.trailDict["tail{0}".format(i)] = [self.trailX[i], self.trailY[i], e_num, a_num]

        def killcheck(self):
            for i in range(len(self.trailDict)):
                tempVal = self.trailDict["tail{0}".format(i)]
                if tempVal[2] != 0 and tempVal[3] != 0:
                    if self.x == tempVal[2] and self.y == tempVal[3]:
                        return True
            return False

        def draw(self, win):
            if game.orient == "up":
                win.blit(snake_head_up, (game.player.x, game.player.y))
            elif game.orient == "down":
                win.blit(snake_head_down, (game.player.x, game.player.y))
            elif game.orient == "right":
                win.blit(snake_head_right, (game.player.x, game.player.y))
            elif game.orient == "left":
                win.blit(snake_head, (game.player.x, game.player.y))
            c = 0
            for x in range(floor(len(game.coordinates))):
                try:
                    win.blit(snake_tail, (game.coordinates[c]))
                    c += 1
                except IndexError:
                    pass


    # Main game object#


    class Game(object):

        def __init__(self, player):
            self.app = apple((randint(6, 45) * 10), (randint(6, 45) * 10))
            self.coordinates = []
            self.deaths = gameData["deaths"]
            self.eating = False
            self.fileLoops = 0
            self.gamesPlayed = gameData["games played"]
            self.high_score = gameData["highest score"]
            self.moves = gameData["moves"]
            self.music = gameConfig["Music"]
            self.myFont = pygame.font.SysFont('Lato', 16)
            self.orient = ""
            self.paused = False
            self.player = player
            self.player_living = True
            self.run = True
            self.sliderX = 390
            self.sliderY = 245
            self.snake_colour = gameConfig["colour"]
            self.speed = gameConfig["speed"]

        def beginGame(self):
            while True:
                pygame.time.delay(100)
                click = pygame.mouse.get_pressed()
                if click[0]:
                    break
                for events in pygame.event.get():
                    if events.type == pygame.QUIT:
                        self.run = False
                        end_sound.play()
                        pygame.time.delay(1000)
                        pygame.quit()
                        exit()
                keys = pygame.key.get_pressed()
                text = myFont.render("Press Space", False, (0, 200, 175))
                win.blit(welcome_screen, (0, 0))
                if keys[pygame.K_SPACE]:
                    return True
                    break
                win.blit(text, (200, 300))
                pygame.display.update()

        def bite(self):
            if self.player.x == self.app.x and self.player.y == self.app.y:
                eat.play()
                self.eating = True
                self.app.x = (randint(6, 45) * 10)
                self.app.y = (randint(6, 45) * 10)
                test = self.app.x % self.player.vel
                if test != 0:
                    dif = test % self.player.width
                    test += dif
                    self.app.x = test
                test = self.app.y % self.player.vel
                if test != 0:
                    dif = test % self.player.width
                    test += dif
                    self.app.x = test
                win.blit(snake_eat, (player.x, player.y))
                pygame.display.update()
                self.player.eatCount += 1
                return True
            return False

        def checkClick(self, minx, maxX, miny, maxy):
            click = pygame.mouse.get_pressed()
            if click[0]:
                mouse = pygame.mouse.get_pos()
                if minx <= mouse[0] <= maxX and miny <= mouse[1] <= maxy:
                    return True
                else:
                    return False

        def end(self):
            win.blit(end_screen, (0, 0))
            pygame.display.update()
            end_sound.play()
            pygame.quit()
            return 0

        def endgame(self):
            while True:
                pygame.time.delay(100)
                self.fileLoops += 1
                score = myFont.render(("Score: " + str(self.player.eatCount)), False, (0, 0, 0))
                for events in pygame.event.get():
                    if events.type == pygame.QUIT:
                        end_sound.play()
                        pygame.time.delay(1000)
                        self.run = False
                        pygame.quit()
                keys = pygame.key.get_pressed()
                win.blit(death_scr, (0, 0))
                win.blit(score, (200, 270))
                if keys[pygame.K_q]:
                    return True
                    break
                if keys[pygame.K_e]:
                    return False
                    break
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        end_sound.play()
                        pygame.quit()
                        exit()
                pygame.display.update()

        def keyPress(self):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.moves += 1
                if player.face == 180:
                    pass
                else:
                    self.player.face = 0
                    self.orient = "up"

            if keys[pygame.K_s]:
                self.moves += 1
                if player.face == 0:
                    pass
                else:
                    self.player.face = 180
                    self.orient = "down"

            if keys[pygame.K_a]:
                self.moves += 1
                if player.face == 90:
                    pass
                else:
                    self.player.face = 270
                    self.orient = "left"

            if keys[pygame.K_d]:
                self.moves += 1
                if player.face == 270:
                    pass
                else:
                    self.player.face = 90
                    self.orient = "right"
            if keys[pygame.K_UP]:
                self.moves += 1
                if player.face == 180:
                    pass
                else:
                    self.player.face = 0
                    self.orient = "up"

            if keys[pygame.K_DOWN]:
                self.moves += 1
                if player.face == 0:
                    pass
                else:
                    self.player.face = 180
                    self.orient = "down"

            if keys[pygame.K_LEFT]:
                self.moves += 1
                if player.face == 90:
                    pass
                else:
                    self.player.face = 270
                    self.orient = "left"

            if keys[pygame.K_RIGHT]:
                self.moves += 1
                if player.face == 270:
                    pass
                else:
                    self.player.face = 90
                    self.orient = "right"

        def move(self, orient):
            game.player_living = True
            if self.orient == "right":
                test = (self.player.x + self.player.vel)
                if test % self.player.width != 0:
                    div = test % self.player.width
                    test += div
                    self.player.x = test
                    self.player.x = round(self.player.x / 10) * 10
                else:
                    self.player.x += self.player.vel
                    self.player.x = round(self.player.x / 10) * 10
            elif self.orient == "right":
                self.player_living = False

            if self.orient == "up":
                test = (self.player.y - self.player.vel)
                if test % self.player.width != 0:
                    div = test % self.player.width
                    test -= div
                    self.player.y = test
                    self.player.y = round(self.player.y / 10) * 10
                else:
                    self.player.y -= self.player.vel
                    self.player.y = round(self.player.y / 10) * 10
            elif self.orient == "up" and self.player.y > self.player.vel:
                self.player_living = False

            if self.orient == "left":
                test = (self.player.x - self.player.vel)
                if test % self.player.width != 0:
                    div = test % self.player.width
                    test -= div
                    self.player.x = test
                    self.player.x = round(self.player.x / 10) * 10
                else:
                    self.player.x -= self.player.vel
                    self.player.x = round(self.player.x / 10) * 10
            elif self.orient == "left" and self.player.x > self.player.vel:
                self.player_living = False

            if self.orient == "down":
                test = (self.player.y + self.player.vel)
                if test % self.player.width != 0:
                    div = test % self.player.width
                    test += div
                    self.player.y = test
                    self.player.y = round(self.player.y / 10) * 10
                else:
                    self.player.y += self.player.vel
                    self.player.y = round(self.player.y / 10) * 10
            elif self.orient == "down" and self.player.y < 500 - self.player.height - self.player.vel:
                self.player_living = False

                return self.player_living

        def pause(self):
            colours = {
                0: "red",
                1: "blue",
                2: "purple",
                3: "white",
                4: "green"
            }
            colourrgb = {
                "red": (228, 11, 11),
                "blue": (2, 84, 160),
                "purple": (86, 0, 71),
                "white": (255, 255, 255),
                "green": (7, 160, 2)
            }
            vals = colours.values()
            loops = (list(vals).index(self.snake_colour))
            while True:
                pygame.time.delay(20)
                keys = pygame.key.get_pressed()
                if self.checkClick(50, 100, 240, 290):
                    pygame.time.delay(30)
                    loops += 1
                elif keys[pygame.K_r]:
                    pygame.time.delay(60)
                    loops += 1
                if loops >= 5:
                    loops = 0
                if self.checkClick(240, 260, 20, 30):
                    break
                if self.checkClick(200, 300, 250, 300):
                    self.runStats()
                if self.checkClick(240,310,425,455):
                    if self.music:
                        self.music = False
                    elif not self.music:
                        self.music = True
                self.setSpeed()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    break
                for events in pygame.event.get():
                    if events.type == pygame.QUIT:
                        end_sound.play()
                        pygame.time.delay(1000)
                        pygame.display.quit()
                        exit()
                text = myFont.render("Speed", False, (0, 0, 0))
                text2 = myFont.render("Colour:", False, (0, 0, 0))
                text3 = myFont.render("R", False, (0, 0, 0))
                text4 = myFont.render("MUSIC:", False, (255, 255, 255))
                win.blit(bg, (0, 0))
                win.blit(pause_screen, (0, 100))
                win.blit(bar, (400, 200))
                win.blit(slider, (self.sliderX, self.sliderY))
                win.blit(top_bar, (0, 0))
                win.blit(play_button, (240, 10))
                win.blit(stats_button, (200, 250))
                pygame.draw.rect(win, (0, 0, 0), (40, 230, 70, 70))
                pygame.draw.rect(win, (colourrgb[colours[loops]]), (50, 240, 50, 50) )
                win.blit(text, (390, 170))
                win.blit(text2, (50, 210))
                win.blit(text3, (72, 310))
                win.blit(text4, (180, 430))
                if self.music:
                    win.blit(on, (240, 425))
                elif not self.music:
                    win.blit(off, (240, 425))
                pygame.display.update()

            self.snake_colour = colours[loops]
            gameConfig["colour"] = colours[loops]
            self.reSkin()
            self.paused = False

        def pauseGameCheck(self):
            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    end_sound.play()
                    pygame.time.delay(1000)
                    pygame.display.quit()
                    exit()
            clicked = pygame.mouse.get_pressed()
            if clicked[0]:
                mouse = pygame.mouse.get_pos()
                if 240 <= mouse[0] <= 260 and 10 <= mouse[1] <= 30:
                    return True

        def refresh(self):
            win.blit(bg, (0, 0))
            win.blit(top_bar, (0, 0))
            self.player.draw(win)
            pxy = myFont.render(str(self.player.x) + " " + str(self.player.y), False, (255, 255, 255))
            points = myFont.render(str(player.eatCount), False, (255, 255, 128))
            win.blit(pause_button, (240, 10))
            win.blit(pxy, (420, 10))
            win.blit(points, (10, 10))
            win.blit(apple_pic, (self.app.x, self.app.y))
            pygame.display.update()

        def reSkin(self):
            colour = self.snake_colour
            global snake_head, snake_head_up, snake_head_down, snake_head_down, snake_head_right, snake_tail, snake_eat, snake_dead
            snake_head = pygame.image.load('textures/snake_textures/{}/snake_head.png'.format(colour))
            snake_head_up = pygame.image.load('textures/snake_textures/{}/snake_head_up.png'.format(colour))
            snake_head_down = pygame.image.load('textures/snake_textures/{}/snake_head_down.png'.format(colour))
            snake_head_right = pygame.image.load('textures/snake_textures/{}/snake_head_right.png'.format(colour))
            snake_tail = pygame.image.load('textures/snake_textures/{}/snake_tail.png'.format(colour))
            snake_eat = pygame.image.load('textures/snake_textures/{}/snake_eat.png'.format(colour))
            snake_dead = pygame.image.load('textures/snake_textures/{}/snake_dead.png'.format(colour))

        def runGame(self):
            startup.play()
            self.run = True
            self.player_living = True
            bites = bool
            while self.run:
                # time delay# Do not put anything before, glitches happen#
                pygame.time.delay(50)
                keys = pygame.key.get_pressed()
                if not self.music:
                    pass
                elif self.music:
                    pass
                # refresh 1#
                self.refresh()
                if bool(self.player_living):
                    if self.checkClick(240, 260, 10, 30):
                        self.pause()
                    for events in pygame.event.get():
                        if events.type == pygame.QUIT:
                            self.run = False
                            end_sound.play()
                            pygame.time.delay(1000)
                            pygame.display.quit()
                            pygame.quit()
                            exit()
                    if keys[pygame.K_ESCAPE]:
                        self.pause()
                    self.coordinates.append((self.player.x, self.player.y))
                    if len(self.coordinates) > self.player.eatCount:
                        del self.coordinates[0]
                    for events in pygame.event.get():
                        if events.type == pygame.QUIT:
                            self.run = False
                    # Detecting the keys#
                    # refresh 2#
                    self.refresh()
                    if keys[pygame.K_ESCAPE]:
                        self.pause()
                    self.paused = self.pauseGameCheck()
                    self.keyPress()
                    # refresh 3#
                    self.refresh()
                    self.paused = self.pauseGameCheck()
                    if self.player.eatCount > self.high_score:
                        self.high_score = self.player.eatCount
                    # moving#
                    # refresh 4#
                    self.refresh()
                    if keys[pygame.K_ESCAPE]:
                        self.pause()
                    self.move(self.orient)
                    for i in range(len(self.coordinates)):
                        if (self.player.x, self.player.y) == self.coordinates[i]:
                            self.player_living = False
                    if self.player.x > 500:
                        self.player_living = bool
                        self.player_living = False
                    if self.player.y < 50:
                        self.player_living = bool
                        self.player_living = False
                    if self.player.x < 0:
                        self.player_living = bool
                        self.player_living = False
                    if self.player.y > 500:
                        self.player_living = bool
                        self.player_living = False
                    retry = bool
                    self.keyPress()
                    # refresh 5#
                    if keys[pygame.K_ESCAPE]:
                        self.pause()
                    self.refresh()
                    self.paused = self.pauseGameCheck()
                    if not self.player_living:
                        death_sound.play()
                        self.deaths += 1
                        self.app.x = (randint(6, 45) * 10)
                        self.app.y = (randint(6, 45) * 10)
                        retry = self.endgame()
                        if retry:
                            self.coordinates.clear()
                            self.player.eatCount = 0
                            self.player.x = 220
                            self.player.y = 200
                            self.player.face = 90
                            self.player_living = True
                            self.orient = ""
                        elif not retry:
                            self.gamesPlayed+=1
                            self.player.eatCount = 0
                            e = self.end()
                            self.run = True
                            return 0
                    self.paused = self.pauseGameCheck()
                    self.paused = self.pauseGameCheck()
                    # refresh 6#
                    self.keyPress()
                    self.refresh()
                    if self.paused:
                        self.pause()
                    if self.fileLoops == 1000:
                        gameData["highest score"] = self.high_score
                        gameData["deaths"] = self.deaths
                        gameData["moves"] = self.moves
                        with open('Data/gameData.json', 'w') as f:
                            json.dump(gameData, f)
                        self.fileLoops = 0
                    bites = self.bite()
                    # refresh 7#
                    self.refresh()

        def runStats(self):
            while True:
                for events in pygame.event.get():
                    if events.type == pygame.QUIT:
                        end_sound.play()
                        pygame.time.delay(1000)
                        pygame.display.quit()
                        exit()
                win.blit(statistics, (0, 0))
                win.blit(exit_button, (240, 0))
                score = myFont.render("High Score: " + str(gameData["highest score"]), False, (0, 0, 0))
                deaths = myFont.render("Deaths: " + str(gameData["deaths"]), False, (0, 0, 0))
                moves = myFont.render("Total Moves: " + str(gameData["moves"]), False, (0, 0, 0))
                if self.checkClick(240, 260, 10, 30):
                    break
                win.blit(score, (100, 250))
                win.blit(deaths, (100, 300))
                win.blit(moves, (100, 350))
                pygame.display.update()

        def setSpeed(self):
            click = pygame.mouse.get_pressed()
            if click[0]:
                mouse = pygame.mouse.get_pos()
                if 400 <= mouse[0] <= 415:
                    if 200 <= mouse[1] <= 230:
                        self.player.vel = 10
                        self.sliderY = 200
                        gameConfig["speed"] = 10
                    elif 231 <= mouse[1] <= 260:
                        self.player.vel = 5
                        self.sliderY = 245
                        gameConfig["speed"] = 5
                    elif 261 <= mouse[1] <= 290:
                        self.player.vel = 3
                        self.sliderY = 290
                        gameConfig["speed"] = 3


    # END of classes#
    # creating variables#
    myFont = pygame.font.SysFont('Lato', 16)
    player = snake(200, 220, 10, 10)
    game = Game(player)
    game.beginGame()
    game.runGame()
    gameData["games played"] = game.gamesPlayed
    gameData["highest score"] = game.high_score
    gameData["deaths"] = game.deaths
    gameData["moves"] = game.moves
    gameConfig["Music"] = game.music
    with open('Data/gameData.json', 'w') as f:
        json.dump(gameData, f)
    with open('Data/gameConfig.json', 'w') as f:
        json.dump(gameConfig, f)
    end_sound.play()
    pygame.display.quit()
    pygame.quit()
    exit()
except FileNotFoundError:
    while True:
        pygame.init()
        red = (255, 0, 0)
        win = pygame.display.set_mode((500, 500))
        win.fill(red)
        font = pygame.font.SysFont('Lato', 25)
        Err = font.render("ERROR IMPORTANT: ", False, (0, 0, 0))
        Gam = font.render("GAME FILES NOT FOUND ", False, (0, 0, 0))
        Plz = font.render("PLEASE RECOVER FILES", False, (0, 0, 0))
        win.blit(Err, (100, 50))
        win.blit(Gam, (100, 100))
        win.blit(Plz, (100, 150))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
