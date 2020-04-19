import pygame
from Board import Board
from LoadImage import load_image
from backImageSprites import BackImage
import random
from Player import Player, PlayerSprites
from Enemys import Enemy, EnemySprites
import names
import sqlite3
from askItem import askItem
from Items import Item
from names import score
import sys
from PyQt5.QtWidgets import QApplication


class mainGameBoard(Board):
    def __init__(self, width, height, enemyCount, backImage, playerImage, enemyImage, screen):
        super().__init__(width, height)
        self.screen = screen
        self.itemsOnTheMap = dict()
        self.codes = {
            30: 'head', 31: 'body', 32: 'arms', 33: 'legs', 34: 'weapon', 35: 'shild'
        }
        self.attack_coords = (0, 0)
        self.backImage = load_image(backImage, -1)
        self.playerImage = load_image(playerImage, -1)
        self.backSprites = pygame.sprite.Group()
        self.playerSprites = pygame.sprite.Group()
        self.EnemySprites = pygame.sprite.Group()
        self.dora = 1
        self.EnemyImage = load_image(enemyImage)
        self.headImage = load_image("head.png")
        self.bodyImage = load_image("body.png")
        self.armsImage = load_image("arms.png")
        self.legsImage = load_image("legs.png")
        self.weaponImage = load_image("weapon.png")
        self.shildImage = load_image("shild.png")
        self.enemys = []
        self.pause = False
        self.attack_dir = ""
        self.player = Player((random.randint(0, 31), random.randint(0, 17)), self.playerImage, "")
        self.con = sqlite3.connect('database/database.db')
        self.cur = self.con.cursor()
        self.player_coords = list(self.cur.execute(
            "SELECT position FROM players WHERE login = '{log}'".format(log=names.player_login)
        ))[0][0].split()
        self.player = Player((int(self.player_coords[0]), int(self.player_coords[1])), self.playerImage, "")
        names.player_coords = (int(self.player_coords[0]), int(self.player_coords[1]))
        self.board[self.player.return_coords()[0]][self.player.return_coords()[1]] = 1
        self.EnemySpr = []
        self.eqip = [self.player.head, self.player.body, self.player.arms,
                     self.player.legs, self.player.weapon, self.player.shild]
        self.hasInventory = False
        self.hasLog = False
        self.EAU = False
        self.EAD = False
        self.EAR = False
        self.EAL = False
        self.items = [i[0] for i in self.cur.execute('SELECT name FROM items').fetchall()]
        self.itemOnBoard = 0
        self.logMeseges = []
        self.recalc_Eqip()
        for i in range(enemyCount):
            x = random.randint(0, 31)
            y = random.randint(0, 17)
            while self.board[x][y] != -1:
                x = random.randint(0, 31)
                y = random.randint(0, 17)
            enemy = Enemy((x, y), self.EnemyImage, "")
            self.enemys.append(enemy)
            self.EnemySpr.append(EnemySprites(self.EnemySprites, enemy.return_image(),
                                           (enemy.coords[0] * 40, enemy.coords[1] * 40)))
            self.board[x][y] = 2
        self.playerSpr = PlayerSprites(self.playerSprites, self.player.return_image(),
                                       (self.player.coords[0] * 40, self.player.coords[1] * 40))
        self.blade_left = load_image("blade_left.png", -1)
        self.blade_right = load_image("blade_right.png", -1)
        self.blade_down = load_image("blade_down.png", -1)
        self.blade_up = load_image("blade_up.png", -1)
        for row in range(self.height):
            for col in range(self.width):
                rect = pygame.Rect(
                    self.left + self.cell_size * col,
                    self.top + self.cell_size * row,
                    self.cell_size, self.cell_size
                )
                BackImage(self.backSprites, self.backImage, rect)

    def updateEnemys(self):
        for i in self.enemys:
            if i.hp <= 0:
                for j in self.EnemySprites:
                    if i.coords[0] * 40 == j.rect.x and i.coords[1] * 40 == j.rect.y:
                        self.EnemySprites.remove(j)
                        break
                self.enemys.remove(i)
                self.board[i.coords[0]][i.coords[1]] = -1
                names.score += names.ScoreK
                if self.hasLog:
                    self.showMesegesInLog(self.screen, "Вы убили орка. И получили {} очков".format(names.ScoreK))
                    self.showMesegesInLog(self.screen, "")

    def render(self, screen):
        self.backSprites.draw(screen)
        self.playerSprites.draw(screen)
        self.EnemySprites.draw(screen)
        for row in range(self.height):
            for col in range(self.width):
                rect = pygame.Rect(
                    self.left + self.cell_size * col,
                    self.top + self.cell_size * row,
                    self.cell_size, self.cell_size
                )
                pygame.draw.rect(screen, self.color, rect, 1)
                if self.board[col][row] == -5 or self.board[col][row] == 10:
                    screen.blit(self.blade_left, (col * 40, row * 40))
                if self.board[col][row] == -6 or self.board[col][row] == 12:
                    screen.blit(self.blade_down, (col * 40, row * 40))
                if self.board[col][row] == -7 or self.board[col][row] == 14:
                    screen.blit(self.blade_right, (col * 40, row * 40))
                if self.board[col][row] == -8 or self.board[col][row] == 16:
                    screen.blit(self.blade_up, (col * 40, row * 40))
                if self.board[col][row] == 30:
                    screen.blit(self.headImage, (col * 40, row * 40))
                if self.board[col][row] == 31:
                    screen.blit(self.bodyImage, (col * 40, row * 40))
                if self.board[col][row] == 32:
                    screen.blit(self.armsImage, (col * 40, row * 40))
                if self.board[col][row] == 33:
                    screen.blit(self.legsImage, (col * 40, row * 40))
                if self.board[col][row] == 34:
                    screen.blit(self.weaponImage, (col * 40, row * 40))
                if self.board[col][row] == 35:
                    screen.blit(self.shildImage, (col * 40, row * 40))

    def on_click(self, cell_coords):
        if cell_coords:
            if cell_coords[0] == self.player.coords[0] - 1 and cell_coords[1] == self.player.coords[1]:
                if self.board[self.player.coords[0] - 1][self.player.coords[1]] == -1 or \
                        self.board[self.player.coords[0] - 1][self.player.coords[1]] == 2:
                    self.board[self.player.coords[0] - 1][self.player.coords[1]] *= 5
                    self.attack_coords = (self.player.coords[0] - 1, self.player.coords[1])
                    self.attack_dir = "left"
            elif cell_coords[0] == self.player.coords[0] + 1 and cell_coords[1] == self.player.coords[1]:
                if self.board[self.player.coords[0] + 1][self.player.coords[1]] == -1 or \
                        self.board[self.player.coords[0] + 1][self.player.coords[1]] == 2:
                    self.board[self.player.coords[0] + 1][self.player.coords[1]] *= 7
                    self.attack_coords = (self.player.coords[0] + 1, self.player.coords[1])
                    self.attack_dir = "right"
            elif - 1 <= self.player.coords[0] - cell_coords[0] <= 1:
                if self.player.coords[1] > cell_coords[1]:
                    if self.board[self.player.coords[0]][self.player.coords[1] - 1] == -1 or \
                            self.board[self.player.coords[0]][self.player.coords[1] - 1] == 2:
                        self.board[self.player.coords[0]][self.player.coords[1] - 1] *= 8
                        self.attack_coords = (self.player.coords[0], self.player.coords[1] - 1)
                        self.attack_dir = "up"
                if self.player.coords[1] < cell_coords[1]:
                    if self.board[self.player.coords[0]][self.player.coords[1] + 1] == -1 or \
                            self.board[self.player.coords[0]][self.player.coords[1] + 1] == 2:
                        self.board[self.player.coords[0]][self.player.coords[1] + 1] *= 6
                        self.attack_coords = (self.player.coords[0], self.player.coords[1] + 1)
                        self.attack_dir = "down"
            elif - 1 <= self.player.coords[1] - cell_coords[1] <= 1:
                if self.player.coords[0] > cell_coords[0]:
                    if self.board[self.player.coords[0] - 1][self.player.coords[1]] == -1 or \
                            self.board[self.player.coords[0] - 1][self.player.coords[1]] == 2:
                        self.board[self.player.coords[0] - 1][self.player.coords[1]] *= 5
                        self.attack_coords = (self.player.coords[0] - 1, self.player.coords[1])
                        self.attack_dir = "left"
                if self.player.coords[0] < cell_coords[0]:
                    if self.board[self.player.coords[0] + 1][self.player.coords[1]] == -1 or \
                            self.board[self.player.coords[0] + 1][self.player.coords[1]] == 2:
                        self.board[self.player.coords[0] + 1][self.player.coords[1]] *= 7
                        self.attack_coords = (self.player.coords[0] + 1, self.player.coords[1])
                        self.attack_dir = "right"
        if self.board[self.attack_coords[0]][self.attack_coords[1]] > 0:
            for i in self.enemys:
                if i.coords == self.attack_coords:
                    self.player.attack(i)
                    if self.hasLog:
                        self.showMesegesInLog(self.screen,
                                              "Вы нанесли {} урона орку.".format(self.player.attackDamage))
                        self.showMesegesInLog(self.screen,
                                              "У него осталось {} хп из {}".format(i.hp, int(names.sHp)))
                        if i.hp > 0:
                            self.showMesegesInLog(self.screen, "")
            self.updateEnemys()

    def del_attack(self):
        if self.board[self.attack_coords[0]][self.attack_coords[1]] < 0:
            self.board[self.attack_coords[0]][self.attack_coords[1]] = -1
        else:
            if self.attack_dir == "left":
                self.board[self.attack_coords[0]][self.attack_coords[1]] /= 5
            if self.attack_dir == "right":
                self.board[self.attack_coords[0]][self.attack_coords[1]] /= 7
            if self.attack_dir == "down":
                self.board[self.attack_coords[0]][self.attack_coords[1]] /= 6
            if self.attack_dir == "up":
                self.board[self.attack_coords[0]][self.attack_coords[1]] /= 8
        self.attack_dir = ""
        self.attack_coords = (0, 0)

    def go(self, dir):
        if dir == "up":
            if self.player.coords[1] != 0:
                if self.board[self.player.coords[0]][self.player.coords[1] - 1] == -1:
                    self.board[self.player.coords[0]][self.player.coords[1] - 1] = 1
                    self.board[self.player.coords[0]][self.player.coords[1]] = -1
                    self.player.coords = (self.player.coords[0], self.player.coords[1] - 1)
                    self.playerSpr.update("up")
                elif self.board[self.player.coords[0]][self.player.coords[1] - 1] >= 30:
                    self.askItem(
                        self.codes[self.board[self.player.coords[0]][self.player.coords[1] - 1]],
                        self.itemsOnTheMap[str(self.player.coords[0]) + ' ' + str(self.player.coords[1] - 1)],
                        self.player.eq[self.codes[self.board[self.player.coords[0]][self.player.coords[1] - 1]]]
                    )
                    self.board[self.player.coords[0]][self.player.coords[1] - 1] = 1
                    self.board[self.player.coords[0]][self.player.coords[1]] = -1
                    self.player.coords = (self.player.coords[0], self.player.coords[1] - 1)
                    self.playerSpr.update("up")
        if dir == "down":
            if self.player.coords[1] + 1 != self.height:
                if self.board[self.player.coords[0]][self.player.coords[1] + 1] == -1:
                    self.board[self.player.coords[0]][self.player.coords[1] + 1] = 1
                    self.board[self.player.coords[0]][self.player.coords[1]] = -1
                    self.player.coords = (self.player.coords[0], self.player.coords[1] + 1)
                    self.playerSpr.update("down")
                elif self.board[self.player.coords[0]][self.player.coords[1] + 1] >= 30:
                    self.askItem(
                        self.codes[self.board[self.player.coords[0]][self.player.coords[1] + 1]],
                        self.itemsOnTheMap[str(self.player.coords[0]) + ' ' + str(self.player.coords[1] + 1)],
                        self.player.eq[self.codes[self.board[self.player.coords[0]][self.player.coords[1] + 1]]]
                    )
                    self.board[self.player.coords[0]][self.player.coords[1] + 1] = 1
                    self.board[self.player.coords[0]][self.player.coords[1]] = -1
                    self.player.coords = (self.player.coords[0], self.player.coords[1] + 1)
                    self.playerSpr.update("down")
        if dir == "right":
            if self.player.coords[0] + 1 != self.width:
                if self.board[self.player.coords[0] + 1][self.player.coords[1]] == -1:
                    self.board[self.player.coords[0] + 1][self.player.coords[1]] = 1
                    self.board[self.player.coords[0]][self.player.coords[1]] = -1
                    self.player.coords = (self.player.coords[0] + 1, self.player.coords[1])
                    self.playerSpr.update("right")
                elif self.board[self.player.coords[0] + 1][self.player.coords[1]] >= 30:
                    self.askItem(
                        self.codes[self.board[self.player.coords[0] + 1][self.player.coords[1]]],
                        self.itemsOnTheMap[str(self.player.coords[0] + 1) + ' ' + str(self.player.coords[1])],
                        self.player.eq[self.codes[self.board[self.player.coords[0] + 1][self.player.coords[1]]]]
                    )
                    self.board[self.player.coords[0] + 1][self.player.coords[1]] = 1
                    self.board[self.player.coords[0]][self.player.coords[1]] = -1
                    self.player.coords = (self.player.coords[0] + 1, self.player.coords[1])
                    self.playerSpr.update("right")
        if dir == "left":
            if self.player.coords[0] != 0:
                if self.board[self.player.coords[0] - 1][self.player.coords[1]] == -1:
                    self.board[self.player.coords[0] - 1][self.player.coords[1]] = 1
                    self.board[self.player.coords[0]][self.player.coords[1]] = -1
                    self.player.coords = (self.player.coords[0] - 1, self.player.coords[1])
                    self.playerSpr.update("left")
                elif self.board[self.player.coords[0] - 1][self.player.coords[1]] >= 30:
                    self.askItem(
                        self.codes[self.board[self.player.coords[0] - 1][self.player.coords[1]]],
                        self.itemsOnTheMap[str(self.player.coords[0] - 1) + ' ' + str(self.player.coords[1])],
                        self.player.eq[self.codes[self.board[self.player.coords[0] - 1][self.player.coords[1]]]]
                    )
                    self.board[self.player.coords[0] - 1][self.player.coords[1]] = 1
                    self.board[self.player.coords[0]][self.player.coords[1]] = -1
                    self.player.coords = (self.player.coords[0] - 1, self.player.coords[1])
                    self.playerSpr.update("left")
        names.player_coords = self.player.return_coords()

    def log(self):
        if not self.hasLog:
            self.hasLog = True
            screen = pygame.display.set_mode((self.currentWidth + 300, self.currentHeight))
            self.currentWidth += 300
            screen.fill((0, 0, 0), (self.standartWidth * 40, 0, 300, self.standartHeight * 40))
            self.render(screen)
            self.screen = screen
            return screen
        else:
            self.hasLog = False
            screen = pygame.display.set_mode((self.currentWidth - 300, self.currentHeight))
            self.currentWidth -= 300
            self.render(screen)
            self.screen = screen
            self.logMeseges = []
            return screen

    def showMesegesInLog(self, screen, messege, color=(255, 255, 255)):
        font = pygame.font.Font(None, 25)
        text = font.render(messege, 1, color)
        text_x = self.standartWidth * 40 + 10
        text_y = 5 + text.get_height() * len(self.logMeseges)
        if text_y >= self.height * 40 and messege != "":
            self.logMeseges = []
            text_y = 5 + text.get_height() * len(self.logMeseges)
            screen.fill((0, 0, 0), (self.standartWidth * 40, 0, 300, self.standartHeight * 40))
        screen.blit(text, (text_x, text_y))
        self.logMeseges.append(text)

    def moreEnemys(self):
        x = random.randint(0, 31)
        y = random.randint(0, 17)
        while self.board[x][y] != -1:
            x = random.randint(0, 31)
            y = random.randint(0, 17)
        enemy = Enemy((x, y), self.EnemyImage, "")
        self.enemys.append(enemy)
        self.EnemySpr.append(EnemySprites(self.EnemySprites, enemy.return_image(),
                                          (enemy.coords[0] * 40, enemy.coords[1] * 40)))
        self.board[x][y] = 2

    def moveToHeroAndAttack(self):
        for i in self.enemys:
            if i.coords[0] - self.player.coords[0] == 0 and i.coords[1] - self.player.coords[1] == 1:
                self.attackOrc("up", i)
            elif i.coords[0] - self.player.coords[0] == 0 and i.coords[1] - self.player.coords[1] == -1:
                self.attackOrc("down", i)
            elif i.coords[0] - self.player.coords[0] == 1 and i.coords[1] - self.player.coords[1] == 0:
                self.attackOrc("left", i)
            elif i.coords[0] - self.player.coords[0] == -1 and i.coords[1] - self.player.coords[1] == 0:
                self.attackOrc("right", i)
            elif i.coords[0] - self.player.coords[0] == 0:
                if i.coords[1] < self.player.coords[1]:
                    if self.board[i.coords[0]][i.coords[1] + 1] == -1 or self.board[i.coords[0]][i.coords[1] + 1] >= 30\
                            or i.coords[0] == self.attack_coords[0] and i.coords[1] + 1 == self.attack_coords[1] \
                            and self.board[i.coords[0]][i.coords[1] + 1] != 2:
                        self.board[i.coords[0]][i.coords[1]] = -1
                        self.board[i.coords[0]][i.coords[1] + 1] = 2
                        for j in self.EnemySprites:
                            if i.coords[0] * 40 == j.rect.x and i.coords[1] * 40 == j.rect.y:
                                j.update("down")
                                break
                        i.set_coords((i.coords[0], i.coords[1] + 1))
                if i.coords[1] > self.player.coords[1]:
                    if self.board[i.coords[0]][i.coords[1] - 1] == -1 or self.board[i.coords[0]][i.coords[1] - 1] >= 30\
                            or i.coords[0] == self.attack_coords[0] and i.coords[1] - 1 == self.attack_coords[1] \
                            and self.board[i.coords[0]][i.coords[1] - 1] != 2:
                        self.board[i.coords[0]][i.coords[1]] = -1
                        self.board[i.coords[0]][i.coords[1] - 1] = 2
                        for j in self.EnemySprites:
                            if i.coords[0] * 40 == j.rect.x and i.coords[1] * 40 == j.rect.y:
                                j.update("up")
                                break
                        i.set_coords((i.coords[0], i.coords[1] - 1))
            elif i.coords[0] < self.player.coords[0]:
                if self.board[i.coords[0] + 1][i.coords[1]] == -1 or self.board[i.coords[0] + 1][i.coords[1]] >= 30 \
                        or i.coords[0] + 1 == self.attack_coords[0] and i.coords[1] == self.attack_coords[1]\
                        and self.board[i.coords[0] + 1][i.coords[1]] != 2:
                    self.board[i.coords[0]][i.coords[1]] = -1
                    self.board[i.coords[0] + 1][i.coords[1]] = 2
                    for j in self.EnemySprites:
                        if i.coords[0] * 40 == j.rect.x and i.coords[1] * 40 == j.rect.y:
                            j.update("right")
                            break
                    i.set_coords((i.coords[0] + 1, i.coords[1]))
            elif i.coords[0] > self.player.coords[0]:
                if self.board[i.coords[0] - 1][i.coords[1]] == -1 or self.board[i.coords[0] - 1][i.coords[1]] >= 30 \
                        or i.coords[0] - 1 == self.attack_coords[0] and i.coords[1] == self.attack_coords[1] \
                        and self.board[i.coords[0] - 1][i.coords[1]] != 2:
                    self.board[i.coords[0]][i.coords[1]] = -1
                    self.board[i.coords[0] - 1][i.coords[1]] = 2
                    for j in self.EnemySprites:
                        if i.coords[0] * 40 == j.rect.x and i.coords[1] * 40 == j.rect.y:
                            j.update("left")
                            break
                    i.set_coords((i.coords[0] - 1, i.coords[1]))

    def attackOrc(self, dir, orc):
        if dir == "up" and not self.EAU:
            self.EAU = True
            orc.attack(self.player)
        if dir == "down" and not self.EAD:
            self.EAD = True
            orc.attack(self.player)
        if dir == "right" and not self.EAR:
            self.EAR = True
            orc.attack(self.player)
        if dir == "left" and not self.EAL:
            self.EAL = True
            orc.attack(self.player)
        if self.hasLog:
            self.showMesegesInLog(self.screen,
                                  "Вам нанесли {} урона.".format(orc.attackDamage),
                                  pygame.Color("red"))
            self.showMesegesInLog(self.screen, "У вас осталось {} хр из {}.".format(self.player.hp, self.player.maxHp),
                                  pygame.Color("red"))
            self.showMesegesInLog(self.screen, "")
        if self.player.hp <= 0:
            self.restart()

    def delEnemyAttack(self):
        self.EAU = False
        self.EAD = False
        self.EAR = False
        self.EAL = False

    def restart(self):
        self.showMesegesInLog(self.screen, "Вы умерли. Набрав {} очков.".format(names.score),
                              pygame.Color("green"))
        self.showMesegesInLog(self.screen, "У вас был {} уровень".format(names.pLvl), pygame.Color("green"))
        self.board = [[-1] * self.height for _ in range(self.width)]
        self.enemys = []
        self.backSprites = pygame.sprite.Group()
        self.playerSprites = pygame.sprite.Group()
        self.EnemySprites = pygame.sprite.Group()
        self.attack_dir = ""
        self.player = Player((random.randint(0, 31), random.randint(0, 17)), self.playerImage, "", restart=True)
        self.board[self.player.return_coords()[0]][self.player.return_coords()[1]] = 1
        self.recalc_Eqip()
        self.EnemySpr = []
        names.sHp = 100
        names.sAt = 20
        names.sD = 1
        names.lvlK = 100
        names.score = 0
        names.k = 1500
        names.delHer = 500
        names.upd = True
        self.EAU = False
        self.EAD = False
        self.EAR = False
        self.EAL = False
        for i in range(5):
            x = random.randint(0, 31)
            y = random.randint(0, 17)
            while self.board[x][y] != -1:
                x = random.randint(0, 31)
                y = random.randint(0, 17)
            enemy = Enemy((x, y), self.EnemyImage, "")
            self.enemys.append(enemy)
            self.EnemySpr.append(EnemySprites(self.EnemySprites, enemy.return_image(),
                                              (enemy.coords[0] * 40, enemy.coords[1] * 40)))
            self.board[x][y] = 2
        self.playerSpr = PlayerSprites(self.playerSprites, self.player.return_image(),
                                       (self.player.coords[0] * 40, self.player.coords[1] * 40))
        for row in range(self.height):
            for col in range(self.width):
                rect = pygame.Rect(
                    self.left + self.cell_size * col,
                    self.top + self.cell_size * row,
                    self.cell_size, self.cell_size
                )
                BackImage(self.backSprites, self.backImage, rect)

    def showInventory(self):
        if not self.hasInventory:
            self.hasInventory = True
            screen = pygame.display.set_mode((self.currentWidth, self.currentHeight + 100))
            self.currentHeight += 100
            self.render(screen)
            self.screen = screen
            font = pygame.font.Font(None, 25)
            text = font.render("На вас надето:", 1, (255, 255, 255))
            text_x = 5
            text_y = self.standartHeight * 40
            screen.blit(text, (text_x, text_y))

            if self.eqip[0] == 0:
                head = "ничего"
            else:
                head = self.eqip[0].name
            text = font.render("На голове: " + head, 1, (255, 255, 255))
            text_x = 5
            text_y = self.standartHeight * 40 + text.get_height()
            screen.blit(text, (text_x, text_y))

            if self.eqip[1] == 0:
                body = "ничего"
            else:
                body = self.eqip[1].name
            text = font.render("На теле: " + body, 1, (255, 255, 255))
            text_x = 5
            text_y = self.standartHeight * 40 + text.get_height() * 2
            screen.blit(text, (text_x, text_y))

            if self.eqip[2] == 0:
                arms = "ничего"
            else:
                arms = self.eqip[2].name
            text = font.render("На руках: " + arms, 1, (255, 255, 255))
            text_x = 5
            text_y = self.standartHeight * 40 + text.get_height() * 3
            screen.blit(text, (text_x, text_y))

            if self.eqip[3] == 0:
                legs = "ничего"
            else:
                legs = self.eqip[3].name
            text = font.render("На ногах: " + legs, 1, (255, 255, 255))
            text_x = 5
            text_y = self.standartHeight * 40 + text.get_height() * 4
            screen.blit(text, (text_x, text_y))

            if self.eqip[4] == 0:
                weapon = "кулаки"
            else:
                weapon = self.eqip[4].name
            text = font.render("Оружие: " + weapon, 1, (255, 255, 255))
            text_x = 5 + 300
            text_y = self.standartHeight * 40
            screen.blit(text, (text_x, text_y))

            if self.eqip[5] == 0:
                shild = "кулаки"
            else:
                shild = self.eqip[5].name
            text = font.render("Щит: " + shild, 1, (255, 255, 255))
            text_x = 5 + 300
            text_y = self.standartHeight * 40 + text.get_height()
            screen.blit(text, (text_x, text_y))
            return screen
        else:
            self.hasInventory = False
            screen = pygame.display.set_mode((self.currentWidth, self.currentHeight - 100))
            self.currentHeight -= 100
            screen.fill((0, 0, 0), pygame.Rect(0, self.standartHeight * 40, self.standartWidth * 40, 100))
            self.render(screen)
            self.screen = screen
            return screen

    def showNothing(self):
        font = pygame.font.Font(None, 25)
        text = font.render("Ничего: ", 1, (255, 255, 255))
        text_x = 5 + 400
        text_y = self.standartHeight * 40
        self.screen.blit(text, (text_x, text_y))
        text = font.render("Сила: 0", 1, (255, 255, 255))
        text_x = 5 + 400
        text_y = self.standartHeight * 40 + text.get_height()
        self.screen.blit(text, (text_x, text_y))
        text = font.render("Ловкость: 0", 1, (255, 255, 255))
        text_x = 5 + 400
        text_y = self.standartHeight * 40 + text.get_height() * 2
        self.screen.blit(text, (text_x, text_y))
        text = font.render("Интелект: 0", 1, (255, 255, 255))
        text_x = 5 + 400
        text_y = self.standartHeight * 40 + text.get_height() * 3
        self.screen.blit(text, (text_x, text_y))
        text = font.render("Защита: 0", 1, (255, 255, 255))
        text_x = 5 + 400
        text_y = self.standartHeight * 40 + text.get_height() * 4
        self.screen.blit(text, (text_x, text_y))

    def showInfo(self, name, strengh, agility, intelligent, wdora, dora):
        font = pygame.font.Font(None, 25)
        text = font.render("{}: ".format(name), 1, (255, 255, 255))
        text_x = 5 + 600
        text_y = self.standartHeight * 40
        self.screen.blit(text, (text_x, text_y))
        text = font.render("Сила: {}".format(strengh), 1, (255, 255, 255))
        text_x = 5 + 600
        text_y = self.standartHeight * 40 + text.get_height()
        self.screen.blit(text, (text_x, text_y))
        text = font.render("Ловкость: {}".format(agility), 1, (255, 255, 255))
        text_x = 5 + 600
        text_y = self.standartHeight * 40 + text.get_height() * 2
        self.screen.blit(text, (text_x, text_y))
        text = font.render("Интелект: {}".format(intelligent), 1, (255, 255, 255))
        text_x = 5 + 600
        text_y = self.standartHeight * 40 + text.get_height() * 3
        self.screen.blit(text, (text_x, text_y))
        if wdora == "a":
            text = font.render("Урон: {}".format(dora), 1, (255, 255, 255))
        else:
            text = font.render("Защита: {}".format(dora), 1, (255, 255, 255))
        text_x = 5 + 600
        text_y = self.standartHeight * 40 + text.get_height() * 4
        self.screen.blit(text, (text_x, text_y))

    def showInfoAbout(self, item):
        self.screen.fill((0, 0, 0), pygame.Rect(5 + 400, self.standartHeight * 40, 200, 200))
        if item == "head":
            if self.eqip[0] == 0:
                self.showNothing()
            else:
                self.showInfo(self.eqip[0].name, self.eqip[0].strength,
                              self.eqip[0].agility, self.eqip[0].intelligent, "d", self.eqip[0].dora)
        if item == "body":
            if self.eqip[1] == 0:
                self.showNothing()
            else:
                self.showInfo(self.eqip[1].name, self.eqip[1].strength,
                              self.eqip[1].agility, self.eqip[1].intelligent, "d", self.eqip[1].dora)
        if item == "arms":
            if self.eqip[2] == 0:
                self.showNothing()
            else:
                self.showInfo(self.eqip[2].name, self.eqip[2].strength,
                              self.eqip[2].agility, self.eqip[2].intelligent, "d", self.eqip[2].dora)
        if item == "legs":
            if self.eqip[3] == 0:
                self.showNothing()
            else:
                self.showInfo(self.eqip[3].name, self.eqip[3].strength,
                              self.eqip[3].agility, self.eqip[3].intelligent, "d", self.eqip[3].dora)
        if item == "weapon":
            if self.eqip[4] == 0:
                self.showInfo("Кулаки", 0,
                              0, 0, "a", 10)
            else:
                self.showInfo(self.eqip[4].name, self.eqip[4].strength,
                              self.eqip[4].agility, self.eqip[4].intelligent, "a", self.eqip[4].dora)
        if item == "shild":
            if self.eqip[5] == 0:
                self.showInfo("Кулаки", 0,
                              0, 0, "d", 0)
            else:
                self.showInfo(self.eqip[5].name, self.eqip[5].strength,
                              self.eqip[5].agility, self.eqip[5].intelligent, "d", self.eqip[5].dora)

    def updateEqip(self, old_numb, newItem):
        self.n_type = newItem.type
        if self.n_type == 'head':
            self.player.eq['head'] = newItem
            self.player.head = newItem
        elif self.n_type == 'body':
            self.player.eq['body'] = newItem
            self.player.body = newItem
        elif self.n_type == 'arms':
            self.player.eq['arms'] = newItem
            self.player.arms = newItem
        elif self.n_type == 'legs':
            self.player.eq['legs'] = newItem
            self.player.legs = newItem
        elif self.n_type == 'weapon':
            self.player.eq['weapon'] = newItem
            self.player.weapon = newItem
        elif self.n_type == 'shild':
            self.player.eq['shild'] = newItem
            self.player.shild = newItem
        self.eqip[old_numb] = newItem
        strength = 0
        agility = 0
        intelligent = 0
        defnse = 0
        attack = 0
        for i in range(6):
            strength += int(self.eqip[i].strength)
            agility += int(self.eqip[i].agility)
            intelligent += int(self.eqip[i].intelligent)
            if self.eqip[i].type == "weapon":
                attack += int(self.eqip[i].dora)
            else:
                defnse += int(self.eqip[i].dora)
        self.player.updateAtributs(strength, agility, intelligent, defnse, attack)

    def randomItemInRandomPlace(self):
        x = random.randint(0, 31)
        y = random.randint(0, 17)
        while self.board[x][y] != -1:
            x = random.randint(0, 31)
            y = random.randint(0, 17)
        self.choosenItem = random.choice(self.items)
        while self.choosenItem in ["free shild", "free ironwood's stick", "free boots", "free gloves",
                                   "free coat", "free mask"]:
            self.choosenItem = random.choice(self.items)
        self.itemsOnTheMap[str(x) + ' ' + str(y)] = Item(self.choosenItem)
        item = Item(self.choosenItem, (x, y))
        if item.type == "head":
            self.board[x][y] = 30
        if item.type == "body":
            self.board[x][y] = 31
        if item.type == "arms":
            self.board[x][y] = 32
        if item.type == "legs":
            self.board[x][y] = 33
        if item.type == "weapon":
            self.board[x][y] = 34
        if item.type == "shild":
            self.board[x][y] = 35

    def askItem(self, type, item1, item2):
        names.pause = True
        global aI
        aI = askItem(type, item1, item2, self)
        aI.show()
        if aI.ret:
            self.ifs(type, item1)

    def ifs(self, type, item1):
        if type == "head":
            self.updateEqip(0, item1)
        if type == "body":
            self.updateEqip(1, item1)
        if type == "arms":
            self.updateEqip(2, item1)
        if type == "legs":
            self.updateEqip(3, item1)
        if type == "weapon":
            self.updateEqip(4, item1)
        if type == "shild":
            self.updateEqip(5, item1)

    def recalc_Eqip(self):
        strength = 0
        agility = 0
        intelligent = 0
        defnse = 0
        attack = 0
        for i in range(6):
            strength += int(self.eqip[i].strength)
            agility += int(self.eqip[i].agility)
            intelligent += int(self.eqip[i].intelligent)
            if self.eqip[i].type == "weapon":
                attack += int(self.eqip[i].dora)
            else:
                defnse += int(self.eqip[i].dora)
        self.player.updateAtributs(strength, agility, intelligent, defnse, attack)
