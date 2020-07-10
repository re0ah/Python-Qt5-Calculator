from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt
from hotkeys import Hotkey

class HotkeyWindow(QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__(None, Qt.WindowFlags())
		self.window = uic.loadUi("ui\\hotkeys.ui")
		self.set_text_lbls()
		self.window.btn_default_settings.clicked.connect(self.set_default)
		self.window.btn_accept.clicked.connect(self.accept)

	def set_default(self):
		"""Функция нажатия на кнопку Сбросить настройки"""
		for i in range(len(self.obj_l)):
			Hotkey.now_hotkeys[self.dict_v[i]] = Hotkey.std_hotkeys[self.dict_v[i]]
		Hotkey.set_hotkeys()
		self.window.hide()

	def accept(self):
		"""Функция нажатия на кнопку Принять"""
		for i in range(len(self.obj_l)):
			Hotkey.now_hotkeys[self.dict_v[i]] = self.obj_l[i].text()
		Hotkey.set_hotkeys()
		self.window.hide()

	def set_text_lbls(self):
		"""Устанавливает текст у labels соответствующий данным в файле hotkeys.json"""
		self.dict_v = ["0", "1", "2", "3", "4",
				  "5", "6", "7", "8", "9",
				  "+", "-", "*", "/", "%",
				  ".", "exp", "pi", "clear",
				  "=", "calc", "(", ")",
				  "backspace", "factorial",
				  "power", "root", "lg",
				  "log", "ln", "ctg", "tg",
				  "sin", "cos"]
		self.obj_l = [self.window.hotkey_0, self.window.hotkey_1,
				 self.window.hotkey_2, self.window.hotkey_3,
				 self.window.hotkey_4, self.window.hotkey_5,
				 self.window.hotkey_6, self.window.hotkey_7,
				 self.window.hotkey_8, self.window.hotkey_9,
				 self.window.hotkey_add, self.window.hotkey_sub,
				 self.window.hotkey_mul, self.window.hotkey_div,
				 self.window.hotkey_percent, self.window.hotkey_dot,
				 self.window.hotkey_exp, self.window.hotkey_pi,
				 self.window.hotkey_clear, self.window.hotkey_equal,
				 self.window.hotkey_calc, self.window.hotkey_left_br,
				 self.window.hotkey_right_br, self.window.hotkey_backspace,
				 self.window.hotkey_fact, self.window.hotkey_pow,
				 self.window.hotkey_root, self.window.hotkey_lg,
				 self.window.hotkey_log, self.window.hotkey_ln,
				 self.window.hotkey_ctg, self.window.hotkey_tg,
				 self.window.hotkey_sin, self.window.hotkey_cos]
		for i in range(len(self.obj_l)):
			self.obj_l[i].setText(Hotkey.now_hotkeys[self.dict_v[i]])