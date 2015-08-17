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
import sys

from brute import Brute

class MainWindow(QMainWindow):
	"""
		Главное окно приложения
	"""
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)

		self.resize(800, 600)
		self.setWindowTitle(u"""
			Составление "идеального" расписания
			""")

		self.peopleLabel = QLabel(u"Количество человек: ", self)
		self.groupLabel = QLabel(u"Группы по: ", self)
		self.toursLabel = QLabel(u"Количество туров: ", self)

		self.peopleSpin = QSpinBox(self)
		self.peopleSpin.setMinimum(0)

		self.groupSpin = QSpinBox(self)
		self.groupSpin.setMinimum(0)

		self.toursSpin = QSpinBox(self)
		self.toursSpin.setMinimum(0)

		self.calculateButton = QPushButton(u"Вычислить", self)

		self.moduleBox = QComboBox(self)
		self.moduleBox.insertItem(0, u"Brute")

		self.centralWidget = QWidget(self)
		self.grid = QGridLayout()

		self.grid.addWidget(self.peopleLabel, 0, 0)
		self.grid.addWidget(self.peopleSpin, 0, 1)
		self.grid.addWidget(self.groupLabel, 1, 0)
		self.grid.addWidget(self.groupSpin, 1, 1)
		self.grid.addWidget(self.toursLabel, 2, 0)
		self.grid.addWidget(self.toursSpin, 2, 1)
		self.grid.addWidget(self.calculateButton, 3, 0)

		self.centralWidget.setLayout(self.grid)
		self.setCentralWidget(self.centralWidget)

		self.calculateButton.clicked.connect(self.__calculate)

	@Slot()
	def __calculate(self):
		"""
			В общем, структура класса алгоритма должна быть
			понятна -- инициализация с тремя параметрами и метод run()
		"""
		alg = getattr(sys.modules[__name__], self.moduleBox.currentText())(
																			self.peopleSpin.value(),
																			self.toursSpin.value(),
																			self.groupSpin.value()
		)
		alg.run()

if __name__ == "__main__":
	app = QApplication([])
	win = MainWindow()
	win.show()
	app.exec_()