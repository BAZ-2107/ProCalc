from exceptions import DecodeError
from objects import *

class Decode:
	f = open("functions.txt", "r")
	functions = f.read().split()
	f.close()

	def decode(self, st):
		array = list(st)
		if ("(" in array) or (")" in array):
			self.check_brackets(array)
		elem = self.decode_expression(array)
		return elem

	def decode_and_check(self, array):
		if "|" in array:
			array = self.decode_module(array)
		array = self.convert_numbers(array)
		array = self.convert_functions(array)
		array = self.convert_constants(array)
		array = self.convert_perems(array)
		array = self.convert_st_f_r_i(array)
		array = self.convert_m_d_a_s(array)
		return array[0]

	def decode_module(self, array):
		issign = lambda x: x in "+-*/^√["
		ismodulebracket = lambda x: x == "|"
		k = 0
		for i, ch in enumerate(array):
			if ismodulebracket(ch):
				if (k == 0) or (i != 0 and issign(array[i - 1])):
					array[i], k = "[", k + 1
				else:
					array[i], k = "]", k - 1
		if k != 0:
					raise DecodeError("Не удалось расшифровать модуль в выражении")
		while "[" in array:
			stop = array.index("]")
			start = stop
			while array[start] != "[":
				start -= 1
			in_module = array[start + 1: stop]
			del array[start:stop+1]
			in_module = self.decode_and_check(in_module)
			array.insert(start, Module(in_module))
		return array

	def decode_expression(self, array):
		while "(" in array:
			stop = array.index(")")
			start = stop
			while array[start] != "(":
				start -= 1
			in_brackets = array[start + 1: stop]
			del array[start:stop+1]
			if in_brackets:
				in_brackets = self.decode_and_check(in_brackets)
				array.insert(start, in_brackets)
		result = self.decode_and_check(array)
		return result

