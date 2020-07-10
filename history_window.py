from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtCore import Qt
from history import History

class HistoryWindow(QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__(None, Qt.WindowFlags())
		self.window = uic.loadUi("ui\\history.ui")
		self.window.btn_clear.clicked.connect(self.clear)
		self.display()

	def display(self):
		"""Обновление поля вывода данных, которые берутся из файла history.txt"""
		self.window.display.setText(History.load())

	def clear(self):
		"""Очищает историю и обновляет поле вывода данных"""
		History.clear()
		self.display()