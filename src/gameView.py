'''
File: gameView.py
Auth: Blake Wingard - bats23456789@gmail.com
Date: 01/05/2024
Desc: The GameView of the project.
'''
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtCore import Qt
from BoardView import BoardScene
from battleship import Board


class GameView(QMainWindow):
    def __init__(self, gameBoard: Board, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = uic.loadUi('GameUI.ui', self)
        self.isFullScreen = True

        self.setWindowState(Qt.WindowState.WindowFullScreen)

        size = self.size()

        self.setFixedSize(size)

        scale = 0.85
        boardSz = int(min(size.width() * scale, size.height() * scale))

        self.board.setFixedSize(boardSz, boardSz)

        scene = BoardScene(gameBoard, 0, 0, self.board.width(), self.board.height())
        self.board.setScene(scene)

        # Connect signals
        self.FireButton.clicked.connect(scene.shoot)

    def keyPressEvent(self, e: QKeyEvent):
        match(e.text()):
            case 'q':
                self.close()
            case 'f':
                if self.isFullScreen:
                    self.setWindowState(Qt.WindowState.WindowMaximized)
                    self.isFullScreen = False
                else:
                    self.setWindowState(Qt.WindowState.WindowFullScreen)
                    self.isFullScreen = True
