# -*- coding: utf-8 -*-
"""
Метод роя частиц
"""

import math
import sys
import copy
import random
from metaheuristic import MetaHeuristic

MAX_ITERATIONS = 10000
PARTICLES_COUNT = 10
MIN_ERR = 2

def error(position, func):
	# err = 0.0

	# for i, x in enumerate(position):
	# 	for j, y in enumerate(x):
	# 		for k, z in enumerate(y):
	# 			err += position[i][j][k]**2 - (10 * math.cos(2 * math.pi * position[i][j][k])) + 10
	err = func(position)

	return err

class Particle:
	def __init__(self, n, m, k, totalgroups, func):
		self.position = MetaHeuristic.generateRandomSchedule(n, m, k, totalgroups)
		self.velocity = [[[0.0 for i in xrange(k)] for j in xrange(totalgroups)] for k in xrange(m)]
		self.error = error(self.position, func)
		self.best_part_pos = copy.copy(self.position)
		self.best_part_err = self.error

	def check_position(self):
		for i, tour in enumerate(self.position):
			prev_group = []
			for j, group in enumerate(tour):
				if set(group).isdisjoint(group):
					return false
				prev_group = group

		return true



class ParticleSwarm(MetaHeuristic):

	def __init__(self, n, m, k, funcName):
		super(ParticleSwarm, self).__init__(n, m, k, funcName)

	def run(self):
		"""
		Оптимизация методом роя частиц.
		Черт знает как оно вообще будет
		работать, но какой-то результат
		должен получиться.
		"""
		rnd = random.Random(0)
		err_func = getattr(self, self._funcName)

		# накидать в пространстве нужное количество рандомных точек (сейчас они могут попасть в одно и то же место)
		swarm = [Particle(self._n, self._m, self._k, self._totalGroups, err_func) for i in xrange(PARTICLES_COUNT)]

		best_swarm_err = sys.float_info.max # минимальное значение функции ошибки в рое
		# лучшая позиция в рое при такой функции ошибки
		best_swarm_pos = [[[0.0 for i in xrange(self._k)] for j in xrange(self._totalGroups)] for k in xrange(self._m)]

		for i in xrange(PARTICLES_COUNT):
			if swarm[i].error < best_swarm_err:
				best_swarm_err = swarm[i].error
				best_swarm_pos = copy.copy(swarm[i].position)

		iteration = 0
		w = 0.729    # inertia
		c1 = 1.49445 # cognitive (particle)
		c2 = 1.49445 # social (swarm)

		while iteration < MAX_ITERATIONS:

			if iteration % 10 == 0 and iteration > 1:
				print "Iteration = %s "%(str(iteration))
				print " best error = %s"%best_swarm_err

			for particle_index in xrange(PARTICLES_COUNT):
				# высчитать новую скорость для каждой точки

				for i, x in enumerate(swarm[particle_index].velocity):
					for j, y in enumerate(x):
						for k, z in enumerate(y):
							r1 = rnd.random()
							r2 = rnd.random()

							swarm[particle_index].velocity[i][j][k] = ( (w * swarm[particle_index].velocity[i][j][k]) + \
								(c1 * r1 * (swarm[particle_index].best_part_pos[i][j][k] - \
								swarm[particle_index].position[i][j][k])) +  \
								(c2 * r2 * (best_swarm_pos[i][j][k] - \
								swarm[particle_index].position[i][j][k])) )

							if swarm[particle_index].velocity[i][j][k] < 0:
								swarm[i].velocity[i][j][k] = 0
							elif swarm[i].velocity[i][j][k] > self._n:
								swarm[i].velocity[i][j][k] = self._n

							# все числа должны оказываться в пределах от 0 до количества участников
							if swarm[particle_index].position[i][j][k] < 0 or swarm[particle_index].position[i][j][k] > self._n:
								swarm[particle_index].position = swarm[particle_index].best_part_pos
								break

							# прибавим округленную позицию
							swarm[particle_index].position[i][j][k] += swarm[particle_index].velocity[i][j][k]

				if not swarm[particle_index].check_position:
					swarm[particle_index].position = swarm[particle_index].best_part_pos

				# применить целевую функцию к новой позиции
				swarm[particle_index].error = error(swarm[particle_index].position, err_func)

				# проверка лучшая ли позиция сейчас у частицы
				if swarm[particle_index].error < swarm[particle_index].best_part_err:
					swarm[particle_index].best_part_err = swarm[particle_index].error
					swarm[particle_index].best_part_pos = copy.copy(swarm[particle_index].position)

				# проверка лучшая ли у частицы позиция в рое
				if swarm[particle_index].error < best_swarm_err:
					best_swarm_err = swarm[particle_index].error
					best_swarm_pos = copy.copy(swarm[particle_index].position)

			iteration += 1

		for x in best_swarm_pos:
			for y in x:
				for z in y:
					z = round(z)

		self.function_result = best_swarm_err

		return best_swarm_pos