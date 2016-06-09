# -*- coding: utf-8 -*-
import time, sys

from brute import Brute
from particle_swarm import ParticleSwarm
from smart_insertion import SmartInsertion
from simulated_annealing import SimulatedAnnealing
from genetic_algorithm import GeneticAlgorithm

class AlgorithmTester(object):
	"""
	Класс сравнения работы разных алгоритмов
	"""

	def __init__(self):
		pass

	def run(self, alg_list, n, m, k, funcName):
		"""
		Сюда передается список алгоритмов
		и параметры для проверки, резуль-
		татом будет текстовый вывод
		"""
		result = {}
		for alg_name in alg_list:
			try:
				alg = getattr(sys.modules[__name__], alg_name)(n, m, k, funcName)
			except Exception as e:
				print "Error retrieving %s"%alg_name
				print e

			try:
				start = time.time()
				res = alg.run()
				exec_time = time.time() - start
				print "%s - Time: %.03f s"%(alg_name, exec_time)
				# костыль для отсечения ненужных групп длиной меньше, чем k - 1
				for tour in res:
					if len(tour[-1]) < (k - 1):
						del tour[-1]
				# Положим результат работы алгоритма в словарь под его именем
				result[alg_name] = (alg.function_result, exec_time)
			except Exception as e:
				print "Error running %s"%alg_name
				print e
		for key, value in result.iteritems():
			print "Algorithm: %s, function result = %s, t = %s"%(key, value[0], value[1])


if __name__ == "__main__":
	alg_list = [ "ParticleSwarm", "SmartInsertion", "SimulatedAnnealing", "GeneticAlgorithm"]
	tester = AlgorithmTester()

	tester.run(alg_list, int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])