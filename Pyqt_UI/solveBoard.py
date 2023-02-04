
import sys
from LS_DP import Board
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import \
    (QApplication, QFileDialog, QGridLayout, QLabel, QMainWindow,
     QMenu, QPushButton, QVBoxLayout, QWidget)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Find the longest consecutive sequence')

        ## Setup the central widget
        widget = QWidget()
        central = QVBoxLayout()
        widget.setLayout(central)
        self.setCentralWidget(widget)

        ## Setup the grid layout
        self.grid = QGridLayout()
        self.grid.setSpacing(1)
        self.grid.setContentsMargins(0,0,0,0)
        central.addLayout(self.grid)

        ## Set the solve button
        button = QPushButton('Solve')
        central.addWidget(button)
        button.clicked.connect(self.solveButtonClicked)

        ## Load the board
        self.board = Board()
        self.loadBoardFromFile(sys.argv[1])
    
        ## Setup the menu bar
        loadAction = QAction('&Load board from CSV', self)
        loadAction.triggered.connect(self.loadBoardDialog)
        self.menuBar().addMenu('&File').addAction(loadAction)

    def loadBoardFromFile(self, filename):
        while self.grid.count()>0:
            self.grid.takeAt(0).widget().deleteLater()
        self.board.load(filename)
        self.resize(40*self.board.ncols, 40+40*self.board.nrows)
        for i in range(self.board.nrows):
            for j in range(self.board.ncols):
                cell = QLabel(self.board.values[i][j])
                cell.setStyleSheet('color: #002d7c;background:white;'
                                   'font-family: Arial; font-size: 14px; font-weight: bold;')
                cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.grid.addWidget(cell, i, j)

    def solveButtonClicked(self, e):
        seq = self.board.getLongestEqualSequence()
        self.board.maskSequence(*seq)
        for i in range(self.board.nrows):
            for j in range(self.board.ncols):
                if self.board.values[i][j]=='#':
                    cell = self.grid.itemAtPosition(i,j).widget()
                    ss = cell.styleSheet().replace('background:white','background:yellow')
                    cell.setStyleSheet(ss)

    def loadBoardDialog(self):
        filename,format = QFileDialog.getOpenFileName(self, 'Load board file', '.', 'CSV File (*.csv)')
        if filename:
            self.loadBoardFromFile(filename)

if __name__=='__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()