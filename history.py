class History():
	fname = "info\\history.txt"
	def save(str):
		"""Добавляет к файлу history.txt в самое начало переданный аргумент. Если файла нет, то он будет создан"""
		try:
			"""Открытие файла на чтение+запись"""
			with open(History.fname, "r+") as fp_w:
				"""Считывание файла"""
				lines = fp_w.readlines()
				"""Переход указателя на файл в самое начало"""
				fp_w.seek(0)
				"""Запись в файл данных, которые было изначально с данными, полученными в функцию"""
				fp_w.writelines(list(str) + lines)
		except FileNotFoundError:
			"""В случае отсутствия файла history.txt - создать его и вызвать функцию еще раз"""
			with open(History.fname, "w") as create:
				History.save(str)

	def load():
		"""Загружает данные из файла history.txt"""
		load = ""
		with open(History.fname, "r") as fp_r:
			"""Считывает данные из файла"""
			load = fp_r.readlines()
		ret = ""
		"""Так как данные из файла считываются в список строк, то нужно их преобразовать в строку"""
		for i in load:
			ret += i
		return ret

	def clear():
		"""Очищает файл history.txt"""
		with open(History.fname, "w") as f:
			pass