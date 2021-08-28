import json
import sys

from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class MainWindow(QMainWindow):
	def __init__(self, *args, **kwargs):
		super().__init__()
		self.EPOCH = QDateTime()
		self.EPOCH.setTime_t(0)
		self.initUI()

	def initUI(self):
		self.mainCol = QVBoxLayout()

		self.inputRow = QHBoxLayout()

		self.boatNumberInput = QLineEdit()
		self.boatNameInput = QLineEdit()
		self.boatTimeInput = QDateTimeEdit(self.EPOCH)
		self.boatClassInput = QComboBox()
		self.boatSubmit = QPushButton("Submit")


		self.boatTimeInput.setDisplayFormat("h'h' m'm' s's' z'ms'")

		self.boatSubmit.clicked.connect(self.submitBoatTime)

		self.boatNumberInput.setPlaceholderText("Boat Number")
		self.boatNameInput.setPlaceholderText("Boat Name")

		self.handicapData = self.getHandicapData()

		self.boatClassInput.addItem("Boat Class")
		for boatClass in sorted(self.handicapData.keys()):
			self.boatClassInput.addItem(boatClass)
		self.boatClassInput.setCurrentIndex(0)

		self.inputRow.addWidget(self.boatNumberInput)
		self.inputRow.addWidget(self.boatNameInput)
		self.inputRow.addWidget(self.boatTimeInput)
		self.inputRow.addWidget(self.boatClassInput)
		self.inputRow.addWidget(self.boatSubmit)

		self.inputRowWidget = QWidget()
		self.inputRowWidget.setLayout(self.inputRow)

		self.mainCol.addWidget(self.inputRowWidget)

		self.timesTable = QTableWidget()

		self.timesTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.timesTable.setColumnCount(6)
		self.timesTable.setHorizontalHeaderLabels(["Class", "Number", "Name", "PY Number", "Time", "Adjusted Time"])

		self.mainCol.addWidget(self.timesTable)

		self.mainWidget = QWidget()
		self.mainWidget.setLayout(self.mainCol)

		self.setCentralWidget(self.mainWidget)

		self.resize(800, 600)
		self.setWindowTitle("Sailing Handicap Calculator")
		self.show()

	@staticmethod
	def getHandicapData():
		with open("handicaps.json") as f:
			return json.load(f)

	def submitBoatTime(self):
		pyNum = self.handicapData[self.boatClassInput.currentText()]
		originalTime = self.boatTimeInput.dateTime()
		adjustedTime = QDateTime.fromMSecsSinceEpoch(int((self.boatTimeInput.dateTime().toMSecsSinceEpoch() * 1000) / pyNum))
		self.timesTable.insertRow(0)
		self.timesTable.setItem(0, 0, QTableWidgetItem(self.boatClassInput.currentText()))
		self.timesTable.setItem(0, 1, QTableWidgetItem(self.boatNumberInput.text()))
		self.timesTable.setItem(0, 2, QTableWidgetItem(self.boatNameInput.text()))
		self.timesTable.setItem(0, 3, QTableWidgetItem(str(pyNum)))
		self.timesTable.setItem(0, 4, QTableWidgetItem(originalTime.toString("h'h' m'm' s's' z'ms'")))
		self.timesTable.setItem(0, 5, QTableWidgetItem(adjustedTime.toString("h'h' m'm' s's' z'ms'")))

		self.timesTable.sortItems(5, QtCore.Qt.AscendingOrder)

		self.boatNumberInput.clear()
		self.boatNameInput.clear()
		self.boatTimeInput.setDateTime(self.EPOCH)
		# self.boatClassInput.setCurrentIndex(0)


def main(args):
	app = QApplication(args)
	_ = MainWindow()
	sys.exit(app.exec_())


if __name__ == "__main__":
	main(sys.argv)
