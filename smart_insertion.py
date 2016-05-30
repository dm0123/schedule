# -*- coding: utf-8 -*-
"""
1) c := 0
2) Строим расписание, заполненное пустыми элементами (нулями), шаблон, куда мы будем вставлять наших участников
3) Дальше сложнее: заполняем расписание, соблюдая одновременно следующие условия:
    а) Вставляем элемент в ту группу, в которой он не был во всех предыдущих турах
    б) Вставляем элемент в группу с наибольшим количеством свободных мест (нулей)
    в) Вставляем элемент в туре не в ту же группу, что вставили предыдущий элемент (вот насчет этого сомневаюсь)
4) Проверяем значение с в соответсвии с целевой функцией (изначальная версия была прибавим к c единицу, если не выполнилось одно из предыдущих условий)
5) Повторять 2) - 4), пока не переберем все элементы
6) Вернем расписание. Значение с -- минимум функции.
"""

from algorithm import Algorithm, BadNumbers
import random

class SmartInsertion(Algorithm):
	"""
	Алгоритм умной вставки
	собственной разработки
	"""

	def __init__(self, n, m, k, funcName):
		super(SmartInsertion, self).__init__(n, m, k, funcName)

	def run(self):
		# главный счетчик алгоритма (на самом деле, совсем не нужен)
		collision_count = 0

		# генератор пустышки расписаний, которую мы будем заполнять элементами
		template = [[[0 for i in xrange(self._k)] for j in xrange(self._totalGroups)] for k in xrange(self._m)]
		
		# для каждого учатсника перебираем пустышку и выполняем шаги по вставке 
		for participant in self._participants: 
			for m, tour in enumerate(template):

				# сюда будем записывать группы, где участник уже был
				in_prev_group_list = []
				# сюда будем записывать группы, где участник еще не был
				candidate_groups = []

				# Condition_1: Вставляем элемент в ту группу, в которой он не был во всех предыдущих турах
				for i in xrange(m):
					for num, prev_group in enumerate(template):
						if(participant in prev_group):
							in_prev_group_list.append(num)

				candidate_groups = filter(lambda x: x not in in_prev_group_list, xrange(self._totalGroups))
				print "participant: %s, m: %s, tour: %s"%(participant, m, tour)
				# Condition_2: Вставляем элемент в группу с наибольшим количеством свободных мест (нулей)
				nulls = map(lambda x: x.count(0), tour)

				# Сложно: находим номер группы, которая есть в кандидатах из первого условия и одновременно
				# максимально свободную
				try:
					group_index = nulls.index(nulls[max(candidate_groups)])
				except ValueError:
					# если не получается
					collision_count += 1

					# если и первое условие свалилось
					if len(candidate_groups) < 1:
						# просто запишем в самый свободный
						group_index = nulls.index(max(nulls))
					else:
						group_index = random.choice(candidate_groups)

				# найдем индекс первого пустого элемента в группе, которую мы собрались заполнять
				participant_index = template[m][group_index].index(0)
				# наконец, мы нашли что и чем заполнять
				template[m][group_index][participant_index] = participant

		print "Collision count: %s"%collision_count
		return template


