'''
File: GameBoardModal.py
Auth: Blake Wingard - bats23456789@gmail.com
Date: 01/09/2024
Desc: The BoardModal of the project.
'''
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QStyleOptionGraphicsItem
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPixmap, QPainter, QColor, QFont, QPen, QColorConstants
from PyQt6.QtCore import QRectF, Qt, QEvent, QPointF, QObject
from itertools import product
from util import linearInterpolateColor
from battleship import Board


class BoardView(QGraphicsView):
    '''
    A class to represent the view of the board
    '''

    def __init__(self, *args, **kwargs):
        '''
        Constructs all the necesarry attributes for the BoardScene object
        '''
        super().__init__(*args, **kwargs)


class GameBoardScene(QGraphicsScene):
    '''
    A class for the scene of the Board

    Attributes
    ----------
    shotColor: QColor
        The color of a shot cell

    idleColor: QColor
        The default color of a cell

    highlightColor: QColor
        The color of a highlighted cell

    labelColor: QColor
        The color of a label

    cornerColor: QColor
        The color of the corner

    highlightShotColor: QColor
        The color of a highlighted cell that's been shot

    bgImage: QPixmap
        The background of the scene

    cells: list[Cell]
        A list of Cells

    board: Board
        The modal of the view

    isLocked: bool
        Determines if a cell is locked in

    lockedPos: int
        The index for the cell that was locked in

    Methods
    -------
    getCellIndex(point): int
        Get the index of a cell that contains the point

    highlightgrid(index)
        Highlights all cells in a row and col for the rectangle in the index

    refreshCells
        Redraw the cells

    shoot
        Fire the shot if a location is selected
    '''

    shotColor = QColorConstants.Red
    idleColor = QColor(49, 149, 202)
    highlightColor = QColor(240, 141, 65)
    labelColor = QColor(194, 194, 194)
    cornerColor = QColorConstants.Black
    highlightShotColor = linearInterpolateColor(highlightColor, shotColor, 0.4)

    def __init__(self, board: Board, *args, **kwargs):
        '''
        Constructs all the necesarry attributes for the BoardScene object

        Parameters
        ----------
        board: Board
            The board to serve as the modal
        '''
        super().__init__(*args, **kwargs)
        self.bgImage = QPixmap('QtResources/images/BoardBackground.jpg')

        # Setup game cells
        sz = self.width() / 11
        coords = product(range(11), range(11))
        rect = QRectF(0, 0, sz, sz)
        self.cells = [Cell(x - 1, y - 1, x == 0 or y == 0, rect) for y, x in coords]

        # Set the properties of the cells
        for i, cell in enumerate(self.cells):
            if not cell.border:
                cell.setBrush(self.idleColor)
                cell.setOpacity(0.8)
            elif i != 0:
                cell.setBrush(self.labelColor)
                cell.setOpacity(1)
            else:
                cell.setBrush(self.cornerColor)
                cell.setOpacity(1)

            cell.setPos((i % 11) * sz, (i // 11) * sz)

            self.addItem(cell)

        self.installEventFilter(self)

        self.board = board
        self.isLocked = False
        self.lockedPos = -1

    def drawBackground(self, painter: QPainter, rect: QRectF):
        '''
        Override for the drawBackground method

        Parameters
        ----------
        painter: QPainter
            The painter for the background

        rect: QRectF
            The rectangle for the scene
        '''
        winSize = rect.size().toSize()
        painter.drawPixmap(0, 0, winSize.width(), winSize.height(), self.bgImage)

    def getCellIndex(self, point: QPointF):
        '''
        Get the index of a cell that contains the point

        Only considers cells not along the border

        Parameters
        ----------
        point: QPointF
            The point used for finding the cell

        Returns
        -------
        int: The index of the cell, or -1
        '''
        for i, cell in enumerate(self.cells):
            x = [cell.pos().x(), cell.pos().x() + cell.rect().width()]
            y = [cell.pos().y(), cell.pos().y() + cell.rect().height()]
            if x[0] <= point.x() <= x[1] and y[0] <= point.y() <= y[1] and not cell.border:
                return i

        return -1

    def eventFilter(self, o: QObject, e: QEvent) -> bool:
        '''
        Override for the eventFilterMethod

        Parameters
        ----------
        o: QObject
            The object sending the event

        e: QEvent
            The event sent

        Returns
        -------
        bool: True if the event was handled
        '''
        if not e:
            return False

        match(e.type()):
            case QEvent.Type.GraphicsSceneMouseMove:
                i = self.getCellIndex(e.scenePos())

                if i == -1 and not self.isLocked:
                    self.refreshCells()
                    self.update()
                    return False

                if not self.isLocked:
                    self.highlightGrid(i)

                self.update()
                return True
            case QEvent.Type.GraphicsSceneLeave:
                if self.isLocked:
                    return True
                self.refreshCells()
                self.update()
                return True
            case QEvent.Type.GraphicsSceneMousePress:
                i = self.getCellIndex(e.scenePos())
                if i == -1:
                    return True

                self.isLocked = True
                self.lockedPos = i
                self.highlightGrid(self.lockedPos)
                self.update()
                return True

        return False

    def highlightGrid(self, index: int):
        '''
        Highlights all cells in a row and col for the rectangle in the index

        Parameters
        ----------
        index: int
            The index of the cell to highlight
        '''
        col = index % 11
        row = index // 11
        for i, rect in enumerate(self.cells):
            if not rect.border:
                if i % 11 == col or i // 11 == row:
                    if self.board.grid[rect.row][rect.col] == 1:
                        color = self.highlightShotColor
                    else:
                        color = self.highlightColor
                elif self.board.grid[rect.row][rect.col] == 1:
                    color = self.shotColor
                else:
                    color = self.idleColor
                rect.setBrush(color)
                rect.update()

    def refreshCells(self):
        '''
        Redraw the cells
        '''
        for i, rect in enumerate(self.cells):
            if not rect.border:
                if self.board.grid[rect.row][rect.col] == 1:
                    color = self.shotColor
                else:
                    color = self.idleColor
                rect.setBrush(color)
                rect.update()

    def shoot(self):
        '''
        Fire the shot if a location is selected
        '''
        if not self.isLocked:
            return

        pos = str(self.cells[self.lockedPos])

        if self.board.isShot(pos):
            return

        self.board.shoot(pos)
        self.cells[self.lockedPos].setBrush(self.shotColor)
        self.isLocked = False
        self.lockedPos = -1
        self.refreshCells()
        self.update()


class Cell(QGraphicsRectItem):
    '''
    A class for representing a cell in the board

    Attributes
    ----------
    font: QFont
        The font of the cell
    '''
    font = QFont('Times', 20, QFont.Weight.Bold)

    def __init__(self, col: int, row: int, isBorder: bool, *args, **kwargs):
        '''
        Constructs all the necesarry attributes for the BoardScene object

        Parameters
        ----------
        col: int
            The col of the cell

        row: int
            The row of the cell

        isBorder: bool
            True if the current cell is a border cell
        '''
        self.row = row
        self.col = col
        self.border = isBorder

        super().__init__(*args, **kwargs)

        self.setAcceptHoverEvents(True)

    def __repr__(self) -> str:
        '''
        Returns the string representation of the Cell
        '''
        if self.border:
            if self.row == self.col:
                return 'X'
            elif self.col == 9:
                return '10'
            elif self.row == -1:
                return chr(self.col + ord('1'))
            else:
                return chr(self.row + ord('A'))
        else:
            return f'{chr(self.row + ord("A"))}{self.col + 1}'

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget = None):
        '''
        Override of the paint method

        Parameters
        ----------
        painter: QPainter
            The painter of the Cell

        option: QStyleOptionGraphicsItem
            The options for the cell

        widget: QWidget
            The widget being painted
        '''
        super().paint(painter, option, widget)
        if self.border and self.row != self.col:
            painter.setFont(self.font)
            painter.setPen(QPen(QColor(0, 0, 0), 10))
            label = self.__repr__()
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, label)
