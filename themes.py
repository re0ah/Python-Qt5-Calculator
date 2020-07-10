class Themes:
	theme_now = "standard"
	def init():
		with open("themes\\theme_now.txt", "r") as fp_r:
			"""Считывает данные из файла"""
			Themes.theme_now = fp_r.readlines()[0]

	def change_theme_now(dir_name):
		with open("themes\\theme_now.txt", "w") as fp_w:
			fp_w.writelines(dir_name)

	def set_certain_ui(ui, fname):
		load = ""
		with open(fname, "r") as fp_r:
			"""Считывает данные из файла"""
			load = fp_r.readlines()
		"""Удаление табуляций и символов переноса строки из считанных строк"""
		for i in range(len(load)):
			load[i] = load[i].replace('\t', '')
			load[i] = load[i].replace('\n', '')
		style_now = 0 #0 - считывается, к каким объектам будет применен стиль
					  #1 - считывается стиль
		stylesheet = ""
		objects = []
		i = 0
		while i < len(load):
			if load[i] == ']': #Конец описания стиля
				"""Удаление символов [ и ], так как они считываются вместе со стилем и не нужны"""
				stylesheet = stylesheet.replace('[', '')
				stylesheet = stylesheet.replace(']', '')
				"""Применение стиля к каждому объекту"""
				for k in objects:
					if k == "Form":
						ui.setStyleSheet(stylesheet)
					else:
						getattr(ui, "%s" %k).setStyleSheet(stylesheet)
				stylesheet = ""
				style_now = 0
			if style_now == 0:
				result = ""
				"""Считывание до тех пор, пока не встретится ["""
				while i < len(load):
					if load[i] == '[':
						style_now = 1
						break
					tmp = load[i].replace(' ', '')
					result += load[i]
					i += 1
				objects = result.split(',')
				for b in range(len(objects)):
					"""Удаление лишних символов и объектов"""
					objects[b] = objects[b].replace(' ', '')
					objects[b] = objects[b].replace('[', '')
					objects[b] = objects[b].replace(']', '')
					if objects[b] == "":
						del objects[b]
			else:
				stylesheet += load[i]
			i += 1

	def set(dir_name):
		Themes.theme_now = dir_name
		Themes.change_theme_now(dir_name)
		try:
			Themes.set_certain_ui(Themes.main_ui, "themes\\" + dir_name + "\\main_window.txt")
		except:
			pass
		try:
			Themes.set_certain_ui(Themes.themes_ui, "themes\\" + dir_name + "\\themes_window.txt")
		except:
			pass
		try:
			Themes.set_certain_ui(Themes.history_ui, "themes\\" + dir_name + "\\history_window.txt")
		except:
			pass
		try:
			Themes.set_certain_ui(Themes.hotkeys_ui, "themes\\" + dir_name + "\\hotkeys_window.txt")
		except:
			pass

	def set_ui_main(ui):
		Themes.main_ui = ui

	def set_ui_themes(ui):
		Themes.themes_ui = ui
	
	def set_ui_history(ui):
		Themes.history_ui = ui

	def set_ui_hotkeys(ui):
		Themes.hotkeys_ui = ui