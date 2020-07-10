from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtCore import Qt
from themes import Themes
import os
import sys

class ThemesWindow(QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__(None, Qt.WindowFlags())
		self.window = uic.loadUi("ui\\themes.ui")
		self.window.pushbtn_accept.clicked.connect(self.accept)
		self.fill_list()

	def fill_list(self):
		"""Список директорий в папке themes"""
		dir_list = ([i for i in os.walk("themes")][0][1])
		self.window.list.addItems(dir_list)

	def accept(self):
		try:
			Themes.set(self.window.list.currentItem().text())
		except:
			return