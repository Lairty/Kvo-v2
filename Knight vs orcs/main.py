import pygame
from mainGameBoard import mainGameBoard
from PyQt5.QtWidgets import QApplication
from Menu import FormStarting, Registration
import names
import sys
import sqlite3
from random import choice


pygame.init()
NEWENEMYCREATE = pygame.USEREVENT + 1
ENEMYMOVE = pygame.USEREVENT + 2
DELHEROATTACK = pygame.USEREVENT + 3
DELENEMYATTACK = pygame.USEREVENT + 4
CREATEITEM = pygame.USEREVENT + 5
MOREHARD = pygame.USEREVENT + 6
SCORETIC = pygame.USEREVENT + 7
pygame.time.set_timer(NEWENEMYCREATE, 10000)
pygame.time.set_timer(ENEMYMOVE, 1500)
pygame.time.set_timer(DELHEROATTACK, 500)
pygame.time.set_timer(DELENEMYATTACK, 1500)
pygame.time.set_timer(CREATEITEM, 2000)
pygame.time.set_timer(MOREHARD, 7000)
pygame.time.set_timer(SCORETIC, 1000)
size = width, height = 1280, 720
clock = pygame.time.Clock()
screen = False
fps = 60
running = True
while running:
    if names.closing:
        running = False
        break
    if names.upd:
        pygame.time.set_timer(DELHEROATTACK, names.delHer)
        names.upd = False
    if screen is False and names.closing is False:
        screen = pygame.display.set_mode(size)
        screen.fill((0, 0, 0))
        pygame.display.flip()
        mgb = mainGameBoard(32, 18, 5, "grass_top.png", "charecter.png", "enemyImage.png", screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                names.pause = not names.pause
            if event.key == pygame.K_l and not mgb.hasInventory:
                screen = mgb.log()
            if event.key == pygame.K_i and not mgb.hasLog:
                screen = mgb.showInventory()
            if event.key == pygame.K_1 and mgb.hasInventory:
                mgb.showInfoAbout("head")
            if event.key == pygame.K_2 and mgb.hasInventory:
                mgb.showInfoAbout("body")
            if event.key == pygame.K_3 and mgb.hasInventory:
                mgb.showInfoAbout("arms")
            if event.key == pygame.K_4 and mgb.hasInventory:
                mgb.showInfoAbout("legs")
            if event.key == pygame.K_5 and mgb.hasInventory:
                mgb.showInfoAbout("weapon")
            if event.key == pygame.K_6 and mgb.hasInventory:
                mgb.showInfoAbout("shild")
            if event.key == pygame.K_m and mgb.hasLog:
                mgb.showInfoAbout("shild")
        if not names.pause:
            if event.type == CREATEITEM:
                mgb.randomItemInRandomPlace()
            if event.type == SCORETIC:
                names.score += 1
            if event.type == MOREHARD:
                if names.k > 500:
                    pygame.time.set_timer(ENEMYMOVE, int(names.k))
                    pygame.time.set_timer(DELENEMYATTACK, int(names.k))
                    names.k *= 0.9
                if names.sHp <= mgb.player.hp:
                    names.sHp *= names.kH
                if names.sAt <= mgb.player.attackDamage:
                    names.sAt *= names.kH
                if names.sD <= mgb.player.defense:
                    names.sD *= names.kH
            if event.type == NEWENEMYCREATE or len(mgb.enemys) == 0:
                if len(mgb.enemys) < 10:
                    mgb.moreEnemys()
            if event.type == ENEMYMOVE:
                mgb.moveToHeroAndAttack()
            if event.type == DELHEROATTACK:
                mgb.del_attack()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT and names.game \
                    and mgb.attack_coords == (0, 0):
                mgb.get_click(event.pos)
            if event.type == DELENEMYATTACK:
                mgb.delEnemyAttack()
            if event.type == pygame.KEYDOWN and names.game:
                if event.key == pygame.K_w:
                    mgb.go("up")
                if event.key == pygame.K_s:
                    mgb.go("down")
                if event.key == pygame.K_d:
                    mgb.go("right")
                if event.key == pygame.K_a:
                    mgb.go("left")
    if names.menu:
        names.menu = False
        names.game = True
    if names.game:
        screen.fill((0, 0, 0), (0, 0, width, height))
        mgb.render(screen)
    if names.score >= names.lvlK:
        names.score -= int(names.lvlK)
        names.lvlK *= names.kH
        names.pLvl += 1
        mgb.player.hp = mgb.player.maxHp
        cub = choice([1, 2, 3, 4])
        mgb.showMesegesInLog(screen, "Вы повсили уровень.", pygame.Color('blue'))
        if cub == 1:
            k = choice([1, 2, 3])
            names.pS += k
            mgb.showMesegesInLog(screen, "Вы получили {} силы.".format(k), pygame.Color('blue'))
        elif cub == 2:
            k = choice([1, 2, 3])
            names.pAg += k
            mgb.showMesegesInLog(screen, "Вы получили {} ловкости.".format(k), pygame.Color('blue'))
            if names.delHer >= 250:
                names.delHer = names.delHer - k * 50
            pygame.time.set_timer(DELHEROATTACK, names.delHer)
        elif cub == 3:
            k = choice([10, 20, 30])
            names.pHp += k
            mgb.showMesegesInLog(screen, "Вы получили {} здоровья.".format(k), pygame.Color('blue'))
        elif cub == 4:
            k = choice([5, 10, 15])
            names.pAt += k
            mgb.showMesegesInLog(screen, "Вы получили {} урона.".format(k), pygame.Color('blue'))
        mgb.recalc_Eqip()
    pygame.display.flip()
    clock.tick(fps)
if names.player_login != '' and names.player_coords != '':
    con = sqlite3.connect('database/database.db')
    cur = con.cursor()
    cur.execute(
        'UPDATE players SET position = "{cor}",'
        ' helm = "{helm}",'
        ' cuirass = "{cuirass}",'
        ' weapon = "{weapon}",'
        ' legs = "{legs}",'
        ' Str = "{str}",'
        ' Agil = "{ag}",'
        ' At = "{at}",'
        ' MaxHp = "{maxHp}",'
        ' Hp = "{hp}",'
        ' Lvl = "{lvl}",'
        ' shild = "{shild}" WHERE login = "{log}"'.format(
            cor=str(names.player_coords[0]) + ' ' + str(names.player_coords[1]),
            log=names.player_login,
            helm=list(cur.execute('SELECT id FROM items WHERE name = "{name}"'.format(name=mgb.player.head.name)))[0][0],
            cuirass=list(cur.execute('SELECT id FROM items WHERE name = "{name}"'.format(name=mgb.player.body.name)))[0][0],
            weapon=list(cur.execute('SELECT id FROM items WHERE name = "{name}"'.format(name=mgb.player.weapon.name)))[0][0],
            legs=list(cur.execute('SELECT id FROM items WHERE name = "{name}"'.format(name=mgb.player.legs.name)))[0][0],
            shild=list(cur.execute('SELECT id FROM items WHERE name = "{name}"'.format(name=mgb.player.shild.name)))[0][0],
            str=names.pS, ag=names.pAg, at=names.pAt, maxHp=mgb.player.maxHp, hp=mgb.player.hp, lvl=names.pLvl
        )
    )
    con.commit()
names.game = False
names.menu = True
pygame.quit()
names.closing = False
