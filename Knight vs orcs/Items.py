import pygame
import sqlite3


class Item:
    def __init__(self, name, *place):
        self.name = name
        self.place = place
        self.con = sqlite3.connect('database/database.db')
        self.cur = self.con.cursor()
        self.stats = [i for i in self.cur.execute(
            'SELECT strength, agility, intelligent, type, dora FROM items WHERE name = "{name}"'.format(name=self.name)
        ).fetchall()[0]]
        self.strength = self.stats[0]
        self.agility = self.stats[1]
        self.intelligent = self.stats[2]
        self.type = self.stats[3]
        self.dora = self.stats[4]
