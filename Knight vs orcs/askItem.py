import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
import names


class askItem(QMainWindow):
    def __init__(self, type, item1, item2, m):
        super().__init__()
        uic.loadUi('ui_files/askItem.ui', self)
        self.item1 = item1
        self.m = m
        self.item2 = item2
        self.type = type
        self.name1.setText(item1.name)
        self.str1.setText("Сила: " + item1.strength)
        self.agl1.setText("Ловкость: " + item1.agility)
        self.int1.setText("Интелект: " + item1.intelligent)
        if type == "weapon":
            self.dora.setText("Урон: " + item1.dora)
        else:
            self.dora.setText("Защита: " + item1.dora)
        if item2 != 0:
            self.name2.setText(item2.name)
            self.str2.setText("Сила: " + item2.strength)
            self.agl2.setText("Ловкость: " + item2.agility)
            self.int2.setText("Интелект: " + item2.intelligent)
            if type == "weapon":
                self.dora2.setText("Урон: " + item2.dora)
            else:
                self.dora2.setText("Защита: " + item2.dora)
        else:
            self.name2.setText(item1.name)
            if type == "weapon" or type == "shild":
                self.name2.setText("Кулаки")
            else:
                self.name2.setText("Ничего")
            self.str2.setText("Сила: " + "0")
            self.agl2.setText("Ловкость: " + "0")
            self.int2.setText("Интелект: " + "0")
            if type == "weapon":
                self.dora2.setText("Урон: " + "10")
            else:
                self.dora2.setText("Защита: " + "0")
        self.pushButton.clicked.connect(self.returnTrue)
        self.pushButton_2.clicked.connect(self.returnFasle)
        self.ret = False
        self.clicked = True

    def returnTrue(self):
        names.ret = True
        names.clicked = True
        self.ret = True
        self.clicked = True
        names.eqip = self.item1
        self.m.ifs(self.type, self.item1)
        names.pause = False
        self.close()

    def returnFasle(self):
        names.ret = False
        names.clicked = True
        self.ret = False
        self.clicked = True
        names.eqip = self.item2
        self.close()

    def closeEvent(self, event):
        if event.type() == 19:
            names.pause = False
            self.close()
        if event:
            event.accept()
        else:
            self.close()
