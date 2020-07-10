import sys
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt
from calc import *
from hotkeys import Hotkey
import hotkeys_window
from history import History
import history_window
import number_system
from themes import Themes
import themes_window

class MainWindow(QtGui.QMainWindow):
	def __init__(self):
		super().__init__(None, Qt.WindowFlags())
		self.window = uic.loadUi("ui\\mainwindow.ui")
		self.window.show()
		self.assignWidgets()
		Hotkey.init_hotkeys(self.window)
		self.num_sys_now = self.window.spinbox_num_sys.text()
		Themes.set_ui_main(self.window)
		Themes.set_certain_ui(Themes.main_ui, "themes\\" + Themes.theme_now + "\\main_window.txt")
		self.entry_line_input_init()

	def keyPressEvent(self, event):
		print("EVENT< BLYAD", event)

	def assignWidgets(self):
		"""Устанавливает функции у кнопок"""
		pushbtn_numbers = [getattr(self.window, "pushbtn_%s" %i) for i in range(10)]
		for btn in pushbtn_numbers:
			btn.clicked.connect(self.push_number)
		pushbtn_symbols = [self.window.pushbtn_percent,
						   self.window.pushbtn_add,
						   self.window.pushbtn_sub,
						   self.window.pushbtn_mul,
						   self.window.pushbtn_div]
		for btn in pushbtn_symbols:
			btn.clicked.connect(self.push_symbol)

		self.window.pushbtn_pi.clicked.connect(self.push_const)
		self.window.pushbtn_exp.clicked.connect(self.push_const)

		self.window.pushbtn_dot.clicked.connect(self.push_dot)

		self.window.pushbtn_clear.clicked.connect(self.push_clear)

		self.window.pushbtn_equal.clicked.connect(self.calc)
		"""Установка функции на действие нажатия на enter при выделенном поле ввода"""
		self.window.entry_line.returnPressed.connect(self.calc)

		self.window.pushbtn_left_br.clicked.connect(self.push_left_br)
		self.window.pushbtn_right_br.clicked.connect(self.push_right_br)

		self.window.pushbtn_backspace.clicked.connect(self.del_last_symb)

		self.window.pushbtn_fact.clicked.connect(self.fact)
		self.window.pushbtn_pow.clicked.connect(self.power)
		self.window.pushbtn_sqr.clicked.connect(self.sqr)
		self.window.pushbtn_root.clicked.connect(self.root)
		self.window.pushbtn_lg.clicked.connect(self.lg)
		self.window.pushbtn_log.clicked.connect(self.log)
		self.window.pushbtn_ln.clicked.connect(self.ln)
		self.window.pushbtn_ctg.clicked.connect(self.ctg)
		self.window.pushbtn_tg.clicked.connect(self.tg)
		self.window.pushbtn_sin.clicked.connect(self.sin)
		self.window.pushbtn_cos.clicked.connect(self.cos)

		self.window.pushbtn_history.clicked.connect(self.open_history)
		self.window.pushbtn_hotkeys.clicked.connect(self.open_hotkeys)
		self.window.pushbtn_themes.clicked.connect(self.open_themes)

		self.window.spinbox_num_sys.valueChanged.connect(self.change_num_sys)

	def open_history(self):
		"""Открывает окно с историей действий"""
		self.w_history = history_window.HistoryWindow()
		self.w_history.window.show()
		Themes.set_ui_history(self.w_history.window)
		Themes.set_certain_ui(Themes.history_ui, "themes\\" + Themes.theme_now + "\\history_window.txt")

	def open_hotkeys(self):
		"""Открывает окно, где можно установить горячие клавиши"""
		self.w_hotkey = hotkeys_window.HotkeyWindow()
		self.w_hotkey.window.show()
		Themes.set_ui_hotkeys(self.w_hotkey.window)
		Themes.set_certain_ui(Themes.hotkeys_ui, "themes\\" + Themes.theme_now + "\\hotkeys_window.txt")

	def open_themes(self):
		"""Открывает окно с историей действий"""
		self.w_themes = themes_window.ThemesWindow()
		self.w_themes.window.show()
		Themes.set_ui_themes(self.w_themes.window)
		try:
			Themes.set_certain_ui(Themes.themes_ui,  "themes\\" + Themes.theme_now + "\\themes_window.txt")
		except:
			pass

	def entry_line_cat(self, text):
		"""Добавляет к текущему тексту в поле ввода переданный текст"""
		self.window.entry_line.setText(self.window.entry_line.text() + text)

	def del_last_symb(self):
		"""Удаляет последний символ из поля ввода"""
		self.window.entry_line.setText(self.window.entry_line.text()[:-1])

	def entry_line_last_symbol(self):
		"""Возвращает последний символ из поля ввода. Если строка пустая, возвращает '\0'"""
		text = self.window.entry_line.text()
		text_len = len(text)
		if text_len == 0:
			return '\0'
		return text[-1]

	def push_number(self):
		"""Функция нажатия на кнопки с цифрами"""
		text = self.window.entry_line.text()
		text_len = len(text)
		if text_len == 0:
			"""Если поле ввода пусто, то просто цифра просто добавляется в поле ввода"""
			self.entry_line_cat(self.sender().text())
			return
		"""Проверка на то, что последним введено pi или exp. После них нельзя ставить число, поэтому если они введены
		   то происходит выход из функции"""
		if text_len >= 2:
			if (text[-2] == 'p') & (text[-1] == 'i'):
				return
		if text_len >= 3:
			if (text[-3] == 'e') & (text[-2] == 'x') & (text[-1] == 'p'):
				return
		"""Добавление цифры в поле ввода"""
		self.entry_line_cat(self.sender().text())

	def push_symbol(self):
		"""Функция нажатия на математические символы (+, -, *, /, %)"""
		last_symbol = self.entry_line_last_symbol()
		if last_symbol == '\0':
			"""Если поле ввода пусто, то проверяется минус ли это: только он может быть в самом начале выражения.
			   Если это минус, то он добавляется к строке"""
			if self.sender().text() == '-':
				self.entry_line_cat(self.sender().text())
			return
		unallowed_characters = ["*", "/", "-", "+", "(", "^", ".", "%"]
		"""Проверка последнего символа в поле ввода: является ли он допустимым"""
		if (last_symbol in unallowed_characters) == 0:
			self.entry_line_cat(self.sender().text())
		"""Проверка последнего символа в поле ввода: эта проверка нужна для выражений типа 5(-2), чтоб после
		   ( можно было ставить -"""
		if ((last_symbol == '(') & (self.sender().text() == '-')):
			self.entry_line_cat(self.sender().text())

	def push_dot(self):
		"""Функция нажатия на кнопку ."""
		text = self.window.entry_line.text()
		text_len = len(text)
		"""Вероятно, стоит удалить это и сделать возможность обработки чисел с целой частью в 0 в виде, например,
		   .5 + .5 = 1.0"""
		if text_len == 0:
			return
		if text[-1] == ')':
			return
		"""Проверка на то, что последним введено pi или exp. После них нельзя ставить точку, поэтому если они введены
		   то происходит выход из функции"""
		if text_len >= 2:
			if (text[-2] == 'p') & (text[-1] == 'i'):
				return
		if text_len >= 3:
			if (text[-3] == 'e') & (text[-2] == 'x') & (text[-1] == 'p'):
				return
		"""Проверка последнего символа в поле ввода: является ли он допустимым"""
		unallowed_characters = ["*", "/", "-", "+", "(", "^", ".", "%"]
		if (text[-1] in unallowed_characters) == 0:
			self.entry_line_cat(self.sender().text())

	def push_const(self):
		"""Функция нажатия на кнопки pi и exp"""
		last_symbol = self.entry_line_last_symbol()
		"""В случае, если строка пуста, то константа просто добавляется в поле ввода"""
		if last_symbol == '\0':
			self.entry_line_cat(self.sender().text())
			return
		"""Проверка на допустимый последний символ"""
		self.entry_line_cat(self.sender().text())

	def push_clear(self):
		"""Очищает поле ввода"""
		self.window.entry_line.setText("")
		self.window.result_field.setText("")

	def push_left_br(self):
		"""Функция нажатия на ("""
		last_symbol = self.entry_line_last_symbol()
		"""В случае, если строка пуста, то ( просто добавляется в поле ввода"""
		if last_symbol == '\0':
			self.entry_line_cat(self.sender().text())
			return
		"""Проверка на допустимый последний символ"""
		allowed_characters = ["*", "/", "+", "-", "(", ")", "^", "%",
							  "0", "1", "2", "3", "4", "5", "6", "7",
							  "8", "9", "!"]
		if last_symbol in allowed_characters:
			self.entry_line_cat(self.sender().text())

	def push_right_br(self):
		"""Функция нажатия на ("""
		last_symbol = self.entry_line_last_symbol()
		"""В случае, если строка пуста, то ) просто добавляется в поле ввода"""
		if last_symbol == '\0':
			return
		"""Проверка на допустимый последний символ"""
		unallowed_characters = ["*", "/", "+", "-", "(", ".", "^", "%"]
		if (last_symbol in unallowed_characters) == 0:
			self.entry_line_cat(self.sender().text())

	def change_num_sys(self):
		self.num_sys_will = self.sender().text()
		try:
			text = number_system.convert_num_sys_math_expr(self.window.entry_line.text(),
													   int(self.num_sys_now),
													   int(self.num_sys_will))
			self.window.entry_line.setText(text)
		except:
			pass
		try:
			text = number_system.convert_num_sys_math_expr(self.window.result_field.text(),
													   int(self.num_sys_now),
													   int(self.num_sys_will))
			if str(text)[-1] == '0':
				text = str(text)[:len(str(text)) - 2]
			self.window.result_field.setText(text)
		except:
			pass
		self.num_sys_now = self.num_sys_will

	def calc(self):
		"""Функция подсчета выражения, вывода и сохранения результата"""
		try:
			"""Считает текущее введенное математическое выражение"""
			expr = self.window.entry_line.text()
			if self.num_sys_now != 10:
				expr = number_system.convert_num_sys_math_expr(self.window.entry_line.text(),
													   int(self.num_sys_now),
													   int(10))
			tmp = calculate(expr)
			"""Вывод результата в поле результата"""
			result = tmp.result
			if self.num_sys_now != 10:
				result = number_system.convert_num_sys_math_expr(str(tmp.result),
													   int(10),
													   int(self.num_sys_now))
			if str(result)[-1] == '0':
				result = str(result)[:len(str(result)) - 2]
			self.window.result_field.setText(str(result))
			"""Сохранение результата"""
			History.save(self.window.entry_line.text() + ' = ' + str(tmp.result) + '\n')
			try:
				"""В случае, если окно истории открыто - обновить его"""
				self.w_history.display()
			except:
				pass
		except:
			"""В случае неудачи вывести в поле результата Fail"""
			self.window.result_field.setText("Fail")

	def fact(self):
		last_symbol = self.entry_line_last_symbol()
		"""Проверка на допустимость последнего символа в поле ввода"""
		unallowed_characters = ["*", "/", "+", "-", "(", ".", "^", "%", "!"]
		if (last_symbol in unallowed_characters) == 0:
			self.entry_line_cat('!')

	def power(self):
		last_symbol = self.entry_line_last_symbol()
		"""Проверка на допустимость последнего символа в поле ввода"""
		unallowed_characters = ["*", "/", "+", "-", "(", ".", "^", "%", "!"]
		if (last_symbol in unallowed_characters) == 0:
			self.entry_line_cat('^')

	def sqr(self):
		last_symbol = self.entry_line_last_symbol()
		"""Проверка на допустимость последнего символа в поле ввода"""
		unallowed_characters = ["*", "/", "+", "-", "(", ".", "^", "%", "!"]
		if (last_symbol in unallowed_characters) == 0:
			self.entry_line_cat('^2')

	def root(self):
		self.entry_line_cat('root_')

	def lg(self):
		self.entry_line_cat('lg(')

	def log(self):
		self.entry_line_cat('log_')

	def ln(self):
		self.entry_line_cat('ln(')

	def ctg(self):
		self.entry_line_cat('ctg(')

	def tg(self):
		self.entry_line_cat('tg(')

	def sin(self):
		self.entry_line_cat('sin(')

	def cos(self):
		self.entry_line_cat('cos(')

	def entry_line_keyPressEvent(self, event):
		"""Сохраненная функция от entry_line, инициализируется в функции entry_line_input_init"""
		self.entry_line_key_press(event)
		"""Считывание сканкода нажатой клавиши. Может не работать на других компьютерах, так как нативен"""
		scancode = event.nativeScanCode()
		if scancode == 284: #Numpad enter
			self.window.pushbtn_equal.animateClick() #Вызов анимации нажатия клавиши
			self.calc()
		elif scancode == 339: #Delete
			self.window.pushbtn_clear.animateClick() #Вызов анимации нажатия клавиши
			self.push_clear()

	def spinbox_num_sys_keyPressEvent(self, event):
		"""Сохраненная функция от spinbox_num_sys, инициализируется в функции entry_line_input_init"""

		"""Считывание сканкода нажатой клавиши. Может не работать на других компьютерах, так как нативен"""
		scancode = event.nativeScanCode()
		if scancode == 339: #Delete
			self.window.pushbtn_clear.animateClick() #Вызов анимации нажатия клавиши
			self.push_clear()
			return
		self.spinbox_num_sys_key_press(event)
		
	def entry_line_input_init(self):
		"""Сохранение функций нажатия на клавишу, чтобы после ее можно было вызвать в функции, которая ее заменит"""
		self.entry_line_key_press = self.window.entry_line.keyPressEvent
		self.spinbox_num_sys_key_press = self.window.spinbox_num_sys.keyPressEvent
		"""Подмена функций"""
		self.window.entry_line.keyPressEvent = self.entry_line_keyPressEvent
		self.window.spinbox_num_sys.keyPressEvent = self.spinbox_num_sys_keyPressEvent


if __name__ == "__main__":
	QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
	app = QtWidgets.QApplication([])
	Themes.init()
	mainWin = MainWindow()
	sys.exit(app.exec())