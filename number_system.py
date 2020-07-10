import baseconvert

def convert_num_sys(number, sys_now, sys_will):
	"""Функция baseconvert.base не поддерживает отрицательные числа, поэтому нужна эта обертка."""
	ret = number
	neg = ret[0] == '-'
	if neg:
		"""Приходится извращаться с удалением символов при работе со строками. И че ж они del не поддерживают?"""
		ret = ret[1:len(ret)]
	print(number)
	ret = baseconvert.base(ret, sys_now, sys_will, string=True, recurring=False)
	if neg:
		"""Как удален был знак, так и должен быть восстановлен"""
		ret = '-' + ret
	if ret[-1] == '.':
		ret += '0'
	else:
		try:
			tmp = round(float(ret), 5)
			return str(tmp)
		except:
			pass
	return ret

allow = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
		 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
		 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
		 'U', 'V', 'W', 'X', 'Y', 'Z']
def isdigit(num):
	"""Нужна проверка на разные системы счисления, в 16-й системе буква F это тоже число"""
	return num in allow
print(allow)

def convert_num_sys_math_expr(str, sys_now, sys_will):
	"""Переводит систему счисления в математическом выражении"""
	i = 0
	"""Нужно для того, чтобы: последнее число было преобразовано (для этого нужен '\n'.
				  	 Почему? Число обрабатывается, когда находится что-то, кроме '.', ',' или числа.
				  	 Если '\n' не будет, то последнее число пропустится) и для сообщения о окончании строки,
				  	 т.е. когда будет символ '\0' то строка окончена."""
	str += '\n\0' 
	num = ""
	num_start = 0
	num_end = 0
	ret = ""
	while str[i] != '\0':
		if str[i] == ' ':
			pass
		elif isdigit(str[i]):
			"""И тут возникла проблема. Абсолютно все числа могут быть представлены как буквы, если
			   они в нужной системе счисления."""
			if num == "":
				num_start = i
				num_end = i
			else:
				num_end += 1
			num += str[i]
		elif (str[i] == '.') | (str[i] == ','):
			num_end += 1
			num += '.'
		else:
			if num == "":
				i += 1
				continue
			tmp = convert_num_sys(num, sys_now, sys_will)
			tmp_str = str[0:num_start] + tmp + str[num_end + 1:len(str)]
			"""dif - разница между измененной длиной строки и той, которая была до этого.
			   Иногда при переводе из 1-й системы счисления в другую изменяется количество
			   позиций в числе, поэтому нужно инкрементировать i, чтобы выйти за границы 
			   добавленного числа. Пример: 2 + 2, 10 > 2. Количество позиций изменилось:
			   число 2 в двоичной системе это 10. Поэтому нужно перейти за это число."""
			dif = len(tmp_str) - len(str)
			if dif != 0:
				i += dif
			str = tmp_str
			num = ""
		i += 1
	"""-2 нужно, чтобы убрать добавленные до этого '\n' и '\0'"""
	return str[0:len(str) - 2]