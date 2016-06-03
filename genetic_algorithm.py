# -*- coding: utf-8 -*-

import random
import math
from metaheuristic import MetaHeuristic

"""
Алгоритм мало отличается от имитации отжига (да и от прочих эвристических алгоритмов),
главная суть -- в операциях скрещивания и мутаций. Для простоты оставим только мутации.

Задать целевую функцию (приспособленности) для особей популяции
Создать начальную популяцию
(Начало цикла)
Размножение (скрещивание)
Мутирование
Вычислить значение целевой функции для всех особей
Формирование нового поколения (селекция)
Если выполняются условия остановки, то (конец цикла), иначе (начало цикла).
"""

# Количество особей в нашей популяции мамонтов
# Мамонты? ну они тоже здоровые
MAMMOTH_COUNT = 10

MAX_ITERATION = 1000

class GeneticAlgorithm(MetaHeuristic):
	"""
	Условно генетический алгоритм
	"""
	def __init__(self, n, m, k, funcName):
		super(GeneticAlgorithm, self).__init__(n, m, k, funcName)

	def run(self):
		# Сгенерируем популяцию мамонтов.
		# Тут, конечно, эффективнее было бы воспользоваться генератором, а не запоминать все в памяти
		mammoth_list = [MetaHeuristic.generateRandomSchedule(self._n, self._m, self._k, self._totalGroups) for mammoth in xrange(MAMMOTH_COUNT)]
		# Зададим нашу функцию, которую мы хотим оптимизировать
		optimization_func = getattr(self, self._funcName)

		def sorting_func(x, y):
			"""
			Функция сравнения двух особей
			для сортировки их списка и
			отбрасывания ненужных
			"""
			return cmp(optimization_func(x), optimization_func(y))
		# Дальше ход алгоритма
		for iteration in xrange(MAX_ITERATION):
			print "iteration: %s\n"%iteration
			for mammoth in mammoth_list:
				# self.__crossing() 
				self.__mutation(mammoth)

			# Селекция. Для начала, берем первые 5 лучших
			temp_mammoths = sorted(mammoth_list, cmp=sorting_func)[:5]
			# Прицепим еще 5 рандомных к мутированным
			for i in xrange(5):
				temp_mammoths.append(MetaHeuristic.generateRandomSchedule(self._n, self._m, self._k, self._totalGroups))
			mammoth_list = temp_mammoths

		# Возвращаем лучшую из найденных особей
		return mammoth_list[0]


	def __mutation(self, schedule):
		"""
		Функция мутации особи.
		В случайном туре пере-
		мешаем участников.
		"""
		# tour = random.choice(range(self._m))
		# groups = reduce(lambda acc, x: acc + x, reduce(lambda acc2, y: acc2 + y, schedule[tour]))
		# random.shuffle(groups)
		# schedule[tour] = list(MetaHeuristic.split_list(groups, MetaHeuristic.split_list(self._totalGroups)))
		print "MUTATING: %s\n\n"%schedule

		tour = random.choice(range(self._m))
		group = random.choice(range(self._totalGroups))
		random.shuffle(schedule[tour][group])
		random.shuffle(schedule[tour])

	def __crossing(self, left_schedule, right_schedule):
		"""
		Функция скрещивания двух особей.
		На самом деле, скрещивание имеет
		очень мало смысла, и, если прики-
		нуть, не особо отличается от му-
		таций.
		"""
		pass