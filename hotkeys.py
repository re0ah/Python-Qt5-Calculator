import json
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtGui import QKeySequence

class Hotkey():
	hkeys_stdfname = "info\\hotkeys.json"

	std_hotkeys = {"0": "0",
				   "1": "1",
				   "2": "2",
				   "3": "3",
				   "4": "4",
				   "5": "5",
				   "6": "6",
				   "7": "7",
				   "8": "8",
				   "9": "9",
				   "+": "+",
				   "-": "-",
				   "*": "*",
				   "/": "/",
				   "%": "%",
				   ".": ".",
				   "exp": "e",
				   "pi": "p",
				   "clear": "c",
				   "=": "=",
				   "(": "(",
				   ")": ")",
				   "backspace": "Backspace",
				   "factorial": "!",
				   "power": "^",
				   "root": "r",
				   "lg": "g",
				   "log": "l",
				   "ln": "n",
				   "ctg": "y",
				   "tg": "t",
				   "sin": "s",
				   "cos": "o"}
	now_hotkeys = {}

	def init_hotkeys(ui):
		"""Инициализирует горячие клавиши в окне mainwindow"""
		"""ui - это окно mainwindow"""
		Hotkey.ui = ui
		"""Загружает значения горячих клавиш из файла hotkeys.json"""
		with open(Hotkey.hkeys_stdfname) as fp_r:
			Hotkey.now_hotkeys = json.load(fp_r)
		Hotkey.set_hotkeys()

	def set_hotkeys():
		"""Устанавливает горячие клавиши окна mainwindow"""
		ui_list = [Hotkey.ui.pushbtn_0, Hotkey.ui.pushbtn_1, Hotkey.ui.pushbtn_2, Hotkey.ui.pushbtn_3,
				   Hotkey.ui.pushbtn_4, Hotkey.ui.pushbtn_5, Hotkey.ui.pushbtn_6, Hotkey.ui.pushbtn_7,
				   Hotkey.ui.pushbtn_8, Hotkey.ui.pushbtn_9,

				   Hotkey.ui.pushbtn_percent, Hotkey.ui.pushbtn_add, Hotkey.ui.pushbtn_sub,
				   Hotkey.ui.pushbtn_mul, Hotkey.ui.pushbtn_div,

				   Hotkey.ui.pushbtn_left_br, Hotkey.ui.pushbtn_right_br, Hotkey.ui.pushbtn_dot]
		for btn in ui_list:
			btn.setShortcut(Hotkey.now_hotkeys[btn.text()])

		for hotk in [Hotkey.now_hotkeys["="], "Return"]:
			shcut = QtWidgets.QShortcut(hotk, Hotkey.ui.pushbtn_equal)
			shcut.activated.connect(Hotkey.ui.pushbtn_equal.animateClick)

		shcut = QtWidgets.QShortcut(QKeySequence(284), Hotkey.ui.pushbtn_equal)
		shcut.activated.connect(Hotkey.ui.pushbtn_equal.animateClick)

		for hotk in [Hotkey.now_hotkeys["clear"], "Delete"]:
			shcut = QtWidgets.QShortcut(hotk, Hotkey.ui.pushbtn_clear)
			shcut.activated.connect(Hotkey.ui.pushbtn_clear.animateClick)

		Hotkey.ui.pushbtn_pi.setShortcut(Hotkey.now_hotkeys["pi"])
		Hotkey.ui.pushbtn_exp.setShortcut(Hotkey.now_hotkeys["exp"])
		Hotkey.ui.pushbtn_backspace.setShortcut(Hotkey.now_hotkeys["backspace"])
		Hotkey.ui.pushbtn_fact.setShortcut(Hotkey.now_hotkeys["factorial"])
		Hotkey.ui.pushbtn_pow.setShortcut(Hotkey.now_hotkeys["power"])
		Hotkey.ui.pushbtn_root.setShortcut(Hotkey.now_hotkeys["root"])
		Hotkey.ui.pushbtn_lg.setShortcut(Hotkey.now_hotkeys["lg"])
		Hotkey.ui.pushbtn_log.setShortcut(Hotkey.now_hotkeys["log"])
		Hotkey.ui.pushbtn_ln.setShortcut(Hotkey.now_hotkeys["ln"])
		Hotkey.ui.pushbtn_ctg.setShortcut(Hotkey.now_hotkeys["ctg"])
		Hotkey.ui.pushbtn_tg.setShortcut(Hotkey.now_hotkeys["tg"])
		Hotkey.ui.pushbtn_sin.setShortcut(Hotkey.now_hotkeys["sin"])
		Hotkey.ui.pushbtn_cos.setShortcut(Hotkey.now_hotkeys["cos"])

		Hotkey.save_hotkeys()

	def save_hotkeys():
		"""Сохраняет текущие настройки"""
		with open(Hotkey.hkeys_stdfname, "w") as fp_w:
			json.dump(Hotkey.now_hotkeys, fp_w)

	def load_hotkeys():
		"""Загружает настройки"""
		load = {}
		with open(Hotkey.hkeys_stdfname, "r") as fp_r:
			load = json.load(fp_r)