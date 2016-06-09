# -*- coding: utf-8 -*-

import random
import math
from metaheuristic import MetaHeuristic

# Конечная температура
COOL = 0.001
#  Начальная температура какая-нибудь огромная 
START_TEMPERATURE = 200
# Значение декремента убывающей функции
DECREMENT = 1.0001

MAGIC_CONSTANT = 0.01

"""
1) сравниваем текущее значение F с наилучшим найденным;
	если текущее значение лучше — меняем глобальное наилучшее
2) случайным образом генерируем новое состояние;
	распределение вероятности для него должно зависеть от текущего состояния и текущей температуры
3) вычисляем значение функции для сгенерированной точки
4) принимаем или не принимаем сгенерированное состояние в качестве текущего;
	вероятность этого решения должна зависеть от разности функций сгенерированного и текущего состояний
	и, конечно, от температуры (чем выше температура, тем больше вероятность принять
	состояние хуже текущего)
	если новое состояние не принято, генерируем другое и повторяем действия с третьего пункта,
	если принято — переходим к следующей итерации, понизив температуру
	(но чаще переход к следующему шагу производят в любом случае, чтобы избежать долгого зацикливания)
"""

class SimulatedAnnealing(MetaHeuristic):
	"""
	Алгоритм, схожий с имитацией отжига
	"""
	def __init__(self, n, m, k, funcName):
		super(SimulatedAnnealing, self).__init__(n, m, k, funcName)

	def run(self):
		# Возьмем случайное расписание
		schedule = MetaHeuristic.generateRandomSchedule(self._n, self._m, self._k, self._totalGroups)
		# Обзовем его текущим лучшим
		best_schedule = schedule
		# Зададим начальную температуру
		temperature = START_TEMPERATURE

		# введем распределение вероятности принятия нового состояния
		h = lambda T, delE: 1 / (1 + math.exp(-delE / T));

		# введем функцию понижения температуры
		decrease_temperature = lambda T, iteration: T*math.exp(-DECREMENT * math.pow(iteration, 1/(self._m*self._k)))

		# Зададим нашу функцию, которую мы хотим оптимизировать
		optimization_func = getattr(self, self._funcName)

		best_function_result = 0

		# Пока температура не опустилась, выполняем алгоритм
		iteration = 0
		while temperature > COOL:
			self.__move_to_new_tours(schedule, temperature)

			if optimization_func(schedule) < best_function_result:
				best_schedule = schedule
			else:
				if random.random() > h(temperature, optimization_func(schedule) - best_function_result):
					schedule = best_schedule
				else:
					best_schedule = schedule

			best_function_result = optimization_func(schedule)

			print "best_function_result: %s"%best_function_result

			temperature = decrease_temperature(temperature, iteration)
			print "temperature: %s"%temperature
			iteration += 1

		self.function_result = best_function_result

		return best_schedule


	def __move_to_new_tours(self, schedule, temperature):
		"""
		Функция случайного выбора следующего тура
		на основе текущей вероятности
		TODO: add serious implementation
		"""
		alpha = random.random()

		# на самом деле, поскольку пример алгоритма был для коэффициента движения
		# по доске координаты, то тут он особо не имеет смысла. Поэтому мы на основе
		# коэффициента, раз он зависит от температуры, будем просто принимать решение
		# о генерации нового тура. Конечно, эффективность будет очевидно снижена.
		z = (math.pow((1 + 1/temperature), (2 * alpha - 1)) - 1) * temperature;

		print "ZZZZ: %s\n\n"%z
		tour = random.choice(range(self._m))
		group = random.choice(range(self._totalGroups))
		if z > MAGIC_CONSTANT:
			random.shuffle(schedule[tour][group])
		else:
			schedule = MetaHeuristic.generateRandomSchedule(self._n, self._m, self._k, self._totalGroups) 
