import re

class Html_Parser:
	# конструктор
	def __init__(self, html):
		self.html_code = html
		#удаляем переносы строк
		self.html_code = re.sub("\n", " ", self.html_code)
		#удаляем тег head
		self.html_code = re.sub("<head(.*?)head>", "", self.html_code)
		#удаляем тег script
		self.html_code = re.sub("<script(.*?)</script>", "", self.html_code)
		#удаляем тег noscript
		self.html_code = re.sub("<noscript(.*?)</noscript>", "", self.html_code)
		#находим позиции открывающих и закрывающих тегов
		indexes_start_tag = self.find_all_indexes(self.html_code, "<div")
		indexes_end_tag = self.find_all_indexes(self.html_code, "</div>")
		#узнаем количество индексов для обоих листов
		count_start_tag = len(indexes_start_tag)
		count_end_tag = len(indexes_start_tag)
		#выбираем минимальное количество, т.к. открывающих и закрывающих тегов может быть разное количество, и цикл while станет бесконечным т.к. не сможет по итогу найти пару
		max_count = min(count_start_tag, count_end_tag)
		#создаем пустой лист и запускаем цикл while, пока количество индексов не станет нужным
		self.indexes = []
		while(len(self.indexes) < max_count): #пока не наберем нужное кол-во индексов
			for i in range(len(indexes_start_tag)): #запускаем цикл перебора списка indexes_start_tag
				for n in range(len(indexes_end_tag)): #запускаем цикл перебора списка indexes_end_tag
					if(indexes_end_tag[n]>indexes_start_tag[i]): #ищем индекс позиции end_tag который больше чем текущая позиция start_tag
						buffer_index_end_tag = n #запоминаем индекс этой позиции у end_tag
						break #как только индекс позиции найден, завершаем цикл перебора списка indexes_end_tag

				if((i+1)<len(indexes_start_tag)): #проверяем существует ли следующий элемент в списке indexes_start_tag
					#если позиция end_tag меньше чем позиция следующего start_tag, то найдена пара - позиции открывающего и закрывающего тегов
					if(indexes_start_tag[i+1] > indexes_end_tag[buffer_index_end_tag]):
						self.indexes.append([indexes_start_tag[i], indexes_end_tag[buffer_index_end_tag]]) #добавляем найденную пару в список indexes
						indexes_start_tag.pop(i) #удаляем найденный элемент из indexes_start_tag
						indexes_end_tag.pop(buffer_index_end_tag) #удаляем найденный элемент из indexes_end_tag
						break #прерываем цикл перебора списка indexes_start_tag
				else: #если следующего элемента в списке indexes_start_tag не существует, то вероятно остался последний тег и его закрывающий тег тоже один
					self.indexes.append([indexes_start_tag[i], indexes_end_tag[buffer_index_end_tag]]) #добавляем найденную пару в список indexes
					indexes_start_tag.pop(i) #удаляем найденный элемент из indexes_start_tag
					indexes_end_tag.pop(buffer_index_end_tag) #удаляем найденный элемент из indexes_end_tag
					break #прерываем цикл перебора списка indexes_start_tag

	# поиск кусков кода подходящих по условию (куски кода начинаются и заканчиваются на <div....</div>)
	def find_all_matches(self, match):
		search_result = []
		for i in range(len(self.indexes)):
			this_string = self.html_code[self.indexes[i][0]:self.indexes[i][1]+6] # +6 потому что длина закрываюещего тега </div> - 6 символов
			if(re.search(match, this_string)):
				search_result.append(this_string)
		return search_result

	def replace(self, string, match, to):
		return re.sub(match, to, string)

	def get_int(self, string):
		return ''.join(x for x in string if x.isdigit())

	#функция для поиска в нужных кусках кода различной информации
	#list_parents список с кусками кода
	#list_matches двумерный список, на втором уровне нулевой элемент - название, первый - сама регулярка, второй это какой кусок пихаем в ответ (какую группу)
	def get_results(self, list_parents, list_matches):
		result_list = []
		result_dict = {}
		for i in range(len(list_parents)):
			for n in range(len(list_matches)):
				find_result = re.search(list_matches[n][1], list_parents[i])
				if(find_result):
					result_dict[list_matches[n][0]] = find_result.group(list_matches[n][2])
				else:
					result_dict[list_matches[n][0]] = 'not_result'
			buffer_dict = result_dict.copy()
			result_list.append(buffer_dict)
			result_dict.clear()
		return result_list

	#функция для поиска индексов по которым находится подстрока
	def find_all_indexes(self, input_str, search_str):
		l1 = []
		length = len(input_str)
		index = 0
		while index < length:
			i = input_str.find(search_str, index)
			if i == -1:
				return l1
			l1.append(i)
			index = i + 1
		return l1