# -*- coding: utf-8 -*-

from itertools import permutations, combinations
import sys

class Brute():
	"""
		Модуль алгоритма полного
		перебора.
	"""
	def __init__(self, n, m, k, funcName):
		"""
			n -- общее количество участников,
			m -- общее количество туров,
			k -- наибольшее количество участников в группе
		"""
		# придется вычесть единицу, т.к.
		# нумерация, очевидно, с нуля
		if k > n:
			raise BadNumbers("it's too much")
		self._n = n
		self._m = m
		self._k = k
		self._mtrxs = []
		self._toursCombs = []
		self._participants = range(self._n)
		self._funcName = funcName
		if n % k == 0:
			self._totalGroups = n / k
		else:
			self._totalGroups = n // k + 1

	def run(self):

		# if(n % k == 0):
		# 	pass
		# else:
		# 	pass

		# нужно найти все возможные сочетания из n по k,
		# а потом составить из них возможные наборы туров по m

		# здесь получится список кортежей возможных групп
		# из ВСЕХ элементов, независимо от того, делится
		# n на k нацело
		combs = tuple(combinations(self._participants, self._k))

		# теперь нужно склеить их во все возможные
		# варианты для одного тура
		combCombs = list(combinations(combs, self._totalGroups))
		# если одно из возможных сочетаний сочетаний образует
		# исходное множество, тогда оно нам подходит
		check = lambda x: sorted(list(reduce(lambda acc, y: acc+y, x))) == self._participants

		oneTourCombs = filter(check, combCombs)

		# теперь ищем варианты прохождения m туров
		self._toursCombs = list(combinations(oneTourCombs, self._m))

		# теперь нужно применить для них целевую функцию
		# и посмотреть на результат

		# здесь я иду по простому пути перебора и
		# хранения промежуточных результатов в памяти.
		# конечно, это наверняка можно оптимизировать
		# и вообще это не python-way, но не время над
		# этим думать
		self._mtrxs = [[[0 for i in self._participants] for j in self._participants] for k in range(len(self._toursCombs))]

		for i in self._participants:
			for j in self._participants:
				for k, combination in enumerate(self._toursCombs):
					for schedule in combination:
						for tour in schedule:
							if i != j and i in tour and j in tour:
								self._mtrxs[k][i][j] += 1

		res = getattr(self, self._funcName)()
		return res

	def maxCollisions(self):
		maxs = []
		for i in self._mtrxs:
			temp = []
			for j in i:
				temp.append(sorted(j)[-1])
			maxs.append(temp)

		res = []
		for i in maxs:
			res.append(max(i))

		return self._toursCombs[res.index(min(res))]

	def sumOfCollisions(self):
		sums = [
			reduce(
					lambda acc, i: acc+i, reduce(
							lambda acc, y: acc+y, x
			))
		for x in self._mtrxs]
		return self._toursCombs[sums.index(min(sums))]

	def maxOfSums(self):
		sums = []
		for mtrx in self._mtrxs:
			temp = []
			for i in self._participants:
				s = 0
				for j in self._participants:
					if i != j:
						s += mtrx[i][j]
				temp.append(s)
			sums.append(temp)

		res = []
		for i in sums:
			res.append(sorted(i)[-1])

		return self._toursCombs[res.index(min(res))]

		

class BadNumbers(Exception): pass