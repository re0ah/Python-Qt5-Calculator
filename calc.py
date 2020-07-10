import math
def check_const(str):
	ret = 0
	if str[0: 2] == "pi":
		ret = math.pi
	if str[0: 3] == "exp":
		ret = math.e
	return ret

def check_func(str):
	"""функции lg, ln, ctg, tg, sin и cos имеют вид f(a)
	   функции root и log имеют вид f_n(a), где n - основание"""
	f = ""
	f_2 = ["lg", "ln", "tg"]		   #по кол-ву символов
	f_3 = ["ctg", "sin", "cos", "log"] #по кол-ву символов
	f_4 = ["root"]					   #по кол-ву символов
	if str[0:2] in f_2:
		f = str[0:2]
	elif str[0:3] in f_3:
		f = str[0:3]
	elif str[0:4] in f_4:
		f = str[0:4]
	return f

class calculate():
	expression = ""
	cur_expression = ""
	tokens = []

	def __init__(self, expression):
		if expression == "":
			self.result = 0
			return
		self.tokens = []
		self.result = None
		self.expression = expression + '\n'
		self.cur_expression = expression + '\n'
		self.tokenize(expression)
		if len(self.tokens) > 1:
			if self.validate_tokens() == False:
				self.result = None
				return
			self.simplification()
			self.action_in_parenthases()
			self.final_calc()
		else:
			self.result = self.tokens[0]
	   
	def check_number(self, c):
		ret = c.isdigit()
		return ret

	def check_string(self, c):
		ret = (c == 'p') | (c == 'i') | (c == 'e') | (c == 'x') | (c == 's') | (c == 'n') | (c == 'o') | (c == 'l') | (c == 'g') | (c == 't') | (c == 'r') | (c == 'c')
		return ret

	def check_function(self, token):
		func = ["sin", "cos", "tg", "ctg", "ln", "lg", "log", "root"]
		return token in func

	def tokenize(self, str):
		num = ""
		i = 0
		while i < len(str):
			if str[i] == ' ':
				i += 1
				continue
			if (str[i] == '.') | (str[i] == ','):
				num += '.'
				i += 1
				continue
			if str[i].isdigit():
				num += str[i]
			else:
				"""если в num записано какое-то число, то:"""
				if num != "":
					"""нужно чтобы в выражениях по-типу cos(0)2 после ) ставился знак умножения"""
					if len(self.tokens) > 0:
						if (self.tokens[-1] == ')') | (self.tokens[-1] == '!') | (self.tokens[-1] == math.pi) | (self.tokens[-1] == math.e):
							self.tokens.append('*')
					self.tokens.append(float(num))
					num = ""
				ch_f = check_func(str[i:i+4])
				if ch_f != "":
					if len(self.tokens) > 0:
						if (type(self.tokens[-1]) == float) | (self.tokens[-1] == ')'):
							self.tokens.append('*')
					"""функции log и root особые, т.к. имеют основание, указанное в виде f_n(a), где n - основание"""
					tmp = ""
					self.tokens.append(ch_f)
					if (ch_f == "log") | (ch_f == "root"):
						i += len(ch_f) + 1
						"""обработка основания"""
						while str[i] != '(':
								tmp += str[i]
								i += 1
								print(tmp)
						self.tokens.append(float(tmp))
						i += 1
						self.tokens.append('(')
					else:
						i += len(ch_f)
					continue
				"""Проверка на число pi и e"""
				if (str[i:i+2] == "pi") | (str[i:i+3] == "exp"):
					if len(self.tokens) > 0:
						if (type(self.tokens[-1]) == float) | (self.tokens[-1] == ')') | (self.tokens[-1] == '!'):
							self.tokens.append('*')
					const = check_const(str[i:i+3])
					self.tokens.append(const)
					"""pi занимает 2 символа, exp - 3. Поэтому при проверке на константу e добавляется еще 1"""
					i += 2
					if const == math.e:
						i += 1
					continue
				elif str[i] == '(':
					if len(self.tokens) == 0:
						pass
					elif len(self.tokens) > 0:
						"""Проверка на выражение типа n( - нужно подставить знак умножения, то же самое для
						   выражений вида (a)(b)(c)"""
						if (type(self.tokens[-1]) == float) | (self.tokens[-1] == ')'):
							self.tokens.append('*')
					self.tokens.append(str[i])
				elif str[i] == ')':
					self.tokens.append(str[i])
				else:
					"""+, -, *, /"""
					self.tokens.append(str[i])
			i += 1
		"""Последнее значение не успевает быть записано в случае, если это число"""
		if num != "":
			if len(self.tokens) > 0:
				if (self.tokens[-1] == ')') | (self.tokens[-1] == '!') | (self.tokens[-1] == math.pi) | (self.tokens[-1] == math.e):
					self.tokens.append('*')
			self.tokens.append(float(num))

	def validate_tokens(self):
		allow_token = ["-", "+", "*", "/", ".", "(", ")", "%", "^", "!"]
		for i in self.tokens:
			if (i in allow_token) | (type(i) == type(0.0)) | (self.check_function(i)):
				continue
			else:
				return False
		return True

	def simplification(self):
		#Заменяет простые конструкции вроде '+'' '-'' '5' на '+' '-5', (5) на 5 и прочее
		i = 0
		while i < len(self.tokens):
			c = self.tokens[i]
			if len(self.tokens) > 1:
				if (i == 0) & (c == '-') & (type(self.tokens[1]) == type(0.0)):
					self.tokens[1] = -self.tokens[1]
					del self.tokens[0]
					continue
			if (i > 0) & (i != (len(self.tokens) - 1)):
				if (self.tokens[i - 1] == '(') & (type(self.tokens[i]) == type(0.0)) & (self.tokens[i + 1] == ')'):
					del self.tokens[i - 1]
					del self.tokens[i]
					i = 0
					continue
				if i > 1:
					if (self.tokens[i - 2] == '+') & (self.tokens[i - 1] == '-') & (type(self.tokens[i]) == type(0.0)):
						self.tokens[i] = -self.tokens[i]
						del self.tokens[i - 1]
						i = 0
						continue
				if (i > 2) & (i < (len(self.tokens) - 1)):
					if (self.tokens[i - 2] == '(') & ((self.tokens[i - 1] == '-') | (self.tokens[i - 1] == '+')) & (type(self.tokens[i]) == type(0.0)) & (self.tokens[i + 1] == ')'):
						if self.tokens[i - 1] == '-':
							self.tokens[i] = -self.tokens[i]
						del self.tokens[i - 2]
						del self.tokens[i - 2]
						del self.tokens[i - 1]
						i = 0
						continue
			i += 1

	def action_in_parenthases(self):
		#Основная цель функции - избавиться от всех скобок путем их упрощения. Вместо (2 + 5) будет 7
		i = 0
		nesting = 0
		while i < len(self.tokens):
			c = self.tokens[i]
			if c == '(':
				nesting = i
			elif c == ')':
				length = i - nesting
				tmp = self.calc_token(self.tokens[nesting + 1: i])
				self.tokens[nesting] = tmp
				for i in range(length):
					del self.tokens[nesting + 1]
				i = 0
				continue
			i += 1

	def calc_token(self, tokens):
		i = 0
		while(len(tokens) > 1):
			print(tokens)
			op = 0
			for j in range(len(tokens)):
				if self.check_function(tokens[j]):
					op = j
					break
				elif tokens[j] == '^':
					op = j
				elif tokens[j] == '!':
					op = j
				elif (tokens[j] == '*') | (tokens[j] == '/'):
					if(tokens[op] == '!'):
						continue
					if (tokens[op] != '*') | (tokens[op] != '/'):
						op = j
				elif (tokens[j] == '+') | (tokens[j] == '-'):
					if op == 0:
						op = j
			if self.check_function(tokens[op]):
				if tokens[op] == "sin":
					tokens[op] = math.sin(tokens[op + 1])
				elif tokens[op] == "cos":
					tokens[op] = math.cos(tokens[op + 1])
				elif tokens[op] == "tg":
					tokens[op] = math.tan(tokens[op + 1])
				elif tokens[op] == "ctg":
					tokens[op] = math.cos(tokens[op + 1]) / math.sin(tokens[op + 1])
				elif tokens[op] == "ln":
					tokens[op] = math.log(tokens[op + 1], math.e)
				elif tokens[op] == "log":
					tokens[op] = math.log(tokens[op + 2], tokens[op + 1])
					del tokens[op + 1]
				elif tokens[op] == "lg":
					tokens[op] = math.log2(tokens[op + 1])
				elif tokens[op] == "root":
					print(tokens[op])
					print(tokens[op + 1])
					print(tokens[op + 2])
					tokens[op] = tokens[op + 2]**(1./tokens[op + 1])
					del tokens[op + 1]
				del tokens[op + 1]
				i += 1
				continue
			elif tokens[op] == '-':
				tokens[op - 1] -= tokens[op + 1]
			elif tokens[op] == '+':
				print(tokens[op - 1])
				print(tokens[op])
				print(tokens[op + 1])
				tokens[op - 1] += tokens[op + 1]
			elif tokens[op] == '%':
				tokens[op - 1] %= tokens[op + 1]
			elif tokens[op] == '*':
				tokens[op - 1] *= tokens[op + 1]
			elif tokens[op] == '/':
				tokens[op - 1] /= tokens[op + 1]
			elif tokens[op] == '^':
				tokens[op - 1] = pow(tokens[op - 1], tokens[op + 1])
			elif tokens[op] == '!':
				tokens[op - 1] = float(math.factorial(tokens[op - 1]))
				del tokens[op]
				i += 1
				continue
			del tokens[op]
			del tokens[op]
			i += 1
		return tokens[0]

	def final_calc(self):
		self.tokens = self.calc_token(self.tokens)
		self.result = self.tokens

print(calculate("log_2(4)").result)