# проверка скобок выражений
	def check_brackets(self, array):
		isleftbracket = lambda x: x == "("
		isrightbracket = lambda x: x == ")"
		k = 0
		for ch in array:
			if isleftbracket(ch):
				k += 1
			if isrightbracket(ch):
				k -= 1
			if k == -1:
				raise DecodeError("Некорректное число скобок")
		if k != 0:
			raise DecodeError("Некорректное число скобок")

	# метод конвертировки цифр в числа
	def convert_numbers(self, array):
		isnumber = lambda ch: ch in list("0123456789,")
		iscorrectnumber = lambda number: (number.count(",") < 2) and ("" not in number.split(","))
		start, step, end = 0, 0, len(array)
		while start <= end:
			if start != end and isnumber(array[start]):
				step += 1
			elif step:
				stop = start
				start -= step
				number = "".join(array[start:stop])
				if not iscorrectnumber(number):
					raise DecodeError(f"Неправильная запись числа: <{str(num)}>")
				del array[start:stop]
				if "," in number:
					array.insert(start, Rational(*from_decimal_to_rational(number)))
				else:
					array.insert(start, Natural(int(number)))
				step, end = 0, len(array)
			start += 1
		return array

	# функция конвертировки букв в названия функций
	def convert_functions(self, array):
		start, end  = 0, len(array)
		while start != end:
			if (type(array[start]) == str) and (array[start].isalpha()):
				for func in self.functions:
					stop = start + len(func)
					if (stop <= end) and (array[start:stop] == list(func)):
						del array[start:stop]
						array.insert(start, func)
						end = len(array)
						break
			start += 1
		return array

	def convert_constants(self, array):
		return list(map(lambda elem: elem if elem not in ["e", "π"] else Const(elem), array))

	def convert_perems(self, array):
		isunknown = lambda x: (type(x) == str) and (len(x) == 1) and x.isalpha()
		return list(map(lambda elem: Perem(elem) if isunknown(elem) else elem, array))

	def convert_st_f_r_i(self, array):
		signs, funcs = lambda x: type(x) == str, self.functions
		message = "Некорректная запись у  объекта  <{}>"
		first, last = array[0], array[-1]
		if (last in funcs) or (last in list("√^")):
			raise DecodeError(f"Объект <{last}> не должен стоять в конце выражения")
		if first == "^":
			raiseDecodeError(f"Объект <{first}> не должен стоять в начале выражения")
		for i in range(len(array) - 2, -1, -1):
			elem, elem_1 = array[i], array[i + 1]
			if elem in funcs:
				if elem != "log":
					if elem_1 == "^":
						st = array[i + 2]
						if i + 3 == len(array):
							raise DecodeError(message.format(elem))
						arg = array[i + 3]
						if signs(arg) or signs(st):
							raise DecodeError(message.format(elem))
						array[i] = Pow(diction[elem](arg), st)
						del array[i+1:i+4]
					else:
						arg = array[i+1]
						if signs(arg):
							raise DecodeError(message.format(elem))
						array[i] = diction[elem](arg)
						del array[i+1]
				elif elem == "log":
					if elem_1 == "^":
						st = array[i+2]
						if i + 4 >= len(array):
							raise DecodeError(message.format(elem))
						arg1, arg2 = array[i+3:i+5]
						if signs(st) or signs(arg1) or signs(arg2):
							raise DecodeError(message.format(elem))
						array[i] = Pow(diction[elem](arg1, arg2), st)
						del array[i+1:i+5]
					else:
						if i + 2 == len(array):
							raise DecodeError(message.format(elem))
						arg1, arg2 = array[i+1:i+3]
						if signs(arg1) or signs(arg2):
							raise DecodeError(message.format(elem))
						array[i] = diction[elem](arg1, arg2)
						del array[i+1:i+3]
			elif elem == "√":
				if signs(elem_1):
						raise DecodeError(message.format(elem))
				array[i] = Radical(elem_1)
				del array[i+1]
			elif elem_1 == "^":
				st = array[i+2]
				if signs(elem) or signs(st):
					raise DecodeError(f"Объект <{elem_1}> не должен соединять <{elem}> и <{st}>")
				array[i] = Pow(elem, st)
				del array[i+1:i+3]
			elif (i == 0) and (elem == "-"):
				if signs(elem_1):
					raise DecodeError(message.format(elem))
				array[i] = Invers(elem_1)
				del array[i+1]
				
		return array

	def convert_m_d_a_s(self, array):
		signs = lambda x: type(x) == str
		message = "Некорректная запись у  объекта  <{}>"
		first, last = array[0], array[-1]
		if last in list("+-*/"):
			raise DecodeError(f"Объект <{last}> не должен стоять в конце выражения")
		if first in list("+-*/"):
			raise DecodeError(f"Объект <{first}> не должен стоять в начале выражения")
		for i in range(1 - len(array), 0):
			elem_1, elem = array[i-1], array[i]
			if not (signs(elem) or signs(elem_1)):
				array[i] = Mul(elem_1, elem)
				del array[i-1]
			elif elem_1 == "*" or elem_1 == "/":
				elem_2 = array[i-2]
				if signs(elem) or signs(elem_2):
					raise DecodeError(message.format(elem_1))
				array[i] = Mul(elem_2, elem) if elem_1 == "*" else Div(elem_2, elem)
				del array[i-2:i]

		for i in range(1 - len(array), 0):
			elem_1, elem = array[i-1], array[i]
			if elem_1 == "+" or elem_1 == "-":
				elem_2 = array[i-2]
				if signs(elem) or signs(elem_2):
					raise DecodeError(message.format(elem_1))
				array[i] = Add(elem_2, elem) if elem_1 == "+" else Sub(elem_2, elem)
				del array[i-2:i]

		return array
			
#a = Decode().decode("log^2ab")
#print(str(a), type(a))
"""
objects:
	number 0123456789,
	const pi e
	unknown xyz...
	function sin cos ...
	module ||
	expression ()

signs:
	+
	-
	*
	/
	^

	√
"""