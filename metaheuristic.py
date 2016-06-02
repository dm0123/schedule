# -*- coding: utf-8 -*-

import random
from algorithm import Algorithm, BadNumbers

class MetaHeuristic(Algorithm):

	def __init__(self, n, m, k, funcName):
		super(MetaHeuristic, self).__init__(n, m, k, funcName)

	@staticmethod
	def generateRandomSchedule(n, m, k, totalGroups):
		"""
		Генерация случайного расписания
		"""

		res = []
		tour = []
		while len(res) < m:
			tour = MetaHeuristic.generateRandomTour(n, k, totalGroups)
			if tour not in res:
				res.append(tour)
		return res


	@staticmethod
	def generateRandomTour(n, k, totalGroups):
		"""
		Генерация случайного тура.
		"""

		res = []
		# group = [] 
		# while len(res) < totalGroups:
		# 	group = MetaHeuristic.generateRandomGroup(k)
		# 	check = lambda x: set(x).isdisjoint(group)
		# 	cond = filter(check, res)
		# 	if len(cond) < 1:
		# 		res.append(group)

		participants = range(n)
		random.shuffle(participants)

		res = list(MetaHeuristic.split_list(participants, k))

		return res

	@staticmethod
	def generateRandomGroup(k):
		"""
		Генерация случайной группы фиксированной длины.
		"""

		res = range(k)
		random.shuffle(res)
		return res

	@staticmethod
	def split_list(l, n):
		"""Разбить список l на списки длины n"""
		for i in xrange(0, len(l), n):
			yield l[i:i+n]

	@staticmethod
	def encode_schedule(schedule): pass

	@staticmethod
	def decode_schedule(encoded): pass

	def __getMtrx(self, schedule):
		"""
		Возвращает сколько раз элемент из множества
		участников входил в подмножество с остальными
		элементами
		"""
		mtrx = [[0 for i in self._participants] for j in self._participants]

		for i in self._participants:
			for j in self._participants:
				for tour in schedule:
					for group in tour:
						if i != j and i in group and j in group:
							mtrx[i][j] += 1
		return mtrx

	def maxCollisions(self, schedule):
		"""
		Возвращает максимальное число из
		количества игр одного участника
		с другим
		"""
		maxs = []
		mtrx = self.__getMtrx(schedule)

		for i in mtrx:
			maxs.append(sorted(i)[-1])

		return max(maxs)

	def sumOfCollisions(self, schedule):
		"""
		Метод возращает сумму всех игр
		каждого участника с каждым
		"""

		mtrx = self.__getMtrx(schedule)

		summ = reduce(
					lambda acc, i: acc+i, reduce(
							lambda acc, y: acc+y, mtrx
			))

		return summ

	def maxOfSums(self, schedule):
		"""
		Метод возвращает максимальную
		сумму количества игр одного
		участника с остальными
		"""
		mtrx = self.__getMtrx(schedule) 
		temp = []
		sums = []

		for i in self._participants:
			s = 0
			for j in self._participants:
				if i != j:
					s += mtrx[i][j]
			temp.append(s)
		sums.append(temp)

		return sorted(sums)[-1]
