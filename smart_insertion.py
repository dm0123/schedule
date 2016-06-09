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
6) Вернем расписание. Значение с -- условный минимум функции.
"""

from algorithm import Algorithm, BadNumbers
from metaheuristic import MetaHeuristic
import random, copy

EMPTY = -1


class SmartInsertion(MetaHeuristic):
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
		template = [[[EMPTY for i in xrange(self._k)] for j in xrange(self._totalGroups)] for k in xrange(self._m)]

		# для каждого учатсника перебираем пустышку и выполняем шаги по вставке
		for participant in self._participants:
			for m in xrange(self._m):

				# сюда будем записывать группы, где участник уже был
				in_prev_group_list = []

				collision_groups = []
				# not_collision_groups = []
				# сюда будем записывать группы, где участник еще не был
				candidate_groups = []

				# Condition_1: Вставляем элемент в ту группу, в которой он не был во всех предыдущих турах
				# if participant > 0:
				for i in xrange(m):
					for num, prev_group in enumerate(template[i]):
						if participant in prev_group:
							in_prev_group_list.append(num)
						elif participant > 0 and participant - 1 in prev_group:
							in_prev_group_list.append(num)

				print "in_prev_group_list: %s" % in_prev_group_list

				candidate_groups = filter(lambda x: x not in in_prev_group_list, xrange(self._totalGroups))
				# not_collision_groups = filter(lambda x: x not in collision_groups, xrange(self._totalGroups))
				# print "iteration: %s" % participant
				# print "candidate_groups: %s" % candidate_groups
				# print "TEMPLATE: %s" % template
				# Condition_2: Вставляем элемент в группу с наибольшим количеством свободных мест (нулей)
				nulls = map(lambda x: x.count(EMPTY), template[m])

				# Сложно: находим номер группы, которая есть в кандидатах из первого условия и одновременно
				# максимально свободную
				group_index = -1

				most_empty = nulls.index(max(nulls))

				# если есть группа-кандитат на вставку
				if len(candidate_groups) > 0:
					best_null = 0
					# найдем среди списка групп-кандидатов со свободными местами максимально свободную
					for i, null in enumerate(nulls):
						if i in candidate_groups:
							if best_null < null:
								best_null = null
								group_index = candidate_groups[candidate_groups.index(i)]

					print "len > 0"
				else:
					# если не получается
					collision_count += 1
					print "len < 1"

					# if len(candidate_groups) > 0:
					# 	if most_empty in candidate_groups:
					# 		group_index = most_empty

				if group_index == -1:
					# просто запишем в самый свободный
					
					try:
						group_index = most_empty
					except ValueError:
						pass

				try:
					# найдем индекс первого пустого элемента в группе, которую мы собрались заполнять
					participant_index = template[m][group_index].index(EMPTY)
					# наконец, мы нашли что и чем заполнять
					template[m][group_index][participant_index] = participant
				except Exception as e:
					print "FATAL!"
					print e
					print template[m]
					continue

		self.function_result = getattr(self, self._funcName)(template)

		print "Collision count: %s" % collision_count
		return template
