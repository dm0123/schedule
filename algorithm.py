# -*- coding: utf-8 -*-

class Algorithm(object):
	"""
	Базовый класс для всех алгоритмов.
	Вкратце описывает интерфейс, которого ждет гуй
	"""

	def __init__(self, n, m, k, funcName):
		"""
			n -- общее количество участников,
			m -- общее количество туров,
			k -- наибольшее количество участников в группе
		"""
		if k > n:
			raise BadNumbers("it's too much")
		self._n = n
		self._m = m
		self._k = k
		self._mtrxs = lambda: []
		self._results = []
		self._participants = xrange(self._n)
		self._funcName = funcName
		if n % k == 0:
			self._totalGroups = n / k
		else:
			self._totalGroups = n // k + 1


	def run(self): 
		return []

class BadNumbers(Exception): pass