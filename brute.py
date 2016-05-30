# -*- coding: utf-8 -*-

from itertools import permutations, combinations
from algorithm import Algorithm, BadNumbers
import sys

class Brute(Algorithm):
	"""
		Модуль алгоритма полного
		перебора.
	"""
	def __init__(self, n, m, k, funcName):
		super(Brute, self).__init__(n, m, k, funcName)

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

		# теперь нужно склеить их во все возможные
		# варианты для одного тура
		# если одно из возможных сочетаний сочетаний образует
		# исходное множество, тогда оно нам подходит

		# теперь ищем варианты прохождения m туров

		# теперь нужно применить для них целевую функцию
		# и посмотреть на результат

		# здесь я иду по простому пути перебора и
		# хранения промежуточных результатов в памяти.
		# конечно, это наверняка можно оптимизировать
		# и вообще это не python-way, но не время над
		# этим думать
		self._mtrxs = [[[0 for i in self._participants] for j in self._participants] for k in self.__toursCombs()]

		# -----------------------------------
		# print "self._mtrxs: ", self._mtrxs 
		# -----------------------------------


		print "Great cycle..."

		for i in self._participants:
			for j in self._participants:
				for k, combination in enumerate(self.__toursCombs()):
					for schedule in combination:
						for tour in schedule:
							if i != j and i in tour and j in tour:
								self._mtrxs[k][i][j] += 1
								# self._results.append((k, i, j)) # приклеим кортеж найденных индексов для простоты

		print "Done great cycle!"

		# print "n: %s, m: %s, k: %s, RESULTS COUNT: %s"%(self._n, self._m, self._k, len(list(self.__toursCombs())))

		# return []
		return getattr(self, self._funcName)()

	def __toursCombs(self):
		for comb in combinations(self.__oneTourCombsGenerator(), self._m):
			yield comb

	def __combs(self):
		"""
		здесь получится список кортежей возможных групп
		из ВСЕХ элементов, независимо от того, делится
		n на k нацело
		"""
		for comb in combinations(self._participants, self._k):
			yield comb

	def __combCombs(self):
		"""
		теперь нужно склеить их во все возможные
		варианты для одного тура
		"""
		for comb in combinations(self.__combs(), self._totalGroups):
			yield comb

	def __oneTourCombsGenerator(self):
		for comb in self.__combCombs():
			if(sorted(list(reduce(lambda acc, y: acc+y, comb))) == list(self._participants)):
				yield comb

	def __combinationsCount(n,r):
		f = math.factorial
		return xrange(f(n) / f(r) / f(n-r))

	# Целевые функции:

	def maxCollisions(self):
		print "maxCollisions!"
		maxs = []
		for i in self._mtrxs:
			temp = []
			for j in i:
				temp.append(sorted(j)[-1])
			maxs.append(temp)

		res = []
		for i in maxs:
			res.append(max(i))

		return list(list(self.__toursCombs())[res.index(min(res))])

	def sumOfCollisions(self):
		sums = [
			reduce(
					lambda acc, i: acc+i, reduce(
							lambda acc, y: acc+y, x
			))
		for x in self._mtrxs]
		# print list(self._toursCombs)
		return list(list(self.__toursCombs)[sums.index(min(sums))])

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

		return list(list(self.__toursCombs())[res.index(min(res))])	