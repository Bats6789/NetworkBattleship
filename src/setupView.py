from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtCore import Qt
from setupBoardModal import SetupBoardScene
from battleship import Board


class SetupView(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = uic.loadUi('SetupUI.ui', self)
        self.isFullScreen = True

        self.gameBoard = Board()

        self.setWindowState(Qt.WindowState.WindowFullScreen)

        size = self.size()

        self.setFixedSize(size)

        scale = 0.85
        boardSz = int(min(size.width() * scale, size.height() * scale))

        self.board.setFixedSize(boardSz, boardSz)

        scene = SetupBoardScene(self.gameBoard, 0, 0, self.board.width(), self.board.height())
        self.board.setScene(scene)

    def keyPressEvent(self, e: QKeyEvent):
        '''
        Override of the keyPressEvent

        Parameters
        ----------
        e: QKeyEvent
            The event to process
        '''
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
