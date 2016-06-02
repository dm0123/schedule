# -*- coding: utf-8 -*-
"""
	Главный модуль, содержащий,
	в принципе, весь гуй. К нему
	подцепляются (жутким образом)
	модули с реализованными в них
	классами алгоритмов.
"""

from PySide.QtCore import *
from PySide.QtGui import *
import sys, traceback

from brute import Brute
from particle_swarm import ParticleSwarm
from smart_insertion import SmartInsertion
from simulated_annealing import SimulatedAnnealing

class MainWindow(QMainWindow):
	"""
		Главное окно приложения
	"""
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)

		self.resize(400, 400)
		self.setWindowTitle(u"""
			Составление "идеального" расписания
			""")

		self.peopleLabel = QLabel(u"Количество человек: ", self)
		self.groupLabel = QLabel(u"Группы по: ", self)
		self.toursLabel = QLabel(u"Количество туров: ", self)
		self.functionLabel = QLabel(u"Целевая функция:", self)

		self.peopleSpin = QSpinBox(self)
		self.peopleSpin.setMinimum(0)

		self.groupSpin = QSpinBox(self)
		self.groupSpin.setMinimum(0)

		self.toursSpin = QSpinBox(self)
		self.toursSpin.setMinimum(0)

		self.calculateButton = QPushButton(u"Вычислить", self)

		self._names = {
			u"Полный перебор" 				:	u"Brute",
			u"Метод роя частиц"				:	u"ParticleSwarm",
			u"Умное заполнение"				:	u"SmartInsertion",
			u"Метод имитации отжига"		:	u"SimulatedAnnealing",
			u"Максимальное число вхождений"	:	u"maxCollisions",
			u"Сумма вхождений"				:	u"sumOfCollisions",
			u"Максимальная сумма вхождений"	:	u"maxOfSums"
		}

		self.moduleBox = QComboBox(self)
		self.moduleBox.insertItem(0, u"Полный перебор")
		self.moduleBox.insertItem(1, u"Метод роя частиц")
		self.moduleBox.insertItem(2, u"Умное заполнение")
		self.moduleBox.insertItem(3, u"Метод имитации отжига")

		self.functionBox = QComboBox(self)
		self.functionBox.insertItem(0, u"Максимальное число вхождений")
		self.functionBox.insertItem(1, u"Сумма вхождений")
		self.functionBox.insertItem(2, u"Максимальная сумма вхождений")

		self.centralWidget = QWidget(self)
		self.grid = QGridLayout()

		self.grid.addWidget(self.peopleLabel, 0, 0)
		self.grid.addWidget(self.peopleSpin, 0, 1)
		self.grid.addWidget(self.groupLabel, 1, 0)
		self.grid.addWidget(self.groupSpin, 1, 1)
		self.grid.addWidget(self.toursLabel, 2, 0)
		self.grid.addWidget(self.toursSpin, 2, 1)
		self.grid.addWidget(self.functionLabel, 3, 0)
		self.grid.addWidget(self.functionBox, 3, 1)
		self.grid.addWidget(self.moduleBox, 4, 0)
		self.grid.addWidget(self.calculateButton, 4, 1)

		self.centralWidget.setLayout(self.grid)
		self.setCentralWidget(self.centralWidget)

		self.calculateButton.clicked.connect(self.__calculate)

	@Slot()
	def __calculate(self):
		"""
			В общем, структура класса алгоритма должна быть
			понятна -- инициализация с четыремя параметрами и метод run()
		"""
		alg = getattr(sys.modules[__name__], self._names[self.moduleBox.currentText()])(
																			self.peopleSpin.value(),
																			self.toursSpin.value(),
																			self.groupSpin.value(),
																			self._names[self.functionBox.currentText()]
		)
		try:
			res = alg.run()
		except Exception as e:
			print 'FAIL!'
			exc_type, exc_value, exc_traceback = sys.exc_info()
			traceback.print_tb(exc_traceback)
			QMessageBox.critical(self, "No!", str(e))
			self.close()
			return

		# print res

		with open("output.txt", "w+") as f:
			s = u"==="*20 + u" Найденное расписание " + u"==="*20 + u"\n\n"
			f.write(s.encode('utf-8'))
			for i, x in enumerate(res):
				f.write("Тур № %s\n"%(i+1))
				for j, y in enumerate(x):
					for z in y:
						f.write("%s"%(z+1))
						f.write(' ')
					f.write('\n')
			f.write('\n\n')
		QMessageBox.information(self, "Done!", "Open output.txt!")

if __name__ == "__main__":
	app = QApplication([])
	win = MainWindow()
	win.show()
	app.exec_()